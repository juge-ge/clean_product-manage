"""
PCB行业清洁生产审核模块Controller
实现企业、指标、审核结果、方案的CRUD操作和业务逻辑
"""
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

from tortoise.expressions import Q
from tortoise.functions import Count

from app.core.crud import CRUDBase
from app.models.pcb import (
    PCBAuditReport,
    PCBAuditResult,
    PCBEnterprise,
    PCBEnterpriseScheme,
    PCBIndicator,
    PCBIndicatorSchemeRelation,
    PCBPreAuditData,
    PCBScheme,
)
from app.schemas.pcb import (
    PCBAuditResultCreate,
    PCBAuditResultUpdate,
    PCBEnterpriseCreate,
    PCBEnterpriseSchemeCreate,
    PCBEnterpriseSchemeUpdate,
    PCBEnterpriseUpdate,
    PCBIndicatorCreate,
    PCBIndicatorSchemeRelationCreate,
    PCBIndicatorUpdate,
    PCBPreAuditDataCreate,
    PCBPreAuditDataUpdate,
    PCBSchemeCreate,
    PCBSchemeUpdate,
)


class PCBEnterpriseController(CRUDBase[PCBEnterprise, PCBEnterpriseCreate, PCBEnterpriseUpdate]):
    """PCB企业控制器"""

    def __init__(self):
        super().__init__(model=PCBEnterprise)

    async def get_list(
        self,
        page: int = 1,
        page_size: int = 10,
        search: Optional[str] = None,
        region: Optional[str] = None,
        district: Optional[str] = None,
        audit_status: Optional[str] = None,
    ) -> tuple[List[PCBEnterprise], int]:
        """
        获取企业列表（支持搜索和筛选）
        """
        query = self.model.filter(is_deleted=False)

        # 搜索条件
        if search:
            query = query.filter(
                Q(name__icontains=search)
                | Q(region__icontains=search)
                | Q(district__icontains=search)
            )

        # 筛选条件
        if region:
            query = query.filter(region=region)
        if district:
            query = query.filter(district=district)
        if audit_status:
            query = query.filter(audit_status=audit_status)

        # 分页
        total = await query.count()
        offset = (page - 1) * page_size
        enterprises = await query.offset(offset).limit(page_size).order_by("-created_at")

        return enterprises, total

    async def soft_delete(self, id: int) -> bool:
        """软删除企业"""
        enterprise = await self.model.get_or_none(id=id)
        if enterprise:
            enterprise.is_deleted = True
            await enterprise.save()
            return True
        return False


class PCBIndicatorController(CRUDBase[PCBIndicator, PCBIndicatorCreate, PCBIndicatorUpdate]):
    """PCB指标控制器"""

    def __init__(self):
        super().__init__(model=PCBIndicator)

    async def get_by_indicator_id(self, indicator_id: int) -> Optional[PCBIndicator]:
        """根据指标编号获取指标"""
        return await self.model.get_or_none(indicator_id=indicator_id)

    async def get_all(self) -> List[PCBIndicator]:
        """获取所有指标"""
        return await self.model.all().order_by("indicator_id")

    async def get_indicators_by_category(self, category: str) -> List[PCBIndicator]:
        """根据类别获取指标列表"""
        return await self.model.filter(category=category).order_by("order", "indicator_id")

    async def get_limiting_indicators(self) -> List[PCBIndicator]:
        """获取所有限定性指标"""
        return await self.model.filter(is_limiting=True).order_by("indicator_id")

    async def get_indicators_tree(self) -> List[Dict]:
        """获取指标树形结构"""
        indicators = await self.model.all().order_by("category", "order", "indicator_id")

        # 按类别分组
        tree = {}
        for indicator in indicators:
            if indicator.category not in tree:
                tree[indicator.category] = {
                    "label": indicator.category,
                    "key": indicator.category,
                    "children": [],
                }

            tree[indicator.category]["children"].append(
                {
                    "label": indicator.name,
                    "key": str(indicator.indicator_id),
                    "indicator_id": indicator.indicator_id,
                    "is_limiting": indicator.is_limiting,
                }
            )

        return list(tree.values())


class PCBAuditResultController(CRUDBase[PCBAuditResult, PCBAuditResultCreate, PCBAuditResultUpdate]):
    """PCB审核结果控制器"""

    def __init__(self):
        super().__init__(model=PCBAuditResult)

    async def get_enterprise_results(self, enterprise_id: int) -> List[PCBAuditResult]:
        """获取企业所有审核结果"""
        return await self.model.filter(enterprise_id=enterprise_id).order_by("indicator_id")
    
    async def get_level2_and_below_indicators(self, enterprise_id: int) -> List[Dict]:
        """获取企业Ⅱ级及以下的指标列表（用于问题清单）"""
        # 查询Ⅱ级、Ⅲ级、不达标的审核结果
        results = await self.model.filter(
            enterprise_id=enterprise_id,
            level__in=["II级", "III级", "不达标"]
        ).order_by("indicator_id")
        
        # 获取所有指标信息
        from app.models.pcb import PCBIndicator
        indicators = await PCBIndicator.all()
        indicator_map = {ind.id: ind for ind in indicators}
        
        # 构建问题清单
        issue_list = []
        for result in results:
            indicator = indicator_map.get(result.indicator_id)
            if not indicator:
                continue
            
            issue_list.append({
                "indicator_id": result.indicator_id,
                "primary_indicator": indicator.category,
                "primary_weight": float(indicator.category_weight) if indicator.category_weight else 0.0,
                "secondary_indicator": indicator.name,
                "secondary_weight": float(indicator.weight) if indicator.weight else 0.0,
                "current_level": result.level or "",
                "problem": result.comment or "",
                "advice": "",
                "department": "",
                "owner": "",
                "deadline": ""
            })
        
        return issue_list

    async def get_or_create_result(
        self, enterprise_id: int, indicator_id: int
    ) -> PCBAuditResult:
        """获取或创建审核结果"""
        result = await self.model.get_or_none(enterprise_id=enterprise_id, indicator_id=indicator_id)
        if not result:
            result = await self.model.create(enterprise_id=enterprise_id, indicator_id=indicator_id)
        return result

    async def update_indicator_level(
        self,
        enterprise_id: int,
        indicator_id: int,
        level: str,
        score: Optional[Decimal] = None,
        manual_override: bool = False,
        override_reason: Optional[str] = None,
        auditor_id: Optional[int] = None,
        selected_scheme_ids: Optional[List[int]] = None,
    ) -> PCBAuditResult:
        """更新指标评级"""
        result = await self.get_or_create_result(enterprise_id, indicator_id)

        result.level = level
        if score is not None:
            result.score = score
        result.manual_override = manual_override
        result.override_reason = override_reason
        if selected_scheme_ids is not None:
            result.selected_scheme_ids = selected_scheme_ids
            result.scheme_selection_date = datetime.now()
        if auditor_id:
            result.auditor_id = auditor_id
        result.audit_date = datetime.now()

        await result.save()
        return result

    async def batch_update_results(
        self, enterprise_id: int, results_data: List[Dict]
    ) -> List[PCBAuditResult]:
        """批量更新审核结果"""
        from datetime import datetime
        updated_results = []
        for data in results_data:
            indicator_id = data.get("indicator_id")
            level = data.get("level")
            score = data.get("score")
            current_value = data.get("current_value")
            remark = data.get("remark") or data.get("comment")  # 支持remark和comment两个字段名

            result = await self.get_or_create_result(enterprise_id, indicator_id)
            if level is not None:
                result.level = level
            if score is not None:
                result.score = Decimal(str(score))
            if current_value is not None:
                # 如果是字符串类型（等级文本），不存储到Decimal字段，保持current_value为None
                # 但可以通过其他方式存储（如果模型有文本字段的话）
                if isinstance(current_value, str):
                    # 字符串类型（如"Ⅰ级、Ⅱ级、Ⅲ级"）不存储在Decimal字段
                    # 可以存储在comment字段中作为备注，或者保持current_value为None
                    pass
                else:
                    result.current_value = Decimal(str(current_value))
            if remark is not None:
                result.comment = remark
            
            # 更新审核时间
            result.audit_date = datetime.now()
            await result.save()
            updated_results.append(result)

        return updated_results

    async def get_indicator_recommended_schemes(self, enterprise_id: int, indicator_id: int) -> List[Dict]:
        """获取指标推荐方案"""
        # 获取指标方案关联
        relation_controller = PCBIndicatorSchemeRelationController()
        relations = await relation_controller.get_schemes_by_indicator(indicator_id)
        
        # 获取方案详情
        schemes = []
        for relation in relations:
            scheme = await PCBScheme.get_or_none(id=relation.scheme_id)
            if scheme:
                schemes.append({
                    "id": scheme.id,
                    "scheme_id": scheme.scheme_id,
                    "name": scheme.name,
                    "type": scheme.scheme_type,
                    "description": scheme.description,
                    "implementation": scheme.implementation,
                    "expected_effect": scheme.environmental_benefit,
                    "investment": float(scheme.investment) if scheme.investment else 0,
                    "payback_period": float(scheme.payback_period) if scheme.payback_period else 0,
                    "relevance_score": float(relation.relevance_score),
                    "priority": relation.priority,
                    "recommendation_reason": relation.recommendation_reason
                })
        
        # 按优先级和关联度排序
        schemes.sort(key=lambda x: (x["priority"], -x["relevance_score"]))
        return schemes

    async def calculate_summary(
        self, 
        enterprise_id: int,
        product_outputs: Optional[Dict[int, float]] = None
    ) -> Dict:
        """
        计算审核汇总数据（使用新的综合评价指数计算方法）
        
        参数:
            enterprise_id: 企业ID
            product_outputs: 产品产量数据 {indicator_id: output_value}
        """
        from app.utils.pcb_score_calculator import (
            calculate_comprehensive_evaluation_index,
            determine_clean_production_level
        )
        
        results = await self.get_enterprise_results(enterprise_id)
        
        # 准备指标数据用于计算综合评价指数
        indicators_data = []
        limiting_indicators_level = []
        
        improvement_items = 0
        limiting_indicators = 0
        
        for result in results:
            # 获取指标信息
            indicator = await PCBIndicator.get_or_none(id=result.indicator_id)
            if not indicator:
                continue
            
            # 统计限定性指标
            if indicator.is_limiting:
                limiting_indicators += 1
                if result.level:
                    limiting_indicators_level.append(result.level)
            
            # 统计待改进项：三级及三级以下的指标个数，删去限定性指标
            if result.level and result.level not in ["I级", "待评估"]:
                # 排除限定性指标
                if not indicator.is_limiting:
                    # 三级及三级以下：II级、III级、不达标
                    if result.level in ["II级", "III级", "不达标"]:
                        improvement_items += 1
            
            # 准备指标数据
            indicators_data.append({
                'indicator_id': result.indicator_id,
                'id': result.indicator_id,
                'category': indicator.category,
                'category_weight': float(indicator.category_weight) if indicator.category_weight else 0,
                'weight': float(indicator.weight) if indicator.weight else 0,
                'is_dynamic_weight': indicator.is_dynamic_weight,
                'level': result.level if result.level and result.level != "待评估" else None,
                'is_limiting': indicator.is_limiting,
            })
        
        # 计算YⅠ, YⅡ, YⅢ
        y1 = calculate_comprehensive_evaluation_index(
            indicators_data, 'I级', product_outputs
        )
        y2 = calculate_comprehensive_evaluation_index(
            indicators_data, 'II级', product_outputs
        )
        y3 = calculate_comprehensive_evaluation_index(
            indicators_data, 'III级', product_outputs
        )
        
        # 准备所有指标的评级信息（用于判定I级时需要检查非限定性指标）
        all_indicators_level = [
            {
                'indicator_id': ind.get('indicator_id') or ind.get('id'),
                'level': ind.get('level'),
                'is_limiting': ind.get('is_limiting', False)
            }
            for ind in indicators_data if ind.get('level')
        ]
        
        # 确定清洁生产水平
        overall_level = determine_clean_production_level(
            y1, y2, y3, limiting_indicators_level, all_indicators_level
        )
        
        return {
            "y1": float(y1),
            "y2": float(y2),
            "y3": float(y3),
            "total_score": float(y1),  # 保持兼容性，使用YⅠ作为总分
            "overall_level": overall_level,
            "improvement_items": improvement_items,
            "limiting_indicators": limiting_indicators,
            "limiting_indicators_level": limiting_indicators_level,
            "evaluation_details": {
                "y1": float(y1),
                "y2": float(y2),
                "y3": float(y3),
                "meet_level1_conditions": y1 >= 85 and overall_level == "I级",
                "meet_level2_conditions": y2 >= 85 and overall_level == "II级",
                "meet_level3_conditions": y3 == 100 and overall_level == "III级",
            }
        }


class PCBSchemeController(CRUDBase[PCBScheme, PCBSchemeCreate, PCBSchemeUpdate]):
    """PCB方案控制器"""

    def __init__(self):
        super().__init__(model=PCBScheme)

    async def get_by_scheme_id(self, scheme_id: int) -> Optional[PCBScheme]:
        """根据方案编号获取方案"""
        return await self.model.get_or_none(scheme_id=scheme_id)

    async def get_schemes_by_indicator(self, indicator_id: int) -> List[Dict]:
        """获取指标关联的方案列表"""
        relations = await PCBIndicatorSchemeRelation.filter(indicator_id=indicator_id).all()

        schemes = []
        for relation in relations:
            scheme = await self.model.get_or_none(id=relation.scheme_id)
            if scheme and scheme.is_active:
                scheme_dict = await scheme.to_dict()
                scheme_dict["relevance_score"] = float(relation.relevance_score)
                schemes.append(scheme_dict)

        # 按关联度排序
        schemes.sort(key=lambda x: x["relevance_score"], reverse=True)
        return schemes

    async def search_schemes(
        self,
        page: int = 1,
        page_size: int = 10,
        search: Optional[str] = None,
        scheme_type: Optional[str] = None,
        indicator_ids: Optional[List[int]] = None,
    ) -> tuple[List[PCBScheme], int]:
        """搜索方案"""
        query = self.model.filter(is_active=True)

        # 搜索条件
        if search:
            query = query.filter(
                Q(name__icontains=search)
                | Q(description__icontains=search)
                | Q(problem__icontains=search)
            )

        # 方案类型筛选
        if scheme_type:
            query = query.filter(scheme_type=scheme_type)

        # 指标筛选
        if indicator_ids:
            # 获取关联的方案ID
            relations = await PCBIndicatorSchemeRelation.filter(
                indicator_id__in=indicator_ids
            ).all()
            scheme_ids = list(set([r.scheme_id for r in relations]))
            query = query.filter(id__in=scheme_ids)

        # 分页
        total = await query.count()
        offset = (page - 1) * page_size
        schemes = await query.offset(offset).limit(page_size).order_by("scheme_id")

        return schemes, total


class PCBIndicatorSchemeRelationController(
    CRUDBase[
        PCBIndicatorSchemeRelation,
        PCBIndicatorSchemeRelationCreate,
        PCBIndicatorSchemeRelationCreate,
    ]
):
    """PCB指标方案关联控制器"""

    def __init__(self):
        super().__init__(model=PCBIndicatorSchemeRelation)

    async def create_relation(
        self, indicator_id: int, scheme_id: int, relevance_score: Decimal = Decimal("1.0"),
        priority: int = 1, recommendation_reason: str = None
    ) -> PCBIndicatorSchemeRelation:
        """创建指标方案关联"""
        # 检查是否已存在
        existing = await self.model.get_or_none(indicator_id=indicator_id, scheme_id=scheme_id)
        if existing:
            existing.relevance_score = relevance_score
            existing.priority = priority
            existing.recommendation_reason = recommendation_reason
            await existing.save()
            return existing

        return await self.model.create(
            indicator_id=indicator_id, scheme_id=scheme_id, relevance_score=relevance_score,
            priority=priority, recommendation_reason=recommendation_reason
        )

    async def batch_create_relations(self, relations_data: List[Dict]) -> List[PCBIndicatorSchemeRelation]:
        """批量创建指标方案关联"""
        relations = []
        for data in relations_data:
            relation = await self.create_relation(
                indicator_id=data["indicator_id"],
                scheme_id=data["scheme_id"],
                relevance_score=Decimal(str(data.get("relevance_score", 1.0))),
                priority=data.get("priority", 1),
                recommendation_reason=data.get("recommendation_reason")
            )
            relations.append(relation)
        return relations

    async def get_schemes_by_indicator(self, indicator_id: int) -> List[PCBIndicatorSchemeRelation]:
        """根据指标ID获取推荐方案"""
        relations = await self.model.filter(indicator_id=indicator_id)
        return relations

    async def get_indicators_by_scheme(self, scheme_id: int) -> List[PCBIndicatorSchemeRelation]:
        """根据方案ID获取关联指标"""
        relations = await self.model.filter(scheme_id=scheme_id)
        return relations


class PCBPreAuditDataController(CRUDBase[PCBPreAuditData, PCBPreAuditDataCreate, PCBPreAuditDataUpdate]):
    """PCB预审核数据控制器"""

    def __init__(self):
        super().__init__(model=PCBPreAuditData)

    async def get_by_enterprise(self, enterprise_id: int) -> Optional[PCBPreAuditData]:
        """获取企业预审核数据"""
        return await self.model.get_or_none(enterprise_id=enterprise_id)

    async def update_or_create(self, enterprise_id: int, data: Dict) -> PCBPreAuditData:
        """更新或创建预审核数据"""
        pre_audit = await self.get_by_enterprise(enterprise_id)

        if pre_audit:
            # 更新现有数据
            for key, value in data.items():
                if value is not None:
                    setattr(pre_audit, key, value)
            await pre_audit.save()
        else:
            # 创建新数据
            pre_audit = await self.model.create(enterprise_id=enterprise_id, **data)

        return pre_audit

    async def submit_data(self, enterprise_id: int) -> PCBPreAuditData:
        """提交预审核数据"""
        pre_audit = await self.get_by_enterprise(enterprise_id)
        if pre_audit:
            pre_audit.status = "submitted"
            pre_audit.submitted_at = datetime.now()
            await pre_audit.save()
        return pre_audit


class PCBEnterpriseSchemeController(
    CRUDBase[PCBEnterpriseScheme, PCBEnterpriseSchemeCreate, PCBEnterpriseSchemeUpdate]
):
    """PCB企业方案控制器"""

    def __init__(self):
        super().__init__(model=PCBEnterpriseScheme)

    async def get_enterprise_schemes(
        self, enterprise_id: int, status: Optional[str] = None
    ) -> List[PCBEnterpriseScheme]:
        """获取企业选择的方案"""
        query = self.model.filter(enterprise_id=enterprise_id)
        if status:
            query = query.filter(status=status)
        return await query.all()

    async def recommend_scheme(
        self, enterprise_id: int, scheme_id: int, indicator_id: Optional[int] = None
    ) -> PCBEnterpriseScheme:
        """推荐方案给企业"""
        # 检查是否已存在
        existing = await self.model.get_or_none(
            enterprise_id=enterprise_id, scheme_id=scheme_id
        )
        if existing:
            return existing

        return await self.model.create(
            enterprise_id=enterprise_id,
            scheme_id=scheme_id,
            indicator_id=indicator_id,
            status="recommended",
        )

    async def batch_recommend_schemes(
        self, enterprise_id: int, scheme_indicator_pairs: List[Dict]
    ) -> List[PCBEnterpriseScheme]:
        """批量推荐方案"""
        recommendations = []
        for pair in scheme_indicator_pairs:
            rec = await self.recommend_scheme(
                enterprise_id=enterprise_id,
                scheme_id=pair["scheme_id"],
                indicator_id=pair.get("indicator_id"),
            )
            recommendations.append(rec)
        return recommendations

    async def save_selected_schemes(
        self, enterprise_id: int, selected_schemes: List[Dict]
    ) -> List[PCBEnterpriseScheme]:
        """保存企业选定的方案"""
        # 先删除旧的选定方案
        await self.model.filter(enterprise_id=enterprise_id, status="selected").delete()
        
        # 保存新的选定方案
        selected_list = []
        for scheme_data in selected_schemes:
            scheme = await self.model.create(
                enterprise_id=enterprise_id,
                scheme_id=scheme_data["scheme_id"],
                indicator_id=scheme_data.get("indicator_id"),
                status="selected"
            )
            selected_list.append(scheme)
        
        return selected_list


class PCBAuditReportController(CRUDBase[PCBAuditReport, Dict, Dict]):
    """PCB审核报告控制器"""

    def __init__(self):
        super().__init__(model=PCBAuditReport)

    async def get_by_enterprise(self, enterprise_id: int) -> Optional[PCBAuditReport]:
        """获取企业审核报告"""
        return await self.model.get_or_none(enterprise_id=enterprise_id)

    async def generate_report(
        self, enterprise_id: int, auditor_id: int, auditor_name: str
    ) -> PCBAuditReport:
        """生成审核报告"""
        # 获取审核汇总数据
        audit_controller = PCBAuditResultController()
        summary = await audit_controller.calculate_summary(enterprise_id)

        # 获取或创建报告
        report = await self.get_by_enterprise(enterprise_id)
        if not report:
            report = await self.model.create(enterprise_id=enterprise_id)

        # 更新报告数据
        report.total_score = Decimal(str(summary["total_score"]))
        report.overall_level = summary["overall_level"]
        report.improvement_items = summary["improvement_items"]
        report.limiting_indicators_count = summary["limiting_indicators"]
        report.non_compliant_limiting_count = summary["non_compliant_limiting"]
        report.summary = summary
        report.auditor_id = auditor_id
        report.auditor_name = auditor_name
        report.audit_date = datetime.now().date()
        report.status = "draft"

        await report.save()
        return report

    async def submit_report(self, enterprise_id: int) -> PCBAuditReport:
        """提交审核报告"""
        report = await self.get_by_enterprise(enterprise_id)
        if report:
            report.status = "submitted"
            await report.save()
        return report


# 创建控制器实例
pcb_enterprise_controller = PCBEnterpriseController()
pcb_indicator_controller = PCBIndicatorController()
pcb_audit_result_controller = PCBAuditResultController()
pcb_scheme_controller = PCBSchemeController()
pcb_indicator_scheme_relation_controller = PCBIndicatorSchemeRelationController()
pcb_pre_audit_data_controller = PCBPreAuditDataController()
pcb_enterprise_scheme_controller = PCBEnterpriseSchemeController()
pcb_audit_report_controller = PCBAuditReportController()



