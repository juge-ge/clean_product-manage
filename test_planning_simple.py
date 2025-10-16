#!/usr/bin/env python3
"""
PCB筹划与组织模块简单功能测试
"""
import requests
import json
from datetime import datetime, timedelta

def test_planning_simple():
    """测试筹划与组织模块的简单功能"""
    print("=" * 60)
    print("PCB筹划与组织模块简单功能测试")
    print("=" * 60)
    
    try:
        # 1. 登录获取token
        print("\n1. 登录获取token...")
        login_data = {
            'username': 'admin',
            'password': '123456'
        }
        login_response = requests.post('http://localhost:9999/api/v1/base/access_token', 
                                     json=login_data, timeout=10)
        print(f"登录状态: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"登录失败: {login_response.text}")
            return
        
        token_data = login_response.json()
        token = token_data.get('data', {}).get('access_token')
        print(f"Token获取成功: {token[:20]}...")
        
        headers = {'token': token}
        
        # 2. 测试领导小组功能
        print("\n2. 测试领导小组功能...")
        
        # 获取领导小组
        response = requests.get('http://localhost:9999/api/v1/pcb/enterprise/1/leadership-team', 
                              headers=headers, timeout=10)
        print(f"获取领导小组状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"领导小组数量: {len(data.get('data', {}).get('items', []))}")
        else:
            print(f"获取领导小组失败: {response.text}")
        
        # 添加领导小组成员
        member_data = {
            "name": "测试领导",
            "position": "测试职位",
            "department": "测试部门",
            "role": "组长",
            "responsibilities": "测试职责",
            "phone": "13800138000"
        }
        response = requests.post('http://localhost:9999/api/v1/pcb/enterprise/1/leadership-team', 
                               json=member_data, headers=headers, timeout=10)
        print(f"添加领导小组成员状态: {response.status_code}")
        if response.status_code == 200:
            print("领导小组成员添加成功")
        else:
            print(f"添加领导小组成员失败: {response.text}")
        
        # 3. 测试工作小组功能
        print("\n3. 测试工作小组功能...")
        
        # 获取工作小组
        response = requests.get('http://localhost:9999/api/v1/pcb/enterprise/1/work-team', 
                              headers=headers, timeout=10)
        print(f"获取工作小组状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"工作小组数量: {len(data.get('data', {}).get('items', []))}")
        else:
            print(f"获取工作小组失败: {response.text}")
        
        # 4. 测试工作计划功能
        print("\n4. 测试工作计划功能...")
        
        # 获取工作计划
        response = requests.get('http://localhost:9999/api/v1/pcb/enterprise/1/work-plans', 
                              headers=headers, timeout=10)
        print(f"获取工作计划状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"工作计划数量: {len(data.get('data', {}).get('items', []))}")
        else:
            print(f"获取工作计划失败: {response.text}")
        
        # 5. 测试培训记录功能
        print("\n5. 测试培训记录功能...")
        
        # 获取培训记录
        response = requests.get('http://localhost:9999/api/v1/pcb/enterprise/1/training-records', 
                              headers=headers, timeout=10)
        print(f"获取培训记录状态: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"培训记录数量: {len(data.get('data', {}).get('items', []))}")
        else:
            print(f"获取培训记录失败: {response.text}")
        
        print("\n" + "=" * 60)
        print("所有功能测试完成！")
        print("=" * 60)
                
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_planning_simple()
