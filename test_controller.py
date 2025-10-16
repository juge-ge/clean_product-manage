#!/usr/bin/env python3
"""
测试控制器
"""
import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings import settings
from app.controllers.pcb_planning import pcb_leadership_team_controller

async def test_controller():
    print("初始化数据库连接...")
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    try:
        print("测试获取领导小组...")
        members = await pcb_leadership_team_controller.get_by_enterprise(1)
        print(f"获取到 {len(members)} 个成员")
        
        for member in members:
            print(f"成员: {member.name}, 角色: {member.role}")
            member_dict = await member.to_dict()
            print(f"转换为字典: {member_dict}")
            
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(test_controller())
