from sqlalchemy.orm import Session
from . import models, schemas
import anubis.default as default
from fastapi import HTTPException
import uuid
from anubis.policies import models as mp
from anubis.tenants import models as mt

def create_restriciton(db: Session, restriction: schemas.RestrictionCreate, target_name: str, target_id: str):
    pid = str(uuid.uuid4())
    new_restriction = models.Restriction(id=pid, name=restriction.name)
    
    #Set_target pour définir la colonne target avec le nom de la table et l'id de l'instace qu'on veut cibler 
    # grâce aux paramètres de la fonction routers.create_restriciton()
    new_restriction.set_target(target_name, target_id)
    
    if new_restriction.get_target_name() not in default.DEFAULT_TABLES:
        raise HTTPException(status_code=400, detail="Invalid table name. Must be one of 'Policy', 'ServicePath', 'Agent'")
    
    #Vérification que l'instance de la table que l'on veut cibler existe
    target_exists = False

    if target_name == "policy":
        target_exists = (db.query(mp.Policy).filter(mp.Policy.id == target_id).first() is not None)

    elif target_name == "servicepath":
        target_exists = (db.query(mt.ServicePath).filter(mt.ServicePath.id == target_id).first() is not None)
    
    elif target_name == "agent":
        if (target_id not in default.DEFAULT_AGENTS):
            raise HTTPException(status_code=400, detail=f"Cet agent n'est pas défini")
        target_exists = True

    if not target_exists:
        # Cas où l'ID n'existe pas dans la table cible
        raise HTTPException(status_code=400, detail=f"Cible inexistante ou non définie pas dans la table {target_name}")

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
