"""
#用户名 : 17954
#日期 : 2025/4/17 13:49
"""
from fastapi import APIRouter, Query, Depends, HTTPException
from app.controllers.human_impact import human_impact_controller
from app.schemas import Success, SuccessExtra
from app.schemas.disaster import *
from app.models.admin import User
from datetime import datetime, timedelta
from tortoise.expressions import Q

router = APIRouter()

@router.get("/get", summary="查看人员影响")
async def get_disaster(
        dis_no: str = Query(..., description="灾害编号")
):
    try:
        disaster = await human_impact_controller.get(dis_no=dis_no)
        return Success(data=await disaster.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@router.get("/recent-stats", summary="最近n年影响人数/死亡受伤人数")
async def recent_disaster_stats(
    n: int = Query(..., description="最近的年份数量", ge=1),
    country: str = Query(None, description="国家名称（可选）")
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        yearly_stats = await human_impact_controller.get_recent_disaster_stats(start_year, current_year, country)
        # 处理 Decimal 类型
        processed_stats = []
        for stat in yearly_stats:
            processed_stat = {
                "start_year": stat["start_year"],
                "total_affected_sum": float(stat["total_affected_sum"]),
                "death_injured_sum": float(stat["death_injured_sum"])
            }
            processed_stats.append(processed_stat)
        return SuccessExtra(data=processed_stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-type-stats", summary="最近n年各类型灾害影响人数/死亡受伤人数")
async def recent_type_disaster_stats(
    n: int = Query(..., description="最近的年份数量", ge=1),
    country: str = Query(None, description="国家名称（可选）")
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        type_stats = await human_impact_controller.get_recent_type_disaster_stats(start_year, current_year, country)
        # 处理 Decimal 类型
        processed_stats = []
        for stat in type_stats:
            processed_stat = {
                "disaster_type": stat["disaster_type"],
                "total_affected_sum": float(stat["total_affected_sum"]),
                "death_injured_sum": float(stat["death_injured_sum"])
            }
            processed_stats.append(processed_stat)
        return SuccessExtra(data=processed_stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-country-casualties", summary="最近n年每个国家的总影响/伤亡人数")
async def recent_country_casualties(
    n: int = Query(..., description="最近的年份数量", ge=1)
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1

        # 使用 HumanImpactController 查询并统计最近n年每个国家的总影响/伤亡人数
        country_casualties = await human_impact_controller.get_recent_country_casualties(start_year, current_year)
        # 处理 Decimal 类型
        processed_casualties = []
        for item in country_casualties:
            processed_casualties.append({
                "country": item["country"],
                "total_casualties": float(item["total_casualties"])
            })
        return SuccessExtra(data=processed_casualties)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-affected-total", summary="最近n年受影响人数总数")
async def recent_affected_total(
    n: int = Query(..., description="最近的年份数量", ge=1)
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        # 使用 disaster_controller 查询并统计最近n年受影响人数的总数
        total_affected = await human_impact_controller.get_recent_affected_total(start_year, current_year)
        # 处理 Decimal 类型
        total_affected_float = float(total_affected)
        return SuccessExtra(data={"total_affected": total_affected_float})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/country-affected-people", summary="指定时间段内各国灾害影响人数")
async def country_affected_people(
    start_date: str = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: str = Query(None, description="结束日期 (YYYY-MM-DD)"),
    disaster_type: str = Query(None, description="灾害类型")
):
    try:
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        # 如果未提供 start_date 和 end_date，默认统计最近 1 年
        if not start_date or not end_date:
            today = datetime.today()
            start_date = today - timedelta(days=365)  # 大约 1 年前
            end_date = today

        query = Q(start_date__gte=start_date, start_date__lte=end_date)
        if disaster_type:
            query &= Q(disaster_type=disaster_type)
        country_affected = await human_impact_controller.get_country_affected_people(query)

        result = []
        for item in country_affected:
            result.append({
                "country": item["country"],
                "total_affected": float(item["total_affected"])
            })
        return SuccessExtra(data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/country-casualties", summary="指定时间段内各国灾害伤亡人数")
async def country_casualties(
    start_date: str = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: str = Query(None, description="结束日期 (YYYY-MM-DD)"),
    disaster_type: str = Query(None, description="灾害类型")
):
    try:
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d")

        if not start_date or not end_date:
            today = datetime.today()
            start_date = today - timedelta(days=365)  # 大约 1 年前
            end_date = today

        query = Q(start_date__gte=start_date, start_date__lte=end_date)
        if disaster_type:
            query &= Q(disaster_type=disaster_type)

        country_casualties = await human_impact_controller.get_country_casualties(query)

        result = []
        for item in country_casualties:
            result.append({
                "country": item["country"],
                "total_casualties": float(item["total_casualties"])
            })

        return SuccessExtra(data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))