#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深圳市鑫满达公司数据录入脚本 - 简化版
"""

import asyncio
import json
import sys
import os
from datetime import datetime, date
from decimal import Decimal

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


class XinmandaDataInserter:
    """深圳市鑫满达公司数据录入器"""
    
    def __init__(self):
        self.enterprise_id = None
        
    async def init_database(self):
        """初始化数据库连接"""
        await Tortoise.init(config=settings.TORTOISE_ORM)
        print("数据库连接初始化成功")
    
    async def close_database(self):
        """关闭数据库连接"""
        await Tortoise.close_connections()
        print("数据库连接已关闭")
    
    async def create_enterprise(self):
        """创建企业基本信息"""
        print("正在创建企业基本信息...")
        
        enterprise_data = {
            "name": "深圳市鑫满达电子科技有限公司",
            "unified_social_credit_code": "91440300MA5F8K9X2L",
            "region": "深圳市",
            "district": "宝安区",
            "address": "深圳市宝安区西乡街道固戍社区固戍一路88号鑫满达科技园",
            "legal_representative": "陈志强",
            "contact_person": "李工程师",
            "contact_phone": "0755-2798-8888",
            "contact_email": "info@xinmanda.com",
            "industry_type": "PCB制造",
            "capital": Decimal("5000.00"),
            "capacity": Decimal("120.00"),
            "audit_status": "pending",
            "current_step": 0
        }
        
        enterprise = await PCBEnterprise.create(**enterprise_data)
        self.enterprise_id = enterprise.id
        print(f"企业创建成功，ID: {self.enterprise_id}")
        return enterprise
    
    async def create_production_data(self):
        """创建生产情况数据"""
        print("正在创建生产情况数据...")
        
        # 产品产量数据
        product_outputs = [
            {"type": "rigid", "main_product": "单面板", "year": "2022", "output": Decimal("15.2"), "unit": "万m²"},
            {"type": "rigid", "main_product": "单面板", "year": "2023", "output": Decimal("18.5"), "unit": "万m²"},
            {"type": "rigid", "main_product": "单面板", "year": "2024", "output": Decimal("22.3"), "unit": "万m²"},
            {"type": "rigid", "main_product": "双面板", "year": "2022", "output": Decimal("45.8"), "unit": "万m²"},
            {"type": "rigid", "main_product": "双面板", "year": "2023", "output": Decimal("52.6"), "unit": "万m²"},
            {"type": "rigid", "main_product": "双面板", "year": "2024", "output": Decimal("58.9"), "unit": "万m²"},
            {"type": "rigid", "main_product": "多层板(4-8层)", "year": "2022", "output": Decimal("28.6"), "unit": "万m²", "layers": 6},
            {"type": "rigid", "main_product": "多层板(4-8层)", "year": "2023", "output": Decimal("32.1"), "unit": "万m²", "layers": 6},
            {"type": "rigid", "main_product": "多层板(4-8层)", "year": "2024", "output": Decimal("35.7"), "unit": "万m²", "layers": 6},
            {"type": "rigid", "main_product": "HDI板", "year": "2022", "output": Decimal("8.4"), "unit": "万m²", "layers": 8},
            {"type": "rigid", "main_product": "HDI板", "year": "2023", "output": Decimal("12.3"), "unit": "万m²", "layers": 8},
            {"type": "rigid", "main_product": "HDI板", "year": "2024", "output": Decimal("15.2"), "unit": "万m²", "layers": 8},
            {"type": "flexible", "main_product": "软硬结合板", "year": "2022", "output": Decimal("2.1"), "unit": "万m²"},
            {"type": "flexible", "main_product": "软硬结合板", "year": "2023", "output": Decimal("3.2"), "unit": "万m²"},
            {"type": "flexible", "main_product": "软硬结合板", "year": "2024", "output": Decimal("4.8"), "unit": "万m²"},
        ]
        
        for data in product_outputs:
            data["enterprise_id"] = self.enterprise_id
            await PCBProductOutput.create(**data)
        
        # 产品合格率数据
        qualification_rates = [
            {"year": "2022", "rate": Decimal("97.2")},
            {"year": "2023", "rate": Decimal("97.8")},
            {"year": "2024", "rate": Decimal("98.3")},
        ]
        
        for data in qualification_rates:
            data["enterprise_id"] = self.enterprise_id
            await PCBQualificationRate.create(**data)
        
        # 产值数据
        output_values = [
            {"year": "2022", "unit": "万元", "annual_output_value": Decimal("28500.00")},
            {"year": "2023", "unit": "万元", "annual_output_value": Decimal("32500.00")},
            {"year": "2024", "unit": "万元", "annual_output_value": Decimal("36800.00")},
        ]
        
        for data in output_values:
            data["enterprise_id"] = self.enterprise_id
            await PCBOutputValue.create(**data)
        
        print("生产情况数据创建成功")
    
    async def create_resource_consumption_data(self):
        """创建资源能源消耗数据"""
        print("正在创建资源能源消耗数据...")
        
        # 用电数据
        electricity_data = [
            {"project": "生产车间用电", "unit": "kWh", "amount_2022": Decimal("8500000"), "amount_2023": Decimal("9600000"), "amount_2024": Decimal("10800000")},
            {"project": "辅助生产用电", "unit": "kWh", "amount_2022": Decimal("1200000"), "amount_2023": Decimal("1350000"), "amount_2024": Decimal("1500000")},
            {"project": "办公用电", "unit": "kWh", "amount_2022": Decimal("180000"), "amount_2023": Decimal("200000"), "amount_2024": Decimal("220000")},
            {"project": "生活用电", "unit": "kWh", "amount_2022": Decimal("150000"), "amount_2023": Decimal("170000"), "amount_2024": Decimal("190000")},
            {"project": "照明用电", "unit": "kWh", "amount_2022": Decimal("200000"), "amount_2023": Decimal("220000"), "amount_2024": Decimal("240000")},
            {"project": "空调用电", "unit": "kWh", "amount_2022": Decimal("800000"), "amount_2023": Decimal("900000"), "amount_2024": Decimal("1000000")},
        ]
        
        for data in electricity_data:
            data["enterprise_id"] = self.enterprise_id
            await PCBElectricityConsumptionRecord.create(**data)
        
        # 用水数据
        water_data = [
            {"project": "生产用水", "unit": "m³", "amount_2022": Decimal("85000"), "amount_2023": Decimal("95000"), "amount_2024": Decimal("105000")},
            {"project": "生活用水", "unit": "m³", "amount_2022": Decimal("12000"), "amount_2023": Decimal("13500"), "amount_2024": Decimal("15000")},
            {"project": "办公用水", "unit": "m³", "amount_2022": Decimal("3000"), "amount_2023": Decimal("3500"), "amount_2024": Decimal("4000")},
            {"project": "冷却用水", "unit": "m³", "amount_2022": Decimal("15000"), "amount_2023": Decimal("17000"), "amount_2024": Decimal("19000")},
            {"project": "清洗用水", "unit": "m³", "amount_2022": Decimal("8000"), "amount_2023": Decimal("9000"), "amount_2024": Decimal("10000")},
        ]
        
        for data in water_data:
            data["enterprise_id"] = self.enterprise_id
            await PCBWaterConsumptionRecord.create(**data)
        
        # 天然气数据
        gas_data = [
            {"project": "锅炉天然气", "unit": "m³", "amount_2022": Decimal("45000"), "amount_2023": Decimal("50000"), "amount_2024": Decimal("55000")},
            {"project": "工业煤气", "unit": "m³", "amount_2022": Decimal("12000"), "amount_2023": Decimal("13500"), "amount_2024": Decimal("15000")},
        ]
        
        for data in gas_data:
            data["enterprise_id"] = self.enterprise_id
            await PCBGasConsumptionRecord.create(**data)
        
        print("资源能源消耗数据创建成功")
    
    async def create_pollution_control_data(self):
        """创建污染防治数据"""
        print("正在创建污染防治数据...")
        
        # 废水分析数据
        wastewater_data = [
            {
                "category": "含铜废水",
                "source": "电镀、蚀刻工序",
                "pollutants": "总铜、COD、SS",
                "disposal": "化学沉淀+膜过滤，总铜<0.5mg/L"
            },
            {
                "category": "有机废水",
                "source": "清洗、显影工序",
                "pollutants": "COD、SS、有机污染物",
                "disposal": "生化处理+深度处理，COD<50mg/L"
            },
            {
                "category": "酸碱废水",
                "source": "酸洗、碱洗工序",
                "pollutants": "pH、SS",
                "disposal": "中和处理，pH 6-9"
            },
            {
                "category": "清洗废水",
                "source": "设备清洗、地面清洗",
                "pollutants": "SS、COD",
                "disposal": "混凝沉淀，SS<30mg/L"
            }
        ]
        
        for data in wastewater_data:
            data["enterprise_id"] = self.enterprise_id
            await PCBWastewaterAnalysis.create(**data)
        
        # 废气分析数据
        wastegas_data = [
            {
                "gas_type": "有机废气",
                "pollutants": "非甲烷总烃、苯、甲苯、二甲苯",
                "location": "印刷、清洗、烘干工序",
                "treatment": "活性炭吸附+催化燃烧，非甲烷总烃<50mg/m³"
            },
            {
                "gas_type": "酸雾废气",
                "pollutants": "硫酸雾、盐酸雾",
                "location": "酸洗、蚀刻工序",
                "treatment": "碱液喷淋，硫酸雾<30mg/m³"
            },
            {
                "gas_type": "粉尘废气",
                "pollutants": "颗粒物",
                "location": "钻孔、打磨工序",
                "treatment": "布袋除尘，颗粒物<20mg/m³"
            }
        ]
        
        for data in wastegas_data:
            data["enterprise_id"] = self.enterprise_id
            await PCBWasteGasAnalysis.create(**data)
        
        print("污染防治数据创建成功")
    
    async def create_solid_waste_data(self):
        """创建固体废物数据"""
        print("正在创建固体废物数据...")
        
        # 固体废物记录
        solid_waste_data = [
            {"category": "金属废物", "name": "废铜屑", "unit": "吨", "amount_2022": Decimal("85"), "amount_2023": Decimal("95"), "amount_2024": Decimal("105"), "disposal_method": "回收利用"},
            {"category": "边角料", "name": "废边角料", "unit": "吨", "amount_2022": Decimal("120"), "amount_2023": Decimal("135"), "amount_2024": Decimal("150"), "disposal_method": "回收利用"},
            {"category": "危险废物", "name": "废化学试剂", "unit": "吨", "amount_2022": Decimal("15"), "amount_2023": Decimal("18"), "amount_2024": Decimal("20"), "disposal_method": "危废处置"},
            {"category": "危险废物", "name": "废活性炭", "unit": "吨", "amount_2022": Decimal("8"), "amount_2023": Decimal("10"), "amount_2024": Decimal("12"), "disposal_method": "危废处置"},
            {"category": "危险废物", "name": "污泥", "unit": "吨", "amount_2022": Decimal("25"), "amount_2023": Decimal("28"), "amount_2024": Decimal("32"), "disposal_method": "危废处置"},
            {"category": "生活垃圾", "name": "生活垃圾", "unit": "吨", "amount_2022": Decimal("45"), "amount_2023": Decimal("50"), "amount_2024": Decimal("55"), "disposal_method": "市政处理"},
        ]
        
        for data in solid_waste_data:
            data["enterprise_id"] = self.enterprise_id
            await PCBSolidWasteRecord.create(**data)
        
        print("固体废物数据创建成功")
    
    async def create_self_monitoring_data(self):
        """创建自行监测数据"""
        print("正在创建自行监测数据...")
        
        # 有组织废气监测
        organized_gas_data = [
            {"monitoring_point": "有机废气排放口", "monitoring_time": "2024-12-01", "non_methane_hydrocarbons": Decimal("35.2")},
            {"monitoring_point": "酸雾废气排放口", "monitoring_time": "2024-12-01", "sulfuric_acid_mist": Decimal("22.5")},
            {"monitoring_point": "粉尘废气排放口", "monitoring_time": "2024-12-01", "phenol": Decimal("15.8")},
        ]
        
        for data in organized_gas_data:
            data["enterprise_id"] = self.enterprise_id
            await PCBOrganizedGasMonitoring.create(**data)
        
        # 废水监测
        wastewater_monitoring_data = [
            {"sampling_date": "2024-12-01", "ph": Decimal("7.2"), "cod": Decimal("45.5"), "total_copper": Decimal("0.3")},
        ]
        
        for data in wastewater_monitoring_data:
            data["enterprise_id"] = self.enterprise_id
            await PCBWastewaterMonitoring.create(**data)
        
        # 噪声监测
        noise_monitoring_data = [
            {"monitoring_time": "2024-12-01", "monitoring_point": "厂界东侧", "daytime_result": Decimal("52.5"), "nighttime_result": Decimal("48.5"), "daytime_standard": Decimal("65"), "nighttime_standard": Decimal("55")},
            {"monitoring_time": "2024-12-01", "monitoring_point": "厂界南侧", "daytime_result": Decimal("48.8"), "nighttime_result": Decimal("45.2"), "daytime_standard": Decimal("65"), "nighttime_standard": Decimal("55")},
            {"monitoring_time": "2024-12-01", "monitoring_point": "厂界西侧", "daytime_result": Decimal("51.2"), "nighttime_result": Decimal("47.8"), "daytime_standard": Decimal("65"), "nighttime_standard": Decimal("55")},
            {"monitoring_time": "2024-12-01", "monitoring_point": "厂界北侧", "daytime_result": Decimal("49.5"), "nighttime_result": Decimal("46.1"), "daytime_standard": Decimal("65"), "nighttime_standard": Decimal("55")},
        ]
        
        for data in noise_monitoring_data:
            data["enterprise_id"] = self.enterprise_id
            await PCBNoiseMonitoring.create(**data)
        
        print("自行监测数据创建成功")
    
    async def create_pre_audit_data(self):
        """创建预审核数据"""
        print("正在创建预审核数据...")
        
        pre_audit_data = {
            "enterprise_id": self.enterprise_id,
            "production_info": {
                "total_output_2022": 28500,
                "total_output_2023": 32500,
                "total_output_2024": 36800,
                "main_products": ["单面板", "双面板", "多层板", "HDI板", "软硬结合板"],
                "production_capacity": 120,
                "employee_count": 580
            },
            "raw_materials": {
                "main_materials": [
                    {"name": "覆铜板", "unit": "kg", "usage_2022": 1250000, "usage_2023": 1420000, "usage_2024": 1580000},
                    {"name": "铜箔", "unit": "kg", "usage_2022": 850000, "usage_2023": 960000, "usage_2024": 1080000},
                    {"name": "玻璃纤维布", "unit": "m²", "usage_2022": 2800000, "usage_2023": 3200000, "usage_2024": 3600000},
                    {"name": "环氧树脂", "unit": "kg", "usage_2022": 180000, "usage_2023": 205000, "usage_2024": 230000}
                ],
                "auxiliary_materials": [
                    {"name": "蚀刻液", "unit": "L", "usage_2022": 45000, "usage_2023": 52000, "usage_2024": 58000},
                    {"name": "电镀液", "unit": "L", "usage_2022": 38000, "usage_2023": 43000, "usage_2024": 48000},
                    {"name": "阻焊油墨", "unit": "kg", "usage_2022": 65000, "usage_2023": 75000, "usage_2024": 85000}
                ]
            },
            "process_equipment": {
                "main_equipment": [
                    {"name": "开料机", "model": "LPKF-2000", "quantity": 3, "purchase_date": "2015-03"},
                    {"name": "钻孔机", "model": "东台精机-6000", "quantity": 8, "purchase_date": "2015-03"},
                    {"name": "沉铜线", "model": "奥宝-3000", "quantity": 2, "purchase_date": "2015-05"},
                    {"name": "电镀线", "model": "奥宝-4000", "quantity": 2, "purchase_date": "2015-05"}
                ]
            },
            "resource_consumption": {
                "electricity": {
                    "total_2022": 11050000,
                    "total_2023": 12440000,
                    "total_2024": 13900000,
                    "unit_consumption": 110.3
                },
                "water": {
                    "total_2022": 123000,
                    "total_2023": 138500,
                    "total_2024": 153000,
                    "unit_consumption": 1.23
                },
                "gas": {
                    "total_2022": 57000,
                    "total_2023": 63500,
                    "total_2024": 70000
                }
            },
            "pollution_control": {
                "wastewater": {
                    "treatment_capacity": 100000,
                    "discharge_standard": "达标排放",
                    "reuse_rate": 0
                },
                "waste_gas": {
                    "treatment_facilities": ["活性炭吸附", "催化燃烧", "碱液喷淋", "布袋除尘"],
                    "discharge_standard": "达标排放"
                }
            },
            "solid_waste": {
                "hazardous_waste": {
                    "annual_generation": 70,
                    "disposal_method": "委托有资质单位处置",
                    "storage_facility": "标准化危废贮存库"
                },
                "general_waste": {
                    "annual_generation": 360,
                    "disposal_method": "回收利用+市政处理"
                }
            },
            "self_monitoring": {
                "monitoring_frequency": "定期监测",
                "monitoring_items": ["废水", "废气", "噪声"],
                "compliance_rate": 100
            },
            "status": "draft"
        }
        
        await PCBPreAuditData.create(**pre_audit_data)
        print("预审核数据创建成功")
    
    async def create_audit_report(self):
        """创建审核报告"""
        print("正在创建审核报告...")
        
        audit_report_data = {
            "enterprise_id": self.enterprise_id,
            "total_score": Decimal("0.00"),
            "overall_level": "待评估",
            "improvement_items": 0,
            "limiting_indicators_count": 0,
            "non_compliant_limiting_count": 0,
            "summary": {
                "enterprise_name": "深圳市鑫满达电子科技有限公司",
                "audit_date": "2024-12-01",
                "auditor": "待分配",
                "status": "待审核"
            },
            "recommendations": "待审核完成后生成",
            "status": "draft",
            "auditor_name": "待分配",
            "audit_date": date(2024, 12, 1)
        }
        
        await PCBAuditReport.create(**audit_report_data)
        print("审核报告创建成功")
    
    async def run(self):
        """执行完整的数据录入流程"""
        try:
            print("开始录入深圳市鑫满达公司数据...")
            
            await self.init_database()
            
            # 1. 创建企业基本信息
            await self.create_enterprise()
            
            # 2. 创建生产情况数据
            await self.create_production_data()
            
            # 3. 创建资源能源消耗数据
            await self.create_resource_consumption_data()
            
            # 4. 创建污染防治数据
            await self.create_pollution_control_data()
            
            # 5. 创建固体废物数据
            await self.create_solid_waste_data()
            
            # 6. 创建自行监测数据
            await self.create_self_monitoring_data()
            
            # 7. 创建预审核数据
            await self.create_pre_audit_data()
            
            # 8. 创建审核报告
            await self.create_audit_report()
            
            print(f"\n深圳市鑫满达公司数据录入完成！")
            print(f"企业ID: {self.enterprise_id}")
            print(f"数据包括:")
            print(f"   - 企业基本信息")
            print(f"   - 生产情况数据 (产品产量、合格率、产值)")
            print(f"   - 资源能源消耗数据 (用电、用水、天然气)")
            print(f"   - 污染防治数据 (废水、废气)")
            print(f"   - 固体废物数据")
            print(f"   - 自行监测数据")
            print(f"   - 预审核数据")
            print(f"   - 审核报告")
            
        except Exception as e:
            print(f"数据录入失败: {str(e)}")
            raise
        finally:
            try:
                await self.close_database()
            except:
                pass


async def main():
    """主函数"""
    inserter = XinmandaDataInserter()
    await inserter.run()


if __name__ == "__main__":
    asyncio.run(main())
