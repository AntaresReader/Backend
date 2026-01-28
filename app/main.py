from fastapi import FastAPI
from app.antares import antares

app = FastAPI(title="Antares API")

# 自动注册所有 Antares 路由
print("\n=== 正在加载 Antares 路由 ===")
antares.register_routes(app)
print("=== 路由加载完成 ===\n")

@app.get("/")
async def root():
    return {"message": "Antares Server"}
