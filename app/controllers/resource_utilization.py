"""
PCB企业资源利用数据控制器
"""
from typing import List, Dict
from decimal import Decimal
from app.core.crud import CRUDBase
from app.models.resource_utilization import (
    PCBEnergyConsumption,
    PCBFreshWaterConsumption,
    PCBWastewaterTotalConsumption,
    PCBWastewaterCuConsumption,
    PCBWastewaterCODConsumption,
    PCBRawMaterialConsumption
)
from app.schemas.resource_utilization import (
    PCBEnergyConsumptionCreate,
    PCBEnergyConsumptionUpdate,
    PCBFreshWaterConsumptionCreate,
    PCBFreshWaterConsumptionUpdate,
    PCBWastewaterTotalConsumptionCreate,
    PCBWastewaterTotalConsumptionUpdate,
    PCBWastewaterCuConsumptionCreate,
    PCBWastewaterCuConsumptionUpdate,
    PCBWastewaterCODConsumptionCreate,
    PCBWastewaterCODConsumptionUpdate,
    PCBRawMaterialConsumptionCreate,
    PCBRawMaterialConsumptionUpdate,
)


class PCBEnergyConsumptionController(CRUDBase[PCBEnergyConsumption, PCBEnergyConsumptionCreate, PCBEnergyConsumptionUpdate]):
    """能源消耗控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBEnergyConsumption]:
        """获取企业的所有能源消耗记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('type', 'main_product')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBEnergyConsumption]:
        """批量更新或插入能源消耗记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有能源消耗记录
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for item in items:
            # 安全地获取Decimal值
            def get_decimal_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                try:
                    return Decimal(str(value))
                except (ValueError, TypeError):
                    return None
            
            record_data = {
                "enterprise_id": enterprise_id,
                "type": item.get("type") or "",
                "main_product": item.get("mainProduct") or item.get("main_product") or "",
                "layers": item.get("layers") or 1,
                "output": get_decimal_value("output"),
                "electricity": get_decimal_value("electricity"),
                "unit_consumption": get_decimal_value("unitConsumption"),
                "rating": item.get("rating") or None,
            }
            
            # 验证必填字段
            if not record_data["type"] or not record_data["main_product"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBFreshWaterConsumptionController(CRUDBase[PCBFreshWaterConsumption, PCBFreshWaterConsumptionCreate, PCBFreshWaterConsumptionUpdate]):
    """新鲜水耗控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBFreshWaterConsumption]:
        """获取企业的所有新鲜水耗记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('product', 'layers')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBFreshWaterConsumption]:
        """批量更新或插入新鲜水耗记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有新鲜水耗记录
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for item in items:
            # 安全地获取Decimal值
            def get_decimal_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                try:
                    return Decimal(str(value))
                except (ValueError, TypeError):
                    return None
            
            record_data = {
                "enterprise_id": enterprise_id,
                "product": item.get("product") or "",
                "layers": item.get("layers") or 1,
                "output": get_decimal_value("output"),
                "fresh_water": get_decimal_value("freshWater"),
                "unit_fresh_water": get_decimal_value("unitFreshWater"),
                "rating": item.get("rating") or None,
            }
            
            # 验证必填字段
            if not record_data["product"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBWastewaterTotalConsumptionController(CRUDBase[PCBWastewaterTotalConsumption, PCBWastewaterTotalConsumptionCreate, PCBWastewaterTotalConsumptionUpdate]):
    """废水总量控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWastewaterTotalConsumption]:
        """获取企业的所有废水总量记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('product', 'layers')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBWastewaterTotalConsumption]:
        """批量更新或插入废水总量记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有废水总量记录
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for item in items:
            # 安全地获取Decimal值
            def get_decimal_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                try:
                    return Decimal(str(value))
                except (ValueError, TypeError):
                    return None
            
            record_data = {
                "enterprise_id": enterprise_id,
                "product": item.get("product") or "",
                "layers": item.get("layers") or 1,
                "output": get_decimal_value("output"),
                "wastewater_total": get_decimal_value("wastewaterTotal"),
                "unit_wastewater": get_decimal_value("unitWastewater"),
                "rating": item.get("rating") or None,
            }
            
            # 验证必填字段
            if not record_data["product"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBWastewaterCuConsumptionController(CRUDBase[PCBWastewaterCuConsumption, PCBWastewaterCuConsumptionCreate, PCBWastewaterCuConsumptionUpdate]):
    """废水中总铜浓度控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWastewaterCuConsumption]:
        """获取企业的所有废水中总铜浓度记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('product', 'layers')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBWastewaterCuConsumption]:
        """批量更新或插入废水中总铜浓度记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有废水中总铜浓度记录
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for item in items:
            # 安全地获取Decimal值
            def get_decimal_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                try:
                    return Decimal(str(value))
                except (ValueError, TypeError):
                    return None
            
            record_data = {
                "enterprise_id": enterprise_id,
                "product": item.get("product") or "",
                "layers": item.get("layers") or 1,
                "output": get_decimal_value("output"),
                "wastewater_total": get_decimal_value("wastewaterTotal"),
                "wastewater_cu": get_decimal_value("wastewaterCu"),
                "unit_cu": get_decimal_value("unitWastewaterCu"),
                "rating": item.get("rating") or None,
            }
            
            # 验证必填字段
            if not record_data["product"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBWastewaterCODConsumptionController(CRUDBase[PCBWastewaterCODConsumption, PCBWastewaterCODConsumptionCreate, PCBWastewaterCODConsumptionUpdate]):
    """废水中COD浓度控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWastewaterCODConsumption]:
        """获取企业的所有废水中COD浓度记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('product', 'layers')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBWastewaterCODConsumption]:
        """批量更新或插入废水中COD浓度记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有废水中COD浓度记录
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for item in items:
            # 安全地获取Decimal值
            def get_decimal_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                try:
                    return Decimal(str(value))
                except (ValueError, TypeError):
                    return None
            
            record_data = {
                "enterprise_id": enterprise_id,
                "product": item.get("product") or "",
                "layers": item.get("layers") or 1,
                "output": get_decimal_value("output"),
                "wastewater_total": get_decimal_value("wastewaterTotal"),
                "wastewater_cod": get_decimal_value("wastewaterCOD"),
                "unit_cod": get_decimal_value("unitWastewaterCOD"),
                "rating": item.get("rating") or None,
            }
            
            # 验证必填字段
            if not record_data["product"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


class PCBRawMaterialConsumptionController(CRUDBase[PCBRawMaterialConsumption, PCBRawMaterialConsumptionCreate, PCBRawMaterialConsumptionUpdate]):
    """原/辅料消耗（覆铜板）控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBRawMaterialConsumption]:
        """获取企业的所有原/辅料消耗记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by('type', 'main_product')
    
    async def batch_upsert(self, enterprise_id: int, items: List[Dict]) -> List[PCBRawMaterialConsumption]:
        """批量更新或插入原/辅料消耗记录 - 先删除后创建确保删除功能正常"""
        # 先删除该企业的所有原/辅料消耗记录
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 创建新记录
        results = []
        for item in items:
            # 安全地获取Decimal值
            def get_decimal_value(key):
                value = item.get(key)
                if value is None or value == "":
                    return None
                try:
                    return Decimal(str(value))
                except (ValueError, TypeError):
                    return None
            
            record_data = {
                "enterprise_id": enterprise_id,
                "type": item.get("type") or "",
                "main_product": item.get("mainProduct") or item.get("main_product") or "",
                "layers": item.get("layers") or 1,
                "output": get_decimal_value("output"),
                "ccl_consumption": get_decimal_value("cclConsumption"),
                "ccl_utilization": get_decimal_value("cclUtilization"),
                "rating": item.get("rating") or None,
            }
            
            # 验证必填字段
            if not record_data["type"] or not record_data["main_product"]:
                continue
            
            new_record = await self.model.create(**record_data)
            results.append(new_record)
        
        return results


# 创建控制器实例
energy_consumption_controller = PCBEnergyConsumptionController(PCBEnergyConsumption)
fresh_water_consumption_controller = PCBFreshWaterConsumptionController(PCBFreshWaterConsumption)
wastewater_total_consumption_controller = PCBWastewaterTotalConsumptionController(PCBWastewaterTotalConsumption)
wastewater_cu_consumption_controller = PCBWastewaterCuConsumptionController(PCBWastewaterCuConsumption)
wastewater_cod_consumption_controller = PCBWastewaterCODConsumptionController(PCBWastewaterCODConsumption)
raw_material_consumption_controller = PCBRawMaterialConsumptionController(PCBRawMaterialConsumption)

