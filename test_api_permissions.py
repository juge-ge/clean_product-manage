import asyncio
from app.models.admin import Api, Role
from tortoise import Tortoise

async def test_api_permissions():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    
    # 检查PCB筹划与组织相关的API
    pcb_apis = await Api.filter(path__contains='pcb/enterprise').all()
    print('PCB筹划与组织相关API:')
    for api in pcb_apis:
        print(f'  {api.method} {api.path}')
    
    # 检查管理员角色的API权限
    admin_role = await Role.filter(name='管理员').first()
    if admin_role:
        admin_apis = await admin_role.apis.all()
        pcb_admin_apis = [api for api in admin_apis if 'pcb/enterprise' in api.path]
        print(f'\n管理员角色的PCB API权限数量: {len(pcb_admin_apis)}')
        for api in pcb_admin_apis:
            print(f'  {api.method} {api.path}')
    else:
        print('未找到管理员角色')
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(test_api_permissions())
