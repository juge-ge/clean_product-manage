import asyncio
from app.models.pcb_planning import PCBLeadershipTeam, PCBWorkTeam, PCBWorkPlan, PCBTrainingRecord
from tortoise import Tortoise

async def test_models():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    
    # 检查表是否存在
    tables = await Tortoise.get_connection('default').execute_query('SELECT name FROM sqlite_master WHERE type="table" AND name LIKE "pcb_%"')
    print('PCB相关表:', [row[0] for row in tables[1]])
    
    # 检查企业ID为7的数据
    leadership_count = await PCBLeadershipTeam.filter(enterprise_id=7).count()
    work_team_count = await PCBWorkTeam.filter(enterprise_id=7).count()
    work_plan_count = await PCBWorkPlan.filter(enterprise_id=7).count()
    training_count = await PCBTrainingRecord.filter(enterprise_id=7).count()
    
    print(f'企业ID=7的数据统计:')
    print(f'  领导小组: {leadership_count}')
    print(f'  工作小组: {work_team_count}')
    print(f'  工作计划: {work_plan_count}')
    print(f'  培训记录: {training_count}')
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(test_models())
