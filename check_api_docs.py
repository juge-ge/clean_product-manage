#!/usr/bin/env python3
"""
检查API文档
"""

import requests
import json

def check_api_docs():
    """检查API文档"""
    try:
        response = requests.get("http://localhost:9999/openapi.json")
        if response.status_code == 200:
            openapi = response.json()
            paths = openapi.get("paths", {})
            
            print("检查API路径:")
            for path in paths:
                if "production-data" in path or "resource-consumption" in path:
                    print(f"  找到: {path}")
                    methods = paths[path]
                    for method in methods:
                        if method.upper() in ["GET", "POST", "PUT", "DELETE"]:
                            print(f"    {method.upper()}: {methods[method].get('summary', '无描述')}")
            
            # 检查是否有这些路径
            production_path = "/api/v1/pcb/enterprise/{enterprise_id}/production-data"
            resource_path = "/api/v1/resource-consumption/enterprise/{enterprise_id}/all-data"
            
            if production_path in paths:
                print(f"\n生产数据API存在: {production_path}")
            else:
                print(f"\n生产数据API不存在: {production_path}")
                
            if resource_path in paths:
                print(f"资源能源消耗API存在: {resource_path}")
            else:
                print(f"资源能源消耗API不存在: {resource_path}")
                
        else:
            print(f"获取API文档失败: {response.status_code}")
            
    except Exception as e:
        print(f"检查失败: {e}")

if __name__ == "__main__":
    check_api_docs()
