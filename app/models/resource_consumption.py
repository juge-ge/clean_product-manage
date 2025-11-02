"""
PCB企业资源能源消耗数据模型
用于存储企业用水、用电、天然气消耗的详细数据
"""
from tortoise import fields
from .base import BaseModel, TimestampMixin


class PCBWaterConsumptionRecord(BaseModel, TimestampMixin):
    """PCB企业用水消耗记录表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 基本信息
    project = fields.CharField(max_length=100, description="项目名称（生产用水/生活用水）", index=True)
    workshop = fields.CharField(max_length=200, null=True, description="使用车间", index=True)
    unit = fields.CharField(max_length=20, description="单位")
    
    # 年份数据 - 支持年份范围选择
    amount_2020 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2020年用量")
    amount_2021 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2021年用量")
    amount_2022 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2022年用量")
    amount_2023 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2023年用量")
    amount_2024 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2024年用量")
    
    # 其他信息
    water_type = fields.CharField(max_length=50, null=True, description="用水类型")
    source = fields.CharField(max_length=200, null=True, description="用水来源")
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_water_consumption_record"


class PCBElectricityConsumptionRecord(BaseModel, TimestampMixin):
    """PCB企业用电消耗记录表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 基本信息
    project = fields.CharField(max_length=100, description="项目名称（生产用电/非直接生产用电）", index=True)
    workshop = fields.CharField(max_length=200, null=True, description="使用车间", index=True)
    unit = fields.CharField(max_length=20, description="单位")
    
    # 年份数据 - 支持年份范围选择
    amount_2020 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2020年用量")
    amount_2021 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2021年用量")
    amount_2022 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2022年用量")
    amount_2023 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2023年用量")
    amount_2024 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2024年用量")
    
    # 其他信息
    electricity_type = fields.CharField(max_length=50, null=True, description="用电类型")
    region = fields.CharField(max_length=100, null=True, description="区域")
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_electricity_consumption_record"


class PCBGasConsumptionRecord(BaseModel, TimestampMixin):
    """PCB企业天然气消耗记录表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 基本信息
    project = fields.CharField(max_length=100, description="项目名称（生产用气/非直接生产用气）", index=True)
    workshop = fields.CharField(max_length=200, null=True, description="使用车间", index=True)
    unit = fields.CharField(max_length=20, description="单位")
    
    # 年份数据 - 支持年份范围选择
    amount_2020 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2020年用量")
    amount_2021 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2021年用量")
    amount_2022 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2022年用量")
    amount_2023 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2023年用量")
    amount_2024 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2024年用量")
    
    # 其他信息
    gas_type = fields.CharField(max_length=50, null=True, description="燃气类型")
    source = fields.CharField(max_length=200, null=True, description="燃气来源")
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_gas_consumption_record"


class PCBResourceConsumptionSummary(BaseModel, TimestampMixin):
    """PCB企业资源能源消耗汇总表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    year = fields.IntField(description="年份", index=True)
    
    # 用水汇总
    total_water_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="总用水量")
    production_water_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="生产用水量")
    domestic_water_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="生活用水量")
    water_reuse_rate = fields.DecimalField(max_digits=5, decimal_places=2, null=True, description="水资源重复利用率(%)")
    
    # 用电汇总
    total_electricity_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="总用电量")
    production_electricity_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="生产用电量")
    auxiliary_electricity_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="辅助生产用电量")
    office_electricity_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="办公用电量")
    
    # 天然气汇总
    total_gas_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="总天然气用量")
    production_gas_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="生产用气量")
    domestic_gas_consumption = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="生活用气量")
    
    # 计算指标
    water_consumption_per_unit = fields.DecimalField(max_digits=10, decimal_places=4, null=True, description="单位产品水耗(m³/m²)")
    electricity_consumption_per_unit = fields.DecimalField(max_digits=10, decimal_places=4, null=True, description="单位产品电耗(kWh/m²)")
    gas_consumption_per_unit = fields.DecimalField(max_digits=10, decimal_places=4, null=True, description="单位产品气耗(m³/m²)")
    
    class Meta:
        table = "pcb_resource_consumption_summary"
        unique_together = (("enterprise_id", "year"),)
