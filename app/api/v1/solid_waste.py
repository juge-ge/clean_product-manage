"""
PCB企业固体废物管理数据API路由
提供固体废物记录数据的增删改查接口
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.controllers.solid_waste import (
    solid_waste_record_controller,
    solid_waste_category_controller,
    solid_waste_data_controller
)
from app.schemas.solid_waste import (
    PCBSolidWasteRecordCreate,
    PCBSolidWasteRecordUpdate,
    PCBSolidWasteRecordResponse,
    PCBSolidWasteCategoryCreate,
    PCBSolidWasteCategoryUpdate,
    PCBSolidWasteCategoryResponse,
    PCBSolidWasteDataRequest,
    PCBSolidWasteDataResponse,
    PCBSolidWasteSaveResponse
)
from app.core.dependency import DependAuth

router = APIRouter()


# ==================== 固体废物记录相关API ====================

@router.get("/enterprise/{enterprise_id}/solid-waste-records", response_model=List[PCBSolidWasteRecordResponse])
async def get_solid_waste_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业固体废物记录列表"""
    try:
        records = await solid_waste_record_controller.get_by_enterprise(enterprise_id)
        
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
            detail=f"获取固体废物记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/solid-waste-records", response_model=PCBSolidWasteRecordResponse)
async def create_solid_waste_record(
    enterprise_id: int,
    data: PCBSolidWasteRecordCreate,
    current_user=DependAuth
):
    """创建固体废物记录"""
    try:
        record = await solid_waste_record_controller.create({
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
            detail=f"创建固体废物记录失败: {str(e)}"
        )


@router.put("/solid-waste-records/{record_id}", response_model=PCBSolidWasteRecordResponse)
async def update_solid_waste_record(
    record_id: int,
    data: PCBSolidWasteRecordUpdate,
    current_user=DependAuth
):
    """更新固体废物记录"""
    try:
        record = await solid_waste_record_controller.update(record_id, data.dict(exclude_unset=True))
        
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
            detail=f"更新固体废物记录失败: {str(e)}"
        )


@router.delete("/solid-waste-records/{record_id}")
async def delete_solid_waste_record(
    record_id: int,
    current_user=DependAuth
):
    """删除固体废物记录"""
    try:
        await solid_waste_record_controller.remove(record_id)
        
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
            detail=f"删除固体废物记录失败: {str(e)}"
        )


# ==================== 固体废物分类相关API ====================

@router.get("/solid-waste-categories", response_model=List[PCBSolidWasteCategoryResponse])
async def get_solid_waste_categories(current_user=DependAuth):
    """获取固体废物分类列表"""
    try:
        categories = await solid_waste_category_controller.get_all()
        
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
            detail=f"获取固体废物分类失败: {str(e)}"
        )


@router.post("/solid-waste-categories", response_model=PCBSolidWasteCategoryResponse)
async def create_solid_waste_category(
    data: PCBSolidWasteCategoryCreate,
    current_user=DependAuth
):
    """创建固体废物分类"""
    try:
        category = await solid_waste_category_controller.create(data.dict())
        
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
            detail=f"创建固体废物分类失败: {str(e)}"
        )


@router.put("/solid-waste-categories/{category_id}", response_model=PCBSolidWasteCategoryResponse)
async def update_solid_waste_category(
    category_id: int,
    data: PCBSolidWasteCategoryUpdate,
    current_user=DependAuth
):
    """更新固体废物分类"""
    try:
        category = await solid_waste_category_controller.update(category_id, data.dict(exclude_unset=True))
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "更新成功",
                "data": category
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新固体废物分类失败: {str(e)}"
        )


@router.delete("/solid-waste-categories/{category_id}")
async def delete_solid_waste_category(
    category_id: int,
    current_user=DependAuth
):
    """删除固体废物分类"""
    try:
        await solid_waste_category_controller.remove(category_id)
        
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
            detail=f"删除固体废物分类失败: {str(e)}"
        )


# ==================== 固体废物数据汇总API ====================

@router.get("/enterprise/{enterprise_id}/all-data", summary="获取所有固体废物数据")
async def get_all_solid_waste_data(enterprise_id: int, current_user=DependAuth):
    """获取企业所有固体废物数据"""
    try:
        data = await solid_waste_data_controller.get_all_data(enterprise_id)
        
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
            detail=f"获取所有固体废物数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/all-data", response_model=PCBSolidWasteSaveResponse, summary="保存所有固体废物数据")
async def save_all_solid_waste_data(
    enterprise_id: int,
    data: PCBSolidWasteDataRequest,
    current_user=DependAuth
):
    """保存企业所有固体废物数据"""
    try:
        result = await solid_waste_data_controller.save_all_data(enterprise_id, data)
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
            detail=f"保存所有固体废物数据失败: {str(e)}"
        )


@router.delete("/enterprise/{enterprise_id}/all-data", summary="删除所有固体废物数据")
async def delete_all_solid_waste_data(enterprise_id: int, current_user=DependAuth):
    """删除企业所有固体废物数据"""
    try:
        result = await solid_waste_data_controller.delete_all_data(enterprise_id)
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
            detail=f"删除所有固体废物数据失败: {str(e)}"
        )
