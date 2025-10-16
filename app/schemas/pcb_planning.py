"""
PCB筹划与组织模块Pydantic Schemas
"""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field


# ==================== 领导小组 Schemas ====================

class PCBLeadershipTeamBase(BaseModel):
    """领导小组基础Schema"""
    name: str = Field(..., description="成员姓名")
    position: Optional[str] = Field(None, description="职位")
    department: Optional[str] = Field(None, description="部门")
    role: str = Field(..., description="角色(组长/副组长/成员)")
    responsibilities: Optional[str] = Field(None, description="职责描述")
    phone: Optional[str] = Field(None, description="联系电话")


class PCBLeadershipTeamCreate(PCBLeadershipTeamBase):
    """创建领导小组成员请求Schema"""
    pass


class PCBLeadershipTeamUpdate(BaseModel):
    """更新领导小组成员请求Schema"""
    name: Optional[str] = Field(None, description="成员姓名")
    position: Optional[str] = Field(None, description="职位")
    department: Optional[str] = Field(None, description="部门")
    role: Optional[str] = Field(None, description="角色")
    responsibilities: Optional[str] = Field(None, description="职责描述")
    phone: Optional[str] = Field(None, description="联系电话")


class PCBLeadershipTeamResponse(PCBLeadershipTeamBase):
    """领导小组成员响应Schema"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime


# ==================== 工作小组 Schemas ====================

class PCBWorkTeamBase(BaseModel):
    """工作小组基础Schema"""
    name: str = Field(..., description="成员姓名")
    position: Optional[str] = Field(None, description="职位")
    department: Optional[str] = Field(None, description="部门")
    role: str = Field(..., description="角色(组长/副组长/成员)")
    responsibilities: Optional[str] = Field(None, description="职责描述")
    phone: Optional[str] = Field(None, description="联系电话")


class PCBWorkTeamCreate(PCBWorkTeamBase):
    """创建工作小组成员请求Schema"""
    pass


class PCBWorkTeamUpdate(BaseModel):
    """更新工作小组成员请求Schema"""
    name: Optional[str] = Field(None, description="成员姓名")
    position: Optional[str] = Field(None, description="职位")
    department: Optional[str] = Field(None, description="部门")
    role: Optional[str] = Field(None, description="角色")
    responsibilities: Optional[str] = Field(None, description="职责描述")
    phone: Optional[str] = Field(None, description="联系电话")


class PCBWorkTeamResponse(PCBWorkTeamBase):
    """工作小组成员响应Schema"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime


# ==================== 工作计划 Schemas ====================

class PCBWorkPlanBase(BaseModel):
    """工作计划基础Schema"""
    stage_order: int = Field(..., ge=1, le=10, description="阶段顺序(1-10)")
    stage: str = Field(..., description="阶段名称")
    work_content: Optional[str] = Field(None, description="工作内容")
    planned_start_date: Optional[datetime] = Field(None, description="计划开始时间")
    planned_end_date: Optional[datetime] = Field(None, description="计划结束时间")
    responsible_department: Optional[str] = Field(None, description="责任部门")
    actual_start_date: Optional[datetime] = Field(None, description="实际开始时间")
    actual_end_date: Optional[datetime] = Field(None, description="实际结束时间")


class PCBWorkPlanCreate(PCBWorkPlanBase):
    """创建工作计划请求Schema"""
    pass


class PCBWorkPlanUpdate(BaseModel):
    """更新工作计划请求Schema"""
    stage_order: Optional[int] = Field(None, ge=1, le=10, description="阶段顺序")
    stage: Optional[str] = Field(None, description="阶段名称")
    work_content: Optional[str] = Field(None, description="工作内容")
    planned_start_date: Optional[datetime] = Field(None, description="计划开始时间")
    planned_end_date: Optional[datetime] = Field(None, description="计划结束时间")
    responsible_department: Optional[str] = Field(None, description="责任部门")
    actual_start_date: Optional[datetime] = Field(None, description="实际开始时间")
    actual_end_date: Optional[datetime] = Field(None, description="实际结束时间")


class PCBWorkPlanResponse(PCBWorkPlanBase):
    """工作计划响应Schema"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime


class PCBWorkPlansUpdate(BaseModel):
    """批量更新工作计划请求Schema"""
    work_plans: List[PCBWorkPlanUpdate] = Field(..., description="工作计划列表")


# ==================== 培训记录 Schemas ====================

class PCBTrainingImageResponse(BaseModel):
    """培训图片响应Schema"""
    id: int
    image_path: str
    image_name: Optional[str]
    image_size: Optional[int]
    upload_time: datetime


class PCBTrainingRecordBase(BaseModel):
    """培训记录基础Schema"""
    title: str = Field(..., description="培训标题")
    date: datetime = Field(..., description="培训日期")
    duration: Optional[int] = Field(None, description="培训时长(分钟)")
    participants: Optional[int] = Field(None, description="参与人数")
    content: Optional[str] = Field(None, description="培训内容")
    instructor: Optional[str] = Field(None, description="培训讲师")
    location: Optional[str] = Field(None, description="培训地点")


class PCBTrainingRecordCreate(PCBTrainingRecordBase):
    """创建培训记录请求Schema"""
    pass


class PCBTrainingRecordUpdate(BaseModel):
    """更新培训记录请求Schema"""
    title: Optional[str] = Field(None, description="培训标题")
    date: Optional[datetime] = Field(None, description="培训日期")
    duration: Optional[int] = Field(None, description="培训时长")
    participants: Optional[int] = Field(None, description="参与人数")
    content: Optional[str] = Field(None, description="培训内容")
    instructor: Optional[str] = Field(None, description="培训讲师")
    location: Optional[str] = Field(None, description="培训地点")


class PCBTrainingRecordResponse(PCBTrainingRecordBase):
    """培训记录响应Schema"""
    id: int
    enterprise_id: int
    created_at: datetime
    updated_at: datetime
    images: List[PCBTrainingImageResponse] = Field(default_factory=list, description="培训图片")


# ==================== 列表响应 Schemas ====================

class PCBLeadershipTeamList(BaseModel):
    """领导小组列表响应Schema"""
    total: int
    items: List[PCBLeadershipTeamResponse]


class PCBWorkTeamList(BaseModel):
    """工作小组列表响应Schema"""
    total: int
    items: List[PCBWorkTeamResponse]


class PCBWorkPlansList(BaseModel):
    """工作计划列表响应Schema"""
    total: int
    items: List[PCBWorkPlanResponse]


class PCBTrainingRecordsList(BaseModel):
    """培训记录列表响应Schema"""
    total: int
    items: List[PCBTrainingRecordResponse]
