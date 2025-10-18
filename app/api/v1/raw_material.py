from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.controllers.raw_material import raw_material_controller
from app.schemas.raw_material import (
    RawMaterialCreate,
    RawMaterialUpdate,
    RawMaterialInDB,
    RawMaterialSearchResponse
)
from app.core.dependency import DependAuth

router = APIRouter()

@router.get("/materials", response_model=RawMaterialSearchResponse, summary="获取原辅材料列表")
async def get_raw_materials(
    keyword: str = Query(None, description="搜索关键词"),
    current_user=DependAuth
):
    """
    获取原辅材料列表，支持关键词搜索
    """
    materials = await raw_material_controller.get_materials_by_keyword(keyword)
    return RawMaterialSearchResponse(materials=materials)

@router.get("/materials/search", response_model=List[RawMaterialInDB], summary="搜索原辅材料")
async def search_raw_materials(
    q: str = Query(..., description="搜索关键词"),
    current_user=DependAuth
):
    """
    根据关键词搜索原辅材料，支持模糊匹配
    """
    materials = await raw_material_controller.get_materials_by_keyword(q)
    return materials

@router.get("/materials/{material_id}", response_model=RawMaterialInDB, summary="获取材料详情")
async def get_material_detail(
    material_id: int,
    current_user=DependAuth
):
    """
    获取指定材料的详细信息
    """
    material = await raw_material_controller.get_by_id(material_id)
    if not material:
        raise HTTPException(status_code=404, detail="材料不存在")
    return material


@router.post("/materials", response_model=RawMaterialInDB, summary="创建新材料")
async def create_raw_material(
    material: RawMaterialCreate,
    current_user=DependAuth
):
    """
    创建新的原辅材料
    """
    # 检查材料名称是否已存在
    existing = await raw_material_controller.get_material_by_name(material.name)
    if existing:
        raise HTTPException(status_code=400, detail="材料名称已存在")
    
    new_material = await raw_material_controller.create(material)
    return new_material

@router.put("/materials/{material_id}", response_model=RawMaterialInDB, summary="更新材料信息")
async def update_raw_material(
    material_id: int,
    material: RawMaterialUpdate,
    current_user=DependAuth
):
    """
    更新原辅材料信息
    """
    existing = await raw_material_controller.get_by_id(material_id)
    if not existing:
        raise HTTPException(status_code=404, detail="材料不存在")
    
    updated_material = await raw_material_controller.update(material_id, material)
    return updated_material

@router.delete("/materials/{material_id}", summary="删除材料")
async def delete_raw_material(
    material_id: int,
    current_user=DependAuth
):
    """
    删除原辅材料（软删除，设置为不启用）
    """
    existing = await raw_material_controller.get_by_id(material_id)
    if not existing:
        raise HTTPException(status_code=404, detail="材料不存在")
    
    # 软删除：设置为不启用
    await raw_material_controller.update(material_id, {"is_active": False})
    return {"message": "材料已删除"}
