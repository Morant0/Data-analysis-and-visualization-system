"""
#用户名 : 17954
#日期 : 2025/4/17 13:40
"""
from app.core.crud import CRUDBase
from app.models.admin import HumanImpact
from app.schemas.human_impact import *
from typing import Optional
from tortoise.expressions import F
from tortoise.functions import Coalesce, Sum
from tortoise.expressions import Q

class HumanImpactController(CRUDBase[HumanImpact, HumanImpactCreate, HumanImpactUpdate]):
    def __init__(self):
        super().__init__(model=HumanImpact)

    async def get(self, dis_no: str) -> Optional[HumanImpact]:
        # 使用 Tortoise 的查询方法
        return await self.model.get_or_none(dis_no=dis_no)

    # 重写 update 方法，适配 dis_no 主键
    async def update(self, dis_no: str, obj_in: HumanImpactUpdate) -> HumanImpact:
        obj = await self.model.get(dis_no=dis_no)
        obj.update_from_dict(obj_in.dict(exclude_unset=True))
        await obj.save()
        return obj

    async def remove(self, dis_no: str) -> None:
        obj = await self.get(dis_no=dis_no)
        await obj.delete()

    @classmethod
    async def get_recent_disaster_stats(cls, start_year: int, end_year: int, country: str = None):
        query = HumanImpact.filter(start_year__gte=start_year, start_year__lte=end_year)
        if country:
            query = query.filter(country__icontains=country)
        # 使用 TortoiseORM 进行聚合查询
        query = (
            query
                .annotate(
                total_affected_sum=Coalesce(Sum(F('total_affected')), 0),
                total_deaths_sum=Coalesce(Sum(F('total_deaths')), 0),
                num_injured_sum=Coalesce(Sum(F('num_injured')), 0)
            )
                .annotate(
                death_injured_sum=F('total_deaths_sum') + F('num_injured_sum')
            )
                .group_by("start_year")
                .order_by("start_year")
                .values("start_year", "total_affected_sum", "death_injured_sum")
        )
        return await query

    @classmethod
    async def get_recent_type_disaster_stats(cls, start_year: int, end_year: int, country: str = None):
        query = HumanImpact.filter(start_year__gte=start_year, start_year__lte=end_year)
        if country:
            query = query.filter(country__icontains=country)
        # 使用 TortoiseORM 进行聚合查询
        query = (
            query
                .annotate(
                total_affected_sum=Coalesce(Sum(F('total_affected')), 0),
                total_deaths_sum=Coalesce(Sum(F('total_deaths')), 0),
                num_injured_sum=Coalesce(Sum(F('num_injured')), 0)
            )
                .annotate(
                death_injured_sum=F('total_deaths_sum') + F('num_injured_sum')
            )
                .group_by("disaster_type")
                .order_by("disaster_type")
                .values("disaster_type", "total_affected_sum", "death_injured_sum")
        )
        return await query

    @classmethod
    async def get_recent_country_casualties(cls, start_year: int, end_year: int):
        # 使用 TortoiseORM 进行聚合查询
        query = (
            HumanImpact
                .filter(start_year__gte=start_year, start_year__lte=end_year)
                .annotate(
                total_affected_sum=Coalesce(Sum(F('total_affected')), 0),
                total_deaths_sum=Coalesce(Sum(F('total_deaths')), 0),
                num_injured_sum=Coalesce(Sum(F('num_injured')), 0)
            )
                .annotate(
                total_casualties=F('total_affected_sum') + F('total_deaths_sum') + F('num_injured_sum')
            )
                .group_by("country")
                .order_by("country")
                .values("country", "total_casualties")
        )
        return await query

    @classmethod
    async def get_recent_affected_total(cls, start_year: int, end_year: int):
        # 使用 TortoiseORM 进行聚合查询
        query = (
            HumanImpact
                .filter(start_year__gte=start_year, start_year__lte=end_year)
                .annotate(total_affected_sum=Coalesce(Sum(F('total_affected')), 0))
        )
        result = await query.first().values("total_affected_sum")
        return result["total_affected_sum"] if result else 0

    @classmethod
    async def get_country_affected_people(cls, query: Q):
        # 使用 TortoiseORM 进行聚合查询
        query = (
            HumanImpact
                .filter(query)
                .annotate(total_affected=Coalesce(Sum("total_affected"), 0))
                .group_by("country")
                .order_by("country")
                .values("country", "total_affected")
        )
        return await query

    @classmethod
    async def get_country_casualties(cls, query: Q):
        # 使用 TortoiseORM 进行聚合查询
        query = (
            HumanImpact
                .filter(query)
                .annotate(
                total_deaths_sum=Coalesce(Sum(F('total_deaths')), 0),
                num_injured_sum=Coalesce(Sum(F('num_injured')), 0)
            )
            .annotate(
                total_casualties=F('total_deaths_sum') + F('num_injured_sum')
            )
                .group_by("country")
                .order_by("country")
                .values("country", "total_casualties")
        )
        return await query

human_impact_controller = HumanImpactController()