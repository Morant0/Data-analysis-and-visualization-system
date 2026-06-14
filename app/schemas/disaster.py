"""
#用户名 : 17954
#日期 : 2025/4/14 15:41
"""
from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class DisasterBase(BaseModel):
    dis_no: str
    classification_key: str
    disaster_group: str
    disaster_subgroup: str
    disaster_type: str
    disaster_subtype: str
    event_name: Optional[str] = None
    iso: str
    country: str
    subregion: str
    region: str
    location: Optional[str] = None
    origin: Optional[str] = None
    ofda_response: bool
    appeal: bool
    declaration: bool
    magnitude: Optional[float] = None
    magnitude_scale: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    river_basin: Optional[str] = None
    start_year: Optional[int] = None
    start_month: Optional[int] = None
    start_day: Optional[int] = None
    end_year: Optional[int] = None
    end_month: Optional[int] = None
    end_day: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    duration_days: Optional[int] = None

class DisasterCreate(DisasterBase):
    pass

class DisasterUpdate(DisasterBase):
    pass
