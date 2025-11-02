"""
PCB企业工艺装备数据验证模式
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class PCBEquipmentRecordBase(BaseModel):
    """设备记录基础模式 - 支持前端camelCase字段名"""
    equipment_name: str = Field(..., alias="equipmentName", description="设备名称", max_length=100)
    equipment_model: str = Field(..., alias="equipmentModel", description="设备型号", max_length=200)
    motor_model: str = Field(..., alias="motorModel", description="电机型号", max_length=100)
    power: Optional[Decimal] = Field(None, alias="power", description="功率(KW)", ge=0)
    quantity: int = Field(1, alias="quantity", description="数量", ge=1)
    process: str = Field(..., alias="process", description="应用工艺", max_length=100)
    status: str = Field("良好", alias="status", description="运行状况", max_length=50)
    remark: Optional[str] = Field(None, alias="remark", description="备注")
    
    model_config = {"extra": "allow", "populate_by_name": True}  # Pydantic 2.x: 允许额外字段和字段名别名


class PCBEquipmentRecordCreate(PCBEquipmentRecordBase):
    """创建设备记录"""
    pass


class PCBEquipmentRecordUpdate(BaseModel):
    """更新设备记录"""
    equipment_name: Optional[str] = Field(None, description="设备名称", max_length=100)
    equipment_model: Optional[str] = Field(None, description="设备型号", max_length=200)
    motor_model: Optional[str] = Field(None, description="电机型号", max_length=100)
    power: Optional[Decimal] = Field(None, description="功率(KW)", ge=0)
    quantity: Optional[int] = Field(None, description="数量", ge=1)
    process: Optional[str] = Field(None, description="应用工艺", max_length=100)
    status: Optional[str] = Field(None, description="运行状况", max_length=50)
    remark: Optional[str] = Field(None, description="备注")


class PCBEquipmentRecordResponse(PCBEquipmentRecordBase):
    """设备记录响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PCBEquipmentItemResponse(BaseModel):
    """设备项响应 - 前端camelCase格式"""
    id: Optional[int] = None
    equipmentName: str = Field(..., description="设备名称")
    equipmentModel: str = Field(..., description="设备型号")
    motorModel: str = Field(..., description="电机型号")
    power: Optional[float] = Field(None, description="功率(KW)")
    quantity: int = Field(1, description="数量")
    process: str = Field(..., description="应用工艺")
    status: str = Field("良好", description="运行状况")
    remark: Optional[str] = Field(None, description="备注")
    
    model_config = {"extra": "allow"}


class PCBEquipmentCategoryBase(BaseModel):
    """设备分类基础模式"""
    name: str = Field(..., description="分类名称", max_length=100)
    description: Optional[str] = Field(None, description="分类描述")
    sort_order: int = Field(0, description="排序")


class PCBEquipmentCategoryCreate(PCBEquipmentCategoryBase):
    """创建设备分类"""
    pass


class PCBEquipmentCategoryUpdate(BaseModel):
    """更新设备分类"""
    name: Optional[str] = Field(None, description="分类名称", max_length=100)
    description: Optional[str] = Field(None, description="分类描述")
    sort_order: Optional[int] = Field(None, description="排序")


class PCBEquipmentCategoryResponse(PCBEquipmentCategoryBase):
    """设备分类响应"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 批量操作相关Schema
class PCBEquipmentItem(BaseModel):
    """设备项Schema - 支持前端camelCase字段名，允许空字段"""
    equipmentName: Optional[str] = Field(None, description="设备名称", max_length=100)
    equipmentModel: Optional[str] = Field(None, description="设备型号", max_length=200)
    motorModel: Optional[str] = Field(None, description="电机型号", max_length=100)
    power: Optional[float] = Field(None, description="功率(KW)", ge=0)
    quantity: Optional[int] = Field(1, description="数量", ge=1)
    process: Optional[str] = Field(None, description="应用工艺", max_length=100)
    status: Optional[str] = Field("良好", description="运行状况", max_length=50)
    remark: Optional[str] = Field(None, description="备注")
    
    model_config = {"extra": "allow", "populate_by_name": True}


class PCBEquipmentDataRequest(BaseModel):
    """设备数据请求"""
    items: List[PCBEquipmentItem] = Field(default_factory=list, description="设备记录列表")


class PCBEquipmentDataResponse(BaseModel):
    """设备数据响应"""
    equipment: List[PCBEquipmentRecordResponse] = Field(default_factory=list, description="设备记录")


class PCBEquipmentSaveResponse(BaseModel):
    """设备保存响应"""
    success: bool = Field(True, description="保存是否成功")
    message: str = Field("保存成功", description="响应消息")
    data: Optional[dict] = Field(None, description="保存的数据")
