from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from ..utils import get_db, require_admin

router = APIRouter(prefix="/vaccines", tags=["Vaccines"])

# GET all vaccines
@router.get("/", response_model=list[schemas.VaccineOut])
def get_vaccines(db: Session = Depends(get_db)):
    return db.query(models.Vaccine).all()

# HEAD vaccine
@router.head("/{vaccine_id}")
def head_vaccine(vaccine_id: int, db: Session = Depends(get_db)):
    exists = db.query(models.Vaccine).filter(models.Vaccine.id == vaccine_id).first()
    if not exists:
        raise HTTPException(status_code=404)
    return Response(status_code=200)

# GET vaccine by ID
@router.get("/{vaccine_id}", response_model=schemas.VaccineOut)
def get_vaccine(vaccine_id: int, db: Session = Depends(get_db)):
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    return vaccine

# POST vaccine (admin only)
@router.post("/", response_model=schemas.VaccineOut)
def create_vaccine(vaccine: schemas.VaccineCreate, db: Session = Depends(get_db),
                   admin: models.User = Depends(require_admin)):
    exists = db.query(models.Vaccine).filter(models.Vaccine.name == vaccine.name).first()
    if exists:
        raise HTTPException(status_code=400, detail="Vaccine already exists")
    new_vaccine = models.Vaccine(**vaccine.dict())
    db.add(new_vaccine)
    db.commit()
    db.refresh(new_vaccine)
    return new_vaccine

# PATCH vaccine (admin only)
@router.patch("/{vaccine_id}", response_model=schemas.VaccineOut)
def update_vaccine(vaccine_id: int, vaccine: schemas.VaccineCreate, db: Session = Depends(get_db),
                   admin: models.User = Depends(require_admin)):
    db_vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == vaccine_id).first()
    if not db_vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    for key, value in vaccine.dict(exclude_unset=True).items():
        setattr(db_vaccine, key, value)
    db.commit()
    db.refresh(db_vaccine)
    return db_vaccine

# DELETE vaccine (admin only)
@router.delete("/{vaccine_id}", status_code=204)
def delete_vaccine(vaccine_id: int, db: Session = Depends(get_db),
                   admin: models.User = Depends(require_admin)):
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    if vaccine.appointments or vaccine.vaccinations:
        raise HTTPException(status_code=400, detail="Cannot delete vaccine linked to appointments or vaccinations")
    db.delete(vaccine)
    db.commit()
    return Response(status_code=204)
