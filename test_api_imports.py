#!/usr/bin/env python3
"""
测试API导入
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_imports():
    """测试API导入"""
    print("测试API导入:")
    
    # 测试生产数据API导入
    try:
        from app.api.v1.pcb_production import router as pcb_production_router
        print("  pcb_production_router: 导入成功")
        
        # 检查路由
        routes = [route.path for route in pcb_production_router.routes]
        print(f"  路由: {routes}")
        
    except Exception as e:
        print(f"  pcb_production_router: 导入失败 - {e}")
        import traceback
        traceback.print_exc()
    
    # 测试资源能源消耗API导入
    try:
        from app.api.v1.resource_consumption import router as resource_consumption_router
        print("  resource_consumption_router: 导入成功")
        
        # 检查路由
        routes = [route.path for route in resource_consumption_router.routes]
        print(f"  路由: {routes}")
        
    except Exception as e:
        print(f"  resource_consumption_router: 导入失败 - {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api_imports()
