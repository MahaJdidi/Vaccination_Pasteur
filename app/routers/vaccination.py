from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from ..utils import get_db, require_admin

router = APIRouter(prefix="/vaccinations", tags=["Vaccinations"])

# GET all vaccinations
@router.get("/", response_model=list[schemas.VaccinationOut])
def get_vaccinations(db: Session = Depends(get_db)):
    return db.query(models.Vaccination).all()

# HEAD vaccination
@router.head("/{vaccination_id}")
def head_vaccination(vaccination_id: int, db: Session = Depends(get_db)):
    exists = db.query(models.Vaccination).filter(models.Vaccination.id == vaccination_id).first()
    if not exists:
        raise HTTPException(status_code=404)
    return Response(status_code=200)

# GET vaccination by ID
@router.get("/{vaccination_id}", response_model=schemas.VaccinationOut)
def get_vaccination(vaccination_id: int, db: Session = Depends(get_db)):
    vaccination = db.query(models.Vaccination).filter(models.Vaccination.id == vaccination_id).first()
    if not vaccination:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    return vaccination

# POST vaccination (admin only)
@router.post("/", response_model=schemas.VaccinationOut)
def create_vaccination(vaccination: schemas.VaccinationCreate, db: Session = Depends(get_db),
                       admin: models.User = Depends(require_admin)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == vaccination.appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    new_vaccination = models.Vaccination(**vaccination.dict(), admin_id=admin.id)
    db.add(new_vaccination)
    db.commit()
    db.refresh(new_vaccination)
    return new_vaccination

# PATCH vaccination (admin only)
@router.patch("/{vaccination_id}", response_model=schemas.VaccinationOut)
def update_vaccination(vaccination_id: int, vaccination: schemas.VaccinationCreate, db: Session = Depends(get_db),
                       admin: models.User = Depends(require_admin)):
    db_vacc = db.query(models.Vaccination).filter(models.Vaccination.id == vaccination_id).first()
    if not db_vacc:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    for key, value in vaccination.dict(exclude_unset=True).items():
        setattr(db_vacc, key, value)
    db.commit()
    db.refresh(db_vacc)
    return db_vacc

# DELETE vaccination (admin only)
@router.delete("/{vaccination_id}", status_code=204)
def delete_vaccination(vaccination_id: int, db: Session = Depends(get_db),
                       admin: models.User = Depends(require_admin)):
    vacc = db.query(models.Vaccination).filter(models.Vaccination.id == vaccination_id).first()
    if not vacc:
        raise HTTPException(status_code=404, detail="Vaccination not found")
    db.delete(vacc)
    db.commit()
    return Response(status_code=204)
