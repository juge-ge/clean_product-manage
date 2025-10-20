"""
PCB企业自行监测数据API路由
提供有组织废气、无组织废气、废水、废气排放、噪声监测数据的增删改查接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
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
