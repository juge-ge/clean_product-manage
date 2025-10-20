#!/usr/bin/env python3
"""
测试DependAuth
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings

async def test_depend_auth():
    """测试DependAuth"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models']}
        )
        
        # 测试DependAuth
        print("测试DependAuth:")
        try:
            from app.core.dependency import AuthControl
            user = await AuthControl.is_authed("dev")
            print(f"  用户: {user}")
            print(f"  用户ID: {user.id if user else None}")
        except Exception as e:
            print(f"  DependAuth失败: {e}")
            import traceback
            traceback.print_exc()
        
        await Tortoise.close_connections()
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_depend_auth())
