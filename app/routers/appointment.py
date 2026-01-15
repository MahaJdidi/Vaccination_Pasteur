from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import SessionLocal
from ..utils import get_db, require_admin, require_citizen

router = APIRouter(prefix="/appointments", tags=["Appointments"])

# GET all appointments
@router.get("/", response_model=list[schemas.AppointmentOut])
def get_appointments(db: Session = Depends(get_db)):
    return db.query(models.Appointment).all()

# HEAD appointment
@router.head("/{appointment_id}")
def head_appointment(appointment_id: int, db: Session = Depends(get_db)):
    exists = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not exists:
        raise HTTPException(status_code=404)
    return Response(status_code=200)

# GET appointment by ID
@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

# POST appointment (citizen only)
@router.post("/", response_model=schemas.AppointmentOut)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db),
                       citizen: models.User = Depends(require_citizen)):
    if appointment.citizen_id != citizen.id:
        raise HTTPException(status_code=403, detail="You can only book for yourself")
    vaccine = db.query(models.Vaccine).filter(models.Vaccine.id == appointment.vaccine_id).first()
    if not vaccine:
        raise HTTPException(status_code=404, detail="Vaccine not found")
    new_appointment = models.Appointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

# PATCH appointment status (admin only)
@router.patch("/{appointment_id}/status", response_model=schemas.AppointmentOut)
def update_appointment_status(appointment_id: int, status: str, reason_rejection: str = None,
                              db: Session = Depends(get_db), admin: models.User = Depends(require_admin)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if status not in ["pending", "approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")
    appointment.status = status
    appointment.reason_rejection = reason_rejection
    appointment.admin_id = admin.id
    db.commit()
    db.refresh(appointment)
    return appointment

# DELETE appointment (citizen or admin)
@router.delete("/{appointment_id}", status_code=204)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db),
                       user: models.User = Depends(require_citizen)):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if user.role == "citizen" and appointment.citizen_id != user.id:
        raise HTTPException(status_code=403, detail="You cannot delete this appointment")
    db.delete(appointment)
    db.commit()
    return Response(status_code=204)
