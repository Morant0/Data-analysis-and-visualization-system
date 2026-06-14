"""
#用户名 : 17954
#日期 : 2025/4/15 14:05
"""
from fastapi import APIRouter, Query, Depends, HTTPException
from app.controllers.disaster import disaster_controller
from app.schemas import Success, SuccessExtra
from app.schemas.disaster import *
from app.models.admin import User
from tortoise.expressions import Q
from app.models.admin import Disaster
from datetime import datetime, timedelta


router = APIRouter()

@router.get("/get", summary="查看灾害详情")
async def get_disaster(
        dis_no: str = Query(..., description="灾害编号")
):
    try:
        disaster = await disaster_controller.get(dis_no=dis_no)
        return Success(data=await disaster.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")


@router.get("/list", summary="查看灾害列表")
async def list_disaster(
    dis_no: str = Query(None, description="按编号过滤"),
    country: str = Query(None, description="按国家过滤"),
    type: str = Query(None, description="按类型过滤"),
    keyword: str = Query(None, description="关键字搜索（国家、编号、类型）"),
    page: int = Query(1, description="页码"),
    page_size: int = Query(20, description="每页数量"),
    start_time: str = Query("", description="开始时间"),
    end_time: str = Query("", description="结束时间"),
):
    try:
        query = Q()
        if dis_no:
            query &= Q(dis_no=dis_no)
        if country:
            query &= Q(country__icontains=country)
        if type:
            query &= Q(disaster_type__icontains=type)
        if start_time and end_time:
            query &= Q(start_date__range=[start_time, end_time])
        elif start_time:
            query &= Q(start_date__gte=start_time)
        elif end_time:
            query &= Q(start_date__lte=end_time)
        if keyword:
            query &= (Q(country__icontains=keyword) | Q(dis_no__icontains=keyword) | Q(disaster_type__icontains=keyword))

        # 构造查询并按 start_date 降序排序
        query = Disaster.filter(query).order_by("-start_date")

        total = await query.count()
        data_objs = await query.offset((page - 1) * page_size).limit(page_size)
        data = [await obj.to_dict() for obj in data_objs]
        return SuccessExtra(data=data, total=total, page=page, page_size=page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create", summary="创建灾害")
async def create_country(
        data: DisasterCreate
):
    await disaster_controller.create(data)
    return Success(msg="创建成功")

@router.post("/update", summary="更新灾害")
async def update_country(
        data: DisasterUpdate
):
    await disaster_controller.update(dis_no=data.dis_no, obj_in=data)  # 传递 iso 参数
    return Success(msg="更新成功")

@router.delete("/delete", summary="删除灾害")
async def delete_country(
        dis_no: str = Query(..., description="灾害编号")
):
    await disaster_controller.remove(dis_no=dis_no)
    return Success(msg="删除成功")


@router.get("/yearly_count", summary="最近n年每年灾害发生次数")
async def recent_disaster_yearly_count(
        n: int = Query(..., description="最近的年份数量", ge=1),
        country: str = Query(None, description="国家名称（可选）")
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        yearly_counts = await disaster_controller.geDisaster_yearly_count(start_year, current_year, country)
        return SuccessExtra(data=yearly_counts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/yearly_count_by_type", summary="最近n年各类型灾害发生次数")
async def recent_disaster_yearly_count_by_type(
    n: int = Query(..., description="最近的年份数量", ge=1),
    country: str = Query(None, description="国家名称（可选）")
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        yearly_counts_by_type = await disaster_controller.getDisaster_yearly_count_by_type(start_year, current_year, country)
        return SuccessExtra(data=yearly_counts_by_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/country-disaster-count", summary="最近n年每个国家的灾害发生次数")
async def recent_country_disaster_count(
    n: int = Query(..., description="最近的年份数量", ge=1)
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        country_disaster_counts = await disaster_controller.get_recent_country_disaster_count(start_year, current_year)
        return SuccessExtra(data=country_disaster_counts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/check-keyword", summary="检查关键字是否存在")
async def check_keyword_exists(
    keyword: str = Query(..., description="关键字")
):
    try:
        exists = await disaster_controller.check_keyword_exists(keyword)
        return SuccessExtra(data=[{"exists": exists}])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-disaster-count", summary="最近n年灾害发生次数总数")
async def recent_disaster_count(
    n: int = Query(..., description="最近的年份数量", ge=1)
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        total_count = await disaster_controller.get_disaster_count_in_n_years(start_year, current_year)
        return SuccessExtra(data={"total_disaster_count": total_count})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/country-count", summary="指定时间段内各国灾害发生次数")
async def country_disaster_count(
    start_date: str = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: str = Query(None, description="结束日期 (YYYY-MM-DD)"),
    disaster_type: str = Query(None, description="灾害类型")
):
    try:
        # 转换日期为 datetime 对象
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

        country_counts = await disaster_controller.get_country_disaster_count(query)
        return SuccessExtra(data=country_counts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))