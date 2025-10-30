#!/usr/bin/env python3
"""
直接测试API调用
"""
import asyncio
import httpx
from app.settings import settings
from tortoise import Tortoise
from app.models.admin import User
from app.utils.jwt_utils import create_access_token
from datetime import datetime, timedelta, timezone

async def test_api_direct():
    """直接测试API调用"""
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    print("=" * 80)
    print("直接测试API调用")
    print("=" * 80)
    
    # 1. 获取用户并生成token
    user = await User.filter().first()
    if not user:
        print("没有找到用户")
        await Tortoise.close_connections()
        return
    
    print(f"用户: {user.username} (ID: {user.id})")
    print(f"是否超级用户: {user.is_superuser}")
    
    # 生成token
    access_token_expires = timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + access_token_expires
    
    token = create_access_token(
        data={
            "user_id": user.id,
            "username": user.username,
            "is_superuser": user.is_superuser,
            "exp": expire,
        }
    )
    
    print(f"生成的token: {token[:50]}...")
    
    # 2. 测试API调用
    base_url = "http://localhost:8000"
    headers = {
        "token": token,
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient() as client:
        # 测试用户信息API
        print(f"\n测试用户信息API...")
        try:
            response = await client.get(f"{base_url}/api/v1/base/userinfo", headers=headers)
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"响应: {data}")
            else:
                print(f"错误: {response.text}")
        except Exception as e:
            print(f"请求失败: {e}")
        
        # 测试企业列表API
        print(f"\n测试企业列表API...")
        try:
            response = await client.get(f"{base_url}/api/v1/pcb/enterprise?page=1&page_size=10", headers=headers)
            print(f"状态码: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"响应: {data}")
            else:
                print(f"错误: {response.text}")
        except Exception as e:
            print(f"请求失败: {e}")
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(test_api_direct())