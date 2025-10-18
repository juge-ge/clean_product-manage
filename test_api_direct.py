import requests
import json

# 测试API是否可以直接访问
def test_api():
    base_url = "http://localhost:9999"
    
    # 先尝试登录获取token
    login_data = {
        "username": "admin",
        "password": "123456"
    }
    
    try:
        # 登录
        login_response = requests.post(f"{base_url}/api/v1/base/access_token", json=login_data)
        print(f"登录响应状态: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            token = token_data.get('data', {}).get('access_token')
            print(f"获取到token: {token[:20]}..." if token else "未获取到token")
            
            if token:
                # 测试PCB筹划与组织API
                headers = {
                    "token": token,
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                
                # 测试领导小组API
                leadership_response = requests.get(
                    f"{base_url}/api/v1/pcb/enterprise/7/leadership-team",
                    headers=headers
                )
                print(f"领导小组API响应状态: {leadership_response.status_code}")
                print(f"领导小组API响应内容: {leadership_response.text[:200]}...")
                
                # 测试工作小组API
                work_team_response = requests.get(
                    f"{base_url}/api/v1/pcb/enterprise/7/work-team",
                    headers=headers
                )
                print(f"工作小组API响应状态: {work_team_response.status_code}")
                print(f"工作小组API响应内容: {work_team_response.text[:200]}...")
                
        else:
            print(f"登录失败: {login_response.text}")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    test_api()