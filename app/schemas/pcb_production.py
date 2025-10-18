"""
PCB企业生产情况数据Schema
定义API请求和响应的数据结构
"""
from typing import List, Optional
from decimal import Decimal
from pydantic import BaseModel, Field


class PCBProductOutputBase(BaseModel):
    """PCB产品产量基础Schema"""
    type: str = Field(..., description="类型(rigid/flexible)")
    main_product: str = Field(..., description="主要产品")
    unit: str = Field(..., description="单位")
    year: str = Field(..., description="年份")
    output: Optional[float] = Field(None, description="产量")
    layers: Optional[int] = Field(None, description="层数")


class PCBProductOutputCreate(PCBProductOutputBase):
    """创建PCB产品产量Schema"""
    pass


class PCBProductOutputUpdate(BaseModel):
    """更新PCB产品产量Schema"""
    type: Optional[str] = None
    main_product: Optional[str] = None
    unit: Optional[str] = None
    year: Optional[str] = None
    output: Optional[float] = None
    layers: Optional[int] = None


class PCBProductOutputResponse(PCBProductOutputBase):
    """PCB产品产量响应Schema"""
    id: int
    enterprise_id: int

    class Config:
        from_attributes = True


class PCBQualificationRateBase(BaseModel):
    """PCB合格率基础Schema"""
    year: str = Field(..., description="年份")
    rate: Optional[float] = Field(None, description="合格率(%)")


class PCBQualificationRateCreate(PCBQualificationRateBase):
    """创建PCB合格率Schema"""
    pass


class PCBQualificationRateUpdate(BaseModel):
    """更新PCB合格率Schema"""
    year: Optional[str] = None
    rate: Optional[float] = None


class PCBQualificationRateResponse(PCBQualificationRateBase):
    """PCB合格率响应Schema"""
    id: int
    enterprise_id: int

    class Config:
        from_attributes = True


class PCBOutputValueBase(BaseModel):
    """PCB产值情况基础Schema"""
    year: str = Field(..., description="年份")
    unit: str = Field(..., description="单位")
    annual_output_value: Optional[float] = Field(None, description="年产值")
    income_tax: Optional[float] = Field(None, description="所得税")


class PCBOutputValueCreate(PCBOutputValueBase):
    """创建PCB产值情况Schema"""
    pass


class PCBOutputValueUpdate(BaseModel):
    """更新PCB产值情况Schema"""
    year: Optional[str] = None
    unit: Optional[str] = None
    annual_output_value: Optional[float] = None
    income_tax: Optional[float] = None


class PCBOutputValueResponse(PCBOutputValueBase):
    """PCB产值情况响应Schema"""
    id: int
    enterprise_id: int

    class Config:
        from_attributes = True


class PCBProductionDataRequest(BaseModel):
    """PCB企业生产情况数据请求Schema"""
    productOutput: List[PCBProductOutputCreate] = Field(default_factory=list, description="产品产量数据")
    qualificationRate: List[PCBQualificationRateCreate] = Field(default_factory=list, description="合格率数据")
    outputValue: List[PCBOutputValueCreate] = Field(default_factory=list, description="产值情况数据")


class PCBProductionDataResponse(BaseModel):
    """PCB企业生产情况数据响应Schema"""
    productOutput: List[PCBProductOutputResponse] = Field(default_factory=list, description="产品产量数据")
    qualificationRate: List[PCBQualificationRateResponse] = Field(default_factory=list, description="合格率数据")
    outputValue: List[PCBOutputValueResponse] = Field(default_factory=list, description="产值情况数据")


class PCBProductionDataSaveResponse(BaseModel):
    """PCB企业生产情况数据保存响应Schema"""
    productOutput: int = Field(..., description="产品产量记录数")
    qualificationRate: int = Field(..., description="合格率记录数")
    outputValue: int = Field(..., description="产值情况记录数")
