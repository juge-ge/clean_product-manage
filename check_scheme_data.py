import asyncio
from tortoise import Tortoise
from app.models.pcb import PCBScheme

async def check_scheme_data():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    
    print('=== 检查方案数据 ===')
    schemes = await PCBScheme.all()
    print(f'方案总数: {len(schemes)}')
    
    print('\n前10个方案:')
    for i, scheme in enumerate(schemes[:10]):
        print(f'{i+1}. ID:{scheme.id}, 方案编号:{scheme.scheme_id}, 名称:{scheme.name}, 类型:{scheme.scheme_type}')
    
    print('\n检查方案编号1-10:')
    for scheme_id in range(1, 11):
        scheme = await PCBScheme.filter(scheme_id=scheme_id).first()
        if scheme:
            print(f'方案编号{scheme_id}: {scheme.name}')
        else:
            print(f'方案编号{scheme_id}: 不存在')
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(check_scheme_data())
