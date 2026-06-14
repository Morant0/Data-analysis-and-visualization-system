"""
#用户名 : 17954
#日期 : 2025/4/14 21:16
"""
from fastapi import APIRouter

from .countries import router

countries_router = APIRouter()
countries_router.include_router(router, tags=["城市模块"])

__all__ = ["countries_router"]