"""
PCB企业自行监测数据API路由
提供有组织废气、无组织废气、废水、废气排放、噪声监测数据的增删改查接口
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from fastapi.responses import JSONResponse

from app.controllers.self_monitoring import (
    organized_gas_monitoring_controller,
    unorganized_gas_monitoring_controller,
    wastewater_monitoring_controller,
    gas_emission_monitoring_controller,
    noise_monitoring_controller,
    self_monitoring_data_controller
)
from app.schemas.self_monitoring import (
    PCBOrganizedGasMonitoringCreate,
    PCBOrganizedGasMonitoringUpdate,
    PCBOrganizedGasMonitoringResponse,
    PCBUnorganizedGasMonitoringCreate,
    PCBUnorganizedGasMonitoringUpdate,
    PCBUnorganizedGasMonitoringResponse,
    PCBWastewaterMonitoringCreate,
    PCBWastewaterMonitoringUpdate,
    PCBWastewaterMonitoringResponse,
    PCBGasEmissionMonitoringCreate,
    PCBGasEmissionMonitoringUpdate,
    PCBGasEmissionMonitoringResponse,
    PCBNoiseMonitoringCreate,
    PCBNoiseMonitoringUpdate,
    PCBNoiseMonitoringResponse,
    PCBSelfMonitoringDataRequest,
    PCBSelfMonitoringDataResponse,
    PCBSelfMonitoringSaveResponse
)
from app.core.dependency import DependAuth
from app.schemas.base import Success

router = APIRouter()


# ==================== 有组织废气检测相关API ====================

@router.get("/enterprise/{enterprise_id}/organized-gas-monitoring", response_model=List[PCBOrganizedGasMonitoringResponse])
async def get_organized_gas_monitoring_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业有组织废气检测记录列表"""
    try:
        records = await organized_gas_monitoring_controller.get_by_enterprise(enterprise_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功",
                "data": records
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取有组织废气检测记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/organized-gas-monitoring", response_model=PCBOrganizedGasMonitoringResponse)
async def create_organized_gas_monitoring_record(
    enterprise_id: int,
    data: PCBOrganizedGasMonitoringCreate,
    current_user=DependAuth
):
    """创建有组织废气检测记录"""
    try:
        record = await organized_gas_monitoring_controller.create({
            **data.dict(),
            "enterprise_id": enterprise_id
        })
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "code": 201,
                "message": "创建成功",
                "data": record
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建有组织废气检测记录失败: {str(e)}"
        )


@router.put("/organized-gas-monitoring/{record_id}", response_model=PCBOrganizedGasMonitoringResponse)
async def update_organized_gas_monitoring_record(
    record_id: int,
    data: PCBOrganizedGasMonitoringUpdate,
    current_user=DependAuth
):
    """更新有组织废气检测记录"""
    try:
        record = await organized_gas_monitoring_controller.update(record_id, data.dict(exclude_unset=True))
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "更新成功",
                "data": record
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新有组织废气检测记录失败: {str(e)}"
        )


@router.delete("/organized-gas-monitoring/{record_id}")
async def delete_organized_gas_monitoring_record(
    record_id: int,
    current_user=DependAuth
):
    """删除有组织废气检测记录"""
    try:
        await organized_gas_monitoring_controller.remove(record_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "删除成功"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除有组织废气检测记录失败: {str(e)}"
        )


# ==================== 无组织废气检测相关API ====================

@router.get("/enterprise/{enterprise_id}/unorganized-gas-monitoring", response_model=List[PCBUnorganizedGasMonitoringResponse])
async def get_unorganized_gas_monitoring_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业无组织废气检测记录列表"""
    try:
        records = await unorganized_gas_monitoring_controller.get_by_enterprise(enterprise_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功",
                "data": records
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取无组织废气检测记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/unorganized-gas-monitoring", response_model=PCBUnorganizedGasMonitoringResponse)
async def create_unorganized_gas_monitoring_record(
    enterprise_id: int,
    data: PCBUnorganizedGasMonitoringCreate,
    current_user=DependAuth
):
    """创建无组织废气检测记录"""
    try:
        record = await unorganized_gas_monitoring_controller.create({
            **data.dict(),
            "enterprise_id": enterprise_id
        })
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "code": 201,
                "message": "创建成功",
                "data": record
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建无组织废气检测记录失败: {str(e)}"
        )


@router.put("/unorganized-gas-monitoring/{record_id}", response_model=PCBUnorganizedGasMonitoringResponse)
async def update_unorganized_gas_monitoring_record(
    record_id: int,
    data: PCBUnorganizedGasMonitoringUpdate,
    current_user=DependAuth
):
    """更新无组织废气检测记录"""
    try:
        record = await unorganized_gas_monitoring_controller.update(record_id, data.dict(exclude_unset=True))
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "更新成功",
                "data": record
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新无组织废气检测记录失败: {str(e)}"
        )


@router.delete("/unorganized-gas-monitoring/{record_id}")
async def delete_unorganized_gas_monitoring_record(
    record_id: int,
    current_user=DependAuth
):
    """删除无组织废气检测记录"""
    try:
        await unorganized_gas_monitoring_controller.remove(record_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "删除成功"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除无组织废气检测记录失败: {str(e)}"
        )


# ==================== 废水排放监测相关API ====================

@router.get("/enterprise/{enterprise_id}/wastewater-monitoring", response_model=List[PCBWastewaterMonitoringResponse])
async def get_wastewater_monitoring_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业废水排放监测记录列表"""
    try:
        records = await wastewater_monitoring_controller.get_by_enterprise(enterprise_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功",
                "data": records
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取废水排放监测记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/wastewater-monitoring", response_model=PCBWastewaterMonitoringResponse)
async def create_wastewater_monitoring_record(
    enterprise_id: int,
    data: PCBWastewaterMonitoringCreate,
    current_user=DependAuth
):
    """创建废水排放监测记录"""
    try:
        record = await wastewater_monitoring_controller.create({
            **data.dict(),
            "enterprise_id": enterprise_id
        })
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "code": 201,
                "message": "创建成功",
                "data": record
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建废水排放监测记录失败: {str(e)}"
        )


@router.put("/wastewater-monitoring/{record_id}", response_model=PCBWastewaterMonitoringResponse)
async def update_wastewater_monitoring_record(
    record_id: int,
    data: PCBWastewaterMonitoringUpdate,
    current_user=DependAuth
):
    """更新废水排放监测记录"""
    try:
        record = await wastewater_monitoring_controller.update(record_id, data.dict(exclude_unset=True))
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "更新成功",
                "data": record
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新废水排放监测记录失败: {str(e)}"
        )


@router.delete("/wastewater-monitoring/{record_id}")
async def delete_wastewater_monitoring_record(
    record_id: int,
    current_user=DependAuth
):
    """删除废水排放监测记录"""
    try:
        await wastewater_monitoring_controller.remove(record_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "删除成功"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除废水排放监测记录失败: {str(e)}"
        )


# ==================== 废气排放监测相关API ====================

@router.get("/enterprise/{enterprise_id}/gas-emission-monitoring", response_model=List[PCBGasEmissionMonitoringResponse])
async def get_gas_emission_monitoring_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业废气排放监测记录列表"""
    try:
        records = await gas_emission_monitoring_controller.get_by_enterprise(enterprise_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功",
                "data": records
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取废气排放监测记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/gas-emission-monitoring", response_model=PCBGasEmissionMonitoringResponse)
async def create_gas_emission_monitoring_record(
    enterprise_id: int,
    data: PCBGasEmissionMonitoringCreate,
    current_user=DependAuth
):
    """创建废气排放监测记录"""
    try:
        record = await gas_emission_monitoring_controller.create({
            **data.dict(),
            "enterprise_id": enterprise_id
        })
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "code": 201,
                "message": "创建成功",
                "data": record
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建废气排放监测记录失败: {str(e)}"
        )


@router.put("/gas-emission-monitoring/{record_id}", response_model=PCBGasEmissionMonitoringResponse)
async def update_gas_emission_monitoring_record(
    record_id: int,
    data: PCBGasEmissionMonitoringUpdate,
    current_user=DependAuth
):
    """更新废气排放监测记录"""
    try:
        record = await gas_emission_monitoring_controller.update(record_id, data.dict(exclude_unset=True))
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "更新成功",
                "data": record
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新废气排放监测记录失败: {str(e)}"
        )


@router.delete("/gas-emission-monitoring/{record_id}")
async def delete_gas_emission_monitoring_record(
    record_id: int,
    current_user=DependAuth
):
    """删除废气排放监测记录"""
    try:
        await gas_emission_monitoring_controller.remove(record_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "删除成功"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除废气排放监测记录失败: {str(e)}"
        )


# ==================== 噪声监测相关API ====================

@router.get("/enterprise/{enterprise_id}/noise-monitoring", response_model=List[PCBNoiseMonitoringResponse])
async def get_noise_monitoring_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业噪声监测记录列表"""
    try:
        records = await noise_monitoring_controller.get_by_enterprise(enterprise_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功",
                "data": records
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取噪声监测记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/noise-monitoring", response_model=PCBNoiseMonitoringResponse)
async def create_noise_monitoring_record(
    enterprise_id: int,
    data: PCBNoiseMonitoringCreate,
    current_user=DependAuth
):
    """创建噪声监测记录"""
    try:
        record = await noise_monitoring_controller.create({
            **data.dict(),
            "enterprise_id": enterprise_id
        })
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "code": 201,
                "message": "创建成功",
                "data": record
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建噪声监测记录失败: {str(e)}"
        )


@router.put("/noise-monitoring/{record_id}", response_model=PCBNoiseMonitoringResponse)
async def update_noise_monitoring_record(
    record_id: int,
    data: PCBNoiseMonitoringUpdate,
    current_user=DependAuth
):
    """更新噪声监测记录"""
    try:
        record = await noise_monitoring_controller.update(record_id, data.dict(exclude_unset=True))
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "更新成功",
                "data": record
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新噪声监测记录失败: {str(e)}"
        )


@router.delete("/noise-monitoring/{record_id}")
async def delete_noise_monitoring_record(
    record_id: int,
    current_user=DependAuth
):
    """删除噪声监测记录"""
    try:
        await noise_monitoring_controller.remove(record_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "删除成功"
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除噪声监测记录失败: {str(e)}"
        )


# ==================== 批量保存API（各个表格独立）====================

@router.get("/enterprise/{enterprise_id}/organized-gas/batch", summary="获取有组织废气检测记录")
async def get_organized_gas_batch(
    enterprise_id: int,
    current_user=DependAuth
):
    """批量获取有组织废气检测记录"""
    try:
        records = await organized_gas_monitoring_controller.get_by_enterprise(enterprise_id)
        
        # 转换为前端格式
        items = []
        for record in records:
            item = {
                "id": record.id,
                "monitoringPoint": record.monitoring_point,
                "monitoringTime": record.monitoring_time,
            }
            # 转换监测项目字段
            monitoring_fields = {
                "result_氮氧化物": record.nitrogen_oxides,
                "result_氯化氢": record.hydrogen_chloride,
                "result_氰化氢": record.hydrogen_cyanide,
                "result_硫酸雾": record.sulfuric_acid_mist,
                "result_铬酸雾": record.chromic_acid_mist,
                "result_氟化物": record.fluoride,
                "result_酚类": record.phenol,
                "result_非甲烷总烃": record.non_methane_hydrocarbons,
                "result_苯": record.benzene,
                "result_甲苯": record.toluene,
                "result_二甲苯": record.xylene,
                "result_甲苯与二甲苯合计": record.toluene_xylene_total,
                "result_VOCs": record.vocs,
            }
            for key, value in monitoring_fields.items():
                if value is not None:
                    # 支持ND值：如果是ND字符串，保持字符串；否则尝试转换为数字
                    if str(value).upper() == 'ND':
                        item[key] = 'ND'
                    else:
                        try:
                            item[key] = float(value)
                        except (ValueError, TypeError):
                            item[key] = str(value)
                else:
                    item[key] = None
            
            items.append(item)
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取有组织废气检测记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/organized-gas/batch", summary="批量保存有组织废气检测记录")
async def batch_save_organized_gas(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="有组织废气检测记录列表"),
    current_user=DependAuth
):
    """批量保存有组织废气检测记录"""
    try:
        results = await organized_gas_monitoring_controller.batch_upsert(enterprise_id, items)
        
        # 返回保存后的数据
        saved_records = await organized_gas_monitoring_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            item = {
                "id": record.id,
                "monitoringPoint": record.monitoring_point,
                "monitoringTime": record.monitoring_time,
            }
            monitoring_fields = {
                "result_氮氧化物": record.nitrogen_oxides,
                "result_氯化氢": record.hydrogen_chloride,
                "result_氰化氢": record.hydrogen_cyanide,
                "result_硫酸雾": record.sulfuric_acid_mist,
                "result_铬酸雾": record.chromic_acid_mist,
                "result_氟化物": record.fluoride,
                "result_酚类": record.phenol,
                "result_非甲烷总烃": record.non_methane_hydrocarbons,
                "result_苯": record.benzene,
                "result_甲苯": record.toluene,
                "result_二甲苯": record.xylene,
                "result_甲苯与二甲苯合计": record.toluene_xylene_total,
                "result_VOCs": record.vocs,
            }
            for key, value in monitoring_fields.items():
                if value is not None:
                    # 支持ND值：如果是ND字符串，保持字符串；否则尝试转换为数字
                    if str(value).upper() == 'ND':
                        item[key] = 'ND'
                    else:
                        try:
                            item[key] = float(value)
                        except (ValueError, TypeError):
                            item[key] = str(value)
                else:
                    item[key] = None
            saved_items.append(item)
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存有组织废气检测记录失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/unorganized-gas/batch", summary="获取无组织废气检测记录")
async def get_unorganized_gas_batch(
    enterprise_id: int,
    current_user=DependAuth
):
    """批量获取无组织废气检测记录"""
    try:
        records = await unorganized_gas_monitoring_controller.get_by_enterprise(enterprise_id)
        
        items = []
        for record in records:
            # 处理排放浓度：支持ND值
            emission_concentration = record.emission_concentration
            if emission_concentration is not None:
                if str(emission_concentration).upper() == 'ND':
                    emission_concentration = 'ND'
                else:
                    try:
                        emission_concentration = float(emission_concentration)
                    except (ValueError, TypeError):
                        emission_concentration = str(emission_concentration)
            
            items.append({
                "id": record.id,
                "samplingTime": record.sampling_time,
                "samplingPoint": record.sampling_point,
                "monitoringFactor": record.monitoring_factor,
                "emissionConcentration": emission_concentration,
                "emissionLimit": float(record.emission_limit) if record.emission_limit is not None else None,
                "compliance": record.compliance
            })
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取无组织废气检测记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/unorganized-gas/batch", summary="批量保存无组织废气检测记录")
async def batch_save_unorganized_gas(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="无组织废气检测记录列表"),
    current_user=DependAuth
):
    """批量保存无组织废气检测记录"""
    try:
        results = await unorganized_gas_monitoring_controller.batch_upsert(enterprise_id, items)
        
        saved_records = await unorganized_gas_monitoring_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            # 处理排放浓度：支持ND值
            emission_concentration = record.emission_concentration
            if emission_concentration is not None:
                if str(emission_concentration).upper() == 'ND':
                    emission_concentration = 'ND'
                else:
                    try:
                        emission_concentration = float(emission_concentration)
                    except (ValueError, TypeError):
                        emission_concentration = str(emission_concentration)
            
            saved_items.append({
                "id": record.id,
                "samplingTime": record.sampling_time,
                "samplingPoint": record.sampling_point,
                "monitoringFactor": record.monitoring_factor,
                "emissionConcentration": emission_concentration,
                "emissionLimit": float(record.emission_limit) if record.emission_limit is not None else None,
                "compliance": record.compliance
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存无组织废气检测记录失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/wastewater/batch", summary="获取废水排放监测记录")
async def get_wastewater_batch(
    enterprise_id: int,
    current_user=DependAuth
):
    """批量获取废水排放监测记录"""
    try:
        records = await wastewater_monitoring_controller.get_by_enterprise(enterprise_id)
        
        items = []
        for record in records:
            item = {
                "id": record.id,
                "monitoringTime": record.sampling_date,
                "monitoringPoint": record.monitoring_point or "",
            }
            # 转换检测项目字段
            project_fields = {
                "result_pH": record.ph,
                "result_COD": record.cod,
                "result_氨氮": record.ammonia_nitrogen,
                "result_总氮": record.total_nitrogen,
                "result_总磷": record.total_phosphorus,
                "result_铜": record.total_copper,
                "result_镍": record.nickel,
                "result_总氰化物": record.total_cyanide,
                "result_镍（镍排口）": record.nickel_outlet,
            }
            for key, value in project_fields.items():
                if value is not None:
                    item[key] = float(value)
                else:
                    item[key] = None
            
            items.append(item)
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取废水排放监测记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/wastewater/batch", summary="批量保存废水排放监测记录")
async def batch_save_wastewater(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="废水排放监测记录列表"),
    current_user=DependAuth
):
    """批量保存废水排放监测记录"""
    try:
        results = await wastewater_monitoring_controller.batch_upsert(enterprise_id, items)
        
        saved_records = await wastewater_monitoring_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            item = {
                "id": record.id,
                "monitoringTime": record.sampling_date,
                "monitoringPoint": record.monitoring_point or "",
            }
            project_fields = {
                "result_pH": record.ph,
                "result_COD": record.cod,
                "result_氨氮": record.ammonia_nitrogen,
                "result_总氮": record.total_nitrogen,
                "result_总磷": record.total_phosphorus,
                "result_铜": record.total_copper,
                "result_镍": record.nickel,
                "result_总氰化物": record.total_cyanide,
                "result_镍（镍排口）": record.nickel_outlet,
            }
            for key, value in project_fields.items():
                if value is not None:
                    item[key] = float(value)
                else:
                    item[key] = None
            saved_items.append(item)
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存废水排放监测记录失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/gas-emission/batch", summary="获取废气排放监测记录")
async def get_gas_emission_batch(
    enterprise_id: int,
    current_user=DependAuth
):
    """批量获取废气排放监测记录"""
    try:
        records = await gas_emission_monitoring_controller.get_by_enterprise(enterprise_id)
        
        items = []
        for record in records:
            # 检测结果直接返回字符串，不进行类型转换，允许任意内容
            detection_result = getattr(record, 'detection_result', None)
            
            # 使用getattr安全访问字段，兼容旧数据
            items.append({
                "id": record.id,
                "detectionPoint": record.detection_point,
                "detectionItem": record.detection_item,
                "emissionRate": float(getattr(record, 'emission_rate', None)) if getattr(record, 'emission_rate', None) is not None else None,
                "benchmarkFlow": float(getattr(record, 'benchmark_flow', None)) if getattr(record, 'benchmark_flow', None) is not None else None,
                "detectionResult": detection_result,  # 直接返回字符串，不限制内容
                "permittedEmissionLimit": float(record.permitted_emission_limit) if record.permitted_emission_limit is not None else None,
                "stackHeight": float(record.stack_height) if record.stack_height is not None else None
            })
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取废气排放监测记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/gas-emission/batch", summary="批量保存废气排放监测记录")
async def batch_save_gas_emission(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="废气排放监测记录列表"),
    current_user=DependAuth
):
    """批量保存废气排放监测记录"""
    try:
        results = await gas_emission_monitoring_controller.batch_upsert(enterprise_id, items)
        
        saved_records = await gas_emission_monitoring_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            # 检测结果直接返回字符串，不进行类型转换，允许任意内容
            detection_result = getattr(record, 'detection_result', None)
            
            # 使用getattr安全访问字段，兼容旧数据
            saved_items.append({
                "id": record.id,
                "detectionPoint": record.detection_point,
                "detectionItem": record.detection_item,
                "emissionRate": float(getattr(record, 'emission_rate', None)) if getattr(record, 'emission_rate', None) is not None else None,
                "benchmarkFlow": float(getattr(record, 'benchmark_flow', None)) if getattr(record, 'benchmark_flow', None) is not None else None,
                "detectionResult": detection_result,  # 直接返回字符串，不限制内容
                "permittedEmissionLimit": float(record.permitted_emission_limit) if record.permitted_emission_limit is not None else None,
                "stackHeight": float(record.stack_height) if record.stack_height is not None else None
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存废气排放监测记录失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/noise/batch", summary="获取噪声监测记录")
async def get_noise_batch(
    enterprise_id: int,
    current_user=DependAuth
):
    """批量获取噪声监测记录"""
    try:
        records = await noise_monitoring_controller.get_by_enterprise(enterprise_id)
        
        items = []
        for record in records:
            items.append({
                "id": record.id,
                "monitoringTime": record.monitoring_time,
                "monitoringPoint": record.monitoring_point,
                "daytimeResult": float(record.daytime_result) if record.daytime_result is not None else None,
                "nighttimeResult": float(record.nighttime_result) if record.nighttime_result is not None else None,
                "daytimeStandard": float(record.daytime_standard) if record.daytime_standard is not None else None,
                "nighttimeStandard": float(record.nighttime_standard) if record.nighttime_standard is not None else None
            })
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取噪声监测记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/noise/batch", summary="批量保存噪声监测记录")
async def batch_save_noise(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="噪声监测记录列表"),
    current_user=DependAuth
):
    """批量保存噪声监测记录"""
    try:
        results = await noise_monitoring_controller.batch_upsert(enterprise_id, items)
        
        saved_records = await noise_monitoring_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            saved_items.append({
                "id": record.id,
                "monitoringTime": record.monitoring_time,
                "monitoringPoint": record.monitoring_point,
                "daytimeResult": float(record.daytime_result) if record.daytime_result is not None else None,
                "nighttimeResult": float(record.nighttime_result) if record.nighttime_result is not None else None,
                "daytimeStandard": float(record.daytime_standard) if record.daytime_standard is not None else None,
                "nighttimeStandard": float(record.nighttime_standard) if record.nighttime_standard is not None else None
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存噪声监测记录失败: {str(e)}"
        )


# ==================== 自行监测数据汇总API ====================

@router.get("/enterprise/{enterprise_id}/all-data", summary="获取所有自行监测数据")
async def get_all_self_monitoring_data(enterprise_id: int, current_user=DependAuth):
    """获取企业所有自行监测数据"""
    try:
        data = await self_monitoring_data_controller.get_all_data(enterprise_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功",
                "data": data
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取所有自行监测数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/all-data", response_model=PCBSelfMonitoringSaveResponse, summary="保存所有自行监测数据")
async def save_all_self_monitoring_data(
    enterprise_id: int,
    data: PCBSelfMonitoringDataRequest,
    current_user=DependAuth
):
    """保存企业所有自行监测数据"""
    try:
        result = await self_monitoring_data_controller.save_all_data(enterprise_id, data)
        if result['success']:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "code": 200,
                    "message": result['message'],
                    "data": result['data']
                }
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result['message'])
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存所有自行监测数据失败: {str(e)}"
        )


@router.delete("/enterprise/{enterprise_id}/all-data", summary="删除所有自行监测数据")
async def delete_all_self_monitoring_data(enterprise_id: int, current_user=DependAuth):
    """删除企业所有自行监测数据"""
    try:
        result = await self_monitoring_data_controller.delete_all_data(enterprise_id)
        if result['success']:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "code": 200,
                    "message": result['message']
                }
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=result['message'])
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除所有自行监测数据失败: {str(e)}"
        )
