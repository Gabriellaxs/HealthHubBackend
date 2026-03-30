from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix='/turni', tags=['Turni'])


@router.post('/', response_model=schemas.TurnoRead, status_code=status.HTTP_201_CREATED)
def crea_turno(payload: schemas.TurnoCreate, db: Session = Depends(get_db)):
    medico = db.get(models.Medico, payload.id_medico)
    if not medico:
        raise HTTPException(status_code=400, detail='Medico inesistente')
    sede = db.get(models.Sede, payload.id_sede)
    if not sede:
        raise HTTPException(status_code=400, detail='Sede inesistente')
    if payload.ora_fine <= payload.ora_inizio:
        raise HTTPException(status_code=400, detail='Ora fine deve essere successiva a ora inizio')
    new_item = models.Turno(**payload.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get('/', response_model=List[schemas.TurnoRead])
def lista(db: Session = Depends(get_db)):
    return db.query(models.Turno).all()


@router.get('/medico/{id_medico}', response_model=List[schemas.TurnoRead])
def per_medico(id_medico: int, db: Session = Depends(get_db)):
    return db.query(models.Turno).filter(models.Turno.id_medico == id_medico).all()


@router.get('/{turno_id}', response_model=schemas.TurnoRead)
def leggi(turno_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Turno, turno_id)
    if not item:
        raise HTTPException(status_code=404, detail='Turno non trovato')
    return item


@router.put('/{turno_id}', response_model=schemas.TurnoRead)
def aggiorna_turno(turno_id: int, payload: schemas.TurnoUpdate, db: Session = Depends(get_db)):
    item = db.get(models.Turno, turno_id)
    if not item:
        raise HTTPException(status_code=404, detail='Turno non trovato')
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete('/{turno_id}', status_code=status.HTTP_204_NO_CONTENT)
def elimina(turno_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Turno, turno_id)
    if not item:
        raise HTTPException(status_code=404, detail='Turno non trovato')
    db.delete(item)
    db.commit()
    return None
