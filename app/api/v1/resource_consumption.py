"""
PCB企业资源能源消耗数据API路由
提供用水、用电、天然气消耗数据的增删改查接口
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import JSONResponse

from app.controllers.resource_consumption import (
    water_consumption_record_controller,
    electricity_consumption_record_controller,
    gas_consumption_record_controller,
    resource_consumption_summary_controller,
    resource_consumption_data_controller
)
from app.schemas.resource_consumption import (
    PCBWaterConsumptionRecordCreate,
    PCBWaterConsumptionRecordUpdate,
    PCBWaterConsumptionRecordResponse,
    PCBElectricityConsumptionRecordCreate,
    PCBElectricityConsumptionRecordUpdate,
    PCBElectricityConsumptionRecordResponse,
    PCBGasConsumptionRecordCreate,
    PCBGasConsumptionRecordUpdate,
    PCBGasConsumptionRecordResponse,
    PCBResourceConsumptionSummaryCreate,
    PCBResourceConsumptionSummaryUpdate,
    PCBResourceConsumptionSummaryResponse,
    PCBResourceConsumptionDataRequest,
    PCBResourceConsumptionDataResponse,
    PCBResourceConsumptionSaveResponse
)
from app.core.dependency import DependAuth

router = APIRouter()


# ==================== 用水消耗相关API ====================



@router.get("/enterprise/{enterprise_id}/water-records")
async def get_water_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业用水记录列表"""
    try:
        records = await water_consumption_record_controller.get_by_enterprise(enterprise_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功",
                "data": records
            }
        )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用水记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/water-records", response_model=PCBWaterConsumptionRecordResponse)
async def create_water_record(
    enterprise_id: int,
    record_data: PCBWaterConsumptionRecordCreate,
    current_user=DependAuth
):
    """创建用水记录"""
    try:
        record_data_dict = record_data.dict()
        record_data_dict['enterprise_id'] = enterprise_id
        record = await water_consumption_record_controller.create(record_data_dict)
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
            detail=f"创建用水记录失败: {str(e)}"
        )


# ==================== 用电消耗相关API ====================

@router.get("/enterprise/{enterprise_id}/electricity-records")
async def get_electricity_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业用电记录列表"""
    try:
        records = await electricity_consumption_record_controller.get_by_enterprise(enterprise_id)
        
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
            detail=f"获取用电记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/electricity-records", response_model=PCBElectricityConsumptionRecordResponse)
async def create_electricity_record(
    enterprise_id: int,
    record_data: PCBElectricityConsumptionRecordCreate,
    current_user=DependAuth
):
    """创建用电记录"""
    try:
        record_data_dict = record_data.dict()
        record_data_dict['enterprise_id'] = enterprise_id
        record = await electricity_consumption_record_controller.create(record_data_dict)
        
        
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
            detail=f"创建用电记录失败: {str(e)}"
        )


@router.put("/electricity-records/{record_id}", response_model=PCBElectricityConsumptionRecordResponse)
async def update_electricity_record(
    record_id: int,
    record_data: PCBElectricityConsumptionRecordUpdate,
    current_user=DependAuth
):
    """更新用电记录"""
    try:
        record = await electricity_consumption_record_controller.update(record_id, record_data.dict(exclude_unset=True))
        
        
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
            detail=f"更新用电记录失败: {str(e)}"
        )


# ==================== 天然气消耗相关API ====================

@router.get("/enterprise/{enterprise_id}/gas-records")
async def get_gas_records(
    enterprise_id: int,
    start_year: Optional[int] = Query(None, description="开始年份"),
    end_year: Optional[int] = Query(None, description="结束年份"),
    current_user=DependAuth
):
    """获取企业天然气记录列表"""
    try:
        if start_year and end_year:
            records = await gas_consumption_record_controller.get_by_year_range(enterprise_id, start_year, end_year)
        else:
            records = await gas_consumption_record_controller.get_by_enterprise(enterprise_id)
        
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
            detail=f"获取天然气记录失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/gas-records", response_model=PCBGasConsumptionRecordResponse)
async def create_gas_record(
    enterprise_id: int,
    record_data: PCBGasConsumptionRecordCreate,
    current_user=DependAuth
):
    """创建天然气记录"""
    try:
        record_data_dict = record_data.dict()
        record_data_dict['enterprise_id'] = enterprise_id
        record = await gas_consumption_record_controller.create(record_data_dict)
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
            detail=f"创建天然气记录失败: {str(e)}"
        )


@router.put("/gas-records/{record_id}", response_model=PCBGasConsumptionRecordResponse)
async def update_gas_record(
    record_id: int,
    record_data: PCBGasConsumptionRecordUpdate,
    current_user=DependAuth
):
    """更新天然气记录"""
    try:
        record = await gas_consumption_record_controller.update(record_id, record_data.dict(exclude_unset=True))
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
            detail=f"更新天然气记录失败: {str(e)}"
        )


@router.delete("/gas-records/{record_id}")
async def delete_gas_record(
    record_id: int,
    current_user=DependAuth
):
    """删除天然气记录"""
    try:
        await gas_consumption_record_controller.remove(record_id)
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
            detail=f"删除天然气记录失败: {str(e)}"
        )


# ==================== 汇总数据相关API ====================

@router.get("/enterprise/{enterprise_id}/summary", response_model=List[PCBResourceConsumptionSummaryResponse])
async def get_resource_consumption_summary(
    enterprise_id: int,
    year: Optional[int] = Query(None, description="年份"),
    current_user=DependAuth
):
    """获取企业资源能源消耗汇总数据"""
    try:
        if year:
            summary = await resource_consumption_summary_controller.get_by_year(enterprise_id, year)
            summaries = [summary] if summary else []
        else:
            summaries = await resource_consumption_summary_controller.get_by_enterprise(enterprise_id)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功",
                "data": summaries
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取汇总数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/summary/calculate")
async def calculate_resource_consumption_summary(
    enterprise_id: int,
    year: int,
    current_user=DependAuth
):
    """计算企业资源能源消耗汇总数据"""
    try:
        summary = await resource_consumption_summary_controller.calculate_summary(enterprise_id, year)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "计算成功",
                "data": summary
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"计算汇总数据失败: {str(e)}"
        )


# ==================== 批量操作API ====================

@router.get("/enterprise/{enterprise_id}/all-data")
async def get_all_resource_consumption_data(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业的所有资源能源消耗数据"""
    try:
        # 获取用水记录
        water_records = await water_consumption_record_controller.get_by_enterprise(enterprise_id)
        
        # 获取用电记录
        electricity_records = await electricity_consumption_record_controller.get_by_enterprise(enterprise_id)
        
        # 获取天然气记录
        gas_records = await gas_consumption_record_controller.get_by_enterprise(enterprise_id)
        
        # 转换为字典列表
        water_data = [await record.to_dict() for record in water_records]
        electricity_data = [await record.to_dict() for record in electricity_records]
        gas_data = [await record.to_dict() for record in gas_records]
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功",
                "data": {
                    "water": water_data,
                    "electricity": electricity_data,
                    "gas": gas_data
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取数据失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/all-data", response_model=PCBResourceConsumptionSaveResponse)
async def save_all_resource_consumption_data(
    enterprise_id: int,
    data: PCBResourceConsumptionDataRequest,
    current_user=DependAuth
):
    """保存企业的所有资源能源消耗数据"""
    try:
        result = await resource_consumption_data_controller.save_all_data(enterprise_id, data)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": result['message'],
                "data": result['data']
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存数据失败: {str(e)}"
        )


@router.delete("/enterprise/{enterprise_id}/all-data")
async def delete_all_resource_consumption_data(
    enterprise_id: int,
    current_user=DependAuth
):
    """删除企业的所有资源能源消耗数据"""
    try:
        success = await resource_consumption_data_controller.delete_all_data(enterprise_id)
        if success:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={
                    "code": 200,
                    "message": "删除成功"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="删除数据失败"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除数据失败: {str(e)}"
        )
