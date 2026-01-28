# FastAPI Antares 项目

基于 FastAPI 的自动路由注册系统，支持热重载。

## 项目结构

```
.
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI 应用主文件
│   ├── config.py         # 配置文件
│   └── antares/          # 路由根目录
│       ├── __init__.py   # Antares 路由注册器
│       ├── root.at.py    # 根路由 -> /root
│       └── users/
│           ├── users.at.py      # -> /users
│           └── users1.at.py     # -> /users/users1
├── requirements.txt
├── .env.example
├── run.bat / run.ps1 / run.py  # 启动脚本
└── README.md
```

## 路由映射规则

文件名格式：`*.at.py`

映射规则：
- `antares/users/users.at.py` → `/users`（文件名与目录名相同，省略文件名）
- `antares/users/users1.at.py` → `/users/users1`（文件名不同，加上文件名）
- `antares/root.at.py` → `/root`
- `antares/admin/dashboard/dashboard.at.py` → `/admin/dashboard`
- `antares/admin/dashboard/analytics.at.py` → `/admin/dashboard/analytics`

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行应用

```bash
uvicorn app.main:app --reload
```

应用将在 http://localhost:8000 运行

### 3. 创建新路由

在 `app/antares/` 目录下创建 `.at.py` 文件：

```python
# app/antares/posts/posts.at.py
from fastapi import APIRouter

router = APIRouter()

@router.get("")
async def get_posts():
    return {"posts": []}

@router.post("")
async def create_post(title: str):
    return {"message": f"Created: {title}"}
```

保存后，自动生效！路由为 `/posts`

### 4. 查看 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API 示例

```bash
# 获取所有用户
curl http://localhost:8000/users

# 获取单个用户
curl http://localhost:8000/users/1

# 获取用户配置
curl http://localhost:8000/users/users1

# 创建用户
curl -X POST http://localhost:8000/users?name=Charlie
```
