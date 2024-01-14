from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status, Response, Header
from . import operations, schemas
import anubis.default as default
from ..dependencies import get_db
from ..utils import OptionalHTTPBearer, parse_auth_token


auth_scheme = OptionalHTTPBearer()
router = APIRouter(prefix="/v1/restrictions",
                   tags=["restrictions"],
                   responses={404: {"description": "Not found"}},)

@router.post("/", response_class=Response, status_code=status.HTTP_201_CREATED, summary="Create restriction")
def create_restriciton(response: Response, restriction : schemas.RestrictionCreate, target_name: str, target_id: str, db: Session = Depends(get_db)):
    #Création d'une restriction avec target_name en lowercase
    new_restriction = operations.create_restriciton(db=db, restriction=restriction, target_name=target_name.lower().replace(" ", ""), target_id=target_id)
    
    #Si target_name (en lowercase) n'est pas dans la liste DEFAULT_TABLES (defult.py) une erreur de validation est levée. 
    if new_restriction.get_target_name() not in default.DEFAULT_TABLES:
        raise HTTPException(status_code=400, detail="Invalid table name. Must be one of 'Policy', 'ServicePath', 'Agent'")
    
    response.headers["Restriction-ID"] = new_restriction.id
    response.status_code = status.HTTP_201_CREATED
    return response

@router.put("/{restriction_id}", response_model=schemas.Restriction)
def update_restriction(restriction_id: str, restriction: schemas.RestrictionCreate, db: Session = Depends(get_db)):
    updated_restriction = operations.update_restriction(db, restriction_id, restriction)
    if updated_restriction is None:
        raise HTTPException(status_code=404, detail="Restriction not found")
    return updated_restriction

@router.get("/", response_model=List[schemas.Restriction])
def get_all_restrictions(db: Session = Depends(get_db)):
    db_restrictions = operations.get_all_restrictions(db)
    return db_restrictions



@router.get("/{restriction_id}", response_model=schemas.Restriction)
def read_restriction(
    restriction_id: str,
    db: Session = Depends(get_db)):
    db_restriction = operations.get_restriction(db, restriction_id)
    if db_restriction is None:
        raise HTTPException(status_code=404, detail="Restriction not found")
    return db_restriction



@router.delete("/{restriction_id}", response_model=schemas.Restriction)
def delete_restriction(
    restriction_id: str,
    db: Session = Depends(get_db)):
 
    db_restriction = operations.delete_restriction(db, restriction_id)
    if db_restriction is None:
        raise HTTPException(status_code=404, detail="Restriction not found")
    return db_restriction

@router.delete("/", response_model=schemas.Message)
def delete_all_restrictions_api(db: Session = Depends(get_db)):
    operations.delete_all_restrictions(db)
    return {"message": "All restrictions have been deleted"}




# @router.post("/values/", response_class=Response, status_code=status.HTTP_201_CREATED, summary="Create a restriction value")
# def create_restriction_value(response: Response, restriction_value: schemas.RestrictionValueCreate, db: Session = Depends(get_db)):
#     new_restriction_value = operations.create_restriction_value(db=db, restriction_value=restriction_value)
#     response.headers["RestrictionValue-ID"] = new_restriction_value.id
#     response.status_code = status.HTTP_201_CREATED
#     return response

# @router.get("/values/", response_model=List[schemas.RestrictionValue])
# def get_all_restriction_values(db: Session = Depends(get_db)):
#     return operations.get_all_restriction_values(db)

# @router.get("/values/{restriction_value_id}", response_model=schemas.RestrictionValue)
# def read_restriction_value(restriction_value_id: str, db: Session = Depends(get_db)):
#     db_restriction_value = operations.get_restriction_value(db, restriction_value_id)
#     if db_restriction_value is None:
#         raise HTTPException(status_code=404, detail="RestrictionValue not found1")
#     return db_restriction_value

# @router.put("/values/{restriction_value_id}", response_model=schemas.RestrictionValue)
# def update_restriction_value(restriction_value_id: str, restriction_value: schemas.RestrictionValueCreate, db: Session = Depends(get_db)):
#     updated_restriction_value = operations.update_restriction_value(db, restriction_value_id, restriction_value)
#     if updated_restriction_value is None:
#         raise HTTPException(status_code=404, detail="RestrictionValue not found2")
#     return updated_restriction_value

# @router.delete("/values/{restriction_value_id}", response_class=Response, status_code=status.HTTP_204_NO_CONTENT)
# def delete_restriction_value(restriction_value_id: str, db: Session = Depends(get_db)):
#     db_restriction_value = operations.delete_restriction_value(db, restriction_value_id)
#     if db_restriction_value is None:
#         raise HTTPException(status_code=404, detail="RestrictionValue not found3")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)



# @router.get("/restrctions",
#             response_model=List[schemas.Restriction],
#             responses=policies_not_json_responses,
#             summary="List restrictions")
# def read_restriciton(
#         response: Response,
#         accept: Optional[str] = Header(
#             'application/json'),
#         skip: int = 0,
#         limit: int = defaultLimit,
#         db: Session = Depends(get_db)):
    
#     x = operations.get_restricitons(db=db, skip=skip, limi=limit)
#     return x

# curl -X 'GET' \
#   'http://localhost:8000/v1/policies/restrctions?skip=0&limit=1000' \
#   -H 'accept: application/json' \
#   -H 'fiware-service: Tenant1' \
#   -H 'fiware-servicepath: /#'
