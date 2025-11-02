# PCB审核模块修改完成报告

## 修改日期
2025年1月

## 修改内容概述

根据新的需求，对PCB审核模块进行了以下修改：

1. **移除推荐方案功能**
2. **新增一级指标权重显示**（从数据库读取`category_weight`）
3. **保留二级指标权重显示**（从数据库读取`weight`）
4. **保留评级功能**（枚举：Ⅰ级、Ⅱ级、Ⅲ级）

## 详细修改内容

### 1. 后端API修改

#### 文件：`app/api/v1/pcb.py`

**修改点1：获取审核结果API**
- **位置**：`GET /api/v1/pcb/enterprise/{enterprise_id}/audit`
- **修改**：移除了推荐方案的获取和返回
- **代码变更**：
```python
# 修改前
recommended_schemes = await pcb_audit_result_controller.get_indicator_recommended_schemes(...)
result_dict["recommended_schemes"] = recommended_schemes

# 修改后
# 移除推荐方案 - 不再返回推荐方案数据
# recommended_schemes = await pcb_audit_result_controller.get_indicator_recommended_schemes(...)
# result_dict["recommended_schemes"] = recommended_schemes
```

**修改点2：批量更新审核结果API**
- **位置**：`POST /api/v1/pcb/enterprise/{enterprise_id}/audit/batch`
- **修改**：移除方案选择处理逻辑
- **代码变更**：
```python
# 修改前
selected_schemes = audit_data.get("selected_schemes", [])
if selected_schemes:
    await pcb_enterprise_scheme_controller.save_selected_schemes(...)

# 修改后
# 移除方案选择处理
# selected_schemes = audit_data.get("selected_schemes", [])
# if selected_schemes:
#     await pcb_enterprise_scheme_controller.save_selected_schemes(...)
```

**修改点3：更新单个指标API**
- **位置**：`PUT /api/v1/pcb/enterprise/{enterprise_id}/audit/indicator/{indicator_id}`
- **修改**：不再处理方案选择，传入`None`

### 2. 前端组件修改

#### 文件：`web/src/views/cloud-audit/pcb/enterprise-detail/audit.vue`

**修改点1：表格列定义**
- **移除**：推荐方案列
- **新增**：一级指标权重列
- **修改**：二级指标权重列（显示动态权重标记*）

**列结构变化**：
```javascript
// 修改前
columns = [
  { title: '序号' },
  { title: '一级指标' },
  { title: '二级指标' },
  { title: '当前值' },
  { title: '指标权重' },
  { title: '评级' },
  { title: '推荐方案' }  // 移除
]

// 修改后
columns = [
  { title: '序号' },
  { title: '一级指标' },
  { title: '二级指标' },
  { title: '当前值' },
  { title: '一级指标权重' },  // 新增，从数据库读取category_weight
  { title: '二级指标权重' },  // 修改，从数据库读取weight，动态权重显示*
  { title: '评级' }
]
```

**修改点2：数据获取逻辑**
- 从API响应中读取`category_weight`和`weight`字段
- 读取`is_dynamic_weight`字段用于标记动态权重
- 移除`recommended_schemes`和`selected_schemes`字段的处理

**修改点3：移除推荐方案相关功能**
- 移除推荐方案弹窗组件
- 移除推荐方案获取函数
- 移除方案选择处理函数
- 移除方案详情显示逻辑

**修改点4：提交审核数据**
- 移除`selected_schemes`字段的收集和提交
- 保持API兼容性（后端会忽略该字段）

## 表格列显示说明

### 列顺序
1. **序号** - 指标编号（1-64）
2. **一级指标** - 一级指标名称
3. **二级指标** - 二级指标名称
4. **当前值** - 指标的当前数值（定量指标）
5. **一级指标权重** - 从数据库`category_weight`字段读取，显示为百分比
6. **二级指标权重** - 从数据库`weight`字段读取，显示为百分比，动态权重显示*标记
7. **评级** - 枚举选择：Ⅰ级、Ⅱ级、Ⅲ级、不达标

### 权重显示规则

1. **一级指标权重**：
   - 一级指标行：显示该一级指标下所有二级指标的统一权重
   - 二级指标行：显示对应的一级指标权重
   - 格式：`15.0%`（category_weight * 100）

2. **二级指标权重**：
   - 仅二级指标行显示
   - 格式：`20.0%`（weight * 100）
   - 动态权重显示：`1.0%*`（带*标记）

3. **动态权重说明**：
   - 带`*`标记的权重需要根据企业实际产品产量动态计算
   - 标记来自数据库`is_dynamic_weight`字段

## 数据库字段使用

### 使用的字段
- `category_weight`：一级指标权重（DECIMAL(5,3)）
- `weight`：二级指标权重（DECIMAL(5,3)）
- `is_dynamic_weight`：动态权重标记（BOOLEAN）
- `level`：评级结果（CHAR）

### API响应示例
```json
{
  "code": 200,
  "data": [
    {
      "indicator": {
        "id": 1,
        "indicator_id": 1,
        "name": "基本要求",
        "category": "生产工艺与装备要求",
        "category_weight": 0.15,
        "weight": 0.2,
        "is_dynamic_weight": false,
        "indicator_type": "qualitative",
        ...
      },
      "current_value": null,
      "level": "待评估",
      "score": 0
    }
  ]
}
```

## 兼容性保证

### 后端API兼容性
- ✅ API端点保持不变
- ✅ 请求参数向后兼容（不传`selected_schemes`不影响）
- ✅ 响应格式保持兼容（新字段自动返回）

### 前端兼容性
- ✅ 移除的功能不影响现有审核流程
- ✅ 新字段有默认值，不会导致错误
- ✅ 评级功能完全保留

## 注意事项

1. **权重显示**：
   - 一级指标权重和二级指标权重都从数据库读取
   - 前端显示时乘以100转换为百分比格式
   - 动态权重自动添加*标记

2. **评级选项**：
   - 保持原有枚举：Ⅰ级、Ⅱ级、Ⅲ级、不达标
   - 限定性指标只有：符合（Ⅰ级）、不符合（不达标）

3. **数据提交**：
   - 不再提交方案选择数据
   - 仅提交指标评级和当前值

4. **API兼容性**：
   - 后端仍支持`selected_scheme_ids`参数（可选），但前端不再传递
   - 不影响现有API的正常运行

## 验证清单

- [x] 后端API移除推荐方案返回
- [x] 前端移除推荐方案列
- [x] 前端添加一级指标权重列
- [x] 前端修改二级指标权重列显示
- [x] 确保从数据库读取权重字段
- [x] 移除推荐方案相关函数和组件
- [x] 保持评级功能正常
- [x] 保持API向后兼容

## 总结

✅ 所有修改已完成  
✅ API保持向后兼容  
✅ 权重数据从数据库正确读取  
✅ 推荐方案功能已完全移除  
✅ 评级功能完全保留  

系统现在按照新的需求正常工作：显示序号、一级指标、二级指标、当前值、一级指标权重（从数据库读取）、二级指标权重（从数据库读取）、评级（枚举：Ⅰ级、Ⅱ级、Ⅲ级）。

