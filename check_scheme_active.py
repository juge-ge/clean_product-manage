#!/usr/bin/env python3
"""
检查方案的is_active字段
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme


async def check_scheme_active():
    """检查方案的is_active字段"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取所有方案
        all_schemes = await PCBScheme.all().count()
        print(f"总方案数: {all_schemes}")
        
        # 获取激活的方案
        active_schemes = await PCBScheme.filter(is_active=True).count()
        print(f"激活方案数: {active_schemes}")
        
        # 获取非激活的方案
        inactive_schemes = await PCBScheme.filter(is_active=False).count()
        print(f"非激活方案数: {inactive_schemes}")
        
        # 获取is_active为None的方案
        null_schemes = await PCBScheme.filter(is_active__isnull=True).count()
        print(f"is_active为NULL的方案数: {null_schemes}")
        
        # 显示前5个方案的is_active状态
        print("\n前5个方案的is_active状态:")
        schemes = await PCBScheme.all().limit(5)
        for scheme in schemes:
            print(f"  方案{scheme.scheme_id}: is_active = {scheme.is_active}")
        
    except Exception as e:
        print(f"检查失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_scheme_active())
