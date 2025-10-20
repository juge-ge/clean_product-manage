#!/usr/bin/env python3
"""
测试API（不使用权限检查）
"""

import requests
import json

def test_api_no_permission():
    """测试API（不使用权限检查）"""
    BASE_URL = "http://localhost:9999/api/v1"
    
    # 测试一个已知工作的API（不使用权限）
    print("测试已知工作的API（不使用权限）:")
    try:
        response = requests.get(f"{BASE_URL}/base/userinfo")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("基础API工作正常")
        else:
            print(f"基础API失败: {response.text}")
    except Exception as e:
        print(f"基础API异常: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # 测试原辅材料API（不使用权限）
    print("测试原辅材料API（不使用权限）:")
    try:
        response = requests.get(f"{BASE_URL}/raw-material/materials")
        print(f"状态码: {response.status_code}")
        if response.status_code == 200:
            print("原辅材料API工作正常")
        else:
            print(f"原辅材料API失败: {response.text}")
    except Exception as e:
        print(f"原辅材料API异常: {e}")

if __name__ == "__main__":
    test_api_no_permission()
