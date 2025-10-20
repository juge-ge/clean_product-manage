#!/usr/bin/env python3
"""
检查原始数据，找出不是我添加的关联关系
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def check_original_data():
    """检查原始数据"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取不是我添加的关联关系（推荐理由不包含"针对指标"）
        original_relations = await PCBIndicatorSchemeRelation.filter(
            recommendation_reason__isnull=True
        ).all()
        
        print(f"原始关联关系数量: {len(original_relations)}")
        
        if original_relations:
            print("\n原始关联关系示例:")
            for i, relation in enumerate(original_relations[:10]):
                scheme = await PCBScheme.get_or_none(id=relation.scheme_id)
                indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
                if scheme and indicator:
                    print(f"  {i+1}. 方案{scheme.scheme_id}({scheme.name}) -> 指标{indicator.indicator_id}({indicator.name})")
                    print(f"     关联度: {relation.relevance_score}")
                    print(f"     优先级: {relation.priority}")
                    print(f"     推荐理由: {relation.recommendation_reason}")
        
        # 检查所有关联关系的推荐理由分布
        print("\n推荐理由分布:")
        relations_with_reason = await PCBIndicatorSchemeRelation.filter(
            recommendation_reason__isnull=False
        ).all()
        
        reason_counts = {}
        for relation in relations_with_reason:
            reason = relation.recommendation_reason or "无"
            reason_counts[reason] = reason_counts.get(reason, 0) + 1
        
        for reason, count in reason_counts.items():
            print(f"  '{reason}': {count}个")
        
    except Exception as e:
        print(f"检查失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_original_data())
