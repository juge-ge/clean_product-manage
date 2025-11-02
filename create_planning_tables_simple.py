 #!/usr/bin/env python3
"""
创建PCB筹划与组织相关的数据库表 - 简化版本
"""
import sqlite3
import os

def create_planning_tables():
    """创建筹划与组织相关的数据库表"""
    print("开始创建PCB筹划与组织数据库表...")
    
    # 连接数据库
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. 创建领导小组表
        print("创建领导小组表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pcb_leadership_team (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enterprise_id INTEGER NOT NULL,
                name VARCHAR(100) NOT NULL,
                position VARCHAR(100),
                department VARCHAR(100),
                role VARCHAR(50) NOT NULL,
                responsibilities TEXT,
                phone VARCHAR(20),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_leadership_enterprise_role 
            ON pcb_leadership_team(enterprise_id, role)
        """)
        
        # 2. 创建工作小组表
        print("创建工作小组表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pcb_work_team (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enterprise_id INTEGER NOT NULL,
                name VARCHAR(100) NOT NULL,
                position VARCHAR(100),
                department VARCHAR(100),
                role VARCHAR(50) NOT NULL,
                responsibilities TEXT,
                phone VARCHAR(20),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_work_team_enterprise_role 
            ON pcb_work_team(enterprise_id, role)
        """)
        
        # 3. 创建工作计划表
        print("创建工作计划表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pcb_work_plans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enterprise_id INTEGER NOT NULL,
                stage_order INTEGER NOT NULL,
                stage VARCHAR(100) NOT NULL,
                work_content TEXT,
                planned_start_date DATETIME,
                planned_end_date DATETIME,
                responsible_department VARCHAR(100),
                actual_start_date DATETIME,
                actual_end_date DATETIME,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建唯一索引和普通索引
        cursor.execute("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_work_plans_enterprise_stage 
            ON pcb_work_plans(enterprise_id, stage_order)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_work_plans_enterprise 
            ON pcb_work_plans(enterprise_id)
        """)
        
        # 4. 创建培训记录表
        print("创建培训记录表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pcb_training_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enterprise_id INTEGER NOT NULL,
                title VARCHAR(200) NOT NULL,
                date DATETIME NOT NULL,
                duration INTEGER,
                participants INTEGER,
                content TEXT,
                instructor VARCHAR(100),
                location VARCHAR(200),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_training_enterprise_date 
            ON pcb_training_records(enterprise_id, date)
        """)
        
        # 5. 创建培训图片表
        print("创建培训图片表...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pcb_training_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                training_id INTEGER NOT NULL,
                image_path TEXT NOT NULL,
                image_name VARCHAR(200),
                image_size INTEGER,
                upload_time DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_training_images_training 
            ON pcb_training_images(training_id)
        """)
        
        # 提交事务
        conn.commit()
        print("所有筹划与组织相关表创建完成!")
        
        # 验证表是否创建成功
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE 'pcb_%' 
            ORDER BY name
        """)
        
        tables = cursor.fetchall()
        print("\n当前PCB相关表:")
        for table in tables:
            print(f"  - {table[0]}")
            
    except Exception as e:
        print(f"创建表时出错: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    create_planning_tables()
