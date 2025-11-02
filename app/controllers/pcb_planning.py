"""
PCB筹划与组织模块Controller
"""
from datetime import datetime
from typing import Dict, List, Optional

from tortoise.expressions import Q
from app.core.crud import CRUDBase
from app.models.pcb_planning import (
    PCBLeadershipTeam,
    PCBWorkTeam,
    PCBWorkPlan,
    PCBTrainingRecord,
    PCBTrainingImage,
)
from app.schemas.pcb_planning import (
    PCBLeadershipTeamCreate,
    PCBLeadershipTeamUpdate,
    PCBWorkTeamCreate,
    PCBWorkTeamUpdate,
    PCBWorkPlanCreate,
    PCBWorkPlanUpdate,
    PCBTrainingRecordCreate,
    PCBTrainingRecordUpdate,
)


class PCBLeadershipTeamController(CRUDBase[PCBLeadershipTeam, PCBLeadershipTeamCreate, PCBLeadershipTeamUpdate]):
    """PCB领导小组控制器"""

    def __init__(self):
        super().__init__(model=PCBLeadershipTeam)

    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBLeadershipTeam]:
        """获取企业的领导小组成员"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by("role", "id")

    async def create_member(self, enterprise_id: int, member_data: PCBLeadershipTeamCreate) -> PCBLeadershipTeam:
        """创建领导小组成员"""
        member_dict = member_data.dict()
        member_dict["enterprise_id"] = enterprise_id
        return await self.model.create(**member_dict)

    async def remove(self, id: int) -> None:
        """删除成员（覆盖基类，提供更明确的接口）"""
        await super().remove(id=id)


class PCBWorkTeamController(CRUDBase[PCBWorkTeam, PCBWorkTeamCreate, PCBWorkTeamUpdate]):
    """PCB工作小组控制器"""

    def __init__(self):
        super().__init__(model=PCBWorkTeam)

    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWorkTeam]:
        """获取企业的工作小组成员"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by("role", "id")

    async def create_member(self, enterprise_id: int, member_data: PCBWorkTeamCreate) -> PCBWorkTeam:
        """创建工作小组成员"""
        member_dict = member_data.dict()
        member_dict["enterprise_id"] = enterprise_id
        return await self.model.create(**member_dict)

    async def remove(self, id: int) -> None:
        """删除成员（覆盖基类，提供更明确的接口）"""
        await super().remove(id=id)


class PCBWorkPlanController(CRUDBase[PCBWorkPlan, PCBWorkPlanCreate, PCBWorkPlanUpdate]):
    """PCB工作计划控制器"""

    def __init__(self):
        super().__init__(model=PCBWorkPlan)

    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBWorkPlan]:
        """获取企业的工作计划"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by("stage_order")

    async def create_plan(self, enterprise_id: int, plan_data: PCBWorkPlanCreate) -> PCBWorkPlan:
        """创建工作计划"""
        plan_dict = plan_data.dict()
        plan_dict["enterprise_id"] = enterprise_id
        return await self.model.create(**plan_dict)

    async def update_plans(self, enterprise_id: int, plans_data: List) -> List[PCBWorkPlan]:
        """批量更新工作计划"""
        from app.schemas.pcb_planning import PCBWorkPlanUpdate
        
        updated_plans = []
        
        for plan_data in plans_data:
            # 如果是 Pydantic 模型，转换为字典；如果是字典，直接使用
            if isinstance(plan_data, PCBWorkPlanUpdate):
                plan_dict = plan_data.model_dump(exclude_unset=True)
            elif isinstance(plan_data, dict):
                plan_dict = plan_data
            else:
                # 如果是其他类型，尝试转换为字典
                try:
                    plan_dict = plan_data.model_dump(exclude_unset=True) if hasattr(plan_data, 'model_dump') else dict(plan_data)
                except:
                    plan_dict = dict(plan_data)
            
            plan_id = plan_dict.get("id")
            if plan_id:
                # 更新现有计划
                plan = await self.model.get_or_none(id=plan_id, enterprise_id=enterprise_id)
                if plan:
                    for key, value in plan_dict.items():
                        if key != "id" and value is not None:
                            setattr(plan, key, value)
                    plan.updated_at = datetime.now()
                    await plan.save()
                    updated_plans.append(plan)
            else:
                # 创建新计划
                plan_dict_copy = {k: v for k, v in plan_dict.items() if k != "id"}
                plan_dict_copy["enterprise_id"] = enterprise_id
                plan = await self.model.create(**plan_dict_copy)
                updated_plans.append(plan)
        
        return updated_plans

    async def reorder_stages(self, enterprise_id: int) -> List[PCBWorkPlan]:
        """重新排序阶段"""
        plans = await self.get_by_enterprise(enterprise_id)
        for i, plan in enumerate(plans, 1):
            plan.stage_order = i
            plan.updated_at = datetime.now()
            await plan.save()
        return plans

    async def remove(self, id: int) -> None:
        """删除计划（覆盖基类）"""
        await super().remove(id=id)


class PCBTrainingRecordController(CRUDBase[PCBTrainingRecord, PCBTrainingRecordCreate, PCBTrainingRecordUpdate]):
    """PCB培训记录控制器"""

    def __init__(self):
        super().__init__(model=PCBTrainingRecord)

    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBTrainingRecord]:
        """获取企业的培训记录"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by("-date")

    async def remove(self, id: int) -> None:
        """删除培训记录（覆盖基类）"""
        await super().remove(id=id)

    async def create_record(self, enterprise_id: int, record_data: PCBTrainingRecordCreate) -> PCBTrainingRecord:
        """创建培训记录"""
        record_dict = record_data.dict()
        record_dict["enterprise_id"] = enterprise_id
        return await self.model.create(**record_dict)

    async def get_with_images(self, record_id: int) -> Optional[PCBTrainingRecord]:
        """获取带图片的培训记录"""
        record = await self.model.get_or_none(id=record_id)
        if record:
            # 获取关联的图片
            images = await PCBTrainingImage.filter(training_id=record_id).all()
            # 将图片信息添加到记录中
            record.images = images
        return record


class PCBTrainingImageController:
    """PCB培训图片控制器"""

    async def create_image(self, training_id: int, image_path: str, image_name: str = None, image_size: int = None) -> PCBTrainingImage:
        """创建培训图片记录"""
        return await PCBTrainingImage.create(
            training_id=training_id,
            image_path=image_path,
            image_name=image_name,
            image_size=image_size
        )

    async def get_by_training(self, training_id: int) -> List[PCBTrainingImage]:
        """获取培训记录的所有图片"""
        return await PCBTrainingImage.filter(training_id=training_id).all()

    async def delete_image(self, image_id: int) -> bool:
        """删除培训图片"""
        image = await PCBTrainingImage.get_or_none(id=image_id)
        if image:
            await image.delete()
            return True
        return False


# 创建控制器实例
pcb_leadership_team_controller = PCBLeadershipTeamController()
pcb_work_team_controller = PCBWorkTeamController()
pcb_work_plan_controller = PCBWorkPlanController()
pcb_training_record_controller = PCBTrainingRecordController()
pcb_training_image_controller = PCBTrainingImageController()
