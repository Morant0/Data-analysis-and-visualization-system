"""
#用户名 : 17954
#日期 : 2025/4/14 21:17
"""
from fastapi import APIRouter, Query, HTTPException
from app.controllers.country import country_controller
from app.schemas import Success
from app.schemas.countries import *

router = APIRouter()

@router.get("/list", summary="查看国家列表")
async def list_country():
    try:
        # 确认使用 await 并明确查询字段
        data = await country_controller.model.all().values("iso", "country", "subregion", "region")
        return Success(data=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")


@router.get("/get", summary="查看国家详情")
async def get_country(
    iso: str = Query(..., description="ISO3国家代码"),
):
    country = await country_controller.get(iso=iso)
    return Success(data=await country.to_dict())

@router.post("/create", summary="创建国家")
async def create_country(
        data: CountryCreate
):
    await country_controller.create(data)
    return Success(msg="创建成功")

@router.post("/create", summary="创建国家")
async def create_country(
        data: CountryCreate
):
    await country_controller.create(data)
    return Success(msg="创建成功")

@router.post("/update", summary="更新国家")
async def update_country(
        data: CountryUpdate
):
    await country_controller.update(iso=data.iso, obj_in=data)  # 传递 iso 参数
    return Success(msg="更新成功")

@router.delete("/delete", summary="删除国家")
async def delete_country(
        iso: str = Query(..., description="ISO3国家代码")
):
    await country_controller.remove(iso=iso)
    return Success(msg="删除成功")

