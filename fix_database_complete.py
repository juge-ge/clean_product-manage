#!/usr/bin/env python3
"""
彻底修复PCB数据库中的Decimal字段问题
"""
import asyncio
import sqlite3
from tortoise import Tortoise
from app.settings import settings

async def fix_database_complete():
    """彻底修复数据库中的Decimal字段问题"""
    print("开始彻底修复数据库...")
    
    # 初始化数据库连接
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    # 获取数据库连接
    conn = Tortoise.get_connection("sqlite")
    
    try:
        # 检查表结构
        result = await conn.execute_query("PRAGMA table_info(pcb_enterprise)")
        print("当前表结构:")
        for row in result[1]:
            print(f"  {row[1]} {row[2]}")
        
        # 检查是否有数据
        result = await conn.execute_query("SELECT COUNT(*) FROM pcb_enterprise")
        count = result[1][0][0]
        print(f"企业表中有 {count} 条记录")
        
        if count > 0:
            # 修复所有可能的Decimal字段问题
            print("修复Decimal字段...")
            
            # 更新所有空字符串或无效值为NULL
            await conn.execute_query("UPDATE pcb_enterprise SET capital = NULL WHERE capital = '' OR capital = 'None' OR capital = 'null'")
            await conn.execute_query("UPDATE pcb_enterprise SET capacity = NULL WHERE capacity = '' OR capacity = 'None' OR capacity = 'null'")
            
            # 检查并修复任何非数字的capital值
            await conn.execute_query("UPDATE pcb_enterprise SET capital = NULL WHERE capital NOT GLOB '*[0-9]*' AND capital IS NOT NULL")
            
            # 检查并修复任何非数字的capacity值
            await conn.execute_query("UPDATE pcb_enterprise SET capacity = NULL WHERE capacity NOT GLOB '*[0-9]*' AND capacity IS NOT NULL")
            
            print("Decimal字段修复完成")
            
            # 验证修复结果
            result = await conn.execute_query("SELECT id, name, capital, capacity FROM pcb_enterprise LIMIT 5")
            print("修复后的前5条记录:")
            for row in result[1]:
                print(f"  ID: {row[0]}, Name: {row[1]}, Capital: {row[2]}, Capacity: {row[3]}")
        
        print("数据库彻底修复完成!")
        
    except Exception as e:
        print(f"修复过程中出错: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(fix_database_complete())
