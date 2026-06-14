"""
#用户名 : 17954
#日期 : 2025/4/28 13:46
"""
from fastapi import APIRouter, Query, HTTPException
import json
from app.schemas import Success

router = APIRouter()

@router.get("/list", summary="获取所有灾害关联规则")
async def get_all_rules():
    try:
        with open("app/api/v1/association/disaster_association_rules.json", "r") as f:
            disaster_rules = json.load(f)
        return Success(data=disaster_rules)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")

@router.get("/get", summary="根据灾害类型获取关联规则")
async def get_rules_by_type(disaster_type: str):
    try:
        with open("app/api/v1/association/disaster_association_rules.json", "r") as f:
            disaster_rules = json.load(f)
        filtered_rules = [
            rule for rule in disaster_rules
            if disaster_type in rule["antecedents"] or disaster_type in rule["consequents"]
        ]
        if not filtered_rules:
            raise HTTPException(status_code=404, detail="No rules found for this disaster type")
        return Success(data=filtered_rules)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database Error: {str(e)}")