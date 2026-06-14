"""
#用户名 : 17954
#日期 : 2025/4/17 13:49
"""
from fastapi import APIRouter

from .human_impact import router

human_impact_router = APIRouter()
human_impact_router.include_router(router, tags=["人员影响模块"])

__all__ = ["human_impact_router"]