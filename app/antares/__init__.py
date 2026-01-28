"""Antares 路由注册系统"""
import os
import sys
import importlib.util
from pathlib import Path
from typing import Dict, List, Any
from fastapi import APIRouter

class AntaresRouter:
    """全局路由注册器"""
    
    def __init__(self):
        self.routers: Dict[str, APIRouter] = {}
        self.modules: Dict[str, Any] = {}
        self._antares_path = Path(__file__).parent
        
    def _get_route_path(self, file_path: Path) -> str:
        """根据文件路径生成路由路径
        
        示例：
        - users/users.at.py → /users
        - users/users1.at.py → /users/users1
        - admin/dashboard/dashboard.at.py → /admin/dashboard
        - admin/dashboard/analytics.at.py → /admin/dashboard/analytics
        """
        relative_path = file_path.relative_to(self._antares_path)
        
        # 移除 .at.py 后缀，得到真实文件名
        filename_with_suffix = relative_path.name  # users.at.py
        filename = filename_with_suffix.replace('.at.py', '')  # users
        
        parts = list(relative_path.parts[:-1])  # 目录部分
        
        # 获取父目录名
        if parts:
            parent_dir = parts[-1]
            # 如果文件名和父目录名相同，只用目录路径
            if filename == parent_dir:
                route = "/" + "/".join(parts)
            else:
                # 否则加上文件名
                route = "/" + "/".join(parts + [filename])
        else:
            route = "/" + filename
            
        return route
    
    def _import_module(self, file_path: Path) -> Any:
        """动态导入模块"""
        module_name = f"antares_{file_path.stem}_{hash(str(file_path))}"
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    
    def load_routes(self) -> Dict[str, APIRouter]:
        """扫描并加载所有 .at.py 文件"""
        at_files = list(self._antares_path.glob("**/*.at.py"))
        
        for file_path in at_files:
            try:
                route_path = self._get_route_path(file_path)
                module = self._import_module(file_path)
                
                # 查找模块中的 router 对象
                if hasattr(module, 'router') and isinstance(module.router, APIRouter):
                    self.routers[route_path] = module.router
                    self.modules[route_path] = module
                    print(f"✓ 注册路由: {route_path} <- {file_path.relative_to(self._antares_path)}")
                else:
                    print(f"⚠ 警告: {file_path.relative_to(self._antares_path)} 中未找到 router 对象")
            except Exception as e:
                print(f"✗ 加载失败: {file_path.relative_to(self._antares_path)} - {e}")
        
        return self.routers
    
    def register_routes(self, app) -> None:
        """将所有路由注册到 FastAPI 应用"""
        routers = self.load_routes()
        for route_path, router in routers.items():
            app.include_router(router, prefix=route_path)
            print(f"  已包含: {route_path}")
    
    def get_routers(self) -> Dict[str, APIRouter]:
        """获取已加载的所有路由"""
        return self.routers

# 全局实例
antares = AntaresRouter()
