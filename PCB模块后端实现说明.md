# PCB行业清洁生产审核模块后端实现说明

## 📋 概述

本文档说明PCB行业清洁生产审核模块的后端数据库和API实现情况。

## 🗄️ 数据库设计

### 核心表结构（8张表）

已严格按照《PCB审核模块数据库与交互设计方案.md》创建以下8张核心表：

#### 1. `pcb_enterprise` - 企业基本信息表
- **字段**: 企业名称、地区、联系信息、产能、审核状态等
- **功能**: 存储PCB企业的基本信息和审核进度

#### 2. `pcb_indicator` - 审核指标表
- **字段**: 指标编号(1-64)、名称、类别、类型、单位、权重、评级标准等
- **功能**: 定义64项PCB清洁生产审核指标

#### 3. `pcb_audit_result` - 审核结果表
- **字段**: 企业ID、指标ID、当前值、评级、得分、审核意见等
- **功能**: 存储每个企业每个指标的审核结果
- **约束**: (enterprise_id, indicator_id) 唯一

#### 4. `pcb_scheme` - 清洁生产方案表
- **字段**: 方案编号(1-130)、名称、类型、问题描述、实施方案、经济效益、环境效益等
- **功能**: 存储130项清洁生产改进方案

#### 5. `pcb_indicator_scheme_relation` - 指标方案关联表
- **字段**: 指标ID、方案ID、关联度
- **功能**: 建立指标与方案的多对多关联关系
- **约束**: (indicator_id, scheme_id) 唯一

#### 6. `pcb_enterprise_scheme` - 企业方案记录表
- **字段**: 企业ID、方案ID、指标ID、状态、实施计划、实际效果等
- **功能**: 记录企业选择和实施方案的情况

#### 7. `pcb_pre_audit_data` - 预审核数据表
- **字段**: 企业ID、生产信息、原辅材料、工艺装备、资源消耗等（JSON格式）
- **功能**: 存储预审核阶段企业填报的详细数据

#### 8. `pcb_audit_report` - 审核报告表
- **字段**: 企业ID、总分、综合等级、改进项数、限定性指标统计等
- **功能**: 生成和存储企业审核报告

## 🔌 API接口设计

### 基础路径
所有PCB模块API的基础路径为: `/api/v1/pcb`

### 接口分类

#### 1. 企业管理接口
- `GET /api/v1/pcb/enterprise` - 获取企业列表（支持搜索、筛选、分页）
- `POST /api/v1/pcb/enterprise` - 创建企业
- `GET /api/v1/pcb/enterprise/{id}` - 获取企业详情
- `PUT /api/v1/pcb/enterprise/{id}` - 更新企业信息
- `DELETE /api/v1/pcb/enterprise/{id}` - 删除企业（软删除）

#### 2. 指标管理接口
- `GET /api/v1/pcb/indicator` - 获取指标列表
- `GET /api/v1/pcb/indicator/tree` - 获取指标树形结构
- `GET /api/v1/pcb/indicator/limiting` - 获取限定性指标
- `GET /api/v1/pcb/indicator/{indicator_id}` - 获取指标详情
- `POST /api/v1/pcb/indicator` - 创建指标
- `PUT /api/v1/pcb/indicator/{indicator_id}` - 更新指标

#### 3. 预审核数据接口
- `GET /api/v1/pcb/enterprise/{id}/pre-audit` - 获取预审核数据
- `POST /api/v1/pcb/enterprise/{id}/pre-audit` - 保存预审核数据
- `POST /api/v1/pcb/enterprise/{id}/pre-audit/submit` - 提交预审核数据

#### 4. 审核结果接口
- `GET /api/v1/pcb/enterprise/{id}/audit` - 获取审核结果（包含所有64项指标）
- `PUT /api/v1/pcb/enterprise/{id}/audit/indicator/{indicator_id}` - 更新单个指标审核结果
- `POST /api/v1/pcb/enterprise/{id}/audit/batch` - 批量更新审核结果
- `GET /api/v1/pcb/enterprise/{id}/audit/summary` - 获取审核汇总
- `POST /api/v1/pcb/enterprise/{id}/audit/auto-calculate` - 自动计算审核结果

#### 5. 方案库接口
- `GET /api/v1/pcb/scheme` - 获取方案列表（支持搜索、筛选、分页）
- `GET /api/v1/pcb/scheme/{scheme_id}` - 获取方案详情
- `POST /api/v1/pcb/scheme` - 创建方案
- `PUT /api/v1/pcb/scheme/{scheme_id}` - 更新方案
- `DELETE /api/v1/pcb/scheme/{scheme_id}` - 删除方案
- `GET /api/v1/pcb/indicator/{indicator_id}/schemes` - 获取指标关联方案
- `GET /api/v1/pcb/enterprise/{id}/audit/schemes/{indicator_id}` - 获取企业指标推荐方案

#### 6. 指标方案关联接口
- `POST /api/v1/pcb/indicator-scheme-relation` - 创建指标方案关联
- `POST /api/v1/pcb/indicator-scheme-relation/batch` - 批量创建关联

#### 7. 企业方案管理接口
- `GET /api/v1/pcb/enterprise/{id}/scheme` - 获取企业选择的方案
- `POST /api/v1/pcb/enterprise/{id}/scheme` - 企业选择方案
- `PUT /api/v1/pcb/enterprise/{id}/scheme/{scheme_id}` - 更新企业方案状态

#### 8. 审核报告接口
- `GET /api/v1/pcb/enterprise/{id}/report` - 获取审核报告
- `POST /api/v1/pcb/enterprise/{id}/report/generate` - 生成审核报告
- `POST /api/v1/pcb/enterprise/{id}/report/submit` - 提交审核报告

## 📁 文件结构

```
app/
├── models/
│   ├── __init__.py          # 已添加 PCB 模型导入
│   └── pcb.py              # ✅ 新增：PCB 数据模型（8个核心表）
├── schemas/
│   └── pcb.py              # ✅ 新增：PCB Pydantic Schema
├── controllers/
│   └── pcb.py              # ✅ 新增：PCB 业务逻辑控制器
└── api/v1/
    ├── __init__.py         # 已添加 PCB 路由注册
    └── pcb.py              # ✅ 新增：PCB RESTful API 路由

migrations/
└── init_pcb_data.py        # ✅ 新增：数据初始化脚本
```

## 🔧 核心功能实现

### 1. 前后端解耦
- ✅ 所有数据交互通过 RESTful API 完成
- ✅ 前端通过 HTTP 请求调用后端接口
- ✅ 使用 Pydantic 进行严格的数据验证

### 2. CRUD 完整实现
- ✅ 企业信息：增删改查
- ✅ 审核指标：增删改查
- ✅ 审核结果：增删改查
- ✅ 方案库：增删改查
- ✅ 预审核数据：增删改查

### 3. 业务逻辑
- ✅ 审核结果自动计算（根据评级计算分数）
- ✅ 审核汇总统计（总分、等级、改进项、限定性指标）
- ✅ 方案自动推荐（根据指标评级推荐相关方案）
- ✅ 指标与方案关联管理
- ✅ 报告自动生成

### 4. 数据验证
- ✅ 使用 Pydantic Schema 进行请求数据验证
- ✅ 唯一性约束（指标ID、方案ID、企业-指标组合等）
- ✅ 外键关联验证

## 🚀 部署步骤

### 1. 数据库迁移
```bash
# 系统会自动创建表结构（Tortoise ORM）
# 首次运行应用时会自动生成数据库表
```

### 2. 初始化基础数据
```bash
# 运行数据初始化脚本
python migrations/init_pcb_data.py
```

这将初始化：
- 64项审核指标
- 130项清洁生产方案（需要补充完整数据）
- 指标与方案的关联关系

### 3. 启动应用
```bash
# 启动 FastAPI 应用
python run.py
```

### 4. API文档访问
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📊 数据初始化说明

### 已完成
- ✅ 64项指标的完整定义
- ✅ 指标分类、类型、权重配置
- ✅ 定量指标的评级标准
- ✅ 限定性指标标记

### 需要补充
- ⚠️ 130项方案的完整数据（当前仅包含2个示例）
- ⚠️ 指标与方案的完整关联关系

### 数据补充方式
1. 从《PCB 清洁生产方案.md》文件中提取130项方案数据
2. 更新 `migrations/init_pcb_data.py` 中的 `SCHEMES_DATA_SAMPLE` 变量
3. 建立指标编号与方案编号的关联关系表
4. 重新运行数据初始化脚本

## 🔐 权限控制

所有PCB模块的API接口已集成权限验证：
```python
v1_router.include_router(pcb_router, prefix="/pcb", dependencies=[DependPermission])
```

用户需要登录并拥有相应权限才能访问这些接口。

## 📝 API调用示例

### 创建企业
```http
POST /api/v1/pcb/enterprise
Content-Type: application/json

{
  "name": "深圳某某电路板有限公司",
  "region": "深圳市",
  "district": "宝安区",
  "contact_person": "张三",
  "contact_phone": "13800138000",
  "capacity": 120.50
}
```

### 获取企业审核结果
```http
GET /api/v1/pcb/enterprise/1/audit
```

### 更新指标审核结果
```http
PUT /api/v1/pcb/enterprise/1/audit/indicator/7
Content-Type: application/json

{
  "current_value": 115.5,
  "level": "II级",
  "score": 80,
  "comment": "电耗符合II级标准"
}
```

### 获取推荐方案
```http
GET /api/v1/pcb/enterprise/1/audit/schemes/30
```

## ⚡ 性能优化

已实现的优化：
- ✅ 数据库索引（企业ID、指标ID、审核状态等）
- ✅ 分页查询（企业列表、方案列表）
- ✅ 软删除机制（避免物理删除）
- ✅ 批量操作接口（批量更新审核结果）

## 🔍 测试建议

### 功能测试
1. 测试企业的CRUD操作
2. 测试审核流程：预审核 → 审核 → 报告生成
3. 测试方案推荐逻辑
4. 测试审核汇总计算

### 数据一致性测试
1. 测试指标与审核结果的关联
2. 测试方案与指标的关联
3. 测试软删除机制

## 📖 相关文档

- 《PCB审核模块数据库与交互设计方案.md》 - 数据库设计规范
- 《PCB具体内容技术方案.md》 - 前端技术方案
- 《PCB 清洁生产方案.md》 - 130项方案详细内容

## ✅ 实现清单

- [x] 创建8个核心数据表
- [x] 实现 Pydantic Schema 数据验证
- [x] 实现 CRUD 控制器
- [x] 实现 RESTful API 接口
- [x] 实现审核逻辑和汇总计算
- [x] 实现方案推荐逻辑
- [x] 集成权限验证
- [x] 创建数据初始化脚本
- [x] 64项指标数据初始化
- [ ] 130项方案数据补充（需要手动补充）

## 🎯 后续工作

1. **补充130项方案完整数据**
   - 从《PCB 清洁生产方案.md》提取数据
   - 更新初始化脚本

2. **前端集成**
   - 前端调用API实现界面交互
   - 实现表单提交和数据展示

3. **功能增强**
   - 实现审核流程控制
   - 添加数据导出功能
   - 实现报告PDF生成

4. **性能优化**
   - 添加缓存机制
   - 优化复杂查询
   - 实现异步任务处理

---

**实现时间**: 2025年
**技术栈**: FastAPI + Tortoise ORM + Pydantic + SQLite
**状态**: ✅ 核心功能已完成，可开始前端集成



