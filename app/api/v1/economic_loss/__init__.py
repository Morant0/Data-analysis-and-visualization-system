"""
#用户名 : 17954
#日期 : 2025/4/17 13:45
"""
from fastapi import APIRouter

from .economic_loss import router

economic_loss_router = APIRouter()
economic_loss_router.include_router(router, tags=["经济损失模块"])

__all__ = ["economic_loss_router"]