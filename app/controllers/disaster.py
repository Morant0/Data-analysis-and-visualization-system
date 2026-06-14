"""
#用户名 : 17954
#日期 : 2025/4/15 14:05
"""
from tortoise.expressions import F, Q
from tortoise.functions import Count
from app.core.crud import CRUDBase
from app.models.admin import Disaster, Country
from app.schemas.disaster import DisasterCreate, DisasterUpdate
from typing import Optional

class DisasterController(CRUDBase[Disaster, DisasterCreate, DisasterUpdate]):
    def __init__(self):
        super().__init__(model=Disaster)

    async def get(self, dis_no: str) -> Optional[Disaster]:
        return await self.model.get_or_none(dis_no=dis_no)

    async def update(self, dis_no: str, obj_in: DisasterUpdate) -> Disaster:
        obj = await self.model.get(dis_no=dis_no)
        obj.update_from_dict(obj_in.dict(exclude_unset=True))
        await obj.save()
        return obj

    async def remove(self, dis_no: str) -> None:
        obj = await self.get(dis_no=dis_no)
        await obj.delete()

    @classmethod
    async def geDisaster_yearly_count(cls, start_year: int, end_year: int, country: str = None):
        query = Disaster.filter(start_year__gte=start_year, start_year__lte=end_year)
        if country:
            query = query.filter(country__icontains=country)
        query = (
            query
                .annotate(count=Count("dis_no"))
                .group_by("start_year")
                .order_by("start_year")
                .values("start_year", "count")
        )
        return await query

    @classmethod
    async def getDisaster_yearly_count_by_type(cls, start_year: int, end_year: int, country: str = None):
        query = Disaster.filter(start_year__gte=start_year, start_year__lte=end_year)
        if country:
            query = query.filter(country__icontains=country)
        query = (
            query
                .annotate(total_count=Count("dis_no"))
                .group_by("disaster_type")
                .values("disaster_type", "total_count")
        )
        return await query

    @classmethod
    async def get_recent_country_disaster_count(cls, start_year: int, end_year: int):
        query = (
            Disaster
                .filter(start_year__gte=start_year, start_year__lte=end_year)
                .annotate(count=Count("dis_no"))
                .group_by("country")
                .order_by("country")
                .values("country", "count")
        )
        return await query

    @classmethod
    async def check_keyword_exists(cls, keyword: str):
        query = (
            Disaster
                .filter(
                Q(country__icontains=keyword) |
                Q(dis_no__icontains=keyword) |
                Q(disaster_type__icontains=keyword)
            )
        )
        return await query.exists()

    @classmethod
    async def get_disaster_count_in_n_years(cls, start_year: int, end_year: int):
        query = (
            Disaster
                .filter(start_year__gte=start_year, start_year__lte=end_year)
        )
        return await query.count()


    @classmethod
    async def get_country_disaster_count(cls, query: Q):
        query = (
            Disaster
                .filter(query)
                .annotate(count=Count("dis_no"))
                .group_by("country")
                .order_by("country")
                .values("country", "count")
        )
        return await query

disaster_controller = DisasterController()