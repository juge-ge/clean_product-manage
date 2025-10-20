#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
补充深圳市鑫满达公司(ID:11)的完整数据
包括：筹划与组织、预审核所有模块的数据
"""

import asyncio
import sys
import os
from decimal import Decimal
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings import settings
from app.models.pcb import PCBEnterprise
from app.models.pcb_planning import PCBLeadershipTeam, PCBWorkTeam, PCBWorkPlan, PCBTrainingRecord
from app.models.resource_consumption import (
    PCBElectricityConsumptionRecord, 
    PCBWaterConsumptionRecord,
    PCBGasConsumptionRecord
)
from app.models.pollution_control import (
    PCBWastewaterAnalysis,
    PCBWasteGasAnalysis
)
from app.models.solid_waste import PCBSolidWasteRecord
from app.models.self_monitoring import (
    PCBOrganizedGasMonitoring,
    PCBWastewaterMonitoring,
    PCBNoiseMonitoring
)
from app.models.process_equipment import PCBEquipmentRecord
from app.models.raw_material import EnterpriseRawMaterialUsage


class XinmandaDataSupplement:
    """鑫满达公司数据补充器"""
    
    def __init__(self):
        self.enterprise_id = 11
    
    async def init_db(self):
        """初始化数据库"""
        await Tortoise.init(config=settings.TORTOISE_ORM)
        print("数据库连接成功")
    
    async def close_db(self):
        """关闭数据库"""
        await Tortoise.close_connections()
        print("数据库连接已关闭")
    
    async def add_leadership_team(self):
        """补充领导小组数据"""
        print("\n[1/10] 补充领导小组数据...")
        
        members = [
            {
                "name": "陈志强",
                "position": "总经理",
                "department": "总经理办公室",
                "role": "组长",
                "responsibilities": "负责清洁生产审核工作的总体协调和决策",
                "phone": "0755-27988888"
            },
            {
                "name": "李工程师",
                "position": "生产副总经理",
                "department": "生产部",
                "role": "副组长",
                "responsibilities": "负责生产工艺改进和技术指导",
                "phone": "0755-27988889"
            },
            {
                "name": "王环保",
                "position": "环保主管",
                "department": "环保部",
                "role": "成员",
                "responsibilities": "负责环保设施运行和污染物监测",
                "phone": "0755-27988890"
            },
            {
                "name": "张质量",
                "position": "质量经理",
                "department": "质量部",
                "role": "成员",
                "responsibilities": "负责产品质量控制和质量体系管理",
                "phone": "0755-27988891"
            },
            {
                "name": "赵财务",
                "position": "财务经理",
                "department": "财务部",
                "role": "成员",
                "responsibilities": "负责清洁生产投资预算和效益分析",
                "phone": "0755-27988892"
            }
        ]
        
        for member in members:
            await PCBLeadershipTeam.create(
                enterprise_id=self.enterprise_id,
                **member
            )
        
        print(f"  已添加 {len(members)} 条领导小组记录")
    
    async def add_work_team(self):
        """补充工作小组数据"""
        print("\n[2/10] 补充工作小组数据...")
        
        members = [
            {
                "name": "李技术",
                "position": "工程师",
                "department": "技术部",
                "role": "组长",
                "responsibilities": "负责清洁生产方案的技术论证和实施",
                "phone": "0755-27988893"
            },
            {
                "name": "周生产",
                "position": "生产主管",
                "department": "生产车间",
                "role": "副组长",
                "responsibilities": "负责生产现场的清洁生产措施落实",
                "phone": "0755-27988894"
            },
            {
                "name": "吴设备",
                "position": "设备工程师",
                "department": "设备部",
                "role": "成员",
                "responsibilities": "负责设备改造和维护",
                "phone": "0755-27988895"
            },
            {
                "name": "郑环境",
                "position": "环境工程师",
                "department": "环保部",
                "role": "成员",
                "responsibilities": "负责环境监测和污染治理",
                "phone": "0755-27988896"
            },
            {
                "name": "孙能源",
                "position": "能源管理员",
                "department": "动力车间",
                "role": "成员",
                "responsibilities": "负责能源消耗统计和节能措施",
                "phone": "0755-27988897"
            },
            {
                "name": "钱物料",
                "position": "物料管理员",
                "department": "仓储部",
                "role": "成员",
                "responsibilities": "负责原辅材料管理和统计",
                "phone": "0755-27988898"
            }
        ]
        
        for member in members:
            await PCBWorkTeam.create(
                enterprise_id=self.enterprise_id,
                **member
            )
        
        print(f"  已添加 {len(members)} 条工作小组记录")
    
    async def add_work_plans(self):
        """补充工作计划数据"""
        print("\n[3/10] 补充工作计划数据...")
        
        base_date = datetime(2024, 1, 1)
        
        plans = [
            {
                "stage_order": 1,
                "stage": "审核准备",
                "work_content": "成立清洁生产审核领导小组和工作小组，制定审核工作计划",
                "planned_start_date": base_date,
                "planned_end_date": base_date + timedelta(days=30),
                "responsible_department": "总经理办公室",
                "actual_start_date": base_date,
                "actual_end_date": base_date + timedelta(days=28)
            },
            {
                "stage_order": 2,
                "stage": "预审核",
                "work_content": "收集企业生产、能源、环保等基础数据，进行初步分析",
                "planned_start_date": base_date + timedelta(days=31),
                "planned_end_date": base_date + timedelta(days=60),
                "responsible_department": "技术部",
                "actual_start_date": base_date + timedelta(days=31),
                "actual_end_date": base_date + timedelta(days=58)
            },
            {
                "stage_order": 3,
                "stage": "审核",
                "work_content": "对64项指标进行逐一审核评估，确定等级",
                "planned_start_date": base_date + timedelta(days=61),
                "planned_end_date": base_date + timedelta(days=90),
                "responsible_department": "技术部",
                "actual_start_date": base_date + timedelta(days=61),
                "actual_end_date": None
            },
            {
                "stage_order": 4,
                "stage": "方案制定",
                "work_content": "针对不达标指标制定清洁生产改进方案",
                "planned_start_date": base_date + timedelta(days=91),
                "planned_end_date": base_date + timedelta(days=120),
                "responsible_department": "技术部",
                "actual_start_date": None,
                "actual_end_date": None
            },
            {
                "stage_order": 5,
                "stage": "方案筛选",
                "work_content": "对各项方案进行技术经济可行性分析和筛选",
                "planned_start_date": base_date + timedelta(days=121),
                "planned_end_date": base_date + timedelta(days=135),
                "responsible_department": "技术部、财务部",
                "actual_start_date": None,
                "actual_end_date": None
            },
            {
                "stage_order": 6,
                "stage": "方案实施",
                "work_content": "实施选定的清洁生产改进方案",
                "planned_start_date": base_date + timedelta(days=136),
                "planned_end_date": base_date + timedelta(days=270),
                "responsible_department": "生产部、设备部",
                "actual_start_date": None,
                "actual_end_date": None
            },
            {
                "stage_order": 7,
                "stage": "效果评估",
                "work_content": "评估清洁生产方案的实施效果",
                "planned_start_date": base_date + timedelta(days=271),
                "planned_end_date": base_date + timedelta(days=300),
                "responsible_department": "技术部、环保部",
                "actual_start_date": None,
                "actual_end_date": None
            },
            {
                "stage_order": 8,
                "stage": "持续改进",
                "work_content": "建立清洁生产长效机制，持续改进",
                "planned_start_date": base_date + timedelta(days=301),
                "planned_end_date": base_date + timedelta(days=365),
                "responsible_department": "全体部门",
                "actual_start_date": None,
                "actual_end_date": None
            },
            {
                "stage_order": 9,
                "stage": "报告编制",
                "work_content": "编制清洁生产审核报告",
                "planned_start_date": base_date + timedelta(days=331),
                "planned_end_date": base_date + timedelta(days=350),
                "responsible_department": "技术部",
                "actual_start_date": None,
                "actual_end_date": None
            },
            {
                "stage_order": 10,
                "stage": "审核验收",
                "work_content": "接受专家组审核验收",
                "planned_start_date": base_date + timedelta(days=351),
                "planned_end_date": base_date + timedelta(days=365),
                "responsible_department": "总经理办公室",
                "actual_start_date": None,
                "actual_end_date": None
            }
        ]
        
        for plan in plans:
            await PCBWorkPlan.create(
                enterprise_id=self.enterprise_id,
                **plan
            )
        
        print(f"  已添加 {len(plans)} 条工作计划记录")
    
    async def add_training_records(self):
        """补充培训记录数据"""
        print("\n[4/10] 补充培训记录数据...")
        
        base_date = datetime(2024, 1, 15)
        
        records = [
            {
                "title": "清洁生产基础知识培训",
                "date": base_date,
                "duration": 120,
                "participants": 50,
                "content": "清洁生产的基本概念、意义和方法介绍",
                "instructor": "李工程师",
                "location": "公司会议室"
            },
            {
                "title": "PCB行业清洁生产评价指标体系培训",
                "date": base_date + timedelta(days=7),
                "duration": 180,
                "participants": 30,
                "content": "64项评价指标的详细讲解和评分标准",
                "instructor": "外部专家",
                "location": "公司会议室"
            },
            {
                "title": "废水处理系统操作培训",
                "date": base_date + timedelta(days=14),
                "duration": 90,
                "participants": 15,
                "content": "废水处理系统的运行操作和日常维护",
                "instructor": "王环保",
                "location": "污水处理站"
            },
            {
                "title": "危险废物管理培训",
                "date": base_date + timedelta(days=21),
                "duration": 60,
                "participants": 25,
                "content": "危险废物的分类、收集、贮存和转移要求",
                "instructor": "郑环境",
                "location": "危废暂存间"
            }
        ]
        
        for record in records:
            await PCBTrainingRecord.create(
                enterprise_id=self.enterprise_id,
                **record
            )
        
        print(f"  已添加 {len(records)} 条培训记录")
    
    async def add_electricity_records(self):
        """补充用电记录数据"""
        print("\n[5/10] 补充用电消耗数据...")
        
        years = [2022, 2023, 2024]
        electricity_data = {
            2022: [
                {"type": "生产车间用电", "amount": Decimal("8500000"), "unit": "kWh"},
                {"type": "辅助生产用电", "amount": Decimal("1200000"), "unit": "kWh"},
                {"type": "办公用电", "amount": Decimal("180000"), "unit": "kWh"},
                {"type": "生活用电", "amount": Decimal("150000"), "unit": "kWh"},
                {"type": "照明用电", "amount": Decimal("200000"), "unit": "kWh"},
                {"type": "空调用电", "amount": Decimal("800000"), "unit": "kWh"},
            ],
            2023: [
                {"type": "生产车间用电", "amount": Decimal("9600000"), "unit": "kWh"},
                {"type": "辅助生产用电", "amount": Decimal("1350000"), "unit": "kWh"},
                {"type": "办公用电", "amount": Decimal("200000"), "unit": "kWh"},
                {"type": "生活用电", "amount": Decimal("170000"), "unit": "kWh"},
                {"type": "照明用电", "amount": Decimal("220000"), "unit": "kWh"},
                {"type": "空调用电", "amount": Decimal("900000"), "unit": "kWh"},
            ],
            2024: [
                {"type": "生产车间用电", "amount": Decimal("10800000"), "unit": "kWh"},
                {"type": "辅助生产用电", "amount": Decimal("1500000"), "unit": "kWh"},
                {"type": "办公用电", "amount": Decimal("220000"), "unit": "kWh"},
                {"type": "生活用电", "amount": Decimal("190000"), "unit": "kWh"},
                {"type": "照明用电", "amount": Decimal("240000"), "unit": "kWh"},
                {"type": "空调用电", "amount": Decimal("1000000"), "unit": "kWh"},
            ]
        }
        
        count = 0
        for year in years:
            for record in electricity_data[year]:
                await PCBElectricityConsumptionRecord.create(
                    enterprise_id=self.enterprise_id,
                    year=str(year),
                    **record
                )
                count += 1
        
        print(f"  已添加 {count} 条用电记录")
    
    async def add_water_records(self):
        """补充用水记录数据"""
        print("\n[6/10] 补充用水消耗数据...")
        
        years = [2022, 2023, 2024]
        water_data = {
            2022: [
                {"type": "生产用水", "amount": Decimal("85000"), "unit": "m³", "source": "市政供水"},
                {"type": "生活用水", "amount": Decimal("12000"), "unit": "m³", "source": "市政供水"},
                {"type": "办公用水", "amount": Decimal("3000"), "unit": "m³", "source": "市政供水"},
                {"type": "冷却用水", "amount": Decimal("15000"), "unit": "m³", "source": "市政供水"},
                {"type": "清洗用水", "amount": Decimal("8000"), "unit": "m³", "source": "市政供水"},
            ],
            2023: [
                {"type": "生产用水", "amount": Decimal("95000"), "unit": "m³", "source": "市政供水"},
                {"type": "生活用水", "amount": Decimal("13500"), "unit": "m³", "source": "市政供水"},
                {"type": "办公用水", "amount": Decimal("3500"), "unit": "m³", "source": "市政供水"},
                {"type": "冷却用水", "amount": Decimal("17000"), "unit": "m³", "source": "市政供水"},
                {"type": "清洗用水", "amount": Decimal("9000"), "unit": "m³", "source": "市政供水"},
            ],
            2024: [
                {"type": "生产用水", "amount": Decimal("105000"), "unit": "m³", "source": "市政供水"},
                {"type": "生活用水", "amount": Decimal("15000"), "unit": "m³", "source": "市政供水"},
                {"type": "办公用水", "amount": Decimal("4000"), "unit": "m³", "source": "市政供水"},
                {"type": "冷却用水", "amount": Decimal("19000"), "unit": "m³", "source": "市政供水"},
                {"type": "清洗用水", "amount": Decimal("10000"), "unit": "m³", "source": "市政供水"},
            ]
        }
        
        count = 0
        for year in years:
            for record in water_data[year]:
                await PCBWaterConsumptionRecord.create(
                    enterprise_id=self.enterprise_id,
                    year=str(year),
                    **record
                )
                count += 1
        
        print(f"  已添加 {count} 条用水记录")
    
    async def add_gas_records(self):
        """补充天然气记录数据"""
        print("\n[7/10] 补充天然气消耗数据...")
        
        years = [2022, 2023, 2024]
        gas_data = {
            2022: [
                {"type": "锅炉天然气", "amount": Decimal("45000"), "unit": "m³"},
                {"type": "工业煤气", "amount": Decimal("12000"), "unit": "m³"},
            ],
            2023: [
                {"type": "锅炉天然气", "amount": Decimal("50000"), "unit": "m³"},
                {"type": "工业煤气", "amount": Decimal("13500"), "unit": "m³"},
            ],
            2024: [
                {"type": "锅炉天然气", "amount": Decimal("55000"), "unit": "m³"},
                {"type": "工业煤气", "amount": Decimal("15000"), "unit": "m³"},
            ]
        }
        
        count = 0
        for year in years:
            for record in gas_data[year]:
                await PCBGasConsumptionRecord.create(
                    enterprise_id=self.enterprise_id,
                    year=str(year),
                    **record
                )
                count += 1
        
        print(f"  已添加 {count} 条天然气记录")
    
    async def add_wastewater_analysis(self):
        """补充废水分析数据"""
        print("\n[8/10] 补充废水处理数据...")
        
        analysis_records = [
            {
                "type": "含铜废水",
                "generation": Decimal("45000"),
                "treatment_method": "化学沉淀+膜过滤",
                "discharge_standard": "总铜<0.5mg/L",
                "actual_concentration": Decimal("0.3"),
                "is_compliant": True
            },
            {
                "type": "有机废水",
                "generation": Decimal("28000"),
                "treatment_method": "生化处理+深度处理",
                "discharge_standard": "COD<50mg/L",
                "actual_concentration": Decimal("35"),
                "is_compliant": True
            },
            {
                "type": "酸碱废水",
                "generation": Decimal("15000"),
                "treatment_method": "中和处理",
                "discharge_standard": "pH 6-9",
                "actual_concentration": Decimal("7.5"),
                "is_compliant": True
            },
            {
                "type": "清洗废水",
                "generation": Decimal("12000"),
                "treatment_method": "混凝沉淀",
                "discharge_standard": "SS<30mg/L",
                "actual_concentration": Decimal("20"),
                "is_compliant": True
            }
        ]
        
        for record in analysis_records:
            await PCBWastewaterAnalysis.create(
                enterprise_id=self.enterprise_id,
                year="2024",
                **record
            )
        
        print(f"  已添加 {len(analysis_records)} 条废水分析记录")
    
    async def add_solid_waste_records(self):
        """补充固体废物记录数据"""
        print("\n[9/10] 补充固体废物数据...")
        
        years = [2022, 2023, 2024]
        waste_data = {
            2022: [
                {"type": "一般固废", "name": "废铜屑", "category": "金属废料", "amount": Decimal("85"), "unit": "t", "disposal_method": "回收利用"},
                {"type": "一般固废", "name": "废边角料", "category": "废基材", "amount": Decimal("120"), "unit": "t", "disposal_method": "回收利用"},
                {"type": "危险废物", "name": "废化学试剂", "category": "HW06", "amount": Decimal("15"), "unit": "t", "disposal_method": "委托处置"},
                {"type": "危险废物", "name": "废活性炭", "category": "HW49", "amount": Decimal("8"), "unit": "t", "disposal_method": "委托处置"},
                {"type": "危险废物", "name": "污泥", "category": "HW17", "amount": Decimal("25"), "unit": "t", "disposal_method": "委托处置"},
                {"type": "生活垃圾", "name": "生活垃圾", "category": "一般垃圾", "amount": Decimal("45"), "unit": "t", "disposal_method": "市政处理"},
            ],
            2023: [
                {"type": "一般固废", "name": "废铜屑", "category": "金属废料", "amount": Decimal("95"), "unit": "t", "disposal_method": "回收利用"},
                {"type": "一般固废", "name": "废边角料", "category": "废基材", "amount": Decimal("135"), "unit": "t", "disposal_method": "回收利用"},
                {"type": "危险废物", "name": "废化学试剂", "category": "HW06", "amount": Decimal("18"), "unit": "t", "disposal_method": "委托处置"},
                {"type": "危险废物", "name": "废活性炭", "category": "HW49", "amount": Decimal("10"), "unit": "t", "disposal_method": "委托处置"},
                {"type": "危险废物", "name": "污泥", "category": "HW17", "amount": Decimal("28"), "unit": "t", "disposal_method": "委托处置"},
                {"type": "生活垃圾", "name": "生活垃圾", "category": "一般垃圾", "amount": Decimal("50"), "unit": "t", "disposal_method": "市政处理"},
            ],
            2024: [
                {"type": "一般固废", "name": "废铜屑", "category": "金属废料", "amount": Decimal("105"), "unit": "t", "disposal_method": "回收利用"},
                {"type": "一般固废", "name": "废边角料", "category": "废基材", "amount": Decimal("150"), "unit": "t", "disposal_method": "回收利用"},
                {"type": "危险废物", "name": "废化学试剂", "category": "HW06", "amount": Decimal("20"), "unit": "t", "disposal_method": "委托处置"},
                {"type": "危险废物", "name": "废活性炭", "category": "HW49", "amount": Decimal("12"), "unit": "t", "disposal_method": "委托处置"},
                {"type": "危险废物", "name": "污泥", "category": "HW17", "amount": Decimal("32"), "unit": "t", "disposal_method": "委托处置"},
                {"type": "生活垃圾", "name": "生活垃圾", "category": "一般垃圾", "amount": Decimal("55"), "unit": "t", "disposal_method": "市政处理"},
            ]
        }
        
        count = 0
        for year in years:
            for record in waste_data[year]:
                await PCBSolidWasteRecord.create(
                    enterprise_id=self.enterprise_id,
                    year=str(year),
                    **record
                )
                count += 1
        
        print(f"  已添加 {count} 条固体废物记录")
    
    async def add_monitoring_records(self):
        """补充自行监测数据"""
        print("\n[10/10] 补充自行监测数据...")
        
        # 废水监测
        await PCBWastewaterMonitoring.create(
            enterprise_id=self.enterprise_id,
            monitoring_point="废水总排口",
            monitoring_item="pH值",
            monitoring_frequency="每日",
            monitoring_method="玻璃电极法",
            standard_limit="6-9",
            actual_value="7.2",
            is_compliant=True,
            monitoring_date=datetime.now()
        )
        
        await PCBWastewaterMonitoring.create(
            enterprise_id=self.enterprise_id,
            monitoring_point="废水总排口",
            monitoring_item="化学需氧量(COD)",
            monitoring_frequency="每周",
            monitoring_method="重铬酸钾法",
            standard_limit="50mg/L",
            actual_value="35mg/L",
            is_compliant=True,
            monitoring_date=datetime.now()
        )
        
        await PCBWastewaterMonitoring.create(
            enterprise_id=self.enterprise_id,
            monitoring_point="废水总排口",
            monitoring_item="总铜",
            monitoring_frequency="每周",
            monitoring_method="原子吸收分光光度法",
            standard_limit="0.5mg/L",
            actual_value="0.3mg/L",
            is_compliant=True,
            monitoring_date=datetime.now()
        )
        
        # 废气监测
        await PCBOrganizedGasMonitoring.create(
            enterprise_id=self.enterprise_id,
            monitoring_point="有机废气排口",
            monitoring_item="非甲烷总烃",
            monitoring_frequency="每季度",
            monitoring_method="气相色谱法",
            standard_limit="50mg/m³",
            actual_value="35mg/m³",
            is_compliant=True,
            monitoring_date=datetime.now()
        )
        
        # 噪声监测
        for direction in ["东", "南", "西", "北"]:
            await PCBNoiseMonitoring.create(
                enterprise_id=self.enterprise_id,
                monitoring_point=f"厂界{direction}侧",
                monitoring_frequency="每季度",
                monitoring_method="声级计法",
                day_standard_limit="65dB(A)",
                day_actual_value="60dB(A)",
                night_standard_limit="55dB(A)",
                night_actual_value="50dB(A)",
                is_compliant=True,
                monitoring_date=datetime.now()
            )
        
        print(f"  已添加监测记录")
    
    async def run(self):
        """执行所有数据补充"""
        try:
            await self.init_db()
            
            print("\n" + "=" * 80)
            print("开始补充深圳市鑫满达公司(ID:11)完整数据")
            print("=" * 80)
            
            # 执行所有补充操作
            await self.add_leadership_team()
            await self.add_work_team()
            await self.add_work_plans()
            await self.add_training_records()
            await self.add_electricity_records()
            await self.add_water_records()
            await self.add_gas_records()
            await self.add_wastewater_analysis()
            await self.add_solid_waste_records()
            await self.add_monitoring_records()
            
            print("\n" + "=" * 80)
            print("数据补充完成！")
            print("=" * 80)
            
        except Exception as e:
            print(f"\n错误: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            await self.close_db()


if __name__ == "__main__":
    补充器 = XinmandaDataSupplement()
    asyncio.run(补充器.run())

