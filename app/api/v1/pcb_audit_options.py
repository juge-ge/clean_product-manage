"""
PCB审核选项型数据API路由
提供生产工艺与装备要求、温室气体排放、产品特征、清洁生产管理、资源综合利用的增删改查接口
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Body

from app.controllers.pcb_audit_options import (
    process_equipment_requirement_controller,
    greenhouse_gas_emission_controller,
    product_characteristics_controller,
    clean_production_management_controller,
    resource_reutilization_controller,
)
from app.schemas.base import Success
from app.core.dependency import DependAuth

router = APIRouter()


# ==================== 生产工艺与装备要求相关API ====================

@router.get("/enterprise/{enterprise_id}/process-requirement", summary="获取企业生产工艺与装备要求")
async def get_process_equipment_requirement(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业生产工艺与装备要求"""
    try:
        record = await process_equipment_requirement_controller.get_by_enterprise(enterprise_id)
        
        if not record:
            return Success(data={
                "basicRequirements": [],
                "mechanicalFacilities": [],
                "printingProcess": [],
                "cleaning": [],
                "etching": [],
                "plating": []
            }, msg="获取成功")
        
        return Success(data={
            "id": record.id,
            "basicRequirements": record.basic_requirements or [],
            "mechanicalFacilities": record.mechanical_facilities or [],
            "printingProcess": record.printing_process or [],
            "cleaning": record.cleaning or [],
            "etching": record.etching or [],
            "plating": record.plating or []
        }, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业生产工艺与装备要求失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/process-requirement", summary="保存企业生产工艺与装备要求")
async def save_process_equipment_requirement(
    enterprise_id: int,
    data: Dict[str, Any] = Body(..., description="生产工艺与装备要求数据"),
    current_user=DependAuth
):
    """保存企业生产工艺与装备要求"""
    try:
        result = await process_equipment_requirement_controller.upsert(enterprise_id, data)
        
        return Success(data={
            "id": result.id,
            "basicRequirements": result.basic_requirements or [],
            "mechanicalFacilities": result.mechanical_facilities or [],
            "printingProcess": result.printing_process or [],
            "cleaning": result.cleaning or [],
            "etching": result.etching or [],
            "plating": result.plating or []
        }, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业生产工艺与装备要求失败: {str(e)}"
        )


# ==================== 温室气体排放相关API ====================

@router.get("/enterprise/{enterprise_id}/greenhouse-gas-emission", summary="获取企业温室气体排放")
async def get_greenhouse_gas_emission(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业温室气体排放"""
    try:
        record = await greenhouse_gas_emission_controller.get_by_enterprise(enterprise_id)
        
        if not record:
            return Success(data={
                "carbonManagement": [],
                "emissionPerOutput": [],
                "emissionIntensity": []
            }, msg="获取成功")
        
        return Success(data={
            "id": record.id,
            "carbonManagement": record.carbon_management or [],
            "emissionPerOutput": record.emission_per_output or [],
            "emissionIntensity": record.emission_intensity or []
        }, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业温室气体排放失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/greenhouse-gas-emission", summary="保存企业温室气体排放")
async def save_greenhouse_gas_emission(
    enterprise_id: int,
    data: Dict[str, Any] = Body(..., description="温室气体排放数据"),
    current_user=DependAuth
):
    """保存企业温室气体排放"""
    try:
        result = await greenhouse_gas_emission_controller.upsert(enterprise_id, data)
        
        return Success(data={
            "id": result.id,
            "carbonManagement": result.carbon_management or [],
            "emissionPerOutput": result.emission_per_output or [],
            "emissionIntensity": result.emission_intensity or []
        }, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业温室气体排放失败: {str(e)}"
        )


# ==================== 产品特征相关API ====================

@router.get("/enterprise/{enterprise_id}/product-characteristics", summary="获取企业产品特征")
async def get_product_characteristics(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业产品特征"""
    try:
        record = await product_characteristics_controller.get_by_enterprise(enterprise_id)
        
        if not record:
            return Success(data={
                "auxiliaryMaterial": [],
                "packaging": [],
                "hazardousSubstance": [],
                "productPerformance": []
            }, msg="获取成功")
        
        return Success(data={
            "id": record.id,
            "auxiliaryMaterial": record.auxiliary_material or [],
            "packaging": record.packaging or [],
            "hazardousSubstance": record.hazardous_substance or [],
            "productPerformance": record.product_performance or []
        }, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业产品特征失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/product-characteristics", summary="保存企业产品特征")
async def save_product_characteristics(
    enterprise_id: int,
    data: Dict[str, Any] = Body(..., description="产品特征数据"),
    current_user=DependAuth
):
    """保存企业产品特征"""
    try:
        result = await product_characteristics_controller.upsert(enterprise_id, data)
        
        return Success(data={
            "id": result.id,
            "auxiliaryMaterial": result.auxiliary_material or [],
            "packaging": result.packaging or [],
            "hazardousSubstance": result.hazardous_substance or [],
            "productPerformance": result.product_performance or []
        }, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业产品特征失败: {str(e)}"
        )


# ==================== 清洁生产管理相关API ====================

@router.get("/enterprise/{enterprise_id}/clean-production-management", summary="获取企业清洁生产管理")
async def get_clean_production_management(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业清洁生产管理"""
    try:
        record = await clean_production_management_controller.get_by_enterprise(enterprise_id)
        
        if not record:
            return Success(data={
                "environmentalLaw": [],
                "industrialPolicy": [],
                "cleanProductionManagement": [],
                "cleanProductionAudit": [],
                "energyManagement": [],
                "emissionMonitoring": [],
                "chemicalManagement": [],
                "measurementEquipment": [],
                "solidWasteDisposal": [],
                "soilPollutionRisk": [],
                "transportMode": []
            }, msg="获取成功")
        
        return Success(data={
            "id": record.id,
            "environmentalLaw": record.environmental_law or [],
            "industrialPolicy": record.industrial_policy or [],
            "cleanProductionManagement": record.clean_production_management or [],
            "cleanProductionAudit": record.clean_production_audit or [],
            "energyManagement": record.energy_management or [],
            "emissionMonitoring": record.emission_monitoring or [],
            "chemicalManagement": record.chemical_management or [],
            "measurementEquipment": record.measurement_equipment or [],
            "solidWasteDisposal": record.solid_waste_disposal or [],
            "soilPollutionRisk": record.soil_pollution_risk or [],
            "transportMode": record.transport_mode or []
        }, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业清洁生产管理失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/clean-production-management", summary="保存企业清洁生产管理")
async def save_clean_production_management(
    enterprise_id: int,
    data: Dict[str, Any] = Body(..., description="清洁生产管理数据"),
    current_user=DependAuth
):
    """保存企业清洁生产管理"""
    try:
        result = await clean_production_management_controller.upsert(enterprise_id, data)
        
        return Success(data={
            "id": result.id,
            "environmentalLaw": result.environmental_law or [],
            "industrialPolicy": result.industrial_policy or [],
            "cleanProductionManagement": result.clean_production_management or [],
            "cleanProductionAudit": result.clean_production_audit or [],
            "energyManagement": result.energy_management or [],
            "emissionMonitoring": result.emission_monitoring or [],
            "chemicalManagement": result.chemical_management or [],
            "measurementEquipment": result.measurement_equipment or [],
            "solidWasteDisposal": result.solid_waste_disposal or [],
            "soilPollutionRisk": result.soil_pollution_risk or [],
            "transportMode": result.transport_mode or []
        }, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业清洁生产管理失败: {str(e)}"
        )


# ==================== 资源综合利用相关API ====================

@router.get("/enterprise/{enterprise_id}/resource-reutilization", summary="获取企业资源综合利用")
async def get_resource_reutilization(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业资源综合利用"""
    try:
        record = await resource_reutilization_controller.get_by_enterprise(enterprise_id)
        
        if not record:
            return Success(data={
                "waterReuse": [],
                "etchingRecovery": [],
                "generalSolidUtil": [],
                "wastewaterCollection": [],
                "wasteGasTreatment": [],
                "generalSolidCollection": [],
                "hazardousWasteCollection": [],
                "noise": []
            }, msg="获取成功")
        
        return Success(data={
            "id": record.id,
            "waterReuse": record.water_reuse or [],
            "etchingRecovery": record.etching_recovery or [],
            "generalSolidUtil": record.general_solid_util or [],
            "wastewaterCollection": record.wastewater_collection or [],
            "wasteGasTreatment": record.waste_gas_treatment or [],
            "generalSolidCollection": record.general_solid_collection or [],
            "hazardousWasteCollection": record.hazardous_waste_collection or [],
            "noise": record.noise or []
        }, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业资源综合利用失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/resource-reutilization", summary="保存企业资源综合利用")
async def save_resource_reutilization(
    enterprise_id: int,
    data: Dict[str, Any] = Body(..., description="资源综合利用数据"),
    current_user=DependAuth
):
    """保存企业资源综合利用"""
    try:
        result = await resource_reutilization_controller.upsert(enterprise_id, data)
        
        return Success(data={
            "id": result.id,
            "waterReuse": result.water_reuse or [],
            "etchingRecovery": result.etching_recovery or [],
            "generalSolidUtil": result.general_solid_util or [],
            "wastewaterCollection": result.wastewater_collection or [],
            "wasteGasTreatment": result.waste_gas_treatment or [],
            "generalSolidCollection": result.general_solid_collection or [],
            "hazardousWasteCollection": result.hazardous_waste_collection or [],
            "noise": result.noise or []
        }, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业资源综合利用失败: {str(e)}"
        )

