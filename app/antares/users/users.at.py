"""Users 路由"""
from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def get_users():
    """获取所有用户"""
    return {
        "users": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
    }

@router.get("/{user_id:int}")
async def get_user(user_id: int):
    """获取单个用户"""
    return {"user_id": user_id, "name": f"User {user_id}"}

@router.post("")
async def create_user(name: str):
    """创建用户"""
    return {"message": f"Created user: {name}"}
