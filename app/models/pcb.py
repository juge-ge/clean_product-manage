"""
PCB行业清洁生产审核模块数据库模型
根据PCB审核模块数据库与交互设计方案定义的8个核心表
"""
from tortoise import fields

from .base import BaseModel, TimestampMixin


class PCBEnterprise(BaseModel, TimestampMixin):
    """PCB企业基本信息表"""
    name = fields.CharField(max_length=200, description="企业名称", index=True)
    unified_social_credit_code = fields.CharField(max_length=50, null=True, description="统一社会信用代码", index=True)
    region = fields.CharField(max_length=100, null=True, description="地市")
    district = fields.CharField(max_length=100, null=True, description="区县")
    address = fields.CharField(max_length=500, null=True, description="详细地址")
    legal_representative = fields.CharField(max_length=50, null=True, description="法人代表")
    contact_person = fields.CharField(max_length=50, null=True, description="联系人")
    contact_phone = fields.CharField(max_length=50, null=True, description="联系电话")
    contact_email = fields.CharField(max_length=100, null=True, description="联系邮箱")
    industry_type = fields.CharField(max_length=100, null=True, description="行业类型")
    capital = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="注册资本(万元)")
    capacity = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="年产能(万m²)")
    
    # 审核流程状态
    audit_status = fields.CharField(max_length=50, default="pending", description="审核状态", index=True)
    current_step = fields.IntField(default=0, description="当前步骤", index=True)
    
    # 软删除标记
    is_deleted = fields.BooleanField(default=False, description="软删除标记", index=True)
    
    class Meta:
        table = "pcb_enterprise"


class PCBIndicator(BaseModel, TimestampMixin):
    """PCB审核指标表 - 64项指标定义"""
    indicator_id = fields.IntField(unique=True, description="指标编号(1-64)", index=True)
    name = fields.CharField(max_length=200, description="指标名称")
    category = fields.CharField(max_length=100, description="一级指标分类", index=True)
    indicator_type = fields.CharField(max_length=50, description="指标类型", index=True)
    # indicator_type: qualitative(定性), quantitative(定量), limiting(限定性)
    
    unit = fields.CharField(max_length=50, null=True, description="计量单位")
    
    # 权重字段
    category_weight = fields.DecimalField(max_digits=5, decimal_places=3, default=0.0, 
                                         description="一级指标权重")
    weight = fields.DecimalField(max_digits=5, decimal_places=3, default=1.0, 
                                 description="二级指标权重")
    
    # 动态权重标记：某些指标的权重需要根据产量动态计算（带*标记）
    is_dynamic_weight = fields.BooleanField(default=False, 
                                           description="是否需要根据产量动态计算权重")
    
    # 评级标准（JSON格式存储不同等级的标准值）
    level_standards = fields.JSONField(null=True, description="评级标准")
    
    is_limiting = fields.BooleanField(default=False, description="是否为限定性指标", index=True)
    description = fields.TextField(null=True, description="指标说明")
    
    # 排序
    order = fields.IntField(default=0, description="排序", index=True)
    
    class Meta:
        table = "pcb_indicator"


class PCBAuditResult(BaseModel, TimestampMixin):
    """PCB审核结果表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    indicator_id = fields.BigIntField(description="指标ID", index=True)
    
    # 审核数据
    current_value = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="当前值")
    level = fields.CharField(max_length=50, null=True, description="评级结果", index=True)
    # level: I级, II级, III级, 不达标, 待评估
    
    score = fields.DecimalField(max_digits=5, decimal_places=2, default=0, description="得分")
    
    # 审核意见
    comment = fields.TextField(null=True, description="审核意见")
    manual_override = fields.BooleanField(default=False, description="是否手动调整")
    override_reason = fields.TextField(null=True, description="调整原因")
    
    # 方案选择
    selected_scheme_ids = fields.JSONField(null=True, description="选择的方案ID列表")
    scheme_selection_date = fields.DatetimeField(null=True, description="方案选择时间")
    
    # 审核人信息
    auditor_id = fields.BigIntField(null=True, description="审核人ID", index=True)
    audit_date = fields.DatetimeField(null=True, description="审核时间")
    
    class Meta:
        table = "pcb_audit_result"
        unique_together = (("enterprise_id", "indicator_id"),)


class PCBScheme(BaseModel, TimestampMixin):
    """PCB清洁生产方案表 - 130项方案"""
    scheme_id = fields.IntField(unique=True, description="方案编号(1-130)", index=True)
    name = fields.CharField(max_length=200, description="方案名称", index=True)
    scheme_type = fields.CharField(max_length=100, null=True, description="方案类型")
    
    # 方案内容
    problem = fields.TextField(null=True, description="解决的问题")
    description = fields.TextField(null=True, description="方案简介")
    implementation = fields.TextField(null=True, description="实施方案")
    
    # 经济效益
    economic_benefit = fields.TextField(null=True, description="经济效益")
    investment = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="投资估算(万元)")
    payback_period = fields.DecimalField(max_digits=5, decimal_places=1, null=True, description="投资回收期(年)")
    
    # 环境效益
    environmental_benefit = fields.TextField(null=True, description="环境效益")
    
    # 状态
    is_active = fields.BooleanField(default=True, description="是否启用", index=True)
    
    class Meta:
        table = "pcb_scheme"


class PCBIndicatorSchemeRelation(BaseModel, TimestampMixin):
    """PCB指标与方案关联表"""
    indicator_id = fields.BigIntField(description="指标ID", index=True)
    scheme_id = fields.BigIntField(description="方案ID", index=True)
    relevance_score = fields.DecimalField(max_digits=3, decimal_places=2, default=1.0, description="关联度")
    priority = fields.IntField(default=1, description="优先级(1-10)")
    recommendation_reason = fields.TextField(null=True, description="推荐理由")
    
    class Meta:
        table = "pcb_indicator_scheme_relation"
        unique_together = (("indicator_id", "scheme_id"),)


class PCBEnterpriseScheme(BaseModel, TimestampMixin):
    """PCB企业选择方案记录表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    scheme_id = fields.BigIntField(description="方案ID", index=True)
    indicator_id = fields.BigIntField(null=True, description="关联指标ID", index=True)
    
    # 方案状态
    status = fields.CharField(max_length=50, default="recommended", description="方案状态", index=True)
    # status: recommended(推荐), selected(已选择), implementing(实施中), completed(已完成), rejected(已拒绝)
    
    # 实施信息
    implementation_plan = fields.TextField(null=True, description="实施计划")
    start_date = fields.DateField(null=True, description="开始日期")
    expected_completion_date = fields.DateField(null=True, description="预计完成日期")
    actual_completion_date = fields.DateField(null=True, description="实际完成日期")
    
    # 实施效果
    actual_investment = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="实际投资(万元)")
    actual_benefit = fields.TextField(null=True, description="实际效益")
    
    notes = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_enterprise_scheme"


class PCBPreAuditData(BaseModel, TimestampMixin):
    """PCB预审核数据表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 预审核数据（JSON格式存储）
    production_info = fields.JSONField(null=True, description="企业总体生产情况")
    raw_materials = fields.JSONField(null=True, description="原辅材料使用情况")
    process_equipment = fields.JSONField(null=True, description="主要工艺及装备使用")
    resource_consumption = fields.JSONField(null=True, description="资源能源消耗")
    pollution_control = fields.JSONField(null=True, description="污染防治")
    solid_waste = fields.JSONField(null=True, description="工业固体废物管理")
    self_monitoring = fields.JSONField(null=True, description="自行监测情况")
    
    # 提交状态
    status = fields.CharField(max_length=50, default="draft", description="状态", index=True)
    # status: draft(草稿), submitted(已提交), approved(已审核)
    
    submitted_at = fields.DatetimeField(null=True, description="提交时间")
    approved_at = fields.DatetimeField(null=True, description="审核通过时间")
    
    class Meta:
        table = "pcb_pre_audit_data"


class PCBAuditReport(BaseModel, TimestampMixin):
    """PCB审核报告表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 审核汇总
    total_score = fields.DecimalField(max_digits=5, decimal_places=2, default=0, description="总分")
    overall_level = fields.CharField(max_length=50, null=True, description="综合等级")
    improvement_items = fields.IntField(default=0, description="待改进项数")
    limiting_indicators_count = fields.IntField(default=0, description="限定性指标数量")
    non_compliant_limiting_count = fields.IntField(default=0, description="不达标限定性指标数")
    
    # 报告内容
    summary = fields.JSONField(null=True, description="审核摘要")
    recommendations = fields.TextField(null=True, description="改进建议")
    
    # 报告状态
    status = fields.CharField(max_length=50, default="draft", description="报告状态", index=True)
    # status: draft(草稿), submitted(已提交), approved(已批准)
    
    # 审核人信息
    auditor_id = fields.BigIntField(null=True, description="审核人ID")
    auditor_name = fields.CharField(max_length=100, null=True, description="审核人姓名")
    audit_date = fields.DateField(null=True, description="审核日期")
    
    # 报告文件
    report_file_id = fields.CharField(max_length=200, null=True, description="报告文件ID")
    
    class Meta:
        table = "pcb_audit_report"


class PCBProblemSolutionScoring(BaseModel, TimestampMixin):
    """PCB问题方案权重总和计分排序表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 因素配置（JSON格式存储）
    factors = fields.JSONField(null=True, description="因素列表，格式: [{'key': str, 'name': str, 'weight': int}, ...]")
    
    # 审核重点配置（JSON格式存储）
    focuses = fields.JSONField(null=True, description="审核重点列表，格式: [{'id': int, 'name': str}, ...]")
    
    # 评分矩阵（JSON格式存储）
    # 格式: {focus_id: {factor_key: {'r': int, 'rw': int}, ...}, ...}
    scores = fields.JSONField(null=True, description="评分矩阵")
    
    # 计算结果（JSON格式存储）
    rankings = fields.JSONField(null=True, description="排序结果，格式: [{'id': int, 'name': str, 'total_score': float}, ...]")
    
    class Meta:
        table = "pcb_problem_solution_scoring"
        unique_together = (("enterprise_id",),)


class PCBLowCostScheme(BaseModel, TimestampMixin):
    """PCB无/低费方案表（企业自定义方案）"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 方案来源
    source = fields.CharField(max_length=50, default="custom", description="方案来源")
    # source: custom(自定义), library(方案库导入)
    
    # 如果是从方案库导入，关联方案ID
    scheme_id = fields.BigIntField(null=True, description="关联方案库方案ID", index=True)
    
    # 关联指标ID（用于从方案库导入时，根据指标筛选）
    indicator_ids = fields.JSONField(null=True, description="关联指标ID列表")
    
    # 方案基本信息
    name = fields.CharField(max_length=200, description="方案名称", index=True)
    intro = fields.TextField(null=True, description="方案简介")
    
    # 效益
    economic_benefit = fields.TextField(null=True, description="经济效益")
    environment_benefit = fields.TextField(null=True, description="环境效益")
    
    # 备注
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_low_cost_scheme"


class PCBMediumHighCostScheme(BaseModel, TimestampMixin):
    """PCB中/高费方案表（企业自定义方案）"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 方案来源
    source = fields.CharField(max_length=50, default="custom", description="方案来源")
    # source: custom(自定义), library(方案库导入)
    
    # 费用等级
    cost_level = fields.CharField(max_length=20, default="middle", description="费用等级", index=True)
    # cost_level: middle(中费), high(高费)
    
    # 如果是从方案库导入，关联方案ID
    scheme_id = fields.BigIntField(null=True, description="关联方案库方案ID", index=True)
    
    # 关联指标ID（用于从方案库导入时，根据指标筛选）
    indicator_ids = fields.JSONField(null=True, description="关联指标ID列表")
    
    # 方案基本信息
    name = fields.CharField(max_length=200, description="方案名称", index=True)
    intro = fields.TextField(null=True, description="方案简介")
    
    # 方案内容（仅自定义方案需要）
    problem = fields.TextField(null=True, description="解决的问题")
    content = fields.TextField(null=True, description="方案内容/实施步骤")
    effect = fields.TextField(null=True, description="预期效果")
    
    # 效益
    economic_benefit = fields.TextField(null=True, description="经济效益")
    environment_benefit = fields.TextField(null=True, description="环境效益")
    
    # 备注
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_medium_high_cost_scheme"


