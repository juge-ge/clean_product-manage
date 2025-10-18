from tortoise import fields
from .base import BaseModel, TimestampMixin

class RawMaterial(BaseModel, TimestampMixin):
    """原辅材料基础信息表 - 所有企业共用的材料库"""
    name = fields.CharField(max_length=200, description="材料名称", index=True)
    unit = fields.CharField(max_length=50, description="默认单位", index=True)
    process = fields.CharField(max_length=100, description="适用工序", index=True)
    category = fields.CharField(max_length=100, description="材料类别", index=True)
    description = fields.TextField(null=True, description="材料描述")
    is_active = fields.BooleanField(default=True, description="是否启用")
    
    class Meta:
        table = "raw_materials"

class EnterpriseRawMaterialUsage(BaseModel, TimestampMixin):
    """企业原辅材料使用情况表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    material_id = fields.BigIntField(description="材料ID", index=True)
    year = fields.CharField(max_length=10, description="年份", index=True)
    amount = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="用量")
    unit = fields.CharField(max_length=50, null=True, description="使用单位")
    process = fields.CharField(max_length=100, null=True, description="使用工序")
    state = fields.CharField(max_length=50, null=True, description="状态(固体/液体/气体)")
    voc_content = fields.DecimalField(max_digits=5, decimal_places=2, null=True, description="VOC含量(%)")
    
    # 关系字段 - 使用不同的字段名避免冲突
    material_info = fields.ForeignKeyField("models.RawMaterial", related_name="usage_records", null=True, to_field="id")
    
    class Meta:
        table = "enterprise_raw_material_usage"
        unique_together = (("enterprise_id", "material_id", "year"),)
