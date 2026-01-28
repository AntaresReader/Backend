"""Users 其他功能路由"""
from fastapi import APIRouter, Query

router = APIRouter()

@router.get("")
async def get_user_profile():
    """获取用户配置文件"""
    return {"profiles": ["profile1", "profile2"]}

@router.post("")
async def update_user_profile(profile_name: str = Query(...)):
    """更新用户配置文件"""
    return {"message": f"Updated profile: {profile_name}"}
