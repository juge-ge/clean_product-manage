import asyncio
from tortoise import Tortoise
from app.models.pcb import PCBEnterprise
from app.models.pcb_planning import PCBLeadershipTeam, PCBWorkTeam, PCBWorkPlan, PCBTrainingRecord
from app.models.pcb import PCBPreAuditData

async def check_data():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    
    # 检查企业数据
    enterprises = await PCBEnterprise.all()
    print('=== 企业数据 ===')
    for ent in enterprises:
        print(f'ID: {ent.id}, 名称: {ent.name}, 状态: {ent.audit_status}')
    
    # 检查筹划与组织数据
    if enterprises:
        enterprise_id = enterprises[0].id
        print(f'\n=== 筹划与组织数据 (企业ID: {enterprise_id}) ===')
        
        # 领导小组
        leadership = await PCBLeadershipTeam.filter(enterprise_id=enterprise_id)
        print(f'领导小组成员数: {len(leadership)}')
        
        # 工作小组
        work_team = await PCBWorkTeam.filter(enterprise_id=enterprise_id)
        print(f'工作小组成员数: {len(work_team)}')
        
        # 工作计划
        work_plans = await PCBWorkPlan.filter(enterprise_id=enterprise_id)
        print(f'工作计划数: {len(work_plans)}')
        
        # 培训记录
        training = await PCBTrainingRecord.filter(enterprise_id=enterprise_id)
        print(f'培训记录数: {len(training)}')
        
        # 预审核数据
        pre_audit = await PCBPreAuditData.filter(enterprise_id=enterprise_id)
        print(f'预审核数据数: {len(pre_audit)}')
        if pre_audit:
            print(f'预审核数据状态: {pre_audit[0].status}')
    else:
        print('没有找到企业数据')
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(check_data())