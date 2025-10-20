"""
PCB企业工艺装备数据模型
"""
from tortoise import fields
from .base import BaseModel, TimestampMixin


class PCBEquipmentRecord(BaseModel, TimestampMixin):
    """PCB企业设备记录表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 设备基本信息
    equipment_name = fields.CharField(max_length=100, description="设备名称", index=True)
    equipment_model = fields.CharField(max_length=200, description="设备型号")
    motor_model = fields.CharField(max_length=100, description="电机型号")
    power = fields.DecimalField(max_digits=10, decimal_places=1, null=True, description="功率(KW)")
    quantity = fields.IntField(default=1, description="数量")
    process = fields.CharField(max_length=100, description="应用工艺")
    status = fields.CharField(max_length=50, default="良好", description="运行状况")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_equipment_record"


class PCBEquipmentCategory(BaseModel, TimestampMixin):
    """PCB设备分类表"""
    name = fields.CharField(max_length=100, description="分类名称", unique=True)
    description = fields.TextField(null=True, description="分类描述")
    sort_order = fields.IntField(default=0, description="排序")
    
    class Meta:
        table = "pcb_equipment_category"
