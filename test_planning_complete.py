#!/usr/bin/env python3
"""
PCB筹划与组织模块完整功能测试
"""
import asyncio
import httpx
import json
from datetime import datetime, timedelta

async def test_planning_complete():
    """测试筹划与组织模块的完整功能"""
    print("=" * 60)
    print("PCB筹划与组织模块完整功能测试")
    print("=" * 60)
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            # 1. 登录获取token
            print("\n1. 登录获取token...")
            login_data = {
                'username': 'admin',
                'password': '123456'
            }
            login_response = await client.post('http://localhost:9999/api/v1/base/access_token', json=login_data)
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
            response = await client.get('http://localhost:9999/api/v1/pcb/enterprise/1/leadership-team', headers=headers)
            print(f"获取领导小组状态: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"领导小组数量: {len(data.get('data', {}).get('items', []))}")
            
            # 添加领导小组成员
            member_data = {
                "name": "测试领导",
                "position": "测试职位",
                "department": "测试部门",
                "role": "组长",
                "responsibilities": "测试职责",
                "phone": "13800138000"
            }
            response = await client.post('http://localhost:9999/api/v1/pcb/enterprise/1/leadership-team', 
                                       json=member_data, headers=headers)
            print(f"添加领导小组成员状态: {response.status_code}")
            if response.status_code == 200:
                print("领导小组成员添加成功")
            
            # 3. 测试工作小组功能
            print("\n3. 测试工作小组功能...")
            
            # 获取工作小组
            response = await client.get('http://localhost:9999/api/v1/pcb/enterprise/1/work-team', headers=headers)
            print(f"获取工作小组状态: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"工作小组数量: {len(data.get('data', {}).get('items', []))}")
            
            # 添加工作小组成员
            member_data = {
                "name": "测试工作员",
                "position": "测试职位",
                "department": "测试部门",
                "role": "成员",
                "responsibilities": "测试职责",
                "phone": "13800138001"
            }
            response = await client.post('http://localhost:9999/api/v1/pcb/enterprise/1/work-team', 
                                       json=member_data, headers=headers)
            print(f"添加工作小组成员状态: {response.status_code}")
            if response.status_code == 200:
                print("工作小组成员添加成功")
            
            # 4. 测试工作计划功能
            print("\n4. 测试工作计划功能...")
            
            # 获取工作计划
            response = await client.get('http://localhost:9999/api/v1/pcb/enterprise/1/work-plans', headers=headers)
            print(f"获取工作计划状态: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"工作计划数量: {len(data.get('data', {}).get('items', []))}")
            
            # 添加工作计划
            plan_data = {
                "stage_order": 11,
                "stage": "测试阶段",
                "work_content": "测试工作内容",
                "planned_start_date": (datetime.now() + timedelta(days=1)).isoformat(),
                "planned_end_date": (datetime.now() + timedelta(days=30)).isoformat(),
                "responsible_department": "测试部门"
            }
            response = await client.post('http://localhost:9999/api/v1/pcb/enterprise/1/work-plans', 
                                       json=plan_data, headers=headers)
            print(f"添加工作计划状态: {response.status_code}")
            if response.status_code == 200:
                print("工作计划添加成功")
            
            # 5. 测试培训记录功能
            print("\n5. 测试培训记录功能...")
            
            # 获取培训记录
            response = await client.get('http://localhost:9999/api/v1/pcb/enterprise/1/training-records', headers=headers)
            print(f"获取培训记录状态: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"培训记录数量: {len(data.get('data', {}).get('items', []))}")
            
            # 添加培训记录
            training_data = {
                "title": "测试培训",
                "date": datetime.now().isoformat(),
                "duration": 120,
                "participants": 20,
                "content": "测试培训内容",
                "instructor": "测试讲师",
                "location": "测试地点"
            }
            response = await client.post('http://localhost:9999/api/v1/pcb/enterprise/1/training-records', 
                                       json=training_data, headers=headers)
            print(f"添加培训记录状态: {response.status_code}")
            if response.status_code == 200:
                print("培训记录添加成功")
            
            print("\n" + "=" * 60)
            print("所有功能测试完成！")
            print("=" * 60)
                
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_planning_complete())
