#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试Word报告生成功能
"""

import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.utils.word_report_generator import PCBWordReportGenerator


async def test_word_report():
    """测试Word报告生成"""
    
    # 模拟数据
    enterprise_data = {
        "name": "深圳市鑫满达电子科技有限公司",
        "unified_social_credit_code": "91440300MA5F8K9X2L",
        "region": "深圳市",
        "district": "宝安区",
        "address": "深圳市宝安区西乡街道固戍社区固戍一路88号鑫满达科技园",
        "legal_representative": "陈志强",
        "contact_person": "李工程师",
        "contact_phone": "0755-2798-8888",
        "capital": "5000",
        "capacity": "120",
        "audit_status": "已完成"
    }
    
    planning_data = {
        "leadership_team": [
            {"name": "陈志强", "position": "总经理", "department": "总经理办公室", 
             "role": "组长", "responsibilities": "负责清洁生产审核工作的总体协调和决策", 
             "phone": "0755-27988888"}
        ],
        "work_team": [
            {"name": "李技术", "position": "工程师", "department": "技术部",
             "role": "组长", "responsibilities": "负责清洁生产方案的技术论证和实施",
             "phone": "0755-27988893"}
        ],
        "work_plans": [
            {"stage_order": 1, "stage": "审核准备", "work_content": "成立审核小组",
             "planned_start_date": "2024-01-01", "planned_end_date": "2024-01-31",
             "responsible_department": "总经理办公室"}
        ],
        "training_records": [
            {"title": "清洁生产基础知识培训", "date": "2024-01-15",
             "duration": 120, "participants": 50, "instructor": "李工程师", "location": "会议室"}
        ]
    }
    
    preaudit_data = {
        "production": {
            "productOutput": [
                {"type": "刚性", "main_product": "双面板", "layers": 2, "unit": "m²",
                 "year": "2024", "output": 589000.0}
            ]
        },
        "resourceConsumption": {
            "electricity": [
                {"project": "生产车间用电", "unit": "kWh",
                 "amount_2022": 8500000, "amount_2023": 9600000, "amount_2024": 10800000}
            ],
            "water": [
                {"project": "生产用水", "unit": "m³",
                 "amount_2022": 85000, "amount_2023": 95000, "amount_2024": 105000}
            ],
            "gas": []
        },
        "processEquipment": {"equipment": []},
        "pollutionControl": {"wastewater": [], "wasteGas": []},
        "solidWaste": {"waste": []},
        "selfMonitoring": {"organizedGas": [], "wastewater": [], "noise": []}
    }
    
    audit_data = {
        "indicators": [],
        "summary": {
            "total_score": 85.5,
            "overall_level": "II级",
            "improvement_items": 15,
            "limiting_indicators": 0
        }
    }
    
    # 生成报告
    generator = PCBWordReportGenerator()
    filepath = generator.generate_report(
        enterprise_data=enterprise_data,
        planning_data=planning_data,
        preaudit_data=preaudit_data,
        audit_data=audit_data
    )
    
    print(f"Word report generated: {filepath}")
    
    # 检查文件是否存在
    if os.path.exists(filepath):
        print(f"File exists! Size: {os.path.getsize(filepath)} bytes")
        return True
    else:
        print("File not found!")
        return False


if __name__ == "__main__":
    result = asyncio.run(test_word_report())
    sys.exit(0 if result else 1)

