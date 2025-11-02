"""
PCB企业原辅材料使用情况数据模型（三年数据）
用于存储企业近三年原辅材料使用情况
"""
from tortoise import fields
from .base import BaseModel, TimestampMixin


class PCBRawMaterialUsage(BaseModel, TimestampMixin):
    """PCB企业原辅材料使用情况表（三年数据）"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 产品信息
    type = fields.CharField(max_length=50, null=True, description="类型(rigid/flexible)", index=True)
    main_product = fields.CharField(max_length=100, null=True, description="主要产品", index=True)
    product_output = fields.DecimalField(max_digits=15, decimal_places=2, null=True, description="产品产量(m²)")
    
    # 原辅材料信息
    material_name = fields.CharField(max_length=200, null=True, description="原辅材料名称", index=True)
    unit = fields.CharField(max_length=50, null=True, description="单位")
    
    # 年份数据 - 年消耗量
    amount_2020 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2020年消耗量")
    amount_2021 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2021年消耗量")
    amount_2022 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2022年消耗量")
    amount_2023 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2023年消耗量")
    amount_2024 = fields.DecimalField(max_digits=15, decimal_places=4, null=True, description="2024年消耗量")
    
    # 年份数据 - 单位产品消耗量(/m²)
    unitConsumption_2020 = fields.DecimalField(max_digits=15, decimal_places=6, null=True, description="2020年单位产品消耗量")
    unitConsumption_2021 = fields.DecimalField(max_digits=15, decimal_places=6, null=True, description="2021年单位产品消耗量")
    unitConsumption_2022 = fields.DecimalField(max_digits=15, decimal_places=6, null=True, description="2022年单位产品消耗量")
    unitConsumption_2023 = fields.DecimalField(max_digits=15, decimal_places=6, null=True, description="2023年单位产品消耗量")
    unitConsumption_2024 = fields.DecimalField(max_digits=15, decimal_places=6, null=True, description="2024年单位产品消耗量")
    
    class Meta:
        table = "pcb_raw_material_usage"
        unique_together = (("enterprise_id", "type", "main_product", "material_name"),)

