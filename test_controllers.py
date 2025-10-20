#!/usr/bin/env python3
"""
测试控制器
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings

async def test_controllers():
    """测试控制器"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models']}
        )
        
        # 测试生产数据控制器
        print("测试生产数据控制器:")
        try:
            from app.controllers.pcb_production import pcb_production_data_controller
            data = await pcb_production_data_controller.get_all_production_data(7)
            print(f"  生产数据: {data}")
        except Exception as e:
            print(f"  生产数据控制器失败: {e}")
        
        # 测试资源能源消耗控制器
        print("\n测试资源能源消耗控制器:")
        try:
            from app.controllers.resource_consumption import resource_consumption_data_controller
            data = await resource_consumption_data_controller.get_all_data(7)
            print(f"  资源能源消耗数据: {data}")
        except Exception as e:
            print(f"  资源能源消耗控制器失败: {e}")
        
        await Tortoise.close_connections()
        
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_controllers())
