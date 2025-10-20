#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试预审核模块所有API接口
"""

import requests
import json

BASE_URL = "http://localhost:9999/api/v1"
ENTERPRISE_ID = 11
TOKEN = None


def get_token():
    """获取访问token"""
    global TOKEN
    print("\n" + "="*80)
    print("Logging in to get token...")
    print("="*80)
    
    try:
        response = requests.post(
            f"{BASE_URL}/base/login",
            json={"username": "admin", "password": "123456"},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            TOKEN = result.get('data', {}).get('token')
            if TOKEN:
                print(f"Login successful! Token: {TOKEN[:20]}...")
                return True
            else:
                print("Login failed: No token in response")
                return False
        else:
            print(f"Login failed: {response.text}")
            return False
    except Exception as e:
        print(f"Login error: {str(e)}")
        return False


def test_api(method, endpoint, data=None, desc=""):
    """测试API接口"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*80}")
    print(f"Testing: {desc}")
    print(f"Method: {method}")
    print(f"URL: {url}")
    print('='*80)
    
    headers = {}
    if TOKEN:
        headers['token'] = TOKEN
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code < 400:
            result = response.json()
            print(f"Response: {json.dumps(result, ensure_ascii=False, indent=2)[:500]}...")
            return True
        else:
            print(f"Error: {response.text[:500]}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("ERROR: Cannot connect to server. Is it running on port 9999?")
        return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False


def main():
    """执行所有API测试"""
    print("\n" + "="*80)
    print("PCB Pre-Audit APIs Testing")
    print("="*80)
    
    # 先登录获取token
    if not get_token():
        print("\nFailed to get token. Exiting...")
        return
    
    results = []
    
    # 1. 测试筹划与组织API
    results.append(test_api("GET", f"/pcb/enterprise/{ENTERPRISE_ID}/leadership-team", 
                           desc="1. 获取领导小组"))
    results.append(test_api("GET", f"/pcb/enterprise/{ENTERPRISE_ID}/work-team", 
                           desc="2. 获取工作小组"))
    results.append(test_api("GET", f"/pcb/enterprise/{ENTERPRISE_ID}/work-plans", 
                           desc="3. 获取工作计划"))
    results.append(test_api("GET", f"/pcb/enterprise/{ENTERPRISE_ID}/training-records", 
                           desc="4. 获取培训记录"))
    
    # 2. 测试生产情况API
    results.append(test_api("GET", f"/pcb/enterprise/{ENTERPRISE_ID}/production-data", 
                           desc="5. 获取生产情况数据"))
    
    # 3. 测试资源能源消耗API
    results.append(test_api("GET", f"/resource-consumption/enterprise/{ENTERPRISE_ID}/all-data", 
                           desc="6. 获取资源能源消耗数据"))
    results.append(test_api("GET", f"/resource-consumption/enterprise/{ENTERPRISE_ID}/water-records", 
                           desc="7. 获取用水记录"))
    results.append(test_api("GET", f"/resource-consumption/enterprise/{ENTERPRISE_ID}/electricity-records", 
                           desc="8. 获取用电记录"))
    results.append(test_api("GET", f"/resource-consumption/enterprise/{ENTERPRISE_ID}/gas-records", 
                           desc="9. 获取天然气记录"))
    
    # 4. 测试工艺装备API
    results.append(test_api("GET", f"/process-equipment/enterprise/{ENTERPRISE_ID}/all-data", 
                           desc="10. 获取工艺装备数据"))
    
    # 5. 测试污染防治API
    results.append(test_api("GET", f"/pollution-control/enterprise/{ENTERPRISE_ID}/all-data", 
                           desc="11. 获取污染防治数据"))
    
    # 6. 测试固体废物API
    results.append(test_api("GET", f"/solid-waste/enterprise/{ENTERPRISE_ID}/all-data", 
                           desc="12. 获取固体废物数据"))
    
    # 7. 测试自行监测API
    results.append(test_api("GET", f"/self-monitoring/enterprise/{ENTERPRISE_ID}/all-data", 
                           desc="13. 获取自行监测数据"))
    
    # 8. 测试原辅材料API
    results.append(test_api("GET", f"/pcb/enterprise/{ENTERPRISE_ID}/raw-materials", 
                           desc="14. 获取原辅材料使用情况"))
    
    # 统计结果
    print("\n" + "="*80)
    print("Test Summary")
    print("="*80)
    total = len(results)
    passed = sum(results)
    failed = total - passed
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Success Rate: {passed/total*100:.1f}%")
    print("="*80)


if __name__ == "__main__":
    main()

