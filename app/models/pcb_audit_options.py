"""
PCB审核选项型数据模型
用于存储生产工艺与装备要求、温室气体排放、产品特征、清洁生产管理、资源综合利用等选项型数据
每个模块一个表，存储该模块所有二级指标的选择（JSON格式）
"""
from tortoise import fields
from .base import BaseModel, TimestampMixin


class PCBProcessEquipmentRequirement(BaseModel, TimestampMixin):
    """PCB生产工艺与装备要求表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 6个二级指标，每个存储为JSON字符串（数组格式）
    basic_requirements = fields.JSONField(null=True, description="基本要求")
    mechanical_facilities = fields.JSONField(null=True, description="机械加工及辅助设施")
    printing_process = fields.JSONField(null=True, description="线路与阻焊图形形成")
    cleaning = fields.JSONField(null=True, description="板面清洗")
    etching = fields.JSONField(null=True, description="蚀刻")
    plating = fields.JSONField(null=True, description="电镀与化学镀")
    
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_process_equipment_requirement"
        unique_together = [("enterprise_id",)]


class PCBGreenhouseGasEmission(BaseModel, TimestampMixin):
    """PCB温室气体排放表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 3个二级指标
    carbon_management = fields.JSONField(null=True, description="碳减排管理")
    emission_per_output = fields.JSONField(null=True, description="单位产值碳排放量")
    emission_intensity = fields.JSONField(null=True, description="碳排放强度")
    
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_greenhouse_gas_emission"
        unique_together = [("enterprise_id",)]


class PCBProductCharacteristics(BaseModel, TimestampMixin):
    """PCB产品特征表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 4个二级指标
    auxiliary_material = fields.JSONField(null=True, description="使用无毒无害或低毒低害的生产辅助材料")
    packaging = fields.JSONField(null=True, description="包装")
    hazardous_substance = fields.JSONField(null=True, description="有害物质限制使用")
    product_performance = fields.JSONField(null=True, description="产品性能")
    
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_product_characteristics"
        unique_together = [("enterprise_id",)]


class PCBCleanProductionManagement(BaseModel, TimestampMixin):
    """PCB清洁生产管理表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 11个二级指标
    environmental_law = fields.JSONField(null=True, description="环保法律法规执行情况")
    industrial_policy = fields.JSONField(null=True, description="产业政策符合性")
    clean_production_management = fields.JSONField(null=True, description="清洁生产管理")
    clean_production_audit = fields.JSONField(null=True, description="清洁生产审核")
    energy_management = fields.JSONField(null=True, description="节能管理")
    emission_monitoring = fields.JSONField(null=True, description="污染物排放监测")
    chemical_management = fields.JSONField(null=True, description="危险化学品管理")
    measurement_equipment = fields.JSONField(null=True, description="计量器具配备情况")
    solid_waste_disposal = fields.JSONField(null=True, description="固体废物处理处置")
    soil_pollution_risk = fields.JSONField(null=True, description="土壤污染隐患排查")
    transport_mode = fields.JSONField(null=True, description="运输方式")
    
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_clean_production_management"
        unique_together = [("enterprise_id",)]


class PCBResourceReutilization(BaseModel, TimestampMixin):
    """PCB资源综合利用表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 8个二级指标
    water_reuse = fields.JSONField(null=True, description="水资源重复利用率")
    etching_recovery = fields.JSONField(null=True, description="蚀刻液回收率")
    general_solid_util = fields.JSONField(null=True, description="一般工业固体废物综合利用率")
    wastewater_collection = fields.JSONField(null=True, description="废水收集与处理")
    waste_gas_treatment = fields.JSONField(null=True, description="废气收集与处理")
    general_solid_collection = fields.JSONField(null=True, description="一般固体废物收集与处理")
    hazardous_waste_collection = fields.JSONField(null=True, description="危险废物收集与处理")
    noise = fields.JSONField(null=True, description="噪声")
    
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_resource_reutilization"
        unique_together = [("enterprise_id",)]

