from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix='/ricoveri', tags=['Ricoveri'])


@router.post('/', response_model=schemas.RicoveroRead, status_code=status.HTTP_201_CREATED)
def crea_ricovero(payload: schemas.RicoveroCreate, db: Session = Depends(get_db)):
    if payload.data_dimissione and payload.data_dimissione < payload.data_ingresso:
        raise HTTPException(status_code=400, detail='La dimissione deve essere successiva alla data di ingresso')
    paziente = db.get(models.Paziente, payload.id_paziente)
    if not paziente:
        raise HTTPException(status_code=400, detail='Paziente inesistente')
    reparto = db.get(models.Reparto, payload.id_reparto)
    if not reparto:
        raise HTTPException(status_code=400, detail='Reparto inesistente')
    sede = db.get(models.Sede, payload.id_sede)
    if not sede:
        raise HTTPException(status_code=400, detail='Sede inesistente')
    if reparto.id_sede != payload.id_sede:
        raise HTTPException(status_code=400, detail='Il reparto non appartiene alla sede selezionata')
    if payload.id_medico_responsabile is not None:
        medico = db.get(models.Medico, payload.id_medico_responsabile)
        if not medico:
            raise HTTPException(status_code=400, detail='Medico responsabile inesistente')
        if medico.id_reparto != payload.id_reparto:
            raise HTTPException(status_code=400, detail='Il medico responsabile non appartiene al reparto selezionato')
    new_item = models.Ricovero(**payload.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get('/', response_model=List[schemas.RicoveroRead])
def lista(db: Session = Depends(get_db)):
    return db.query(models.Ricovero).all()


@router.get('/attivi', response_model=List[schemas.RicoveroRead])
def ricoveri_attivi(db: Session = Depends(get_db)):
    return (
        db.query(models.Ricovero)
        .filter(models.Ricovero.data_dimissione.is_(None))
        .all()
    )


@router.get('/sede/{id_sede}', response_model=List[schemas.RicoveroRead])
def per_sede(id_sede: int, db: Session = Depends(get_db)):
    return db.query(models.Ricovero).filter(models.Ricovero.id_sede == id_sede).all()


@router.get('/{ricovero_id}', response_model=schemas.RicoveroRead)
def leggi(ricovero_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Ricovero, ricovero_id)
    if not item:
        raise HTTPException(status_code=404, detail='Ricovero non trovato')
    return item


@router.put('/{ricovero_id}', response_model=schemas.RicoveroRead)
def aggiorna_ricovero(ricovero_id: int, payload: schemas.RicoveroUpdate, db: Session = Depends(get_db)):
    item = db.get(models.Ricovero, ricovero_id)
    if not item:
        raise HTTPException(status_code=404, detail='Ricovero non trovato')
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete('/{ricovero_id}', status_code=status.HTTP_204_NO_CONTENT)
def elimina(ricovero_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Ricovero, ricovero_id)
    if not item:
        raise HTTPException(status_code=404, detail='Ricovero non trovato')
    db.delete(item)
    db.commit()
    return None
