"""
PCB企业污染防治数据验证模式
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class PCBWastewaterAnalysisBase(BaseModel):
    """废水产生分析基础模式"""
    category: str = Field(..., description="废水类别", max_length=100)
    source: str = Field(..., description="来源")
    pollutants: str = Field(..., description="主要污染物")
    disposal: str = Field(..., description="处置方式")
    remark: Optional[str] = Field(None, description="备注")


class PCBWastewaterAnalysisCreate(PCBWastewaterAnalysisBase):
    """创建废水产生分析"""
    pass


class PCBWastewaterAnalysisUpdate(BaseModel):
    """更新废水产生分析"""
    category: Optional[str] = Field(None, description="废水类别", max_length=100)
    source: Optional[str] = Field(None, description="来源")
    pollutants: Optional[str] = Field(None, description="主要污染物")
    disposal: Optional[str] = Field(None, description="处置方式")
    remark: Optional[str] = Field(None, description="备注")


class PCBWastewaterAnalysisResponse(PCBWastewaterAnalysisBase):
    """废水产生分析响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PCBWasteGasAnalysisBase(BaseModel):
    """废气产生情况基础模式"""
    gas_type: str = Field(..., description="种类", max_length=100)
    pollutants: str = Field(..., description="主要污染物", max_length=200)
    location: str = Field(..., description="产生部位")
    treatment: str = Field(..., description="处理方法")
    remark: Optional[str] = Field(None, description="备注")


class PCBWasteGasAnalysisCreate(PCBWasteGasAnalysisBase):
    """创建废气产生情况"""
    pass


class PCBWasteGasAnalysisUpdate(BaseModel):
    """更新废气产生情况"""
    gas_type: Optional[str] = Field(None, description="种类", max_length=100)
    pollutants: Optional[str] = Field(None, description="主要污染物", max_length=200)
    location: Optional[str] = Field(None, description="产生部位")
    treatment: Optional[str] = Field(None, description="处理方法")
    remark: Optional[str] = Field(None, description="备注")


class PCBWasteGasAnalysisResponse(PCBWasteGasAnalysisBase):
    """废气产生情况响应"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# 批量操作相关Schema
class PCBWastewaterDataRequest(BaseModel):
    """废水数据请求"""
    wastewater: List[PCBWastewaterAnalysisCreate] = Field(default_factory=list, description="废水分析数据")


class PCBWasteGasDataRequest(BaseModel):
    """废气数据请求"""
    wasteGas: List[PCBWasteGasAnalysisCreate] = Field(default_factory=list, description="废气分析数据")


class PCBWastewaterDataResponse(BaseModel):
    """废水数据响应"""
    wastewater: List[PCBWastewaterAnalysisResponse] = Field(default_factory=list, description="废水分析数据")


class PCBWasteGasDataResponse(BaseModel):
    """废气数据响应"""
    wasteGas: List[PCBWasteGasAnalysisResponse] = Field(default_factory=list, description="废气分析数据")


class PCBPollutionControlDataRequest(BaseModel):
    """污染防治数据请求"""
    wastewater: PCBWastewaterDataRequest = Field(default_factory=PCBWastewaterDataRequest, description="废水数据")
    wasteGas: PCBWasteGasDataRequest = Field(default_factory=PCBWasteGasDataRequest, description="废气数据")


class PCBPollutionControlDataResponse(BaseModel):
    """污染防治数据响应"""
    wastewater: List[PCBWastewaterAnalysisResponse] = Field(default_factory=list, description="废水分析数据")
    wasteGas: List[PCBWasteGasAnalysisResponse] = Field(default_factory=list, description="废气分析数据")


class PCBPollutionControlSaveResponse(BaseModel):
    """污染防治保存响应"""
    success: bool = Field(True, description="保存是否成功")
    message: str = Field("保存成功", description="响应消息")
    data: Optional[dict] = Field(None, description="保存的数据")
