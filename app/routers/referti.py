from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix='/referti', tags=['Referti'])


@router.post('/', response_model=schemas.RefertoRead, status_code=status.HTTP_201_CREATED)
def crea_referto(payload: schemas.RefertoCreate, db: Session = Depends(get_db)):
    pren = db.get(models.Prenotazione, payload.id_prenotazione)
    if not pren:
        raise HTTPException(status_code=400, detail='Prenotazione inesistente')
    existing = db.query(models.Referto).filter(models.Referto.id_prenotazione == payload.id_prenotazione).first()
    if existing:
        raise HTTPException(status_code=409, detail='Esiste gia un referto per questa prenotazione')
    new_item = models.Referto(**payload.model_dump())
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.get('/', response_model=List[schemas.RefertoRead])
def lista(db: Session = Depends(get_db)):
    return db.query(models.Referto).all()


@router.get('/prenotazione/{id_prenotazione}', response_model=schemas.RefertoRead)
def per_prenotazione(id_prenotazione: int, db: Session = Depends(get_db)):
    ref = db.query(models.Referto).filter(models.Referto.id_prenotazione == id_prenotazione).first()
    if not ref:
        raise HTTPException(status_code=404, detail='Referto non trovato')
    return ref


@router.get('/{referto_id}', response_model=schemas.RefertoRead)
def leggi_referto(referto_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Referto, referto_id)
    if not item:
        raise HTTPException(status_code=404, detail='Referto non trovato')
    return item


@router.put('/{referto_id}', response_model=schemas.RefertoRead)
def aggiorna_referto(referto_id: int, payload: schemas.RefertoUpdate, db: Session = Depends(get_db)):
    item = db.get(models.Referto, referto_id)
    if not item:
        raise HTTPException(status_code=404, detail='Referto non trovato')
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete('/{referto_id}', status_code=status.HTTP_204_NO_CONTENT)
def elimina(referto_id: int, db: Session = Depends(get_db)):
    item = db.get(models.Referto, referto_id)
    if not item:
        raise HTTPException(status_code=404, detail='Referto non trovato')
    db.delete(item)
    db.commit()
    return None
