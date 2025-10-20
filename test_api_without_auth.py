#!/usr/bin/env python3
"""
测试API（不使用认证）
"""

import requests
import json

BASE_URL = "http://localhost:9999/api/v1"

def test_api_without_auth(endpoint, method="GET", data=None):
    """测试API接口（不使用认证）"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n测试 {method} {endpoint} (无认证)")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            print("成功")
            try:
                result = response.json()
                print(f"响应数据: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}...")
            except:
                print(f"响应内容: {response.text[:500]}...")
        else:
            print("失败")
            print(f"错误信息: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"请求异常: {e}")
        return False

def main():
    print("=" * 60)
    print("测试API（不使用认证）")
    print("=" * 60)
    
    # 测试生产数据API
    print("\n1. 测试生产数据API")
    test_api_without_auth("/pcb/enterprise/7/production-data")
    
    # 测试资源能源消耗API
    print("\n2. 测试资源能源消耗API")
    test_api_without_auth("/resource-consumption/enterprise/7/all-data")

if __name__ == "__main__":
    main()
