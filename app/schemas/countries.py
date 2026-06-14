"""
#用户名 : 17954
#日期 : 2025/4/14 19:36
"""
from pydantic import BaseModel
from typing import Optional

class CountryBase(BaseModel):
    iso: str
    country: str
    subregion: str
    region: str

class CountryCreate(CountryBase):
    pass

class CountryUpdate(CountryBase):
    pass
