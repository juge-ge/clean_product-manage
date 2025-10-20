#!/usr/bin/env python3
"""
详细测试API权限
"""

import requests
import json

def test_api_permissions_detailed():
    """详细测试API权限"""
    BASE_URL = "http://localhost:9999/api/v1"
    HEADERS = {"token": "dev"}
    
    # 测试生产数据API
    print("测试生产数据API:")
    try:
        response = requests.get(f"{BASE_URL}/pcb/enterprise/7/production-data", headers=HEADERS)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            except:
                print("不是JSON格式")
    except Exception as e:
        print(f"请求异常: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试资源能源消耗API
    print("测试资源能源消耗API:")
    try:
        response = requests.get(f"{BASE_URL}/resource-consumption/enterprise/7/all-data", headers=HEADERS)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"JSON数据: {json.dumps(data, ensure_ascii=False, indent=2)}")
            except:
                print("不是JSON格式")
    except Exception as e:
        print(f"请求异常: {e}")

if __name__ == "__main__":
    test_api_permissions_detailed()
