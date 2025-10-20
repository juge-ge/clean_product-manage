#!/usr/bin/env python3
"""
测试API实现
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings

async def test_api_implementation():
    """测试API实现"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models']}
        )
        
        # 测试生产数据API实现
        print("测试生产数据API实现:")
        try:
            from app.api.v1.pcb_production import get_production_data
            from app.core.dependency import DependAuth
            
            # 创建一个模拟的用户对象
            from app.models import User
            user = await User.filter().first()
            
            # 直接调用API函数
            result = await get_production_data(7, user)
            print(f"  生产数据API调用成功: {result}")
        except Exception as e:
            print(f"  生产数据API调用失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 测试资源能源消耗API实现
        print("\n测试资源能源消耗API实现:")
        try:
            from app.api.v1.resource_consumption import get_all_resource_consumption_data
            
            # 直接调用API函数
            result = await get_all_resource_consumption_data(7, user)
            print(f"  资源能源消耗API调用成功: {result}")
        except Exception as e:
            print(f"  资源能源消耗API调用失败: {e}")
            import traceback
            traceback.print_exc()
        
        await Tortoise.close_connections()
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_api_implementation())
