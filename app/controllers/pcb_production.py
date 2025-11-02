"""
PCB企业生产情况数据控制器
实现企业生产情况数据的CRUD操作
"""
from typing import Dict, List, Optional
from decimal import Decimal

from app.core.crud import CRUDBase
from app.models.pcb_production import (
    PCBProductOutput,
    PCBQualificationRate,
    PCBOutputValue,
)


class PCBProductOutputController(CRUDBase[PCBProductOutput, Dict, Dict]):
    """PCB企业产品产量控制器"""

    def __init__(self):
        super().__init__(model=PCBProductOutput)

    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBProductOutput]:
        """获取企业所有产品产量数据"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by("year", "type", "main_product")

    async def batch_upsert(self, enterprise_id: int, data_list: List[Dict]) -> List[PCBProductOutput]:
        """批量更新或插入产品产量数据"""
        results = []
        
        for data in data_list:
            # 确保必填字段不为空
            type_val = data.get("type")
            main_product_val = data.get("main_product")
            year_val = data.get("year")
            
            # 跳过无效数据
            if not type_val or not main_product_val or not year_val:
                continue
            
            # 检查是否已存在
            existing = await self.model.get_or_none(
                enterprise_id=enterprise_id,
                type=type_val,
                main_product=main_product_val,
                year=year_val
            )
            
            if existing:
                # 更新现有记录
                existing.unit = data.get("unit")
                existing.output = Decimal(str(data.get("output"))) if data.get("output") else None
                existing.layers = data.get("layers")
                await existing.save()
                results.append(existing)
            else:
                # 创建新记录
                new_record = await self.model.create(
                    enterprise_id=enterprise_id,
                    type=type_val,
                    main_product=main_product_val,
                    unit=data.get("unit"),
                    year=year_val,
                    output=Decimal(str(data.get("output"))) if data.get("output") else None,
                    layers=data.get("layers")
                )
                results.append(new_record)
        
        return results

    async def delete_by_enterprise(self, enterprise_id: int) -> int:
        """删除企业所有产品产量数据"""
        return await self.model.filter(enterprise_id=enterprise_id).delete()


class PCBQualificationRateController(CRUDBase[PCBQualificationRate, Dict, Dict]):
    """PCB企业合格率控制器"""

    def __init__(self):
        super().__init__(model=PCBQualificationRate)

    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBQualificationRate]:
        """获取企业所有合格率数据"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by("year")

    async def batch_upsert(self, enterprise_id: int, data_list: List[Dict]) -> List[PCBQualificationRate]:
        """批量更新或插入合格率数据"""
        results = []
        
        for data in data_list:
            # 检查是否已存在
            existing = await self.model.get_or_none(
                enterprise_id=enterprise_id,
                year=data.get("year")
            )
            
            if existing:
                # 更新现有记录
                existing.rate = Decimal(str(data.get("rate"))) if data.get("rate") else None
                await existing.save()
                results.append(existing)
            else:
                # 创建新记录
                new_record = await self.model.create(
                    enterprise_id=enterprise_id,
                    year=data.get("year"),
                    rate=Decimal(str(data.get("rate"))) if data.get("rate") else None
                )
                results.append(new_record)
        
        return results

    async def delete_by_enterprise(self, enterprise_id: int) -> int:
        """删除企业所有合格率数据"""
        return await self.model.filter(enterprise_id=enterprise_id).delete()


class PCBOutputValueController(CRUDBase[PCBOutputValue, Dict, Dict]):
    """PCB企业产值情况控制器"""

    def __init__(self):
        super().__init__(model=PCBOutputValue)

    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBOutputValue]:
        """获取企业所有产值情况数据"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by("year")

    async def batch_upsert(self, enterprise_id: int, data_list: List[Dict]) -> List[PCBOutputValue]:
        """批量更新或插入产值情况数据"""
        results = []
        
        for data in data_list:
            # 验证必填字段
            year_val = data.get("year")
            if not year_val:
                continue
            
            # 检查是否已存在
            existing = await self.model.get_or_none(
                enterprise_id=enterprise_id,
                year=year_val
            )
            
            # 处理年产值：0是有效值，需要区分None和0
            annual_output_value = data.get("annualOutputValue")
            if annual_output_value is None or annual_output_value == "":
                annual_output_value_decimal = None
            else:
                try:
                    annual_output_value_decimal = Decimal(str(annual_output_value))
                except (ValueError, TypeError):
                    annual_output_value_decimal = None
            
            # 处理所得税：0是有效值，需要区分None和0
            income_tax = data.get("incomeTax")
            if income_tax is None or income_tax == "":
                income_tax_decimal = None
            else:
                try:
                    income_tax_decimal = Decimal(str(income_tax))
                except (ValueError, TypeError):
                    income_tax_decimal = None
            
            if existing:
                # 更新现有记录
                existing.unit = data.get("unit") or "wan_yuan"
                existing.annual_output_value = annual_output_value_decimal
                existing.income_tax = income_tax_decimal
                await existing.save()
                results.append(existing)
            else:
                # 创建新记录
                new_record = await self.model.create(
                    enterprise_id=enterprise_id,
                    year=year_val,
                    unit=data.get("unit") or "wan_yuan",
                    annual_output_value=annual_output_value_decimal,
                    income_tax=income_tax_decimal
                )
                results.append(new_record)
        
        return results

    async def delete_by_enterprise(self, enterprise_id: int) -> int:
        """删除企业所有产值情况数据"""
        return await self.model.filter(enterprise_id=enterprise_id).delete()


class PCBProductionDataController:
    """PCB企业生产情况数据综合控制器"""

    def __init__(self):
        self.product_output_controller = PCBProductOutputController()
        self.qualification_rate_controller = PCBQualificationRateController()
        self.output_value_controller = PCBOutputValueController()
        # 延迟导入避免循环依赖
        from app.controllers.pcb_raw_material import pcb_raw_material_usage_controller
        self.raw_material_usage_controller = pcb_raw_material_usage_controller

    async def get_all_production_data(self, enterprise_id: int) -> Dict:
        """获取企业所有生产情况数据"""
        try:
            product_outputs = await self.product_output_controller.get_by_enterprise(enterprise_id)
        except Exception as e:
            print(f"获取产品产量数据失败: {e}")
            product_outputs = []
        
        try:
            qualification_rates = await self.qualification_rate_controller.get_by_enterprise(enterprise_id)
        except Exception as e:
            print(f"获取合格率数据失败: {e}")
            qualification_rates = []
        
        try:
            output_values = await self.output_value_controller.get_by_enterprise(enterprise_id)
        except Exception as e:
            print(f"获取产值数据失败: {e}")
            output_values = []

        return {
            "productOutput": [
                {
                    "type": getattr(item, 'type', None),
                    "mainProduct": getattr(item, 'main_product', None),
                    "unit": getattr(item, 'unit', None),
                    "year": getattr(item, 'year', None),
                    "output": float(item.output) if hasattr(item, 'output') and item.output is not None else None,
                    "layers": getattr(item, 'layers', None)
                }
                for item in product_outputs
            ],
            "qualificationRate": [
                {
                    "year": getattr(item, 'year', None),
                    "rate": float(item.rate) if hasattr(item, 'rate') and item.rate is not None else None
                }
                for item in qualification_rates
            ],
            "outputValue": [
                {
                    "year": getattr(item, 'year', None),
                    "unit": getattr(item, 'unit', None),
                    "annualOutputValue": float(item.annual_output_value) if hasattr(item, 'annual_output_value') and item.annual_output_value is not None else None,
                    "incomeTax": float(item.income_tax) if hasattr(item, 'income_tax') and item.income_tax is not None else None
                }
                for item in output_values
            ]
        }

    async def save_all_production_data(self, enterprise_id: int, data: Dict) -> Dict:
        """保存企业所有生产情况数据"""
        # 先删除旧数据
        await self.product_output_controller.delete_by_enterprise(enterprise_id)
        await self.qualification_rate_controller.delete_by_enterprise(enterprise_id)
        await self.output_value_controller.delete_by_enterprise(enterprise_id)

        # 保存新数据
        product_outputs = await self.product_output_controller.batch_upsert(
            enterprise_id, data.get("productOutput", [])
        )
        qualification_rates = await self.qualification_rate_controller.batch_upsert(
            enterprise_id, data.get("qualificationRate", [])
        )
        output_values = await self.output_value_controller.batch_upsert(
            enterprise_id, data.get("outputValue", [])
        )

        return {
            "productOutput": len(product_outputs),
            "qualificationRate": len(qualification_rates),
            "outputValue": len(output_values)
        }

    async def get_three_years_product_output(self, enterprise_id: int, year_range: str) -> List[Dict]:
        """获取企业近三年产品产量数据（按年份范围）"""
        # 解析年份范围
        start_year, end_year = map(int, year_range.split('-'))
        years = [str(y) for y in range(start_year, end_year + 1)]
        
        # 获取该年份范围内的所有数据
        all_outputs = await self.product_output_controller.get_by_enterprise(enterprise_id)
        filtered_outputs = [item for item in all_outputs if item.year in years]
        
        # 按 type, main_product, unit, layers 分组
        grouped = {}
        for item in filtered_outputs:
            # 使用元组作为键，处理None值
            key = (
                item.type or "",
                item.main_product or "",
                item.unit or "",
                item.layers if item.layers is not None else -1
            )
            
            if key not in grouped:
                # 使用前端期望的字段名（camelCase）
                grouped[key] = {
                    "type": item.type,
                    "mainProduct": item.main_product,  # 转换为camelCase
                    "unit": item.unit,
                    "layers": item.layers
                }
                # 初始化所有年份字段
                for year in years:
                    grouped[key][f"output_{year}"] = None
            
            # 填充对应年份的数据
            if item.year in years:
                grouped[key][f"output_{item.year}"] = float(item.output) if item.output else None
        
        return list(grouped.values())

    async def save_three_years_product_output(self, enterprise_id: int, year_range: str, items: List[Dict]) -> int:
        """保存企业近三年产品产量数据"""
        # 解析年份范围
        start_year, end_year = map(int, year_range.split('-'))
        years = [str(y) for y in range(start_year, end_year + 1)]
        
        # 先删除该年份范围内的所有数据，确保删除功能正常工作
        await self.product_output_controller.model.filter(
            enterprise_id=enterprise_id,
            year__in=years
        ).delete()
        
        # 准备要保存的数据列表
        data_list = []
        for item in items:
            type_val = item.get("type")
            main_product_val = item.get("main_product")
            unit_val = item.get("unit")
            layers_val = item.get("layers")
            
            # 验证必填字段
            if not type_val or not main_product_val or not unit_val:
                continue
            
            for year in years:
                output_key = f"output_{year}"
                output_value = item.get(output_key)
                
                # 只保存有值的数据（跳过None值）
                if output_value is not None:
                    data_list.append({
                        "type": type_val,
                        "main_product": main_product_val,
                        "unit": unit_val,
                        "year": year,
                        "output": output_value,
                        "layers": layers_val
                    })
        
        # 批量创建新记录
        results = []
        for data_item in data_list:
            new_record = await self.product_output_controller.model.create(
                enterprise_id=enterprise_id,
                **data_item
            )
            results.append(new_record)
        
        return len(results)

    async def get_three_years_qualification_rate(self, enterprise_id: int, year_range: str) -> List[Dict]:
        """获取企业近三年合格率数据"""
        start_year, end_year = map(int, year_range.split('-'))
        years = [str(y) for y in range(start_year, end_year + 1)]
        
        all_rates = await self.qualification_rate_controller.get_by_enterprise(enterprise_id)
        filtered_rates = [item for item in all_rates if item.year in years]
        
        # 转换为字典列表
        result = []
        for item in filtered_rates:
            result.append({
                "year": item.year,
                "rate": float(item.rate) if item.rate else None
            })
        
        return result

    async def save_three_years_qualification_rate(self, enterprise_id: int, year_range: str, items: List[Dict]) -> int:
        """保存企业近三年合格率数据"""
        # 先删除该年份范围内的所有数据，确保删除功能正常工作
        years = [item.get("year") for item in items if item.get("year")]
        if years:
            await self.qualification_rate_controller.model.filter(
                enterprise_id=enterprise_id,
                year__in=years
            ).delete()
        
        # 批量创建新记录
        results = []
        for item in items:
            if item.get("year"):
                new_record = await self.qualification_rate_controller.model.create(
                    enterprise_id=enterprise_id,
                    year=item.get("year"),
                    rate=Decimal(str(item.get("rate"))) if item.get("rate") is not None else None
                )
                results.append(new_record)
        
        return len(results)

    async def get_three_years_output_value(self, enterprise_id: int, year_range: str) -> List[Dict]:
        """获取企业近三年产值数据"""
        start_year, end_year = map(int, year_range.split('-'))
        years = [str(y) for y in range(start_year, end_year + 1)]
        
        all_values = await self.output_value_controller.get_by_enterprise(enterprise_id)
        filtered_values = [item for item in all_values if item.year in years]
        
        # 创建一个以年份为键的字典，方便查找
        values_by_year = {}
        for item in filtered_values:
            # 处理年产值：0是有效值，需要正确转换
            annual_value = None
            if item.annual_output_value is not None:
                try:
                    annual_value = float(item.annual_output_value)
                except (ValueError, TypeError):
                    annual_value = None
            
            # 处理所得税：0是有效值，需要正确转换
            income_tax_value = None
            if item.income_tax is not None:
                try:
                    income_tax_value = float(item.income_tax)
                except (ValueError, TypeError):
                    income_tax_value = None
            
            values_by_year[item.year] = {
                "year": item.year,
                "unit": item.unit or "wan_yuan",
                "annualOutputValue": annual_value,
                "incomeTax": income_tax_value
            }
        
        # 按年份范围生成结果，确保每年都有数据（即使为空）
        result = []
        for year in years:
            if year in values_by_year:
                result.append(values_by_year[year])
            else:
                # 如果没有该年份的数据，创建一个空记录
                result.append({
                    "year": year,
                    "unit": "wan_yuan",
                    "annualOutputValue": None,
                    "incomeTax": None
                })
        
        return result

    async def save_three_years_output_value(self, enterprise_id: int, year_range: str, items: List[Dict]) -> int:
        """保存企业近三年产值数据"""
        # 先删除该年份范围内的所有数据，确保删除功能正常工作
        years = [item.get("year") for item in items if item.get("year")]
        if years:
            await self.output_value_controller.model.filter(
                enterprise_id=enterprise_id,
                year__in=years
            ).delete()
        
        # 批量创建新记录
        results = []
        for item in items:
            if item.get("year"):
                # 处理年产值和所得税：0是有效值
                annual_output_value = item.get("annualOutputValue")
                if annual_output_value is None or annual_output_value == "":
                    annual_output_value_decimal = None
                else:
                    try:
                        annual_output_value_decimal = Decimal(str(annual_output_value))
                    except (ValueError, TypeError):
                        annual_output_value_decimal = None
                
                income_tax = item.get("incomeTax")
                if income_tax is None or income_tax == "":
                    income_tax_decimal = None
                else:
                    try:
                        income_tax_decimal = Decimal(str(income_tax))
                    except (ValueError, TypeError):
                        income_tax_decimal = None
                
                new_record = await self.output_value_controller.model.create(
                    enterprise_id=enterprise_id,
                    year=item.get("year"),
                    unit=item.get("unit"),
                    annual_output_value=annual_output_value_decimal,
                    income_tax=income_tax_decimal
                )
                results.append(new_record)
        
        return len(results)

    async def get_three_years_raw_material_usage(self, enterprise_id: int, year_range: str) -> List[Dict]:
        """获取企业近三年原辅材料使用情况数据"""
        # 解析年份范围
        start_year, end_year = map(int, year_range.split('-'))
        years = [str(y) for y in range(start_year, end_year + 1)]
        
        # 获取所有数据
        all_usages = await self.raw_material_usage_controller.get_by_enterprise(enterprise_id)
        
        # 转换为前端需要的格式
        result = []
        for usage in all_usages:
            item = {
                "type": usage.type,
                "mainProduct": usage.main_product,  # camelCase
                "productOutput": float(usage.product_output) if usage.product_output else None,
                "materialName": usage.material_name,
                "unit": usage.unit
            }
            
            # 添加动态年份字段
            for year in years:
                amount_key = f"amount_{year}"
                unit_consumption_key = f"unitConsumption_{year}"
                
                amount_value = getattr(usage, amount_key, None)
                unit_consumption_value = getattr(usage, unit_consumption_key, None)
                
                item[amount_key] = float(amount_value) if amount_value else None
                item[unit_consumption_key] = float(unit_consumption_value) if unit_consumption_value else None
            
            result.append(item)
        
        return result

    async def save_three_years_raw_material_usage(self, enterprise_id: int, year_range: str, items: List[Dict]) -> int:
        """保存企业近三年原辅材料使用情况数据"""
        # 先删除该企业的所有原辅材料数据，确保删除功能正常工作
        await self.raw_material_usage_controller.model.filter(enterprise_id=enterprise_id).delete()
        
        # 转换前端字段名（camelCase -> snake_case）
        converted_items = []
        for item in items:
            converted_item = {
                "type": item.get("type"),
                "main_product": item.get("mainProduct") or item.get("main_product"),
                "product_output": item.get("productOutput") or item.get("product_output"),
                "material_name": item.get("materialName") or item.get("material_name"),
                "unit": item.get("unit")
            }
            
            # 添加动态年份字段（保持原样）
            for key in item.keys():
                if key.startswith("amount_") or key.startswith("unitConsumption_"):
                    converted_item[key] = item[key]
            
            converted_items.append(converted_item)
        
        # 批量创建新记录
        results = await self.raw_material_usage_controller.batch_upsert(enterprise_id, converted_items)
        return len(results)


# 创建控制器实例
pcb_product_output_controller = PCBProductOutputController()
pcb_qualification_rate_controller = PCBQualificationRateController()
pcb_output_value_controller = PCBOutputValueController()
pcb_production_data_controller = PCBProductionDataController()
