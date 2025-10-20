#!/usr/bin/env python3
"""
检查PCB指标数据
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import PCBIndicator


async def check_indicators():
    """检查指标数据"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 获取所有指标
        indicators = await PCBIndicator.all().order_by("indicator_id")
        
        print(f"数据库中的指标数量: {len(indicators)}")
        
        if len(indicators) == 0:
            print("没有找到指标数据，需要初始化指标数据")
            return
        
        print("\n前10个指标:")
        for i, indicator in enumerate(indicators[:10]):
            print(f"  {indicator.indicator_id}: {indicator.name}")
        
        if len(indicators) > 10:
            print(f"  ... 还有 {len(indicators) - 10} 个指标")
        
        # 检查是否有缺失的指标ID
        indicator_ids = [ind.indicator_id for ind in indicators]
        missing_ids = []
        for i in range(1, 65):  # 检查1-64
            if i not in indicator_ids:
                missing_ids.append(i)
        
        if missing_ids:
            print(f"\n缺失的指标ID: {missing_ids}")
        else:
            print("\n所有64项指标都存在")
        
        # 按类别统计
        categories = {}
        for indicator in indicators:
            category = indicator.category or "未分类"
            if category not in categories:
                categories[category] = 0
            categories[category] += 1
        
        print("\n按类别统计:")
        for category, count in categories.items():
            print(f"  {category}: {count} 个指标")
        
    except Exception as e:
        print(f"检查失败: {e}")
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_indicators())
