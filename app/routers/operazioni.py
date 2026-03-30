from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix='/operazioni', tags=['Operazioni'])


@router.post('/', response_model=schemas.OperazioneRead, status_code=status.HTTP_201_CREATED)
def crea_operazione(payload: schemas.OperazioneCreate, db: Session = Depends(get_db)):
    if payload.data_operazione < date.today():
        raise HTTPException(status_code=400, detail='La data dell operazione non puo essere nel passato')
    paziente = db.get(models.Paziente, payload.id_paziente)
    if not paziente:
        raise HTTPException(status_code=400, detail='Paziente inesistente')
    medico = db.get(models.Medico, payload.id_medico)
    if not medico:
        raise HTTPException(status_code=400, detail='Medico inesistente')
    reparto = db.get(models.Reparto, payload.id_reparto)
    if not reparto:
        raise HTTPException(status_code=400, detail='Reparto inesistente')
    sede = db.get(models.Sede, payload.id_sede)
    if not sede:
        raise HTTPException(status_code=400, detail='Sede inesistente')
    if reparto.id_sede != payload.id_sede:
        raise HTTPException(status_code=400, detail='Il reparto non appartiene alla sede selezionata')
    if medico.id_reparto != payload.id_reparto:
        raise HTTPException(status_code=400, detail='Il medico non appartiene al reparto selezionato')
    data = payload.model_dump()
    data.setdefault('stato', 'programmata')
    new_item = models.Operazione(**data)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get('/', response_model=List[schemas.OperazioneRead])
def lista(db: Session = Depends(get_db)):
    return db.query(models.Operazione).all()


@router.get('/future', response_model=List[schemas.OperazioneRead])
def future(db: Session = Depends(get_db)):
    return db.query(models.Operazione).filter(models.Operazione.data_operazione >= date.today()).all()


@router.get('/medico/{id_medico}', response_model=List[schemas.OperazioneRead])
def per_medico(id_medico: int, db: Session = Depends(get_db)):
    return db.query(models.Operazione).filter(models.Operazione.id_medico == id_medico).all()


@router.get('/{operazione_id}', response_model=schemas.OperazioneRead)
def leggi(operazione_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Operazione, operazione_id)
    if not item:
        raise HTTPException(status_code=404, detail='Operazione non trovata')
    return item


@router.put('/{operazione_id}', response_model=schemas.OperazioneRead)
def aggiorna_operazione(operazione_id: int, payload: schemas.OperazioneUpdate, db: Session = Depends(get_db)):
    item = db.get(models.Operazione, operazione_id)
    if not item:
        raise HTTPException(status_code=404, detail='Operazione non trovata')
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete('/{operazione_id}', status_code=status.HTTP_204_NO_CONTENT)
def elimina(operazione_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Operazione, operazione_id)
    if not item:
        raise HTTPException(status_code=404, detail='Operazione non trovata')
    db.delete(item)
    db.commit()
    return None
