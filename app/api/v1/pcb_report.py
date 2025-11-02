"""
PCB审核报告生成API
支持报告生成、预览、导出Word功能
"""
import os
from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import FileResponse
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

from app.core.dependency import DependAuth
from app.schemas.base import Success
from app.utils.word_report_generator import PCBWordReportGenerator

router = APIRouter()


class ReportGenerateRequest(BaseModel):
    """报告生成请求"""
    sections: List[str] = Field(default_factory=lambda: ["enterprise", "planning", "preaudit", "audit", "problem"], description="包含的模块列表")
    include_tables: bool = Field(default=True, description="是否包含详细表格")
    include_charts: bool = Field(default=True, description="是否包含图表")
    include_recommendations: bool = Field(default=True, description="是否包含改进建议")
    
    class Config:
        extra = "allow"  # 允许额外字段，提高兼容性


@router.post("/enterprise/{enterprise_id}/report/generate", summary="生成审核报告")
async def generate_audit_report(
    enterprise_id: int,
    request_data: ReportGenerateRequest = Body(...),
    current_user=DependAuth
):
    """
    生成PCB清洁生产审核报告
    按照企业信息、筹划与组织、预审核、审核、问题及清洁生产方案的顺序生成完整报告
    """
    try:
        from app.models.pcb import PCBEnterprise
        from app.utils.word_report_generator import PCBWordReportGenerator
        
        # 验证企业是否存在
        enterprise = await PCBEnterprise.get_or_none(id=enterprise_id)
        if not enterprise:
            raise HTTPException(status_code=404, detail=f"企业ID {enterprise_id} 不存在")
        
        from app.utils.word_report_generator import generator
        
        # 使用请求数据，Pydantic已经设置了默认值
        sections = request_data.sections
        include_tables = request_data.include_tables
        include_recommendations = request_data.include_recommendations
        
        # 收集所有需要的数据
        report_data = await collect_report_data(enterprise_id, sections)
        
        # 生成Word报告
        report_path = await generator.generate_complete_report(
            enterprise_id=enterprise_id,
            enterprise_data=report_data.get("enterprise"),
            planning_data=report_data.get("planning"),
            preaudit_data=report_data.get("preaudit"),
            audit_data=report_data.get("audit"),
            problem_solution_data=report_data.get("problem"),
            include_tables=include_tables,
            include_recommendations=include_recommendations
        )
        
        return Success(
            data={
                "report_path": report_path,
                "report_filename": os.path.basename(report_path),
                "sections_generated": sections,
                "generated_at": generator.get_current_time().strftime('%Y-%m-%d %H:%M:%S')
            },
            msg="报告生成成功"
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"报告生成失败: {str(e)}")


@router.get("/enterprise/{enterprise_id}/report/preview", summary="预览审核报告")
async def preview_audit_report(
    enterprise_id: int,
    current_user=DependAuth
):
    """预览PCB清洁生产审核报告内容（返回结构化数据）"""
    try:
        from app.models.pcb import PCBEnterprise, PCBPreAuditData, PCBAuditResult, PCBAuditReport
        from app.models.pcb_planning import PCBLeadershipTeam, PCBWorkTeam, PCBWorkPlan, PCBTrainingRecord
        from app.controllers.pcb_problem_solution import get_level_two_and_below_issues
        
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
        
        # 获取问题及清洁生产方案数据
        issues = await get_level_two_and_below_issues(enterprise_id)
        
        # 构建预览数据（确保所有Decimal类型都转换为float）
        from decimal import Decimal
        def convert_decimal(value):
            """将Decimal类型转换为float，确保JSON可序列化"""
            if isinstance(value, Decimal):
                return float(value) if value is not None else None
            return value
        
        def convert_dict_decimals(d):
            """递归转换字典中的所有Decimal类型"""
            if isinstance(d, dict):
                return {k: convert_dict_decimals(v) for k, v in d.items()}
            elif isinstance(d, list):
                return [convert_dict_decimals(item) for item in d]
            elif isinstance(d, Decimal):
                return float(d) if d is not None else None
            return d
        
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
                "capacity": convert_decimal(enterprise.capacity),
                "capital": convert_decimal(enterprise.capital),
                "audit_status": enterprise.audit_status
            },
            "planning_organization": {
                "leadership_team_count": len(leadership_team),
                "work_team_count": len(work_team),
                "work_plans_count": len(work_plans),
                "training_records_count": len(training_records),
                "leadership_team": [convert_dict_decimals(await item.to_dict()) for item in leadership_team],
                "work_team": [convert_dict_decimals(await item.to_dict()) for item in work_team],
                "work_plans": [convert_dict_decimals(await item.to_dict()) for item in work_plans],
                "training_records": [convert_dict_decimals(await item.to_dict()) for item in training_records]
            },
            "pre_audit_data": {
                "has_data": pre_audit_data is not None,
                "status": pre_audit_data.status if pre_audit_data else None,
                "production_info": pre_audit_data.production_info if pre_audit_data else None,
                "raw_materials": pre_audit_data.raw_materials if pre_audit_data else None,
                "process_equipment": pre_audit_data.process_equipment if pre_audit_data else None,
                "resource_consumption": pre_audit_data.resource_consumption if pre_audit_data else None,
                "pollution_control": pre_audit_data.pollution_control if pre_audit_data else None,
                "solid_waste": pre_audit_data.solid_waste if pre_audit_data else None,
                "self_monitoring": pre_audit_data.self_monitoring if pre_audit_data else None
            },
            "audit_results": {
                "total_indicators": len(audit_results),
                "completed_indicators": len([r for r in audit_results if r.level]),
                "results": [convert_dict_decimals(await r.to_dict()) for r in audit_results],
                "has_audit_report": audit_report is not None,
                "total_score": convert_decimal(audit_report.total_score) if audit_report and audit_report.total_score else None,
                "overall_level": audit_report.overall_level if audit_report else None
            },
            "problem_solution": {
                "issues_count": len(issues),
                "issues": convert_dict_decimals(issues)  # issues可能包含Decimal类型
            }
        }
        
        return Success(data=preview_data, msg="报告预览数据获取成功")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"报告预览失败: {str(e)}")


@router.get("/enterprise/{enterprise_id}/report/download", summary="下载审核报告Word文档")
async def download_audit_report(
    enterprise_id: int,
    current_user=DependAuth
):
    """下载PCB清洁生产审核报告Word文档"""
    try:
        from app.models.pcb import PCBEnterprise
        
        # 验证企业是否存在
        enterprise = await PCBEnterprise.get_or_none(id=enterprise_id)
        if not enterprise:
            raise HTTPException(status_code=404, detail=f"企业ID {enterprise_id} 不存在")
        
        # 查找报告文件（按企业ID）
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir, exist_ok=True)
            raise HTTPException(status_code=404, detail="报告文件不存在，请先生成报告")
        
        # 查找匹配的报告文件
        report_filename = f"PCB审核报告_{enterprise.name}_{enterprise_id}.docx"
        report_path = os.path.join(reports_dir, report_filename)
        
        # 如果不存在，尝试查找通用格式
        if not os.path.exists(report_path):
            report_files = [f for f in os.listdir(reports_dir) 
                          if f.endswith('.docx') and str(enterprise_id) in f]
            if report_files:
                report_filename = report_files[0]
                report_path = os.path.join(reports_dir, report_filename)
            else:
                raise HTTPException(status_code=404, detail="报告文件不存在，请先生成报告")
        
        if not os.path.exists(report_path):
            raise HTTPException(status_code=404, detail="报告文件不存在")
        
        # 使用绝对路径
        import urllib.parse
        from pathlib import Path
        
        # 转换为绝对路径
        abs_report_path = os.path.abspath(report_path)
        if not os.path.exists(abs_report_path):
            raise HTTPException(status_code=404, detail="报告文件不存在")
        
        # 处理中文文件名的编码
        # Starlette 的 FileResponse 在设置 headers 时会将值编码为 latin-1
        # 关键：header 值必须是 latin-1 可编码的，所以不能包含中文字符
        
        # 生成 ASCII 后备文件名（安全的后备名称）
        ascii_filename = f"PCB_Report_{enterprise_id}.docx"
        
        # URL 编码原始文件名（用于 filename*=UTF-8'' 格式）
        # urllib.parse.quote 将中文字符编码为 %XX 格式，结果是纯 ASCII 字符串
        encoded_filename = urllib.parse.quote(report_filename, safe='')
        
        # 构造 Content-Disposition header
        # 使用 RFC 5987 格式：filename*=UTF-8''encoded_filename
        # 所有字符串都是 ASCII，可以安全编码为 latin-1
        content_disposition_value = 'attachment; filename="' + ascii_filename + '"; filename*=UTF-8\'\'' + encoded_filename
        
        # 双重验证：确保整个 header 值可以编码为 latin-1
        try:
            # 尝试编码为 latin-1
            test_encoding = content_disposition_value.encode('latin-1')
            # 确保可以解码回来（完整性检查）
            test_decoding = test_encoding.decode('latin-1')
            if test_decoding != content_disposition_value:
                # 如果编码/解码后不一致，只使用 ASCII 后备
                content_disposition_value = 'attachment; filename="' + ascii_filename + '"'
        except (UnicodeEncodeError, UnicodeDecodeError):
            # 如果编码失败，只使用 ASCII 后备文件名
            content_disposition_value = 'attachment; filename="' + ascii_filename + '"'
        
        return FileResponse(
            path=abs_report_path,
            filename=ascii_filename,  # 使用 ASCII 文件名作为主要文件名
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            headers={
                "Content-Disposition": content_disposition_value
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"报告下载失败: {str(e)}")


@router.get("/enterprise/{enterprise_id}/report", summary="获取审核报告信息")
async def get_report_info(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取审核报告基本信息"""
    try:
        from app.models.pcb import PCBAuditReport, PCBEnterprise
        
        enterprise = await PCBEnterprise.get_or_none(id=enterprise_id)
        if not enterprise:
            raise HTTPException(status_code=404, detail=f"企业ID {enterprise_id} 不存在")
        
        audit_report = await PCBAuditReport.get_or_none(enterprise_id=enterprise_id)
        
        if audit_report:
            return Success(
                data=await audit_report.to_dict(),
                msg="获取成功"
            )
        else:
            return Success(
                data=None,
                msg="报告尚未生成"
            )
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"获取报告信息失败: {str(e)}")


async def collect_report_data(enterprise_id: int, sections: List[str]) -> Dict[str, Any]:
    """
    收集报告所需的所有数据
    按照：企业信息、筹划与组织、预审核、审核、问题及清洁生产方案的顺序
    """
    data = {}
    
    try:
        from app.models.pcb import (
            PCBEnterprise, PCBPreAuditData, PCBAuditResult, PCBAuditReport,
            PCBLowCostScheme, PCBMediumHighCostScheme, PCBProblemSolutionScoring,
            PCBIndicator
        )
        from app.models.pcb_planning import (
            PCBLeadershipTeam, PCBWorkTeam, PCBWorkPlan, PCBTrainingRecord
        )
        from app.controllers.pcb_problem_solution import get_level_two_and_below_issues
        from app.models.pcb_production import (
            PCBProductOutput, PCBQualificationRate, PCBOutputValue
        )
        from app.models.pcb_raw_material import PCBRawMaterialUsage
        from app.models.process_equipment import PCBEquipmentRecord
        from app.models.resource_consumption import (
            PCBWaterConsumptionRecord, PCBElectricityConsumptionRecord, PCBGasConsumptionRecord
        )
        from app.models.pollution_control import (
            PCBWastewaterAnalysis, PCBWasteGasAnalysis, PCBWastewaterStatRecord
        )
        from app.models.solid_waste import PCBSolidWasteRecord
        from app.models.self_monitoring import (
            PCBOrganizedGasMonitoring, PCBUnorganizedGasMonitoring,
            PCBWastewaterMonitoring, PCBGasEmissionMonitoring, PCBNoiseMonitoring
        )
        
        # 1. 企业信息
        if "enterprise" in sections:
            enterprise = await PCBEnterprise.get_or_none(id=enterprise_id)
            if enterprise:
                data["enterprise"] = await enterprise.to_dict()
        
        # 2. 筹划与组织
        if "planning" in sections:
            leadership_team = await PCBLeadershipTeam.filter(enterprise_id=enterprise_id)
            work_team = await PCBWorkTeam.filter(enterprise_id=enterprise_id)
            work_plans = await PCBWorkPlan.filter(enterprise_id=enterprise_id).order_by('stage_order')
            training_records = await PCBTrainingRecord.filter(enterprise_id=enterprise_id)
            
            data["planning"] = {
                "leadership_team": [await item.to_dict() for item in leadership_team],
                "work_team": [await item.to_dict() for item in work_team],
                "work_plans": [await item.to_dict() for item in work_plans],
                "training_records": [await item.to_dict() for item in training_records]
            }
        
        # 3. 预审核 - 从各个独立表中收集数据
        if "preaudit" in sections:
            preaudit_dict = {}
            
            # 3.1 企业总体生产情况
            product_outputs = await PCBProductOutput.filter(enterprise_id=enterprise_id)
            qualification_rates = await PCBQualificationRate.filter(enterprise_id=enterprise_id)
            output_values = await PCBOutputValue.filter(enterprise_id=enterprise_id)
            
            preaudit_dict["production"] = {
                "product_outputs": [await item.to_dict() for item in product_outputs],
                "qualification_rates": [await item.to_dict() for item in qualification_rates],
                "output_values": [await item.to_dict() for item in output_values]
            }
            
            # 3.2 原辅材料使用情况
            raw_materials = await PCBRawMaterialUsage.filter(enterprise_id=enterprise_id)
            preaudit_dict["raw_materials"] = [await item.to_dict() for item in raw_materials]
            
            # 3.3 主要工艺及装备使用
            equipment = await PCBEquipmentRecord.filter(enterprise_id=enterprise_id)
            preaudit_dict["equipment"] = [await item.to_dict() for item in equipment]
            
            # 3.4 资源能源消耗
            water_records = await PCBWaterConsumptionRecord.filter(enterprise_id=enterprise_id)
            electricity_records = await PCBElectricityConsumptionRecord.filter(enterprise_id=enterprise_id)
            gas_records = await PCBGasConsumptionRecord.filter(enterprise_id=enterprise_id)
            
            preaudit_dict["resource_consumption"] = {
                "water": [await item.to_dict() for item in water_records],
                "electricity": [await item.to_dict() for item in electricity_records],
                "gas": [await item.to_dict() for item in gas_records]
            }
            
            # 3.5 污染防治
            wastewater_analysis = await PCBWastewaterAnalysis.filter(enterprise_id=enterprise_id)
            waste_gas_analysis = await PCBWasteGasAnalysis.filter(enterprise_id=enterprise_id)
            wastewater_stat = await PCBWastewaterStatRecord.filter(enterprise_id=enterprise_id)
            
            preaudit_dict["pollution_control"] = {
                "wastewater_analysis": [await item.to_dict() for item in wastewater_analysis],
                "waste_gas_analysis": [await item.to_dict() for item in waste_gas_analysis],
                "wastewater_stat": [await item.to_dict() for item in wastewater_stat]
            }
            
            # 3.6 工业固体废物管理
            solid_waste = await PCBSolidWasteRecord.filter(enterprise_id=enterprise_id)
            preaudit_dict["solid_waste"] = [await item.to_dict() for item in solid_waste]
            
            # 3.7 自行监测情况
            organized_gas = await PCBOrganizedGasMonitoring.filter(enterprise_id=enterprise_id)
            unorganized_gas = await PCBUnorganizedGasMonitoring.filter(enterprise_id=enterprise_id)
            wastewater_monitoring = await PCBWastewaterMonitoring.filter(enterprise_id=enterprise_id)
            gas_emission = await PCBGasEmissionMonitoring.filter(enterprise_id=enterprise_id)
            noise = await PCBNoiseMonitoring.filter(enterprise_id=enterprise_id)
            
            preaudit_dict["self_monitoring"] = {
                "organized_gas": [await item.to_dict() for item in organized_gas],
                "unorganized_gas": [await item.to_dict() for item in unorganized_gas],
                "wastewater": [await item.to_dict() for item in wastewater_monitoring],
                "gas_emission": [await item.to_dict() for item in gas_emission],
                "noise": [await item.to_dict() for item in noise]
            }
            
            data["preaudit"] = preaudit_dict
        
        # 4. 审核 - 获取审核结果和指标详情
        if "audit" in sections:
            audit_results = await PCBAuditResult.filter(enterprise_id=enterprise_id)
            audit_report = await PCBAuditReport.get_or_none(enterprise_id=enterprise_id)
            
            # 获取指标详情
            results_with_indicators = []
            for result in audit_results:
                indicator = await PCBIndicator.get_or_none(id=result.indicator_id)
                result_dict = await result.to_dict()
                if indicator:
                    result_dict["indicator"] = await indicator.to_dict()
                results_with_indicators.append(result_dict)
            
            data["audit"] = {
                "results": results_with_indicators,
                "summary": await audit_report.to_dict() if audit_report else None
            }
        
        # 5. 问题及清洁生产方案
        if "problem" in sections:
            issues = await get_level_two_and_below_issues(enterprise_id)
            low_cost_schemes = await PCBLowCostScheme.filter(enterprise_id=enterprise_id)
            mh_cost_schemes = await PCBMediumHighCostScheme.filter(enterprise_id=enterprise_id)
            scoring = await PCBProblemSolutionScoring.get_or_none(enterprise_id=enterprise_id)
            
            data["problem"] = {
                "issues": issues,
                "low_cost_schemes": [await item.to_dict() for item in low_cost_schemes],
                "medium_high_cost_schemes": [await item.to_dict() for item in mh_cost_schemes],
                "scoring": await scoring.to_dict() if scoring else None
            }
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise Exception(f"收集报告数据失败: {str(e)}")
    
    return data
