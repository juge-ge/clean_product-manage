import asyncio
from tortoise import Tortoise
from app.utils.report_generator import report_generator

async def test_report_generation():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['app.models']}
    )
    
    enterprise_id = 11  # 深圳市鑫满达公司
    
    try:
        print('=== 测试报告生成功能 ===')
        print(f'为企业ID {enterprise_id} 生成报告...')
        
        # 生成报告
        report_path = await report_generator.generate_report(enterprise_id)
        
        print(f'报告生成成功！')
        print(f'报告路径: {report_path}')
        
        # 检查文件是否存在
        import os
        if os.path.exists(report_path):
            file_size = os.path.getsize(report_path)
            print(f'文件大小: {file_size} 字节')
        else:
            print('警告: 报告文件不存在')
        
    except Exception as e:
        print(f'报告生成失败: {e}')
        import traceback
        traceback.print_exc()
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(test_report_generation())
