#!/usr/bin/env python3
"""
调试方案关联关系数据
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def debug_scheme_relations():
    """调试方案关联关系"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取前5个方案
        schemes = await PCBScheme.all().order_by("scheme_id").limit(5)
        
        for scheme in schemes:
            print(f"\n方案 {scheme.scheme_id}: {scheme.name}")
            print(f"  方案数据库ID: {scheme.id}")
            
            # 查询关联关系
            relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).all()
            print(f"  找到 {len(relations)} 个关联关系")
            
            for relation in relations:
                indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
                if indicator:
                    print(f"    - 指标{indicator.indicator_id}: {indicator.name}")
                else:
                    print(f"    - 指标ID {relation.indicator_id} 不存在")
        
    except Exception as e:
        print(f"调试失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(debug_scheme_relations())
