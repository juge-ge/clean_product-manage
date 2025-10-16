#!/usr/bin/env python3
"""
检查数据库数据
"""
import sqlite3

def check_data():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # 检查企业表
    print("企业表数据:")
    cursor.execute("SELECT id, name FROM pcb_enterprise LIMIT 5")
    enterprises = cursor.fetchall()
    for enterprise in enterprises:
        print(f"  ID: {enterprise[0]}, 名称: {enterprise[1]}")
    
    # 检查领导小组表
    print("\n领导小组表数据:")
    cursor.execute("SELECT id, enterprise_id, name, role FROM pcb_leadership_team")
    members = cursor.fetchall()
    for member in members:
        print(f"  ID: {member[0]}, 企业ID: {member[1]}, 姓名: {member[2]}, 角色: {member[3]}")
    
    # 检查工作小组表
    print("\n工作小组表数据:")
    cursor.execute("SELECT id, enterprise_id, name, role FROM pcb_work_team")
    members = cursor.fetchall()
    for member in members:
        print(f"  ID: {member[0]}, 企业ID: {member[1]}, 姓名: {member[2]}, 角色: {member[3]}")
    
    # 检查工作计划表
    print("\n工作计划表数据:")
    cursor.execute("SELECT id, enterprise_id, stage_order, stage FROM pcb_work_plans")
    plans = cursor.fetchall()
    for plan in plans:
        print(f"  ID: {plan[0]}, 企业ID: {plan[1]}, 阶段: {plan[2]}, 名称: {plan[3]}")
    
    # 检查培训记录表
    print("\n培训记录表数据:")
    cursor.execute("SELECT id, enterprise_id, title FROM pcb_training_records")
    records = cursor.fetchall()
    for record in records:
        print(f"  ID: {record[0]}, 企业ID: {record[1]}, 标题: {record[2]}")
    
    conn.close()

if __name__ == "__main__":
    check_data()
