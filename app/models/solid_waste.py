"""
PCB企业固体废物管理数据模型
"""
from tortoise import fields
from .base import BaseModel, TimestampMixin


class PCBSolidWasteRecord(BaseModel, TimestampMixin):
    """PCB企业固体废物记录表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 废物基本信息
    category = fields.CharField(max_length=50, description="类别", index=True)
    name = fields.CharField(max_length=100, description="名称", index=True)
    unit = fields.CharField(max_length=20, description="单位")
    
    # 年份数据 - 支持年份范围选择
    amount_2020 = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="2020年用量")
    amount_2021 = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="2021年用量")
    amount_2022 = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="2022年用量")
    amount_2023 = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="2023年用量")
    amount_2024 = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="2024年用量")
    
    # 处置信息
    disposal_method = fields.CharField(max_length=200, null=True, description="处置方式")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_solid_waste_record"


class PCBSolidWasteCategory(BaseModel, TimestampMixin):
    """PCB固体废物分类表"""
    name = fields.CharField(max_length=50, description="分类名称", unique=True)
    description = fields.TextField(null=True, description="分类描述")
    sort_order = fields.IntField(default=0, description="排序")
    
    class Meta:
        table = "pcb_solid_waste_category"
