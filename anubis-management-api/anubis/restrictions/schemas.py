from pydantic import BaseModel

class RestrictionBase(BaseModel):
    name: str

class RestrictionCreate(RestrictionBase):
    pass

class Restriction(RestrictionBase):
    id: str
    table_target_id: str
        
    class Config:
        orm_mode = True
