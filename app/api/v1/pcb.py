"""
PCB行业清洁生产审核模块API路由
提供企业、指标、审核结果、方案的RESTful API接口
"""
from typing import List, Optional

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
from app.models.pcb import PCBIndicator, PCBScheme
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
    updated_enterprise = await pcb_enterprise_controller.update(id=enterprise_id, obj=enterprise)
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

    updated_indicator = await pcb_indicator_controller.update(id=existing_indicator.id, obj=indicator)
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
        else:
            # 如果没有结果，创建默认结果
            result_dict = {
                "enterprise_id": enterprise_id,
                "indicator_id": indicator.id,
                "current_value": None,
                "level": "待评估",
                "score": 0,
                "comment": None,
                "manual_override": False,
            }

        # 添加指标信息
        indicator_dict = await indicator.to_dict()
        result_dict["indicator"] = indicator_dict

        # 获取推荐方案
        if result and result.level and result.level not in ["I级", "待评估"]:
            recommended_schemes = await pcb_scheme_controller.get_schemes_by_indicator(indicator.id)
            result_dict["recommended_schemes"] = recommended_schemes
        else:
            result_dict["recommended_schemes"] = []

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

    result = await pcb_audit_result_controller.update_indicator_level(
        enterprise_id=enterprise_id,
        indicator_id=indicator_id,
        level=update_data.level,
        score=score,
        manual_override=update_data.manual_override or False,
        override_reason=update_data.override_reason,
    )

    return Success(data=await result.to_dict(), msg="审核结果更新成功")


@pcb_router.post("/enterprise/{enterprise_id}/audit/batch", summary="批量更新审核结果")
async def batch_update_audit_results(enterprise_id: int, results_data: List[dict]):
    """批量更新多个指标的审核结果"""
    results = await pcb_audit_result_controller.batch_update_results(
        enterprise_id=enterprise_id, results_data=results_data
    )

    data = []
    for result in results:
        data.append(await result.to_dict())

    return Success(data=data, msg="审核结果批量更新成功")


@pcb_router.get("/enterprise/{enterprise_id}/audit/summary", summary="获取审核汇总")
async def get_audit_summary(enterprise_id: int):
    """获取企业审核汇总数据"""
    summary = await pcb_audit_result_controller.calculate_summary(enterprise_id)
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
        data.append(await scheme.to_dict())

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
    new_scheme = await pcb_scheme_controller.create(obj=scheme)
    return Success(data=await new_scheme.to_dict(), msg="方案创建成功")


@pcb_router.put("/scheme/{scheme_id}", summary="更新方案")
async def update_scheme(scheme_id: int, scheme: PCBSchemeUpdate):
    """更新方案信息（根据scheme_id字段更新）"""
    existing_scheme = await pcb_scheme_controller.get_by_scheme_id(scheme_id)
    if not existing_scheme:
        raise HTTPException(status_code=404, detail="方案不存在")

    updated_scheme = await pcb_scheme_controller.update(id=existing_scheme.id, obj=scheme)
    return Success(data=await updated_scheme.to_dict(), msg="方案更新成功")


@pcb_router.delete("/scheme/{scheme_id}", summary="删除方案")
async def delete_scheme(scheme_id: int):
    """删除方案（软删除，设置is_active=False）"""
    existing_scheme = await pcb_scheme_controller.get_by_scheme_id(scheme_id)
    if not existing_scheme:
        raise HTTPException(status_code=404, detail="方案不存在")

    existing_scheme.is_active = False
    await existing_scheme.save()

    return Success(msg="方案删除成功")


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

    # 获取审核结果
    result = await pcb_audit_result_controller.get_or_create_result(enterprise_id, indicator_id)

    # 只有非I级才推荐方案
    if result.level and result.level not in ["I级", "待评估"]:
        schemes = await pcb_scheme_controller.get_schemes_by_indicator(indicator_id)
        return Success(data=schemes)
    else:
        return Success(data=[])


# ==================== Indicator-Scheme Relation APIs ====================

@pcb_router.post("/indicator-scheme-relation", summary="创建指标方案关联")
async def create_indicator_scheme_relation(relation: PCBIndicatorSchemeRelationCreate):
    """创建指标与方案的关联关系"""
    new_relation = await pcb_indicator_scheme_relation_controller.create_relation(
        indicator_id=relation.indicator_id,
        scheme_id=relation.scheme_id,
        relevance_score=relation.relevance_score,
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

    updated_es = await pcb_enterprise_scheme_controller.update(id=es.id, obj=update_data)
    return Success(data=await updated_es.to_dict(), msg="企业方案更新成功")


# ==================== Audit Report APIs ====================

@pcb_router.get("/enterprise/{enterprise_id}/report", summary="获取审核报告")
async def get_audit_report(enterprise_id: int):
    """获取企业审核报告"""
    report = await pcb_audit_report_controller.get_by_enterprise(enterprise_id)
    if not report:
        raise HTTPException(status_code=404, detail="审核报告不存在")

    return Success(data=await report.to_dict())


@pcb_router.post("/enterprise/{enterprise_id}/report/generate", summary="生成审核报告")
async def generate_audit_report(
    enterprise_id: int,
    auditor_id: int = Query(..., description="审核人ID"),
    auditor_name: str = Query(..., description="审核人姓名"),
):
    """生成或更新审核报告"""
    report = await pcb_audit_report_controller.generate_report(
        enterprise_id=enterprise_id, auditor_id=auditor_id, auditor_name=auditor_name
    )
    return Success(data=await report.to_dict(), msg="审核报告生成成功")


@pcb_router.post("/enterprise/{enterprise_id}/report/submit", summary="提交审核报告")
async def submit_audit_report(enterprise_id: int):
    """提交审核报告"""
    report = await pcb_audit_report_controller.submit_report(enterprise_id)
    if not report:
        raise HTTPException(status_code=404, detail="审核报告不存在")

    return Success(data=await report.to_dict(), msg="审核报告提交成功")


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



