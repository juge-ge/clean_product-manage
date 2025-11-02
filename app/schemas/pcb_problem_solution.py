"""
PCB问题及清洁生产方案模块Schemas
"""
from decimal import Decimal
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


# ==================== 问题清单 Schemas ====================

class ProblemIssueItem(BaseModel):
    """问题清单项"""
    indicator_id: int = Field(..., description="指标ID")
    primary_indicator: str = Field(..., description="一级指标")
    primary_weight: Decimal = Field(..., description="一级指标权重")
    secondary_indicator: str = Field(..., description="二级指标")
    secondary_weight: Decimal = Field(..., description="二级指标权重")
    current_level: str = Field(..., description="当前评级")


# ==================== 权重总和计分排序 Schemas ====================

class ScoringFactor(BaseModel):
    """评分因素"""
    key: str = Field(..., description="因素键")
    name: str = Field(..., description="因素名称")
    weight: int = Field(..., ge=0, le=20, description="权重W")


class ScoringFocus(BaseModel):
    """审核重点"""
    id: int = Field(..., description="审核重点ID")
    name: str = Field(..., description="审核重点名称")


class ScoringMatrixItem(BaseModel):
    """评分矩阵项"""
    r: int = Field(0, ge=0, le=10, description="评分R")
    rw: int = Field(0, ge=0, le=100, description="加权评分RW")


class ProblemSolutionScoringBase(BaseModel):
    """问题方案权重计分基础Schema"""
    factors: List[ScoringFactor] = Field(..., description="因素列表")
    focuses: List[ScoringFocus] = Field(..., description="审核重点列表")
    scores: Dict[str, Dict[str, ScoringMatrixItem]] = Field(..., description="评分矩阵")
    rankings: Optional[List[Dict[str, Any]]] = Field(None, description="排序结果")


class ProblemSolutionScoringCreate(ProblemSolutionScoringBase):
    """创建问题方案权重计分请求Schema"""
    pass


class ProblemSolutionScoringUpdate(BaseModel):
    """更新问题方案权重计分请求Schema"""
    factors: Optional[List[ScoringFactor]] = Field(None, description="因素列表")
    focuses: Optional[List[ScoringFocus]] = Field(None, description="审核重点列表")
    scores: Optional[Dict[str, Dict[str, ScoringMatrixItem]]] = Field(None, description="评分矩阵")
    rankings: Optional[List[Dict[str, Any]]] = Field(None, description="排序结果")


class ProblemSolutionScoringResponse(ProblemSolutionScoringBase):
    """问题方案权重计分响应Schema"""
    id: int
    enterprise_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ==================== 无/低费方案 Schemas ====================

class LowCostSchemeBase(BaseModel):
    """无/低费方案基础Schema"""
    source: str = Field(default="custom", description="方案来源: custom(自定义), library(方案库导入)")
    scheme_id: Optional[int] = Field(None, description="关联方案库方案ID")
    indicator_ids: Optional[List[int]] = Field(None, description="关联指标ID列表")
    name: str = Field(..., max_length=200, description="方案名称")
    intro: Optional[str] = Field(None, description="方案简介")
    economic_benefit: Optional[str] = Field(None, description="经济效益")
    environment_benefit: Optional[str] = Field(None, description="环境效益")
    remark: Optional[str] = Field(None, description="备注")


class LowCostSchemeCreate(LowCostSchemeBase):
    """创建无/低费方案请求Schema"""
    pass


class LowCostSchemeUpdate(BaseModel):
    """更新无/低费方案请求Schema"""
    source: Optional[str] = Field(None, description="方案来源")
    scheme_id: Optional[int] = Field(None, description="关联方案库方案ID")
    indicator_ids: Optional[List[int]] = Field(None, description="关联指标ID列表")
    name: Optional[str] = Field(None, max_length=200, description="方案名称")
    intro: Optional[str] = Field(None, description="方案简介")
    economic_benefit: Optional[str] = Field(None, description="经济效益")
    environment_benefit: Optional[str] = Field(None, description="环境效益")
    remark: Optional[str] = Field(None, description="备注")


class LowCostSchemeResponse(LowCostSchemeBase):
    """无/低费方案响应Schema"""
    id: int
    enterprise_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ==================== 中/高费方案 Schemas ====================

class MediumHighCostSchemeBase(BaseModel):
    """中/高费方案基础Schema"""
    source: str = Field(default="custom", description="方案来源: custom(自定义), library(方案库导入)")
    cost_level: str = Field(default="middle", description="费用等级: middle(中费), high(高费)")
    scheme_id: Optional[int] = Field(None, description="关联方案库方案ID")
    indicator_ids: Optional[List[int]] = Field(None, description="关联指标ID列表")
    name: str = Field(..., max_length=200, description="方案名称")
    intro: Optional[str] = Field(None, description="方案简介")
    problem: Optional[str] = Field(None, description="解决的问题")
    content: Optional[str] = Field(None, description="方案内容/实施步骤")
    effect: Optional[str] = Field(None, description="预期效果")
    economic_benefit: Optional[str] = Field(None, description="经济效益")
    environment_benefit: Optional[str] = Field(None, description="环境效益")
    remark: Optional[str] = Field(None, description="备注")


class MediumHighCostSchemeCreate(MediumHighCostSchemeBase):
    """创建中/高费方案请求Schema"""
    pass


class MediumHighCostSchemeUpdate(BaseModel):
    """更新中/高费方案请求Schema"""
    source: Optional[str] = Field(None, description="方案来源")
    cost_level: Optional[str] = Field(None, description="费用等级")
    scheme_id: Optional[int] = Field(None, description="关联方案库方案ID")
    indicator_ids: Optional[List[int]] = Field(None, description="关联指标ID列表")
    name: Optional[str] = Field(None, max_length=200, description="方案名称")
    intro: Optional[str] = Field(None, description="方案简介")
    problem: Optional[str] = Field(None, description="解决的问题")
    content: Optional[str] = Field(None, description="方案内容/实施步骤")
    effect: Optional[str] = Field(None, description="预期效果")
    economic_benefit: Optional[str] = Field(None, description="经济效益")
    environment_benefit: Optional[str] = Field(None, description="环境效益")
    remark: Optional[str] = Field(None, description="备注")


class MediumHighCostSchemeResponse(MediumHighCostSchemeBase):
    """中/高费方案响应Schema"""
    id: int
    enterprise_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True
