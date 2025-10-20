#!/usr/bin/env python3
"""
检查最终的原始数据分布
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def check_final_data():
    """检查最终数据"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取所有关联关系
        all_relations = await PCBIndicatorSchemeRelation.all().count()
        print(f"当前关联关系总数: {all_relations}")
        
        # 检查每个方案有多少关联指标
        schemes = await PCBScheme.all().order_by("scheme_id").limit(20)
        
        print("\n前20个方案的关联指标统计:")
        for scheme in schemes:
            relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).all()
            if relations:
                indicator_ids = [r.indicator_id for r in relations]
                print(f"  方案{scheme.scheme_id}: {len(relations)}个指标 {indicator_ids}")
            else:
                print(f"  方案{scheme.scheme_id}: 无关联指标")
        
        # 统计有/无关联指标的方案数量
        schemes_with_relations = 0
        schemes_without_relations = 0
        
        all_schemes = await PCBScheme.all()
        for scheme in all_schemes:
            relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).count()
            if relations > 0:
                schemes_with_relations += 1
            else:
                schemes_without_relations += 1
        
        print(f"\n方案关联统计:")
        print(f"  有关联指标的方案: {schemes_with_relations} 个")
        print(f"  无关联指标的方案: {schemes_without_relations} 个")
        print(f"  总方案数: {len(all_schemes)} 个")
        
    except Exception as e:
        print(f"检查失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_final_data())
