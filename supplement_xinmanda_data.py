import asyncio
from tortoise import Tortoise
from app.models.pcb_planning import PCBLeadershipTeam, PCBWorkTeam, PCBWorkPlan, PCBTrainingRecord
from app.models.pcb import PCBPreAuditData
from datetime import datetime

async def supplement_xinmanda_data():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    
    enterprise_id = 11  # 深圳市鑫满达公司ID
    
    print('=== 补充深圳市鑫满达公司筹划与组织数据 ===')
    
    # 1. 补充领导小组数据
    print('1. 补充领导小组数据...')
    leadership_data = [
        {"name": "陈志强", "position": "总经理", "department": "总经理办公室", "role": "组长", "responsibilities": "负责清洁生产审核工作的总体协调和决策", "phone": "0755-2798-8888"},
        {"name": "李工程师", "position": "技术总监", "department": "技术部", "role": "副组长", "responsibilities": "负责清洁生产审核工作的技术指导", "phone": "0755-2798-8889"},
        {"name": "王经理", "position": "生产经理", "department": "生产部", "role": "成员", "responsibilities": "负责生产环节的清洁生产改进", "phone": "0755-2798-8890"},
        {"name": "张主管", "position": "环保主管", "department": "环保部", "role": "成员", "responsibilities": "负责环保设施运行和污染物控制", "phone": "0755-2798-8891"},
        {"name": "刘会计", "position": "财务经理", "department": "财务部", "role": "成员", "responsibilities": "负责清洁生产投资和效益分析", "phone": "0755-2798-8892"}
    ]
    
    # 删除现有数据
    await PCBLeadershipTeam.filter(enterprise_id=enterprise_id).delete()
    
    for data in leadership_data:
        await PCBLeadershipTeam.create(enterprise_id=enterprise_id, **data)
    
    print(f'已添加{len(leadership_data)}名领导小组成员')
    
    # 2. 补充工作小组数据
    print('2. 补充工作小组数据...')
    work_team_data = [
        {"name": "李技术", "position": "工艺工程师", "department": "技术部", "role": "组长", "responsibilities": "负责工艺改进和清洁生产技术应用", "phone": "0755-2798-8893"},
        {"name": "陈设备", "position": "设备工程师", "department": "设备部", "role": "副组长", "responsibilities": "负责设备改造和节能技术应用", "phone": "0755-2798-8894"},
        {"name": "郑环保", "position": "环保工程师", "department": "环保部", "role": "成员", "responsibilities": "负责污染防治设施运行管理", "phone": "0755-2798-8895"},
        {"name": "钱能源", "position": "能源管理师", "department": "生产部", "role": "成员", "responsibilities": "负责能源消耗统计和节能措施实施", "phone": "0755-2798-8896"},
        {"name": "赵质量", "position": "质量工程师", "department": "质量部", "role": "成员", "responsibilities": "负责产品质量控制和清洁生产标准执行", "phone": "0755-2798-8897"}
    ]
    
    # 删除现有数据
    await PCBWorkTeam.filter(enterprise_id=enterprise_id).delete()
    
    for data in work_team_data:
        await PCBWorkTeam.create(enterprise_id=enterprise_id, **data)
    
    print(f'已添加{len(work_team_data)}名工作小组成员')
    
    # 3. 补充工作计划数据
    print('3. 补充工作计划数据...')
    work_plan_data = [
        {"stage_order": 1, "stage": "审核准备", "work_content": "成立清洁生产审核领导小组和工作小组，制定审核计划", "planned_start_date": "2024-01-15", "planned_end_date": "2024-01-31", "responsible_department": "总经理办公室"},
        {"stage_order": 2, "stage": "预审核", "work_content": "收集企业基础资料，进行现状调研和问题识别", "planned_start_date": "2024-02-01", "planned_end_date": "2024-02-28", "responsible_department": "技术部"},
        {"stage_order": 3, "stage": "审核", "work_content": "开展清洁生产审核，评估清洁生产水平", "planned_start_date": "2024-03-01", "planned_end_date": "2024-03-31", "responsible_department": "环保部"},
        {"stage_order": 4, "stage": "方案制定", "work_content": "制定清洁生产改进方案和实施计划", "planned_start_date": "2024-04-01", "planned_end_date": "2024-04-30", "responsible_department": "技术部"},
        {"stage_order": 5, "stage": "方案筛选", "work_content": "对改进方案进行技术经济可行性分析", "planned_start_date": "2024-05-01", "planned_end_date": "2024-05-15", "responsible_department": "财务部"},
        {"stage_order": 6, "stage": "方案实施", "work_content": "实施选定的清洁生产改进方案", "planned_start_date": "2024-05-16", "planned_end_date": "2024-08-31", "responsible_department": "生产部"},
        {"stage_order": 7, "stage": "效果评估", "work_content": "评估清洁生产改进方案的实施效果", "planned_start_date": "2024-09-01", "planned_end_date": "2024-09-30", "responsible_department": "环保部"},
        {"stage_order": 8, "stage": "持续改进", "work_content": "建立清洁生产持续改进机制", "planned_start_date": "2024-10-01", "planned_end_date": "2024-10-31", "responsible_department": "技术部"},
        {"stage_order": 9, "stage": "报告编制", "work_content": "编制清洁生产审核报告", "planned_start_date": "2024-11-01", "planned_end_date": "2024-11-30", "responsible_department": "环保部"},
        {"stage_order": 10, "stage": "验收总结", "work_content": "清洁生产审核验收和总结", "planned_start_date": "2024-12-01", "planned_end_date": "2024-12-31", "responsible_department": "总经理办公室"}
    ]
    
    # 删除现有数据
    await PCBWorkPlan.filter(enterprise_id=enterprise_id).delete()
    
    for data in work_plan_data:
        await PCBWorkPlan.create(enterprise_id=enterprise_id, **data)
    
    print(f'已添加{len(work_plan_data)}个工作计划阶段')
    
    # 4. 补充培训记录数据
    print('4. 补充培训记录数据...')
    training_data = [
        {"title": "清洁生产基础知识培训", "date": "2024-01-20", "duration": 120, "participants": 30, "content": "清洁生产基本概念、原理和方法介绍", "instructor": "李工程师", "location": "公司会议室"},
        {"title": "PCB行业清洁生产指标体系培训", "date": "2024-01-27", "duration": 150, "participants": 25, "content": "PCB行业64项清洁生产指标详解", "instructor": "陈技术", "location": "公司培训室"},
        {"title": "废水处理系统操作培训", "date": "2024-02-03", "duration": 90, "participants": 15, "content": "废水处理设施操作和维护培训", "instructor": "郑环保", "location": "废水处理站"},
        {"title": "危废管理规范培训", "date": "2024-02-10", "duration": 60, "participants": 20, "content": "危险废物分类、贮存、转移管理要求", "instructor": "张主管", "location": "危废贮存库"},
        {"title": "节能技术应用培训", "date": "2024-02-17", "duration": 120, "participants": 18, "content": "节能设备使用和节能措施实施", "instructor": "陈设备", "location": "生产车间"},
        {"title": "清洁生产审核方法培训", "date": "2024-02-24", "duration": 180, "participants": 12, "content": "清洁生产审核程序和方法培训", "instructor": "李工程师", "location": "公司会议室"}
    ]
    
    # 删除现有数据
    await PCBTrainingRecord.filter(enterprise_id=enterprise_id).delete()
    
    for data in training_data:
        await PCBTrainingRecord.create(enterprise_id=enterprise_id, **data)
    
    print(f'已添加{len(training_data)}条培训记录')
    
    # 5. 补充预审核数据
    print('5. 补充预审核数据...')
    pre_audit_data = {
        "production_info": {
            "capacity": 120.0,
            "output": {
                "2022": {
                    "rigidSingle": 15.2,
                    "rigidDouble": 45.8,
                    "rigidMultilayer": 28.6,
                    "rigidHDI": 8.4,
                    "flexibleSingle": 2.1,
                    "flexibleDouble": 0,
                    "flexibleMultilayer": 0,
                    "flexibleHDI": 0
                },
                "2023": {
                    "rigidSingle": 18.5,
                    "rigidDouble": 52.6,
                    "rigidMultilayer": 32.1,
                    "rigidHDI": 12.3,
                    "flexibleSingle": 3.2,
                    "flexibleDouble": 0,
                    "flexibleMultilayer": 0,
                    "flexibleHDI": 0
                },
                "2024": {
                    "rigidSingle": 22.3,
                    "rigidDouble": 58.9,
                    "rigidMultilayer": 35.7,
                    "rigidHDI": 15.2,
                    "flexibleSingle": 4.8,
                    "flexibleDouble": 0,
                    "flexibleMultilayer": 0,
                    "flexibleHDI": 0
                }
            }
        },
        "raw_materials": [
            {"year": 2023, "name": "覆铜板", "unit": "kg", "process": "开料", "amount": 1420000, "state": "固体", "voc": 0},
            {"year": 2023, "name": "铜箔", "unit": "kg", "process": "电镀", "amount": 960000, "state": "固体", "voc": 0},
            {"year": 2023, "name": "玻璃纤维布", "unit": "m2", "process": "压合", "amount": 3200000, "state": "固体", "voc": 0},
            {"year": 2023, "name": "环氧树脂", "unit": "kg", "process": "压合", "amount": 205000, "state": "液体", "voc": 5.2},
            {"year": 2023, "name": "蚀刻液", "unit": "L", "process": "蚀刻", "amount": 52000, "state": "液体", "voc": 0},
            {"year": 2023, "name": "电镀液", "unit": "L", "process": "电镀", "amount": 43000, "state": "液体", "voc": 0},
            {"year": 2023, "name": "阻焊油墨", "unit": "kg", "process": "阻焊", "amount": 75000, "state": "液体", "voc": 8.5},
            {"year": 2023, "name": "助焊剂", "unit": "kg", "process": "焊接", "amount": 14000, "state": "液体", "voc": 12.3}
        ],
        "process_equipment": {
            "rigid": {
                "single": {"line": "单面板生产线", "process": "开料-钻孔-电镀-蚀刻-阻焊-丝印-测试-分板", "equipment": "LPKF-2000开料机,东台精机-6000钻孔机,奥宝-4000电镀线"},
                "double": {"line": "双面板生产线", "process": "开料-钻孔-沉铜-电镀-蚀刻-阻焊-丝印-测试-分板", "equipment": "LPKF-2000开料机,东台精机-6000钻孔机,奥宝-3000沉铜线,奥宝-4000电镀线"},
                "multilayer": {"line": "多层板生产线", "process": "开料-内层制作-压合-钻孔-沉铜-电镀-蚀刻-阻焊-丝印-测试-分板", "equipment": "LPKF-2000开料机,东台精机-6000钻孔机,奥宝-3000沉铜线,奥宝-4000电镀线,奥宝-5000蚀刻线"},
                "hdi": {"line": "HDI板生产线", "process": "开料-内层制作-压合-激光钻孔-沉铜-电镀-蚀刻-阻焊-丝印-测试-分板", "equipment": "LPKF-2000开料机,激光钻孔机,东台精机-6000钻孔机,奥宝-3000沉铜线,奥宝-4000电镀线"}
            },
            "flexible": {
                "single": {"line": "挠性单面板生产线", "process": "开料-钻孔-电镀-蚀刻-阻焊-丝印-测试-分板", "equipment": "挠性板专用开料机,挠性板钻孔机,挠性板电镀线"},
                "double": {"line": "挠性双面板生产线", "process": "开料-钻孔-沉铜-电镀-蚀刻-阻焊-丝印-测试-分板", "equipment": "挠性板专用开料机,挠性板钻孔机,挠性板沉铜线,挠性板电镀线"},
                "multilayer": {"line": "挠性多层板生产线", "process": "开料-内层制作-压合-钻孔-沉铜-电镀-蚀刻-阻焊-丝印-测试-分板", "equipment": "挠性板专用开料机,挠性板钻孔机,挠性板沉铜线,挠性板电镀线"},
                "hdi": {"line": "挠性HDI板生产线", "process": "开料-内层制作-压合-激光钻孔-沉铜-电镀-蚀刻-阻焊-丝印-测试-分板", "equipment": "挠性板专用开料机,挠性板激光钻孔机,挠性板钻孔机,挠性板沉铜线,挠性板电镀线"}
            }
        },
        "resource_consumption": {
            "water": [
                {"year": 2023, "type": "生产用水", "amount": 95000, "source": "市政供水"},
                {"year": 2023, "type": "生活用水", "amount": 13500, "source": "市政供水"},
                {"year": 2023, "type": "办公用水", "amount": 3500, "source": "市政供水"},
                {"year": 2023, "type": "冷却用水", "amount": 17000, "source": "循环水系统"},
                {"year": 2023, "type": "清洗用水", "amount": 9000, "source": "纯水系统"}
            ],
            "electricity": [
                {"year": 2023, "type": "生产车间用电", "amount": 9600000, "source": "电网供电"},
                {"year": 2023, "type": "辅助生产用电", "amount": 1350000, "source": "电网供电"},
                {"year": 2023, "type": "办公用电", "amount": 200000, "source": "电网供电"},
                {"year": 2023, "type": "生活用电", "amount": 170000, "source": "电网供电"},
                {"year": 2023, "type": "照明用电", "amount": 220000, "source": "电网供电"},
                {"year": 2023, "type": "空调用电", "amount": 900000, "source": "电网供电"}
            ],
            "gas": [
                {"year": 2023, "type": "锅炉天然气", "amount": 50000, "source": "天然气公司"},
                {"year": 2023, "type": "工业煤气", "amount": 13500, "source": "工业煤气公司"}
            ]
        },
        "pollution_control": {
            "copperRecovery": [
                {"year": 2023, "amount": 95.2}
            ],
            "waterReuseRate": [
                {"year": 2023, "rate": 65.8}
            ],
            "gasEmission": [
                {"process": "电镀", "category": "有机废气", "method": "活性炭吸附+催化燃烧"},
                {"process": "蚀刻", "category": "酸雾废气", "method": "碱液喷淋"},
                {"process": "钻孔", "category": "粉尘废气", "method": "布袋除尘"}
            ],
            "waterEmission": [
                {"process": "电镀", "category": "含铜废水", "method": "化学沉淀+膜过滤"},
                {"process": "蚀刻", "category": "有机废水", "method": "生化处理+深度处理"},
                {"process": "清洗", "category": "酸碱废水", "method": "中和处理"}
            ]
        },
        "solid_waste": {
            "general": [
                {"year": 2023, "name": "废铜屑", "type": "金属废料", "amount": 95},
                {"year": 2023, "name": "废边角料", "type": "PCB废料", "amount": 135},
                {"year": 2023, "name": "生活垃圾", "type": "生活垃圾", "amount": 50}
            ],
            "hazardous": [
                {"year": 2023, "name": "废化学试剂", "type": "危险废物", "code": "HW06", "amount": 18},
                {"year": 2023, "name": "废活性炭", "type": "危险废物", "code": "HW49", "amount": 10},
                {"year": 2023, "name": "污泥", "type": "危险废物", "code": "HW17", "amount": 28}
            ]
        },
        "self_monitoring": {
            "organizedGas": {
                "item": "非甲烷总烃",
                "concentration": 35.2,
                "point": "排气筒",
                "standard": "50mg/m3",
                "reportFileId": "gas_report_2023.pdf"
            },
            "wastewater": {
                "item": "总铜",
                "concentration": 0.3,
                "point": "总排口",
                "standard": "0.5mg/L",
                "reportFileId": "water_report_2023.pdf"
            },
            "noise": {
                "item": "厂界噪声",
                "level": 58.5,
                "point": "厂界东侧",
                "standard": "65dB(A)",
                "reportFileId": "noise_report_2023.pdf"
            }
        }
    }
    
    # 更新或创建预审核数据
    pre_audit = await PCBPreAuditData.filter(enterprise_id=enterprise_id).first()
    if pre_audit:
        pre_audit.production_info = pre_audit_data["production_info"]
        pre_audit.raw_materials = pre_audit_data["raw_materials"]
        pre_audit.process_equipment = pre_audit_data["process_equipment"]
        pre_audit.resource_consumption = pre_audit_data["resource_consumption"]
        pre_audit.pollution_control = pre_audit_data["pollution_control"]
        pre_audit.solid_waste = pre_audit_data["solid_waste"]
        pre_audit.self_monitoring = pre_audit_data["self_monitoring"]
        pre_audit.status = "draft"
        await pre_audit.save()
        print('已更新预审核数据')
    else:
        await PCBPreAuditData.create(enterprise_id=enterprise_id, **pre_audit_data)
        print('已创建预审核数据')
    
    print('\n=== 数据补充完成 ===')
    print(f'企业ID: {enterprise_id}')
    print(f'领导小组: {len(leadership_data)}人')
    print(f'工作小组: {len(work_team_data)}人')
    print(f'工作计划: {len(work_plan_data)}个阶段')
    print(f'培训记录: {len(training_data)}条')
    print('预审核数据: 已更新')
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(supplement_xinmanda_data())