"""
#用户名 : 17954
#日期 : 2025/4/15 14:05
"""
from fastapi import APIRouter

from .disasters import router

disasters_router = APIRouter()
disasters_router.include_router(router, tags=["灾害模块"])

__all__ = ["disasters_router"]