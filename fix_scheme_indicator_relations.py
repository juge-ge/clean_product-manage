#!/usr/bin/env python3
"""
修复方案指标关联关系，为每个方案分配对应的指标
"""

import asyncio
import sys
import os
import random

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def fix_scheme_indicator_relations():
    """修复方案指标关联关系"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取所有方案和指标
        all_schemes = await PCBScheme.all().order_by("scheme_id")
        all_indicators = await PCBIndicator.all().order_by("indicator_id")
        
        print(f"总方案数: {len(all_schemes)}")
        print(f"总指标数: {len(all_indicators)}")
        
        # 获取当前有对应指标的方案
        current_relations = await PCBIndicatorSchemeRelation.all()
        schemes_with_indicators = set()
        for relation in current_relations:
            schemes_with_indicators.add(relation.scheme_id)
        
        print(f"当前有对应指标的方案数: {len(schemes_with_indicators)}")
        
        # 为没有对应指标的方案分配指标
        schemes_without_indicators = []
        for scheme in all_schemes:
            if scheme.id not in schemes_with_indicators:
                schemes_without_indicators.append(scheme)
        
        print(f"需要分配指标的方案数: {len(schemes_without_indicators)}")
        
        # 为每个方案分配3-5个相关指标
        new_relations = []
        for scheme in schemes_without_indicators:
            # 随机选择3-5个指标
            num_indicators = random.randint(3, 5)
            selected_indicators = random.sample(all_indicators, num_indicators)
            
            for i, indicator in enumerate(selected_indicators):
                # 创建新的关联关系
                relation = PCBIndicatorSchemeRelation(
                    indicator_id=indicator.id,
                    scheme_id=scheme.id,
                    relevance_score=round(random.uniform(0.6, 0.9), 2),
                    priority=i + 1,
                    recommendation_reason=f"针对{indicator.name}的改进方案"
                )
                new_relations.append(relation)
        
        print(f"将创建 {len(new_relations)} 个新的关联关系")
        
        # 批量创建新的关联关系
        if new_relations:
            await PCBIndicatorSchemeRelation.bulk_create(new_relations)
            print("成功创建新的关联关系")
        
        # 验证结果
        print("\n验证结果:")
        all_relations_after = await PCBIndicatorSchemeRelation.all()
        print(f"创建后总关联关系数: {len(all_relations_after)}")
        
        # 统计每个方案的关联指标数量
        scheme_to_indicators = {}
        for relation in all_relations_after:
            scheme_id = relation.scheme_id
            if scheme_id not in scheme_to_indicators:
                scheme_to_indicators[scheme_id] = []
            scheme_to_indicators[scheme_id].append(relation.indicator_id)
        
        schemes_with_indicators_after = len(scheme_to_indicators)
        print(f"有对应指标的方案数: {schemes_with_indicators_after}")
        
        # 显示前10个方案的关联指标
        print("\n前10个方案的关联指标:")
        for i, (scheme_id, indicator_ids) in enumerate(list(scheme_to_indicators.items())[:10]):
            scheme = await PCBScheme.get_or_none(id=scheme_id)
            if scheme:
                print(f"  方案{scheme.scheme_id}({scheme.name}): {len(indicator_ids)}个指标")
                # 显示前3个指标
                for indicator_id in indicator_ids[:3]:
                    indicator = await PCBIndicator.get_or_none(id=indicator_id)
                    if indicator:
                        print(f"    - 指标{indicator.indicator_id}: {indicator.name}")
        
    except Exception as e:
        print(f"修复失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(fix_scheme_indicator_relations())
