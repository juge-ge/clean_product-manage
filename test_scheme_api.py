#!/usr/bin/env python3
"""
测试方案API是否正确返回关联指标数据
"""

import requests
import json

BASE_URL = "http://localhost:9999/api/v1"
headers = {"token": "dev"}

def test_scheme_api():
    """测试方案API"""
    try:
        # 测试方案列表API
        response = requests.get(f"{BASE_URL}/pcb/scheme", headers=headers, params={"page": 1, "page_size": 5})
        
        if response.status_code == 200:
            data = response.json()
            print("方案API测试成功!")
            print(f"返回数据格式: {list(data.keys())}")
            
            if data.get('data') and data['data'].get('items'):
                schemes = data['data']['items']
                print(f"获取到 {len(schemes)} 个方案")
                
                # 检查前3个方案的关联指标
                for i, scheme in enumerate(schemes[:3]):
                    print(f"\n方案 {i+1}: {scheme.get('name', 'N/A')}")
                    print(f"  方案ID: {scheme.get('scheme_id', 'N/A')}")
                    
                    related_indicators = scheme.get('related_indicators', [])
                    print(f"  关联指标数量: {len(related_indicators)}")
                    
                    if related_indicators:
                        print("  关联指标:")
                        for indicator in related_indicators[:3]:  # 只显示前3个
                            print(f"    - 指标{indicator.get('id', 'N/A')}: {indicator.get('name', 'N/A')}")
                    else:
                        print("  无关联指标")
            else:
                print("没有获取到方案数据")
        else:
            print(f"API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_scheme_api()
