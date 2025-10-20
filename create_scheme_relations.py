#!/usr/bin/env python3
"""
为所有方案创建合理的指标关联关系
"""

import asyncio
import sys
import os
import random
from decimal import Decimal

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation


async def create_scheme_relations():
    """为所有方案创建合理的指标关联关系"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取所有方案和指标
        schemes = await PCBScheme.all().order_by("scheme_id")
        indicators = await PCBIndicator.all().order_by("indicator_id")
        
        print(f"找到 {len(schemes)} 个方案和 {len(indicators)} 个指标")
        
        # 为每个方案创建关联关系
        relations_created = 0
        for scheme in schemes:
            # 检查是否已有关联关系
            existing_relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).count()
            if existing_relations > 0:
                print(f"方案{scheme.scheme_id}已有{existing_relations}个关联关系，跳过")
                continue
            
            # 根据方案类型和描述选择合适的指标
            related_indicators = select_related_indicators(scheme, indicators)
            
            # 创建关联关系
            for i, indicator in enumerate(related_indicators):
                await PCBIndicatorSchemeRelation.create(
                    indicator_id=indicator.id,
                    scheme_id=scheme.id,
                    relevance_score=Decimal(str(0.8 - i * 0.1)),  # 0.8, 0.7, 0.6...
                    priority=i + 1,
                    recommendation_reason=f"针对{indicator.name}的改进方案"
                )
                relations_created += 1
            
            print(f"为方案{scheme.scheme_id}创建了{len(related_indicators)}个关联关系")
        
        print(f"\n总共创建了 {relations_created} 个新的关联关系")
        
    except Exception as e:
        print(f"创建关联关系失败: {e}")
    finally:
        await Tortoise.close_connections()


def select_related_indicators(scheme, indicators):
    """根据方案选择合适的指标"""
    related_indicators = []
    
    # 根据方案名称和描述选择相关指标
    scheme_name = scheme.name.lower() if scheme.name else ""
    scheme_desc = scheme.description.lower() if scheme.description else ""
    scheme_problem = scheme.problem.lower() if scheme.problem else ""
    
    # 关键词匹配
    keywords = {
        "废水": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42],  # 废水相关指标
        "废气": [43, 44, 45, 46],  # 废气相关指标
        "能耗": [7, 8, 9, 10, 11, 12, 13, 14],  # 能耗相关指标
        "水耗": [15, 16, 17, 18, 19],  # 水耗相关指标
        "固废": [29],  # 固废相关指标
        "电镀": [6],  # 电镀相关指标
        "蚀刻": [5],  # 蚀刻相关指标
        "工艺": [1, 2, 3, 4],  # 工艺相关指标
        "设备": [1, 2, 3, 4],  # 设备相关指标
        "自动化": [1, 2, 3, 4],  # 自动化相关指标
        "回收": [20, 21, 22, 23, 24, 25, 26, 27, 28],  # 回收相关指标
        "管理": [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64],  # 管理相关指标
    }
    
    # 匹配关键词
    matched_indicators = set()
    for keyword, indicator_ids in keywords.items():
        if keyword in scheme_name or keyword in scheme_desc or keyword in scheme_problem:
            for indicator_id in indicator_ids:
                indicator = next((ind for ind in indicators if ind.indicator_id == indicator_id), None)
                if indicator:
                    matched_indicators.add(indicator)
    
    # 如果没有匹配到，随机选择一些指标
    if not matched_indicators:
        # 随机选择3-5个指标
        num_indicators = random.randint(3, 5)
        matched_indicators = set(random.sample(indicators, min(num_indicators, len(indicators))))
    
    # 限制关联指标数量（最多5个）
    related_indicators = list(matched_indicators)[:5]
    
    return related_indicators


if __name__ == "__main__":
    asyncio.run(create_scheme_relations())
