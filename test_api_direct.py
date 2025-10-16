#!/usr/bin/env python3
"""
直接测试API路由
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings import settings
from app.api.v1.pcb_planning import get_leadership_team

async def test_api_direct():
    print("初始化数据库连接...")
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    try:
        print("测试API路由...")
        result = await get_leadership_team(7)
        print(f"API结果: {result}")
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(test_api_direct())
