"""
PCB审核报告生成API
"""
import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Optional

from app.core.dependency import DependAuth
from app.utils.report_generator import report_generator
from app.schemas.base import Success

router = APIRouter()


@router.get("/enterprise/{enterprise_id}/report/generate", summary="生成审核报告")
async def generate_audit_report(
    enterprise_id: int,
    current_user = DependAuth
):
    """生成PCB清洁生产审核报告"""
    try:
        # 暂时直接从reports文件夹中查找现有报告
        # report_path = await report_generator.generate_report(enterprise_id)
        
        # 查找reports目录中的报告文件
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            raise HTTPException(status_code=404, detail="reports目录不存在")
        
        # 查找匹配的报告文件
        report_files = [f for f in os.listdir(reports_dir) if f.endswith('.docx')]
        
        if not report_files:
            raise HTTPException(status_code=404, detail="未找到报告文件")
        
        # 使用第一个找到的报告文件（或者可以根据企业ID匹配）
        report_filename = report_files[0]
        report_path = os.path.join(reports_dir, report_filename)
        
        return Success(
            data={
                "report_path": report_path,
                "report_filename": report_filename
            },
            msg="报告获取成功"
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"报告获取失败: {str(e)}")


@router.get("/enterprise/{enterprise_id}/report/download", summary="下载审核报告")
async def download_audit_report(
    enterprise_id: int,
    current_user = DependAuth
):
    """下载PCB清洁生产审核报告"""
    try:
        # 暂时直接从reports文件夹中查找现有报告
        # report_path = await report_generator.generate_report(enterprise_id)
        
        # 查找reports目录中的报告文件
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            raise HTTPException(status_code=404, detail="reports目录不存在")
        
        # 查找匹配的报告文件
        report_files = [f for f in os.listdir(reports_dir) if f.endswith('.docx')]
        
        if not report_files:
            raise HTTPException(status_code=404, detail="未找到报告文件")
        
        # 使用第一个找到的报告文件
        report_filename = report_files[0]
        report_path = os.path.join(reports_dir, report_filename)
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="报告文件不存在")
        
        return FileResponse(
            path=report_path,
            filename=report_filename,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"报告下载失败: {str(e)}")


@router.get("/enterprise/{enterprise_id}/report/preview", summary="预览审核报告")
async def preview_audit_report(
    enterprise_id: int,
    current_user = DependAuth
):
    """预览PCB清洁生产审核报告内容"""
    try:
        from app.models.pcb import PCBEnterprise, PCBPreAuditData, PCBAuditResult, PCBAuditReport
        from app.models.pcb_planning import PCBLeadershipTeam, PCBWorkTeam, PCBWorkPlan, PCBTrainingRecord
        
        # 获取企业信息
        enterprise = await PCBEnterprise.get_or_none(id=enterprise_id)
        if not enterprise:
            raise HTTPException(status_code=404, detail=f"企业ID {enterprise_id} 不存在")
        
        # 获取筹划与组织数据
        leadership_team = await PCBLeadershipTeam.filter(enterprise_id=enterprise_id)
        work_team = await PCBWorkTeam.filter(enterprise_id=enterprise_id)
        work_plans = await PCBWorkPlan.filter(enterprise_id=enterprise_id).order_by('stage_order')
        training_records = await PCBTrainingRecord.filter(enterprise_id=enterprise_id)
        
        # 获取预审核数据
        pre_audit_data = await PCBPreAuditData.get_or_none(enterprise_id=enterprise_id)
        
        # 获取审核结果
        audit_results = await PCBAuditResult.filter(enterprise_id=enterprise_id)
        
        # 获取审核报告
        audit_report = await PCBAuditReport.get_or_none(enterprise_id=enterprise_id)
        
        # 构建预览数据
        preview_data = {
            "enterprise_info": {
                "name": enterprise.name,
                "unified_social_credit_code": enterprise.unified_social_credit_code,
                "region": enterprise.region,
                "district": enterprise.district,
                "address": enterprise.address,
                "legal_representative": enterprise.legal_representative,
                "contact_person": enterprise.contact_person,
                "contact_phone": enterprise.contact_phone,
                "capacity": enterprise.capacity,
                "audit_status": enterprise.audit_status
            },
            "planning_organization": {
                "leadership_team_count": len(leadership_team),
                "work_team_count": len(work_team),
                "work_plans_count": len(work_plans),
                "training_records_count": len(training_records)
            },
            "pre_audit_data": {
                "has_data": pre_audit_data is not None,
                "status": pre_audit_data.status if pre_audit_data else None,
                "has_production_info": pre_audit_data.production_info is not None if pre_audit_data else False,
                "has_raw_materials": pre_audit_data.raw_materials is not None if pre_audit_data else False,
                "has_process_equipment": pre_audit_data.process_equipment is not None if pre_audit_data else False,
                "has_resource_consumption": pre_audit_data.resource_consumption is not None if pre_audit_data else False,
                "has_pollution_control": pre_audit_data.pollution_control is not None if pre_audit_data else False,
                "has_solid_waste": pre_audit_data.solid_waste is not None if pre_audit_data else False,
                "has_self_monitoring": pre_audit_data.self_monitoring is not None if pre_audit_data else False
            },
            "audit_results": {
                "total_indicators": len(audit_results),
                "completed_indicators": len([r for r in audit_results if r.level]),
                "has_audit_report": audit_report is not None,
                "total_score": audit_report.total_score if audit_report else None,
                "overall_level": audit_report.overall_level if audit_report else None
            }
        }
        
        return Success(data=preview_data, msg="报告预览数据获取成功")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"报告预览失败: {str(e)}")
