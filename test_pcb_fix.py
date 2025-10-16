#!/usr/bin/env python3
"""
测试PCB企业列表API修复
"""
import requests
import json

def test_pcb_enterprise_api():
    """测试PCB企业列表API"""
    print("=" * 60)
    print("测试PCB企业列表API修复")
    print("=" * 60)
    
    try:
        # 1. 登录获取token
        print("\n1. 登录获取token...")
        login_data = {
            'username': 'admin',
            'password': '123456'
        }
        login_response = requests.post('http://localhost:9999/api/v1/base/access_token', 
                                     json=login_data, timeout=10)
        print(f"登录状态: {login_response.status_code}")
        
        if login_response.status_code != 200:
            print(f"登录失败: {login_response.text}")
            return
        
        token_data = login_response.json()
        token = token_data.get('data', {}).get('access_token')
        print(f"Token获取成功: {token[:20]}...")
        
        headers = {'token': token}
        
        # 2. 测试PCB企业列表API
        print("\n2. 测试PCB企业列表API...")
        response = requests.get('http://localhost:9999/api/v1/pcb/enterprise?page=1&page_size=10', 
                              headers=headers, timeout=10)
        print(f"企业列表API状态: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API调用成功！")
            print(f"返回数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ API调用失败: {response.text}")
        
        print("\n" + "=" * 60)
        print("测试完成！")
        print("=" * 60)
                
    except Exception as e:
        print(f"测试过程中出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_pcb_enterprise_api()
