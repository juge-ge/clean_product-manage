#!/usr/bin/env python3
"""
测试深圳市鑫满达电子科技有限公司的报告生成
"""
import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings import settings
from app.utils.report_generator import PCBReportGenerator

async def test_xinmanda_report():
    """测试深圳市鑫满达电子科技有限公司的报告生成"""
    try:
        # 初始化Tortoise ORM
        await Tortoise.init(config=settings.TORTOISE_ORM)
        
        # 创建报告生成器
        generator = PCBReportGenerator()
        
        # 为企业ID 11（深圳市鑫满达电子科技有限公司）生成报告
        enterprise_id = 11
        print(f"正在为企业ID {enterprise_id} 生成报告...")
        
        report_path = await generator.generate_report(enterprise_id)
        
        print(f"报告生成成功！")
        print(f"报告路径: {report_path}")
        
        # 检查文件是否存在
        if os.path.exists(report_path):
            file_size = os.path.getsize(report_path)
            print(f"文件大小: {file_size} 字节")
            print(f"文件名: {os.path.basename(report_path)}")
        else:
            print("错误: 报告文件未找到")
            
    except Exception as e:
        print(f"报告生成失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(test_xinmanda_report())
