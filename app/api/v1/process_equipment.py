"""
PCB企业工艺装备数据API路由
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.controllers.process_equipment import (
    equipment_record_controller,
    equipment_category_controller,
    equipment_data_controller
)
from app.schemas.process_equipment import (
    PCBEquipmentRecordCreate,
    PCBEquipmentRecordUpdate,
    PCBEquipmentRecordResponse,
    PCBEquipmentCategoryCreate,
    PCBEquipmentCategoryUpdate,
    PCBEquipmentCategoryResponse,
    PCBEquipmentDataRequest,
    PCBEquipmentDataResponse,
    PCBEquipmentSaveResponse
)
from app.core.dependency import DependAuth

router = APIRouter()


# ==================== 设备记录相关API ====================

@router.get("/enterprise/{enterprise_id}/equipment", response_model=List[PCBEquipmentRecordResponse])
async def get_equipment_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业设备记录列表"""
    try:
        records = await equipment_record_controller.get_by_enterprise(enterprise_id)
        
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
            detail=f"获取设备记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/equipment", response_model=PCBEquipmentRecordResponse)
async def create_equipment_record(
    enterprise_id: int,
    record_data: PCBEquipmentRecordCreate,
    current_user=DependAuth
):
    """创建设备记录"""
    try:
        record_data_dict = record_data.dict()
        record_data_dict['enterprise_id'] = enterprise_id
        record = await equipment_record_controller.create(record_data_dict)
        
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
            detail=f"创建设备记录失败: {str(e)}"
        )


@router.put("/equipment/{record_id}", response_model=PCBEquipmentRecordResponse)
async def update_equipment_record(
    record_id: int,
    record_data: PCBEquipmentRecordUpdate,
    current_user=DependAuth
):
    """更新设备记录"""
    try:
        record = await equipment_record_controller.update(record_id, record_data.dict(exclude_unset=True))
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
            detail=f"更新设备记录失败: {str(e)}"
        )


@router.delete("/equipment/{record_id}")
async def delete_equipment_record(
    record_id: int,
    current_user=DependAuth
):
    """删除设备记录"""
    try:
        await equipment_record_controller.remove(record_id)
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
            detail=f"删除设备记录失败: {str(e)}"
        )


# ==================== 设备分类相关API ====================

@router.get("/equipment-categories", response_model=List[PCBEquipmentCategoryResponse])
async def get_equipment_categories(current_user=DependAuth):
    """获取设备分类列表"""
    try:
        categories = await equipment_category_controller.get_all_categories()
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功",
                "data": categories
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取设备分类失败: {str(e)}"
        )


@router.post("/equipment-categories", response_model=PCBEquipmentCategoryResponse)
async def create_equipment_category(
    category_data: PCBEquipmentCategoryCreate,
    current_user=DependAuth
):
    """创建设备分类"""
    try:
        category = await equipment_category_controller.create(category_data.dict())
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "code": 201,
                "message": "创建成功",
                "data": category
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建设备分类失败: {str(e)}"
        )


# ==================== 批量操作API ====================

@router.get("/enterprise/{enterprise_id}/all-data", summary="获取所有设备数据")
async def get_all_equipment_data(enterprise_id: int, current_user=DependAuth):
    """获取企业所有设备数据"""
    try:
        data = await equipment_data_controller.get_all_data(enterprise_id)
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
            detail=f"获取所有设备数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/all-data", response_model=PCBEquipmentSaveResponse, summary="保存所有设备数据")
async def save_all_equipment_data(
    enterprise_id: int,
    data: PCBEquipmentDataRequest,
    current_user=DependAuth
):
    """保存企业所有设备数据"""
    try:
        result = await equipment_data_controller.save_all_data(enterprise_id, data)
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
            detail=f"保存所有设备数据失败: {str(e)}"
        )


@router.delete("/enterprise/{enterprise_id}/all-data", summary="删除所有设备数据")
async def delete_all_equipment_data(enterprise_id: int, current_user=DependAuth):
    """删除企业所有设备数据"""
    try:
        success = await equipment_data_controller.delete_all_data(enterprise_id)
        if success:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "code": 200,
                    "message": "所有设备数据删除成功"
                }
            )
        else:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="删除所有设备数据失败")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除所有设备数据失败: {str(e)}"
        )
