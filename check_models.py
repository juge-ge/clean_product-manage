#!/usr/bin/env python3
"""
检查模型是否存在
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings

async def check_models():
    """检查模型是否存在"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models']}
        )
        
        # 检查生产数据相关模型
        print("检查生产数据模型:")
        try:
            from app.models.pcb_production import PCBProductOutput, PCBQualificationRate, PCBOutputValue
            print("  PCBProductOutput: 存在")
            print("  PCBQualificationRate: 存在")
            print("  PCBOutputValue: 存在")
        except ImportError as e:
            print(f"  生产数据模型导入失败: {e}")
        
        # 检查资源能源消耗相关模型
        print("\n检查资源能源消耗模型:")
        try:
            from app.models.resource_consumption import (
                PCBWaterConsumptionRecord, 
                PCBElectricityConsumptionRecord, 
                PCBGasConsumptionRecord,
                PCBResourceConsumptionSummary
            )
            print("  PCBWaterConsumptionRecord: 存在")
            print("  PCBElectricityConsumptionRecord: 存在")
            print("  PCBGasConsumptionRecord: 存在")
            print("  PCBResourceConsumptionSummary: 存在")
        except ImportError as e:
            print(f"  资源能源消耗模型导入失败: {e}")
        
        # 检查表是否存在
        print("\n检查数据库表:")
        try:
            # 检查生产数据表
            product_outputs = await PCBProductOutput.all().count()
            print(f"  pcb_product_output 表记录数: {product_outputs}")
            
            qualification_rates = await PCBQualificationRate.all().count()
            print(f"  pcb_qualification_rate 表记录数: {qualification_rates}")
            
            output_values = await PCBOutputValue.all().count()
            print(f"  pcb_output_value 表记录数: {output_values}")
            
            # 检查资源能源消耗表
            water_records = await PCBWaterConsumptionRecord.all().count()
            print(f"  pcb_water_consumption_record 表记录数: {water_records}")
            
            electricity_records = await PCBElectricityConsumptionRecord.all().count()
            print(f"  pcb_electricity_consumption_record 表记录数: {electricity_records}")
            
            gas_records = await PCBGasConsumptionRecord.all().count()
            print(f"  pcb_gas_consumption_record 表记录数: {gas_records}")
            
            summaries = await PCBResourceConsumptionSummary.all().count()
            print(f"  pcb_resource_consumption_summary 表记录数: {summaries}")
            
        except Exception as e:
            print(f"  检查表失败: {e}")
        
        await Tortoise.close_connections()
        
    except Exception as e:
        print(f"检查失败: {e}")

if __name__ == "__main__":
    asyncio.run(check_models())
