#!/usr/bin/env python3
"""
删除我添加的指标方案关联关系，只保留原始数据
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBIndicatorSchemeRelation


async def remove_added_relations():
    """删除我添加的关联关系"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取所有关联关系
        all_relations = await PCBIndicatorSchemeRelation.all().count()
        print(f"删除前总关联关系数量: {all_relations}")
        
        # 删除我添加的关联关系（推荐理由包含"针对指标"或"针对"的）
        my_added_relations = await PCBIndicatorSchemeRelation.filter(
            recommendation_reason__icontains="针对"
        ).all()
        
        print(f"找到我添加的关联关系数量: {len(my_added_relations)}")
        
        if my_added_relations:
            # 删除这些关联关系
            deleted_count = 0
            for relation in my_added_relations:
                await relation.delete()
                deleted_count += 1
            
            print(f"已删除 {deleted_count} 个我添加的关联关系")
        
        # 检查删除后的数量
        remaining_relations = await PCBIndicatorSchemeRelation.all().count()
        print(f"删除后剩余关联关系数量: {remaining_relations}")
        
        # 显示剩余的关联关系
        if remaining_relations > 0:
            print("\n剩余的原始关联关系示例:")
            remaining = await PCBIndicatorSchemeRelation.all().limit(5)
            for relation in remaining:
                print(f"  - 方案ID: {relation.scheme_id}, 指标ID: {relation.indicator_id}")
                print(f"    关联度: {relation.relevance_score}, 优先级: {relation.priority}")
                print(f"    推荐理由: {relation.recommendation_reason}")
        
    except Exception as e:
        print(f"删除失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(remove_added_relations())
