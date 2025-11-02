"""
PCB企业自行监测数据验证模式
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class PCBOrganizedGasMonitoringBase(BaseModel):
    """有组织废气检测基础模式"""
    monitoring_point: str = Field(..., description="监测点位", max_length=100)
    monitoring_time: str = Field(..., description="监测时间", max_length=50)
    
    # 监测项目及化验结果（支持ND值，使用字符串类型）
    nitrogen_oxides: Optional[str] = Field(None, description="氮氧化物（支持ND）", max_length=50)
    hydrogen_chloride: Optional[str] = Field(None, description="氯化氢（支持ND）", max_length=50)
    hydrogen_cyanide: Optional[str] = Field(None, description="氰化氢（支持ND）", max_length=50)
    sulfuric_acid_mist: Optional[str] = Field(None, description="硫酸雾（支持ND）", max_length=50)
    chromic_acid_mist: Optional[str] = Field(None, description="铬酸雾（支持ND）", max_length=50)
    fluoride: Optional[str] = Field(None, description="氟化物（支持ND）", max_length=50)
    phenol: Optional[str] = Field(None, description="酚类（支持ND）", max_length=50)
    non_methane_hydrocarbons: Optional[str] = Field(None, description="非甲烷总烃（支持ND）", max_length=50)
    benzene: Optional[str] = Field(None, description="苯（支持ND）", max_length=50)
    toluene: Optional[str] = Field(None, description="甲苯（支持ND）", max_length=50)
    xylene: Optional[str] = Field(None, description="二甲苯（支持ND）", max_length=50)
    toluene_xylene_total: Optional[str] = Field(None, description="甲苯与二甲苯合计（支持ND）", max_length=50)
    vocs: Optional[str] = Field(None, description="VOCs（支持ND）", max_length=50)
    
    remark: Optional[str] = Field(None, description="备注")


class PCBOrganizedGasMonitoringCreate(PCBOrganizedGasMonitoringBase):
    """创建有组织废气检测"""
    pass


class PCBOrganizedGasMonitoringUpdate(BaseModel):
    """更新有组织废气检测"""
    monitoring_point: Optional[str] = Field(None, description="监测点位", max_length=100)
    monitoring_time: Optional[str] = Field(None, description="监测时间", max_length=50)
    
    # 监测项目及化验结果（支持ND值，使用字符串类型）
    nitrogen_oxides: Optional[str] = Field(None, description="氮氧化物（支持ND）", max_length=50)
    hydrogen_chloride: Optional[str] = Field(None, description="氯化氢（支持ND）", max_length=50)
    hydrogen_cyanide: Optional[str] = Field(None, description="氰化氢（支持ND）", max_length=50)
    sulfuric_acid_mist: Optional[str] = Field(None, description="硫酸雾（支持ND）", max_length=50)
    chromic_acid_mist: Optional[str] = Field(None, description="铬酸雾（支持ND）", max_length=50)
    fluoride: Optional[str] = Field(None, description="氟化物（支持ND）", max_length=50)
    phenol: Optional[str] = Field(None, description="酚类（支持ND）", max_length=50)
    non_methane_hydrocarbons: Optional[str] = Field(None, description="非甲烷总烃（支持ND）", max_length=50)
    benzene: Optional[str] = Field(None, description="苯（支持ND）", max_length=50)
    toluene: Optional[str] = Field(None, description="甲苯（支持ND）", max_length=50)
    xylene: Optional[str] = Field(None, description="二甲苯（支持ND）", max_length=50)
    toluene_xylene_total: Optional[str] = Field(None, description="甲苯与二甲苯合计（支持ND）", max_length=50)
    vocs: Optional[str] = Field(None, description="VOCs（支持ND）", max_length=50)
    
    remark: Optional[str] = Field(None, description="备注")


class PCBOrganizedGasMonitoringResponse(PCBOrganizedGasMonitoringBase):
    """有组织废气检测响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PCBUnorganizedGasMonitoringBase(BaseModel):
    """无组织废气检测基础模式"""
    sampling_time: str = Field(..., description="采样时间", max_length=50)
    sampling_point: str = Field(..., description="采样点位", max_length=100)
    monitoring_factor: str = Field(..., description="监测因子", max_length=50)
    emission_concentration: Optional[str] = Field(None, alias="emissionConcentration", description="排放浓度（mg/m³，支持ND）", max_length=50)
    emission_limit: Optional[Decimal] = Field(None, alias="emissionLimit", description="排放浓度限值（mg/m³）", ge=0)
    compliance: str = Field(..., description="达标情况", max_length=20)
    remark: Optional[str] = Field(None, description="备注")
    
    model_config = {"extra": "allow", "populate_by_name": True}


class PCBUnorganizedGasMonitoringCreate(PCBUnorganizedGasMonitoringBase):
    """创建无组织废气检测"""
    pass


class PCBUnorganizedGasMonitoringUpdate(BaseModel):
    """更新无组织废气检测"""
    sampling_time: Optional[str] = Field(None, description="采样时间", max_length=50)
    sampling_point: Optional[str] = Field(None, description="采样点位", max_length=100)
    monitoring_factor: Optional[str] = Field(None, description="监测因子", max_length=50)
    emission_concentration: Optional[str] = Field(None, alias="emissionConcentration", description="排放浓度（mg/m³，支持ND）", max_length=50)
    emission_limit: Optional[Decimal] = Field(None, alias="emissionLimit", description="排放浓度限值（mg/m³）", ge=0)
    compliance: Optional[str] = Field(None, description="达标情况", max_length=20)
    remark: Optional[str] = Field(None, description="备注")
    
    model_config = {"extra": "allow", "populate_by_name": True}


class PCBUnorganizedGasMonitoringResponse(PCBUnorganizedGasMonitoringBase):
    """无组织废气检测响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PCBWastewaterMonitoringBase(BaseModel):
    """废水排放监测基础模式"""
    sampling_date: str = Field(..., description="采样日期", max_length=50)
    monitoring_point: str = Field(default="", description="监测地点", max_length=100)
    
    # 检测结果（单位：mg/L）
    ph: Optional[Decimal] = Field(None, description="pH", ge=0)
    cod: Optional[Decimal] = Field(None, description="COD", ge=0)
    ammonia_nitrogen: Optional[Decimal] = Field(None, description="氨氮", ge=0)
    total_phosphorus: Optional[Decimal] = Field(None, description="总磷", ge=0)
    total_nitrogen: Optional[Decimal] = Field(None, description="总氮", ge=0)
    total_cyanide: Optional[Decimal] = Field(None, description="总氰化物", ge=0)
    total_copper: Optional[Decimal] = Field(None, description="总铜", ge=0)
    nickel: Optional[Decimal] = Field(None, description="镍", ge=0)
    nickel_outlet: Optional[Decimal] = Field(None, description="镍（镍排口）", ge=0)
    
    remark: Optional[str] = Field(None, description="备注")


class PCBWastewaterMonitoringCreate(PCBWastewaterMonitoringBase):
    """创建废水排放监测"""
    pass


class PCBWastewaterMonitoringUpdate(BaseModel):
    """更新废水排放监测"""
    sampling_date: Optional[str] = Field(None, description="采样日期", max_length=50)
    monitoring_point: Optional[str] = Field(None, description="监测地点", max_length=100)
    
    # 检测结果（单位：mg/L）
    ph: Optional[Decimal] = Field(None, description="pH", ge=0)
    cod: Optional[Decimal] = Field(None, description="COD", ge=0)
    ammonia_nitrogen: Optional[Decimal] = Field(None, description="氨氮", ge=0)
    total_phosphorus: Optional[Decimal] = Field(None, description="总磷", ge=0)
    total_nitrogen: Optional[Decimal] = Field(None, description="总氮", ge=0)
    total_cyanide: Optional[Decimal] = Field(None, description="总氰化物", ge=0)
    total_copper: Optional[Decimal] = Field(None, description="总铜", ge=0)
    nickel: Optional[Decimal] = Field(None, description="镍", ge=0)
    nickel_outlet: Optional[Decimal] = Field(None, description="镍（镍排口）", ge=0)
    
    remark: Optional[str] = Field(None, description="备注")


class PCBWastewaterMonitoringResponse(PCBWastewaterMonitoringBase):
    """废水排放监测响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PCBGasEmissionMonitoringBase(BaseModel):
    """废气排放监测基础模式"""
    detection_point: str = Field(..., description="检测点位", max_length=100)
    detection_item: str = Field(..., description="检测项目", max_length=100)
    emission_rate: Optional[Decimal] = Field(None, alias="emissionRate", description="排放速率（kg/h）", ge=0)
    benchmark_flow: Optional[Decimal] = Field(None, alias="benchmarkFlow", description="标杆流量（m³/h）", ge=0)
    detection_result: Optional[str] = Field(None, alias="detectionResult", description="检测结果（支持ND）", max_length=50)
    permitted_emission_limit: Optional[Decimal] = Field(None, alias="permittedEmissionLimit", description="许可排放浓度限值", ge=0)
    stack_height: Optional[Decimal] = Field(None, alias="stackHeight", description="排气筒高（m）", ge=0)
    remark: Optional[str] = Field(None, description="备注")
    
    model_config = {"extra": "allow", "populate_by_name": True}


class PCBGasEmissionMonitoringCreate(PCBGasEmissionMonitoringBase):
    """创建废气排放监测"""
    pass


class PCBGasEmissionMonitoringUpdate(BaseModel):
    """更新废气排放监测"""
    detection_point: Optional[str] = Field(None, description="检测点位", max_length=100)
    detection_item: Optional[str] = Field(None, description="检测项目", max_length=100)
    emission_rate: Optional[Decimal] = Field(None, alias="emissionRate", description="排放速率（kg/h）", ge=0)
    benchmark_flow: Optional[Decimal] = Field(None, alias="benchmarkFlow", description="标杆流量（m³/h）", ge=0)
    detection_result: Optional[str] = Field(None, alias="detectionResult", description="检测结果（支持ND）", max_length=50)
    permitted_emission_limit: Optional[Decimal] = Field(None, alias="permittedEmissionLimit", description="许可排放浓度限值", ge=0)
    stack_height: Optional[Decimal] = Field(None, alias="stackHeight", description="排气筒高（m）", ge=0)
    remark: Optional[str] = Field(None, description="备注")
    
    model_config = {"extra": "allow", "populate_by_name": True}


class PCBGasEmissionMonitoringResponse(PCBGasEmissionMonitoringBase):
    """废气排放监测响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PCBNoiseMonitoringBase(BaseModel):
    """噪声监测基础模式"""
    monitoring_time: str = Field(..., description="监测时间", max_length=50)
    monitoring_point: str = Field(..., description="监测点位", max_length=100)
    
    # 检测结果 Leq（dB（A））
    daytime_result: Optional[Decimal] = Field(None, description="昼间检测结果", ge=0)
    nighttime_result: Optional[Decimal] = Field(None, description="夜间检测结果", ge=0)
    
    # 排放标准 Leq（dB（A））
    daytime_standard: Optional[Decimal] = Field(None, description="昼间排放标准", ge=0)
    nighttime_standard: Optional[Decimal] = Field(None, description="夜间排放标准", ge=0)
    
    remark: Optional[str] = Field(None, description="备注")


class PCBNoiseMonitoringCreate(PCBNoiseMonitoringBase):
    """创建噪声监测"""
    pass


class PCBNoiseMonitoringUpdate(BaseModel):
    """更新噪声监测"""
    monitoring_time: Optional[str] = Field(None, description="监测时间", max_length=50)
    monitoring_point: Optional[str] = Field(None, description="监测点位", max_length=100)
    
    # 检测结果 Leq（dB（A））
    daytime_result: Optional[Decimal] = Field(None, description="昼间检测结果", ge=0)
    nighttime_result: Optional[Decimal] = Field(None, description="夜间检测结果", ge=0)
    
    # 排放标准 Leq（dB（A））
    daytime_standard: Optional[Decimal] = Field(None, description="昼间排放标准", ge=0)
    nighttime_standard: Optional[Decimal] = Field(None, description="夜间排放标准", ge=0)
    
    remark: Optional[str] = Field(None, description="备注")


class PCBNoiseMonitoringResponse(PCBNoiseMonitoringBase):
    """噪声监测响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 批量操作相关Schema
class PCBSelfMonitoringDataRequest(BaseModel):
    """自行监测数据请求"""
    organizedGas: List[PCBOrganizedGasMonitoringCreate] = Field(default_factory=list, description="有组织废气检测数据")
    unorganizedGas: List[PCBUnorganizedGasMonitoringCreate] = Field(default_factory=list, description="无组织废气检测数据")
    wastewater: List[PCBWastewaterMonitoringCreate] = Field(default_factory=list, description="废水监测数据")
    gasEmission: List[PCBGasEmissionMonitoringCreate] = Field(default_factory=list, description="废气排放监测数据")
    noise: List[PCBNoiseMonitoringCreate] = Field(default_factory=list, description="噪声监测数据")


class PCBSelfMonitoringDataResponse(BaseModel):
    """自行监测数据响应"""
    organizedGas: List[PCBOrganizedGasMonitoringResponse] = Field(default_factory=list, description="有组织废气检测数据")
    unorganizedGas: List[PCBUnorganizedGasMonitoringResponse] = Field(default_factory=list, description="无组织废气检测数据")
    wastewater: List[PCBWastewaterMonitoringResponse] = Field(default_factory=list, description="废水监测数据")
    gasEmission: List[PCBGasEmissionMonitoringResponse] = Field(default_factory=list, description="废气排放监测数据")
    noise: List[PCBNoiseMonitoringResponse] = Field(default_factory=list, description="噪声监测数据")


class PCBSelfMonitoringSaveResponse(BaseModel):
    """自行监测保存响应"""
    success: bool = Field(True, description="保存是否成功")
    message: str = Field("保存成功", description="响应消息")
    data: Optional[dict] = Field(None, description="保存的数据")
