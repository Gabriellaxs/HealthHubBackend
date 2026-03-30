from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix='/teleconsulenze', tags=['Teleconsulenze'])


@router.post('/', response_model=schemas.TeleconsulenzaRead, status_code=status.HTTP_201_CREATED)
def crea_teleconsulenza(payload: schemas.TeleconsulenzaCreate, db: Session = Depends(get_db)):
    if payload.data < date.today():
        raise HTTPException(status_code=400, detail='La data della teleconsulenza non puo essere nel passato')
    paziente = db.get(models.Paziente, payload.id_paziente)
    if not paziente:
        raise HTTPException(status_code=400, detail='Paziente inesistente')
    medico = db.get(models.Medico, payload.id_medico)
    if not medico:
        raise HTTPException(status_code=400, detail='Medico inesistente')
    conflict = (
        db.query(models.Teleconsulenza)
        .filter(
            models.Teleconsulenza.id_medico == payload.id_medico,
            models.Teleconsulenza.data == payload.data,
            models.Teleconsulenza.ora == payload.ora,
        )
        .first()
    )
    if conflict:
        raise HTTPException(status_code=409, detail='Teleconsulenza duplicata per lo stesso medico nello stesso slot')
    new_item = models.Teleconsulenza(**payload.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get('/', response_model=List[schemas.TeleconsulenzaRead])
def lista(db: Session = Depends(get_db)):
    return db.query(models.Teleconsulenza).all()


@router.get('/medico/{id_medico}', response_model=List[schemas.TeleconsulenzaRead])
def per_medico(id_medico: int, db: Session = Depends(get_db)):
    return db.query(models.Teleconsulenza).filter(models.Teleconsulenza.id_medico == id_medico).all()


@router.get('/paziente/{id_paziente}', response_model=List[schemas.TeleconsulenzaRead])
def per_paziente(id_paziente: int, db: Session = Depends(get_db)):
    return db.query(models.Teleconsulenza).filter(models.Teleconsulenza.id_paziente == id_paziente).all()


@router.get('/{teleconsulenza_id}', response_model=schemas.TeleconsulenzaRead)
def leggi(teleconsulenza_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Teleconsulenza, teleconsulenza_id)
    if not item:
        raise HTTPException(status_code=404, detail='Teleconsulenza non trovata')
    return item


@router.put('/{teleconsulenza_id}', response_model=schemas.TeleconsulenzaRead)
def aggiorna_teleconsulenza(teleconsulenza_id: int, payload: schemas.TeleconsulenzaUpdate, db: Session = Depends(get_db)):
    item = db.get(models.Teleconsulenza, teleconsulenza_id)
    if not item:
        raise HTTPException(status_code=404, detail='Teleconsulenza non trovata')
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete('/{teleconsulenza_id}', status_code=status.HTTP_204_NO_CONTENT)
def elimina(teleconsulenza_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Teleconsulenza, teleconsulenza_id)
    if not item:
        raise HTTPException(status_code=404, detail='Teleconsulenza non trovata')
    db.delete(item)
    db.commit()
    return None
