#!/usr/bin/env python3
"""
检查方案和指标关联关系数据
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def check_scheme_relations():
    """检查方案和指标关联关系"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取方案数量
        scheme_count = await PCBScheme.all().count()
        print(f"方案数量: {scheme_count}")
        
        # 获取关联关系数量
        relation_count = await PCBIndicatorSchemeRelation.all().count()
        print(f"指标方案关联关系数量: {relation_count}")
        
        if relation_count == 0:
            print("没有找到指标方案关联关系，需要创建一些示例数据")
            return
        
        # 显示前10个关联关系
        print("\n前10个关联关系:")
        relations = await PCBIndicatorSchemeRelation.all().limit(10)
        for relation in relations:
            scheme = await PCBScheme.get_or_none(id=relation.scheme_id)
            indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
            if scheme and indicator:
                print(f"  方案{scheme.scheme_id}({scheme.name}) -> 指标{indicator.indicator_id}({indicator.name})")
        
        # 检查每个方案有多少关联的指标
        print("\n方案关联指标统计:")
        schemes = await PCBScheme.all().limit(10)
        for scheme in schemes:
            relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).all()
            if relations:
                indicator_ids = [r.indicator_id for r in relations]
                print(f"  方案{scheme.scheme_id}: {len(relations)}个指标 {indicator_ids}")
            else:
                print(f"  方案{scheme.scheme_id}: 无关联指标")
        
    except Exception as e:
        print(f"检查失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_scheme_relations())
