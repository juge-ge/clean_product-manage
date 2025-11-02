# PCB评分机制完整实现报告

## 实现日期
2025年1月

## 实现内容概述

完整实现了PCB行业清洁生产审核的综合评价指数计算机制，包括：
1. **指标权重调整**（动态权重计算）
2. **隶属函数计算**（公式5-1）
3. **综合评价指数计算**（公式5-2）
4. **权重调整**（公式5-3）
5. **清洁生产水平判定**（依据表4规则）
6. **前端UI展示**（显示YⅠ、YⅡ、YⅢ和判定结果）

## 核心算法实现

### 1. 公式5-1：隶属函数

```python
def calculate_membership_function(level: str, target_level: str) -> int:
    """
    公式5-1: 计算隶属函数 Ygk(xij)
    如果指标xij属于级别gk，返回100，否则返回0
    """
    if level == target_level:
        return 100
    return 0
```

### 2. 公式5-2：综合评价指数

```python
def calculate_comprehensive_evaluation_index(
    indicators: List[Dict],
    target_level: str,
    product_outputs: Optional[Dict[int, float]] = None
) -> Decimal:
    """
    公式5-2: 计算综合评价指数 Ygk
    
    Ygk = Σ(wi * Σ(wij * Ygk(xij)))
    
    其中：
    - wi: 一级指标权重
    - wij: 二级指标权重（可能是动态权重）
    - Ygk(xij): 隶属函数值
    """
    # 按一级指标分组
    # 遍历每个一级指标
    #   计算该一级指标下二级指标的加权得分
    #   一级指标权重 × 二级指标加权得分
    # 返回总分
```

### 3. 公式5-3：权重调整

```python
def calculate_adjusted_weight(
    original_weight: Decimal,
    total_weight_sum: Decimal
) -> Decimal:
    """
    公式5-3: 计算调整后的二级指标权重
    
    wij' = wij / Σwij
    
    当某些二级指标不适用时，需要重新归一化权重
    """
    if total_weight_sum == 0:
        return Decimal("0")
    return original_weight / total_weight_sum
```

### 4. 动态权重计算公式

```python
def calculate_dynamic_weight(
    indicator_id: int,
    base_weight: Decimal,  # 原二级指标权重
    all_indicators: List[Dict],
    product_outputs: Dict[int, float]
) -> Decimal:
    """
    动态权重计算
    
    公式：某类产品权重 =（该类产品产量 / 总产量）× 原二级指标权重 × 对应一级指标权重
    
    示例：
    - 单面板产量：500 m²
    - 双面板产量：1000 m²
    - 总产量：1500 m²
    - 原二级指标权重：1.0
    - 一级指标权重：0.1
    
    单面板权重 = (500/1500) × 1.0 × 0.1 = 0.0333...
    双面板权重 = (1000/1500) × 1.0 × 0.1 = 0.0666...
    """
    output_ratio = current_output / group_total_output
    actual_weight = output_ratio * base_weight * category_weight
    return actual_weight
```

### 5. 清洁生产水平判定（表4规则）

```python
def determine_clean_production_level(
    y1: Decimal,  # YⅠ
    y2: Decimal,  # YⅡ
    y3: Decimal,  # YⅢ
    limiting_indicators_level: List[str],
    all_indicators_level: Optional[List[Dict]] = None
) -> str:
    """
    根据表4的判定规则判定清洁生产水平
    
    Ⅰ级：清洁生产先进（标杆）水平
    - 同时满足：
      1. YⅠ ≥ 85
      2. 限定性指标全部满足Ⅰ级基准值要求
      3. 非限定性指标全部满足Ⅱ级基准值要求
    
    Ⅱ级：清洁生产准入水平
    - 同时满足：
      1. YⅡ ≥ 85
      2. 限定性指标全部满足Ⅱ级基准值要求及以上
    
    Ⅲ级：清洁生产一般水平
    - 满足：YⅢ = 100
    """
```

## 动态权重组配置

根据需求，以下指标组的权重需要根据产量动态计算：

| 指标范围 | 权重总和 | 一级权重 | 说明 |
|---------|---------|---------|------|
| 7-14 | 1.0 | 0.1 | 能源消耗 - 单位产品电耗 |
| 15-18 | 0.5 | 0.1 | 水资源消耗 - 单位产品新鲜水耗 |
| 20-27 | 1.0 | 0.1 | 原/辅料消耗 - 覆铜板利用率 |
| 30-33 | 0.2 | 0.2 | 污染物产生与排放 - 废水产生量 |
| 34-37 | 0.1 | 0.2 | 污染物产生与排放 - 废水中铜产生量 |
| 38-41 | 0.1 | 0.2 | 污染物产生与排放 - 废水中COD总产生量（双星号**） |

## 前端UI展示

### 汇总统计卡片
- **YⅠ (Ⅰ级指数)**：显示Ⅰ级综合评价指数，≥85显示"达标"标签
- **YⅡ (Ⅱ级指数)**：显示Ⅱ级综合评价指数，≥85显示"达标"标签
- **YⅢ (Ⅲ级指数)**：显示Ⅲ级综合评价指数，=100显示"达标"标签
- **清洁生产水平**：显示最终判定的级别（Ⅰ级、Ⅱ级、Ⅲ级、不达标）
- **待改进项数**：统计未达到Ⅰ级的指标数量
- **限定性指标**：统计限定性指标总数

### 进度图表
- 圆形进度条显示YⅠ指数
- 图例说明判定规则

### 产量输入
- 指标7-14、15-18、20-27、30-33、34-37、38-41：可编辑输入框
- 其他指标：只读显示或空白
- 用户输入产量后，自动重新计算动态权重和综合评价指数

## 数据流

### 完整计算流程：
```
1. 用户输入产量（指标7-41中指定范围）
   ↓
2. 前端收集用户输入的产量
   ↓
3. 调用后端API，传递产量数据
   ↓
4. 后端获取产品产量数据（从生产信息模块）
   ↓
5. 合并用户输入和产品数据（用户输入优先）
   ↓
6. 计算动态权重（根据产量分配权重）
   ↓
7. 计算隶属函数（公式5-1）
   ↓
8. 计算综合评价指数（公式5-2）
   - 计算YⅠ（针对Ⅰ级）
   - 计算YⅡ（针对Ⅱ级）
   - 计算YⅢ（针对Ⅲ级）
   ↓
9. 判定清洁生产水平（表4规则）
   ↓
10. 返回结果到前端显示
```

## 关键技术要点

### 1. 动态权重计算逻辑

```python
# 计算某类产品的权重占比
output_ratio = current_output / group_total_output

# 应用公式：某类产品权重 =（该类产品产量 / 总产量）× 原二级指标权重 × 对应一级指标权重
actual_weight = output_ratio * base_weight * category_weight
```

### 2. 权重归一化

当某些指标不适用时，使用公式5-3进行权重调整：
```python
adjusted_weight = original_weight / total_applicable_weight
```

### 3. 综合评价指数聚合

逐层收敛的计算方式：
```python
# 一级指标下二级指标加权得分
category_score = Σ(wij * Ygk(xij))

# 总综合评价指数
total_score = Σ(wi * category_score)
```

## API接口

### 获取审核汇总
```
GET /api/v1/pcb/enterprise/{enterprise_id}/audit/summary?user_input_outputs={JSON}
```

**参数说明**：
- `enterprise_id`: 企业ID
- `user_input_outputs`: 可选，用户输入的产量数据（JSON字符串，如：`{"7": 500, "8": 1000}`）

**响应格式**：
```json
{
  "code": 200,
  "data": {
    "y1": 85.5,
    "y2": 78.3,
    "y3": 60.0,
    "total_score": 85.5,
    "overall_level": "I级",
    "improvement_items": 5,
    "limiting_indicators": 3,
    "evaluation_details": {
      "y1": 85.5,
      "y2": 78.3,
      "y3": 60.0,
      "meet_level1_conditions": true,
      "meet_level2_conditions": false,
      "meet_level3_conditions": false
    }
  }
}
```

### 批量更新审核结果
```
POST /api/v1/pcb/enterprise/{enterprise_id}/audit/batch
```

**请求体**：
```json
{
  "indicators": [...],
  "user_input_outputs": {
    "7": 500,
    "8": 1000,
    ...
  },
  "auditor_name": "当前用户",
  "audit_date": "2025-01-01"
}
```

## 代码结构

### 后端模块
- `app/utils/pcb_score_calculator.py`: 评分计算工具模块
  - `calculate_membership_function()`: 隶属函数计算
  - `calculate_comprehensive_evaluation_index()`: 综合评价指数计算
  - `calculate_adjusted_weight()`: 权重调整
  - `calculate_dynamic_weight()`: 动态权重计算
  - `determine_clean_production_level()`: 清洁生产水平判定

- `app/controllers/pcb.py`: 控制器
  - `PCBAuditResultController.calculate_summary()`: 计算汇总数据

- `app/api/v1/pcb.py`: API路由
  - `GET /audit/summary`: 获取审核汇总（支持用户输入产量）
  - `POST /audit/batch`: 批量更新审核结果（包含用户输入产量）

### 前端组件
- `web/src/views/cloud-audit/pcb/enterprise-detail/audit.vue`:
  - 产量输入列（可编辑/只读）
  - 动态权重实时计算
  - YⅠ、YⅡ、YⅢ指数显示
  - 清洁生产水平判定显示

## 验证清单

- [x] 隶属函数计算正确（公式5-1）
- [x] 综合评价指数计算正确（公式5-2）
- [x] 权重调整逻辑正确（公式5-3）
- [x] 动态权重计算公式正确（使用原二级指标权重）
- [x] 清洁生产水平判定符合表4规则
- [x] 前端UI显示YⅠ、YⅡ、YⅢ指数
- [x] 前端UI显示清洁生产水平判定
- [x] 用户输入产量后实时更新计算
- [x] 产量输入范围正确（7-14, 15-18, 20-27, 30-33, 34-37, 38-41）
- [x] 其他指标产量列只读显示

## 注意事项

1. **动态权重计算**：
   - 使用原二级指标权重（base_weight），不是权重总和
   - 公式：`（产量占比）× 原二级指标权重 × 一级指标权重`

2. **权重归一化**：
   - 当某些指标不适用时，自动进行权重调整
   - 确保适用指标的权重总和为1

3. **用户输入产量**：
   - 优先使用用户输入的产量
   - 如果没有用户输入，使用产品产量数据
   - 都没有时使用原始权重

4. **清洁生产水平判定**：
   - 严格按表4规则判定
   - Ⅰ级需要同时满足多个条件
   - Ⅲ级要求YⅢ = 100（精确相等）

## 总结

✅ 所有核心算法已实现  
✅ 动态权重计算公式正确  
✅ 综合评价指数计算准确  
✅ 清洁生产水平判定符合标准  
✅ 前端UI完整展示计算结果  
✅ 用户输入产量功能正常  
✅ 实时计算和更新机制完善  

系统现在能够完整实现PCB行业清洁生产审核的综合评价指数计算和判定机制。


