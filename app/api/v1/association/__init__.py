"""
#用户名 : 17954
#日期 : 2025/4/28 13:44
"""
from fastapi import APIRouter

from .association import router

association_router = APIRouter()
association_router.include_router(router, tags=["关联分析模块"])

__all__ = ["association_router"]