#!/usr/bin/env python3
"""
详细测试API查询逻辑
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBScheme, PCBIndicator, PCBIndicatorSchemeRelation
from app.controllers.pcb import pcb_scheme_controller


async def test_api_logic():
    """测试API查询逻辑"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 模拟API中的查询逻辑
        print("=== 测试方案查询逻辑 ===")
        schemes, total = await pcb_scheme_controller.search_schemes(
            page=1,
            page_size=5,
            search=None,
            scheme_type=None,
            indicator_ids=None
        )
        
        print(f"查询到 {len(schemes)} 个方案，总数: {total}")
        
        # 模拟API中的数据处理逻辑
        data = []
        for scheme in schemes:
            print(f"\n处理方案 {scheme.scheme_id}: {scheme.name}")
            print(f"  方案数据库ID: {scheme.id}")
            
            scheme_dict = await scheme.to_dict()
            print(f"  to_dict()结果: {list(scheme_dict.keys())}")
            
            # 获取关联的指标信息
            relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).all()
            print(f"  找到 {len(relations)} 个关联关系")
            
            related_indicators = []
            for relation in relations:
                indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
                if indicator:
                    related_indicators.append({
                        "id": indicator.id,
                        "name": indicator.name,
                        "relevance_score": float(relation.relevance_score),
                        "priority": relation.priority,
                        "recommendation_reason": relation.recommendation_reason
                    })
                    print(f"    - 指标{indicator.indicator_id}: {indicator.name}")
            
            scheme_dict["related_indicators"] = related_indicators
            data.append(scheme_dict)
        
        print(f"\n最终数据包含 {len(data)} 个方案")
        for i, scheme_data in enumerate(data):
            related_count = len(scheme_data.get('related_indicators', []))
            print(f"  方案{i+1}: {related_count}个关联指标")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(test_api_logic())
