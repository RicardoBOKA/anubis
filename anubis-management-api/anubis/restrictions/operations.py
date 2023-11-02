from sqlalchemy.orm import Session
from . import models, schemas
import anubis.default as default
import uuid


def create_restriciton(db: Session, restriction: schemas.RestrictionCreate, target_name: str, target_id: str):
    pid = str(uuid.uuid4())
    new_restriction = models.Restriction(id=pid, name=restriction.name)
    new_restriction.set_target(target_name, target_id)

    db.add(new_restriction)
    db.commit()
    db.refresh(new_restriction)

    return new_restriction

def get_restriction(db: Session, restriction_id: str):
    return db.query(models.Restriction).filter(models.Restriction.id == restriction_id).first()


def get_all_restrictions(db: Session):
    return db.query(models.Restriction).all()


def delete_restriction(db: Session, restriction_id: str):
    db_restriction = db.query(models.Restriction).filter(models.Restriction.id == restriction_id).first()

    if db_restriction:
        db.delete(db_restriction)
        db.commit()

    return db_restriction
