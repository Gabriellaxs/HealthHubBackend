from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import models, schemas
from ..database import get_db


router = APIRouter(
    prefix='/prenotazioni',
    tags=['Prenotazioni'],
)


@router.post('/', response_model=schemas.PrenotazioneRead, status_code=status.HTTP_201_CREATED)
def crea_prenotazione(prenotazione: schemas.PrenotazioneCreate, db: Session = Depends(get_db)):
    if prenotazione.data_visita < date.today():
        raise HTTPException(status_code=400, detail='La data della visita non puo essere nel passato')
    paziente = db.get(models.Paziente, prenotazione.id_paziente)
    if not paziente:
        raise HTTPException(status_code=400, detail='Paziente inesistente')
    medico = db.get(models.Medico, prenotazione.id_medico)
    if not medico:
        raise HTTPException(status_code=400, detail='Medico inesistente')
    prestazione = db.get(models.Prestazione, prenotazione.id_prestazione)
    if not prestazione:
        raise HTTPException(status_code=400, detail='Prestazione inesistente')
    sede = db.get(models.Sede, prenotazione.id_sede)
    if not sede:
        raise HTTPException(status_code=400, detail='Sede inesistente')
    if medico.reparto.id_sede != prenotazione.id_sede:
        raise HTTPException(status_code=400, detail='Il medico non appartiene a un reparto della sede selezionata')
    conflict = (
        db.query(models.Prenotazione)
        .filter(
            models.Prenotazione.id_medico == prenotazione.id_medico,
            models.Prenotazione.data_visita == prenotazione.data_visita,
            models.Prenotazione.ora_visita == prenotazione.ora_visita,
        )
        .first()
    )
    if conflict:
        raise HTTPException(status_code=409, detail='Il medico ha gia una prenotazione in questo slot')
    nuova_prenotazione = models.Prenotazione(**prenotazione.model_dump())
    db.add(nuova_prenotazione)
    db.commit()
    db.refresh(nuova_prenotazione)
    return nuova_prenotazione


@router.get('/', response_model=List[schemas.PrenotazioneRead])
def lista_prenotazioni(db: Session = Depends(get_db)):
    return db.query(models.Prenotazione).all()


@router.get('/paziente/{id_paziente}', response_model=List[schemas.PrenotazioneRead])
def prenotazioni_per_paziente(id_paziente: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Prenotazione)
        .filter(models.Prenotazione.id_paziente == id_paziente)
        .all()
    )


@router.get('/{prenotazione_id}', response_model=schemas.PrenotazioneRead)
def dettaglio_prenotazione(prenotazione_id: int, db: Session = Depends(get_db)):
    pren = db.get(models.Prenotazione, prenotazione_id)
    if not pren:
        raise HTTPException(status_code=404, detail='Prenotazione non trovata')
    return pren


@router.put('/{prenotazione_id}', response_model=schemas.PrenotazioneRead)
def aggiorna_prenotazione(prenotazione_id: int, payload: schemas.PrenotazioneUpdate, db: Session = Depends(get_db)):
    pren = db.get(models.Prenotazione, prenotazione_id)
    if not pren:
        raise HTTPException(status_code=404, detail='Prenotazione non trovata')
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(pren, field, value)
    db.commit()
    db.refresh(pren)
    return pren


@router.delete('/{prenotazione_id}', status_code=status.HTTP_204_NO_CONTENT)
def elimina_prenotazione(prenotazione_id: int, db: Session = Depends(get_db)):
    pren = db.get(models.Prenotazione, prenotazione_id)
    if not pren:
        raise HTTPException(status_code=404, detail='Prenotazione non trovata')
    db.delete(pren)
    db.commit()
    return None
