"""
PCB企业资源利用数据模型
用于存储能源消耗、新鲜水耗、废水总量、废水中总铜浓度、废水中COD浓度、原/辅料消耗数据
"""
from tortoise import fields
from .base import BaseModel, TimestampMixin


class PCBEnergyConsumption(BaseModel, TimestampMixin):
    """PCB企业能源消耗表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 产品信息
    type = fields.CharField(max_length=50, description="类型(rigid/flexible)", index=True)
    main_product = fields.CharField(max_length=100, description="主要产品", index=True)
    layers = fields.IntField(description="层数")
    
    # 消耗数据
    output = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="产量(m²)")
    electricity = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="耗电量")
    unit_consumption = fields.DecimalField(max_digits=10, decimal_places=6, null=True, description="单位产品消耗量")
    
    # 评定等级
    rating = fields.CharField(max_length=20, null=True, description="评定等级(level1/level2/level3/none)")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_energy_consumption"


class PCBFreshWaterConsumption(BaseModel, TimestampMixin):
    """PCB企业新鲜水耗表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 产品信息
    product = fields.CharField(max_length=50, description="产品名称(single/double/multilayer/hdi)", index=True)
    layers = fields.IntField(description="层数")
    
    # 消耗数据
    output = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="产量(m²)")
    fresh_water = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="新鲜水耗(m³)")
    unit_fresh_water = fields.DecimalField(max_digits=10, decimal_places=6, null=True, description="单位产品新鲜水耗(m³/m²)")
    
    # 评定等级
    rating = fields.CharField(max_length=20, null=True, description="评定等级(level1/level2/level3/none)")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_fresh_water_consumption"


class PCBWastewaterTotalConsumption(BaseModel, TimestampMixin):
    """PCB企业废水总量表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 产品信息
    product = fields.CharField(max_length=50, description="产品名称(single/double/multilayer/hdi)", index=True)
    layers = fields.IntField(description="层数")
    
    # 消耗数据
    output = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="产量(m²)")
    wastewater_total = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="废水总量(m³)")
    unit_wastewater = fields.DecimalField(max_digits=10, decimal_places=6, null=True, description="单位产品废水量(m³/m²)")
    
    # 评定等级
    rating = fields.CharField(max_length=20, null=True, description="评定等级(level1/level2/level3/none)")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_wastewater_total_consumption"


class PCBWastewaterCuConsumption(BaseModel, TimestampMixin):
    """PCB企业废水中总铜浓度表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 产品信息
    product = fields.CharField(max_length=50, description="产品名称(single/double/multilayer/hdi)", index=True)
    layers = fields.IntField(description="层数")
    
    # 消耗数据
    output = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="产量(m²)")
    wastewater_total = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="废水总量(m³)")
    wastewater_cu = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="废水中总铜浓度(g/m³)")
    unit_cu = fields.DecimalField(max_digits=10, decimal_places=6, null=True, description="单位产品废水铜产生量(g/m²)")
    
    # 评定等级
    rating = fields.CharField(max_length=20, null=True, description="评定等级(level1/level2/level3/none)")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_wastewater_cu_consumption"


class PCBWastewaterCODConsumption(BaseModel, TimestampMixin):
    """PCB企业废水中COD浓度表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 产品信息
    product = fields.CharField(max_length=50, description="产品名称(single/double/multilayer/hdi)", index=True)
    layers = fields.IntField(description="层数")
    
    # 消耗数据
    output = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="产量(m²)")
    wastewater_total = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="废水总量(m³)")
    wastewater_cod = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="废水中总COD浓度(g/m³)")
    unit_cod = fields.DecimalField(max_digits=10, decimal_places=6, null=True, description="单位产品COD产生量(g/m²)")
    
    # 评定等级
    rating = fields.CharField(max_length=20, null=True, description="评定等级(level1/level2/level3/none)")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_wastewater_cod_consumption"


class PCBRawMaterialConsumption(BaseModel, TimestampMixin):
    """PCB企业原/辅料消耗（覆铜板）表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 产品信息
    type = fields.CharField(max_length=50, description="类型(rigid/flexible)", index=True)
    main_product = fields.CharField(max_length=100, description="主要产品", index=True)
    layers = fields.IntField(description="层数")
    
    # 消耗数据
    output = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="产量(m²)")
    ccl_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="覆铜板消耗量(m²)")
    ccl_utilization = fields.DecimalField(max_digits=5, decimal_places=2, null=True, description="覆铜板利用率(%)")
    
    # 评定等级
    rating = fields.CharField(max_length=20, null=True, description="评定等级(level1/level2/level3/none)")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_raw_material_consumption"

