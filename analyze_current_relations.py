#!/usr/bin/env python3
"""
分析当前的关联关系，理解数据结构
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def analyze_current_relations():
    """分析当前的关联关系"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取所有关联关系
        all_relations = await PCBIndicatorSchemeRelation.all()
        print(f"总关联关系数量: {len(all_relations)}")
        
        # 分析关联关系的分布
        print("\n分析关联关系分布:")
        
        # 统计每个指标对应的方案数量
        indicator_to_schemes = {}
        for relation in all_relations:
            indicator_id = relation.indicator_id
            if indicator_id not in indicator_to_schemes:
                indicator_to_schemes[indicator_id] = []
            indicator_to_schemes[indicator_id].append(relation.scheme_id)
        
        print(f"有对应方案的指标数量: {len(indicator_to_schemes)}")
        
        # 统计每个方案对应的指标数量
        scheme_to_indicators = {}
        for relation in all_relations:
            scheme_id = relation.scheme_id
            if scheme_id not in scheme_to_indicators:
                scheme_to_indicators[scheme_id] = []
            scheme_to_indicators[scheme_id].append(relation.indicator_id)
        
        print(f"有对应指标的方案数量: {len(scheme_to_indicators)}")
        
        # 显示前10个指标的对应方案
        print("\n前10个指标对应的方案:")
        for i, (indicator_id, scheme_ids) in enumerate(list(indicator_to_schemes.items())[:10]):
            indicator = await PCBIndicator.get_or_none(id=indicator_id)
            if indicator:
                print(f"  指标{indicator.indicator_id}({indicator.name}): {len(scheme_ids)}个方案")
                # 显示前3个方案
                for scheme_id in scheme_ids[:3]:
                    scheme = await PCBScheme.get_or_none(id=scheme_id)
                    if scheme:
                        print(f"    - 方案{scheme.scheme_id}: {scheme.name}")
        
        # 显示前10个方案的对应指标
        print("\n前10个方案对应的指标:")
        for i, (scheme_id, indicator_ids) in enumerate(list(scheme_to_indicators.items())[:10]):
            scheme = await PCBScheme.get_or_none(id=scheme_id)
            if scheme:
                print(f"  方案{scheme.scheme_id}({scheme.name}): {len(indicator_ids)}个指标")
                # 显示前3个指标
                for indicator_id in indicator_ids[:3]:
                    indicator = await PCBIndicator.get_or_none(id=indicator_id)
                    if indicator:
                        print(f"    - 指标{indicator.indicator_id}: {indicator.name}")
        
        # 统计没有对应指标的方案
        all_schemes = await PCBScheme.all()
        schemes_without_indicators = []
        for scheme in all_schemes:
            if scheme.id not in scheme_to_indicators:
                schemes_without_indicators.append(scheme)
        
        print(f"\n没有对应指标的方案数量: {len(schemes_without_indicators)}")
        if schemes_without_indicators:
            print("前5个没有对应指标的方案:")
            for scheme in schemes_without_indicators[:5]:
                print(f"  - 方案{scheme.scheme_id}: {scheme.name}")
        
    except Exception as e:
        print(f"分析失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(analyze_current_relations())
