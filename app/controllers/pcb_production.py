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
            # 检查是否已存在
            existing = await self.model.get_or_none(
                enterprise_id=enterprise_id,
                type=data.get("type"),
                main_product=data.get("main_product"),
                year=data.get("year")
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
                    type=data.get("type"),
                    main_product=data.get("main_product"),
                    unit=data.get("unit"),
                    year=data.get("year"),
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
            # 检查是否已存在
            existing = await self.model.get_or_none(
                enterprise_id=enterprise_id,
                year=data.get("year")
            )
            
            if existing:
                # 更新现有记录
                existing.unit = data.get("unit")
                existing.annual_output_value = Decimal(str(data.get("annualOutputValue"))) if data.get("annualOutputValue") else None
                existing.income_tax = Decimal(str(data.get("incomeTax"))) if data.get("incomeTax") else None
                await existing.save()
                results.append(existing)
            else:
                # 创建新记录
                new_record = await self.model.create(
                    enterprise_id=enterprise_id,
                    year=data.get("year"),
                    unit=data.get("unit"),
                    annual_output_value=Decimal(str(data.get("annualOutputValue"))) if data.get("annualOutputValue") else None,
                    income_tax=Decimal(str(data.get("incomeTax"))) if data.get("incomeTax") else None
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

    async def get_all_production_data(self, enterprise_id: int) -> Dict:
        """获取企业所有生产情况数据"""
        product_outputs = await self.product_output_controller.get_by_enterprise(enterprise_id)
        qualification_rates = await self.qualification_rate_controller.get_by_enterprise(enterprise_id)
        output_values = await self.output_value_controller.get_by_enterprise(enterprise_id)

        return {
            "productOutput": [
                {
                    "type": item.type,
                    "mainProduct": item.main_product,
                    "unit": item.unit,
                    "year": item.year,
                    "output": float(item.output) if item.output else None,
                    "layers": item.layers
                }
                for item in product_outputs
            ],
            "qualificationRate": [
                {
                    "year": item.year,
                    "rate": float(item.rate) if item.rate else None
                }
                for item in qualification_rates
            ],
            "outputValue": [
                {
                    "year": item.year,
                    "unit": item.unit,
                    "annualOutputValue": float(item.annual_output_value) if item.annual_output_value else None,
                    "incomeTax": float(item.income_tax) if item.income_tax else None
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


# 创建控制器实例
pcb_product_output_controller = PCBProductOutputController()
pcb_qualification_rate_controller = PCBQualificationRateController()
pcb_output_value_controller = PCBOutputValueController()
pcb_production_data_controller = PCBProductionDataController()
