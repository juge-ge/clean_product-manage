"""
PCB企业固体废物管理数据验证模式
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class PCBSolidWasteRecordBase(BaseModel):
    """固体废物记录基础模式"""
    category: str = Field(..., description="类别", max_length=50)
    name: str = Field(..., description="名称", max_length=100)
    unit: str = Field(..., description="单位", max_length=20)
    
    # 年份数据
    amount_2020: Optional[Decimal] = Field(None, description="2020年用量", ge=0)
    amount_2021: Optional[Decimal] = Field(None, description="2021年用量", ge=0)
    amount_2022: Optional[Decimal] = Field(None, description="2022年用量", ge=0)
    amount_2023: Optional[Decimal] = Field(None, description="2023年用量", ge=0)
    amount_2024: Optional[Decimal] = Field(None, description="2024年用量", ge=0)
    
    # 处置信息
    disposal_method: Optional[str] = Field(None, description="处置方式", max_length=200)
    remark: Optional[str] = Field(None, description="备注")


class PCBSolidWasteRecordCreate(PCBSolidWasteRecordBase):
    """创建固体废物记录"""
    pass


class PCBSolidWasteRecordUpdate(BaseModel):
    """更新固体废物记录"""
    category: Optional[str] = Field(None, description="类别", max_length=50)
    name: Optional[str] = Field(None, description="名称", max_length=100)
    unit: Optional[str] = Field(None, description="单位", max_length=20)
    
    # 年份数据
    amount_2020: Optional[Decimal] = Field(None, description="2020年用量", ge=0)
    amount_2021: Optional[Decimal] = Field(None, description="2021年用量", ge=0)
    amount_2022: Optional[Decimal] = Field(None, description="2022年用量", ge=0)
    amount_2023: Optional[Decimal] = Field(None, description="2023年用量", ge=0)
    amount_2024: Optional[Decimal] = Field(None, description="2024年用量", ge=0)
    
    # 处置信息
    disposal_method: Optional[str] = Field(None, description="处置方式", max_length=200)
    remark: Optional[str] = Field(None, description="备注")


class PCBSolidWasteRecordResponse(PCBSolidWasteRecordBase):
    """固体废物记录响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PCBSolidWasteCategoryBase(BaseModel):
    """固体废物分类基础模式"""
    name: str = Field(..., description="分类名称", max_length=50)
    description: Optional[str] = Field(None, description="分类描述")
    sort_order: int = Field(0, description="排序")


class PCBSolidWasteCategoryCreate(PCBSolidWasteCategoryBase):
    """创建固体废物分类"""
    pass


class PCBSolidWasteCategoryUpdate(BaseModel):
    """更新固体废物分类"""
    name: Optional[str] = Field(None, description="分类名称", max_length=50)
    description: Optional[str] = Field(None, description="分类描述")
    sort_order: Optional[int] = Field(None, description="排序")


class PCBSolidWasteCategoryResponse(PCBSolidWasteCategoryBase):
    """固体废物分类响应"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 批量操作相关Schema
class PCBSolidWasteDataRequest(BaseModel):
    """固体废物数据请求"""
    waste: List[PCBSolidWasteRecordCreate] = Field(default_factory=list, description="固体废物记录数据")


class PCBSolidWasteDataResponse(BaseModel):
    """固体废物数据响应"""
    waste: List[PCBSolidWasteRecordResponse] = Field(default_factory=list, description="固体废物记录")


class PCBSolidWasteSaveResponse(BaseModel):
    """固体废物保存响应"""
    success: bool = Field(True, description="保存是否成功")
    message: str = Field("保存成功", description="响应消息")
    data: Optional[dict] = Field(None, description="保存的数据")
