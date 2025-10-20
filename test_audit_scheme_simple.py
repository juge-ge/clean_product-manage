#!/usr/bin/env python3
"""
简化版PCB审核和方案选择功能测试
"""

import asyncio
import sys
import os
from decimal import Decimal

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings
from app.models.pcb import (
    PCBEnterprise, PCBIndicator, PCBScheme, 
    PCBIndicatorSchemeRelation, PCBAuditResult
)
from app.controllers.pcb import (
    PCBAuditResultController, PCBIndicatorSchemeRelationController
)


async def test_basic_functionality():
    """测试基本功能"""
    print("测试基本功能...")
    
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models.pcb']}
        )
        
        # 测试1: 检查数据
        enterprise_count = await PCBEnterprise.all().count()
        indicator_count = await PCBIndicator.all().count()
        scheme_count = await PCBScheme.all().count()
        relation_count = await PCBIndicatorSchemeRelation.all().count()
        
        print(f"数据统计:")
        print(f"  - 企业: {enterprise_count}")
        print(f"  - 指标: {indicator_count}")
        print(f"  - 方案: {scheme_count}")
        print(f"  - 关联关系: {relation_count}")
        
        # 测试2: 创建测试企业
        enterprise = await PCBEnterprise.get_or_create(
            name="测试PCB企业",
            defaults={
                "region": "广东省",
                "district": "深圳市",
                "address": "测试地址",
                "legal_representative": "测试法人",
                "contact_person": "测试联系人",
                "contact_phone": "13800138000",
                "contact_email": "test@example.com",
                "industry_type": "PCB制造",
                "capacity": Decimal("100.00"),
                "audit_status": "pending"
            }
        )
        enterprise = enterprise[0]
        print(f"创建测试企业: {enterprise.name} (ID: {enterprise.id})")
        
        # 测试3: 获取指标和方案
        indicators = await PCBIndicator.all().limit(3)
        schemes = await PCBScheme.all().limit(3)
        
        if not indicators or not schemes:
            print("缺少指标或方案数据")
            return False
        
        print(f"找到 {len(indicators)} 个指标和 {len(schemes)} 个方案")
        
        # 测试4: 创建关联关系
        controller = PCBIndicatorSchemeRelationController()
        relation = await controller.create_relation(
            indicator_id=indicators[0].id,
            scheme_id=schemes[0].id,
            relevance_score=Decimal("0.9"),
            priority=1,
            recommendation_reason="测试推荐理由"
        )
        print(f"创建关联关系: 指标{indicators[0].id} -> 方案{schemes[0].id}")
        
        # 测试5: 创建审核结果
        audit_controller = PCBAuditResultController()
        result = await audit_controller.update_indicator_level(
            enterprise_id=enterprise.id,
            indicator_id=indicators[0].id,
            level="II级",
            score=Decimal("80.0"),
            selected_scheme_ids=[schemes[0].id]
        )
        print(f"创建审核结果: 指标{indicators[0].id} -> {result.level}")
        print(f"选择方案: {result.selected_scheme_ids}")
        
        # 测试6: 获取推荐方案
        recommended_schemes = await audit_controller.get_indicator_recommended_schemes(
            enterprise.id, indicators[0].id
        )
        print(f"获取推荐方案: {len(recommended_schemes)} 个")
        
        if recommended_schemes:
            scheme = recommended_schemes[0]
            print(f"方案详情: {scheme.get('name', 'N/A')}")
        
        print("所有测试通过!")
        return True
        
    except Exception as e:
        print(f"测试失败: {e}")
        return False
    finally:
        await Tortoise.close_connections()


async def main():
    """主函数"""
    print("开始PCB审核和方案选择功能测试...")
    
    success = await test_basic_functionality()
    
    if success:
        print("测试完成: 所有功能正常!")
    else:
        print("测试完成: 发现问题，请检查!")


if __name__ == "__main__":
    asyncio.run(main())
