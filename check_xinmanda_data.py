import asyncio
from tortoise import Tortoise
from app.models.pcb import PCBEnterprise, PCBPreAuditData
from app.models.pcb_planning import PCBLeadershipTeam, PCBWorkTeam, PCBWorkPlan, PCBTrainingRecord

async def check_xinmanda_data():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    
    # 查找深圳市鑫满达公司
    xinmanda = await PCBEnterprise.filter(name__contains="鑫满达").first()
    if not xinmanda:
        print("未找到深圳市鑫满达公司")
        return
    
    print(f'=== 深圳市鑫满达公司信息 (ID: {xinmanda.id}) ===')
    print(f'企业名称: {xinmanda.name}')
    print(f'统一社会信用代码: {xinmanda.unified_social_credit_code}')
    print(f'地区: {xinmanda.region} {xinmanda.district}')
    print(f'地址: {xinmanda.address}')
    print(f'法人代表: {xinmanda.legal_representative}')
    print(f'联系人: {xinmanda.contact_person}')
    print(f'联系电话: {xinmanda.contact_phone}')
    print(f'年产能: {xinmanda.capacity}万m2')
    print(f'审核状态: {xinmanda.audit_status}')
    
    enterprise_id = xinmanda.id
    
    print(f'\n=== 筹划与组织数据 (企业ID: {enterprise_id}) ===')
    
    # 领导小组
    leadership = await PCBLeadershipTeam.filter(enterprise_id=enterprise_id)
    print(f'领导小组成员数: {len(leadership)}')
    for member in leadership:
        print(f'  - {member.name} ({member.role})')
    
    # 工作小组
    work_team = await PCBWorkTeam.filter(enterprise_id=enterprise_id)
    print(f'工作小组成员数: {len(work_team)}')
    for member in work_team:
        print(f'  - {member.name} ({member.role})')
    
    # 工作计划
    work_plans = await PCBWorkPlan.filter(enterprise_id=enterprise_id)
    print(f'工作计划数: {len(work_plans)}')
    for plan in work_plans:
        print(f'  - 第{plan.stage_order}阶段: {plan.stage}')
    
    # 培训记录
    training = await PCBTrainingRecord.filter(enterprise_id=enterprise_id)
    print(f'培训记录数: {len(training)}')
    for record in training:
        print(f'  - {record.title} ({record.date})')
    
    # 预审核数据
    pre_audit = await PCBPreAuditData.filter(enterprise_id=enterprise_id)
    print(f'预审核数据数: {len(pre_audit)}')
    if pre_audit:
        data = pre_audit[0]
        print(f'预审核数据状态: {data.status}')
        print(f'生产信息: {data.production_info is not None}')
        print(f'原辅材料: {data.raw_materials is not None}')
        print(f'工艺装备: {data.process_equipment is not None}')
        print(f'资源消耗: {data.resource_consumption is not None}')
        print(f'污染防治: {data.pollution_control is not None}')
        print(f'固体废物: {data.solid_waste is not None}')
        print(f'自行监测: {data.self_monitoring is not None}')
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(check_xinmanda_data())
