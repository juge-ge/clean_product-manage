"""
PCB API接口测试脚本
用于测试API调用和验证功能
"""
import asyncio
import json

import httpx


# API基础URL
BASE_URL = "http://localhost:8000"
API_PREFIX = "/api/v1"

# 测试用的认证Token（需要先登录获取）
# 如果需要认证，请先运行登录接口获取token
AUTH_TOKEN = None


def get_headers():
    """获取请求头"""
    headers = {"Content-Type": "application/json"}
    if AUTH_TOKEN:
        headers["Authorization"] = f"Bearer {AUTH_TOKEN}"
    return headers


async def test_api_connection():
    """测试API连接"""
    print("=" * 80)
    print("测试API连接")
    print("=" * 80)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{BASE_URL}/docs")
            if response.status_code == 200:
                print("✅ API服务正常运行")
                print(f"   Swagger文档地址: {BASE_URL}/docs")
                print(f"   ReDoc文档地址: {BASE_URL}/redoc")
                return True
            else:
                print("❌ API服务可能未启动")
                return False
        except Exception as e:
            print(f"❌ 无法连接到API服务: {e}")
            print(f"   请确保应用已启动: python run.py")
            return False


async def test_login():
    """测试登录接口"""
    print("\n" + "=" * 80)
    print("测试登录接口")
    print("=" * 80)

    async with httpx.AsyncClient() as client:
        try:
            # 尝试登录（使用默认管理员账号）
            login_data = {
                "username": "admin",
                "password": "admin123"  # 修改为实际的管理员密码
            }
            
            response = await client.post(
                f"{BASE_URL}{API_PREFIX}/base/login",
                json=login_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 登录成功")
                if "data" in data and "token" in data["data"]:
                    global AUTH_TOKEN
                    AUTH_TOKEN = data["data"]["token"]
                    print(f"   Token: {AUTH_TOKEN[:50]}...")
                return True
            else:
                print(f"❌ 登录失败: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 登录请求失败: {e}")
            return False


async def test_get_indicator_list():
    """测试获取指标列表接口"""
    print("\n" + "=" * 80)
    print("【测试1】获取指标列表")
    print("=" * 80)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}{API_PREFIX}/pcb/indicator",
                headers=get_headers()
            )
            
            print(f"请求URL: GET {BASE_URL}{API_PREFIX}/pcb/indicator")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 请求成功")
                if "data" in data:
                    indicators = data["data"]
                    print(f"   指标总数: {len(indicators)}")
                    if indicators:
                        print(f"   前3项指标:")
                        for ind in indicators[:3]:
                            print(f"     - 指标{ind['indicator_id']}: {ind['name']}")
                return True
            else:
                print(f"❌ 请求失败: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return False


async def test_get_indicator_tree():
    """测试获取指标树接口"""
    print("\n" + "=" * 80)
    print("【测试2】获取指标树")
    print("=" * 80)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}{API_PREFIX}/pcb/indicator/tree",
                headers=get_headers()
            )
            
            print(f"请求URL: GET {BASE_URL}{API_PREFIX}/pcb/indicator/tree")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 请求成功")
                if "data" in data:
                    tree = data["data"]
                    print(f"   一级分类数: {len(tree)}")
                    for category in tree:
                        print(f"     - {category['label']}: {len(category['children'])}项指标")
                return True
            else:
                print(f"❌ 请求失败: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return False


async def test_create_enterprise():
    """测试创建企业接口"""
    print("\n" + "=" * 80)
    print("【测试3】创建企业")
    print("=" * 80)

    enterprise_data = {
        "name": "测试PCB企业有限公司",
        "region": "深圳市",
        "district": "宝安区",
        "address": "深圳市宝安区某某工业园",
        "contact_person": "张三",
        "contact_phone": "13800138000",
        "contact_email": "test@example.com",
        "capacity": 120.50
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BASE_URL}{API_PREFIX}/pcb/enterprise",
                json=enterprise_data,
                headers=get_headers()
            )
            
            print(f"请求URL: POST {BASE_URL}{API_PREFIX}/pcb/enterprise")
            print(f"请求数据: {json.dumps(enterprise_data, ensure_ascii=False, indent=2)}")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 企业创建成功")
                if "data" in data:
                    print(f"   企业ID: {data['data']['id']}")
                    print(f"   企业名称: {data['data']['name']}")
                    return data['data']['id']
            else:
                print(f"❌ 创建失败: {response.text}")
                return None
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return None


async def test_get_enterprise_list():
    """测试获取企业列表接口"""
    print("\n" + "=" * 80)
    print("【测试4】获取企业列表")
    print("=" * 80)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}{API_PREFIX}/pcb/enterprise?page=1&page_size=10",
                headers=get_headers()
            )
            
            print(f"请求URL: GET {BASE_URL}{API_PREFIX}/pcb/enterprise")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 请求成功")
                if "data" in data:
                    items = data["data"]["items"]
                    total = data["data"]["total"]
                    print(f"   企业总数: {total}")
                    if items:
                        print(f"   企业列表:")
                        for ent in items:
                            print(f"     - ID: {ent['id']}, 名称: {ent['name']}, "
                                  f"地区: {ent.get('region', '')}")
                return True
            else:
                print(f"❌ 请求失败: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return False


async def test_get_audit_results(enterprise_id: int):
    """测试获取审核结果接口"""
    print("\n" + "=" * 80)
    print(f"【测试5】获取企业 {enterprise_id} 的审核结果")
    print("=" * 80)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}{API_PREFIX}/pcb/enterprise/{enterprise_id}/audit",
                headers=get_headers()
            )
            
            print(f"请求URL: GET {BASE_URL}{API_PREFIX}/pcb/enterprise/{enterprise_id}/audit")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 请求成功")
                if "data" in data:
                    results = data["data"]
                    print(f"   审核结果总数: {len(results)}")
                    print(f"   前3项审核结果:")
                    for result in results[:3]:
                        indicator = result.get("indicator", {})
                        print(f"     - 指标{indicator.get('indicator_id')}: {indicator.get('name')}")
                        print(f"       评级: {result.get('level')}, 得分: {result.get('score')}")
                return True
            else:
                print(f"❌ 请求失败: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return False


async def test_update_audit_result(enterprise_id: int, indicator_id: int):
    """测试更新审核结果接口"""
    print("\n" + "=" * 80)
    print(f"【测试6】更新企业 {enterprise_id} 指标 {indicator_id} 的审核结果")
    print("=" * 80)

    update_data = {
        "current_value": 115.5,
        "level": "II级",
        "score": 80,
        "comment": "测试更新审核结果"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(
                f"{BASE_URL}{API_PREFIX}/pcb/enterprise/{enterprise_id}/audit/indicator/{indicator_id}",
                json=update_data,
                headers=get_headers()
            )
            
            print(f"请求URL: PUT {BASE_URL}{API_PREFIX}/pcb/enterprise/{enterprise_id}/audit/indicator/{indicator_id}")
            print(f"请求数据: {json.dumps(update_data, ensure_ascii=False, indent=2)}")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 更新成功")
                if "data" in data:
                    print(f"   评级: {data['data']['level']}")
                    print(f"   得分: {data['data']['score']}")
                return True
            else:
                print(f"❌ 更新失败: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return False


async def test_get_audit_summary(enterprise_id: int):
    """测试获取审核汇总接口"""
    print("\n" + "=" * 80)
    print(f"【测试7】获取企业 {enterprise_id} 的审核汇总")
    print("=" * 80)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}{API_PREFIX}/pcb/enterprise/{enterprise_id}/audit/summary",
                headers=get_headers()
            )
            
            print(f"请求URL: GET {BASE_URL}{API_PREFIX}/pcb/enterprise/{enterprise_id}/audit/summary")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 请求成功")
                if "data" in data:
                    summary = data["data"]
                    print(f"   总分: {summary.get('total_score')}")
                    print(f"   综合等级: {summary.get('overall_level')}")
                    print(f"   待改进项数: {summary.get('improvement_items')}")
                    print(f"   限定性指标数: {summary.get('limiting_indicators')}")
                return True
            else:
                print(f"❌ 请求失败: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return False


async def test_get_scheme_list():
    """测试获取方案列表接口"""
    print("\n" + "=" * 80)
    print("【测试8】获取方案列表")
    print("=" * 80)

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{BASE_URL}{API_PREFIX}/pcb/scheme?page=1&page_size=10",
                headers=get_headers()
            )
            
            print(f"请求URL: GET {BASE_URL}{API_PREFIX}/pcb/scheme")
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ 请求成功")
                if "data" in data:
                    items = data["data"]["items"]
                    total = data["data"]["total"]
                    print(f"   方案总数: {total}")
                    if items:
                        print(f"   方案列表:")
                        for scheme in items:
                            print(f"     - 方案{scheme['scheme_id']}: {scheme['name']}")
                return True
            else:
                print(f"❌ 请求失败: {response.text}")
                return False
        except Exception as e:
            print(f"❌ 请求异常: {e}")
            return False


async def run_all_tests():
    """运行所有测试"""
    print("\n")
    print("*" * 80)
    print("*" + " " * 78 + "*")
    print("*" + " " * 20 + "PCB API 接口测试套件" + " " * 28 + "*")
    print("*" + " " * 78 + "*")
    print("*" * 80)

    # 测试API连接
    if not await test_api_connection():
        print("\n❌ API服务未运行，请先启动应用: python run.py")
        return

    # 可选：测试登录（如果需要认证）
    # await test_login()

    # 运行各项测试
    await test_get_indicator_list()
    await test_get_indicator_tree()
    
    enterprise_id = await test_create_enterprise()
    
    await test_get_enterprise_list()
    
    if enterprise_id:
        await test_get_audit_results(enterprise_id)
        await test_update_audit_result(enterprise_id, 7)  # 更新指标7
        await test_get_audit_summary(enterprise_id)
    
    await test_get_scheme_list()

    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)
    print("\n提示:")
    print("  - 所有API接口文档: http://localhost:8000/docs")
    print("  - 可以在Swagger UI中直接测试接口")
    print("  - 使用 check_pcb_database.py 脚本查看数据库内容")


if __name__ == "__main__":
    asyncio.run(run_all_tests())



