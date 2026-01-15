from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models


def seed_vaccines():
    db: Session = SessionLocal()

    vaccines = [
        {"name": "Fièvre Jaune", "price": 92},
        {"name": "Hépatite A", "price": 100},
        {"name": "Hépatite B", "price": 65},
        {"name": "Typhoïde", "price": 33},
        {"name": "Méningite", "price": 120},
        {"name": "Grippe", "price": 35},
        {"name": "Antirabique", "price": 180},
        {"name": "RRO (Rougeole – Rubéole – Oreillons)", "price": 70},
    ]

    for v in vaccines:
        exists = db.query(models.Vaccine).filter(models.Vaccine.name == v["name"]).first()
        if not exists:
            vaccine = models.Vaccine(
                name=v["name"],
                price=v["price"],
                availability=True
            )
            db.add(vaccine)

    db.commit()
    db.close()
    print("🎉 Vaccines inserted successfully!")


if __name__ == "__main__":
    seed_vaccines()
