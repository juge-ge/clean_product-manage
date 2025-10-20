#!/usr/bin/env python3
"""
测试方案API的完整响应
"""

import requests
import json

BASE_URL = "http://localhost:9999/api/v1"
headers = {"token": "dev"}

def test_scheme_response():
    """测试方案API响应"""
    try:
        response = requests.get(f"{BASE_URL}/pcb/scheme", headers=headers, params={"page": 1, "page_size": 2})
        
        if response.status_code == 200:
            data = response.json()
            print("API响应成功!")
            print(f"响应结构: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            # 检查第一个方案的详细数据
            if data.get('data') and data['data'].get('items') and len(data['data']['items']) > 0:
                first_scheme = data['data']['items'][0]
                print(f"\n第一个方案的详细数据:")
                print(f"方案名称: {first_scheme.get('name')}")
                print(f"方案ID: {first_scheme.get('scheme_id')}")
                print(f"关联指标: {first_scheme.get('related_indicators', [])}")
                
                if first_scheme.get('related_indicators'):
                    print("关联指标详情:")
                    for indicator in first_scheme['related_indicators']:
                        print(f"  - 指标{indicator.get('id')}: {indicator.get('name')}")
        else:
            print(f"API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_scheme_response()
