#!/usr/bin/env python3
"""
检查原始的指标方案关联关系
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def check_original_relations():
    """检查原始的指标方案关联关系"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取所有关联关系
        all_relations = await PCBIndicatorSchemeRelation.all()
        print(f"总关联关系数量: {len(all_relations)}")
        
        # 按创建时间排序，查看最早的关系
        relations_by_time = await PCBIndicatorSchemeRelation.all().order_by("created_at")
        
        print("\n最早的10个关联关系:")
        for i, relation in enumerate(relations_by_time[:10]):
            scheme = await PCBScheme.get_or_none(id=relation.scheme_id)
            indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
            if scheme and indicator:
                print(f"  {i+1}. 方案{scheme.scheme_id}({scheme.name}) -> 指标{indicator.indicator_id}({indicator.name})")
                print(f"     创建时间: {relation.created_at}")
                print(f"     关联度: {relation.relevance_score}")
                print(f"     优先级: {relation.priority}")
                print(f"     推荐理由: {relation.recommendation_reason}")
        
        # 检查是否有我添加的数据（通过推荐理由判断）
        my_added_relations = await PCBIndicatorSchemeRelation.filter(
            recommendation_reason__icontains="针对指标"
        ).all()
        
        print(f"\n我添加的关联关系数量: {len(my_added_relations)}")
        
        if my_added_relations:
            print("我添加的关联关系示例:")
            for relation in my_added_relations[:5]:
                scheme = await PCBScheme.get_or_none(id=relation.scheme_id)
                indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
                if scheme and indicator:
                    print(f"  - 方案{scheme.scheme_id} -> 指标{indicator.indicator_id}: {relation.recommendation_reason}")
        
    except Exception as e:
        print(f"检查失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_original_relations())
