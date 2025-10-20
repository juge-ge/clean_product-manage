"""
PCB企业资源能源消耗数据验证模式
用于API接口的数据验证和序列化
"""
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field


# ==================== 用水消耗相关Schema ====================

class PCBWaterConsumptionRecordBase(BaseModel):
    """用水消耗记录基础模式"""
    project: str = Field(..., description="项目名称", max_length=100)
    unit: str = Field(..., description="单位", max_length=20)
    
    # 年份数据
    amount_2020: Optional[Decimal] = Field(None, description="2020年用量", ge=0)
    amount_2021: Optional[Decimal] = Field(None, description="2021年用量", ge=0)
    amount_2022: Optional[Decimal] = Field(None, description="2022年用量", ge=0)
    amount_2023: Optional[Decimal] = Field(None, description="2023年用量", ge=0)
    amount_2024: Optional[Decimal] = Field(None, description="2024年用量", ge=0)
    
    # 其他信息
    water_type: Optional[str] = Field(None, description="用水类型", max_length=50)
    source: Optional[str] = Field(None, description="用水来源", max_length=200)
    remark: Optional[str] = Field(None, description="备注")


class PCBWaterConsumptionRecordCreate(PCBWaterConsumptionRecordBase):
    """创建用水消耗记录"""
    pass


class PCBWaterConsumptionRecordUpdate(BaseModel):
    """更新用水消耗记录"""
    project: Optional[str] = Field(None, description="项目名称", max_length=100)
    unit: Optional[str] = Field(None, description="单位", max_length=20)
    
    # 年份数据
    amount_2020: Optional[Decimal] = Field(None, description="2020年用量", ge=0)
    amount_2021: Optional[Decimal] = Field(None, description="2021年用量", ge=0)
    amount_2022: Optional[Decimal] = Field(None, description="2022年用量", ge=0)
    amount_2023: Optional[Decimal] = Field(None, description="2023年用量", ge=0)
    amount_2024: Optional[Decimal] = Field(None, description="2024年用量", ge=0)
    
    # 其他信息
    water_type: Optional[str] = Field(None, description="用水类型", max_length=50)
    source: Optional[str] = Field(None, description="用水来源", max_length=200)
    remark: Optional[str] = Field(None, description="备注")


class PCBWaterConsumptionRecordResponse(PCBWaterConsumptionRecordBase):
    """用水消耗记录响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 用电消耗相关Schema ====================

class PCBElectricityConsumptionRecordBase(BaseModel):
    """用电消耗记录基础模式"""
    project: str = Field(..., description="项目名称", max_length=100)
    unit: str = Field(..., description="单位", max_length=20)
    
    # 年份数据 - 支持年份范围选择
    amount_2020: Optional[Decimal] = Field(None, description="2020年用量", ge=0)
    amount_2021: Optional[Decimal] = Field(None, description="2021年用量", ge=0)
    amount_2022: Optional[Decimal] = Field(None, description="2022年用量", ge=0)
    amount_2023: Optional[Decimal] = Field(None, description="2023年用量", ge=0)
    amount_2024: Optional[Decimal] = Field(None, description="2024年用量", ge=0)
    
    # 其他信息
    electricity_type: Optional[str] = Field(None, description="用电类型", max_length=50)
    region: Optional[str] = Field(None, description="区域", max_length=100)
    remark: Optional[str] = Field(None, description="备注")


class PCBElectricityConsumptionRecordCreate(PCBElectricityConsumptionRecordBase):
    """创建用电消耗记录"""
    pass


class PCBElectricityConsumptionRecordUpdate(BaseModel):
    """更新用电消耗记录"""
    project: Optional[str] = Field(None, description="项目名称", max_length=100)
    unit: Optional[str] = Field(None, description="单位", max_length=20)
    
    # 年份数据
    amount_2020: Optional[Decimal] = Field(None, description="2020年用量", ge=0)
    amount_2021: Optional[Decimal] = Field(None, description="2021年用量", ge=0)
    amount_2022: Optional[Decimal] = Field(None, description="2022年用量", ge=0)
    amount_2023: Optional[Decimal] = Field(None, description="2023年用量", ge=0)
    amount_2024: Optional[Decimal] = Field(None, description="2024年用量", ge=0)
    
    # 其他信息
    electricity_type: Optional[str] = Field(None, description="用电类型", max_length=50)
    region: Optional[str] = Field(None, description="区域", max_length=100)
    remark: Optional[str] = Field(None, description="备注")


class PCBElectricityConsumptionRecordResponse(PCBElectricityConsumptionRecordBase):
    """用电消耗记录响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 天然气消耗相关Schema ====================

class PCBGasConsumptionRecordBase(BaseModel):
    """天然气消耗记录基础模式"""
    project: str = Field(..., description="项目名称", max_length=100)
    unit: str = Field(..., description="单位", max_length=20)
    
    # 年份数据
    amount_2020: Optional[Decimal] = Field(None, description="2020年用量", ge=0)
    amount_2021: Optional[Decimal] = Field(None, description="2021年用量", ge=0)
    amount_2022: Optional[Decimal] = Field(None, description="2022年用量", ge=0)
    amount_2023: Optional[Decimal] = Field(None, description="2023年用量", ge=0)
    amount_2024: Optional[Decimal] = Field(None, description="2024年用量", ge=0)
    
    # 其他信息
    gas_type: Optional[str] = Field(None, description="燃气类型", max_length=50)
    source: Optional[str] = Field(None, description="燃气来源", max_length=200)
    remark: Optional[str] = Field(None, description="备注")


class PCBGasConsumptionRecordCreate(PCBGasConsumptionRecordBase):
    """创建天然气消耗记录"""
    pass


class PCBGasConsumptionRecordUpdate(BaseModel):
    """更新天然气消耗记录"""
    project: Optional[str] = Field(None, description="项目名称", max_length=100)
    unit: Optional[str] = Field(None, description="单位", max_length=20)
    
    # 年份数据
    amount_2020: Optional[Decimal] = Field(None, description="2020年用量", ge=0)
    amount_2021: Optional[Decimal] = Field(None, description="2021年用量", ge=0)
    amount_2022: Optional[Decimal] = Field(None, description="2022年用量", ge=0)
    amount_2023: Optional[Decimal] = Field(None, description="2023年用量", ge=0)
    amount_2024: Optional[Decimal] = Field(None, description="2024年用量", ge=0)
    
    # 其他信息
    gas_type: Optional[str] = Field(None, description="燃气类型", max_length=50)
    source: Optional[str] = Field(None, description="燃气来源", max_length=200)
    remark: Optional[str] = Field(None, description="备注")


class PCBGasConsumptionRecordResponse(PCBGasConsumptionRecordBase):
    """天然气消耗记录响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 汇总数据相关Schema ====================

class PCBResourceConsumptionSummaryBase(BaseModel):
    """资源能源消耗汇总基础模式"""
    year: int = Field(..., description="年份", ge=2020, le=2030)
    
    # 用水汇总
    total_water_consumption: Optional[Decimal] = Field(None, description="总用水量", ge=0)
    production_water_consumption: Optional[Decimal] = Field(None, description="生产用水量", ge=0)
    domestic_water_consumption: Optional[Decimal] = Field(None, description="生活用水量", ge=0)
    water_reuse_rate: Optional[Decimal] = Field(None, description="水资源重复利用率(%)", ge=0, le=100)
    
    # 用电汇总
    total_electricity_consumption: Optional[Decimal] = Field(None, description="总用电量", ge=0)
    production_electricity_consumption: Optional[Decimal] = Field(None, description="生产用电量", ge=0)
    auxiliary_electricity_consumption: Optional[Decimal] = Field(None, description="辅助生产用电量", ge=0)
    office_electricity_consumption: Optional[Decimal] = Field(None, description="办公用电量", ge=0)
    
    # 天然气汇总
    total_gas_consumption: Optional[Decimal] = Field(None, description="总天然气用量", ge=0)
    production_gas_consumption: Optional[Decimal] = Field(None, description="生产用气量", ge=0)
    domestic_gas_consumption: Optional[Decimal] = Field(None, description="生活用气量", ge=0)
    
    # 计算指标
    water_consumption_per_unit: Optional[Decimal] = Field(None, description="单位产品水耗(m³/m²)", ge=0)
    electricity_consumption_per_unit: Optional[Decimal] = Field(None, description="单位产品电耗(kWh/m²)", ge=0)
    gas_consumption_per_unit: Optional[Decimal] = Field(None, description="单位产品气耗(m³/m²)", ge=0)


class PCBResourceConsumptionSummaryCreate(PCBResourceConsumptionSummaryBase):
    """创建资源能源消耗汇总"""
    pass


class PCBResourceConsumptionSummaryUpdate(BaseModel):
    """更新资源能源消耗汇总"""
    year: Optional[int] = Field(None, description="年份", ge=2020, le=2030)
    
    # 用水汇总
    total_water_consumption: Optional[Decimal] = Field(None, description="总用水量", ge=0)
    production_water_consumption: Optional[Decimal] = Field(None, description="生产用水量", ge=0)
    domestic_water_consumption: Optional[Decimal] = Field(None, description="生活用水量", ge=0)
    water_reuse_rate: Optional[Decimal] = Field(None, description="水资源重复利用率(%)", ge=0, le=100)
    
    # 用电汇总
    total_electricity_consumption: Optional[Decimal] = Field(None, description="总用电量", ge=0)
    production_electricity_consumption: Optional[Decimal] = Field(None, description="生产用电量", ge=0)
    auxiliary_electricity_consumption: Optional[Decimal] = Field(None, description="辅助生产用电量", ge=0)
    office_electricity_consumption: Optional[Decimal] = Field(None, description="办公用电量", ge=0)
    
    # 天然气汇总
    total_gas_consumption: Optional[Decimal] = Field(None, description="总天然气用量", ge=0)
    production_gas_consumption: Optional[Decimal] = Field(None, description="生产用气量", ge=0)
    domestic_gas_consumption: Optional[Decimal] = Field(None, description="生活用气量", ge=0)
    
    # 计算指标
    water_consumption_per_unit: Optional[Decimal] = Field(None, description="单位产品水耗(m³/m²)", ge=0)
    electricity_consumption_per_unit: Optional[Decimal] = Field(None, description="单位产品电耗(kWh/m²)", ge=0)
    gas_consumption_per_unit: Optional[Decimal] = Field(None, description="单位产品气耗(m³/m²)", ge=0)


class PCBResourceConsumptionSummaryResponse(PCBResourceConsumptionSummaryBase):
    """资源能源消耗汇总响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 批量操作相关Schema ====================

class PCBWaterConsumptionDataRequest(BaseModel):
    """用水消耗数据请求"""
    records: List[PCBWaterConsumptionRecordCreate] = Field(default_factory=list, description="用水记录数据")


class PCBElectricityConsumptionDataRequest(BaseModel):
    """用电消耗数据请求"""
    records: List[PCBElectricityConsumptionRecordCreate] = Field(default_factory=list, description="用电记录数据")


class PCBGasConsumptionDataRequest(BaseModel):
    """天然气消耗数据请求"""
    records: List[PCBGasConsumptionRecordCreate] = Field(default_factory=list, description="天然气记录数据")


class PCBResourceConsumptionDataRequest(BaseModel):
    """资源能源消耗数据请求"""
    water: PCBWaterConsumptionDataRequest = Field(default_factory=PCBWaterConsumptionDataRequest, description="用水数据")
    electricity: PCBElectricityConsumptionDataRequest = Field(default_factory=PCBElectricityConsumptionDataRequest, description="用电数据")
    gas: PCBGasConsumptionDataRequest = Field(default_factory=PCBGasConsumptionDataRequest, description="天然气数据")


class PCBResourceConsumptionDataResponse(BaseModel):
    """资源能源消耗数据响应"""
    water_records: List[PCBWaterConsumptionRecordResponse] = Field(default_factory=list, description="用水记录")
    electricity_records: List[PCBElectricityConsumptionRecordResponse] = Field(default_factory=list, description="用电记录")
    gas_records: List[PCBGasConsumptionRecordResponse] = Field(default_factory=list, description="天然气记录")
    summary: Optional[PCBResourceConsumptionSummaryResponse] = Field(None, description="汇总数据")


class PCBResourceConsumptionSaveResponse(BaseModel):
    """资源能源消耗保存响应"""
    success: bool = Field(True, description="保存是否成功")
    message: str = Field("保存成功", description="响应消息")
    data: Optional[Dict[str, Any]] = Field(None, description="保存的数据")
