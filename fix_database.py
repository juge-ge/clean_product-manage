#!/usr/bin/env python3
"""
修复PCB数据库中的Decimal字段问题
"""
import asyncio
import sqlite3
from tortoise import Tortoise
from app.settings import settings

async def fix_database():
    """修复数据库中的Decimal字段问题"""
    print("开始修复数据库...")
    
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
            # 检查是否有问题数据
            try:
                result = await conn.execute_query("SELECT id, name, capital, capacity FROM pcb_enterprise LIMIT 5")
                print("前5条记录:")
                for row in result[1]:
                    print(f"  ID: {row[0]}, Name: {row[1]}, Capital: {row[2]}, Capacity: {row[3]}")
            except Exception as e:
                print(f"查询数据时出错: {e}")
                
                # 尝试修复数据
                print("尝试修复数据...")
                
                # 更新无效的Decimal值
                await conn.execute_query("UPDATE pcb_enterprise SET capital = NULL WHERE capital = '' OR capital = 'None'")
                await conn.execute_query("UPDATE pcb_enterprise SET capacity = NULL WHERE capacity = '' OR capacity = 'None'")
                
                print("数据修复完成")
        
        # 检查表是否需要添加新字段
        result = await conn.execute_query("PRAGMA table_info(pcb_enterprise)")
        columns = [row[1] for row in result[1]]
        
        if 'unified_social_credit_code' not in columns:
            print("添加 unified_social_credit_code 字段...")
            await conn.execute_query("ALTER TABLE pcb_enterprise ADD COLUMN unified_social_credit_code VARCHAR(50)")
            
        if 'capital' not in columns:
            print("添加 capital 字段...")
            await conn.execute_query("ALTER TABLE pcb_enterprise ADD COLUMN capital DECIMAL(15,2)")
            
        print("数据库修复完成!")
        
    except Exception as e:
        print(f"修复过程中出错: {e}")
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(fix_database())
