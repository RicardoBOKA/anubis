import json
from pydantic import BaseModel, validator
from typing import Dict, Any
import re

class RestrictionBase(BaseModel):
    name: str
    data: str

    @validator('name')
    def valid_tenant_name(cls, v):
        p = re.compile("^[a-zA-Z0-9_ ]*$")
        if not p.match(v):
            raise ValueError(
                'name must include only alphanumeric or _ characters')
        if len(v) > 50:
            raise ValueError('name max lenght is 50 characters')
        return v

    @validator('data', pre=True)
    def validate_value(cls, v):
        try:
            data = json.loads(v)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format : {e}")
        
        if 'type' not in data or 'value' not in data:
            raise ValueError("JSON must contain 'type' and 'value' keys")
        
        value = data['value']

        if not isinstance(value, str):
            raise ValueError("Key 'Value' must be a String.")
    

        return json.dumps(data)

    
class RestrictionCreate(RestrictionBase):
    pass

class Restriction(RestrictionBase):
    id: str
    table_target_id: str
    
    class Config:
        orm_mode = True


class Message(BaseModel):
    message: str



# class RestrictionValueBase(BaseModel):
#     value: str
#     value_type: str  # si type de la valeur

# class RestrictionValueCreate(RestrictionValueBase):
#     restriction_id: str

# class RestrictionValue(RestrictionValueBase):
#     id: str
#     restriction: Restriction

#     class Config:
#         orm_mode = True