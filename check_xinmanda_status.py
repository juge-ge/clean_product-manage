#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查深圳市鑫满达公司(ID:11)的数据状态
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings import settings
from app.models.pcb import PCBEnterprise
from app.models.pcb_planning import PCBLeadershipTeam, PCBWorkTeam, PCBWorkPlan, PCBTrainingRecord
from app.models.pcb_production import PCBProductOutput, PCBQualificationRate, PCBOutputValue


async def check_xinmanda():
    """检查鑫满达公司数据状态"""
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    print("=" * 80)
    print("检查深圳市鑫满达公司(ID:11)数据状态")
    print("=" * 80)
    
    # 1. 检查企业基本信息
    enterprise = await PCBEnterprise.filter(id=11).first()
    if enterprise:
        print(f"\n[OK] 企业基本信息存在")
        print(f"  ID: {enterprise.id}")
        print(f"  名称: {enterprise.name}")
        print(f"  审核状态: {enterprise.audit_status}")
    else:
        print(f"\n[FAIL] 企业ID=11不存在")
        await Tortoise.close_connections()
        return
    
    # 2. 检查筹划与组织数据
    leadership_count = await PCBLeadershipTeam.filter(enterprise_id=11).count()
    workteam_count = await PCBWorkTeam.filter(enterprise_id=11).count()
    workplan_count = await PCBWorkPlan.filter(enterprise_id=11).count()
    training_count = await PCBTrainingRecord.filter(enterprise_id=11).count()
    
    print(f"\n筹划与组织数据:")
    print(f"  领导小组成员: {leadership_count} 条")
    print(f"  工作小组成员: {workteam_count} 条")
    print(f"  工作计划: {workplan_count} 条")
    print(f"  培训记录: {training_count} 条")
    
    # 3. 检查预审核-生产情况数据
    output_count = await PCBProductOutput.filter(enterprise_id=11).count()
    qualification_count = await PCBQualificationRate.filter(enterprise_id=11).count()
    value_count = await PCBOutputValue.filter(enterprise_id=11).count()
    
    print(f"\n预审核-生产情况数据:")
    print(f"  产品产量记录: {output_count} 条")
    print(f"  产品合格率记录: {qualification_count} 条")
    print(f"  产值记录: {value_count} 条")
    
    print("\n" + "=" * 80)
    
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_xinmanda())

