"""
PCB企业生产情况数据API路由
提供企业生产情况数据的增删改查接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.controllers.pcb_production import pcb_production_data_controller
from app.schemas.pcb_production import (
    PCBProductionDataRequest,
    PCBProductionDataResponse,
    PCBProductionDataSaveResponse,
)
from app.core.dependency import DependAuth

router = APIRouter()


@router.get("/enterprise/{enterprise_id}/production-data")
async def get_production_data(
    enterprise_id: int,
    current_user=DependAuth
):
    """
    获取企业生产情况数据
    """
    try:
        data = await pcb_production_data_controller.get_all_production_data(enterprise_id)
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
            detail=f"获取企业生产情况数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/production-data", response_model=PCBProductionDataSaveResponse)
async def save_production_data(
    enterprise_id: int,
    data: PCBProductionDataRequest,
    current_user=DependAuth
):
    """
    保存企业生产情况数据
    """
    try:
        # 转换数据格式
        data_dict = {
            "productOutput": [item.dict() for item in data.productOutput],
            "qualificationRate": [item.dict() for item in data.qualificationRate],
            "outputValue": [item.dict() for item in data.outputValue]
        }
        
        result = await pcb_production_data_controller.save_all_production_data(enterprise_id, data_dict)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "保存成功",
                "data": result
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业生产情况数据失败: {str(e)}"
        )


@router.put("/enterprise/{enterprise_id}/production-data", response_model=PCBProductionDataSaveResponse)
async def update_production_data(
    enterprise_id: int,
    data: PCBProductionDataRequest,
    current_user=DependAuth
):
    """
    更新企业生产情况数据
    """
    try:
        # 转换数据格式
        data_dict = {
            "productOutput": [item.dict() for item in data.productOutput],
            "qualificationRate": [item.dict() for item in data.qualificationRate],
            "outputValue": [item.dict() for item in data.outputValue]
        }
        
        result = await pcb_production_data_controller.save_all_production_data(enterprise_id, data_dict)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "更新成功",
                "data": result
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新企业生产情况数据失败: {str(e)}"
        )


@router.delete("/enterprise/{enterprise_id}/production-data")
async def delete_production_data(
    enterprise_id: int,
    current_user=DependAuth
):
    """
    删除企业生产情况数据
    """
    try:
        # 删除所有生产情况数据
        product_output_count = await pcb_production_data_controller.product_output_controller.delete_by_enterprise(enterprise_id)
        qualification_rate_count = await pcb_production_data_controller.qualification_rate_controller.delete_by_enterprise(enterprise_id)
        output_value_count = await pcb_production_data_controller.output_value_controller.delete_by_enterprise(enterprise_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "删除成功",
                "data": {
                    "productOutput": product_output_count,
                    "qualificationRate": qualification_rate_count,
                    "outputValue": output_value_count
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除企业生产情况数据失败: {str(e)}"
        )
