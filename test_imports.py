#!/usr/bin/env python3
"""
测试导入
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试导入"""
    print("测试导入:")
    
    # 测试生产数据相关导入
    try:
        from app.controllers.pcb_production import pcb_production_data_controller
        print("  pcb_production_data_controller: 导入成功")
    except Exception as e:
        print(f"  pcb_production_data_controller: 导入失败 - {e}")
    
    try:
        from app.schemas.pcb_production import PCBProductionDataRequest, PCBProductionDataResponse
        print("  PCB生产数据schemas: 导入成功")
    except Exception as e:
        print(f"  PCB生产数据schemas: 导入失败 - {e}")
    
    # 测试资源能源消耗相关导入
    try:
        from app.controllers.resource_consumption import resource_consumption_data_controller
        print("  resource_consumption_data_controller: 导入成功")
    except Exception as e:
        print(f"  resource_consumption_data_controller: 导入失败 - {e}")
    
    try:
        from app.schemas.resource_consumption import PCBResourceConsumptionDataRequest, PCBResourceConsumptionDataResponse
        print("  资源能源消耗schemas: 导入成功")
    except Exception as e:
        print(f"  资源能源消耗schemas: 导入失败 - {e}")
    
    # 测试API路由导入
    try:
        from app.api.v1.pcb_production import router as pcb_production_router
        print("  pcb_production_router: 导入成功")
    except Exception as e:
        print(f"  pcb_production_router: 导入失败 - {e}")
    
    try:
        from app.api.v1.resource_consumption import router as resource_consumption_router
        print("  resource_consumption_router: 导入成功")
    except Exception as e:
        print(f"  resource_consumption_router: 导入失败 - {e}")

if __name__ == "__main__":
    test_imports()
