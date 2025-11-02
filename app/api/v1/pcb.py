"""
PCB行业清洁生产审核模块API路由
提供企业、指标、审核结果、方案的RESTful API接口
"""
from typing import List, Optional, Dict
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from app.controllers.pcb import (
    pcb_audit_report_controller,
    pcb_audit_result_controller,
    pcb_enterprise_controller,
    pcb_enterprise_scheme_controller,
    pcb_indicator_controller,
    pcb_indicator_scheme_relation_controller,
    pcb_pre_audit_data_controller,
    pcb_scheme_controller,
)
from app.controllers.enterprise_raw_material import enterprise_raw_material_controller
from app.models.pcb import PCBIndicator, PCBScheme, PCBIndicatorSchemeRelation
from app.schemas.base import Success
from app.schemas.pcb import (
    PCBAuditReportResponse,
    PCBAuditResultCreate,
    PCBAuditResultResponse,
    PCBAuditResultUpdate,
    PCBAuditSummaryResponse,
    PCBEnterpriseCreate,
    PCBEnterpriseResponse,
    PCBEnterpriseSchemeCreate,
    PCBEnterpriseSchemeResponse,
    PCBEnterpriseSchemeUpdate,
    PCBEnterpriseUpdate,
    PCBIndicatorCreate,
    PCBIndicatorResponse,
    PCBIndicatorSchemeRelationCreate,
    PCBIndicatorSchemeRelationResponse,
    PCBIndicatorUpdate,
    PCBPreAuditDataCreate,
    PCBPreAuditDataResponse,
    PCBPreAuditDataUpdate,
    PCBSchemeCreate,
    PCBSchemeResponse,
    PCBSchemeUpdate,
)
from app.settings import settings

pcb_router = APIRouter()


# ==================== Enterprise APIs ====================

@pcb_router.get("/enterprise", summary="获取企业列表")
async def get_enterprise_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    region: Optional[str] = Query(None, description="地市"),
    district: Optional[str] = Query(None, description="区县"),
    audit_status: Optional[str] = Query(None, description="审核状态"),
):
    """获取PCB企业列表，支持搜索和筛选"""
    enterprises, total = await pcb_enterprise_controller.get_list(
        page=page,
        page_size=page_size,
        search=search,
        region=region,
        district=district,
        audit_status=audit_status,
    )

    # 转换为字典列表
    data = []
    for enterprise in enterprises:
        enterprise_dict = await enterprise.to_dict()
        enterprise_dict["created_at"] = enterprise_dict["created_at"]
        enterprise_dict["updated_at"] = enterprise_dict["updated_at"]
        data.append(enterprise_dict)

    return Success(
        data={
            "items": data,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@pcb_router.post("/enterprise", summary="创建企业")
async def create_enterprise(enterprise: PCBEnterpriseCreate):
    """创建新的PCB企业"""
    new_enterprise = await pcb_enterprise_controller.create(enterprise)
    return Success(data=await new_enterprise.to_dict(), msg="企业创建成功")


@pcb_router.get("/enterprise/{enterprise_id}", summary="获取企业详情")
async def get_enterprise_detail(enterprise_id: int):
    """获取企业详细信息"""
    enterprise = await pcb_enterprise_controller.get(id=enterprise_id)
    if not enterprise:
        raise HTTPException(status_code=404, detail="企业不存在")

    return Success(data=await enterprise.to_dict())


@pcb_router.put("/enterprise/{enterprise_id}", summary="更新企业信息")
async def update_enterprise(enterprise_id: int, enterprise: PCBEnterpriseUpdate):
    """更新企业基本信息"""
    updated_enterprise = await pcb_enterprise_controller.update(id=enterprise_id, obj_in=enterprise)
    if not updated_enterprise:
        raise HTTPException(status_code=404, detail="企业不存在")

    return Success(data=await updated_enterprise.to_dict(), msg="企业信息更新成功")


@pcb_router.delete("/enterprise/{enterprise_id}", summary="删除企业")
async def delete_enterprise(enterprise_id: int):
    """软删除企业"""
    success = await pcb_enterprise_controller.soft_delete(id=enterprise_id)
    if not success:
        raise HTTPException(status_code=404, detail="企业不存在")

    return Success(msg="企业删除成功")


# ==================== Indicator APIs ====================

@pcb_router.get("/indicator", summary="获取指标列表")
async def get_indicator_list(
    category: Optional[str] = Query(None, description="指标类别"),
    indicator_type: Optional[str] = Query(None, description="指标类型"),
):
    """获取PCB审核指标列表"""
    if category:
        indicators = await pcb_indicator_controller.get_indicators_by_category(category)
    else:
        indicators = await pcb_indicator_controller.get_all()

    # 如果指定了类型，进一步筛选
    if indicator_type:
        indicators = [ind for ind in indicators if ind.indicator_type == indicator_type]

    data = []
    for indicator in indicators:
        data.append(await indicator.to_dict())

    return Success(data=data)


@pcb_router.get("/indicator/tree", summary="获取指标树")
async def get_indicator_tree():
    """获取指标树形结构，用于前端树选择组件"""
    tree = await pcb_indicator_controller.get_indicators_tree()
    return Success(data=tree)


@pcb_router.get("/indicator/limiting", summary="获取限定性指标")
async def get_limiting_indicators():
    """获取所有限定性指标"""
    indicators = await pcb_indicator_controller.get_limiting_indicators()
    data = []
    for indicator in indicators:
        data.append(await indicator.to_dict())

    return Success(data=data)


@pcb_router.get("/indicator/{indicator_id}", summary="获取指标详情")
async def get_indicator_detail(indicator_id: int):
    """获取指标详细信息（根据indicator_id字段查询）"""
    indicator = await pcb_indicator_controller.get_by_indicator_id(indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="指标不存在")

    return Success(data=await indicator.to_dict())


@pcb_router.post("/indicator", summary="创建指标")
async def create_indicator(indicator: PCBIndicatorCreate):
    """创建新的审核指标"""
    new_indicator = await pcb_indicator_controller.create(obj=indicator)
    return Success(data=await new_indicator.to_dict(), msg="指标创建成功")


@pcb_router.put("/indicator/{indicator_id}", summary="更新指标")
async def update_indicator(indicator_id: int, indicator: PCBIndicatorUpdate):
    """更新指标信息（根据indicator_id字段更新）"""
    existing_indicator = await pcb_indicator_controller.get_by_indicator_id(indicator_id)
    if not existing_indicator:
        raise HTTPException(status_code=404, detail="指标不存在")

    updated_indicator = await pcb_indicator_controller.update(id=existing_indicator.id, obj_in=indicator)
    return Success(data=await updated_indicator.to_dict(), msg="指标更新成功")


# ==================== Pre-Audit Data APIs ====================

@pcb_router.get("/enterprise/{enterprise_id}/pre-audit", summary="获取预审核数据")
async def get_pre_audit_data(enterprise_id: int):
    """获取企业预审核数据"""
    pre_audit = await pcb_pre_audit_data_controller.get_by_enterprise(enterprise_id)
    if not pre_audit:
        # 如果没有数据，返回空对象
        return Success(
            data={
                "enterprise_id": enterprise_id,
                "production_info": {},
                "raw_materials": {},
                "process_equipment": {},
                "resource_consumption": {},
                "pollution_control": {},
                "solid_waste": {},
                "self_monitoring": {},
                "status": "draft",
            }
        )

    return Success(data=await pre_audit.to_dict())


@pcb_router.post("/enterprise/{enterprise_id}/pre-audit", summary="保存预审核数据")
async def save_pre_audit_data(enterprise_id: int, data: PCBPreAuditDataUpdate):
    """保存或更新预审核数据"""
    pre_audit = await pcb_pre_audit_data_controller.update_or_create(
        enterprise_id=enterprise_id, data=data.dict(exclude_unset=True)
    )
    return Success(data=await pre_audit.to_dict(), msg="预审核数据保存成功")


@pcb_router.post("/enterprise/{enterprise_id}/pre-audit/submit", summary="提交预审核数据")
async def submit_pre_audit_data(enterprise_id: int):
    """提交预审核数据进行审核"""
    pre_audit = await pcb_pre_audit_data_controller.submit_data(enterprise_id)
    if not pre_audit:
        raise HTTPException(status_code=404, detail="预审核数据不存在")

    return Success(data=await pre_audit.to_dict(), msg="预审核数据提交成功")


# ==================== Audit Result APIs ====================

@pcb_router.get("/enterprise/{enterprise_id}/audit", summary="获取审核结果")
async def get_audit_results(enterprise_id: int):
    """获取企业所有指标的审核结果"""
    results = await pcb_audit_result_controller.get_enterprise_results(enterprise_id)

    # 获取所有指标
    indicators = await pcb_indicator_controller.get_all()
    indicator_map = {ind.id: ind for ind in indicators}

    # 构建完整的审核结果列表
    data = []
    for indicator in indicators:
        # 查找对应的审核结果
        result = next((r for r in results if r.indicator_id == indicator.id), None)

        if result:
            result_dict = await result.to_dict()
            # 为了兼容前端使用remark字段，同时提供comment字段
            if 'comment' in result_dict and 'remark' not in result_dict:
                result_dict['remark'] = result_dict['comment']
        else:
            # 如果没有结果，创建默认结果
            result_dict = {
                "enterprise_id": enterprise_id,
                "indicator_id": indicator.id,
                "current_value": None,
                "level": None,  # 初始为null而不是"待评估"
                "score": 0,
                "comment": None,
                "remark": None,  # 同时提供remark字段
                "manual_override": False,
            }

        # 添加指标信息
        indicator_dict = await indicator.to_dict()
        result_dict["indicator"] = indicator_dict

        # 移除推荐方案 - 不再返回推荐方案数据
        # recommended_schemes = await pcb_audit_result_controller.get_indicator_recommended_schemes(enterprise_id, indicator.id)
        # result_dict["recommended_schemes"] = recommended_schemes

        data.append(result_dict)

    return Success(data=data)


@pcb_router.put(
    "/enterprise/{enterprise_id}/audit/indicator/{indicator_id}",
    summary="更新单个指标审核结果",
)
async def update_indicator_audit(
    enterprise_id: int, indicator_id: int, update_data: PCBAuditResultUpdate
):
    """更新单个指标的审核结果"""
    # 获取指标（根据数据库ID）
    indicator = await PCBIndicator.get_or_none(id=indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="指标不存在")

    # 计算分数
    score = None
    if update_data.level:
        score = calculate_score(update_data.level)

    # 移除方案选择 - 不再处理selected_scheme_ids
    result = await pcb_audit_result_controller.update_indicator_level(
        enterprise_id=enterprise_id,
        indicator_id=indicator_id,
        level=update_data.level,
        score=score,
        manual_override=update_data.manual_override or False,
        override_reason=update_data.override_reason,
        selected_scheme_ids=None,  # 不再处理方案选择
    )

    return Success(data=await result.to_dict(), msg="审核结果更新成功")


@pcb_router.post("/enterprise/{enterprise_id}/audit/batch", summary="批量更新审核结果")
async def batch_update_audit_results(enterprise_id: int, audit_data: dict):
    """批量更新多个指标的审核结果（已移除方案选择功能）"""
    # 提取指标审核结果
    indicators = audit_data.get("indicators", [])
    user_input_outputs = audit_data.get("user_input_outputs", {})  # 用户输入的产量数据
    auditor_name = audit_data.get("auditor_name", "系统")
    audit_date = audit_data.get("audit_date")
    
    # 移除方案选择处理
    # selected_schemes = audit_data.get("selected_schemes", [])
    
    # 更新审核结果
    results = await pcb_audit_result_controller.batch_update_results(
        enterprise_id=enterprise_id, results_data=indicators
    )
    
    # 移除方案保存逻辑
    # # 保存选定的方案
    # if selected_schemes:
    #     await pcb_enterprise_scheme_controller.save_selected_schemes(
    #         enterprise_id=enterprise_id, selected_schemes=selected_schemes
    #     )
    
    # 获取产品产量数据并合并用户输入的产量
    from app.controllers.pcb_production import PCBProductionDataController
    production_controller = PCBProductionDataController()
    
    product_outputs = {}
    try:
        production_data = await production_controller.get_all_production_data(enterprise_id)
        # 从产品数据中映射
        product_outputs = _map_product_output_to_indicators(production_data.get("productOutput", []))
    except Exception as e:
        print(f"获取产品产量数据失败: {e}")
        product_outputs = {}
    
    # 合并用户输入的产量（用户输入优先）
    for indicator_id, output_value in user_input_outputs.items():
        product_outputs[int(indicator_id)] = float(output_value)
    
    # 计算汇总数据
    summary = await pcb_audit_result_controller.calculate_summary(enterprise_id, product_outputs)
    
    return Success(data=summary, msg="审核结果批量更新成功")


@pcb_router.get("/enterprise/{enterprise_id}/audit/summary", summary="获取审核汇总")
async def get_audit_summary(
    enterprise_id: int,
    user_input_outputs: Optional[str] = Query(None, description="用户输入的产量数据(JSON格式)")
):
    """
    获取企业审核汇总数据（使用新的综合评价指数计算方法）
    
    参数:
        enterprise_id: 企业ID
        user_input_outputs: 可选的用户输入产量数据（JSON字符串格式，如：{"7": 500, "8": 1000}）
    """
    # 获取产品产量数据
    from app.controllers.pcb_production import PCBProductionDataController
    production_controller = PCBProductionDataController()
    
    product_outputs = {}
    try:
        production_data = await production_controller.get_all_production_data(enterprise_id)
        # 将产品产量数据转换为indicator_id到产量的映射
        product_outputs = _map_product_output_to_indicators(production_data.get("productOutput", []))
    except Exception as e:
        print(f"获取产品产量数据失败: {e}")
        product_outputs = {}
    
    # 解析并合并用户输入的产量（如果提供）
    if user_input_outputs:
        try:
            import json
            user_outputs = json.loads(user_input_outputs)
            for indicator_id, output_value in user_outputs.items():
                product_outputs[int(indicator_id)] = float(output_value)
        except Exception as e:
            print(f"解析用户输入产量数据失败: {e}")
    
    summary = await pcb_audit_result_controller.calculate_summary(enterprise_id, product_outputs)
    return Success(data=summary)


@pcb_router.post("/enterprise/{enterprise_id}/audit/auto-calculate", summary="自动计算审核结果")
async def auto_calculate_audit(enterprise_id: int):
    """根据预审核数据自动计算审核结果"""
    # 获取预审核数据
    pre_audit = await pcb_pre_audit_data_controller.get_by_enterprise(enterprise_id)
    if not pre_audit:
        raise HTTPException(status_code=404, detail="预审核数据不存在")

    # 获取所有定量指标
    indicators = await pcb_indicator_controller.get_all()

    # 自动计算逻辑（简化版本，实际应根据具体指标计算）
    for indicator in indicators:
        if indicator.indicator_type == "quantitative":
            # 这里应该根据预审核数据和指标标准计算当前值和评级
            # 简化处理：随机设置一个等级作为示例
            pass

    summary = await pcb_audit_result_controller.calculate_summary(enterprise_id)
    return Success(data=summary, msg="自动计算完成")


# ==================== Scheme APIs ====================

@pcb_router.get("/scheme", summary="获取方案列表")
async def get_scheme_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    scheme_type: Optional[str] = Query(None, description="方案类型"),
    indicator_ids: Optional[str] = Query(None, description="指标ID列表，逗号分隔"),
):
    """获取清洁生产方案列表"""
    # 解析指标ID列表
    indicator_id_list = None
    if indicator_ids:
        try:
            indicator_id_list = [int(id.strip()) for id in indicator_ids.split(",")]
        except ValueError:
            raise HTTPException(status_code=400, detail="指标ID格式错误")

    schemes, total = await pcb_scheme_controller.search_schemes(
        page=page,
        page_size=page_size,
        search=search,
        scheme_type=scheme_type,
        indicator_ids=indicator_id_list,
    )

    data = []
    for scheme in schemes:
        scheme_dict = await scheme.to_dict()
        
        # 获取关联的指标信息
        relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id).all()
        related_indicators = []
        for relation in relations:
            indicator = await PCBIndicator.get_or_none(id=relation.indicator_id)
            if indicator:
                related_indicators.append({
                    "id": indicator.id,
                    "name": indicator.name,
                    "relevance_score": float(relation.relevance_score),
                    "priority": relation.priority,
                    "recommendation_reason": relation.recommendation_reason
                })
        
        scheme_dict["related_indicators"] = related_indicators
        data.append(scheme_dict)

    return Success(
        data={
            "items": data,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    )


@pcb_router.get("/scheme/{scheme_id}", summary="获取方案详情")
async def get_scheme_detail(scheme_id: int):
    """获取方案详细信息（根据scheme_id字段查询）"""
    scheme = await pcb_scheme_controller.get_by_scheme_id(scheme_id)
    if not scheme:
        raise HTTPException(status_code=404, detail="方案不存在")

    return Success(data=await scheme.to_dict())


@pcb_router.post("/scheme", summary="创建方案")
async def create_scheme(scheme: PCBSchemeCreate):
    """创建新的清洁生产方案"""
    # 自动生成scheme_id
    max_scheme = await PCBScheme.all().order_by('-scheme_id').first()
    next_scheme_id = (max_scheme.scheme_id + 1) if max_scheme else 1
    
    # 创建方案数据
    scheme_data = scheme.dict()
    scheme_data['scheme_id'] = next_scheme_id
    
    new_scheme = await pcb_scheme_controller.create(obj=scheme_data)
    return Success(data=await new_scheme.to_dict(), msg="方案创建成功")


@pcb_router.put("/scheme/{scheme_id}", summary="更新方案")
async def update_scheme(scheme_id: int, scheme: PCBSchemeUpdate):
    """更新方案信息（根据scheme_id字段更新）"""
    existing_scheme = await pcb_scheme_controller.get_by_scheme_id(scheme_id)
    if not existing_scheme:
        raise HTTPException(status_code=404, detail="方案不存在")

    updated_scheme = await pcb_scheme_controller.update(id=existing_scheme.id, obj_in=scheme)
    return Success(data=await updated_scheme.to_dict(), msg="方案更新成功")


@pcb_router.delete("/scheme/{scheme_id}", summary="删除方案")
async def delete_scheme(scheme_id: int):
    """删除方案（软删除，设置is_active=False）"""
    try:
        existing_scheme = await pcb_scheme_controller.get_by_scheme_id(scheme_id)
        if not existing_scheme:
            raise HTTPException(status_code=404, detail="方案不存在")

        existing_scheme.is_active = False
        await existing_scheme.save()

        return Success(msg="方案删除成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除方案失败: {str(e)}")


@pcb_router.get("/indicator/{indicator_id}/schemes", summary="获取指标推荐方案")
async def get_indicator_schemes(indicator_id: int):
    """获取指标关联的推荐方案列表"""
    # 获取指标（根据indicator_id字段）
    indicator = await pcb_indicator_controller.get_by_indicator_id(indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="指标不存在")

    schemes = await pcb_scheme_controller.get_schemes_by_indicator(indicator.id)
    return Success(data=schemes)


@pcb_router.get(
    "/enterprise/{enterprise_id}/audit/schemes/{indicator_id}",
    summary="获取企业指标推荐方案",
)
async def get_enterprise_indicator_schemes(enterprise_id: int, indicator_id: int):
    """获取企业特定指标的推荐方案"""
    # 获取指标（根据数据库ID）
    indicator = await PCBIndicator.get_or_none(id=indicator_id)
    if not indicator:
        raise HTTPException(status_code=404, detail="指标不存在")

    # 获取推荐方案
    schemes = await pcb_audit_result_controller.get_indicator_recommended_schemes(enterprise_id, indicator_id)
    return Success(data=schemes)


# ==================== Indicator-Scheme Relation APIs ====================

@pcb_router.post("/indicator-scheme-relation", summary="创建指标方案关联")
async def create_indicator_scheme_relation(relation: PCBIndicatorSchemeRelationCreate):
    """创建指标与方案的关联关系"""
    new_relation = await pcb_indicator_scheme_relation_controller.create_relation(
        indicator_id=relation.indicator_id,
        scheme_id=relation.scheme_id,
        relevance_score=relation.relevance_score,
        priority=relation.priority,
        recommendation_reason=relation.recommendation_reason,
    )
    return Success(data=await new_relation.to_dict(), msg="关联创建成功")


@pcb_router.post("/indicator-scheme-relation/batch", summary="批量创建指标方案关联")
async def batch_create_indicator_scheme_relations(relations: List[PCBIndicatorSchemeRelationCreate]):
    """批量创建指标与方案的关联关系"""
    relations_data = [r.dict() for r in relations]
    new_relations = await pcb_indicator_scheme_relation_controller.batch_create_relations(
        relations_data
    )

    data = []
    for relation in new_relations:
        data.append(await relation.to_dict())

    return Success(data=data, msg="批量关联创建成功")


# ==================== Enterprise Scheme APIs ====================

@pcb_router.get("/enterprise/{enterprise_id}/scheme", summary="获取企业方案列表")
async def get_enterprise_schemes(
    enterprise_id: int,
    status: Optional[str] = Query(None, description="方案状态"),
):
    """获取企业选择的方案列表"""
    enterprise_schemes = await pcb_enterprise_scheme_controller.get_enterprise_schemes(
        enterprise_id=enterprise_id, status=status
    )

    data = []
    for es in enterprise_schemes:
        es_dict = await es.to_dict()

        # 获取方案详情
        scheme = await PCBScheme.get_or_none(id=es.scheme_id)
        if scheme:
            es_dict["scheme"] = await scheme.to_dict()

        data.append(es_dict)

    return Success(data=data)


@pcb_router.post("/enterprise/{enterprise_id}/scheme", summary="企业选择方案")
async def select_enterprise_scheme(enterprise_id: int, scheme_data: PCBEnterpriseSchemeCreate):
    """企业选择清洁生产方案"""
    new_es = await pcb_enterprise_scheme_controller.create(obj=scheme_data)
    return Success(data=await new_es.to_dict(), msg="方案选择成功")


@pcb_router.put("/enterprise/{enterprise_id}/scheme/{scheme_id}", summary="更新企业方案")
async def update_enterprise_scheme(
    enterprise_id: int, scheme_id: int, update_data: PCBEnterpriseSchemeUpdate
):
    """更新企业方案状态和实施信息"""
    # 查找企业方案记录
    es = await pcb_enterprise_scheme_controller.model.get_or_none(
        enterprise_id=enterprise_id, scheme_id=scheme_id
    )
    if not es:
        raise HTTPException(status_code=404, detail="企业方案记录不存在")

    updated_es = await pcb_enterprise_scheme_controller.update(id=es.id, obj_in=update_data)
    return Success(data=await updated_es.to_dict(), msg="企业方案更新成功")


# ==================== Audit Report APIs ====================

@pcb_router.get("/enterprise/{enterprise_id}/report", summary="获取审核报告")
async def get_audit_report(enterprise_id: int):
    """获取企业审核报告"""
    report = await pcb_audit_report_controller.get_by_enterprise(enterprise_id)
    if not report:
        raise HTTPException(status_code=404, detail="审核报告不存在")

    return Success(data=await report.to_dict())


# 注意：此路由已迁移到 app/api/v1/pcb_report.py
# 新的路由支持更完整的Word报告生成功能，包括企业信息、筹划与组织、预审核、审核、问题及清洁生产方案等模块
# @pcb_router.post("/enterprise/{enterprise_id}/report/generate", summary="生成审核报告")
# async def generate_audit_report(
#     enterprise_id: int,
#     auditor_id: int = Query(..., description="审核人ID"),
#     auditor_name: str = Query(..., description="审核人姓名"),
# ):
#     """生成或更新审核报告"""
#     report = await pcb_audit_report_controller.generate_report(
#         enterprise_id=enterprise_id, auditor_id=auditor_id, auditor_name=auditor_name
#     )
#     return Success(data=await report.to_dict(), msg="审核报告生成成功")


@pcb_router.post("/enterprise/{enterprise_id}/report/submit", summary="提交审核报告")
async def submit_audit_report(enterprise_id: int):
    """提交审核报告"""
    report = await pcb_audit_report_controller.submit_report(enterprise_id)
    if not report:
        raise HTTPException(status_code=404, detail="审核报告不存在")

    return Success(data=await report.to_dict(), msg="审核报告提交成功")


@pcb_router.get("/enterprise/{enterprise_id}/report/export", summary="导出审核报告Word文档")
async def export_audit_report_word(enterprise_id: int):
    """导出审核报告为Word文档"""
    from fastapi.responses import FileResponse
    import os
    
    try:
        # 暂时直接从reports文件夹中查找现有报告
        # 注释掉原来的报告生成逻辑
        
        # 查找reports目录中的报告文件
        reports_dir = os.path.abspath("reports")
        if not os.path.exists(reports_dir):
            raise HTTPException(status_code=404, detail=f"reports目录不存在: {reports_dir}")
        
        # 查找匹配的报告文件
        report_files = [f for f in os.listdir(reports_dir) if f.endswith('.docx')]
        
        if not report_files:
            raise HTTPException(status_code=404, detail="未找到报告文件")
        
        # 使用第一个找到的报告文件
        report_filename = report_files[0]
        filepath = os.path.join(reports_dir, report_filename)
        
        if not os.path.exists(filepath):
            raise HTTPException(status_code=404, detail="报告文件不存在")
        
        # 返回文件
        return FileResponse(
            filepath,
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            filename=report_filename
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"导出报告失败: {str(e)}"
        )


# ==================== Helper Functions ====================

def calculate_score(level: str) -> float:
    """根据评级计算分数"""
    score_map = {
        "I级": 100.0,
        "II级": 80.0,
        "III级": 60.0,
        "不达标": 0.0,
    }
    return score_map.get(level, 0.0)


def _map_product_output_to_indicators(product_outputs: List[Dict]) -> Dict[int, float]:
    """
    将产品产量数据映射到指标ID
    
    参数:
        product_outputs: 产品产量列表，格式: [
            {type: 'rigid', mainProduct: '单面板', output: 500, ...},
            ...
        ]
    
    返回:
        {indicator_id: total_output} 的字典
    """
    # 指标ID到产品类型的映射（与前端保持一致）
    indicator_product_map = {
        # 刚性单面板
        7: {'type': 'rigid', 'mainProduct': '单面板', 'layers': 1},
        15: {'type': 'rigid', 'mainProduct': '单面板', 'layers': 1},
        20: {'type': 'rigid', 'mainProduct': '单面板', 'layers': 1},
        30: {'type': 'rigid', 'mainProduct': '单面板', 'layers': 1},
        34: {'type': 'rigid', 'mainProduct': '单面板', 'layers': 1},
        38: {'type': 'rigid', 'mainProduct': '单面板', 'layers': 1},
        # 刚性双面板
        8: {'type': 'rigid', 'mainProduct': '双面板', 'layers': 2},
        16: {'type': 'rigid', 'mainProduct': '双面板', 'layers': 2},
        21: {'type': 'rigid', 'mainProduct': '双面板', 'layers': 2},
        31: {'type': 'rigid', 'mainProduct': '双面板', 'layers': 2},
        35: {'type': 'rigid', 'mainProduct': '双面板', 'layers': 2},
        39: {'type': 'rigid', 'mainProduct': '双面板', 'layers': 2},
        # 刚性多层板
        9: {'type': 'rigid', 'mainProduct': '多层板', 'layers': None},
        17: {'type': 'rigid', 'mainProduct': '多层板', 'layers': None},
        22: {'type': 'rigid', 'mainProduct': '多层板', 'layers': None},
        32: {'type': 'rigid', 'mainProduct': '多层板', 'layers': None},
        36: {'type': 'rigid', 'mainProduct': '多层板', 'layers': None},
        40: {'type': 'rigid', 'mainProduct': '多层板', 'layers': None},
        # 刚性HDI板
        10: {'type': 'rigid', 'mainProduct': 'HDI板', 'layers': None},
        18: {'type': 'rigid', 'mainProduct': 'HDI板', 'layers': None},
        23: {'type': 'rigid', 'mainProduct': 'HDI板', 'layers': None},
        33: {'type': 'rigid', 'mainProduct': 'HDI板', 'layers': None},
        37: {'type': 'rigid', 'mainProduct': 'HDI板', 'layers': None},
        41: {'type': 'rigid', 'mainProduct': 'HDI板', 'layers': None},
        # 挠性单面板
        11: {'type': 'flexible', 'mainProduct': '单面板', 'layers': 1},
        24: {'type': 'flexible', 'mainProduct': '单面板', 'layers': 1},
        # 挠性双面板
        12: {'type': 'flexible', 'mainProduct': '双面板', 'layers': 2},
        25: {'type': 'flexible', 'mainProduct': '双面板', 'layers': 2},
        # 挠性多层板
        13: {'type': 'flexible', 'mainProduct': '多层板', 'layers': None},
        26: {'type': 'flexible', 'mainProduct': '多层板', 'layers': None},
        # 挠性HDI板
        14: {'type': 'flexible', 'mainProduct': 'HDI板', 'layers': None},
        27: {'type': 'flexible', 'mainProduct': 'HDI板', 'layers': None},
    }
    
    result = {}
    
    for indicator_id, product_info in indicator_product_map.items():
        total_output = 0.0
        
        # 查找匹配的产品产量数据
        for product in product_outputs:
            if (product.get('type') == product_info['type'] and 
                product.get('mainProduct') == product_info['mainProduct']):
                
                # 如果指定了层数，需要匹配层数
                if product_info['layers'] is not None:
                    if product.get('layers') != product_info['layers']:
                        continue
                
                # 累加产量（处理年份字段）
                output_value = product.get('output')
                if output_value:
                    total_output += float(output_value)
                
                # 如果是年份字段格式（output_2023等）
                for key, value in product.items():
                    if key.startswith('output_') and value:
                        try:
                            total_output += float(value)
                        except (ValueError, TypeError):
                            pass
        
        if total_output > 0:
            result[indicator_id] = total_output
    
    return result


# ==================== Enterprise Raw Material Usage APIs ====================

@pcb_router.get("/enterprise/{enterprise_id}/raw-materials", summary="获取企业原辅材料使用情况")
async def get_enterprise_raw_materials(
    enterprise_id: int,
    year: Optional[str] = Query(None, description="年份")
):
    """获取企业的原辅材料使用情况"""
    usages = await enterprise_raw_material_controller.get_by_enterprise(enterprise_id, year)
    
    # 转换为前端需要的格式
    usage_list = []
    for usage in usages:
        usage_dict = {
            "id": usage.id,
            "year": usage.year,
            "name": usage.material.name if usage.material else "",
            "unit": usage.unit or usage.material.unit if usage.material else "",
            "process": usage.process or usage.material.process if usage.material else "",
            "amount": float(usage.amount) if usage.amount else None,
            "unitConsumption": None,  # 可以根据需要计算
            "state": usage.state,
            "voc": float(usage.voc_content) if usage.voc_content else None
        }
        usage_list.append(usage_dict)
    
    return Success(data=usage_list, msg="获取成功")


@pcb_router.post("/enterprise/{enterprise_id}/raw-materials", summary="保存企业原辅材料使用情况")
async def save_enterprise_raw_materials(
    enterprise_id: int,
    usage_data: dict
):
    """保存企业的原辅材料使用情况"""
    year = usage_data.get("year", str(datetime.now().year))
    materials_data = usage_data.get("materials", [])
    
    # 保存数据
    usages = await enterprise_raw_material_controller.save_usage_data(
        enterprise_id=enterprise_id,
        year=year,
        usage_data=materials_data
    )
    
    return Success(data={"count": len(usages)}, msg="保存成功")


@pcb_router.put("/enterprise/{enterprise_id}/raw-materials", summary="更新企业原辅材料使用情况")
async def update_enterprise_raw_materials(
    enterprise_id: int,
    usage_data: dict
):
    """更新企业的原辅材料使用情况"""
    year = usage_data.get("year", str(datetime.now().year))
    materials_data = usage_data.get("materials", [])
    
    # 更新数据
    usages = await enterprise_raw_material_controller.update_usage_data(
        enterprise_id=enterprise_id,
        year=year,
        usage_data=materials_data
    )
    
    return Success(data={"count": len(usages)}, msg="更新成功")


@pcb_router.get("/enterprise/{enterprise_id}/raw-materials/statistics", summary="获取企业原辅材料使用统计")
async def get_enterprise_raw_materials_statistics(
    enterprise_id: int,
    year: Optional[str] = Query(None, description="年份")
):
    """获取企业原辅材料使用统计信息"""
    statistics = await enterprise_raw_material_controller.get_usage_statistics(enterprise_id, year)
    return Success(data=statistics, msg="获取成功")



