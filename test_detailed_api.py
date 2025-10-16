#!/usr/bin/env python3
"""
详细API测试
"""
import requests
import json
import traceback

def test_detailed_api():
    base_url = "http://localhost:9999/api/v1/pcb"
    enterprise_id = 1
    
    print("测试获取领导小组...")
    try:
        response = requests.get(f"{base_url}/enterprise/{enterprise_id}/leadership-team")
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"错误信息: {response.text}")
            try:
                error_data = response.json()
                print(f"错误JSON: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
            except:
                pass
        else:
            data = response.json()
            print(f"成功获取数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"请求失败: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_detailed_api()
