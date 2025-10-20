#!/usr/bin/env python3
"""
测试简单API
"""

import requests
import json

def test_simple_api():
    """测试简单API"""
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

if __name__ == "__main__":
    test_simple_api()