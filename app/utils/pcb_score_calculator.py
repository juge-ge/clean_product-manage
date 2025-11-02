"""
PCB清洁生产综合评价指数计算工具
实现公式5-1, 5-2, 5-3的评分机制

公式说明：
5-1: 隶属函数 Ygk(xij) = { 100, 若指标xij属于级别gk; 0, 否则 }
5-2: 综合评价指数 Ygk = Σ(wi * Σ(wij * Ygk(xij)))
5-3: 调整后的二级指标权重 wij' = wij / Σwij

权重调整公式（动态权重）：
某类产品权重 =（该类产品产量 / 总产量）× 原二级指标权重 × 对应一级指标权重
"""
from typing import Dict, List, Optional
from decimal import Decimal
from collections import defaultdict


def calculate_membership_function(level: str, target_level: str) -> int:
    """
    公式5-1: 计算隶属函数 Ygk(xij)
    
    评级是层次性的：I级 > II级 > III级 > 不达标
    - 符合I级的必然符合II级和III级
    - 符合II级的必然符合III级
    
    参数:
        level: 指标的实际评级 (I级, II级, III级, 不达标)
        target_level: 目标级别 (I级, II级, III级)
    
    返回:
        - 计算YⅠ：只有I级返回100，其他返回0
        - 计算YⅡ：I级和II级返回100，其他返回0
        - 计算YⅢ：I级、II级、III级返回100，只有不达标返回0
    """
    if not level or level == '待评估' or level == '不达标':
        # 不达标在任何级别都返回0
        if level == '不达标':
            return 0
        # 待评估或空值返回0
        return 0
    
    # 定义评级层次：数字越大，等级越低
    level_hierarchy = {
        'I级': 1,
        'II级': 2,
        'III级': 3,
        '不达标': 4
    }
    
    target_hierarchy = {
        'I级': 1,
        'II级': 2,
        'III级': 3
    }
    
    # 获取实际评级和目标级别的层次值
    actual_rank = level_hierarchy.get(level, 4)
    target_rank = target_hierarchy.get(target_level, 4)
    
    # 如果实际评级小于等于目标级别（即等级更高或相等），返回100
    # 例如：I级(1) <= II级目标(2)，返回100
    if actual_rank <= target_rank:
        return 100
    
    return 0


def calculate_adjusted_weight(
    original_weight: Decimal,
    total_weight_sum: Decimal
) -> Decimal:
    """
    公式5-3: 计算调整后的二级指标权重
    
    参数:
        original_weight: 原始权重
        total_weight_sum: 参与考核的指标权重之和
    
    返回:
        调整后的权重
    """
    if total_weight_sum == 0:
        return Decimal("0")
    return original_weight / total_weight_sum


def calculate_comprehensive_evaluation_index(
    indicators: List[Dict],
    target_level: str,
    product_outputs: Optional[Dict] = None
) -> Decimal:
    """
    公式5-2: 计算综合评价指数 Ygk
    
    参数:
        indicators: 指标列表，每个指标包含:
            - indicator_id: 指标ID
            - category: 一级指标名称
            - category_weight: 一级指标权重
            - weight: 二级指标权重（原始）
            - is_dynamic_weight: 是否动态权重
            - level: 指标评级
        target_level: 目标级别 (I级, II级, III级)
        product_outputs: 产品产量数据，格式: {indicator_id: output_value}
    
    返回:
        综合评价指数得分
    """
    # 按一级指标分组
    category_groups = defaultdict(list)
    for indicator in indicators:
        category = indicator.get('category', '')
        category_groups[category].append(indicator)
    
    total_score = Decimal("0")
    
    # 遍历每个一级指标
    for category, category_indicators in category_groups.items():
        # 获取一级指标权重
        category_weight = Decimal("0")
        if category_indicators:
            category_weight = Decimal(str(category_indicators[0].get('category_weight', 0)))
        
        # 计算该一级指标下二级指标的加权得分
        category_score = Decimal("0")
        applicable_weights = []  # 适用于企业的指标权重
        
        for indicator in category_indicators:
            level = indicator.get('level')
            # 如果评级为空或待评估，跳过
            if not level or level == '待评估':
                continue
            
            # 获取原始权重
            original_weight = Decimal(str(indicator.get('weight', 0)))
            is_dynamic = indicator.get('is_dynamic_weight', False)
            indicator_id = indicator.get('indicator_id') or indicator.get('id')
            
            # 如果是动态权重，需要根据产量计算实际权重
            if is_dynamic and product_outputs:
                actual_weight = calculate_dynamic_weight(
                    indicator_id, original_weight, indicators, product_outputs
                )
            else:
                actual_weight = original_weight
            
            # 计算隶属函数值
            membership_value = calculate_membership_function(level, target_level)
            
            # 累加得分
            category_score += actual_weight * Decimal(str(membership_value))
            
            # 记录适用的权重（用于后续调整）
            applicable_weights.append(actual_weight)
        
        # 公式5-3: 如果有些指标不适用，需要调整权重
        total_applicable_weight = sum(applicable_weights)
        if total_applicable_weight > 0:
            # 重新归一化权重
            normalized_category_score = Decimal("0")
            weight_sum = Decimal("0")
            
            for indicator in category_indicators:
                level = indicator.get('level')
                if not level or level == '待评估':
                    continue
                
                original_weight = Decimal(str(indicator.get('weight', 0)))
                is_dynamic = indicator.get('is_dynamic_weight', False)
                indicator_id = indicator.get('indicator_id') or indicator.get('id')
                
                if is_dynamic and product_outputs:
                    actual_weight = calculate_dynamic_weight(
                        indicator_id, original_weight, indicators, product_outputs
                    )
                else:
                    actual_weight = original_weight
                
                # 调整后的权重
                adjusted_weight = calculate_adjusted_weight(actual_weight, total_applicable_weight)
                membership_value = calculate_membership_function(level, target_level)
                
                normalized_category_score += adjusted_weight * Decimal(str(membership_value))
                weight_sum += adjusted_weight
            
            category_score = normalized_category_score
        
        # 一级指标权重 × 二级指标加权得分
        total_score += category_weight * category_score
    
    return total_score


def calculate_dynamic_weight(
    indicator_id: int,
    base_weight: Decimal,
    all_indicators: List[Dict],
    product_outputs: Dict[int, float]
) -> Decimal:
    """
    根据产量计算动态权重
    
    参数:
        indicator_id: 当前指标ID
        base_weight: 基础权重（来自数据库）
        all_indicators: 所有指标（用于查找同组的指标）
        product_outputs: 产量数据 {indicator_id: output_value}
    
    返回:
        计算后的实际权重
    """
    # 动态权重分组配置
    # 格式: (指标ID范围, 一级权重)
    # 注意：每个组的二级权重总和为1，按产量比例分配
    dynamic_groups = [
        ((7, 14), Decimal("0.1")),      # 能源消耗
        ((15, 18), Decimal("0.1")),      # 水资源消耗
        ((20, 27), Decimal("0.1")),      # 原/辅料消耗
        ((30, 33), Decimal("0.1")),      # 废水产生量（一级权重已从0.2改为0.1）
        ((34, 37), Decimal("0.1")),      # 废水中铜产生量（一级权重已从0.2改为0.1）
        ((38, 41), Decimal("0.1")),      # 废水中COD总产生量（一级权重已从0.2改为0.1）
    ]
    
    # 找到当前指标所属的组
    current_group = None
    for (start_id, end_id), category_weight in dynamic_groups:
        if start_id <= indicator_id <= end_id:
            current_group = {
                'start_id': start_id,
                'end_id': end_id,
                'category_weight': category_weight
            }
            break
    
    if not current_group:
        # 如果不是动态权重组，返回原始权重
        return base_weight
    
    # 计算该组内所有指标的总产量（只计算有产量数据的指标）
    group_total_output = Decimal("0")
    group_indicator_outputs = {}  # 存储该组内每个指标的产量
    
    for indicator in all_indicators:
        ind_id = indicator.get('indicator_id') or indicator.get('id')
        if ind_id and current_group['start_id'] <= ind_id <= current_group['end_id']:
            output = product_outputs.get(ind_id, 0)
            if output and output > 0:
                output_decimal = Decimal(str(output))
                group_indicator_outputs[ind_id] = output_decimal
                group_total_output += output_decimal
    
    # 如果没有产量数据，返回原始权重
    if group_total_output == 0:
        return base_weight
    
    # 计算当前指标的产量
    current_output = Decimal(str(product_outputs.get(indicator_id, 0)))
    if current_output == 0:
        return Decimal("0")
    
    # 计算权重占比
    # 公式：某类产品权重 =（该类产品产量 / 总产量）× 该组二级权重总和（1.0）
    # 例如：单面板产量500，总产量1500
    # 单面板权重 = (500/1500) * 1.0 = 0.333...
    output_ratio = current_output / group_total_output
    # 该组二级权重总和为1，按产量比例分配
    actual_weight = output_ratio * Decimal("1.0")
    
    return actual_weight


def determine_clean_production_level(
    y1: Decimal,  # YⅠ
    y2: Decimal,  # YⅡ
    y3: Decimal,  # YⅢ
    limiting_indicators_level: List[str],  # 限定性指标的评级列表
    all_indicators_level: Optional[List[Dict]] = None  # 所有指标的评级信息（用于检查非限定性指标）
) -> str:
    """
    根据综合评价指数判定清洁生产水平（依据表4的判定规则）
    
    参数:
        y1: YⅠ得分
        y2: YⅡ得分
        y3: YⅢ得分
        limiting_indicators_level: 限定性指标的评级列表
        all_indicators_level: 所有指标的评级信息 [{'indicator_id': int, 'level': str, 'is_limiting': bool}, ...]
    
    返回:
        清洁生产水平: I级, II级, III级, 不达标
    """
    # Ⅰ级：清洁生产先进（标杆）水平
    # 同时满足：
    # 1. YⅠ ≥ 85
    # 2. 限定性指标全部满足Ⅰ级基准值要求
    # 3. 非限定性指标全部满足Ⅱ级基准值要求
    if y1 >= Decimal("85"):
        # 检查限定性指标是否全部为I级
        limiting_meet_i = all(
            level == 'I级' for level in limiting_indicators_level
        ) if limiting_indicators_level else True
        
        # 检查非限定性指标是否全部达到II级或以上
        non_limiting_meet_ii = True
        if all_indicators_level:
            non_limiting = [ind for ind in all_indicators_level if not ind.get('is_limiting', False)]
            non_limiting_meet_ii = all(
                ind.get('level') in ['I级', 'II级'] for ind in non_limiting if ind.get('level')
            )
        
        if limiting_meet_i and non_limiting_meet_ii:
            return "I级"
    
    # Ⅱ级：清洁生产准入水平
    # 同时满足：
    # 1. YⅡ ≥ 85
    # 2. 限定性指标全部满足Ⅱ级基准值要求及以上
    if y2 >= Decimal("85"):
        limiting_meet_ii = all(
            level in ['I级', 'II级'] for level in limiting_indicators_level
        ) if limiting_indicators_level else True
        
        if limiting_meet_ii:
            return "II级"
    
    # Ⅲ级：清洁生产一般水平
    # 满足：YⅢ = 100
    if y3 == Decimal("100"):
        return "III级"
    
    # 未达标
    return "不达标"

