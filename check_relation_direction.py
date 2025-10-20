#!/usr/bin/env python3
"""
检查关联关系的方向
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def check_relation_direction():
    """检查关联关系的方向"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取所有关联关系
        all_relations = await PCBIndicatorSchemeRelation.all()
        print(f"总关联关系数量: {len(all_relations)}")
        
        # 检查前10个关联关系
        print("\n前10个关联关系:")
        for i, relation in enumerate(all_relations[:10]):
            scheme = await PCBScheme.get_or_none(id=relation.scheme_id)
            indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
            if scheme and indicator:
                print(f"  {i+1}. 指标{indicator.indicator_id}({indicator.name}) -> 方案{scheme.scheme_id}({scheme.name})")
        
        # 统计每个方案有多少关联指标
        print("\n每个方案的关联指标统计:")
        schemes = await PCBScheme.all().order_by("scheme_id")
        schemes_with_relations = 0
        schemes_without_relations = 0
        
        for scheme in schemes:
            relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).count()
            if relations > 0:
                schemes_with_relations += 1
                if schemes_with_relations <= 10:  # 只显示前10个
                    relations_list = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).all()
                    indicator_names = []
                    for r in relations_list:
                        indicator = await PCBIndicator.get_or_none(id=r.indicator_id)
                        if indicator:
                            indicator_names.append(f"{indicator.indicator_id}({indicator.name})")
                    print(f"  方案{scheme.scheme_id}: {relations}个指标 - {indicator_names}")
            else:
                schemes_without_relations += 1
        
        print(f"\n统计结果:")
        print(f"  有关联指标的方案: {schemes_with_relations} 个")
        print(f"  无关联指标的方案: {schemes_without_relations} 个")
        print(f"  总方案数: {len(schemes)} 个")
        
        # 检查是否有重复的关联关系
        print("\n检查重复关联关系:")
        relation_pairs = {}
        for relation in all_relations:
            key = f"{relation.indicator_id}-{relation.scheme_id}"
            if key in relation_pairs:
                relation_pairs[key] += 1
            else:
                relation_pairs[key] = 1
        
        duplicates = {k: v for k, v in relation_pairs.items() if v > 1}
        if duplicates:
            print(f"  发现 {len(duplicates)} 个重复的关联关系")
            for key, count in list(duplicates.items())[:5]:
                print(f"    {key}: {count}次")
        else:
            print("  无重复关联关系")
        
    except Exception as e:
        print(f"检查失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_relation_direction())
