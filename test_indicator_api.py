"""
测试指标API的简单脚本
"""
import asyncio
from tortoise import Tortoise
from app.controllers.pcb import pcb_indicator_controller
from app.settings import settings

async def test_indicator_controller():
    await Tortoise.init(config=settings.TORTOISE_ORM)
    
    try:
        print("测试获取所有指标...")
        indicators = await pcb_indicator_controller.get_all()
        print(f"成功获取 {len(indicators)} 个指标")
        
        if indicators:
            print("第一个指标信息:")
            indicator = indicators[0]
            result = await indicator.to_dict()
            print(f"  ID: {result.get('id')}")
            print(f"  indicator_id: {result.get('indicator_id')}")
            print(f"  name: {result.get('name')}")
            print(f"  category: {result.get('category')}")
            print(f"  indicator_type: {result.get('indicator_type')}")
        
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()
    
    await Tortoise.close_connections()

if __name__ == "__main__":
    asyncio.run(test_indicator_controller())


