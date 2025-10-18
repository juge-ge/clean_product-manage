from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field

class RawMaterialBase(BaseModel):
    name: str = Field(..., description="材料名称")
    unit: str = Field(..., description="默认单位")
    process: str = Field(..., description="常用工序")
    state: Optional[str] = Field(None, description="材料状态（固体/液体/气体）")
    voc_content: Optional[float] = Field(None, description="VOC含量(%)")

class RawMaterialCreate(RawMaterialBase):
    pass

class RawMaterialUpdate(RawMaterialBase):
    pass

class RawMaterialInDB(RawMaterialBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class RawMaterialSearchResponse(BaseModel):
    materials: List[RawMaterialInDB]

class EnterpriseRawMaterialUsageSchema(BaseModel):
    id: Optional[int] = None
    enterprise_id: int = Field(..., description="企业ID")
    material_id: int = Field(..., description="材料ID")
    year: str = Field(..., description="年份")
    amount: Optional[float] = Field(None, description="用量")
    unit: Optional[str] = Field(None, description="使用单位")
    process: Optional[str] = Field(None, description="使用工序")
    state: Optional[str] = Field(None, description="状态")
    voc_content: Optional[float] = Field(None, description="VOC含量(%)")

    class Config:
        from_attributes = True

class RawMaterialUsageRequest(BaseModel):
    material_id: int = Field(..., description="材料ID")
    year: str = Field(..., description="年份")
    amount: Optional[float] = Field(None, description="用量")
    unit: Optional[str] = Field(None, description="使用单位")
    process: Optional[str] = Field(None, description="使用工序")
    state: Optional[str] = Field(None, description="状态")
    voc_content: Optional[float] = Field(None, description="VOC含量(%)")

class RawMaterialUsageResponse(BaseModel):
    id: int
    material: RawMaterialInDB
    year: str
    amount: Optional[float]
    unit: Optional[str]
    process: Optional[str]
    state: Optional[str]
    voc_content: Optional[float]

    class Config:
        from_attributes = True

# 企业原辅材料使用情况相关模式
class EnterpriseRawMaterialUsageCreate(BaseModel):
    enterprise_id: int = Field(..., description="企业ID")
    material_id: int = Field(..., description="材料ID")
    year: str = Field(..., description="年份")
    amount: Optional[float] = Field(None, description="用量")
    unit: Optional[str] = Field(None, description="使用单位")
    process: Optional[str] = Field(None, description="使用工序")
    state: Optional[str] = Field(None, description="状态")
    voc_content: Optional[float] = Field(None, description="VOC含量(%)")

class EnterpriseRawMaterialUsageUpdate(BaseModel):
    amount: Optional[float] = Field(None, description="用量")
    unit: Optional[str] = Field(None, description="使用单位")
    process: Optional[str] = Field(None, description="使用工序")
    state: Optional[str] = Field(None, description="状态")
    voc_content: Optional[float] = Field(None, description="VOC含量(%)")

class EnterpriseRawMaterialUsageInDB(BaseModel):
    id: int
    enterprise_id: int
    material_id: int
    year: str
    amount: Optional[float]
    unit: Optional[str]
    process: Optional[str]
    state: Optional[str]
    voc_content: Optional[float]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EnterpriseRawMaterialUsageWithMaterial(BaseModel):
    id: int
    enterprise_id: int
    material_id: int
    year: str
    amount: Optional[float]
    unit: Optional[str]
    process: Optional[str]
    state: Optional[str]
    voc_content: Optional[float]
    material: RawMaterialInDB
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EnterpriseRawMaterialUsageBatchRequest(BaseModel):
    year: str = Field(..., description="年份")
    usage_data: List[Dict[str, Any]] = Field(..., description="使用数据列表")

class EnterpriseRawMaterialUsageStatistics(BaseModel):
    total_materials: int = Field(..., description="总材料数")
    completed_materials: int = Field(..., description="已填写材料数")
    completion_rate: float = Field(..., description="完成率")
    process_statistics: Dict[str, int] = Field(..., description="工序统计")
