"""
PCB筹划与组织模块API路由
"""
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Optional
import os
import uuid
from datetime import datetime

from app.schemas.base import Success
from app.schemas.pcb_planning import (
    PCBLeadershipTeamCreate,
    PCBLeadershipTeamUpdate,
    PCBLeadershipTeamResponse,
    PCBLeadershipTeamList,
    PCBWorkTeamCreate,
    PCBWorkTeamUpdate,
    PCBWorkTeamResponse,
    PCBWorkTeamList,
    PCBWorkPlanCreate,
    PCBWorkPlanUpdate,
    PCBWorkPlanResponse,
    PCBWorkPlansList,
    PCBWorkPlansUpdate,
    PCBTrainingRecordCreate,
    PCBTrainingRecordUpdate,
    PCBTrainingRecordResponse,
    PCBTrainingRecordsList,
)
from app.controllers.pcb_planning import (
    pcb_leadership_team_controller,
    pcb_work_team_controller,
    pcb_work_plan_controller,
    pcb_training_record_controller,
    pcb_training_image_controller,
)

router = APIRouter()

# ==================== 领导小组 API ====================

@router.get("/enterprise/{enterprise_id}/leadership-team", response_model=PCBLeadershipTeamList, summary="获取领导小组")
async def get_leadership_team(enterprise_id: int):
    """获取企业领导小组成员列表"""
    members = await pcb_leadership_team_controller.get_by_enterprise(enterprise_id)
    return Success(data={
        "total": len(members),
        "items": [await member.to_dict() for member in members]
    })


@router.post("/enterprise/{enterprise_id}/leadership-team", response_model=PCBLeadershipTeamResponse, summary="添加领导小组成员")
async def create_leadership_team_member(enterprise_id: int, member: PCBLeadershipTeamCreate):
    """添加领导小组成员"""
    new_member = await pcb_leadership_team_controller.create_member(enterprise_id, member)
    return Success(data=await new_member.to_dict(), msg="领导小组成员添加成功")


@router.put("/enterprise/{enterprise_id}/leadership-team/{member_id}", response_model=PCBLeadershipTeamResponse, summary="更新领导小组成员")
async def update_leadership_team_member(
    enterprise_id: int, 
    member_id: int, 
    member: PCBLeadershipTeamUpdate
):
    """更新领导小组成员"""
    updated_member = await pcb_leadership_team_controller.update(id=member_id, obj=member)
    if not updated_member:
        raise HTTPException(status_code=404, detail="成员不存在")
    return Success(data=await updated_member.to_dict(), msg="成员信息更新成功")


@router.delete("/enterprise/{enterprise_id}/leadership-team/{member_id}", summary="删除领导小组成员")
async def delete_leadership_team_member(enterprise_id: int, member_id: int):
    """删除领导小组成员"""
    try:
        await pcb_leadership_team_controller.remove(id=member_id)
        return Success(msg="成员删除成功")
    except Exception:
        raise HTTPException(status_code=404, detail="成员不存在")


# ==================== 工作小组 API ====================

@router.get("/enterprise/{enterprise_id}/work-team", response_model=PCBWorkTeamList, summary="获取工作小组")
async def get_work_team(enterprise_id: int):
    """获取企业工作小组成员列表"""
    members = await pcb_work_team_controller.get_by_enterprise(enterprise_id)
    return Success(data={
        "total": len(members),
        "items": [await member.to_dict() for member in members]
    })


@router.post("/enterprise/{enterprise_id}/work-team", response_model=PCBWorkTeamResponse, summary="添加工作小组成员")
async def create_work_team_member(enterprise_id: int, member: PCBWorkTeamCreate):
    """添加工作小组成员"""
    new_member = await pcb_work_team_controller.create_member(enterprise_id, member)
    return Success(data=await new_member.to_dict(), msg="工作小组成员添加成功")


@router.put("/enterprise/{enterprise_id}/work-team/{member_id}", response_model=PCBWorkTeamResponse, summary="更新工作小组成员")
async def update_work_team_member(
    enterprise_id: int, 
    member_id: int, 
    member: PCBWorkTeamUpdate
):
    """更新工作小组成员"""
    updated_member = await pcb_work_team_controller.update(id=member_id, obj=member)
    if not updated_member:
        raise HTTPException(status_code=404, detail="成员不存在")
    return Success(data=await updated_member.to_dict(), msg="成员信息更新成功")


@router.delete("/enterprise/{enterprise_id}/work-team/{member_id}", summary="删除工作小组成员")
async def delete_work_team_member(enterprise_id: int, member_id: int):
    """删除工作小组成员"""
    try:
        await pcb_work_team_controller.remove(id=member_id)
        return Success(msg="成员删除成功")
    except Exception:
        raise HTTPException(status_code=404, detail="成员不存在")


# ==================== 工作计划 API ====================

@router.get("/enterprise/{enterprise_id}/work-plans", response_model=PCBWorkPlansList, summary="获取工作计划")
async def get_work_plans(enterprise_id: int):
    """获取企业工作计划列表"""
    plans = await pcb_work_plan_controller.get_by_enterprise(enterprise_id)
    return Success(data={
        "total": len(plans),
        "items": [await plan.to_dict() for plan in plans]
    })


@router.post("/enterprise/{enterprise_id}/work-plans", response_model=PCBWorkPlanResponse, summary="创建工作计划")
async def create_work_plan(enterprise_id: int, plan: PCBWorkPlanCreate):
    """创建工作计划"""
    new_plan = await pcb_work_plan_controller.create_plan(enterprise_id, plan)
    return Success(data=await new_plan.to_dict(), msg="工作计划创建成功")


@router.put("/enterprise/{enterprise_id}/work-plans", response_model=PCBWorkPlansList, summary="批量更新工作计划")
async def update_work_plans(enterprise_id: int, plans_data: PCBWorkPlansUpdate):
    """批量更新工作计划"""
    updated_plans = await pcb_work_plan_controller.update_plans(enterprise_id, plans_data.work_plans)
    return Success(data={
        "total": len(updated_plans),
        "items": [await plan.to_dict() for plan in updated_plans]
    }, msg="工作计划更新成功")


@router.put("/enterprise/{enterprise_id}/work-plans/reorder", response_model=PCBWorkPlansList, summary="重新排序工作计划")
async def reorder_work_plans(enterprise_id: int):
    """重新排序工作计划阶段"""
    reordered_plans = await pcb_work_plan_controller.reorder_stages(enterprise_id)
    return Success(data={
        "total": len(reordered_plans),
        "items": [await plan.to_dict() for plan in reordered_plans]
    }, msg="阶段顺序调整成功")


@router.delete("/enterprise/{enterprise_id}/work-plans/{plan_id}", summary="删除工作计划")
async def delete_work_plan(enterprise_id: int, plan_id: int):
    """删除工作计划"""
    try:
        await pcb_work_plan_controller.remove(id=plan_id)
        return Success(msg="工作计划删除成功")
    except Exception:
        raise HTTPException(status_code=404, detail="工作计划不存在")


# ==================== 培训记录 API ====================

@router.get("/enterprise/{enterprise_id}/training-records", response_model=PCBTrainingRecordsList, summary="获取培训记录")
async def get_training_records(enterprise_id: int):
    """获取企业培训记录列表"""
    records = await pcb_training_record_controller.get_by_enterprise(enterprise_id)
    
    # 为每个记录添加图片信息
    records_with_images = []
    for record in records:
        record_dict = await record.to_dict()
        images = await pcb_training_image_controller.get_by_training(record.id)
        record_dict["images"] = [await image.to_dict() for image in images]
        records_with_images.append(record_dict)
    
    return Success(data={
        "total": len(records_with_images),
        "items": records_with_images
    })


@router.post("/enterprise/{enterprise_id}/training-records", response_model=PCBTrainingRecordResponse, summary="添加培训记录")
async def create_training_record(
    enterprise_id: int,
    title: str = Form(...),
    date: str = Form(...),
    duration: Optional[int] = Form(None),
    participants: Optional[int] = Form(None),
    content: Optional[str] = Form(None),
    instructor: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    images: List[UploadFile] = File(default=[])
):
    """创建培训记录（支持图片上传）"""
    # 解析日期
    try:
        training_date = datetime.fromisoformat(date.replace('Z', '+00:00'))
    except:
        training_date = datetime.now()
    
    # 创建培训记录
    record_data = PCBTrainingRecordCreate(
        title=title,
        date=training_date,
        duration=duration,
        participants=participants,
        content=content,
        instructor=instructor,
        location=location
    )
    
    new_record = await pcb_training_record_controller.create_record(enterprise_id, record_data)
    
    # 处理上传的图片
    uploaded_images = []
    if images:
        # 创建上传目录
        upload_dir = f"uploads/training/{new_record.id}"
        os.makedirs(upload_dir, exist_ok=True)
        
        for image in images:
            if image.filename:
                # 生成唯一文件名
                file_extension = os.path.splitext(image.filename)[1]
                unique_filename = f"{uuid.uuid4()}{file_extension}"
                file_path = os.path.join(upload_dir, unique_filename)
                
                # 保存文件
                with open(file_path, "wb") as buffer:
                    content = await image.read()
                    buffer.write(content)
                
                # 创建图片记录
                image_record = await pcb_training_image_controller.create_image(
                    training_id=new_record.id,
                    image_path=file_path,
                    image_name=image.filename,
                    image_size=len(content)
                )
                uploaded_images.append(await image_record.to_dict())
    
    # 返回带图片的记录
    record_dict = await new_record.to_dict()
    record_dict["images"] = uploaded_images
    
    return Success(data=record_dict, msg="培训记录创建成功")


@router.put("/enterprise/{enterprise_id}/training-records/{record_id}", response_model=PCBTrainingRecordResponse, summary="更新培训记录")
async def update_training_record(
    enterprise_id: int, 
    record_id: int, 
    record: PCBTrainingRecordUpdate
):
    """更新培训记录"""
    updated_record = await pcb_training_record_controller.update(id=record_id, obj=record)
    if not updated_record:
        raise HTTPException(status_code=404, detail="培训记录不存在")
    
    # 获取图片信息
    images = await pcb_training_image_controller.get_by_training(record_id)
    record_dict = await updated_record.to_dict()
    record_dict["images"] = [await image.to_dict() for image in images]
    
    return Success(data=record_dict, msg="培训记录更新成功")


@router.delete("/enterprise/{enterprise_id}/training-records/{record_id}", summary="删除培训记录")
async def delete_training_record(enterprise_id: int, record_id: int):
    """删除培训记录"""
    # 删除关联的图片文件
    images = await pcb_training_image_controller.get_by_training(record_id)
    for image in images:
        try:
            if os.path.exists(image.image_path):
                os.remove(image.image_path)
        except:
            pass
    
    # 删除记录
    try:
        await pcb_training_record_controller.remove(id=record_id)
        return Success(msg="培训记录删除成功")
    except Exception:
        raise HTTPException(status_code=404, detail="培训记录不存在")


@router.delete("/enterprise/{enterprise_id}/training-records/{record_id}/images/{image_id}", summary="删除培训记录图片")
async def delete_training_image(enterprise_id: int, record_id: int, image_id: int):
    """删除培训图片"""
    # 获取图片信息
    image = await pcb_training_image_controller.get_by_training(record_id)
    target_image = None
    for img in image:
        if img.id == image_id:
            target_image = img
            break
    
    if not target_image:
        raise HTTPException(status_code=404, detail="图片不存在")
    
    # 删除文件
    try:
        if os.path.exists(target_image.image_path):
            os.remove(target_image.image_path)
    except:
        pass
    
    # 删除记录
    success = await pcb_training_image_controller.delete_image(image_id)
    if not success:
        raise HTTPException(status_code=404, detail="图片删除失败")
    
    return Success(msg="图片删除成功")
