"""
#用户名 : 17954
#日期 : 2025/4/14 19:40
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class HumanImpactBase(BaseModel):
    dis_no: str
    disaster_type: str
    country: str
    total_deaths: Optional[int] = None
    num_injured: Optional[int] = None
    num_affected: Optional[int] = None
    num_homeless: Optional[int] = None
    total_affected: Optional[int] = None
    start_year: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class HumanImpactCreate(HumanImpactBase):
    pass

class HumanImpactUpdate(HumanImpactBase):
    pass