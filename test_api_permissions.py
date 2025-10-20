#!/usr/bin/env python3
"""
测试API权限
"""

import requests
import json

def test_api_permissions():
    """测试API权限"""
    BASE_URL = "http://localhost:9999/api/v1"
    HEADERS = {"token": "dev"}
    
    # 测试一个已知工作的API
    print("测试已知工作的API:")
    try:
        response = requests.get(f"{BASE_URL}/pcb/enterprise/7/pre-audit", headers=HEADERS)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("预审核API工作正常")
        else:
            print(f"预审核API失败: {response.text}")
    except Exception as e:
        print(f"预审核API异常: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试原辅材料API
    print("测试原辅材料API:")
    try:
        response = requests.get(f"{BASE_URL}/raw-material/materials", headers=HEADERS)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("原辅材料API工作正常")
        else:
            print(f"原辅材料API失败: {response.text}")
    except Exception as e:
        print(f"原辅材料API异常: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试工艺装备API
    print("测试工艺装备API:")
    try:
        response = requests.get(f"{BASE_URL}/process-equipment/enterprise/7/all-data", headers=HEADERS)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("工艺装备API工作正常")
        else:
            print(f"工艺装备API失败: {response.text}")
    except Exception as e:
        print(f"工艺装备API异常: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试生产数据API
    print("测试生产数据API:")
    try:
        response = requests.get(f"{BASE_URL}/pcb/enterprise/7/production-data", headers=HEADERS)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("生产数据API工作正常")
        else:
            print(f"生产数据API失败: {response.text}")
    except Exception as e:
        print(f"生产数据API异常: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试资源能源消耗API
    print("测试资源能源消耗API:")
    try:
        response = requests.get(f"{BASE_URL}/resource-consumption/enterprise/7/all-data", headers=HEADERS)
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("资源能源消耗API工作正常")
        else:
            print(f"资源能源消耗API失败: {response.text}")
    except Exception as e:
        print(f"资源能源消耗API异常: {e}")

if __name__ == "__main__":
    test_api_permissions()