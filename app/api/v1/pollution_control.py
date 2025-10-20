"""
PCB企业污染防治数据API路由
提供废水产生分析、废气产生情况数据的增删改查接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.controllers.pollution_control import (
    wastewater_analysis_controller,
    waste_gas_analysis_controller,
    pollution_control_data_controller
)
from app.schemas.pollution_control import (
    PCBWastewaterAnalysisCreate,
    PCBWastewaterAnalysisUpdate,
    PCBWastewaterAnalysisResponse,
    PCBWasteGasAnalysisCreate,
    PCBWasteGasAnalysisUpdate,
    PCBWasteGasAnalysisResponse,
    PCBPollutionControlDataRequest,
    PCBPollutionControlDataResponse,
    PCBPollutionControlSaveResponse
)
from app.core.dependency import DependAuth

router = APIRouter()


# ==================== 废水产生分析相关API ====================

@router.get("/enterprise/{enterprise_id}/wastewater-analysis", response_model=List[PCBWastewaterAnalysisResponse])
async def get_wastewater_analysis_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业废水产生分析记录列表"""
    try:
        records = await wastewater_analysis_controller.get_by_enterprise(enterprise_id)
        
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
            detail=f"获取废水产生分析记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/wastewater-analysis", response_model=PCBWastewaterAnalysisResponse)
async def create_wastewater_analysis_record(
    enterprise_id: int,
    data: PCBWastewaterAnalysisCreate,
    current_user=DependAuth
):
    """创建废水产生分析记录"""
    try:
        record = await wastewater_analysis_controller.create({
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
            detail=f"创建废水产生分析记录失败: {str(e)}"
        )


@router.put("/wastewater-analysis/{record_id}", response_model=PCBWastewaterAnalysisResponse)
async def update_wastewater_analysis_record(
    record_id: int,
    data: PCBWastewaterAnalysisUpdate,
    current_user=DependAuth
):
    """更新废水产生分析记录"""
    try:
        record = await wastewater_analysis_controller.update(record_id, data.dict(exclude_unset=True))
        
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
            detail=f"更新废水产生分析记录失败: {str(e)}"
        )


@router.delete("/wastewater-analysis/{record_id}")
async def delete_wastewater_analysis_record(
    record_id: int,
    current_user=DependAuth
):
    """删除废水产生分析记录"""
    try:
        await wastewater_analysis_controller.remove(record_id)
        
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
            detail=f"删除废水产生分析记录失败: {str(e)}"
        )


# ==================== 废气产生情况相关API ====================

@router.get("/enterprise/{enterprise_id}/waste-gas-analysis", response_model=List[PCBWasteGasAnalysisResponse])
async def get_waste_gas_analysis_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业废气产生情况记录列表"""
    try:
        records = await waste_gas_analysis_controller.get_by_enterprise(enterprise_id)
        
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
            detail=f"获取废气产生情况记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/waste-gas-analysis", response_model=PCBWasteGasAnalysisResponse)
async def create_waste_gas_analysis_record(
    enterprise_id: int,
    data: PCBWasteGasAnalysisCreate,
    current_user=DependAuth
):
    """创建废气产生情况记录"""
    try:
        record = await waste_gas_analysis_controller.create({
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
            detail=f"创建废气产生情况记录失败: {str(e)}"
        )


@router.put("/waste-gas-analysis/{record_id}", response_model=PCBWasteGasAnalysisResponse)
async def update_waste_gas_analysis_record(
    record_id: int,
    data: PCBWasteGasAnalysisUpdate,
    current_user=DependAuth
):
    """更新废气产生情况记录"""
    try:
        record = await waste_gas_analysis_controller.update(record_id, data.dict(exclude_unset=True))
        
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
            detail=f"更新废气产生情况记录失败: {str(e)}"
        )


@router.delete("/waste-gas-analysis/{record_id}")
async def delete_waste_gas_analysis_record(
    record_id: int,
    current_user=DependAuth
):
    """删除废气产生情况记录"""
    try:
        await waste_gas_analysis_controller.remove(record_id)
        
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
            detail=f"删除废气产生情况记录失败: {str(e)}"
        )


# ==================== 污染防治数据汇总API ====================

@router.get("/enterprise/{enterprise_id}/all-data", summary="获取所有污染防治数据")
async def get_all_pollution_control_data(enterprise_id: int, current_user=DependAuth):
    """获取企业所有污染防治数据"""
    try:
        data = await pollution_control_data_controller.get_all_data(enterprise_id)
        
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
            detail=f"获取所有污染防治数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/all-data", response_model=PCBPollutionControlSaveResponse, summary="保存所有污染防治数据")
async def save_all_pollution_control_data(
    enterprise_id: int,
    data: PCBPollutionControlDataRequest,
    current_user=DependAuth
):
    """保存企业所有污染防治数据"""
    try:
        result = await pollution_control_data_controller.save_all_data(enterprise_id, data)
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
            detail=f"保存所有污染防治数据失败: {str(e)}"
        )


@router.delete("/enterprise/{enterprise_id}/all-data", summary="删除所有污染防治数据")
async def delete_all_pollution_control_data(enterprise_id: int, current_user=DependAuth):
    """删除企业所有污染防治数据"""
    try:
        result = await pollution_control_data_controller.delete_all_data(enterprise_id)
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
            detail=f"删除所有污染防治数据失败: {str(e)}"
        )
