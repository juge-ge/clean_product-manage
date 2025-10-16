#!/usr/bin/env python3
"""
检查用户数据
"""
import sqlite3

def check_users():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    
    # 检查用户表
    print("用户表数据:")
    cursor.execute("SELECT id, username, is_superuser FROM user LIMIT 5")
    users = cursor.fetchall()
    for user in users:
        print(f"  ID: {user[0]}, 用户名: {user[1]}, 超级用户: {user[2]}")
    
    # 检查角色表
    print("\n角色表数据:")
    cursor.execute("SELECT id, name FROM role LIMIT 5")
    roles = cursor.fetchall()
    for role in roles:
        print(f"  ID: {role[0]}, 角色名: {role[1]}")
    
    # 检查用户角色关系
    print("\n用户角色关系:")
    cursor.execute("SELECT user_id, role_id FROM user_role LIMIT 5")
    user_roles = cursor.fetchall()
    for user_role in user_roles:
        print(f"  用户ID: {user_role[0]}, 角色ID: {user_role[1]}")
    
    conn.close()

if __name__ == "__main__":
    check_users()
