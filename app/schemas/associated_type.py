"""
#用户名 : 17954
#日期 : 2025/4/14 19:41
"""
from pydantic import BaseModel

class AssociatedTypeBase(BaseModel):
    type_name: str

class AssociatedTypeCreate(AssociatedTypeBase):
    pass

class AssociatedTypeResponse(AssociatedTypeBase):
    class Config:
        orm_mode = True