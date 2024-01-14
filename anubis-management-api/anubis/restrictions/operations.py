import json
from datetime import datetime as DateTime
from sqlalchemy.orm import Session
from . import models, schemas
import anubis.default as default
from fastapi import HTTPException
import uuid
from anubis.policies import models as mp
from anubis.tenants import models as mt

def create_restriciton(db: Session, restriction: schemas.RestrictionCreate, target_name: str, target_id: str):
    pid = str(uuid.uuid4())
    
    # Check if value of restriction is the right type
    validate_restriction_json(restriction.data)

    new_restriction = models.Restriction(id=pid, name=restriction.name, data=restriction.data)

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

def validate_restriction_json(data):
    try:
        value_data = json.loads(data)

        type = value_data.get('type')
        value = value_data.get('value')

        if type == 'integer':
            if not is_valid_integer(value):
                raise ValueError("Value must be an integer for type 'int'.")
        
        elif type == 'float':
            if not is_valid_float(value):
                raise ValueError("Value must be a float for type 'float'.")     
        
        elif type == 'datetime':
            if not is_valid_datetime(value):
                raise ValueError("Value must be a valid datetime format for type 'datetime' : {Ex : '2021-09-17', '09/17/2021', '17/09/2021'}")
        
        elif type == 'time':
            if not is_valid_time(value):
                raise ValueError("Value must be a valid time format for type 'time' : {Ex : '14:45:06'}")
        
        elif type not in ['integer', 'float', 'string', 'datetime', 'time'] : # add if need
            raise ValueError("(Data type must be one of : 'integer', 'float' 'string' or 'datetime', 'time' {+...+})")
        
        # Add if need
        
    except (ValueError, TypeError, json.JSONDecodeError) as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON data: {e}.")

def is_valid_time(value):
    # Liste des formats du temps à vérifier
    time_formats = [
        "%H:%M:%S",             # Uniquement l'heure
        # "%d/%m/%Y %H:%M:%S",    # Date et heure (format européen)
        # "%m/%d/%Y %H:%M:%S",    # Date et heure (format américain)
    ]

    for date_format in time_formats:
        try:
            DateTime.strptime(value, date_format)
            return True  # Si le parsing réussit, la date est valide
        except ValueError:
            pass  # Si une erreur se produit, essayez le format suivant

    return False
def is_valid_datetime(value):
    # Liste des formats de date/heure à vérifier
    date_time_formats = [
        "%Y-%m-%d",             # Uniquement la date (format ISO 8601)
        "%d/%m/%Y",             # Uniquement la date (format européen)
        "%m/%d/%Y",             # Uniquement la date (format américain)
        # "%d/%m/%Y %H:%M:%S",    # Date et heure (format européen)
        # "%m/%d/%Y %H:%M:%S",    # Date et heure (format américain)
        # Rajouter au besoin
    ]

    for date_format in date_time_formats:
        try:
            DateTime.strptime(value, date_format)
            return True  # Si le parsing réussit, la date est valide
        except ValueError:
            pass  # Si une erreur se produit, essayez le format suivant

    return False
def is_valid_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False
def is_valid_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def update_restriction(db: Session, restriction_id: str, updated_data: schemas.RestrictionCreate):
    db_restriction = db.query(models.Restriction).filter(models.Restriction.id == restriction_id).first()
    if db_restriction:
        db_restriction.name = updated_data.name
        db_restriction.data = updated_data.data
        db.commit()
        db.refresh(db_restriction)
    return db_restriction


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

def delete_all_restrictions(db: Session):
    try:
        db.query(models.Restriction).delete()
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting restriction: {e}")


# #  RestrictionValue

# def create_restriction_value(db: Session, restriction_value: schemas.RestrictionValueCreate):
#     pid = str(uuid.uuid4())
#     new_restriction_value = models.RestrictionValue(
#         id=pid,
#         value=restriction_value.value,
#         restriction_id=restriction_value.restriction_id,
#         value_type=restriction_value.value_type  # si vous avez inclus ce champ
#     )
#     db.add(new_restriction_value)
#     db.commit()
#     db.refresh(new_restriction_value)
#     return new_restriction_value

# def get_restriction_value(db: Session, restriction_value_id: str):
#     return db.query(models.RestrictionValue).filter(models.RestrictionValue.id == restriction_value_id).first()

# def get_all_restriction_values(db: Session):
#     return db.query(models.RestrictionValue).all()

# def update_restriction_value(db: Session, restriction_value_id: str, updated_data: schemas.RestrictionValueCreate):
#     db_restriction_value = db.query(models.RestrictionValue).filter(models.RestrictionValue.id == restriction_value_id).first()
#     if db_restriction_value:
#         db_restriction_value.value = updated_data.value
#         db_restriction_value.value_type = updated_data.value_type  # si ce champ existe
#         db.commit()
#         db.refresh(db_restriction_value)
#     return db_restriction_value

# def delete_restriction_value(db: Session, restriction_value_id: str):
#     db_restriction_value = db.query(models.RestrictionValue).filter(models.RestrictionValue.id == restriction_value_id).first()
#     if db_restriction_value:
#         db.delete(db_restriction_value)
#         db.commit()
#     return db_restriction_value
