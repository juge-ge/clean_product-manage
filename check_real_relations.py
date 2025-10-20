#!/usr/bin/env python3
"""
检查真实的指标方案关联关系
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def check_real_relations():
    """检查真实的指标方案关联关系"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取所有关联关系
        all_relations = await PCBIndicatorSchemeRelation.all()
        print(f"总关联关系数量: {len(all_relations)}")
        
        # 检查前20个关联关系的详细信息
        print("\n前20个关联关系详情:")
        for i, relation in enumerate(all_relations[:20]):
            scheme = await PCBScheme.get_or_none(id=relation.scheme_id)
            indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
            if scheme and indicator:
                print(f"  {i+1}. 方案ID: {relation.scheme_id} ({scheme.scheme_id}) - {scheme.name}")
                print(f"     指标ID: {relation.indicator_id} ({indicator.indicator_id}) - {indicator.name}")
                print(f"     关联度: {relation.relevance_score}, 优先级: {relation.priority}")
                print(f"     推荐理由: {relation.recommendation_reason}")
                print()
        
        # 统计每个方案有多少关联指标
        print("每个方案的关联指标统计:")
        schemes = await PCBScheme.all().order_by("scheme_id")
        for scheme in schemes:
            relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).all()
            if relations:
                indicator_ids = [r.indicator_id for r in relations]
                indicator_names = []
                for r in relations:
                    indicator = await PCBIndicator.get_or_none(id=r.indicator_id)
                    if indicator:
                        indicator_names.append(f"{indicator.indicator_id}({indicator.name})")
                print(f"  方案{scheme.scheme_id}: {len(relations)}个指标 - {indicator_names}")
        
        # 统计每个指标有多少关联方案
        print("\n每个指标的关联方案统计:")
        indicators = await PCBIndicator.all().order_by("indicator_id")
        for indicator in indicators:
            relations = await PCBIndicatorSchemeRelation.filter(indicator_id=indicator.id).all()
            if relations:
                scheme_ids = [r.scheme_id for r in relations]
                scheme_names = []
                for r in relations:
                    scheme = await PCBScheme.get_or_none(id=r.scheme_id)
                    if scheme:
                        scheme_names.append(f"{scheme.scheme_id}({scheme.name})")
                print(f"  指标{indicator.indicator_id}: {len(relations)}个方案 - {scheme_names}")
        
    except Exception as e:
        print(f"检查失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_real_relations())
