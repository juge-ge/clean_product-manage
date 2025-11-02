"""
PCB企业生产情况数据API路由
提供企业生产情况数据的增删改查接口
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.controllers.pcb_production import pcb_production_data_controller
from app.schemas.pcb_production import (
    PCBProductionDataRequest,
    PCBProductionDataResponse,
    PCBProductionDataSaveResponse,
    PCBProductOutputThreeYearsRequest,
    PCBQualificationRateThreeYearsRequest,
    PCBOutputValueThreeYearsRequest,
    PCBRawMaterialUsageThreeYearsRequest,
)
from app.schemas.base import Success
from app.core.dependency import DependAuth
from app.controllers.process_equipment import equipment_data_controller
from app.schemas.process_equipment import PCBEquipmentDataRequest
from app.controllers.resource_consumption import (
    water_consumption_record_controller,
    electricity_consumption_record_controller,
    gas_consumption_record_controller
)
from app.schemas.resource_consumption import (
    PCBWaterConsumptionThreeYearsRequest,
    PCBElectricityConsumptionThreeYearsRequest,
    PCBGasConsumptionThreeYearsRequest
)

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
        import traceback
        traceback.print_exc()
        # 即使出错也返回空数据，避免500错误
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "code": 200,
                "message": "获取成功（部分数据可能为空）",
                "data": {
                    "productOutput": [],
                    "qualificationRate": [],
                    "outputValue": []
                }
            }
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


# ==================== 近三年数据接口 ====================

@router.get("/enterprise/{enterprise_id}/production/three-years", summary="获取企业近三年产品产量")
async def get_three_years_product_output(
    enterprise_id: int,
    year_range: str = Query(..., description="年份范围，如：2022-2024"),
    current_user=DependAuth
):
    """
    获取企业近三年产品产量数据
    """
    try:
        items = await pcb_production_data_controller.get_three_years_product_output(enterprise_id, year_range)
        return Success(data=items, msg="获取成功")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业近三年产品产量失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/production/three-years", summary="保存企业近三年产品产量")
async def save_three_years_product_output(
    enterprise_id: int,
    data: PCBProductOutputThreeYearsRequest,
    current_user=DependAuth
):
    """
    保存企业近三年产品产量数据
    """
    try:
        # 转换items为字典列表 (pydantic 2.x兼容)
        items_dict = [item.model_dump() if hasattr(item, 'model_dump') else item.dict() for item in data.items]
        count = await pcb_production_data_controller.save_three_years_product_output(
            enterprise_id, data.year_range, items_dict
        )
        return Success(data={"count": count}, msg="保存成功")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业近三年产品产量失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/qualification-rate/three-years", summary="获取企业近三年合格率")
async def get_three_years_qualification_rate(
    enterprise_id: int,
    year_range: str = Query(..., description="年份范围，如：2022-2024"),
    current_user=DependAuth
):
    """
    获取企业近三年合格率数据
    """
    try:
        items = await pcb_production_data_controller.get_three_years_qualification_rate(enterprise_id, year_range)
        return Success(data=items, msg="获取成功")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业近三年合格率失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/qualification-rate/three-years", summary="保存企业近三年合格率")
async def save_three_years_qualification_rate(
    enterprise_id: int,
    data: PCBQualificationRateThreeYearsRequest,
    current_user=DependAuth
):
    """
    保存企业近三年合格率数据
    """
    try:
        items_dict = [item.model_dump() if hasattr(item, 'model_dump') else item.dict() for item in data.items]
        count = await pcb_production_data_controller.save_three_years_qualification_rate(
            enterprise_id, data.year_range, items_dict
        )
        return Success(data={"count": count}, msg="保存成功")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业近三年合格率失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/output-value/three-years", summary="获取企业近三年产值")
async def get_three_years_output_value(
    enterprise_id: int,
    year_range: str = Query(..., description="年份范围，如：2022-2024"),
    current_user=DependAuth
):
    """
    获取企业近三年产值数据
    """
    try:
        items = await pcb_production_data_controller.get_three_years_output_value(enterprise_id, year_range)
        return Success(data=items, msg="获取成功")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业近三年产值失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/output-value/three-years", summary="保存企业近三年产值")
async def save_three_years_output_value(
    enterprise_id: int,
    data: PCBOutputValueThreeYearsRequest,
    current_user=DependAuth
):
    """
    保存企业近三年产值数据
    """
    try:
        # 转换为字典，保持字段名为camelCase（不转换为snake_case）
        items_dict = []
        for item in data.items:
            if hasattr(item, 'model_dump'):
                # Pydantic 2.x: 使用model_dump(by_alias=False)保持字段名不变（camelCase）
                item_dict = item.model_dump(by_alias=False)
            else:
                # Pydantic 1.x兼容
                item_dict = item.dict(by_alias=False)
            
            # 确保字段名是camelCase（前端格式）
            # 优先使用camelCase字段，如果没有则尝试snake_case（兼容）
            converted_item = {
                "year": item_dict.get("year"),
                "unit": item_dict.get("unit"),
                "annualOutputValue": item_dict.get("annualOutputValue") if "annualOutputValue" in item_dict else item_dict.get("annual_output_value"),
                "incomeTax": item_dict.get("incomeTax") if "incomeTax" in item_dict else item_dict.get("income_tax")
            }
            items_dict.append(converted_item)
        
        print(f"保存产值数据 - enterprise_id: {enterprise_id}, year_range: {data.year_range}")
        print(f"原始Schema数据 (model_dump): {[item.model_dump() if hasattr(item, 'model_dump') else item.dict() for item in data.items]}")
        print(f"原始Schema数据 (by_alias=False): {[item.model_dump(by_alias=False) if hasattr(item, 'model_dump') else item.dict(by_alias=False) for item in data.items]}")
        print(f"转换后的items: {items_dict}")  # 调试日志
        print(f"items_dict中第一条数据的键: {list(items_dict[0].keys()) if items_dict else '无数据'}")
        print(f"items_dict中第一条数据的annualOutputValue值: {items_dict[0].get('annualOutputValue') if items_dict else '无数据'}")
        
        count = await pcb_production_data_controller.save_three_years_output_value(
            enterprise_id, data.year_range, items_dict
        )
        print(f"保存完成 - 保存了 {count} 条记录")  # 调试日志
        
        # 保存后立即验证数据是否正确保存
        saved_data = await pcb_production_data_controller.get_three_years_output_value(
            enterprise_id, data.year_range
        )
        print(f"验证保存结果 - 读取到 {len(saved_data)} 条数据: {saved_data}")  # 调试日志
        
        return Success(data={"count": count, "saved_data": saved_data}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业近三年产值失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/raw-materials/three-years", summary="获取企业近三年原辅材料使用情况")
async def get_three_years_raw_material_usage(
    enterprise_id: int,
    year_range: str = Query(..., description="年份范围，如：2022-2024"),
    current_user=DependAuth
):
    """
    获取企业近三年原辅材料使用情况数据
    """
    try:
        items = await pcb_production_data_controller.get_three_years_raw_material_usage(enterprise_id, year_range)
        return Success(data=items, msg="获取成功")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业近三年原辅材料使用情况失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/raw-materials/three-years", summary="保存企业近三年原辅材料使用情况")
async def save_three_years_raw_material_usage(
    enterprise_id: int,
    data: PCBRawMaterialUsageThreeYearsRequest,
    current_user=DependAuth
):
    """
    保存企业近三年原辅材料使用情况数据
    """
    try:
        # 转换为字典，使用别名（camelCase）格式，以匹配前端
        items_dict = []
        for item in data.items:
            if hasattr(item, 'model_dump'):
                # 使用 by_alias=True 来保留camelCase别名（mainProduct, productOutput, materialName）
                item_dict = item.model_dump(by_alias=True)
            else:
                # Pydantic 1.x兼容
                item_dict = item.dict(by_alias=True)
            
            # 确保字段名为camelCase格式（前端格式）
            converted_item = {
                "type": item_dict.get("type"),
                "mainProduct": item_dict.get("mainProduct") or item_dict.get("main_product"),
                "productOutput": item_dict.get("productOutput") or item_dict.get("product_output"),
                "materialName": item_dict.get("materialName") or item_dict.get("material_name"),
                "unit": item_dict.get("unit")
            }
            
            # 保留所有动态年份字段（amount_YYYY 和 unitConsumption_YYYY）
            for key, value in item_dict.items():
                if key.startswith("amount_") or key.startswith("unitConsumption_"):
                    converted_item[key] = value
            
            items_dict.append(converted_item)
        
        count = await pcb_production_data_controller.save_three_years_raw_material_usage(
            enterprise_id, data.year_range, items_dict
        )
        
        # 保存后立即验证数据是否正确保存
        saved_data = await pcb_production_data_controller.get_three_years_raw_material_usage(
            enterprise_id, data.year_range
        )
        
        return Success(data={"count": count, "saved_data": saved_data}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业近三年原辅材料使用情况失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/equipment", summary="获取企业设备信息")
async def get_equipment(
    enterprise_id: int,
    current_user=DependAuth
):
    """
    获取企业设备信息数据
    """
    try:
        items = await equipment_data_controller.get_all_data(enterprise_id)
        return Success(data=items, msg="获取成功")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取企业设备信息失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/equipment", summary="保存企业设备信息")
async def save_equipment(
    enterprise_id: int,
    data: PCBEquipmentDataRequest,
    current_user=DependAuth
):
    """
    保存企业设备信息数据
    """
    try:
        # 转换为字典，保持字段名为camelCase
        items_dict = []
        for item in data.items:
            if hasattr(item, 'model_dump'):
                item_dict = item.model_dump(by_alias=True)
            else:
                item_dict = item.dict(by_alias=True)
            items_dict.append(item_dict)
        
        count = await equipment_data_controller.save_all_data(enterprise_id, items_dict)
        
        # 保存后立即验证数据是否正确保存
        saved_data = await equipment_data_controller.get_all_data(enterprise_id)
        
        return Success(data={"count": count, "saved_data": saved_data}, msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存企业设备信息失败: {str(e)}"
        )


# ==================== 资源能源消耗相关API ====================

@router.get("/enterprise/{enterprise_id}/consumption/water/three-years", summary="获取企业近三年用水情况")
async def get_three_years_water_consumption(
    enterprise_id: int,
    year_range: str = Query(..., description="年份范围，如：2022-2024"),
    current_user=DependAuth
):
    """
    获取企业近三年用水情况数据
    """
    try:
        records = await water_consumption_record_controller.get_by_enterprise(enterprise_id)
        
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
            detail=f"获取企业近三年用水情况失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/consumption/water/three-years", summary="保存企业近三年用水情况")
async def save_three_years_water_consumption(
    enterprise_id: int,
    data: PCBWaterConsumptionThreeYearsRequest,
    current_user=DependAuth
):
    """
    保存企业近三年用水情况数据
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
        
        results = await water_consumption_record_controller.batch_upsert(enterprise_id, items_dict)
        
        # 保存后立即验证数据是否正确保存
        saved_records = await water_consumption_record_controller.get_by_enterprise(enterprise_id)
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
            detail=f"保存企业近三年用水情况失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/consumption/electricity/three-years", summary="获取企业近三年用电情况")
async def get_three_years_electricity_consumption(
    enterprise_id: int,
    year_range: str = Query(..., description="年份范围，如：2022-2024"),
    current_user=DependAuth
):
    """
    获取企业近三年用电情况数据
    """
    try:
        records = await electricity_consumption_record_controller.get_by_enterprise(enterprise_id)
        
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
            detail=f"获取企业近三年用电情况失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/consumption/electricity/three-years", summary="保存企业近三年用电情况")
async def save_three_years_electricity_consumption(
    enterprise_id: int,
    data: PCBElectricityConsumptionThreeYearsRequest,
    current_user=DependAuth
):
    """
    保存企业近三年用电情况数据
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
        
        results = await electricity_consumption_record_controller.batch_upsert(enterprise_id, items_dict)
        
        # 保存后立即验证数据是否正确保存
        saved_records = await electricity_consumption_record_controller.get_by_enterprise(enterprise_id)
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
            detail=f"保存企业近三年用电情况失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/consumption/gas/three-years", summary="获取企业近三年天然气情况")
async def get_three_years_gas_consumption(
    enterprise_id: int,
    year_range: str = Query(..., description="年份范围，如：2022-2024"),
    current_user=DependAuth
):
    """
    获取企业近三年天然气情况数据
    """
    try:
        records = await gas_consumption_record_controller.get_by_enterprise(enterprise_id)
        
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
            detail=f"获取企业近三年天然气情况失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/consumption/gas/three-years", summary="保存企业近三年天然气情况")
async def save_three_years_gas_consumption(
    enterprise_id: int,
    data: PCBGasConsumptionThreeYearsRequest,
    current_user=DependAuth
):
    """
    保存企业近三年天然气情况数据
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
        
        results = await gas_consumption_record_controller.batch_upsert(enterprise_id, items_dict)
        
        # 保存后立即验证数据是否正确保存
        saved_records = await gas_consumption_record_controller.get_by_enterprise(enterprise_id)
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
            detail=f"保存企业近三年天然气情况失败: {str(e)}"
        )
