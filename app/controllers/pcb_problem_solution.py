"""
PCB问题及清洁生产方案模块Controllers
"""
from typing import List, Dict, Optional, Any
from decimal import Decimal

from app.core.crud import CRUDBase
from app.models.pcb import (
    PCBProblemSolutionScoring,
    PCBLowCostScheme,
    PCBMediumHighCostScheme,
    PCBAuditResult,
    PCBIndicator,
    PCBScheme,
    PCBIndicatorSchemeRelation
)


async def get_level_two_and_below_issues(enterprise_id: int) -> List[Dict]:
    """
    获取企业Ⅱ级及以下的指标问题清单
    
    返回格式：
    [
        {
            "indicator_id": int,
            "primary_indicator": str,  # 一级指标（category）
            "primary_weight": Decimal,  # 一级指标权重（category_weight）
            "secondary_indicator": str,  # 二级指标（name）
            "secondary_weight": Decimal,  # 二级指标权重（weight）
            "current_level": str  # 当前评级（II级、III级、不达标）
        },
        ...
    ]
    """
    # 获取所有审核结果
    audit_results = await PCBAuditResult.filter(enterprise_id=enterprise_id).order_by("indicator_id")
    
    # 获取所有指标
    indicators = await PCBIndicator.all()
    indicator_map = {ind.id: ind for ind in indicators}
    
    # 筛选Ⅱ级及以下的指标（排除限定性指标）
    issues = []
    for result in audit_results:
        indicator = indicator_map.get(result.indicator_id)
        if not indicator:
            continue
        
        # 排除限定性指标
        if indicator.is_limiting:
            continue
        
        # 只包含Ⅱ级、Ⅲ级、不达标
        if result.level and result.level in ["II级", "III级", "不达标"]:
            issues.append({
                "indicator_id": indicator.id,
                "primary_indicator": indicator.category,
                "primary_weight": float(indicator.category_weight) if indicator.category_weight else 0.0,
                "secondary_indicator": indicator.name,
                "secondary_weight": float(indicator.weight) if indicator.weight else 0.0,
                "current_level": result.level
            })
    
    return issues


from app.schemas.pcb_problem_solution import (
    ProblemSolutionScoringCreate,
    ProblemSolutionScoringUpdate,
    LowCostSchemeCreate,
    LowCostSchemeUpdate,
    MediumHighCostSchemeCreate,
    MediumHighCostSchemeUpdate
)


class PCBProblemSolutionScoringController(
    CRUDBase[PCBProblemSolutionScoring, ProblemSolutionScoringCreate, ProblemSolutionScoringUpdate]
):
    """问题方案权重计分排序控制器"""

    def __init__(self):
        super().__init__(model=PCBProblemSolutionScoring)

    async def get_by_enterprise(self, enterprise_id: int) -> Optional[PCBProblemSolutionScoring]:
        """获取企业的权重计分配置"""
        return await self.model.get_or_none(enterprise_id=enterprise_id)

    async def upsert(self, enterprise_id: int, data: Dict) -> PCBProblemSolutionScoring:
        """更新或创建权重计分配置"""
        existing = await self.get_by_enterprise(enterprise_id)
        
        # 计算排序结果
        rankings = None
        if data.get("scores") and data.get("factors") and data.get("focuses"):
            rankings = self._calculate_ranking(
                data.get("focuses", []),
                data.get("factors", []),
                data.get("scores", {})
            )
            data["rankings"] = rankings
        
        if existing:
            # 更新现有记录
            for key, value in data.items():
                setattr(existing, key, value)
            await existing.save()
            return existing
        else:
            # 创建新记录
            return await self.model.create(enterprise_id=enterprise_id, **data)
    
    def _calculate_ranking(self, focuses: List[Dict], factors: List[Dict], scores: Dict) -> List[Dict]:
        """计算排序结果"""
        ranked = []
        for focus in focuses:
            focus_id = str(focus.get("id"))
            total_score = 0
            
            # 计算总分：Σ (RW * W)
            if focus_id in scores:
                for factor in factors:
                    factor_key = factor.get("key")
                    weight = factor.get("weight", 0)
                    if factor_key in scores[focus_id]:
                        score_item = scores[focus_id][factor_key]
                        if isinstance(score_item, dict):
                            rw = score_item.get("rw", 0)
                        else:
                            rw = 0
                        total_score += rw * weight
            
            ranked.append({
                "id": focus.get("id"),
                "name": focus.get("name"),
                "total_score": total_score
            })
        
        # 按分数降序排序
        ranked.sort(key=lambda x: x.get("total_score", 0), reverse=True)
        return ranked


class PCBLowCostSchemeController(
    CRUDBase[PCBLowCostScheme, LowCostSchemeCreate, LowCostSchemeUpdate]
):
    """无/低费方案控制器"""

    def __init__(self):
        super().__init__(model=PCBLowCostScheme)

    async def get_by_enterprise(self, enterprise_id: int) -> List[PCBLowCostScheme]:
        """获取企业的所有无/低费方案"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by("-created_at")

    async def create_custom(self, enterprise_id: int, data: Dict) -> PCBLowCostScheme:
        """创建自定义无/低费方案"""
        # 从data中移除source（如果存在），因为我们总是设置为"custom"
        data = data.copy()  # 避免修改原始字典
        data.pop("source", None)  # 移除source（如果存在）
        
        return await self.model.create(
            enterprise_id=enterprise_id,
            source="custom",
            **data
        )
    
    async def batch_upsert(self, enterprise_id: int, schemes: List[Dict]) -> List[PCBLowCostScheme]:
        """批量保存无/低费方案（先删除后创建策略）"""
        # 先删除该企业的所有无/低费方案
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 批量创建新记录
        results = []
        for scheme_data in schemes:
            new_scheme = await self.model.create(
                enterprise_id=enterprise_id,
                **scheme_data
            )
            results.append(new_scheme)
        
        return results

    async def batch_import_from_library(
        self, enterprise_id: int, indicator_ids: List[int]
    ) -> List[PCBLowCostScheme]:
        """从方案库批量导入无/低费方案"""
        # 查找与指标关联的方案
        relations = await PCBIndicatorSchemeRelation.filter(
            indicator_id__in=indicator_ids
        )
        
        scheme_ids = list(set([r.scheme_id for r in relations]))
        schemes = await PCBScheme.filter(id__in=scheme_ids, is_active=True)
        
        results = []
        for scheme in schemes:
            # 检查是否已存在
            existing = await self.model.get_or_none(
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
            imported_scheme = await self.model.create(
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
        
        return results


class PCBMediumHighCostSchemeController(
    CRUDBase[PCBMediumHighCostScheme, MediumHighCostSchemeCreate, MediumHighCostSchemeUpdate]
):
    """中/高费方案控制器"""

    def __init__(self):
        super().__init__(model=PCBMediumHighCostScheme)

    async def get_by_enterprise(
        self, enterprise_id: int, cost_level: Optional[str] = None
    ) -> List[PCBMediumHighCostScheme]:
        """获取企业的中/高费方案"""
        query = self.model.filter(enterprise_id=enterprise_id)
        if cost_level:
            query = query.filter(cost_level=cost_level)
        return await query.order_by("-created_at")

    async def create_custom(self, enterprise_id: int, data: Dict) -> PCBMediumHighCostScheme:
        """创建自定义中/高费方案"""
        # 从data中移除source和cost_level（如果存在），因为我们总是设置为固定值
        data = data.copy()  # 避免修改原始字典
        data.pop("source", None)  # 移除source（如果存在）
        # 注意：cost_level保留，因为中/高费方案需要区分费用等级
        
        return await self.model.create(
            enterprise_id=enterprise_id,
            source="custom",
            **data
        )
    
    async def batch_upsert(self, enterprise_id: int, schemes: List[Dict]) -> List[PCBMediumHighCostScheme]:
        """批量保存中/高费方案（先删除后创建策略）"""
        # 先删除该企业的所有中/高费方案
        await self.model.filter(enterprise_id=enterprise_id).delete()
        
        # 批量创建新记录
        results = []
        for scheme_data in schemes:
            new_scheme = await self.model.create(
                enterprise_id=enterprise_id,
                **scheme_data
            )
            results.append(new_scheme)
        
        return results

    async def batch_import_from_library(
        self, enterprise_id: int, indicator_ids: List[int], cost_level: str = "middle"
    ) -> List[PCBMediumHighCostScheme]:
        """从方案库批量导入中/高费方案"""
        # 查找与指标关联的方案
        relations = await PCBIndicatorSchemeRelation.filter(
            indicator_id__in=indicator_ids
        )
        
        scheme_ids = list(set([r.scheme_id for r in relations]))
        schemes = await PCBScheme.filter(id__in=scheme_ids, is_active=True)
        
        results = []
        for scheme in schemes:
            # 检查是否已存在
            existing = await self.model.get_or_none(
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
            imported_scheme = await self.model.create(
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
        
        return results


# 创建控制器实例
problem_solution_scoring_controller = PCBProblemSolutionScoringController()
low_cost_scheme_controller = PCBLowCostSchemeController()
medium_high_cost_scheme_controller = PCBMediumHighCostSchemeController()
