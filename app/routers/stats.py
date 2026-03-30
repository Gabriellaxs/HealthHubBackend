from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, distinct
from datetime import date

from ..database import get_db
from .. import models

router = APIRouter(prefix="/stats", tags=["Dashboard"])


@router.get("/totale_pazienti")
def totale_pazienti(db: Session = Depends(get_db)):
    return {"totale_pazienti": db.query(func.count(models.Paziente.id)).scalar()}


@router.get("/prenotazioni_oggi")
def prenotazioni_oggi(db: Session = Depends(get_db)):
    today = date.today()
    n = db.query(func.count(models.Prenotazione.id)).filter(models.Prenotazione.data_visita == today).scalar()
    return {"data": str(today), "prenotazioni_oggi": n}


@router.get("/prenotazioni_future")
def prenotazioni_future(db: Session = Depends(get_db)):
    today = date.today()
    n = db.query(func.count(models.Prenotazione.id)).filter(models.Prenotazione.data_visita > today).scalar()
    return {"da_data": str(today), "prenotazioni_future": n}


@router.get("/ricoveri_attivi")
def ricoveri_attivi(db: Session = Depends(get_db)):
    n = db.query(func.count(models.Ricovero.id)).filter(models.Ricovero.data_dimissione.is_(None)).scalar()
    return {"ricoveri_attivi": n}


@router.get("/operazioni_programmate")
def operazioni_programmate(db: Session = Depends(get_db)):
    today = date.today()
    n = db.query(func.count(models.Operazione.id)).filter(models.Operazione.data_operazione >= today).scalar()
    return {"da_data": str(today), "operazioni_programmate": n}


@router.get("/teleconsulenze_future")
def teleconsulenze_future(db: Session = Depends(get_db)):
    today = date.today()
    n = db.query(func.count(models.Teleconsulenza.id)).filter(models.Teleconsulenza.data >= today).scalar()
    return {"da_data": str(today), "teleconsulenze_future": n}


@router.get("/pazienti_unici_per_sede")
def pazienti_unici_per_sede(db: Session = Depends(get_db)):
    rows = (
        db.query(models.Sede.id, models.Sede.nome, func.count(distinct(models.Prenotazione.id_paziente)))
        .join(models.Prenotazione, models.Prenotazione.id_sede == models.Sede.id, isouter=True)
        .group_by(models.Sede.id)
        .all()
    )
    return [{"id_sede": r[0], "sede": r[1], "pazienti_unici": r[2]} for r in rows]


@router.get("/prenotazioni_per_sede")
def prenotazioni_per_sede(db: Session = Depends(get_db)):
    rows = (
        db.query(models.Sede.id, models.Sede.nome, func.count(models.Prenotazione.id))
        .join(models.Prenotazione, models.Prenotazione.id_sede == models.Sede.id, isouter=True)
        .group_by(models.Sede.id)
        .all()
    )
    return [{"id_sede": r[0], "sede": r[1], "prenotazioni": r[2]} for r in rows]


@router.get("/top5_medici_operazioni")
def top5_medici_operazioni(db: Session = Depends(get_db)):
    rows = (
        db.query(models.Medico.id, models.Medico.nome, models.Medico.cognome, func.count(models.Operazione.id).label("tot"))
        .join(models.Operazione, models.Operazione.id_medico == models.Medico.id, isouter=True)
        .group_by(models.Medico.id)
        .order_by(func.count(models.Operazione.id).desc())
        .limit(5)
        .all()
    )
    return [{"id_medico": r[0], "nome": r[1], "cognome": r[2], "operazioni": r[3]} for r in rows]


@router.get("/prestazioni_piu_richieste")
def prestazioni_piu_richieste(db: Session = Depends(get_db)):
    rows = (
        db.query(models.Prestazione.id, models.Prestazione.nome, func.count(models.Prenotazione.id).label("tot"))
        .join(models.Prenotazione, models.Prenotazione.id_prestazione == models.Prestazione.id, isouter=True)
        .group_by(models.Prestazione.id)
        .order_by(func.count(models.Prenotazione.id).desc())
        .all()
    )
    return [{"id_prestazione": r[0], "prestazione": r[1], "prenotazioni": r[2]} for r in rows]
