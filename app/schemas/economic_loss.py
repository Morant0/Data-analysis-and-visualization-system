"""
#用户名 : 17954
#日期 : 2025/4/14 19:40
"""
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class EconomicLossBase(BaseModel):
    dis_no: str
    disaster_type: str
    country: str
    reconstruction_adjusted: Optional[float] = None
    insured_adjusted: Optional[float] = None
    total_adjusted: Optional[float] = None
    cpi: Optional[float] = None
    start_year: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None

class EconomicLossCreate(EconomicLossBase):
    pass

class EconomicLossUpdate(EconomicLossBase):
    pass