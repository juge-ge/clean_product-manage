"""
PCB问题及清洁生产方案模块API路由
"""
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query, Body, Depends

from app.schemas.base import Success
from app.controllers.pcb_problem_solution import (
    problem_solution_scoring_controller,
    low_cost_scheme_controller,
    medium_high_cost_scheme_controller,
    get_level_two_and_below_issues
)
from app.schemas.pcb_problem_solution import (
    ProblemSolutionScoringCreate,
    ProblemSolutionScoringUpdate,
    ProblemSolutionScoringResponse,
    LowCostSchemeCreate,
    LowCostSchemeUpdate,
    LowCostSchemeResponse,
    MediumHighCostSchemeCreate,
    MediumHighCostSchemeUpdate,
    MediumHighCostSchemeResponse
)
from app.core.dependency import DependAuth

router = APIRouter(prefix="/problem-solution", tags=["PCB问题及清洁生产方案"])


# ==================== 问题清单 APIs ====================

@router.get("/enterprise/{enterprise_id}/issues", summary="获取Ⅱ级及以下问题清单")
async def get_issues(
    enterprise_id: int,
    current_user=DependAuth
):
    """
    获取企业Ⅱ级及以下的指标问题清单（排除限定性指标）
    """
    try:
        issues = await get_level_two_and_below_issues(enterprise_id)
        return Success(data=issues, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取问题清单失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/issues", summary="暂存问题清单")
async def save_issues(
    enterprise_id: int,
    items: List[Dict[str, Any]] = Body(..., description="问题清单项列表"),
    current_user=DependAuth
):
    """暂存问题清单（更新审核结果的comment字段）"""
    try:
        from app.controllers.pcb import pcb_audit_result_controller
        
        for item in items:
            indicator_id = item.get("indicator_id")
            problem = item.get("problem") or item.get("advice") or ""
            if indicator_id and problem:
                result = await pcb_audit_result_controller.get_or_create_result(enterprise_id, indicator_id)
                result.comment = problem
                await result.save()
        
        return Success(data={"count": len(items)}, msg="暂存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"暂存问题清单失败: {str(e)}"
        )


# ==================== 权重总和计分排序 APIs ====================

@router.get("/enterprise/{enterprise_id}/scoring-config", summary="获取权重总和计分排序配置")
async def get_scoring_config(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业的权重总和计分排序配置"""
    try:
        config = await problem_solution_scoring_controller.get_by_enterprise(enterprise_id)
        if not config:
            # 返回默认空配置
            return Success(
                data={
                    "factors": [],
                    "focuses": [],
                    "scores": {},
                    "rankings": []
                },
                msg="获取成功"
            )
        
        return Success(data=await config.to_dict(), msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取权重计分配置失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/scoring-config", summary="保存权重总和计分排序配置")
async def save_scoring_config(
    enterprise_id: int,
    data: Dict[str, Any] = Body(...),
    current_user=DependAuth
):
    """保存或更新企业的权重总和计分排序配置"""
    try:
        config = await problem_solution_scoring_controller.upsert(enterprise_id, data)
        return Success(data=await config.to_dict(), msg="保存成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存权重计分配置失败: {str(e)}"
        )


# ==================== 无/低费方案 APIs ====================

@router.get("/enterprise/{enterprise_id}/low-cost-schemes", summary="获取无/低费方案列表")
async def get_low_cost_schemes(
    enterprise_id: int,
    current_user=DependAuth
):
    """获取企业的所有无/低费方案"""
    try:
        schemes = await low_cost_scheme_controller.get_by_enterprise(enterprise_id)
        data = [await scheme.to_dict() for scheme in schemes]
        return Success(data=data, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取无/低费方案失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/low-cost-schemes", summary="创建或批量保存无/低费方案")
async def create_or_batch_save_low_cost_schemes(
    enterprise_id: int,
    schemes: List[LowCostSchemeCreate] = Body(..., description="无/低费方案列表"),
    current_user=DependAuth
):
    """批量保存无/低费方案（先删除后创建策略）"""
    try:
        schemes_list = [scheme.model_dump(exclude_unset=True) for scheme in schemes]
        saved_schemes = await low_cost_scheme_controller.batch_upsert(enterprise_id, schemes_list)
        data = [await scheme.to_dict() for scheme in saved_schemes]
        return Success(data=data, msg=f"成功保存 {len(data)} 个方案")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存无/低费方案失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/low-cost-schemes/single", summary="创建单个无/低费方案")
async def create_low_cost_scheme(
    enterprise_id: int,
    scheme: LowCostSchemeCreate,
    current_user=DependAuth
):
    """创建自定义无/低费方案"""
    try:
        scheme_dict = scheme.model_dump(exclude_unset=True)
        new_scheme = await low_cost_scheme_controller.create_custom(enterprise_id, scheme_dict)
        return Success(data=await new_scheme.to_dict(), msg="创建成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建无/低费方案失败: {str(e)}"
        )


@router.put("/enterprise/{enterprise_id}/low-cost-schemes/{scheme_id}", summary="更新无/低费方案")
async def update_low_cost_scheme(
    enterprise_id: int,
    scheme_id: int,
    scheme: LowCostSchemeUpdate,
    current_user=DependAuth
):
    """更新无/低费方案"""
    try:
        scheme_dict = scheme.model_dump(exclude_unset=True)
        updated_scheme = await low_cost_scheme_controller.update(
            id=scheme_id,
            obj_in=scheme_dict
        )
        if not updated_scheme:
            raise HTTPException(status_code=404, detail="方案不存在")
        return Success(data=await updated_scheme.to_dict(), msg="更新成功")
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新无/低费方案失败: {str(e)}"
        )


@router.delete("/enterprise/{enterprise_id}/low-cost-schemes/{scheme_id}", summary="删除无/低费方案")
async def delete_low_cost_scheme(
    enterprise_id: int,
    scheme_id: int,
    current_user=DependAuth
):
    """删除无/低费方案"""
    try:
        await low_cost_scheme_controller.remove(id=scheme_id)
        return Success(msg="删除成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除无/低费方案失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/scheme-library/low-cost", summary="获取方案库无/低费方案（根据指标筛选）")
async def get_library_low_cost_schemes(
    enterprise_id: int,
    indicator_ids: Optional[List[int]] = Query(None, description="指标ID列表，用于筛选"),
    current_user=DependAuth
):
    """获取方案库中的无/低费方案，可根据指标ID筛选"""
    try:
        from app.controllers.pcb_problem_solution import get_level_two_and_below_issues
        from app.models.pcb import PCBScheme, PCBIndicatorSchemeRelation
        
        # 如果没有指定指标ID，获取所有二级及以下指标
        if indicator_ids is None:
            issues = await get_level_two_and_below_issues(enterprise_id)
            indicator_ids = [issue["indicator_id"] for issue in issues]
        
        # 查找与指标关联的方案
        relations = await PCBIndicatorSchemeRelation.filter(
            indicator_id__in=indicator_ids
        )
        scheme_ids = list(set([r.scheme_id for r in relations]))
        
        # 获取方案信息（无/低费方案，通过scheme_type或investment判断）
        # 无/低费方案通常investment为空或较小，或者scheme_type包含"低费"
        all_schemes = await PCBScheme.filter(
            id__in=scheme_ids,
            is_active=True
        )
        # 筛选无/低费方案：investment为空或小于某个阈值（如10万），或者scheme_type包含"低"、"无"
        schemes = [
            s for s in all_schemes 
            if (s.investment is None or (s.investment and float(s.investment) < 10)) 
            or (s.scheme_type and ('低' in s.scheme_type or '无' in s.scheme_type))
        ]
        
        # 组装返回数据
        result = []
        for scheme in schemes:
            # 获取关联的指标
            related_relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id)
            related_indicator_ids = [r.indicator_id for r in related_relations]
            
            # 获取指标详情
            from app.models.pcb import PCBIndicator
            indicators = await PCBIndicator.filter(id__in=related_indicator_ids)
            indicator_names = [ind.name for ind in indicators]
            
            result.append({
                "id": scheme.id,
                "name": scheme.name,
                "description": scheme.description or "",
                "economic_benefit": scheme.economic_benefit or "",
                "environmental_benefit": scheme.environmental_benefit or "",
                "related_indicator_ids": related_indicator_ids,
                "related_indicator_names": indicator_names
            })
        
        return Success(data=result, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取方案库方案失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/low-cost-schemes/import", summary="从方案库导入无/低费方案")
async def import_low_cost_schemes(
    enterprise_id: int,
    scheme_ids: List[int] = Body(..., description="方案ID列表"),
    current_user=DependAuth
):
    """从方案库批量导入无/低费方案（根据方案ID列表）"""
    try:
        from app.models.pcb import PCBScheme, PCBIndicatorSchemeRelation
        
        schemes = await PCBScheme.filter(id__in=scheme_ids, is_active=True)
        
        results = []
        for scheme in schemes:
            # 检查是否已存在
            existing = await low_cost_scheme_controller.model.get_or_none(
                enterprise_id=enterprise_id,
                scheme_id=scheme.id
            )
            if existing:
                continue
            
            # 获取关联的指标ID
            related_indicators = await PCBIndicatorSchemeRelation.filter(
                scheme_id=scheme.id
            )
            indicator_ids_list = [r.indicator_id for r in related_indicators]
            
            # 创建导入记录
            imported_scheme = await low_cost_scheme_controller.model.create(
                enterprise_id=enterprise_id,
                source="library",
                scheme_id=scheme.id,
                indicator_ids=indicator_ids_list,
                name=scheme.name,
                intro=scheme.description,
                economic_benefit=scheme.economic_benefit,
                environment_benefit=scheme.environmental_benefit
            )
            results.append(imported_scheme)
        
        data = [await scheme.to_dict() for scheme in results]
        return Success(data=data, msg=f"成功导入 {len(data)} 个方案")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"导入方案失败: {str(e)}"
        )


# ==================== 中/高费方案 APIs ====================

@router.get("/enterprise/{enterprise_id}/medium-high-cost-schemes", summary="获取中/高费方案列表")
async def get_medium_high_cost_schemes(
    enterprise_id: int,
    cost_level: Optional[str] = Query(None, description="费用等级: middle(中费), high(高费)"),
    current_user=DependAuth
):
    """获取企业的中/高费方案"""
    try:
        schemes = await medium_high_cost_scheme_controller.get_by_enterprise(enterprise_id, cost_level)
        data = [await scheme.to_dict() for scheme in schemes]
        return Success(data=data, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取中/高费方案失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/medium-high-cost-schemes", summary="创建或批量保存中/高费方案")
async def create_or_batch_save_medium_high_cost_schemes(
    enterprise_id: int,
    schemes: List[MediumHighCostSchemeCreate] = Body(..., description="中/高费方案列表"),
    current_user=DependAuth
):
    """批量保存中/高费方案（先删除后创建策略）"""
    try:
        schemes_list = [scheme.model_dump(exclude_unset=True) for scheme in schemes]
        saved_schemes = await medium_high_cost_scheme_controller.batch_upsert(enterprise_id, schemes_list)
        data = [await scheme.to_dict() for scheme in saved_schemes]
        return Success(data=data, msg=f"成功保存 {len(data)} 个方案")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"保存中/高费方案失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/medium-high-cost-schemes/single", summary="创建单个中/高费方案")
async def create_medium_high_cost_scheme(
    enterprise_id: int,
    scheme: MediumHighCostSchemeCreate,
    current_user=DependAuth
):
    """创建自定义中/高费方案"""
    try:
        scheme_dict = scheme.model_dump(exclude_unset=True)
        new_scheme = await medium_high_cost_scheme_controller.create_custom(enterprise_id, scheme_dict)
        return Success(data=await new_scheme.to_dict(), msg="创建成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建中/高费方案失败: {str(e)}"
        )


@router.put("/enterprise/{enterprise_id}/medium-high-cost-schemes/{scheme_id}", summary="更新中/高费方案")
async def update_medium_high_cost_scheme(
    enterprise_id: int,
    scheme_id: int,
    scheme: MediumHighCostSchemeUpdate,
    current_user=DependAuth
):
    """更新中/高费方案"""
    try:
        scheme_dict = scheme.model_dump(exclude_unset=True)
        updated_scheme = await medium_high_cost_scheme_controller.update(
            id=scheme_id,
            obj_in=scheme_dict
        )
        if not updated_scheme:
            raise HTTPException(status_code=404, detail="方案不存在")
        return Success(data=await updated_scheme.to_dict(), msg="更新成功")
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新中/高费方案失败: {str(e)}"
        )


@router.delete("/enterprise/{enterprise_id}/medium-high-cost-schemes/{scheme_id}", summary="删除中/高费方案")
async def delete_medium_high_cost_scheme(
    enterprise_id: int,
    scheme_id: int,
    current_user=DependAuth
):
    """删除中/高费方案"""
    try:
        await medium_high_cost_scheme_controller.remove(id=scheme_id)
        return Success(msg="删除成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除中/高费方案失败: {str(e)}"
        )


@router.get("/enterprise/{enterprise_id}/scheme-library/medium-high-cost", summary="获取方案库中/高费方案（根据指标筛选）")
async def get_library_medium_high_cost_schemes(
    enterprise_id: int,
    indicator_ids: Optional[List[int]] = Query(None, description="指标ID列表，用于筛选"),
    cost_level: Optional[str] = Query(None, description="费用等级: middle(中费), high(高费)"),
    current_user=DependAuth
):
    """获取方案库中的中/高费方案，可根据指标ID和费用等级筛选"""
    try:
        from app.controllers.pcb_problem_solution import get_level_two_and_below_issues
        from app.models.pcb import PCBScheme, PCBIndicatorSchemeRelation
        
        # 如果没有指定指标ID，获取所有二级及以下指标
        if indicator_ids is None:
            issues = await get_level_two_and_below_issues(enterprise_id)
            indicator_ids = [issue["indicator_id"] for issue in issues]
        
        # 查找与指标关联的方案
        relations = await PCBIndicatorSchemeRelation.filter(
            indicator_id__in=indicator_ids
        )
        scheme_ids = list(set([r.scheme_id for r in relations]))
        
        # 获取方案信息（中/高费方案）
        # 通过investment或scheme_type判断中/高费方案
        all_schemes = await PCBScheme.filter(
            id__in=scheme_ids,
            is_active=True
        )
        # 筛选中/高费方案：investment存在且大于等于某个阈值（如10万），或者scheme_type包含"中"、"高"
        schemes = [
            s for s in all_schemes 
            if (s.investment and float(s.investment) >= 10)
            or (s.scheme_type and ('中' in s.scheme_type or '高' in s.scheme_type))
        ]
        # 如果指定了cost_level，进一步筛选
        if cost_level == "middle":
            schemes = [
                s for s in schemes 
                if (s.scheme_type and '中' in s.scheme_type)
                or (s.investment and 10 <= float(s.investment) < 100)
            ]
        elif cost_level == "high":
            schemes = [
                s for s in schemes 
                if (s.scheme_type and '高' in s.scheme_type)
                or (s.investment and float(s.investment) >= 100)
            ]
        
        # 组装返回数据
        result = []
        for scheme in schemes:
            # 获取关联的指标
            related_relations = await PCBIndicatorSchemeRelation.filter(scheme_id=scheme.id)
            related_indicator_ids = [r.indicator_id for r in related_relations]
            
            # 获取指标详情
            from app.models.pcb import PCBIndicator
            indicators = await PCBIndicator.filter(id__in=related_indicator_ids)
            indicator_names = [ind.name for ind in indicators]
            
            # 判断费用等级
            scheme_cost_level = "middle"
            if scheme.investment:
                inv = float(scheme.investment)
                if inv >= 100:
                    scheme_cost_level = "high"
                elif inv >= 10:
                    scheme_cost_level = "middle"
            elif scheme.scheme_type:
                if '高' in scheme.scheme_type:
                    scheme_cost_level = "high"
                elif '中' in scheme.scheme_type:
                    scheme_cost_level = "middle"
            
            result.append({
                "id": scheme.id,
                "name": scheme.name,
                "description": scheme.description or "",
                "economic_benefit": scheme.economic_benefit or "",
                "environmental_benefit": scheme.environmental_benefit or "",
                "cost_level": scheme_cost_level,
                "related_indicator_ids": related_indicator_ids,
                "related_indicator_names": indicator_names
            })
        
        return Success(data=result, msg="获取成功")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取方案库方案失败: {str(e)}"
        )


@router.post("/enterprise/{enterprise_id}/medium-high-cost-schemes/import", summary="从方案库导入中/高费方案")
async def import_medium_high_cost_schemes(
    enterprise_id: int,
    data: Dict[str, Any] = Body(..., description="请求体，包含scheme_ids和cost_level"),
    current_user=DependAuth
):
    """从方案库批量导入中/高费方案（根据方案ID列表）"""
    try:
        from app.models.pcb import PCBScheme, PCBIndicatorSchemeRelation
        
        scheme_ids = data.get("scheme_ids", [])
        cost_level = data.get("cost_level", "middle")
        
        schemes = await PCBScheme.filter(id__in=scheme_ids, is_active=True)
        
        results = []
        for scheme in schemes:
            # 检查是否已存在
            existing = await medium_high_cost_scheme_controller.model.get_or_none(
                enterprise_id=enterprise_id,
                scheme_id=scheme.id
            )
            if existing:
                continue
            
            # 获取关联的指标ID
            related_indicators = await PCBIndicatorSchemeRelation.filter(
                scheme_id=scheme.id
            )
            indicator_ids_list = [r.indicator_id for r in related_indicators]
            
            # 创建导入记录
            imported_scheme = await medium_high_cost_scheme_controller.model.create(
                enterprise_id=enterprise_id,
                source="library",
                cost_level=cost_level,
                scheme_id=scheme.id,
                indicator_ids=indicator_ids_list,
                name=scheme.name,
                intro=scheme.description,
                economic_benefit=scheme.economic_benefit,
                environment_benefit=scheme.environmental_benefit
            )
            results.append(imported_scheme)
        
        result_data = [await scheme.to_dict() for scheme in results]
        return Success(data=result_data, msg=f"成功导入 {len(result_data)} 个方案")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"导入方案失败: {str(e)}"
        )
