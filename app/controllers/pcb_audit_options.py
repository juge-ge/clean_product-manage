"""
PCB审核选项型数据控制器
"""
from typing import Dict, Optional
from app.core.crud import CRUDBase
from app.models.pcb_audit_options import (
    PCBProcessEquipmentRequirement,
    PCBGreenhouseGasEmission,
    PCBProductCharacteristics,
    PCBCleanProductionManagement,
    PCBResourceReutilization
)
from app.schemas.pcb_audit_options import (
    PCBProcessEquipmentRequirementCreate,
    PCBProcessEquipmentRequirementUpdate,
    PCBGreenhouseGasEmissionCreate,
    PCBGreenhouseGasEmissionUpdate,
    PCBProductCharacteristicsCreate,
    PCBProductCharacteristicsUpdate,
    PCBCleanProductionManagementCreate,
    PCBCleanProductionManagementUpdate,
    PCBResourceReutilizationCreate,
    PCBResourceReutilizationUpdate,
)


class PCBProcessEquipmentRequirementController(CRUDBase[PCBProcessEquipmentRequirement, PCBProcessEquipmentRequirementCreate, PCBProcessEquipmentRequirementUpdate]):
    """生产工艺与装备要求控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> Optional[PCBProcessEquipmentRequirement]:
        """获取企业的生产工艺与装备要求记录"""
        return await self.model.filter(enterprise_id=enterprise_id).first()
    
    async def upsert(self, enterprise_id: int, data: Dict) -> PCBProcessEquipmentRequirement:
        """更新或插入生产工艺与装备要求记录"""
        existing = await self.get_by_enterprise(enterprise_id)
        
        if existing:
            # 更新现有记录
            await self.model.filter(id=existing.id).update(
                basic_requirements=data.get("basicRequirements") or data.get("basic_requirements"),
                mechanical_facilities=data.get("mechanicalFacilities") or data.get("mechanical_facilities"),
                printing_process=data.get("printingProcess") or data.get("printing_process"),
                cleaning=data.get("cleaning"),
                etching=data.get("etching"),
                plating=data.get("plating"),
                remark=data.get("remark")
            )
            return await self.model.get(id=existing.id)
        else:
            # 创建新记录
            return await self.model.create(
                enterprise_id=enterprise_id,
                basic_requirements=data.get("basicRequirements") or data.get("basic_requirements"),
                mechanical_facilities=data.get("mechanicalFacilities") or data.get("mechanical_facilities"),
                printing_process=data.get("printingProcess") or data.get("printing_process"),
                cleaning=data.get("cleaning"),
                etching=data.get("etching"),
                plating=data.get("plating"),
                remark=data.get("remark")
            )


class PCBGreenhouseGasEmissionController(CRUDBase[PCBGreenhouseGasEmission, PCBGreenhouseGasEmissionCreate, PCBGreenhouseGasEmissionUpdate]):
    """温室气体排放控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> Optional[PCBGreenhouseGasEmission]:
        """获取企业的温室气体排放记录"""
        return await self.model.filter(enterprise_id=enterprise_id).first()
    
    async def upsert(self, enterprise_id: int, data: Dict) -> PCBGreenhouseGasEmission:
        """更新或插入温室气体排放记录"""
        existing = await self.get_by_enterprise(enterprise_id)
        
        if existing:
            # 更新现有记录
            await self.model.filter(id=existing.id).update(
                carbon_management=data.get("carbonManagement") or data.get("carbon_management"),
                emission_per_output=data.get("emissionPerOutput") or data.get("emission_per_output"),
                emission_intensity=data.get("emissionIntensity") or data.get("emission_intensity"),
                remark=data.get("remark")
            )
            return await self.model.get(id=existing.id)
        else:
            # 创建新记录
            return await self.model.create(
                enterprise_id=enterprise_id,
                carbon_management=data.get("carbonManagement") or data.get("carbon_management"),
                emission_per_output=data.get("emissionPerOutput") or data.get("emission_per_output"),
                emission_intensity=data.get("emissionIntensity") or data.get("emission_intensity"),
                remark=data.get("remark")
            )


class PCBProductCharacteristicsController(CRUDBase[PCBProductCharacteristics, PCBProductCharacteristicsCreate, PCBProductCharacteristicsUpdate]):
    """产品特征控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> Optional[PCBProductCharacteristics]:
        """获取企业的产品特征记录"""
        return await self.model.filter(enterprise_id=enterprise_id).first()
    
    async def upsert(self, enterprise_id: int, data: Dict) -> PCBProductCharacteristics:
        """更新或插入产品特征记录"""
        existing = await self.get_by_enterprise(enterprise_id)
        
        if existing:
            # 更新现有记录
            await self.model.filter(id=existing.id).update(
                auxiliary_material=data.get("auxiliaryMaterial") or data.get("auxiliary_material"),
                packaging=data.get("packaging"),
                hazardous_substance=data.get("hazardousSubstance") or data.get("hazardous_substance"),
                product_performance=data.get("productPerformance") or data.get("product_performance"),
                remark=data.get("remark")
            )
            return await self.model.get(id=existing.id)
        else:
            # 创建新记录
            return await self.model.create(
                enterprise_id=enterprise_id,
                auxiliary_material=data.get("auxiliaryMaterial") or data.get("auxiliary_material"),
                packaging=data.get("packaging"),
                hazardous_substance=data.get("hazardousSubstance") or data.get("hazardous_substance"),
                product_performance=data.get("productPerformance") or data.get("product_performance"),
                remark=data.get("remark")
            )


class PCBCleanProductionManagementController(CRUDBase[PCBCleanProductionManagement, PCBCleanProductionManagementCreate, PCBCleanProductionManagementUpdate]):
    """清洁生产管理控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> Optional[PCBCleanProductionManagement]:
        """获取企业的清洁生产管理记录"""
        return await self.model.filter(enterprise_id=enterprise_id).first()
    
    async def upsert(self, enterprise_id: int, data: Dict) -> PCBCleanProductionManagement:
        """更新或插入清洁生产管理记录"""
        existing = await self.get_by_enterprise(enterprise_id)
        
        if existing:
            # 更新现有记录
            await self.model.filter(id=existing.id).update(
                environmental_law=data.get("environmentalLaw") or data.get("environmental_law"),
                industrial_policy=data.get("industrialPolicy") or data.get("industrial_policy"),
                clean_production_management=data.get("cleanProductionManagement") or data.get("clean_production_management"),
                clean_production_audit=data.get("cleanProductionAudit") or data.get("clean_production_audit"),
                energy_management=data.get("energyManagement") or data.get("energy_management"),
                emission_monitoring=data.get("emissionMonitoring") or data.get("emission_monitoring"),
                chemical_management=data.get("chemicalManagement") or data.get("chemical_management"),
                measurement_equipment=data.get("measurementEquipment") or data.get("measurement_equipment"),
                solid_waste_disposal=data.get("solidWasteDisposal") or data.get("solid_waste_disposal"),
                soil_pollution_risk=data.get("soilPollutionRisk") or data.get("soil_pollution_risk"),
                transport_mode=data.get("transportMode") or data.get("transport_mode"),
                remark=data.get("remark")
            )
            return await self.model.get(id=existing.id)
        else:
            # 创建新记录
            return await self.model.create(
                enterprise_id=enterprise_id,
                environmental_law=data.get("environmentalLaw") or data.get("environmental_law"),
                industrial_policy=data.get("industrialPolicy") or data.get("industrial_policy"),
                clean_production_management=data.get("cleanProductionManagement") or data.get("clean_production_management"),
                clean_production_audit=data.get("cleanProductionAudit") or data.get("clean_production_audit"),
                energy_management=data.get("energyManagement") or data.get("energy_management"),
                emission_monitoring=data.get("emissionMonitoring") or data.get("emission_monitoring"),
                chemical_management=data.get("chemicalManagement") or data.get("chemical_management"),
                measurement_equipment=data.get("measurementEquipment") or data.get("measurement_equipment"),
                solid_waste_disposal=data.get("solidWasteDisposal") or data.get("solid_waste_disposal"),
                soil_pollution_risk=data.get("soilPollutionRisk") or data.get("soil_pollution_risk"),
                transport_mode=data.get("transportMode") or data.get("transport_mode"),
                remark=data.get("remark")
            )


class PCBResourceReutilizationController(CRUDBase[PCBResourceReutilization, PCBResourceReutilizationCreate, PCBResourceReutilizationUpdate]):
    """资源综合利用控制器"""
    
    async def get_by_enterprise(self, enterprise_id: int) -> Optional[PCBResourceReutilization]:
        """获取企业的资源综合利用记录"""
        return await self.model.filter(enterprise_id=enterprise_id).first()
    
    async def upsert(self, enterprise_id: int, data: Dict) -> PCBResourceReutilization:
        """更新或插入资源综合利用记录"""
        existing = await self.get_by_enterprise(enterprise_id)
        
        if existing:
            # 更新现有记录
            await self.model.filter(id=existing.id).update(
                water_reuse=data.get("waterReuse") or data.get("water_reuse"),
                etching_recovery=data.get("etchingRecovery") or data.get("etching_recovery"),
                general_solid_util=data.get("generalSolidUtil") or data.get("general_solid_util"),
                wastewater_collection=data.get("wastewaterCollection") or data.get("wastewater_collection"),
                waste_gas_treatment=data.get("wasteGasTreatment") or data.get("waste_gas_treatment"),
                general_solid_collection=data.get("generalSolidCollection") or data.get("general_solid_collection"),
                hazardous_waste_collection=data.get("hazardousWasteCollection") or data.get("hazardous_waste_collection"),
                noise=data.get("noise"),
                remark=data.get("remark")
            )
            return await self.model.get(id=existing.id)
        else:
            # 创建新记录
            return await self.model.create(
                enterprise_id=enterprise_id,
                water_reuse=data.get("waterReuse") or data.get("water_reuse"),
                etching_recovery=data.get("etchingRecovery") or data.get("etching_recovery"),
                general_solid_util=data.get("generalSolidUtil") or data.get("general_solid_util"),
                wastewater_collection=data.get("wastewaterCollection") or data.get("wastewater_collection"),
                waste_gas_treatment=data.get("wasteGasTreatment") or data.get("waste_gas_treatment"),
                general_solid_collection=data.get("generalSolidCollection") or data.get("general_solid_collection"),
                hazardous_waste_collection=data.get("hazardousWasteCollection") or data.get("hazardous_waste_collection"),
                noise=data.get("noise"),
                remark=data.get("remark")
            )


# 创建控制器实例
process_equipment_requirement_controller = PCBProcessEquipmentRequirementController(PCBProcessEquipmentRequirement)
greenhouse_gas_emission_controller = PCBGreenhouseGasEmissionController(PCBGreenhouseGasEmission)
product_characteristics_controller = PCBProductCharacteristicsController(PCBProductCharacteristics)
clean_production_management_controller = PCBCleanProductionManagementController(PCBCleanProductionManagement)
resource_reutilization_controller = PCBResourceReutilizationController(PCBResourceReutilization)

