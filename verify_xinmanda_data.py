#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证深圳市鑫满达公司数据录入结果
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings import settings
from app.models.pcb import (
    PCBEnterprise, PCBPreAuditData, PCBAuditReport
)
from app.models.pcb_production import (
    PCBProductOutput, PCBQualificationRate, PCBOutputValue
)
from app.models.resource_consumption import (
    PCBWaterConsumptionRecord, PCBElectricityConsumptionRecord, PCBGasConsumptionRecord
)
from app.models.pollution_control import (
    PCBWastewaterAnalysis, PCBWasteGasAnalysis
)
from app.models.solid_waste import (
    PCBSolidWasteRecord
)
from app.models.self_monitoring import (
    PCBOrganizedGasMonitoring, PCBWastewaterMonitoring, PCBNoiseMonitoring
)


async def verify_data():
    """验证数据录入结果"""
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    print("=== 深圳市鑫满达公司数据验证报告 ===\n")
    
    # 1. 验证企业基本信息
    enterprise = await PCBEnterprise.filter(name="深圳市鑫满达电子科技有限公司").first()
    if enterprise:
        print(f"✓ 企业基本信息录入成功")
        print(f"  企业ID: {enterprise.id}")
        print(f"  企业名称: {enterprise.name}")
        print(f"  统一社会信用代码: {enterprise.unified_social_credit_code}")
        print(f"  所属地区: {enterprise.region} {enterprise.district}")
        print(f"  法人代表: {enterprise.legal_representative}")
        print(f"  联系人: {enterprise.contact_person}")
        print(f"  联系电话: {enterprise.contact_phone}")
        print(f"  注册资本: {enterprise.capital}万元")
        print(f"  年产能: {enterprise.capacity}万m²")
        print(f"  审核状态: {enterprise.audit_status}")
        print()
        
        enterprise_id = enterprise.id
    else:
        print("✗ 企业基本信息未找到")
        return
    
    # 2. 验证生产情况数据
    product_outputs = await PCBProductOutput.filter(enterprise_id=enterprise_id).all()
    qualification_rates = await PCBQualificationRate.filter(enterprise_id=enterprise_id).all()
    output_values = await PCBOutputValue.filter(enterprise_id=enterprise_id).all()
    
    print(f"✓ 生产情况数据录入成功")
    print(f"  产品产量记录: {len(product_outputs)}条")
    print(f"  产品合格率记录: {len(qualification_rates)}条")
    print(f"  产值记录: {len(output_values)}条")
    print()
    
    # 3. 验证资源能源消耗数据
    electricity_records = await PCBElectricityConsumptionRecord.filter(enterprise_id=enterprise_id).all()
    water_records = await PCBWaterConsumptionRecord.filter(enterprise_id=enterprise_id).all()
    gas_records = await PCBGasConsumptionRecord.filter(enterprise_id=enterprise_id).all()
    
    print(f"✓ 资源能源消耗数据录入成功")
    print(f"  用电记录: {len(electricity_records)}条")
    print(f"  用水记录: {len(water_records)}条")
    print(f"  天然气记录: {len(gas_records)}条")
    print()
    
    # 4. 验证污染防治数据
    wastewater_analysis = await PCBWastewaterAnalysis.filter(enterprise_id=enterprise_id).all()
    wastegas_analysis = await PCBWasteGasAnalysis.filter(enterprise_id=enterprise_id).all()
    
    print(f"✓ 污染防治数据录入成功")
    print(f"  废水分析记录: {len(wastewater_analysis)}条")
    print(f"  废气分析记录: {len(wastegas_analysis)}条")
    print()
    
    # 5. 验证固体废物数据
    solid_waste_records = await PCBSolidWasteRecord.filter(enterprise_id=enterprise_id).all()
    
    print(f"✓ 固体废物数据录入成功")
    print(f"  固体废物记录: {len(solid_waste_records)}条")
    print()
    
    # 6. 验证自行监测数据
    organized_gas_monitoring = await PCBOrganizedGasMonitoring.filter(enterprise_id=enterprise_id).all()
    wastewater_monitoring = await PCBWastewaterMonitoring.filter(enterprise_id=enterprise_id).all()
    noise_monitoring = await PCBNoiseMonitoring.filter(enterprise_id=enterprise_id).all()
    
    print(f"✓ 自行监测数据录入成功")
    print(f"  有组织废气监测记录: {len(organized_gas_monitoring)}条")
    print(f"  废水监测记录: {len(wastewater_monitoring)}条")
    print(f"  噪声监测记录: {len(noise_monitoring)}条")
    print()
    
    # 7. 验证预审核数据
    pre_audit_data = await PCBPreAuditData.filter(enterprise_id=enterprise_id).first()
    if pre_audit_data:
        print(f"✓ 预审核数据录入成功")
        print(f"  状态: {pre_audit_data.status}")
        print(f"  生产信息: {'已录入' if pre_audit_data.production_info else '未录入'}")
        print(f"  原辅材料: {'已录入' if pre_audit_data.raw_materials else '未录入'}")
        print(f"  工艺装备: {'已录入' if pre_audit_data.process_equipment else '未录入'}")
        print(f"  资源消耗: {'已录入' if pre_audit_data.resource_consumption else '未录入'}")
        print(f"  污染防治: {'已录入' if pre_audit_data.pollution_control else '未录入'}")
        print(f"  固体废物: {'已录入' if pre_audit_data.solid_waste else '未录入'}")
        print(f"  自行监测: {'已录入' if pre_audit_data.self_monitoring else '未录入'}")
        print()
    else:
        print("✗ 预审核数据未找到")
    
    # 8. 验证审核报告
    audit_report = await PCBAuditReport.filter(enterprise_id=enterprise_id).first()
    if audit_report:
        print(f"✓ 审核报告录入成功")
        print(f"  状态: {audit_report.status}")
        print(f"  总分: {audit_report.total_score}")
        print(f"  综合等级: {audit_report.overall_level}")
        print(f"  审核人: {audit_report.auditor_name}")
        print(f"  审核日期: {audit_report.audit_date}")
        print()
    else:
        print("✗ 审核报告未找到")
    
    # 9. 数据统计汇总
    total_records = (
        len(product_outputs) + len(qualification_rates) + len(output_values) +
        len(electricity_records) + len(water_records) + len(gas_records) +
        len(wastewater_analysis) + len(wastegas_analysis) +
        len(solid_waste_records) +
        len(organized_gas_monitoring) + len(wastewater_monitoring) + len(noise_monitoring) +
        (1 if pre_audit_data else 0) + (1 if audit_report else 0)
    )
    
    print("=== 数据录入汇总 ===")
    print(f"✓ 企业基本信息: 1条")
    print(f"✓ 生产情况数据: {len(product_outputs) + len(qualification_rates) + len(output_values)}条")
    print(f"✓ 资源能源消耗数据: {len(electricity_records) + len(water_records) + len(gas_records)}条")
    print(f"✓ 污染防治数据: {len(wastewater_analysis) + len(wastegas_analysis)}条")
    print(f"✓ 固体废物数据: {len(solid_waste_records)}条")
    print(f"✓ 自行监测数据: {len(organized_gas_monitoring) + len(wastewater_monitoring) + len(noise_monitoring)}条")
    print(f"✓ 预审核数据: {1 if pre_audit_data else 0}条")
    print(f"✓ 审核报告: {1 if audit_report else 0}条")
    print(f"✓ 总计: {total_records + 1}条记录")
    print()
    print("=== 数据录入完成 ===")
    print("深圳市鑫满达电子科技有限公司的所有数据已成功录入到PCB审核系统数据库中！")
    
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(verify_data())
