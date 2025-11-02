"""
PCB企业自行监测数据模型
"""
from tortoise import fields
from .base import BaseModel, TimestampMixin


class PCBOrganizedGasMonitoring(BaseModel, TimestampMixin):
    """PCB企业有组织废气检测表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 基本信息
    monitoring_point = fields.CharField(max_length=100, description="监测点位", index=True)
    monitoring_time = fields.CharField(max_length=50, description="监测时间")
    
    # 监测项目及化验结果（支持ND值，使用字符串类型）
    nitrogen_oxides = fields.CharField(max_length=50, null=True, description="氮氧化物（支持ND）")
    hydrogen_chloride = fields.CharField(max_length=50, null=True, description="氯化氢（支持ND）")
    hydrogen_cyanide = fields.CharField(max_length=50, null=True, description="氰化氢（支持ND）")
    sulfuric_acid_mist = fields.CharField(max_length=50, null=True, description="硫酸雾（支持ND）")
    chromic_acid_mist = fields.CharField(max_length=50, null=True, description="铬酸雾（支持ND）")
    fluoride = fields.CharField(max_length=50, null=True, description="氟化物（支持ND）")
    phenol = fields.CharField(max_length=50, null=True, description="酚类（支持ND）")
    non_methane_hydrocarbons = fields.CharField(max_length=50, null=True, description="非甲烷总烃（支持ND）")
    benzene = fields.CharField(max_length=50, null=True, description="苯（支持ND）")
    toluene = fields.CharField(max_length=50, null=True, description="甲苯（支持ND）")
    xylene = fields.CharField(max_length=50, null=True, description="二甲苯（支持ND）")
    toluene_xylene_total = fields.CharField(max_length=50, null=True, description="甲苯与二甲苯合计（支持ND）")
    vocs = fields.CharField(max_length=50, null=True, description="VOCs（支持ND）")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_organized_gas_monitoring"


class PCBUnorganizedGasMonitoring(BaseModel, TimestampMixin):
    """PCB企业无组织废气检测表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 基本信息
    sampling_time = fields.CharField(max_length=50, description="采样时间")
    sampling_point = fields.CharField(max_length=100, description="采样点位", index=True)
    monitoring_factor = fields.CharField(max_length=50, description="监测因子", index=True)
    emission_concentration = fields.CharField(max_length=50, null=True, description="排放浓度（mg/m³，支持ND）")
    emission_limit = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="排放浓度限值（mg/m³）")
    compliance = fields.CharField(max_length=20, description="达标情况")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_unorganized_gas_monitoring"


class PCBWastewaterMonitoring(BaseModel, TimestampMixin):
    """PCB企业废水排放监测情况表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 基本信息
    sampling_date = fields.CharField(max_length=50, description="采样日期")
    monitoring_point = fields.CharField(max_length=100, default="", description="监测地点")
    
    # 检测结果（单位：mg/L）
    ph = fields.DecimalField(max_digits=5, decimal_places=2, null=True, description="pH")
    cod = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="COD")
    ammonia_nitrogen = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="氨氮")
    total_phosphorus = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="总磷")
    total_nitrogen = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="总氮")
    total_cyanide = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="总氰化物")
    total_copper = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="总铜")
    nickel = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="镍")
    nickel_outlet = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="镍（镍排口）")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_wastewater_monitoring"


class PCBGasEmissionMonitoring(BaseModel, TimestampMixin):
    """PCB企业废气排放监测情况表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 基本信息
    detection_point = fields.CharField(max_length=100, description="检测点位", index=True)
    detection_item = fields.CharField(max_length=100, description="检测项目")
    emission_rate = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="排放速率（kg/h）")
    benchmark_flow = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="标杆流量（m³/h）")
    detection_result = fields.CharField(max_length=50, null=True, description="检测结果（支持ND）")
    permitted_emission_limit = fields.DecimalField(max_digits=10, decimal_places=2, null=True, description="许可排放浓度限值")
    stack_height = fields.DecimalField(max_digits=8, decimal_places=1, null=True, description="排气筒高（m）")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_gas_emission_monitoring"


class PCBNoiseMonitoring(BaseModel, TimestampMixin):
    """PCB企业近三年厂界噪声监测情况表"""
    enterprise_id = fields.BigIntField(description="企业ID", index=True)
    
    # 基本信息
    monitoring_time = fields.CharField(max_length=50, description="监测时间")
    monitoring_point = fields.CharField(max_length=100, description="监测点位", index=True)
    
    # 检测结果 Leq（dB（A））
    daytime_result = fields.DecimalField(max_digits=5, decimal_places=1, null=True, description="昼间检测结果")
    nighttime_result = fields.DecimalField(max_digits=5, decimal_places=1, null=True, description="夜间检测结果")
    
    # 排放标准 Leq（dB（A））
    daytime_standard = fields.DecimalField(max_digits=5, decimal_places=1, null=True, description="昼间排放标准")
    nighttime_standard = fields.DecimalField(max_digits=5, decimal_places=1, null=True, description="夜间排放标准")
    
    # 其他信息
    remark = fields.TextField(null=True, description="备注")
    
    class Meta:
        table = "pcb_noise_monitoring"
