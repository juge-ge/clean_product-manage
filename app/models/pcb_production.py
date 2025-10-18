"""
PCB企业生产情况数据模型
用于存储企业总体生产情况的详细数据
"""
from tortoise import fields
from .base import BaseModel, TimestampMixin


class PCBProductOutput(BaseModel, TimestampMixin):
    """PCB企业产品产量表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 产品信息
    type = fields.CharField(max_length=50, null=True, description="类型(rigid/flexible)", index=True)
    main_product = fields.CharField(max_length=100, null=True, description="主要产品", index=True)
    unit = fields.CharField(max_length=50, null=True, description="单位", index=True)
    year = fields.CharField(max_length=10, null=True, description="年份", index=True)
    output = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="产量")
    layers = fields.IntField(null=True, description="层数")
    
    class Meta:
        table = "pcb_product_output"
        unique_together = (("enterprise_id", "type", "main_product", "year"),)


class PCBQualificationRate(BaseModel, TimestampMixin):
    """PCB企业合格率表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    year = fields.CharField(max_length=10, null=True, description="年份", index=True)
    rate = fields.DecimalField(max_digits=5, decimal_places=2, null=True, description="合格率(%)")
    
    class Meta:
        table = "pcb_qualification_rate"
        unique_together = (("enterprise_id", "year"),)


class PCBOutputValue(BaseModel, TimestampMixin):
    """PCB企业产值情况表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    year = fields.CharField(max_length=10, null=True, description="年份", index=True)
    unit = fields.CharField(max_length=50, null=True, description="单位", index=True)
    annual_output_value = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="年产值")
    income_tax = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="所得税")
    
    class Meta:
        table = "pcb_output_value"
        unique_together = (("enterprise_id", "year"),)
