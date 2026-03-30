from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/reparti",
    tags=["Reparti"],
)

# CREA REPARTO
@router.post("/", response_model=schemas.RepartoRead, status_code=status.HTTP_201_CREATED)
def crea_reparto(reparto: schemas.RepartoCreate, db: Session = Depends(get_db)):

    # Controllo che la sede esista
    sede = db.query(models.Sede).get(reparto.id_sede)
    if not sede:
        raise HTTPException(status_code=400, detail="Sede non trovata")

    nuovo_reparto = models.Reparto(**reparto.dict())
    db.add(nuovo_reparto)
    db.commit()
    db.refresh(nuovo_reparto)
    return nuovo_reparto


# LISTA REPARTI
@router.get("/", response_model=List[schemas.RepartoRead])
def lista_reparti(db: Session = Depends(get_db)):
    return db.query(models.Reparto).all()


# DETTAGLIO REPARTO
@router.get("/{reparto_id}", response_model=schemas.RepartoRead)
def dettaglio_reparto(reparto_id: int, db: Session = Depends(get_db)):
    reparto = db.query(models.Reparto).get(reparto_id)
    if not reparto:
        raise HTTPException(status_code=404, detail="Reparto non trovato")
    return reparto


# AGGIORNA REPARTO
@router.put("/{reparto_id}", response_model=schemas.RepartoRead)
def aggiorna_reparto(reparto_id: int, reparto: schemas.RepartoCreate, db: Session = Depends(get_db)):
    reparto_db = db.query(models.Reparto).get(reparto_id)
    if not reparto_db:
        raise HTTPException(status_code=404, detail="Reparto non trovato")

    for key, value in reparto.dict().items():
        setattr(reparto_db, key, value)

    db.commit()
    db.refresh(reparto_db)
    return reparto_db


# ELIMINA REPARTO
@router.delete("/{reparto_id}", status_code=status.HTTP_204_NO_CONTENT)
def elimina_reparto(reparto_id: int, db: Session = Depends(get_db)):
    reparto = db.query(models.Reparto).get(reparto_id)
    if not reparto:
        raise HTTPException(status_code=404, detail="Reparto non trovato")

    db.delete(reparto)
    db.commit()
    return None
