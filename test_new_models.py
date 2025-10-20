"""
测试新创建的模型和API
"""
import asyncio
import os
import sys
from tortoise import Tortoise

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.process_equipment import PCBEquipmentRecord, PCBEquipmentCategory
from app.models.pollution_control import PCBWastewaterAnalysis, PCBWasteGasAnalysis
from app.models.solid_waste import PCBSolidWasteRecord, PCBSolidWasteCategory
from app.models.self_monitoring import (
    PCBOrganizedGasMonitoring,
    PCBUnorganizedGasMonitoring,
    PCBWastewaterMonitoring,
    PCBGasEmissionMonitoring,
    PCBNoiseMonitoring
)

async def test_models():
    print("开始测试新创建的模型...")

    # Initialize Tortoise ORM
    await Tortoise.init(
        db_url="sqlite://./test.db", 
        modules={"models": ["app.models.process_equipment", "app.models.pollution_control", "app.models.solid_waste", "app.models.self_monitoring"]}
    )
    await Tortoise.generate_schemas()

    print("模型初始化完成！")

    # 测试创建设备记录
    print("\n测试创建设备记录...")
    equipment = await PCBEquipmentRecord.create(
        enterprise_id=1,
        equipment_name="镀镍金自动线",
        equipment_model="镀铬镀镍金自动处理线",
        motor_model="MAV21325A-02",
        power=35.0,
        quantity=1,
        process="镀镍金自动线",
        status="良好"
    )
    print(f"设备记录创建成功: ID={equipment.id}, 名称={equipment.equipment_name}")

    # 测试创建废水分析
    print("\n测试创建废水分析...")
    wastewater = await PCBWastewaterAnalysis.create(
        enterprise_id=1,
        category="含镍废水",
        source="电镀镍金、化学沉镍、化金等工序产生的废水及处理工序产生废气的废水",
        pollutants="pH、Ni²⁺、SS、CODcr、NH₄⁺、总氮、Cu²⁺、石油类",
        disposal="管道收集分别收集至化学镍调节池和电镀镍废水调节池"
    )
    print(f"废水分析创建成功: ID={wastewater.id}, 类别={wastewater.category}")

    # 测试创建固体废物记录
    print("\n测试创建固体废物记录...")
    waste = await PCBSolidWasteRecord.create(
        enterprise_id=1,
        category="生活垃圾",
        name="生活垃圾",
        unit="吨",
        amount_2020=10.5,
        amount_2021=11.2,
        amount_2022=12.0,
        disposal_method="环卫部门处理"
    )
    print(f"固体废物记录创建成功: ID={waste.id}, 类别={waste.category}")

    # 测试创建有组织废气监测
    print("\n测试创建有组织废气监测...")
    gas_monitoring = await PCBOrganizedGasMonitoring.create(
        enterprise_id=1,
        monitoring_point="监测点位1",
        monitoring_time="2023-01-01",
        nitrogen_oxides=50.5,
        hydrogen_chloride=30.2
    )
    print(f"有组织废气监测创建成功: ID={gas_monitoring.id}, 监测点位={gas_monitoring.monitoring_point}")

    # 测试查询数据
    print("\n测试查询数据...")
    equipment_count = await PCBEquipmentRecord.all().count()
    wastewater_count = await PCBWastewaterAnalysis.all().count()
    waste_count = await PCBSolidWasteRecord.all().count()
    gas_monitoring_count = await PCBOrganizedGasMonitoring.all().count()

    print(f"设备记录总数: {equipment_count}")
    print(f"废水分析总数: {wastewater_count}")
    print(f"固体废物记录总数: {waste_count}")
    print(f"有组织废气监测总数: {gas_monitoring_count}")

    await Tortoise.close_connections()
    print("\n所有测试完成！")

if __name__ == "__main__":
    asyncio.run(test_models())
