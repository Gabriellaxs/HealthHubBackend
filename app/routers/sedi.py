from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/sedi",
    tags=["Sedi"],
)

# CREA SEDE
@router.post("/", response_model=schemas.SedeRead, status_code=status.HTTP_201_CREATED)
def crea_sede(sede: schemas.SedeCreate, db: Session = Depends(get_db)):
    nuova_sede = models.Sede(**sede.dict())
    db.add(nuova_sede)
    db.commit()
    db.refresh(nuova_sede)
    return nuova_sede


# LISTA SEDI
@router.get("/", response_model=List[schemas.SedeRead])
def lista_sedi(db: Session = Depends(get_db)):
    return db.query(models.Sede).all()


# DETTAGLIO SEDE
@router.get("/{sede_id}", response_model=schemas.SedeRead)
def dettaglio_sede(sede_id: int, db: Session = Depends(get_db)):
    sede = db.query(models.Sede).get(sede_id)
    if not sede:
        raise HTTPException(status_code=404, detail="Sede non trovata")
    return sede


# AGGIORNA SEDE
@router.put("/{sede_id}", response_model=schemas.SedeRead)
def aggiorna_sede(sede_id: int, sede: schemas.SedeCreate, db: Session = Depends(get_db)):
    sede_db = db.query(models.Sede).get(sede_id)

    if not sede_db:
        raise HTTPException(status_code=404, detail="Sede non trovata")

    for key, value in sede.dict().items():
        setattr(sede_db, key, value)

    db.commit()
    db.refresh(sede_db)
    return sede_db


# ELIMINA SEDE
@router.delete("/{sede_id}", status_code=status.HTTP_204_NO_CONTENT)
def elimina_sede(sede_id: int, db: Session = Depends(get_db)):
    sede = db.query(models.Sede).get(sede_id)

    if not sede:
        raise HTTPException(status_code=404, detail="Sede non trovata")

    db.delete(sede)
    db.commit()
    return None
