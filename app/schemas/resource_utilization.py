"""
PCB企业资源利用数据验证模式
用于API接口的数据验证和序列化
"""
from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


# ==================== 能源消耗相关Schema ====================

class PCBEnergyConsumptionBase(BaseModel):
    """能源消耗基础模式"""
    type: str = Field(..., description="类型(rigid/flexible)", max_length=50)
    main_product: str = Field(..., description="主要产品", max_length=100)
    layers: int = Field(..., description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    electricity: Optional[Decimal] = Field(None, description="耗电量", ge=0)
    unit_consumption: Optional[Decimal] = Field(None, description="单位产品消耗量", ge=0)
    rating: Optional[str] = Field(None, description="评定等级(level1/level2/level3/none)", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBEnergyConsumptionCreate(PCBEnergyConsumptionBase):
    """创建能源消耗记录"""
    pass


class PCBEnergyConsumptionUpdate(BaseModel):
    """更新能源消耗记录"""
    type: Optional[str] = Field(None, description="类型", max_length=50)
    main_product: Optional[str] = Field(None, description="主要产品", max_length=100)
    layers: Optional[int] = Field(None, description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    electricity: Optional[Decimal] = Field(None, description="耗电量", ge=0)
    unit_consumption: Optional[Decimal] = Field(None, description="单位产品消耗量", ge=0)
    rating: Optional[str] = Field(None, description="评定等级", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBEnergyConsumptionResponse(PCBEnergyConsumptionBase):
    """能源消耗响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 新鲜水耗相关Schema ====================

class PCBFreshWaterConsumptionBase(BaseModel):
    """新鲜水耗基础模式"""
    product: str = Field(..., description="产品名称(single/double/multilayer/hdi)", max_length=50)
    layers: int = Field(..., description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    fresh_water: Optional[Decimal] = Field(None, description="新鲜水耗(m³)", ge=0)
    unit_fresh_water: Optional[Decimal] = Field(None, description="单位产品新鲜水耗(m³/m²)", ge=0)
    rating: Optional[str] = Field(None, description="评定等级(level1/level2/level3/none)", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBFreshWaterConsumptionCreate(PCBFreshWaterConsumptionBase):
    """创建新鲜水耗记录"""
    pass


class PCBFreshWaterConsumptionUpdate(BaseModel):
    """更新新鲜水耗记录"""
    product: Optional[str] = Field(None, description="产品名称", max_length=50)
    layers: Optional[int] = Field(None, description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    fresh_water: Optional[Decimal] = Field(None, description="新鲜水耗(m³)", ge=0)
    unit_fresh_water: Optional[Decimal] = Field(None, description="单位产品新鲜水耗(m³/m²)", ge=0)
    rating: Optional[str] = Field(None, description="评定等级", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBFreshWaterConsumptionResponse(PCBFreshWaterConsumptionBase):
    """新鲜水耗响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 废水总量相关Schema ====================

class PCBWastewaterTotalConsumptionBase(BaseModel):
    """废水总量基础模式"""
    product: str = Field(..., description="产品名称(single/double/multilayer/hdi)", max_length=50)
    layers: int = Field(..., description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    wastewater_total: Optional[Decimal] = Field(None, description="废水总量(m³)", ge=0)
    unit_wastewater: Optional[Decimal] = Field(None, description="单位产品废水量(m³/m²)", ge=0)
    rating: Optional[str] = Field(None, description="评定等级(level1/level2/level3/none)", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBWastewaterTotalConsumptionCreate(PCBWastewaterTotalConsumptionBase):
    """创建废水总量记录"""
    pass


class PCBWastewaterTotalConsumptionUpdate(BaseModel):
    """更新废水总量记录"""
    product: Optional[str] = Field(None, description="产品名称", max_length=50)
    layers: Optional[int] = Field(None, description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    wastewater_total: Optional[Decimal] = Field(None, description="废水总量(m³)", ge=0)
    unit_wastewater: Optional[Decimal] = Field(None, description="单位产品废水量(m³/m²)", ge=0)
    rating: Optional[str] = Field(None, description="评定等级", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBWastewaterTotalConsumptionResponse(PCBWastewaterTotalConsumptionBase):
    """废水总量响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 废水中总铜浓度相关Schema ====================

class PCBWastewaterCuConsumptionBase(BaseModel):
    """废水中总铜浓度基础模式"""
    product: str = Field(..., description="产品名称(single/double/multilayer/hdi)", max_length=50)
    layers: int = Field(..., description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    wastewater_total: Optional[Decimal] = Field(None, description="废水总量(m³)", ge=0)
    wastewater_cu: Optional[Decimal] = Field(None, description="废水中总铜浓度(g/m³)", ge=0)
    unit_cu: Optional[Decimal] = Field(None, description="单位产品废水铜产生量(g/m²)", ge=0)
    rating: Optional[str] = Field(None, description="评定等级(level1/level2/level3/none)", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBWastewaterCuConsumptionCreate(PCBWastewaterCuConsumptionBase):
    """创建废水中总铜浓度记录"""
    pass


class PCBWastewaterCuConsumptionUpdate(BaseModel):
    """更新废水中总铜浓度记录"""
    product: Optional[str] = Field(None, description="产品名称", max_length=50)
    layers: Optional[int] = Field(None, description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    wastewater_total: Optional[Decimal] = Field(None, description="废水总量(m³)", ge=0)
    wastewater_cu: Optional[Decimal] = Field(None, description="废水中总铜浓度(g/m³)", ge=0)
    unit_cu: Optional[Decimal] = Field(None, description="单位产品废水铜产生量(g/m²)", ge=0)
    rating: Optional[str] = Field(None, description="评定等级", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBWastewaterCuConsumptionResponse(PCBWastewaterCuConsumptionBase):
    """废水中总铜浓度响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 废水中COD浓度相关Schema ====================

class PCBWastewaterCODConsumptionBase(BaseModel):
    """废水中COD浓度基础模式"""
    product: str = Field(..., description="产品名称(single/double/multilayer/hdi)", max_length=50)
    layers: int = Field(..., description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    wastewater_total: Optional[Decimal] = Field(None, description="废水总量(m³)", ge=0)
    wastewater_cod: Optional[Decimal] = Field(None, description="废水中总COD浓度(g/m³)", ge=0)
    unit_cod: Optional[Decimal] = Field(None, description="单位产品COD产生量(g/m²)", ge=0)
    rating: Optional[str] = Field(None, description="评定等级(level1/level2/level3/none)", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBWastewaterCODConsumptionCreate(PCBWastewaterCODConsumptionBase):
    """创建废水中COD浓度记录"""
    pass


class PCBWastewaterCODConsumptionUpdate(BaseModel):
    """更新废水中COD浓度记录"""
    product: Optional[str] = Field(None, description="产品名称", max_length=50)
    layers: Optional[int] = Field(None, description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    wastewater_total: Optional[Decimal] = Field(None, description="废水总量(m³)", ge=0)
    wastewater_cod: Optional[Decimal] = Field(None, description="废水中总COD浓度(g/m³)", ge=0)
    unit_cod: Optional[Decimal] = Field(None, description="单位产品COD产生量(g/m²)", ge=0)
    rating: Optional[str] = Field(None, description="评定等级", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBWastewaterCODConsumptionResponse(PCBWastewaterCODConsumptionBase):
    """废水中COD浓度响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 原/辅料消耗（覆铜板）相关Schema ====================

class PCBRawMaterialConsumptionBase(BaseModel):
    """原/辅料消耗（覆铜板）基础模式"""
    type: str = Field(..., description="类型(rigid/flexible)", max_length=50)
    main_product: str = Field(..., description="主要产品", max_length=100)
    layers: int = Field(..., description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    ccl_consumption: Optional[Decimal] = Field(None, description="覆铜板消耗量(m²)", ge=0)
    ccl_utilization: Optional[Decimal] = Field(None, description="覆铜板利用率(%)", ge=0, le=100)
    rating: Optional[str] = Field(None, description="评定等级(level1/level2/level3/none)", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBRawMaterialConsumptionCreate(PCBRawMaterialConsumptionBase):
    """创建原/辅料消耗（覆铜板）记录"""
    pass


class PCBRawMaterialConsumptionUpdate(BaseModel):
    """更新原/辅料消耗（覆铜板）记录"""
    type: Optional[str] = Field(None, description="类型", max_length=50)
    main_product: Optional[str] = Field(None, description="主要产品", max_length=100)
    layers: Optional[int] = Field(None, description="层数", ge=1, le=30)
    output: Optional[Decimal] = Field(None, description="产量(m²)", ge=0)
    ccl_consumption: Optional[Decimal] = Field(None, description="覆铜板消耗量(m²)", ge=0)
    ccl_utilization: Optional[Decimal] = Field(None, description="覆铜板利用率(%)", ge=0, le=100)
    rating: Optional[str] = Field(None, description="评定等级", max_length=20)
    remark: Optional[str] = Field(None, description="备注")


class PCBRawMaterialConsumptionResponse(PCBRawMaterialConsumptionBase):
    """原/辅料消耗（覆铜板）响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

