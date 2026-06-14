"""
#用户名 : 17954
#日期 : 2025/4/17 13:36
"""
from app.core.crud import CRUDBase
from app.models.admin import EconomicLoss
from app.schemas.economic_loss import *
from typing import Optional
from tortoise.expressions import F
from tortoise.functions import Coalesce, Sum
from tortoise.expressions import Q

class EconomicLossController(CRUDBase[EconomicLoss, EconomicLossCreate, EconomicLossUpdate]):
    def __init__(self):
        super().__init__(model=EconomicLoss)

    async def get(self, dis_no: str) -> Optional[EconomicLoss]:
        # 使用 Tortoise 的查询方法
        return await self.model.get_or_none(dis_no=dis_no)

    # 重写 update 方法，适配 dis_no 主键
    async def update(self, dis_no: str, obj_in: EconomicLossUpdate) -> EconomicLoss:
        obj = await self.model.get(dis_no=dis_no)
        obj.update_from_dict(obj_in.dict(exclude_unset=True))
        await obj.save()
        return obj

    async def remove(self, dis_no: str) -> None:
        obj = await self.get(dis_no=dis_no)
        await obj.delete()

    @classmethod
    async def get_recent_disaster_loss(cls, start_year: int, end_year: int, country: str = None):
        query = EconomicLoss.filter(start_year__gte=start_year, start_year__lte=end_year)
        if country:
            query = query.filter(country__icontains=country)
        # 使用 TortoiseORM 进行聚合查询
        query = (
            query
                .annotate(
                total_loss=Coalesce(Sum(F('total_adjusted')), 0)
            )
                .group_by("start_year")
                .order_by("start_year")
                .values("start_year", "total_loss")
        )
        return await query

    @classmethod
    async def get_recent_disaster_type_loss(cls, start_year: int, end_year: int, country: str = None):
        query = EconomicLoss.filter(start_year__gte=start_year, start_year__lte=end_year)
        if country:
            query = query.filter(country__icontains=country)
        # 使用 TortoiseORM 进行聚合查询
        query = (
            query
                .annotate(
                total_loss=Coalesce(Sum(F('total_adjusted')), 0)
            )
                .group_by("disaster_type")
                .order_by("disaster_type")
                .values("disaster_type", "total_loss")
        )
        return await query

    @classmethod
    async def get_recent_country_loss(cls, start_year: int, end_year: int):
        # 使用 TortoiseORM 进行聚合查询
        query = (
            EconomicLoss
                .filter(start_year__gte=start_year, start_year__lte=end_year)
                .annotate(
                total_loss=Coalesce(Sum(F('total_adjusted')), 0)
            )
                .group_by("country")
                .order_by("country")
                .values("country", "total_loss")
        )
        return await query

    @classmethod
    async def get_recent_loss_total(cls, start_year: int, end_year: int):
        # 使用 TortoiseORM 进行聚合查询
        query = (
            EconomicLoss
                .filter(start_year__gte=start_year, start_year__lte=end_year)
                .annotate(total_loss_sum=Coalesce(Sum(F('total_adjusted')), 0))
        )
        result = await query.first().values("total_loss_sum")
        return result["total_loss_sum"] if result else 0

    @classmethod
    async def get_country_economic_loss(cls, query: Q):
        # 使用 TortoiseORM 进行聚合查询
        query = (
            EconomicLoss
                .filter(query)
                .annotate(total_loss=Coalesce(Sum("total_adjusted"), 0))
                .group_by("country")
                .order_by("country")
                .values("country", "total_loss")
        )

        return await query

economic_loss_controller = EconomicLossController()