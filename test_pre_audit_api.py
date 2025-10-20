import requests
import json

# 测试预审核API接口
base_url = 'http://localhost:8000/api/v1/pcb'

# 测试获取预审核数据
try:
    response = requests.get(f'{base_url}/enterprise/11/pre-audit')
    print('=== 获取预审核数据 ===')
    print(f'状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'响应: {json.dumps(data, ensure_ascii=False, indent=2)}')
    else:
        print(f'错误: {response.text}')
except Exception as e:
    print(f'请求失败: {e}')

# 测试保存预审核数据
try:
    test_data = {
        "production_info": {
            "capacity": 120.0,
            "output": {
                "2022": {"rigidSingle": 15.2, "rigidDouble": 45.8},
                "2023": {"rigidSingle": 18.5, "rigidDouble": 52.6},
                "2024": {"rigidSingle": 22.3, "rigidDouble": 58.9}
            }
        },
        "raw_materials": [
            {
                "year": 2023,
                "name": "覆铜板",
                "unit": "kg",
                "process": "开料",
                "amount": 1420000,
                "state": "固体",
                "voc": 0
            }
        ]
    }
    
    response = requests.post(
        f'{base_url}/enterprise/11/pre-audit',
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    print('\n=== 保存预审核数据 ===')
    print(f'状态码: {response.status_code}')
    if response.status_code == 200:
        data = response.json()
        print(f'响应: {json.dumps(data, ensure_ascii=False, indent=2)}')
    else:
        print(f'错误: {response.text}')
except Exception as e:
    print(f'请求失败: {e}')
