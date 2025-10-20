#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为深圳市鑫满达公司添加原辅材料使用数据
根据深圳市鑫满达公司数据.md中的数据
"""

import asyncio
import sys
import os
from decimal import Decimal

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings import settings
from app.models.raw_material import RawMaterial, EnterpriseRawMaterialUsage


async def add_raw_material_usage():
    """添加原辅材料使用数据"""
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    print("=" * 80)
    print("Adding Xinmanda Raw Material Usage Data")
    print("=" * 80)
    
    enterprise_id = 11
    
    try:
        # 根据深圳市鑫满达公司数据.md中的主要原材料数据
        # material_id: 1-覆铜板, 2-铜箔, 3-玻璃纤维布, 4-环氧树脂, 5-蚀刻液, 6-电镀液, 10-阻焊油墨, 11-助焊剂
        
        materials_data = [
            # 覆铜板 (material_id=1)
            {
                "material_id": 1,
                "year": "2022",
                "amount": Decimal("1250000"),
                "unit": "kg",
                "process": "开料",
                "state": "固体",
                "voc_content": None
            },
            {
                "material_id": 1,
                "year": "2023",
                "amount": Decimal("1420000"),
                "unit": "kg",
                "process": "开料",
                "state": "固体",
                "voc_content": None
            },
            {
                "material_id": 1,
                "year": "2024",
                "amount": Decimal("1580000"),
                "unit": "kg",
                "process": "开料",
                "state": "固体",
                "voc_content": None
            },
            # 铜箔 (material_id=2)
            {
                "material_id": 2,
                "year": "2022",
                "amount": Decimal("850000"),
                "unit": "kg",
                "process": "压合",
                "state": "固体",
                "voc_content": None
            },
            {
                "material_id": 2,
                "year": "2023",
                "amount": Decimal("960000"),
                "unit": "kg",
                "process": "压合",
                "state": "固体",
                "voc_content": None
            },
            {
                "material_id": 2,
                "year": "2024",
                "amount": Decimal("1080000"),
                "unit": "kg",
                "process": "压合",
                "state": "固体",
                "voc_content": None
            },
            # 玻璃纤维布 (material_id=3, 假设存在)
            {
                "material_id": 3,
                "year": "2022",
                "amount": Decimal("2800000"),
                "unit": "m²",
                "process": "压合",
                "state": "固体",
                "voc_content": None
            },
            {
                "material_id": 3,
                "year": "2023",
                "amount": Decimal("3200000"),
                "unit": "m²",
                "process": "压合",
                "state": "固体",
                "voc_content": None
            },
            {
                "material_id": 3,
                "year": "2024",
                "amount": Decimal("3600000"),
                "unit": "m²",
                "process": "压合",
                "state": "固体",
                "voc_content": None
            },
            # 环氧树脂 (material_id=4, 假设存在)
            {
                "material_id": 4,
                "year": "2022",
                "amount": Decimal("180000"),
                "unit": "kg",
                "process": "压合",
                "state": "液体",
                "voc_content": Decimal("5.0")
            },
            {
                "material_id": 4,
                "year": "2023",
                "amount": Decimal("205000"),
                "unit": "kg",
                "process": "压合",
                "state": "液体",
                "voc_content": Decimal("5.0")
            },
            {
                "material_id": 4,
                "year": "2024",
                "amount": Decimal("230000"),
                "unit": "kg",
                "process": "压合",
                "state": "液体",
                "voc_content": Decimal("5.0")
            },
            # 蚀刻液 (material_id=5)
            {
                "material_id": 5,
                "year": "2022",
                "amount": Decimal("45000"),
                "unit": "L",
                "process": "蚀刻",
                "state": "液体",
                "voc_content": None
            },
            {
                "material_id": 5,
                "year": "2023",
                "amount": Decimal("52000"),
                "unit": "L",
                "process": "蚀刻",
                "state": "液体",
                "voc_content": None
            },
            {
                "material_id": 5,
                "year": "2024",
                "amount": Decimal("58000"),
                "unit": "L",
                "process": "蚀刻",
                "state": "液体",
                "voc_content": None
            },
            # 电镀液 (material_id=6, 假设存在)
            {
                "material_id": 6,
                "year": "2022",
                "amount": Decimal("38000"),
                "unit": "L",
                "process": "电镀",
                "state": "液体",
                "voc_content": None
            },
            {
                "material_id": 6,
                "year": "2023",
                "amount": Decimal("43000"),
                "unit": "L",
                "process": "电镀",
                "state": "液体",
                "voc_content": None
            },
            {
                "material_id": 6,
                "year": "2024",
                "amount": Decimal("48000"),
                "unit": "L",
                "process": "电镀",
                "state": "液体",
                "voc_content": None
            },
            # 阻焊油墨 (material_id=10)
            {
                "material_id": 10,
                "year": "2022",
                "amount": Decimal("65000"),
                "unit": "kg",
                "process": "阻焊",
                "state": "液体",
                "voc_content": Decimal("15.5")
            },
            {
                "material_id": 10,
                "year": "2023",
                "amount": Decimal("75000"),
                "unit": "kg",
                "process": "阻焊",
                "state": "液体",
                "voc_content": Decimal("15.5")
            },
            {
                "material_id": 10,
                "year": "2024",
                "amount": Decimal("85000"),
                "unit": "kg",
                "process": "阻焊",
                "state": "液体",
                "voc_content": Decimal("15.5")
            },
            # 助焊剂 (material_id=11, 假设存在)
            {
                "material_id": 11,
                "year": "2022",
                "amount": Decimal("12000"),
                "unit": "kg",
                "process": "表面处理",
                "state": "液体",
                "voc_content": Decimal("8.0")
            },
            {
                "material_id": 11,
                "year": "2023",
                "amount": Decimal("14000"),
                "unit": "kg",
                "process": "表面处理",
                "state": "液体",
                "voc_content": Decimal("8.0")
            },
            {
                "material_id": 11,
                "year": "2024",
                "amount": Decimal("16000"),
                "unit": "kg",
                "process": "表面处理",
                "state": "液体",
                "voc_content": Decimal("8.0")
            }
        ]
        
        # 先删除已有数据（如果有）
        print("\nClearing existing raw material usage data...")
        deleted = await EnterpriseRawMaterialUsage.filter(enterprise_id=enterprise_id).delete()
        print(f"Deleted {deleted} old records")
        
        # 添加新数据
        print("\nAdding new raw material usage data...")
        count = 0
        for data in materials_data:
            try:
                # 检查material_id对应的材料是否存在
                material = await RawMaterial.filter(id=data['material_id']).first()
                if not material:
                    print(f"  Warning: Material ID {data['material_id']} not found, skipping...")
                    continue
                
                await EnterpriseRawMaterialUsage.create(
                    enterprise_id=enterprise_id,
                    **data
                )
                count += 1
            except Exception as e:
                print(f"  Error adding material {data['material_id']}: {str(e)}")
        
        print(f"\nSuccessfully added {count} raw material usage records")
        
        # 验证数据
        print("\nVerifying...")
        total = await EnterpriseRawMaterialUsage.filter(enterprise_id=enterprise_id).count()
        print(f"Total raw material usage records for enterprise {enterprise_id}: {total}")
        
        print("\n" + "=" * 80)
        print("Completed!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        await Tortoise.close_connections()


if __name__ == "__main__":
    asyncio.run(add_raw_material_usage())

