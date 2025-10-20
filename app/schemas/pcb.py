"""
PCB行业清洁生产审核模块Pydantic Schemas
用于API请求和响应的数据验证
"""
from datetime import date, datetime
from decimal import Decimal
from typing import Any, List, Optional

from pydantic import BaseModel, Field


# ==================== PCB Enterprise Schemas ====================

class PCBEnterpriseBase(BaseModel):
    """企业基本信息基础Schema"""
    name: str = Field(..., description="企业名称")
    unified_social_credit_code: Optional[str] = Field(None, description="统一社会信用代码")
    region: Optional[str] = Field(None, description="地市")
    district: Optional[str] = Field(None, description="区县")
    address: Optional[str] = Field(None, description="详细地址")
    legal_representative: Optional[str] = Field(None, description="法人代表")
    contact_person: Optional[str] = Field(None, description="联系人")
    contact_phone: Optional[str] = Field(None, description="联系电话")
    contact_email: Optional[str] = Field(None, description="联系邮箱")
    industry_type: Optional[str] = Field(None, description="行业类型")
    capital: Optional[Decimal] = Field(None, description="注册资本(万元)")
    capacity: Optional[Decimal] = Field(None, description="年产能(万m²)")


class PCBEnterpriseCreate(PCBEnterpriseBase):
    """创建企业请求Schema"""
    pass


class PCBEnterpriseUpdate(BaseModel):
    """更新企业请求Schema"""
    name: Optional[str] = Field(None, description="企业名称")
    unified_social_credit_code: Optional[str] = Field(None, description="统一社会信用代码")
    region: Optional[str] = Field(None, description="地市")
    district: Optional[str] = Field(None, description="区县")
    address: Optional[str] = Field(None, description="详细地址")
    legal_representative: Optional[str] = Field(None, description="法人代表")
    contact_person: Optional[str] = Field(None, description="联系人")
    contact_phone: Optional[str] = Field(None, description="联系电话")
    contact_email: Optional[str] = Field(None, description="联系邮箱")
    industry_type: Optional[str] = Field(None, description="行业类型")
    capital: Optional[Decimal] = Field(None, description="注册资本(万元)")
    capacity: Optional[Decimal] = Field(None, description="年产能(万m²)")
    audit_status: Optional[str] = Field(None, description="审核状态")
    current_step: Optional[int] = Field(None, description="当前步骤")


class PCBEnterpriseResponse(PCBEnterpriseBase):
    """企业信息响应Schema"""
    id: int
    audit_status: str = Field(default="pending", description="审核状态")
    current_step: int = Field(default=0, description="当前步骤")
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ==================== PCB Indicator Schemas ====================

class PCBIndicatorBase(BaseModel):
    """指标基础Schema"""
    indicator_id: int = Field(..., description="指标编号(1-64)")
    name: str = Field(..., description="指标名称")
    category: str = Field(..., description="一级指标分类")
    indicator_type: str = Field(..., description="指标类型")
    unit: Optional[str] = Field(None, description="计量单位")
    weight: Decimal = Field(default=Decimal("1.0"), description="指标权重")
    level_standards: Optional[dict] = Field(None, description="评级标准")
    is_limiting: bool = Field(default=False, description="是否为限定性指标")
    description: Optional[str] = Field(None, description="指标说明")
    order: int = Field(default=0, description="排序")


class PCBIndicatorCreate(PCBIndicatorBase):
    """创建指标请求Schema"""
    pass


class PCBIndicatorUpdate(BaseModel):
    """更新指标请求Schema"""
    name: Optional[str] = Field(None, description="指标名称")
    category: Optional[str] = Field(None, description="一级指标分类")
    indicator_type: Optional[str] = Field(None, description="指标类型")
    unit: Optional[str] = Field(None, description="计量单位")
    weight: Optional[Decimal] = Field(None, description="指标权重")
    level_standards: Optional[dict] = Field(None, description="评级标准")
    is_limiting: Optional[bool] = Field(None, description="是否为限定性指标")
    description: Optional[str] = Field(None, description="指标说明")
    order: Optional[int] = Field(None, description="排序")


class PCBIndicatorResponse(PCBIndicatorBase):
    """指标响应Schema"""
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ==================== PCB Audit Result Schemas ====================

class PCBAuditResultBase(BaseModel):
    """审核结果基础Schema"""
    enterprise_id: int = Field(..., description="企业ID")
    indicator_id: int = Field(..., description="指标ID")
    current_value: Optional[Decimal] = Field(None, description="当前值")
    level: Optional[str] = Field(None, description="评级结果")
    score: Decimal = Field(default=Decimal("0"), description="得分")
    comment: Optional[str] = Field(None, description="审核意见")


class PCBAuditResultCreate(PCBAuditResultBase):
    """创建审核结果请求Schema"""
    pass


class PCBAuditResultUpdate(BaseModel):
    """更新审核结果请求Schema"""
    current_value: Optional[Decimal] = Field(None, description="当前值")
    level: Optional[str] = Field(None, description="评级结果")
    score: Optional[Decimal] = Field(None, description="得分")
    comment: Optional[str] = Field(None, description="审核意见")
    manual_override: Optional[bool] = Field(None, description="是否手动调整")
    override_reason: Optional[str] = Field(None, description="调整原因")
    selected_scheme_ids: Optional[List[int]] = Field(None, description="选择的方案ID列表")


class PCBAuditResultResponse(PCBAuditResultBase):
    """审核结果响应Schema"""
    id: int
    manual_override: bool = Field(default=False, description="是否手动调整")
    override_reason: Optional[str] = Field(None, description="调整原因")
    selected_scheme_ids: Optional[List[int]] = Field(None, description="选择的方案ID列表")
    scheme_selection_date: Optional[str] = Field(None, description="方案选择时间")
    auditor_id: Optional[int] = Field(None, description="审核人ID")
    audit_date: Optional[str] = Field(None, description="审核时间")
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ==================== PCB Scheme Schemas ====================

class PCBSchemeBase(BaseModel):
    """方案基础Schema"""
    scheme_id: int = Field(..., description="方案编号(1-130)")
    name: str = Field(..., description="方案名称")
    scheme_type: Optional[str] = Field(None, description="方案类型")
    problem: Optional[str] = Field(None, description="解决的问题")
    description: Optional[str] = Field(None, description="方案简介")
    implementation: Optional[str] = Field(None, description="实施方案")
    economic_benefit: Optional[str] = Field(None, description="经济效益")
    investment: Optional[Decimal] = Field(None, description="投资估算(万元)")
    payback_period: Optional[Decimal] = Field(None, description="投资回收期(年)")
    environmental_benefit: Optional[str] = Field(None, description="环境效益")
    is_active: bool = Field(default=True, description="是否启用")


class PCBSchemeCreate(PCBSchemeBase):
    """创建方案请求Schema"""
    pass


class PCBSchemeUpdate(BaseModel):
    """更新方案请求Schema"""
    name: Optional[str] = Field(None, description="方案名称")
    scheme_type: Optional[str] = Field(None, description="方案类型")
    problem: Optional[str] = Field(None, description="解决的问题")
    description: Optional[str] = Field(None, description="方案简介")
    implementation: Optional[str] = Field(None, description="实施方案")
    economic_benefit: Optional[str] = Field(None, description="经济效益")
    investment: Optional[Decimal] = Field(None, description="投资估算(万元)")
    payback_period: Optional[Decimal] = Field(None, description="投资回收期(年)")
    environmental_benefit: Optional[str] = Field(None, description="环境效益")
    is_active: Optional[bool] = Field(None, description="是否启用")


class PCBSchemeResponse(PCBSchemeBase):
    """方案响应Schema"""
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ==================== PCB Pre-Audit Data Schemas ====================

class PCBPreAuditDataBase(BaseModel):
    """预审核数据基础Schema"""
    enterprise_id: int = Field(..., description="企业ID")
    production_info: Optional[dict] = Field(None, description="企业总体生产情况")
    raw_materials: Optional[dict] = Field(None, description="原辅材料使用情况")
    process_equipment: Optional[dict] = Field(None, description="主要工艺及装备使用")
    resource_consumption: Optional[dict] = Field(None, description="资源能源消耗")
    pollution_control: Optional[dict] = Field(None, description="污染防治")
    solid_waste: Optional[dict] = Field(None, description="工业固体废物管理")
    self_monitoring: Optional[dict] = Field(None, description="自行监测情况")


class PCBPreAuditDataCreate(PCBPreAuditDataBase):
    """创建预审核数据请求Schema"""
    pass


class PCBPreAuditDataUpdate(BaseModel):
    """更新预审核数据请求Schema"""
    production_info: Optional[dict] = Field(None, description="企业总体生产情况")
    raw_materials: Optional[dict] = Field(None, description="原辅材料使用情况")
    process_equipment: Optional[dict] = Field(None, description="主要工艺及装备使用")
    resource_consumption: Optional[dict] = Field(None, description="资源能源消耗")
    pollution_control: Optional[dict] = Field(None, description="污染防治")
    solid_waste: Optional[dict] = Field(None, description="工业固体废物管理")
    self_monitoring: Optional[dict] = Field(None, description="自行监测情况")
    status: Optional[str] = Field(None, description="状态")


class PCBPreAuditDataResponse(PCBPreAuditDataBase):
    """预审核数据响应Schema"""
    id: int
    status: str = Field(default="draft", description="状态")
    submitted_at: Optional[str] = Field(None, description="提交时间")
    approved_at: Optional[str] = Field(None, description="审核通过时间")
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ==================== PCB Indicator-Scheme Relation Schemas ====================

class PCBIndicatorSchemeRelationBase(BaseModel):
    """指标方案关联基础Schema"""
    indicator_id: int = Field(..., description="指标ID")
    scheme_id: int = Field(..., description="方案ID")
    relevance_score: Decimal = Field(default=Decimal("1.0"), description="关联度")
    priority: int = Field(default=1, description="优先级(1-10)")
    recommendation_reason: Optional[str] = Field(None, description="推荐理由")


class PCBIndicatorSchemeRelationCreate(PCBIndicatorSchemeRelationBase):
    """创建指标方案关联请求Schema"""
    pass


class PCBIndicatorSchemeRelationResponse(PCBIndicatorSchemeRelationBase):
    """指标方案关联响应Schema"""
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ==================== PCB Enterprise Scheme Schemas ====================

class PCBEnterpriseSchemeBase(BaseModel):
    """企业方案基础Schema"""
    enterprise_id: int = Field(..., description="企业ID")
    scheme_id: int = Field(..., description="方案ID")
    indicator_id: Optional[int] = Field(None, description="关联指标ID")
    status: str = Field(default="recommended", description="方案状态")


class PCBEnterpriseSchemeCreate(PCBEnterpriseSchemeBase):
    """创建企业方案请求Schema"""
    implementation_plan: Optional[str] = Field(None, description="实施计划")
    start_date: Optional[date] = Field(None, description="开始日期")
    expected_completion_date: Optional[date] = Field(None, description="预计完成日期")
    notes: Optional[str] = Field(None, description="备注")


class PCBEnterpriseSchemeUpdate(BaseModel):
    """更新企业方案请求Schema"""
    status: Optional[str] = Field(None, description="方案状态")
    implementation_plan: Optional[str] = Field(None, description="实施计划")
    start_date: Optional[date] = Field(None, description="开始日期")
    expected_completion_date: Optional[date] = Field(None, description="预计完成日期")
    actual_completion_date: Optional[date] = Field(None, description="实际完成日期")
    actual_investment: Optional[Decimal] = Field(None, description="实际投资(万元)")
    actual_benefit: Optional[str] = Field(None, description="实际效益")
    notes: Optional[str] = Field(None, description="备注")


class PCBEnterpriseSchemeResponse(PCBEnterpriseSchemeBase):
    """企业方案响应Schema"""
    id: int
    implementation_plan: Optional[str] = Field(None, description="实施计划")
    start_date: Optional[str] = Field(None, description="开始日期")
    expected_completion_date: Optional[str] = Field(None, description="预计完成日期")
    actual_completion_date: Optional[str] = Field(None, description="实际完成日期")
    actual_investment: Optional[Decimal] = Field(None, description="实际投资(万元)")
    actual_benefit: Optional[str] = Field(None, description="实际效益")
    notes: Optional[str] = Field(None, description="备注")
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ==================== PCB Audit Report Schemas ====================

class PCBAuditReportBase(BaseModel):
    """审核报告基础Schema"""
    enterprise_id: int = Field(..., description="企业ID")


class PCBAuditReportCreate(PCBAuditReportBase):
    """创建审核报告请求Schema"""
    pass


class PCBAuditReportUpdate(BaseModel):
    """更新审核报告请求Schema"""
    total_score: Optional[Decimal] = Field(None, description="总分")
    overall_level: Optional[str] = Field(None, description="综合等级")
    improvement_items: Optional[int] = Field(None, description="待改进项数")
    limiting_indicators_count: Optional[int] = Field(None, description="限定性指标数量")
    non_compliant_limiting_count: Optional[int] = Field(None, description="不达标限定性指标数")
    summary: Optional[dict] = Field(None, description="审核摘要")
    recommendations: Optional[str] = Field(None, description="改进建议")
    status: Optional[str] = Field(None, description="报告状态")


class PCBAuditReportResponse(PCBAuditReportBase):
    """审核报告响应Schema"""
    id: int
    total_score: Decimal = Field(default=Decimal("0"), description="总分")
    overall_level: Optional[str] = Field(None, description="综合等级")
    improvement_items: int = Field(default=0, description="待改进项数")
    limiting_indicators_count: int = Field(default=0, description="限定性指标数量")
    non_compliant_limiting_count: int = Field(default=0, description="不达标限定性指标数")
    summary: Optional[dict] = Field(None, description="审核摘要")
    recommendations: Optional[str] = Field(None, description="改进建议")
    status: str = Field(default="draft", description="报告状态")
    auditor_id: Optional[int] = Field(None, description="审核人ID")
    auditor_name: Optional[str] = Field(None, description="审核人姓名")
    audit_date: Optional[str] = Field(None, description="审核日期")
    report_file_id: Optional[str] = Field(None, description="报告文件ID")
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


# ==================== Complex Response Schemas ====================

class PCBIndicatorWithSchemesResponse(PCBIndicatorResponse):
    """指标及关联方案响应Schema"""
    recommended_schemes: List[dict] = Field(default=[], description="推荐方案列表")


class PCBAuditResultDetailResponse(PCBAuditResultResponse):
    """审核结果详情响应Schema（包含指标信息）"""
    indicator: Optional[PCBIndicatorResponse] = Field(None, description="指标信息")
    recommended_schemes: List[dict] = Field(default=[], description="推荐方案列表")


class PCBAuditSummaryResponse(BaseModel):
    """审核汇总响应Schema"""
    total_score: Decimal = Field(..., description="总分")
    overall_level: str = Field(..., description="综合等级")
    improvement_items: int = Field(..., description="待改进项数")
    limiting_indicators: int = Field(..., description="限定性指标数量")
    category_scores: dict = Field(default={}, description="各类别得分")


# ==================== Request Schemas for Complex Operations ====================

class BatchAuditResultUpdate(BaseModel):
    """批量更新审核结果请求Schema"""
    results: List[dict] = Field(..., description="审核结果列表")


class AutoCalculateRequest(BaseModel):
    """自动计算请求Schema"""
    enterprise_id: int = Field(..., description="企业ID")
    recalculate_all: bool = Field(default=False, description="是否重新计算所有指标")


class SubmitAuditRequest(BaseModel):
    """提交审核请求Schema"""
    enterprise_id: int = Field(..., description="企业ID")
    auditor_id: int = Field(..., description="审核人ID")
    comment: Optional[str] = Field(None, description="审核意见")


class GetRecommendedSchemesRequest(BaseModel):
    """获取推荐方案请求Schema"""
    enterprise_id: int = Field(..., description="企业ID")
    indicator_id: int = Field(..., description="指标ID")
    level: Optional[str] = Field(None, description="评级结果")


