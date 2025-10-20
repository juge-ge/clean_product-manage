"""
测试资源能源消耗API接口
"""
import asyncio
import requests
import json
from datetime import datetime


# API基础URL
BASE_URL = "http://localhost:8000/api/v1"


def test_api_connection():
    """测试API连接"""
    try:
        response = requests.get(f"{BASE_URL}/base/health", timeout=5)
        if response.status_code == 200:
            print("API服务器连接正常")
            return True
        else:
            print(f"API服务器响应异常: {response.status_code}")
            return False
    except Exception as e:
        print(f"API服务器连接失败: {str(e)}")
        return False


def test_resource_consumption_apis():
    """测试资源能源消耗相关API"""
    enterprise_id = 1  # 测试企业ID
    
    print(f"\n开始测试企业ID {enterprise_id} 的资源能源消耗API...")
    
    # 测试获取所有数据
    print("\n1. 测试获取所有资源能源消耗数据...")
    try:
        response = requests.get(f"{BASE_URL}/resource-consumption/enterprise/{enterprise_id}/all-data")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   获取成功，数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   获取失败: {response.text}")
    except Exception as e:
        print(f"   请求异常: {str(e)}")
    
    # 测试保存数据
    print("\n2. 测试保存资源能源消耗数据...")
    test_data = {
        "water": {
            "categories": [
                {
                    "name": "测试用水分类",
                    "default_unit": "m³"
                }
            ],
            "records": [
                {
                    "category_id": 1,
                    "year": 2023,
                    "water_type": "生产用水",
                    "unit": "m³",
                    "amount": 1000.50,
                    "source": "市政管网",
                    "remark": "测试用水记录"
                }
            ]
        },
        "electricity": {
            "region_records": [
                {
                    "dimension": "region",
                    "electricity_type": "生产车间_1",
                    "unit": "kWh",
                    "amount_2022": 50000,
                    "amount_2023": 55000,
                    "amount_2024": 60000,
                    "region": "生产车间A",
                    "remark": "测试用电记录"
                }
            ],
            "trend_records": []
        },
        "gas": {
            "records": [
                {
                    "project": "锅炉天然气",
                    "unit": "m³",
                    "amount_2022": 1000,
                    "amount_2023": 1200,
                    "amount_2024": 1100,
                    "gas_type": "天然气",
                    "source": "市政燃气",
                    "remark": "测试天然气记录"
                }
            ]
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/resource-consumption/enterprise/{enterprise_id}/all-data",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   保存成功，响应: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   保存失败: {response.text}")
    except Exception as e:
        print(f"   请求异常: {str(e)}")
    
    # 测试获取用水分类
    print("\n3. 测试获取用水分类...")
    try:
        response = requests.get(f"{BASE_URL}/resource-consumption/enterprise/{enterprise_id}/water-categories")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   获取成功，分类数量: {len(data.get('data', []))}")
        else:
            print(f"   获取失败: {response.text}")
    except Exception as e:
        print(f"   请求异常: {str(e)}")
    
    # 测试获取用电记录
    print("\n4. 测试获取用电记录...")
    try:
        response = requests.get(f"{BASE_URL}/resource-consumption/enterprise/{enterprise_id}/electricity-records")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 获取成功，记录数量: {len(data.get('data', []))}")
        else:
            print(f"   ❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求异常: {str(e)}")
    
    # 测试获取天然气记录
    print("\n5. 测试获取天然气记录...")
    try:
        response = requests.get(f"{BASE_URL}/resource-consumption/enterprise/{enterprise_id}/gas-records")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 获取成功，记录数量: {len(data.get('data', []))}")
        else:
            print(f"   ❌ 获取失败: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求异常: {str(e)}")
    
    # 测试计算汇总数据
    print("\n6. 测试计算汇总数据...")
    try:
        response = requests.post(f"{BASE_URL}/resource-consumption/enterprise/{enterprise_id}/summary/calculate?year=2023")
        print(f"   状态码: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ 计算成功，汇总数据: {json.dumps(data, indent=2, ensure_ascii=False)}")
        else:
            print(f"   ❌ 计算失败: {response.text}")
    except Exception as e:
        print(f"   ❌ 请求异常: {str(e)}")


def main():
    """主函数"""
    print("开始测试资源能源消耗API接口...")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试API连接
    if not test_api_connection():
        print("API服务器连接失败，请确保服务器正在运行")
        return
    
    # 测试资源能源消耗API
    test_resource_consumption_apis()
    
    print("\n资源能源消耗API测试完成!")


if __name__ == "__main__":
    main()
