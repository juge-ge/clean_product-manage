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
    source = fields.TextField(description="来源")
    pollutants = fields.TextField(description="主要污染物")
    disposal = fields.TextField(description="处置方式")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_wastewater_analysis"


class PCBWasteGasAnalysis(BaseModel, TimestampMixin):
    """PCB企业废气产生情况表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 废气基本信息
    gas_type = fields.CharField(max_length=100, description="种类", index=True)
    pollutants = fields.CharField(max_length=200, description="主要污染物")
    location = fields.TextField(description="产生部位")
    treatment = fields.TextField(description="处理方法")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_waste_gas_analysis"
