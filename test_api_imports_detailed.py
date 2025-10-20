#!/usr/bin/env python3
"""
详细测试API导入
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_imports_detailed():
    """详细测试API导入"""
    print("详细测试API导入:")
    
    # 测试生产数据API导入
    print("\n1. 测试生产数据API导入:")
    try:
        print("  导入控制器...")
        from app.controllers.pcb_production import pcb_production_data_controller
        print("  控制器导入成功")
        
        print("  导入schemas...")
        from app.schemas.pcb_production import PCBProductionDataRequest, PCBProductionDataResponse
        print("  schemas导入成功")
        
        print("  导入API路由...")
        from app.api.v1.pcb_production import router as pcb_production_router
        print("  API路由导入成功")
        
        print("  检查路由...")
        routes = [route.path for route in pcb_production_router.routes]
        print(f"  路由: {routes}")
        
    except Exception as e:
        print(f"  生产数据API导入失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 测试资源能源消耗API导入
    print("\n2. 测试资源能源消耗API导入:")
    try:
        print("  导入控制器...")
        from app.controllers.resource_consumption import resource_consumption_data_controller
        print("  控制器导入成功")
        
        print("  导入schemas...")
        from app.schemas.resource_consumption import PCBResourceConsumptionDataRequest, PCBResourceConsumptionDataResponse
        print("  schemas导入成功")
        
        print("  导入API路由...")
        from app.api.v1.resource_consumption import router as resource_consumption_router
        print("  API路由导入成功")
        
        print("  检查路由...")
        routes = [route.path for route in resource_consumption_router.routes]
        print(f"  路由: {routes}")
        
    except Exception as e:
        print(f"  资源能源消耗API导入失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_imports_detailed()
