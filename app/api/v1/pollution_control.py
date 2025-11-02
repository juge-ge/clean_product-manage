"""
PCB企业污染防治数据API路由
提供废水产生分析、废气产生情况数据的增删改查接口
"""
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status, Body
from fastapi.responses import JSONResponse

from app.controllers.pollution_control import (
    wastewater_analysis_controller,
    waste_gas_analysis_controller,
    wastewater_stat_record_controller,
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
    PCBPollutionControlSaveResponse,
    PCBWastewaterStatThreeYearsRequest,
)
from app.schemas.base import Success
from app.core.dependency import DependAuth

router = APIRouter()


# ==================== 废水产生分析相关API ====================

@router.get("/enterprise/{enterprise_id}/wastewater-analysis", summary="获取企业废水产生分析记录")
async def get_wastewater_analysis_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业废水产生分析记录列表"""
    try:
        records = await wastewater_analysis_controller.get_by_enterprise(enterprise_id)
        
        # 转换为字典列表
        records_list = []
        for record in records:
            records_list.append({
                "id": record.id,
                "category": record.category,
                "source": record.source,
                "pollutants": record.pollutants,
                "disposal": record.disposal
            })
        
        return Success(data=records_list, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
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

@router.get("/enterprise/{enterprise_id}/waste-gas-analysis", summary="获取企业废气产生情况记录")
async def get_waste_gas_analysis_records(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业废气产生情况记录列表"""
    try:
        records = await waste_gas_analysis_controller.get_by_enterprise(enterprise_id)
        
        # 转换为字典列表
        records_list = []
        for record in records:
            records_list.append({
                "id": record.id,
                "type": record.gas_type,
                "pollutants": record.pollutants,
                "location": record.location,
                "treatment": record.treatment
            })
        
        return Success(data=records_list, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
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


# ==================== 近三年废水情况统计相关API ====================

@router.get("/enterprise/{enterprise_id}/wastewater-stat/three-years", summary="获取企业近三年废水情况统计")
async def get_three_years_wastewater_stat(
    enterprise_id: int,
    year_range: str = Query(..., description="年份范围，如：2022-2024"),
    current_user=DependAuth
):
    """
    获取企业近三年废水情况统计数据
    """
    try:
        records = await wastewater_stat_record_controller.get_by_enterprise(enterprise_id)
        
        # 解析年份范围
        start_year, end_year = map(int, year_range.split('-'))
        
        # 转换为前端格式
        items = []
        for record in records:
            item = {
                "id": record.id,
                "project": record.project,
                "workshop": record.workshop,
                "unit": record.unit
            }
            # 添加年份数据
            for year in range(start_year, end_year + 1):
                year_key = f"amount_{year}"
                value = getattr(record, year_key, None)
                if value is not None:
                    item[year_key] = float(value)
                else:
                    item[year_key] = None
            
            items.append(item)
        
        return Success(data=items, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业近三年废水情况统计失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/wastewater-stat/three-years", summary="保存企业近三年废水情况统计")
async def save_three_years_wastewater_stat(
    enterprise_id: int,
    data: PCBWastewaterStatThreeYearsRequest,
    current_user=DependAuth
):
    """
    保存企业近三年废水情况统计数据
    """
    try:
        # 转换为字典
        items_dict = []
        for item in data.items:
            if hasattr(item, 'model_dump'):
                item_dict = item.model_dump(by_alias=True)
            else:
                item_dict = item.dict(by_alias=True)
            items_dict.append(item_dict)
        
        results = await wastewater_stat_record_controller.batch_upsert(enterprise_id, items_dict)
        
        # 保存后立即验证数据是否正确保存
        saved_records = await wastewater_stat_record_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        start_year, end_year = map(int, data.year_range.split('-'))
        for record in saved_records:
            item = {
                "id": record.id,
                "project": record.project,
                "workshop": record.workshop,
                "unit": record.unit
            }
            for year in range(start_year, end_year + 1):
                year_key = f"amount_{year}"
                value = getattr(record, year_key, None)
                if value is not None:
                    item[year_key] = float(value)
                else:
                    item[year_key] = None
            saved_items.append(item)
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业近三年废水情况统计失败: {str(e)}"
        )


# ==================== 批量操作API（废水分析、废气分析）====================

@router.post("/enterprise/{enterprise_id}/wastewater-analysis/batch", summary="批量保存废水产生分析")
async def batch_save_wastewater_analysis(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="废水分析记录列表"),
    current_user=DependAuth
):
    """
    批量保存废水产生分析记录
    """
    try:
        print(f"[DEBUG] 批量保存废水分析 - enterprise_id: {enterprise_id}, items数量: {len(items)}")
        print(f"[DEBUG] items类型: {type(items)}")
        print(f"[DEBUG] items内容: {items}")
        
        # 验证输入数据
        if not items:
            return Success(data={"count": 0, "saved_data": []}, msg="没有需要保存的数据")
        
        if not isinstance(items, list):
            raise ValueError(f"items必须是列表类型，当前类型: {type(items)}")
        
        # 预处理数据：确保所有字段都是字符串，None转换为空字符串
        processed_items = []
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                print(f"[WARN] 跳过第 {idx+1} 条记录：不是字典类型")
                continue
            
            processed_item = {
                "category": str(item.get("category", "")).strip() if item.get("category") is not None else "",
                "source": str(item.get("source", "")).strip() if item.get("source") is not None else "",
                "pollutants": str(item.get("pollutants", "")).strip() if item.get("pollutants") is not None else "",
                "disposal": str(item.get("disposal", "")).strip() if item.get("disposal") is not None else "",
            }
            
            # 验证必填字段
            if not processed_item["category"]:
                print(f"[WARN] 跳过第 {idx+1} 条记录：category为空")
                continue
            
            processed_items.append(processed_item)
        
        print(f"[DEBUG] 预处理后的items数量: {len(processed_items)}")
        print(f"[DEBUG] 预处理后的items内容: {processed_items}")
        
        if not processed_items:
            raise ValueError("没有有效的记录需要保存，请检查数据格式")
        
        results = await wastewater_analysis_controller.batch_upsert(enterprise_id, processed_items)
        
        print(f"[DEBUG] 保存成功，创建了 {len(results)} 条记录")
        
        # 返回保存后的数据
        saved_records = await wastewater_analysis_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            saved_items.append({
                "id": record.id,
                "category": record.category,
                "source": record.source,
                "pollutants": record.pollutants,
                "disposal": record.disposal
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except ValueError as e:
        # 业务逻辑错误，返回400
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"批量保存废水产生分析失败: {str(e)}"
        )
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"[ERROR] 批量保存废水产生分析异常详情:")
        print(error_traceback)
        print(f"[ERROR] 异常类型: {type(e).__name__}")
        print(f"[ERROR] 异常消息: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存废水产生分析失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/waste-gas-analysis/batch", summary="批量保存废气产生情况")
async def batch_save_waste_gas_analysis(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="废气分析记录列表"),
    current_user=DependAuth
):
    """
    批量保存废气产生情况记录
    """
    try:
        print(f"[DEBUG] 批量保存废气分析 - enterprise_id: {enterprise_id}, items数量: {len(items)}")
        print(f"[DEBUG] items类型: {type(items)}")
        print(f"[DEBUG] items内容: {items}")
        
        # 验证输入数据
        if not items:
            return Success(data={"count": 0, "saved_data": []}, msg="没有需要保存的数据")
        
        if not isinstance(items, list):
            raise ValueError(f"items必须是列表类型，当前类型: {type(items)}")
        
        # 预处理数据：确保所有字段都是字符串，None转换为空字符串
        processed_items = []
        for idx, item in enumerate(items):
            if not isinstance(item, dict):
                print(f"[WARN] 跳过第 {idx+1} 条记录：不是字典类型")
                continue
            
            processed_item = {
                "type": str(item.get("type", "")).strip() if item.get("type") is not None else "",
                "pollutants": str(item.get("pollutants", "")).strip() if item.get("pollutants") is not None else "",
                "location": str(item.get("location", "")).strip() if item.get("location") is not None else "",
                "treatment": str(item.get("treatment", "")).strip() if item.get("treatment") is not None else "",
            }
            
            # 验证必填字段
            if not processed_item["type"]:
                print(f"[WARN] 跳过第 {idx+1} 条记录：type为空")
                continue
            
            processed_items.append(processed_item)
        
        print(f"[DEBUG] 预处理后的items数量: {len(processed_items)}")
        print(f"[DEBUG] 预处理后的items内容: {processed_items}")
        
        if not processed_items:
            raise ValueError("没有有效的记录需要保存，请检查数据格式")
        
        results = await waste_gas_analysis_controller.batch_upsert(enterprise_id, processed_items)
        
        print(f"[DEBUG] 保存成功，创建了 {len(results)} 条记录")
        
        # 返回保存后的数据
        saved_records = await waste_gas_analysis_controller.get_by_enterprise(enterprise_id)
        saved_items = []
        for record in saved_records:
            saved_items.append({
                "id": record.id,
                "type": record.gas_type,
                "pollutants": record.pollutants,
                "location": record.location,
                "treatment": record.treatment
            })
        
        return Success(data={"count": len(results), "saved_data": saved_items}, msg="保存成功")
    except ValueError as e:
        # 业务逻辑错误，返回400
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"批量保存废气产生情况失败: {str(e)}"
        )
    except Exception as e:
        import traceback
        error_traceback = traceback.format_exc()
        print(f"[ERROR] 批量保存废气产生情况异常详情:")
        print(error_traceback)
        print(f"[ERROR] 异常类型: {type(e).__name__}")
        print(f"[ERROR] 异常消息: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量保存废气产生情况失败: {str(e)}"
        )
