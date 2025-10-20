#!/usr/bin/env python3
"""
测试API路由
"""

import requests
import json

def test_api_routes():
    """测试API路由"""
    BASE_URL = "http://localhost:9999/api/v1"
    HEADERS = {"token": "dev"}
    
    # 测试不同的企业ID
    enterprise_ids = [1, 7, 8, 9, 10]
    
    for enterprise_id in enterprise_ids:
        print(f"\n测试企业ID: {enterprise_id}")
        
        # 测试生产数据API
        try:
            response = requests.get(f"{BASE_URL}/pcb/enterprise/{enterprise_id}/production-data", headers=HEADERS)
            print(f"  生产数据API: {response.status_code}")
            if response.status_code != 200:
                print(f"    错误: {response.text}")
        except Exception as e:
            print(f"  生产数据API异常: {e}")
        
        # 测试资源能源消耗API
        try:
            response = requests.get(f"{BASE_URL}/resource-consumption/enterprise/{enterprise_id}/all-data", headers=HEADERS)
            print(f"  资源能源消耗API: {response.status_code}")
            if response.status_code != 200:
                print(f"    错误: {response.text}")
        except Exception as e:
            print(f"  资源能源消耗API异常: {e}")

if __name__ == "__main__":
    test_api_routes()
