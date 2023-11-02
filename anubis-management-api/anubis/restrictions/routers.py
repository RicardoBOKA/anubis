from typing import List
from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException, status, Response, Header
from . import operations, schemas
from ..dependencies import get_db
from ..utils import OptionalHTTPBearer, parse_auth_token


auth_scheme = OptionalHTTPBearer()
router = APIRouter(prefix="/v1/restrictions",
                   tags=["restrictions"],
                   responses={404: {"description": "Not found"}},)

@router.post("/", response_class=Response, status_code=status.HTTP_201_CREATED, summary="Create restriction")
def create_restriciton(response: Response, restriction : schemas.RestrictionCreate, target_name: str, target_id: str, db: Session = Depends(get_db)):
    
    new_restriction = operations.create_restriciton(db=db, restriction=restriction, target_name=target_name, target_id=target_id)
    
    response.headers["Restriction-ID"] = new_restriction.id
    response.status_code = status.HTTP_201_CREATED
    return response


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
