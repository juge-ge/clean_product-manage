"""
PCB企业资源利用数据API路由
提供能源消耗、新鲜水耗、废水总量、废水中总铜浓度、废水中COD浓度、原/辅料消耗数据的增删改查接口
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from decimal import Decimal

from app.controllers.resource_utilization import (
    energy_consumption_controller,
    fresh_water_consumption_controller,
    wastewater_total_consumption_controller,
    wastewater_cu_consumption_controller,
    wastewater_cod_consumption_controller,
    raw_material_consumption_controller,
)
from app.schemas.base import Success
from app.core.dependency import DependAuth

router = APIRouter()


# ==================== 能源消耗相关API ====================

@router.get("/enterprise/{enterprise_id}/energy-consumption", summary="获取企业能源消耗数据")
async def get_energy_consumption(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业能源消耗数据"""
    try:
        records = await energy_consumption_controller.get_by_enterprise(enterprise_id)
        
        items = []
        for record in records:
            item = {
                "id": record.id,
                "type": record.type,
                "mainProduct": record.main_product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "electricity": float(record.electricity) if record.electricity else None,
                "unitConsumption": float(record.unit_consumption) if record.unit_consumption else None,
                "rating": record.rating,
            }
            items.append(item)
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业能源消耗数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/energy-consumption", summary="批量保存企业能源消耗数据")
async def batch_save_energy_consumption(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="能源消耗记录列表"),
    current_user=DependAuth
):
    """批量保存企业能源消耗数据"""
    try:
        results = await energy_consumption_controller.batch_upsert(enterprise_id, items)
        
        # 返回保存后的数据
        saved_records = await energy_consumption_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            saved_items.append({
                "id": record.id,
                "type": record.type,
                "mainProduct": record.main_product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "electricity": float(record.electricity) if record.electricity else None,
                "unitConsumption": float(record.unit_consumption) if record.unit_consumption else None,
                "rating": record.rating,
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存企业能源消耗数据失败: {str(e)}"
        )


# ==================== 新鲜水耗相关API ====================

@router.get("/enterprise/{enterprise_id}/fresh-water-consumption", summary="获取企业新鲜水耗数据")
async def get_fresh_water_consumption(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业新鲜水耗数据"""
    try:
        records = await fresh_water_consumption_controller.get_by_enterprise(enterprise_id)
        
        items = []
        for record in records:
            item = {
                "id": record.id,
                "product": record.product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "freshWater": float(record.fresh_water) if record.fresh_water else None,
                "unitFreshWater": float(record.unit_fresh_water) if record.unit_fresh_water else None,
                "rating": record.rating,
            }
            items.append(item)
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业新鲜水耗数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/fresh-water-consumption", summary="批量保存企业新鲜水耗数据")
async def batch_save_fresh_water_consumption(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="新鲜水耗记录列表"),
    current_user=DependAuth
):
    """批量保存企业新鲜水耗数据"""
    try:
        results = await fresh_water_consumption_controller.batch_upsert(enterprise_id, items)
        
        # 返回保存后的数据
        saved_records = await fresh_water_consumption_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            saved_items.append({
                "id": record.id,
                "product": record.product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "freshWater": float(record.fresh_water) if record.fresh_water else None,
                "unitFreshWater": float(record.unit_fresh_water) if record.unit_fresh_water else None,
                "rating": record.rating,
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存企业新鲜水耗数据失败: {str(e)}"
        )


# ==================== 废水总量相关API ====================

@router.get("/enterprise/{enterprise_id}/wastewater-total-consumption", summary="获取企业废水总量数据")
async def get_wastewater_total_consumption(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业废水总量数据"""
    try:
        records = await wastewater_total_consumption_controller.get_by_enterprise(enterprise_id)
        
        items = []
        for record in records:
            item = {
                "id": record.id,
                "product": record.product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "wastewaterTotal": float(record.wastewater_total) if record.wastewater_total else None,
                "unitWastewater": float(record.unit_wastewater) if record.unit_wastewater else None,
                "rating": record.rating,
            }
            items.append(item)
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业废水总量数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/wastewater-total-consumption", summary="批量保存企业废水总量数据")
async def batch_save_wastewater_total_consumption(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="废水总量记录列表"),
    current_user=DependAuth
):
    """批量保存企业废水总量数据"""
    try:
        results = await wastewater_total_consumption_controller.batch_upsert(enterprise_id, items)
        
        # 返回保存后的数据
        saved_records = await wastewater_total_consumption_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            saved_items.append({
                "id": record.id,
                "product": record.product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "wastewaterTotal": float(record.wastewater_total) if record.wastewater_total else None,
                "unitWastewater": float(record.unit_wastewater) if record.unit_wastewater else None,
                "rating": record.rating,
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存企业废水总量数据失败: {str(e)}"
        )


# ==================== 废水中总铜浓度相关API ====================

@router.get("/enterprise/{enterprise_id}/wastewater-cu-consumption", summary="获取企业废水中总铜浓度数据")
async def get_wastewater_cu_consumption(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业废水中总铜浓度数据"""
    try:
        records = await wastewater_cu_consumption_controller.get_by_enterprise(enterprise_id)
        
        items = []
        for record in records:
            item = {
                "id": record.id,
                "product": record.product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "wastewaterTotal": float(record.wastewater_total) if record.wastewater_total else None,
                "wastewaterCu": float(record.wastewater_cu) if record.wastewater_cu else None,
                "unitWastewaterCu": float(record.unit_cu) if record.unit_cu else None,
                "rating": record.rating,
            }
            items.append(item)
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业废水中总铜浓度数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/wastewater-cu-consumption", summary="批量保存企业废水中总铜浓度数据")
async def batch_save_wastewater_cu_consumption(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="废水中总铜浓度记录列表"),
    current_user=DependAuth
):
    """批量保存企业废水中总铜浓度数据"""
    try:
        results = await wastewater_cu_consumption_controller.batch_upsert(enterprise_id, items)
        
        # 返回保存后的数据
        saved_records = await wastewater_cu_consumption_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            saved_items.append({
                "id": record.id,
                "product": record.product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "wastewaterTotal": float(record.wastewater_total) if record.wastewater_total else None,
                "wastewaterCu": float(record.wastewater_cu) if record.wastewater_cu else None,
                "unitWastewaterCu": float(record.unit_cu) if record.unit_cu else None,
                "rating": record.rating,
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存企业废水中总铜浓度数据失败: {str(e)}"
        )


# ==================== 废水中COD浓度相关API ====================

@router.get("/enterprise/{enterprise_id}/wastewater-cod-consumption", summary="获取企业废水中COD浓度数据")
async def get_wastewater_cod_consumption(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业废水中COD浓度数据"""
    try:
        records = await wastewater_cod_consumption_controller.get_by_enterprise(enterprise_id)
        
        items = []
        for record in records:
            item = {
                "id": record.id,
                "product": record.product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "wastewaterTotal": float(record.wastewater_total) if record.wastewater_total else None,
                "wastewaterCOD": float(record.wastewater_cod) if record.wastewater_cod else None,
                "unitWastewaterCOD": float(record.unit_cod) if record.unit_cod else None,
                "rating": record.rating,
            }
            items.append(item)
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业废水中COD浓度数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/wastewater-cod-consumption", summary="批量保存企业废水中COD浓度数据")
async def batch_save_wastewater_cod_consumption(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="废水中COD浓度记录列表"),
    current_user=DependAuth
):
    """批量保存企业废水中COD浓度数据"""
    try:
        results = await wastewater_cod_consumption_controller.batch_upsert(enterprise_id, items)
        
        # 返回保存后的数据
        saved_records = await wastewater_cod_consumption_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            saved_items.append({
                "id": record.id,
                "product": record.product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "wastewaterTotal": float(record.wastewater_total) if record.wastewater_total else None,
                "wastewaterCOD": float(record.wastewater_cod) if record.wastewater_cod else None,
                "unitWastewaterCOD": float(record.unit_cod) if record.unit_cod else None,
                "rating": record.rating,
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存企业废水中COD浓度数据失败: {str(e)}"
        )


# ==================== 原/辅料消耗（覆铜板）相关API ====================

@router.get("/enterprise/{enterprise_id}/raw-material-consumption", summary="获取企业原/辅料消耗（覆铜板）数据")
async def get_raw_material_consumption(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业原/辅料消耗（覆铜板）数据"""
    try:
        records = await raw_material_consumption_controller.get_by_enterprise(enterprise_id)
        
        items = []
        for record in records:
            item = {
                "id": record.id,
                "type": record.type,
                "mainProduct": record.main_product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "cclConsumption": float(record.ccl_consumption) if record.ccl_consumption else None,
                "cclUtilization": float(record.ccl_utilization) if record.ccl_utilization else None,
                "rating": record.rating,
            }
            items.append(item)
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业原/辅料消耗数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/raw-material-consumption", summary="批量保存企业原/辅料消耗（覆铜板）数据")
async def batch_save_raw_material_consumption(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="原/辅料消耗记录列表"),
    current_user=DependAuth
):
    """批量保存企业原/辅料消耗（覆铜板）数据"""
    try:
        results = await raw_material_consumption_controller.batch_upsert(enterprise_id, items)
        
        # 返回保存后的数据
        saved_records = await raw_material_consumption_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            saved_items.append({
                "id": record.id,
                "type": record.type,
                "mainProduct": record.main_product,
                "layers": record.layers,
                "output": float(record.output) if record.output else None,
                "cclConsumption": float(record.ccl_consumption) if record.ccl_consumption else None,
                "cclUtilization": float(record.ccl_utilization) if record.ccl_utilization else None,
                "rating": record.rating,
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存企业原/辅料消耗数据失败: {str(e)}"
        )

