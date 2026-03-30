from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/prestazioni",
    tags=["Prestazioni"],
)


# CREA PRESTAZIONE
@router.post("/", response_model=schemas.PrestazioneRead, status_code=status.HTTP_201_CREATED)
def crea_prestazione(prestazione: schemas.PrestazioneCreate, db: Session = Depends(get_db)):

    nuova_prestazione = models.Prestazione(**prestazione.dict())
    db.add(nuova_prestazione)
    db.commit()
    db.refresh(nuova_prestazione)

    return nuova_prestazione


# LISTA PRESTAZIONI
@router.get("/", response_model=List[schemas.PrestazioneRead])
def lista_prestazioni(db: Session = Depends(get_db)):
    return db.query(models.Prestazione).all()


# DETTAGLIO PRESTAZIONE
@router.get("/{prestazione_id}", response_model=schemas.PrestazioneRead)
def dettaglio_prestazione(prestazione_id: int, db: Session = Depends(get_db)):
    prestazione = db.query(models.Prestazione).get(prestazione_id)

    if not prestazione:
        raise HTTPException(status_code=404, detail="Prestazione non trovata")

    return prestazione


# ELIMINA PRESTAZIONE
@router.delete("/{prestazione_id}", status_code=status.HTTP_204_NO_CONTENT)
def elimina_prestazione(prestazione_id: int, db: Session = Depends(get_db)):
    prestazione = db.query(models.Prestazione).get(prestazione_id)

    if not prestazione:
        raise HTTPException(status_code=404, detail="Prestazione non trovata")

    db.delete(prestazione)
    db.commit()
    return None
# AGGIORNA PRESTAZIONE
@router.put("/{prestazione_id}", response_model=schemas.PrestazioneRead)        
def aggiorna_prestazione(prestazione_id: int, prestazione: schemas.PrestazioneCreate, db: Session = Depends(get_db)):
    prestazione_db = db.query(models.Prestazione).get(prestazione_id)

    if not prestazione_db:
        raise HTTPException(status_code=404, detail="Prestazione non trovata")

    for key, value in prestazione.dict().items():
        setattr(prestazione_db, key, value)

    db.commit()
    db.refresh(prestazione_db)

    return prestazione_db