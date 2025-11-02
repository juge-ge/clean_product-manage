"""
PCB审核选项型数据验证模式
用于API接口的数据验证和序列化
"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ==================== 生产工艺与装备要求相关Schema ====================

class PCBProcessEquipmentRequirementBase(BaseModel):
    """生产工艺与装备要求基础模式"""
    basic_requirements: Optional[List[str]] = Field(None, description="基本要求")
    mechanical_facilities: Optional[List[str]] = Field(None, description="机械加工及辅助设施")
    printing_process: Optional[List[str]] = Field(None, description="线路与阻焊图形形成")
    cleaning: Optional[List[str]] = Field(None, description="板面清洗")
    etching: Optional[List[str]] = Field(None, description="蚀刻")
    plating: Optional[List[str]] = Field(None, description="电镀与化学镀")
    remark: Optional[str] = Field(None, description="备注")


class PCBProcessEquipmentRequirementCreate(PCBProcessEquipmentRequirementBase):
    """创建生产工艺与装备要求记录"""
    pass


class PCBProcessEquipmentRequirementUpdate(PCBProcessEquipmentRequirementBase):
    """更新生产工艺与装备要求记录"""
    pass


class PCBProcessEquipmentRequirementResponse(PCBProcessEquipmentRequirementBase):
    """生产工艺与装备要求响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 温室气体排放相关Schema ====================

class PCBGreenhouseGasEmissionBase(BaseModel):
    """温室气体排放基础模式"""
    carbon_management: Optional[List[str]] = Field(None, description="碳减排管理")
    emission_per_output: Optional[List[str]] = Field(None, description="单位产值碳排放量")
    emission_intensity: Optional[List[str]] = Field(None, description="碳排放强度")
    remark: Optional[str] = Field(None, description="备注")


class PCBGreenhouseGasEmissionCreate(PCBGreenhouseGasEmissionBase):
    """创建温室气体排放记录"""
    pass


class PCBGreenhouseGasEmissionUpdate(PCBGreenhouseGasEmissionBase):
    """更新温室气体排放记录"""
    pass


class PCBGreenhouseGasEmissionResponse(PCBGreenhouseGasEmissionBase):
    """温室气体排放响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 产品特征相关Schema ====================

class PCBProductCharacteristicsBase(BaseModel):
    """产品特征基础模式"""
    auxiliary_material: Optional[List[str]] = Field(None, description="使用无毒无害或低毒低害的生产辅助材料")
    packaging: Optional[List[str]] = Field(None, description="包装")
    hazardous_substance: Optional[List[str]] = Field(None, description="有害物质限制使用")
    product_performance: Optional[List[str]] = Field(None, description="产品性能")
    remark: Optional[str] = Field(None, description="备注")


class PCBProductCharacteristicsCreate(PCBProductCharacteristicsBase):
    """创建产品特征记录"""
    pass


class PCBProductCharacteristicsUpdate(PCBProductCharacteristicsBase):
    """更新产品特征记录"""
    pass


class PCBProductCharacteristicsResponse(PCBProductCharacteristicsBase):
    """产品特征响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 清洁生产管理相关Schema ====================

class PCBCleanProductionManagementBase(BaseModel):
    """清洁生产管理基础模式"""
    environmental_law: Optional[List[str]] = Field(None, description="环保法律法规执行情况")
    industrial_policy: Optional[List[str]] = Field(None, description="产业政策符合性")
    clean_production_management: Optional[List[str]] = Field(None, description="清洁生产管理")
    clean_production_audit: Optional[List[str]] = Field(None, description="清洁生产审核")
    energy_management: Optional[List[str]] = Field(None, description="节能管理")
    emission_monitoring: Optional[List[str]] = Field(None, description="污染物排放监测")
    chemical_management: Optional[List[str]] = Field(None, description="危险化学品管理")
    measurement_equipment: Optional[List[str]] = Field(None, description="计量器具配备情况")
    solid_waste_disposal: Optional[List[str]] = Field(None, description="固体废物处理处置")
    soil_pollution_risk: Optional[List[str]] = Field(None, description="土壤污染隐患排查")
    transport_mode: Optional[List[str]] = Field(None, description="运输方式")
    remark: Optional[str] = Field(None, description="备注")


class PCBCleanProductionManagementCreate(PCBCleanProductionManagementBase):
    """创建清洁生产管理记录"""
    pass


class PCBCleanProductionManagementUpdate(PCBCleanProductionManagementBase):
    """更新清洁生产管理记录"""
    pass


class PCBCleanProductionManagementResponse(PCBCleanProductionManagementBase):
    """清洁生产管理响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== 资源综合利用相关Schema ====================

class PCBResourceReutilizationBase(BaseModel):
    """资源综合利用基础模式"""
    water_reuse: Optional[List[str]] = Field(None, description="水资源重复利用率")
    etching_recovery: Optional[List[str]] = Field(None, description="蚀刻液回收率")
    general_solid_util: Optional[List[str]] = Field(None, description="一般工业固体废物综合利用率")
    wastewater_collection: Optional[List[str]] = Field(None, description="废水收集与处理")
    waste_gas_treatment: Optional[List[str]] = Field(None, description="废气收集与处理")
    general_solid_collection: Optional[List[str]] = Field(None, description="一般固体废物收集与处理")
    hazardous_waste_collection: Optional[List[str]] = Field(None, description="危险废物收集与处理")
    noise: Optional[List[str]] = Field(None, description="噪声")
    remark: Optional[str] = Field(None, description="备注")


class PCBResourceReutilizationCreate(PCBResourceReutilizationBase):
    """创建资源综合利用记录"""
    pass


class PCBResourceReutilizationUpdate(PCBResourceReutilizationBase):
    """更新资源综合利用记录"""
    pass


class PCBResourceReutilizationResponse(PCBResourceReutilizationBase):
    """资源综合利用响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

