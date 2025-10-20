#!/usr/bin/env python3
"""
调试API返回的关联关系
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def debug_api_relations():
    """调试API返回的关联关系"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取前5个方案
        schemes = await PCBScheme.all().order_by("scheme_id").limit(5)
        
        print("前5个方案的关联指标详情:")
        for scheme in schemes:
            print(f"\n方案{scheme.scheme_id}: {scheme.name}")
            
            # 获取该方案的所有关联关系
            relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).all()
            print(f"  关联关系数量: {len(relations)}")
            
            if relations:
                print("  关联的指标:")
                for relation in relations:
                    indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
                    if indicator:
                        print(f"    - 指标ID: {relation.indicator_id} ({indicator.indicator_id}) - {indicator.name}")
                        print(f"      关联度: {relation.relevance_score}, 优先级: {relation.priority}")
                        print(f"      推荐理由: {relation.recommendation_reason}")
            else:
                print("  无关联指标")
        
        # 测试API逻辑
        print("\n\n测试API逻辑:")
        for scheme in schemes[:2]:  # 只测试前2个方案
            print(f"\n方案{scheme.scheme_id}: {scheme.name}")
            
            # 模拟API中的逻辑
            relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).all()
            related_indicators = []
            
            for relation in relations:
                indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
                if indicator:
                    related_indicators.append({
                        "id": indicator.id,
                        "name": indicator.name,
                        "relevance_score": relation.relevance_score,
                        "priority": relation.priority,
                        "recommendation_reason": relation.recommendation_reason
                    })
            
            print(f"  API应返回的关联指标: {len(related_indicators)}个")
            for indicator in related_indicators:
                print(f"    - {indicator['name']} (关联度: {indicator['relevance_score']})")
        
    except Exception as e:
        print(f"调试失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(debug_api_relations())
