"""
PCB企业污染防治数据模型
"""
from tortoise import fields
from .base import BaseModel, TimestampMixin


class PCBWastewaterAnalysis(BaseModel, TimestampMixin):
    """PCB企业废水产生分析表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 废水基本信息
    category = fields.CharField(max_length=100, description="废水类别", index=True)
    source = fields.TextField(default="", description="来源")
    pollutants = fields.TextField(default="", description="主要污染物")
    disposal = fields.TextField(default="", description="处置方式")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_wastewater_analysis"


class PCBWasteGasAnalysis(BaseModel, TimestampMixin):
    """PCB企业废气产生情况表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 废气基本信息
    gas_type = fields.CharField(max_length=100, description="种类", index=True)
    pollutants = fields.CharField(max_length=200, default="", description="主要污染物")
    location = fields.TextField(default="", description="产生部位")
    treatment = fields.TextField(default="", description="处理方法")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_waste_gas_analysis"


class PCBWastewaterStatRecord(BaseModel, TimestampMixin):
    """PCB企业近三年废水情况统计记录表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 基本信息
    project = fields.CharField(max_length=100, description="项目名称（生产废水/生活废水）", index=True)
    workshop = fields.CharField(max_length=200, null=True, description="使用车间", index=True)
    unit = fields.CharField(max_length=20, description="单位")
    
    # 年份数据 - 支持年份范围选择
    amount_2020 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2020年用量")
    amount_2021 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2021年用量")
    amount_2022 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2022年用量")
    amount_2023 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2023年用量")
    amount_2024 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2024年用量")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_wastewater_stat_record"