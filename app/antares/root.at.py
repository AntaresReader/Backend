"""Antares 根路由"""
from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def antares_root():
    """Antares 根端点"""
    return {"message": "Welcome to Antares"}
