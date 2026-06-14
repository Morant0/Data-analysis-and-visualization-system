"""
#用户名 : 17954
#日期 : 2025/4/14 20:34
"""
from app.core.crud import CRUDBase
from app.models.admin import Country
from app.schemas.countries import CountryCreate, CountryUpdate
from typing import Optional

class CountryController(CRUDBase[Country, CountryCreate, CountryUpdate]):
    def __init__(self):
        super().__init__(model=Country)

    async def get(self, iso: str) -> Optional[Country]:
        # 使用 Tortoise 的查询方法
        return await self.model.get_or_none(iso=iso)

    async def remove(self, iso: str) -> None:
        obj = await self.get(iso=iso)
        await obj.delete()

    # 重写 update 方法，适配 iso 主键
    async def update(self, iso: str, obj_in: CountryUpdate) -> Country:
        obj = await self.model.get(iso=iso)
        obj.update_from_dict(obj_in.dict(exclude_unset=True))
        await obj.save()
        return obj

country_controller = CountryController()