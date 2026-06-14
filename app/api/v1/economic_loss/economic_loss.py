"""
#用户名 : 17954
#日期 : 2025/4/17 13:45
"""
from fastapi import APIRouter, Query, Depends, HTTPException
from app.controllers.economic_loss import economic_loss_controller
from app.schemas import Success, SuccessExtra
from app.schemas.disaster import *
from app.models.admin import User
from tortoise.expressions import Q
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/get", summary="查看经济损失")
async def get_disaster(
        dis_no: str = Query(..., description="灾害编号")
):
    try:
        disaster = await economic_loss_controller.get(dis_no=dis_no)
        return Success(data=await disaster.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@router.get("/recent-loss", summary="最近n年每年总损失")
async def recent_disaster_loss(
    n: int = Query(..., description="最近的年份数量", ge=1),
    country: str = Query(None, description="国家名称（可选）")
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        yearly_loss = await economic_loss_controller.get_recent_disaster_loss(start_year, current_year, country)
        # 处理 Decimal 类型
        processed_loss = []
        for loss in yearly_loss:
            processed_loss.append({
                "start_year": loss["start_year"],
                "total_loss": float(loss["total_loss"])
            })
        return SuccessExtra(data=processed_loss)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-type-loss", summary="最近n年各类型灾害总损失")
async def recent_disaster_type_loss(
    n: int = Query(..., description="最近的年份数量", ge=1),
    country: str = Query(None, description="国家名称（可选）")
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        type_loss = await economic_loss_controller.get_recent_disaster_type_loss(start_year, current_year, country)
        # 处理 Decimal 类型
        processed_loss = []
        for item in type_loss:
            processed_loss.append({
                "disaster_type": item["disaster_type"],
                "total_loss": float(item["total_loss"])
            })
        return SuccessExtra(data=processed_loss)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-country-loss", summary="最近n年每个国家总损失")
async def recent_country_loss(
    n: int = Query(..., description="最近的年份数量", ge=1)
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        # 使用 disaster_controller 查询并统计最近n年每个国家的总损失
        country_loss = await economic_loss_controller.get_recent_country_loss(start_year, current_year)
        # 处理 Decimal 类型
        processed_loss = []
        for loss in country_loss:
            processed_loss.append({
                "country": loss["country"],
                "total_loss": float(loss["total_loss"])
            })
        return SuccessExtra(data=processed_loss)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/recent-loss-total", summary="最近n年经济损失总数")
async def recent_loss_total(
    n: int = Query(..., description="最近的年份数量", ge=1)
):
    try:
        current_year = datetime.now().year
        start_year = current_year - n + 1
        # 使用 disaster_controller 查询并统计最近n年经济损失的总数
        total_loss = await economic_loss_controller.get_recent_loss_total(start_year, current_year)
        # 处理 Decimal 类型
        total_loss_float = float(total_loss) if total_loss is not None else 0.0
        return SuccessExtra(data={"total_loss": total_loss_float})
    except Exception as e:
        print(f"捕获到异常: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/country-economic-loss", summary="指定时间段内各国直接经济损失")
async def country_economic_loss(
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

        country_losses = await economic_loss_controller.get_country_economic_loss(query)

        result = []
        for item in country_losses:
            result.append({
                "country": item["country"],
                "total_loss": float(item["total_loss"])
            })
        return SuccessExtra(data=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))