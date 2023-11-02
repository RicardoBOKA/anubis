from pydantic import BaseModel, validator
import re

class RestrictionBase(BaseModel):
    name: str

    @validator('name')
    def valid_tenant_name(cls, v):
        p = re.compile("^[a-zA-Z0-9_]*$")
        if not p.match(v):
            raise ValueError(
                'name must include only alphanumeric or _ characters')
        if len(v) > 50:
            raise ValueError('name max lenght is 50 characters')
        return v
    
class RestrictionCreate(RestrictionBase):
    pass

class Restriction(RestrictionBase):
    id: str
    table_target_id: str
    
    class Config:
        orm_mode = True
