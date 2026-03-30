from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix='/medici',
    tags=['Medici'],
)


@router.post('/', response_model=schemas.MedicoRead, status_code=status.HTTP_201_CREATED)
def crea_medico(medico: schemas.MedicoCreate, db: Session = Depends(get_db)):
    nuovo_medico = models.Medico(**medico.dict())
    db.add(nuovo_medico)
    db.commit()
    db.refresh(nuovo_medico)
    return nuovo_medico


@router.get('/', response_model=List[schemas.MedicoRead])
def lista_medici(db: Session = Depends(get_db)):
    return db.query(models.Medico).all()


@router.get('/{medico_id}', response_model=schemas.MedicoRead)
def dettaglio_medico(medico_id: int, db: Session = Depends(get_db)):
    medico = db.query(models.Medico).get(medico_id)
    if not medico:
        raise HTTPException(status_code=404, detail='Medico non trovato')
    return medico


@router.put('/{medico_id}', response_model=schemas.MedicoRead)
def aggiorna_medico(medico_id: int, payload: schemas.MedicoUpdate, db: Session = Depends(get_db)):
    medico = db.query(models.Medico).get(medico_id)
    if not medico:
        raise HTTPException(status_code=404, detail='Medico non trovato')
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(medico, field, value)
    db.commit()
    db.refresh(medico)
    return medico


@router.delete('/{medico_id}', status_code=status.HTTP_204_NO_CONTENT)
def elimina_medico(medico_id: int, db: Session = Depends(get_db)):
    medico = db.query(models.Medico).get(medico_id)
    if not medico:
        raise HTTPException(status_code=404, detail='Medico non trovato')
    db.delete(medico)
    db.commit()
    return None
