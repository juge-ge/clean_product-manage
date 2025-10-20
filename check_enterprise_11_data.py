#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查深圳市鑫满达公司(ID:11)的数据完整性
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
from app.models.process_equipment import (
    PCBEquipmentRecord
)
from app.models.raw_material import (
    EnterpriseRawMaterialUsage
)


async def check_enterprise_11_data():
    """检查企业ID为11的数据完整性"""
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    print("=== 检查深圳市鑫满达公司(ID:11)数据完整性 ===\n")
    
    enterprise_id = 11
    
    # 1. 检查企业基本信息
    enterprise = await PCBEnterprise.filter(id=enterprise_id).first()
    if enterprise:
        print(f"✓ 企业基本信息存在")
        print(f"  企业名称: {enterprise.name}")
        print(f"  审核状态: {enterprise.audit_status}")
        print(f"  当前步骤: {enterprise.current_step}")
    else:
        print(f"✗ 企业ID {enterprise_id} 不存在")
        return
    
    # 2. 检查生产情况数据
    product_outputs = await PCBProductOutput.filter(enterprise_id=enterprise_id).all()
    qualification_rates = await PCBQualificationRate.filter(enterprise_id=enterprise_id).all()
    output_values = await PCBOutputValue.filter(enterprise_id=enterprise_id).all()
    
    print(f"\n生产情况数据:")
    print(f"  产品产量记录: {len(product_outputs)}条")
    print(f"  产品合格率记录: {len(qualification_rates)}条")
    print(f"  产值记录: {len(output_values)}条")
    
    # 3. 检查资源能源消耗数据
    electricity_records = await PCBElectricityConsumptionRecord.filter(enterprise_id=enterprise_id).all()
    water_records = await PCBWaterConsumptionRecord.filter(enterprise_id=enterprise_id).all()
    gas_records = await PCBGasConsumptionRecord.filter(enterprise_id=enterprise_id).all()
    
    print(f"\n资源能源消耗数据:")
    print(f"  用电记录: {len(electricity_records)}条")
    print(f"  用水记录: {len(water_records)}条")
    print(f"  天然气记录: {len(gas_records)}条")
    
    # 4. 检查污染防治数据
    wastewater_analysis = await PCBWastewaterAnalysis.filter(enterprise_id=enterprise_id).all()
    wastegas_analysis = await PCBWasteGasAnalysis.filter(enterprise_id=enterprise_id).all()
    
    print(f"\n污染防治数据:")
    print(f"  废水分析记录: {len(wastewater_analysis)}条")
    print(f"  废气分析记录: {len(wastegas_analysis)}条")
    
    # 5. 检查固体废物数据
    solid_waste_records = await PCBSolidWasteRecord.filter(enterprise_id=enterprise_id).all()
    
    print(f"\n固体废物数据:")
    print(f"  固体废物记录: {len(solid_waste_records)}条")
    
    # 6. 检查自行监测数据
    organized_gas_monitoring = await PCBOrganizedGasMonitoring.filter(enterprise_id=enterprise_id).all()
    wastewater_monitoring = await PCBWastewaterMonitoring.filter(enterprise_id=enterprise_id).all()
    noise_monitoring = await PCBNoiseMonitoring.filter(enterprise_id=enterprise_id).all()
    
    print(f"\n自行监测数据:")
    print(f"  有组织废气监测记录: {len(organized_gas_monitoring)}条")
    print(f"  废水监测记录: {len(wastewater_monitoring)}条")
    print(f"  噪声监测记录: {len(noise_monitoring)}条")
    
    # 7. 检查工艺装备数据
    equipment_records = await PCBEquipmentRecord.filter(enterprise_id=enterprise_id).all()
    
    print(f"\n工艺装备数据:")
    print(f"  设备记录: {len(equipment_records)}条")
    
    # 8. 检查原辅材料使用数据
    raw_material_usage = await EnterpriseRawMaterialUsage.filter(enterprise_id=enterprise_id).all()
    
    print(f"\n原辅材料使用数据:")
    print(f"  原辅材料使用记录: {len(raw_material_usage)}条")
    
    # 9. 检查预审核数据
    pre_audit_data = await PCBPreAuditData.filter(enterprise_id=enterprise_id).first()
    if pre_audit_data:
        print(f"\n预审核数据:")
        print(f"  状态: {pre_audit_data.status}")
        print(f"  生产信息: {'已录入' if pre_audit_data.production_info else '未录入'}")
        print(f"  原辅材料: {'已录入' if pre_audit_data.raw_materials else '未录入'}")
        print(f"  工艺装备: {'已录入' if pre_audit_data.process_equipment else '未录入'}")
        print(f"  资源消耗: {'已录入' if pre_audit_data.resource_consumption else '未录入'}")
        print(f"  污染防治: {'已录入' if pre_audit_data.pollution_control else '未录入'}")
        print(f"  固体废物: {'已录入' if pre_audit_data.solid_waste else '未录入'}")
        print(f"  自行监测: {'已录入' if pre_audit_data.self_monitoring else '未录入'}")
    else:
        print(f"\n✗ 预审核数据不存在")
    
    # 10. 检查审核报告
    audit_report = await PCBAuditReport.filter(enterprise_id=enterprise_id).first()
    if audit_report:
        print(f"\n审核报告:")
        print(f"  状态: {audit_report.status}")
        print(f"  总分: {audit_report.total_score}")
        print(f"  综合等级: {audit_report.overall_level}")
    else:
        print(f"\n✗ 审核报告不存在")
    
    # 数据完整性总结
    total_records = (
        len(product_outputs) + len(qualification_rates) + len(output_values) +
        len(electricity_records) + len(water_records) + len(gas_records) +
        len(wastewater_analysis) + len(wastegas_analysis) +
        len(solid_waste_records) +
        len(organized_gas_monitoring) + len(wastewater_monitoring) + len(noise_monitoring) +
        len(equipment_records) + len(raw_material_usage) +
        (1 if pre_audit_data else 0) + (1 if audit_report else 0)
    )
    
    print(f"\n=== 数据完整性总结 ===")
    print(f"总记录数: {total_records + 1}条 (包含企业基本信息)")
    
    if total_records > 0:
        print("✓ 数据录入基本完整")
    else:
        print("✗ 数据录入不完整，需要补充")
    
    await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(check_enterprise_11_data())

