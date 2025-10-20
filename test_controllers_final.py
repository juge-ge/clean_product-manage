#!/usr/bin/env python3
"""
最终测试控制器
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from tortoise import Tortoise
from app.settings.config import settings

async def test_controllers_final():
    """最终测试控制器"""
    try:
        # 初始化数据库连接
        await Tortoise.init(
            config=settings.TORTOISE_ORM,
            modules={'models': ['app.models']}
        )
        
        # 测试生产数据控制器
        print("测试生产数据控制器:")
        try:
            from app.controllers.pcb_production import pcb_production_data_controller
            data = await pcb_production_data_controller.get_all_production_data(7)
            print(f"  生产数据: {data}")
            print(f"  数据类型: {type(data)}")
            
            # 测试JSON序列化
            import json
            json_data = json.dumps(data, ensure_ascii=False, default=str)
            print(f"  JSON序列化成功: {len(json_data)} 字符")
            
        except Exception as e:
            print(f"  生产数据控制器失败: {e}")
            import traceback
            traceback.print_exc()
        
        # 测试资源能源消耗控制器
        print("\n测试资源能源消耗控制器:")
        try:
            from app.controllers.resource_consumption import resource_consumption_data_controller
            data = await resource_consumption_data_controller.get_all_data(7)
            print(f"  资源能源消耗数据: {data}")
            print(f"  数据类型: {type(data)}")
            
            # 测试JSON序列化
            import json
            if hasattr(data, 'dict'):
                json_data = json.dumps(data.dict(), ensure_ascii=False, default=str)
            else:
                json_data = json.dumps(data, ensure_ascii=False, default=str)
            print(f"  JSON序列化成功: {len(json_data)} 字符")
            
        except Exception as e:
            print(f"  资源能源消耗控制器失败: {e}")
            import traceback
            traceback.print_exc()
        
        await Tortoise.close_connections()
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_controllers_final())
