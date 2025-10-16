#!/usr/bin/env python3
"""
检查数据库表
"""
import sqlite3

def check_database():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # 检查PCB相关表
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'pcb_%'")
    tables = cursor.fetchall()
    
    print("PCB相关表:")
    for table in tables:
        print(f"  - {table[0]}")
    
    # 检查每个表的数据
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  {table_name}: {count} 条记录")
    
    conn.close()

if __name__ == "__main__":
    check_database()
