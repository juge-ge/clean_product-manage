"""
PCB筹划与组织模块数据模型
"""
from tortoise import fields
from app.models.base import BaseModel, TimestampMixin


class PCBLeadershipTeam(BaseModel, TimestampMixin):
    """PCB领导小组表"""
    enterprise_id = fields.IntField(description="企业ID", index=True)
    name = fields.CharField(max_length=100, description="成员姓名")
    position = fields.CharField(max_length=100, null=True, description="职位")
    department = fields.CharField(max_length=100, null=True, description="部门")
    role = fields.CharField(max_length=50, description="角色(组长/副组长/成员)")
    responsibilities = fields.TextField(null=True, description="职责描述")
    phone = fields.CharField(max_length=20, null=True, description="联系电话")
    
    class Meta:
        table = "pcb_leadership_team"


class PCBWorkTeam(BaseModel, TimestampMixin):
    """PCB工作小组表"""
    enterprise_id = fields.IntField(description="企业ID", index=True)
    name = fields.CharField(max_length=100, description="成员姓名")
    position = fields.CharField(max_length=100, null=True, description="职位")
    department = fields.CharField(max_length=100, null=True, description="部门")
    role = fields.CharField(max_length=50, description="角色(组长/副组长/成员)")
    responsibilities = fields.TextField(null=True, description="职责描述")
    phone = fields.CharField(max_length=20, null=True, description="联系电话")
    
    class Meta:
        table = "pcb_work_team"


class PCBWorkPlan(BaseModel, TimestampMixin):
    """PCB工作计划表"""
    enterprise_id = fields.IntField(description="企业ID", index=True)
    stage_order = fields.IntField(description="阶段顺序(1-10)")
    stage = fields.CharField(max_length=100, description="阶段名称")
    work_content = fields.TextField(null=True, description="工作内容")
    planned_start_date = fields.DatetimeField(null=True, description="计划开始时间")
    planned_end_date = fields.DatetimeField(null=True, description="计划结束时间")
    responsible_department = fields.CharField(max_length=100, null=True, description="责任部门")
    actual_start_date = fields.DatetimeField(null=True, description="实际开始时间")
    actual_end_date = fields.DatetimeField(null=True, description="实际结束时间")
    
    class Meta:
        table = "pcb_work_plans"


class PCBTrainingRecord(BaseModel, TimestampMixin):
    """PCB培训记录表"""
    enterprise_id = fields.IntField(description="企业ID", index=True)
    title = fields.CharField(max_length=200, description="培训标题")
    date = fields.DatetimeField(description="培训日期")
    duration = fields.IntField(null=True, description="培训时长(分钟)")
    participants = fields.IntField(null=True, description="参与人数")
    content = fields.TextField(null=True, description="培训内容")
    instructor = fields.CharField(max_length=100, null=True, description="培训讲师")
    location = fields.CharField(max_length=200, null=True, description="培训地点")
    
    class Meta:
        table = "pcb_training_records"


class PCBTrainingImage(BaseModel):
    """PCB培训图片表"""
    training_id = fields.IntField(description="培训记录ID", index=True)
    image_path = fields.TextField(description="图片路径")
    image_name = fields.CharField(max_length=200, null=True, description="图片名称")
    image_size = fields.IntField(null=True, description="图片大小(字节)")
    upload_time = fields.DatetimeField(auto_now_add=True, description="上传时间")
    
    class Meta:
        table = "pcb_training_images"
