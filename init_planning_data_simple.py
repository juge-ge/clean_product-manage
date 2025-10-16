#!/usr/bin/env python3
"""
初始化PCB筹划与组织模块的示例数据 - 简化版本
"""
import sqlite3
import os
from datetime import datetime

def init_planning_data():
    """初始化筹划与组织示例数据"""
    print("开始初始化PCB筹划与组织示例数据...")
    
    # 连接数据库
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 获取现有企业
        cursor.execute("SELECT id, name FROM pcb_enterprise WHERE is_deleted = 0 LIMIT 1")
        enterprise = cursor.fetchone()
        if not enterprise:
            print("没有找到企业数据，请先创建企业")
            return
        
        enterprise_id, enterprise_name = enterprise
        print(f"为企业 '{enterprise_name}' 初始化筹划与组织数据...")
        
        # 1. 初始化领导小组数据
        print("初始化领导小组数据...")
        leadership_team_data = [
            (enterprise_id, "张三", "总经理", "总经理办公室", "组长", "负责清洁生产审核工作的总体协调和决策", "13800138000"),
            (enterprise_id, "李四", "副总经理", "总经理办公室", "副组长", "协助组长开展清洁生产审核工作", "13800138001"),
            (enterprise_id, "王五", "环保部经理", "环保部", "成员", "负责环保相关工作的具体实施", "13800138002")
        ]
        
        cursor.executemany("""
            INSERT INTO pcb_leadership_team 
            (enterprise_id, name, position, department, role, responsibilities, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, leadership_team_data)
        
        # 2. 初始化工作小组数据
        print("初始化工作小组数据...")
        work_team_data = [
            (enterprise_id, "赵六", "生产部经理", "生产部", "组长", "负责生产环节的清洁生产改进工作", "13800138003"),
            (enterprise_id, "钱七", "技术部经理", "技术部", "副组长", "负责技术改进和工艺优化", "13800138004"),
            (enterprise_id, "孙八", "设备部经理", "设备部", "成员", "负责设备维护和改造", "13800138005"),
            (enterprise_id, "周九", "质量部经理", "质量部", "成员", "负责质量控制和检测", "13800138006")
        ]
        
        cursor.executemany("""
            INSERT INTO pcb_work_team 
            (enterprise_id, name, position, department, role, responsibilities, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, work_team_data)
        
        # 3. 初始化工作计划数据
        print("初始化工作计划数据...")
        work_plans_data = [
            (enterprise_id, 1, "审核准备", "成立清洁生产审核领导小组和工作小组，制定审核计划", "2024-01-15T00:00:00", "2024-01-31T00:00:00", "总经理办公室", "2024-01-15T00:00:00", "2024-01-30T00:00:00"),
            (enterprise_id, 2, "预审核", "收集企业基础资料，进行现状调研和问题识别", "2024-02-01T00:00:00", "2024-02-28T00:00:00", "环保部", "2024-02-01T00:00:00", None),
            (enterprise_id, 3, "审核", "对64项指标进行详细审核和评估", "2024-03-01T00:00:00", "2024-03-31T00:00:00", "技术部", None, None),
            (enterprise_id, 4, "方案制定", "制定清洁生产改进方案和实施计划", "2024-04-01T00:00:00", "2024-04-30T00:00:00", "生产部", None, None),
            (enterprise_id, 5, "方案实施", "按照制定的方案进行清洁生产改进", "2024-05-01T00:00:00", "2024-08-31T00:00:00", "设备部", None, None),
            (enterprise_id, 6, "效果评估", "评估清洁生产改进效果和效益", "2024-09-01T00:00:00", "2024-09-30T00:00:00", "质量部", None, None),
            (enterprise_id, 7, "持续改进", "建立持续改进机制，确保清洁生产水平不断提升", "2024-10-01T00:00:00", "2024-10-31T00:00:00", "环保部", None, None),
            (enterprise_id, 8, "报告编制", "编制清洁生产审核报告", "2024-11-01T00:00:00", "2024-11-30T00:00:00", "技术部", None, None),
            (enterprise_id, 9, "报告审核", "对审核报告进行内部审核和外部审核", "2024-12-01T00:00:00", "2024-12-15T00:00:00", "总经理办公室", None, None),
            (enterprise_id, 10, "总结验收", "总结审核工作，进行验收和归档", "2024-12-16T00:00:00", "2024-12-31T00:00:00", "总经理办公室", None, None)
        ]
        
        cursor.executemany("""
            INSERT INTO pcb_work_plans 
            (enterprise_id, stage_order, stage, work_content, planned_start_date, planned_end_date, responsible_department, actual_start_date, actual_end_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, work_plans_data)
        
        # 4. 初始化培训记录数据
        print("初始化培训记录数据...")
        training_records_data = [
            (enterprise_id, "清洁生产基础培训", "2024-01-20T09:00:00", 120, 30, "清洁生产基本概念、法律法规、审核流程等基础知识的培训", "李四", "公司会议室"),
            (enterprise_id, "清洁生产审核方法培训", "2024-02-10T14:00:00", 180, 25, "清洁生产审核的具体方法、工具使用、数据收集等实操培训", "王五", "培训中心"),
            (enterprise_id, "清洁生产技术方案培训", "2024-03-05T10:00:00", 150, 20, "清洁生产技术方案的选择、实施和效果评估方法培训", "赵六", "技术部会议室")
        ]
        
        cursor.executemany("""
            INSERT INTO pcb_training_records 
            (enterprise_id, title, date, duration, participants, content, instructor, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, training_records_data)
        
        # 提交事务
        conn.commit()
        print("筹划与组织示例数据初始化完成!")
        
        # 统计数据
        cursor.execute("SELECT COUNT(*) FROM pcb_leadership_team WHERE enterprise_id = ?", (enterprise_id,))
        leadership_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pcb_work_team WHERE enterprise_id = ?", (enterprise_id,))
        work_team_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pcb_work_plans WHERE enterprise_id = ?", (enterprise_id,))
        work_plans_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM pcb_training_records WHERE enterprise_id = ?", (enterprise_id,))
        training_count = cursor.fetchone()[0]
        
        print(f"\n数据统计:")
        print(f"  领导小组成员: {leadership_count} 人")
        print(f"  工作小组成员: {work_team_count} 人")
        print(f"  工作计划阶段: {work_plans_count} 个")
        print(f"  培训记录: {training_count} 条")
        
    except Exception as e:
        print(f"初始化数据时出错: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    init_planning_data()
