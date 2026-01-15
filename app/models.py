from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


# =========================
# USERS TABLE
# =========================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)

    # citizen or admin
    role = Column(String, nullable=False, default="citizen")

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships (IMPORTANT FIX)
    appointments = relationship(
        "Appointment",
        foreign_keys="Appointment.citizen_id",
        back_populates="citizen",
        cascade="all, delete"
    )

    vaccinations = relationship(
        "Vaccination",
        foreign_keys="Vaccination.citizen_id",
        back_populates="citizen",
        cascade="all, delete"
    )

    articles = relationship(
        "AwarenessArticle",
        foreign_keys="AwarenessArticle.created_by",
        back_populates="author"
    )


# =========================
# VACCINES MASTER TABLE
# =========================
class Vaccine(Base):
    __tablename__ = "vaccines"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False, unique=True)
    price = Column(Float, nullable=True)
    availability = Column(Boolean, default=True)

    appointments = relationship("Appointment", back_populates="vaccine")
    vaccinations = relationship("Vaccination", back_populates="vaccine")


# =========================
# APPOINTMENTS TABLE
# =========================
class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, nullable=False)

    citizen_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    vaccine_id = Column(Integer, ForeignKey("vaccines.id", ondelete="CASCADE"), nullable=False)

    preferred_date = Column(DateTime(timezone=True), nullable=False)

    status = Column(String, nullable=False, default="pending", index=True)

    admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    reason_rejection = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    citizen = relationship("User", foreign_keys=[citizen_id], back_populates="appointments")
    admin = relationship("User", foreign_keys=[admin_id])
    vaccine = relationship("Vaccine", back_populates="appointments")
    vaccination = relationship("Vaccination", back_populates="appointment", uselist=False)


Index("idx_appointment_user_status", "citizen_id", "status")


# =========================
# VACCINATIONS TABLE
# =========================
class Vaccination(Base):
    __tablename__ = "vaccinations"

    id = Column(Integer, primary_key=True, nullable=False)

    appointment_id = Column(Integer, ForeignKey("appointments.id", ondelete="CASCADE"))
    citizen_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    vaccine_id = Column(Integer, ForeignKey("vaccines.id", ondelete="CASCADE"), nullable=False)

    dose_number = Column(Integer, nullable=False)
    batch_number = Column(String, nullable=True)

    vaccination_date = Column(DateTime(timezone=True), server_default=func.now())

    admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    appointment = relationship("Appointment", back_populates="vaccination")
    citizen = relationship("User", foreign_keys=[citizen_id], back_populates="vaccinations")
    admin = relationship("User", foreign_keys=[admin_id])
    vaccine = relationship("Vaccine", back_populates="vaccinations")


# =========================
# AWARENESS ARTICLES TABLE
# =========================
class AwarenessArticle(Base):
    __tablename__ = "awareness_articles"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    created_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))

    author = relationship(
        "User",
        foreign_keys=[created_by],
        back_populates="articles"
    )


