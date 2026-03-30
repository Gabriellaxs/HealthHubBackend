from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix='/pazienti',
    tags=['Pazienti'],
)


@router.post('/', response_model=schemas.PazienteRead, status_code=status.HTTP_201_CREATED)
def crea_paziente(paziente: schemas.PazienteCreate, db: Session = Depends(get_db)):
    nuovo_paziente = models.Paziente(**paziente.dict())
    db.add(nuovo_paziente)
    db.commit()
    db.refresh(nuovo_paziente)
    return nuovo_paziente


@router.get('/', response_model=List[schemas.PazienteRead])
def lista_pazienti(db: Session = Depends(get_db)):
    return db.query(models.Paziente).all()


@router.get('/{paziente_id}', response_model=schemas.PazienteRead)
def leggi_paziente(paziente_id: int, db: Session = Depends(get_db)):
    paziente = db.query(models.Paziente).get(paziente_id)
    if not paziente:
        raise HTTPException(status_code=404, detail='Paziente non trovato')
    return paziente


@router.put('/{paziente_id}', response_model=schemas.PazienteRead)
def aggiorna_paziente(paziente_id: int, payload: schemas.PazienteUpdate, db: Session = Depends(get_db)):
    paziente = db.query(models.Paziente).get(paziente_id)
    if not paziente:
        raise HTTPException(status_code=404, detail='Paziente non trovato')
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(paziente, field, value)
    db.commit()
    db.refresh(paziente)
    return paziente


@router.delete('/{paziente_id}', status_code=status.HTTP_204_NO_CONTENT)
def elimina_paziente(paziente_id: int, db: Session = Depends(get_db)):
    paziente = db.query(models.Paziente).get(paziente_id)
    if not paziente:
        raise HTTPException(status_code=404, detail='Paziente non trovato')
    db.delete(paziente)
    db.commit()
    return None
