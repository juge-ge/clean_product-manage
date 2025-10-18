#!/usr/bin/env python3
"""
初始化原辅材料数据库数据
"""
import asyncio
import sqlite3
import os

async def init_raw_materials():
    """初始化原辅材料数据"""
    db_path = "db.sqlite3"
    
    if not os.path.exists(db_path):
        print(f"数据库文件 {db_path} 不存在")
        return False
    
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("开始创建原辅材料相关表...")
        
        # 创建原辅材料基础信息表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS raw_materials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                name VARCHAR(200) NOT NULL,
                unit VARCHAR(50) NOT NULL,
                process VARCHAR(100) NOT NULL,
                category VARCHAR(100) NOT NULL,
                description TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # 创建企业原辅材料使用情况表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enterprise_raw_material_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                enterprise_id BIGINT NOT NULL,
                material_id BIGINT NOT NULL,
                year VARCHAR(10) NOT NULL,
                amount DECIMAL(15,2),
                unit VARCHAR(50),
                process VARCHAR(100),
                state VARCHAR(50),
                voc_content DECIMAL(5,2)
            )
        """)
        
        # 创建索引
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_raw_materials_name ON raw_materials(name)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_raw_materials_category ON raw_materials(category)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_raw_materials_process ON raw_materials(process)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_enterprise_usage_enterprise_id ON enterprise_raw_material_usage(enterprise_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_enterprise_usage_material_id ON enterprise_raw_material_usage(material_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_enterprise_usage_year ON enterprise_raw_material_usage(year)")
        
        # 插入基础材料数据
        materials_data = [
            # 基础材料
            ('覆铜板', 'm²', '开料', '基础材料', 'PCB制造的基础材料', 1),
            ('铜箔', 'kg', '电镀', '基础材料', '用于电镀工艺的铜箔', 1),
            ('底片', '张', '曝光', '基础材料', '用于图形转移的底片', 1),
            
            # 化学试剂
            ('硫酸铜', 'kg', '电镀', '化学试剂', '电镀工艺用硫酸铜', 1),
            ('蚀刻液', 'L', '蚀刻', '化学试剂', '用于蚀刻工艺的化学试剂', 1),
            ('抗蚀剂', 'L', '阻焊', '化学试剂', '用于阻焊工艺的抗蚀剂', 1),
            ('油墨', 'L', '丝印', '化学试剂', '用于丝印工艺的油墨', 1),
            ('盐酸', 'L', '清洗', '化学试剂', '用于清洗工艺的盐酸', 1),
            ('硫酸', 'L', '清洗', '化学试剂', '用于清洗工艺的硫酸', 1),
            ('氢氧化钠', 'kg', '清洗', '化学试剂', '用于清洗工艺的氢氧化钠', 1),
            
            # 辅助材料
            ('干膜', 'm²', '阻焊', '辅助材料', '用于阻焊工艺的干膜', 1),
            ('显影液', 'L', '阻焊', '辅助材料', '用于显影工艺的显影液', 1),
            ('去膜液', 'L', '阻焊', '辅助材料', '用于去膜工艺的去膜液', 1),
            ('助焊剂', 'L', '焊接', '辅助材料', '用于焊接工艺的助焊剂', 1),
            ('清洗剂', 'L', '清洗', '辅助材料', '用于清洗工艺的清洗剂', 1),
            
            # 包装材料
            ('包装纸', 'kg', '包装', '包装材料', '用于产品包装的包装纸', 1),
            ('防静电袋', '个', '包装', '包装材料', '用于防静电包装的袋子', 1),
            ('标签', '张', '包装', '包装材料', '用于产品标识的标签', 1),
        ]
        
        # 清空现有数据
        cursor.execute("DELETE FROM raw_materials")
        
        # 插入材料数据
        cursor.executemany("""
            INSERT INTO raw_materials (name, unit, process, category, description, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        """, materials_data)
        
        # 提交事务
        conn.commit()
        conn.close()
        
        print(f"成功创建原辅材料相关表并插入 {len(materials_data)} 条基础数据")
        return True
        
    except Exception as e:
        print(f"创建原辅材料表失败: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(init_raw_materials())
