from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# =========================
# USER SCHEMAS
# =========================
class UserBase(BaseModel):
    full_name: str
    email: EmailStr


class UserCreate(UserBase):
    password: str  # plain password for registration
    role: Optional[str] = "citizen"


class UserOut(UserBase):
    id: int
    role: str
    created_at: datetime

    class Config:
        orm_mode = True


# =========================
# VACCINE SCHEMAS
# =========================
class VaccineBase(BaseModel):
    name: str
    price: Optional[float] = None
    availability: Optional[bool] = True


class VaccineCreate(VaccineBase):
    pass


class VaccineOut(VaccineBase):
    id: int

    class Config:
        orm_mode = True


# =========================
# APPOINTMENT SCHEMAS
# =========================
class AppointmentBase(BaseModel):
    citizen_id: int
    vaccine_id: int
    preferred_date: datetime
    status: Optional[str] = "pending"
    reason_rejection: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentOut(AppointmentBase):
    id: int
    admin_id: Optional[int]
    created_at: datetime
    vaccine: VaccineOut  # include vaccine info if needed

    class Config:
        orm_mode = True


# =========================
# VACCINATION SCHEMAS
# =========================
class VaccinationBase(BaseModel):
    appointment_id: int
    citizen_id: int
    vaccine_id: int
    dose_number: int
    batch_number: Optional[str] = None


class VaccinationCreate(VaccinationBase):
    pass


class VaccinationOut(VaccinationBase):
    id: int
    vaccination_date: datetime
    admin_id: Optional[int]
    vaccine: VaccineOut

    class Config:
        orm_mode = True


# =========================
# AWARENESS ARTICLE SCHEMAS
# =========================
class AwarenessArticleBase(BaseModel):
    title: str
    content: str


class AwarenessArticleCreate(AwarenessArticleBase):
    created_by: int  # user_id of the author


class AwarenessArticleOut(AwarenessArticleBase):
    id: int
    created_at: datetime
    author: UserOut

    class Config:
        orm_mode = True


# =========================
# AUTHENTICATION SCHEMAS
# =========================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

