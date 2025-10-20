#!/usr/bin/env python3
"""
测试PCB审核和方案选择API端点
"""

import requests
import json
import time

BASE_URL = "http://localhost:9999/api/v1"

def test_api_endpoint(method, endpoint, data=None, params=None):
    """测试API端点"""
    url = f"{BASE_URL}{endpoint}"
    
    # 添加开发token
    headers = {"token": "dev"}
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers, timeout=10)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        else:
            print(f"不支持的HTTP方法: {method}")
            return None
            
        print(f"{method} {endpoint} -> {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if isinstance(result, list):
                    print(f"  返回 {len(result)} 条记录")
                elif isinstance(result, dict):
                    if 'total' in result:
                        print(f"  总数: {result['total']}")
                    else:
                        print(f"  返回数据: {list(result.keys())}")
                return result
            except:
                print(f"  响应内容: {response.text[:200]}")
        else:
            print(f"  错误: {response.text[:200]}")
            
    except requests.exceptions.RequestException as e:
        print(f"  请求失败: {e}")
    
    return None

def main():
    """主测试函数"""
    print("开始测试PCB审核和方案选择API端点...")
    
    # 等待服务启动
    print("等待服务启动...")
    time.sleep(3)
    
    # 测试基本端点
    print("\n=== 测试基本端点 ===")
    test_api_endpoint("GET", "/pcb/enterprise")
    test_api_endpoint("GET", "/pcb/indicator")
    test_api_endpoint("GET", "/pcb/scheme")
    
    # 测试指标方案关联
    print("\n=== 测试指标方案关联 ===")
    test_api_endpoint("GET", "/pcb/indicator-scheme-relation")
    
    # 测试审核结果
    print("\n=== 测试审核结果 ===")
    test_api_endpoint("GET", "/pcb/audit-result")
    
    # 测试企业审核结果
    print("\n=== 测试企业审核结果 ===")
    enterprises = test_api_endpoint("GET", "/pcb/enterprise")
    if enterprises and enterprises.get('data') and enterprises['data'].get('items') and len(enterprises['data']['items']) > 0:
        enterprise_id = enterprises['data']['items'][0]['id']
        test_api_endpoint("GET", f"/pcb/enterprise/{enterprise_id}/audit-result")
        
        # 测试指标推荐方案
        indicators = test_api_endpoint("GET", "/pcb/indicator")
        if indicators and indicators.get('data') and len(indicators['data']) > 0:
            indicator_id = indicators['data'][0]['id']
            test_api_endpoint("GET", f"/pcb/enterprise/{enterprise_id}/indicator/{indicator_id}/scheme")
    
    print("\nAPI测试完成!")

if __name__ == "__main__":
    main()
