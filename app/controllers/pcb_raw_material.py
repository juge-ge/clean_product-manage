"""
PCB企业原辅材料使用情况控制器
用于处理企业近三年原辅材料使用情况数据
"""
from typing import List, Dict, Optional
from decimal import Decimal
from app.core.crud import CRUDBase
from app.models.pcb_raw_material import PCBRawMaterialUsage


class PCBRawMaterialUsageController(CRUDBase[PCBRawMaterialUsage, Dict, Dict]):
    """PCB企业原辅材料使用情况控制器"""

    def __init__(self):
        super().__init__(model=PCBRawMaterialUsage)

    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBRawMaterialUsage]:
        """获取企业所有原辅材料使用情况数据"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by("type", "main_product", "material_name")

    async def batch_upsert(self, enterprise_id: int, data_list: List[Dict]) -> List[PCBRawMaterialUsage]:
        """批量更新或插入原辅材料使用情况数据"""
        results = []
        
        for data in data_list:
            # 确保必填字段不为空
            type_val = data.get("type")
            main_product_val = data.get("main_product")
            material_name_val = data.get("material_name")
            
            # 跳过无效数据
            if not type_val or not main_product_val or not material_name_val:
                continue
            
            # 检查是否已存在
            existing = await self.model.get_or_none(
                enterprise_id=enterprise_id,
                type=type_val,
                main_product=main_product_val,
                material_name=material_name_val
            )
            
            # 处理产品产量
            product_output = data.get("product_output")
            product_output_decimal = None
            if product_output is not None and product_output != "":
                try:
                    product_output_decimal = Decimal(str(product_output))
                except (ValueError, TypeError):
                    product_output_decimal = None
            
            # 处理动态年份字段
            year_fields = {}
            for year in range(2020, 2025):  # 支持2020-2024
                year_str = str(year)
                
                # 年消耗量字段
                amount_key = f"amount_{year_str}"
                amount_val = data.get(amount_key)
                if amount_val is not None and amount_val != "":
                    try:
                        year_fields[amount_key] = Decimal(str(amount_val))
                    except (ValueError, TypeError):
                        year_fields[amount_key] = None
                else:
                    year_fields[amount_key] = None
                
                # 单位产品消耗量字段（前端可能是unitConsumption_或unit_consumption_，后端模型是unitConsumption_）
                unit_consumption_key_frontend = f"unitConsumption_{year_str}"
                unit_consumption_val = data.get(unit_consumption_key_frontend)
                if unit_consumption_val is None:
                    # 尝试snake_case格式
                    unit_consumption_key_snake = f"unit_consumption_{year_str}"
                    unit_consumption_val = data.get(unit_consumption_key_snake)
                
                # 后端模型字段名使用camelCase格式（unitConsumption_2022）
                unit_consumption_key_model = f"unitConsumption_{year_str}"
                if unit_consumption_val is not None and unit_consumption_val != "":
                    try:
                        year_fields[unit_consumption_key_model] = Decimal(str(unit_consumption_val))
                    except (ValueError, TypeError):
                        year_fields[unit_consumption_key_model] = None
                else:
                    year_fields[unit_consumption_key_model] = None
            
            if existing:
                # 更新现有记录
                existing.product_output = product_output_decimal
                existing.unit = data.get("unit")
                for key, value in year_fields.items():
                    setattr(existing, key, value)
                await existing.save()
                results.append(existing)
            else:
                # 创建新记录
                create_data = {
                    "enterprise_id": enterprise_id,
                    "type": type_val,
                    "main_product": main_product_val,
                    "material_name": material_name_val,
                    "product_output": product_output_decimal,
                    "unit": data.get("unit")
                }
                create_data.update(year_fields)
                new_record = await self.model.create(**create_data)
                results.append(new_record)
        
        return results

    async def delete_by_enterprise(self, enterprise_id: int) -> int:
        """删除企业所有原辅材料使用情况数据"""
        return await self.model.filter(enterprise_id=enterprise_id).delete()


# 创建控制器实例
pcb_raw_material_usage_controller = PCBRawMaterialUsageController()

