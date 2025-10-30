#!/usr/bin/env python3
"""
检查用户权限和API访问问题
"""
import asyncio
from app.settings import settings
from tortoise import Tortoise
from app.models.admin import User, Role, Api
from app.controllers.pcb import pcb_enterprise_controller

async def check_user_permissions():
    """检查用户权限配置"""
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    print("=" * 80)
    print("检查用户权限配置")
    print("=" * 80)
    
    # 1. 检查用户
    users = await User.all()
    print(f"\n用户总数: {len(users)}")
    
    for user in users:
        print(f"\n用户: {user.username} (ID: {user.id})")
        print(f"  是否超级用户: {user.is_superuser}")
        
        # 检查角色
        roles = await user.roles
        print(f"  角色数量: {len(roles)}")
        
        for role in roles:
            print(f"    角色: {role.name}")
            apis = await role.apis
            print(f"    API权限数量: {len(apis)}")
            
            # 检查PCB相关API权限
            pcb_apis = [api for api in apis if 'pcb' in api.path.lower()]
            if pcb_apis:
                print(f"    PCB相关API权限:")
                for api in pcb_apis:
                    print(f"      {api.method} {api.path}")
            else:
                print(f"    无PCB相关API权限")
    
    # 2. 检查API配置
    print(f"\n" + "=" * 50)
    print("检查API配置")
    print("=" * 50)
    
    all_apis = await Api.all()
    pcb_apis = [api for api in all_apis if 'pcb' in api.path.lower()]
    
    print(f"总API数量: {len(all_apis)}")
    print(f"PCB相关API数量: {len(pcb_apis)}")
    
    if pcb_apis:
        print("\nPCB相关API列表:")
        for api in pcb_apis[:10]:  # 只显示前10个
            print(f"  {api.method} {api.path}")
        if len(pcb_apis) > 10:
            print(f"  ... 还有 {len(pcb_apis) - 10} 个API")
    
    # 3. 测试企业列表API
    print(f"\n" + "=" * 50)
    print("测试企业列表API")
    print("=" * 50)
    
    try:
        enterprises, total = await pcb_enterprise_controller.get_list(page=1, page_size=10)
        print(f"企业列表API调用成功")
        print(f"  企业数量: {len(enterprises)}")
        print(f"  总数: {total}")
        
        if enterprises:
            print(f"  第一个企业: {enterprises[0].name}")
    except Exception as e:
        print(f"企业列表API调用失败: {e}")
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(check_user_permissions())
