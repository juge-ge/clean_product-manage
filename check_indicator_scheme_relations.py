import asyncio
from tortoise import Tortoise
from app.models.pcb import PCBIndicator, PCBScheme, PCBIndicatorSchemeRelation

async def check_indicator_scheme_relations():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    
    print('=== 检查指标数据 ===')
    indicators = await PCBIndicator.all()
    print(f'指标总数: {len(indicators)}')
    
    print('\n=== 检查方案数据 ===')
    schemes = await PCBScheme.all()
    print(f'方案总数: {len(schemes)}')
    
    print('\n=== 检查指标方案关联数据 ===')
    relations = await PCBIndicatorSchemeRelation.all()
    print(f'关联关系总数: {len(relations)}')
    
    if relations:
        print('\n前10个关联关系:')
        for i, relation in enumerate(relations[:10]):
            indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
            scheme = await PCBScheme.get_or_none(id=relation.scheme_id)
            print(f'{i+1}. 指标{relation.indicator_id}({indicator.name if indicator else "未知"}) -> 方案{relation.scheme_id}({scheme.name if scheme else "未知"})')
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(check_indicator_scheme_relations())
