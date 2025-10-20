#!/usr/bin/env python3
"""
测试预审核模块的API接口
"""

import requests
import json

BASE_URL = "http://localhost:9999/api/v1"
HEADERS = {"token": "dev"}

def test_api(endpoint, method="GET", data=None):
    """测试API接口"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n测试 {method} {endpoint}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(url, headers=HEADERS, json=data)
        elif method == "PUT":
            response = requests.put(url, headers=HEADERS, json=data)
        
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("成功")
            try:
                result = response.json()
                print(f"响应数据: {json.dumps(result, ensure_ascii=False, indent=2)[:200]}...")
            except:
                print(f"响应内容: {response.text[:200]}...")
        else:
            print("失败")
            print(f"错误信息: {response.text}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"请求异常: {e}")
        return False

def main():
    print("=" * 60)
    print("测试预审核模块API接口")
    print("=" * 60)
    
    # 测试原辅材料API
    print("\n1. 测试原辅材料API")
    test_api("/raw-material/materials")
    
    # 测试生产数据API
    print("\n2. 测试生产数据API")
    test_api("/pcb/enterprise/7/production-data")
    
    # 测试资源能源消耗API
    print("\n3. 测试资源能源消耗API")
    test_api("/resource-consumption/enterprise/7/all-data")
    
    # 测试工艺装备API
    print("\n4. 测试工艺装备API")
    test_api("/process-equipment/enterprise/7/all-data")
    
    # 测试污染防治API
    print("\n5. 测试污染防治API")
    test_api("/pollution-control/enterprise/7/all-data")
    
    # 测试固体废物API
    print("\n6. 测试固体废物API")
    test_api("/solid-waste/enterprise/7/all-data")
    
    # 测试自行监测API
    print("\n7. 测试自行监测API")
    test_api("/self-monitoring/enterprise/7/all-data")
    
    # 测试预审核数据API
    print("\n8. 测试预审核数据API")
    test_api("/pcb/enterprise/7/pre-audit")

if __name__ == "__main__":
    main()