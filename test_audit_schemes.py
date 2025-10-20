#!/usr/bin/env python3
"""
测试审核模块的推荐方案功能
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def test_audit_schemes():
    """测试审核模块的推荐方案功能"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取前5个指标
        indicators = await PCBIndicator.all().order_by("indicator_id").limit(5)
        
        print("前5个指标的推荐方案:")
        for indicator in indicators:
            print(f"\n指标{indicator.indicator_id}: {indicator.name}")
            
            # 获取该指标的推荐方案
            relations = await PCBIndicatorSchemeRelation.filter(
                indicator_id=indicator.id
            ).order_by("-relevance_score", "priority").limit(5)
            
            if relations:
                print(f"  推荐方案数量: {len(relations)}")
                for i, relation in enumerate(relations):
                    scheme = await PCBScheme.get_or_none(id=relation.scheme_id)
                    if scheme:
                        print(f"    {i+1}. 方案{scheme.scheme_id}: {scheme.name}")
                        print(f"       关联度: {relation.relevance_score}, 优先级: {relation.priority}")
                        print(f"       推荐理由: {relation.recommendation_reason}")
            else:
                print("  无推荐方案")
        
        # 测试方案库显示
        print("\n\n方案库显示测试:")
        schemes = await PCBScheme.all().order_by("scheme_id").limit(5)
        
        for scheme in schemes:
            print(f"\n方案{scheme.scheme_id}: {scheme.name}")
            
            # 获取该方案的关联指标
            relations = await PCBIndicatorSchemeRelation.filter(
                scheme_id=scheme.id
            ).order_by("priority")
            
            if relations:
                indicator_numbers = []
                indicator_names = []
                for relation in relations:
                    indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
                    if indicator:
                        indicator_numbers.append(str(indicator.indicator_id))
                        indicator_names.append(indicator.name)
                
                print(f"  主要应对指标编号: {', '.join(indicator_numbers)}")
                print(f"  主要对应指标名称: {', '.join(indicator_names)}")
            else:
                print("  主要应对指标编号: 暂无")
                print("  主要对应指标名称: 暂无")
        
    except Exception as e:
        print(f"测试失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(test_audit_schemes())
