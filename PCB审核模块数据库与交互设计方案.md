# PCB行业清洁生产云审核模块 - 数据库与交互设计方案

## 目录

- [1. 方案概述](#1-方案概述)
- [2. 数据库设计](#2-数据库设计)
- [3. 前后端交互设计](#3-前后端交互设计)
- [4. 核心功能实现方案](#4-核心功能实现方案)
- [5. API接口设计](#5-api接口设计)
- [6. 数据流转图](#6-数据流转图)
- [7. 技术实施建议](#7-技术实施建议)

---

## 1. 方案概述

### 1.1 技术架构

```
┌─────────────────────────────────────────────────────────────┐
│                        前端 (Vue 3)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 企业列表 │ 基本信息 │ 预审核 │ 审核 │ 方案库 │ 报告  │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↕ HTTP/JSON                       │
├─────────────────────────────────────────────────────────────┤
│                    后端 API (FastAPI)                        │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Controllers  │  Services  │  Schemas  │  Models     │   │
│  └──────────────────────────────────────────────────────┘   │
│                            ↕ SQLAlchemy ORM                  │
├─────────────────────────────────────────────────────────────┤
│                      数据库 (SQLite)                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ 企业表 │ 指标表 │ 审核结果表 │ 方案库表 │ 关联表   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 设计原则

1. **前后端完全分离**: 前端只负责展示和交互,所有业务逻辑在后端处理
2. **RESTful API设计**: 采用标准的REST API接口规范
3. **关系型数据库**: 使用SQLite存储结构化数据
4. **增量式开发**: 支持逐步完善功能,不影响现有代码

---

## 2. 数据库设计

### 2.1 核心表结构设计

#### 2.1.1 企业基本信息表 (pcb_enterprises)

```sql
CREATE TABLE pcb_enterprises (
    -- 主键
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 基本信息
    name VARCHAR(200) NOT NULL COMMENT '企业名称',
    unified_social_credit_code VARCHAR(50) UNIQUE COMMENT '统一社会信用代码',
    city VARCHAR(100) NOT NULL COMMENT '所属地市',
    county VARCHAR(100) NOT NULL COMMENT '所属县',
    scale VARCHAR(50) COMMENT '规模(大型/中型/小型)',
    
    -- 财务信息
    capital DECIMAL(15,2) COMMENT '注册资本(万元)',
    annual_output DECIMAL(15,2) COMMENT '年产值(万元)',
    annual_sales DECIMAL(15,2) COMMENT '年销售额(万元)',
    
    -- 联系信息
    legal_representative VARCHAR(100) COMMENT '法人代表',
    address TEXT COMMENT '注册地址',
    production_address TEXT COMMENT '生产地址',
    postal_code VARCHAR(10) COMMENT '邮编',
    contact VARCHAR(100) COMMENT '联系人',
    phone VARCHAR(20) COMMENT '联系电话',
    email VARCHAR(100) COMMENT '电子邮箱',
    
    -- 其他信息
    establishment_date DATE COMMENT '建厂时间',
    industry VARCHAR(100) DEFAULT 'PCB制造' COMMENT '所属行业',
    
    -- 审核状态
    audit_status VARCHAR(50) DEFAULT 'pending' COMMENT '审核状态(pending/in-progress/completed)',
    audit_score DECIMAL(5,2) COMMENT '审核总分',
    audit_level VARCHAR(20) COMMENT '审核等级(I级/II级/III级/不达标)',
    
    -- 时间戳
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME COMMENT '软删除时间戳',
    
    -- 索引
    INDEX idx_name (name),
    INDEX idx_city (city),
    INDEX idx_audit_status (audit_status)
);
```

#### 2.1.2 审核指标定义表 (pcb_indicators)

```sql
CREATE TABLE pcb_indicators (
    -- 主键
    id INTEGER PRIMARY KEY COMMENT '指标ID(1-64)',
    
    -- 指标信息
    name VARCHAR(200) NOT NULL COMMENT '指标名称',
    category VARCHAR(100) NOT NULL COMMENT '一级指标分类',
    type VARCHAR(50) NOT NULL COMMENT '指标类型(qualitative/quantitative/limiting)',
    
    -- 指标属性
    unit VARCHAR(20) COMMENT '单位',
    weight DECIMAL(5,2) DEFAULT 1.0 COMMENT '指标权重',
    is_limiting BOOLEAN DEFAULT FALSE COMMENT '是否为限定性指标',
    
    -- 评级标准(JSON格式存储)
    level1_threshold TEXT COMMENT 'I级阈值(JSON)',
    level2_threshold TEXT COMMENT 'II级阈值(JSON)',
    level3_threshold TEXT COMMENT 'III级阈值(JSON)',
    
    -- 说明
    description TEXT COMMENT '指标说明',
    evaluation_method TEXT COMMENT '评价方法',
    
    -- 排序
    sort_order INTEGER COMMENT '排序序号',
    
    -- 时间戳
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_category (category),
    INDEX idx_type (type)
);
```

#### 2.1.3 企业审核结果表 (pcb_audit_results)

```sql
CREATE TABLE pcb_audit_results (
    -- 主键
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 外键
    enterprise_id INTEGER NOT NULL COMMENT '企业ID',
    indicator_id INTEGER NOT NULL COMMENT '指标ID',
    
    -- 审核数据
    current_value DECIMAL(15,4) COMMENT '当前值',
    level VARCHAR(20) COMMENT '评级(I级/II级/III级/不达标)',
    score DECIMAL(5,2) COMMENT '得分',
    
    -- 审核备注
    remark TEXT COMMENT '备注说明',
    auditor_name VARCHAR(100) COMMENT '审核人',
    audit_date DATE COMMENT '审核日期',
    
    -- 时间戳
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (enterprise_id) REFERENCES pcb_enterprises(id) ON DELETE CASCADE,
    FOREIGN KEY (indicator_id) REFERENCES pcb_indicators(id),
    
    -- 索引
    UNIQUE INDEX idx_enterprise_indicator (enterprise_id, indicator_id),
    INDEX idx_enterprise (enterprise_id),
    INDEX idx_level (level)
);
```

#### 2.1.4 清洁生产方案库表 (pcb_schemes)

```sql
CREATE TABLE pcb_schemes (
    -- 主键
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 方案基本信息
    scheme_number VARCHAR(50) UNIQUE COMMENT '方案编号',
    name VARCHAR(200) NOT NULL COMMENT '方案名称',
    type VARCHAR(50) COMMENT '方案类型(工艺改进/设备改造/管理优化等)',
    
    -- 方案内容
    problem_solved TEXT COMMENT '解决的问题',
    description TEXT COMMENT '方案简介',
    implementation TEXT COMMENT '实施方案',
    
    -- 效益分析
    economic_benefit TEXT COMMENT '经济效益',
    environmental_benefit TEXT COMMENT '环境效益',
    investment DECIMAL(15,2) COMMENT '投资估算(万元)',
    payback_period DECIMAL(5,2) COMMENT '投资回收期(年)',
    
    -- 状态
    status VARCHAR(20) DEFAULT 'active' COMMENT '状态(active/inactive)',
    
    -- 时间戳
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    deleted_at DATETIME COMMENT '软删除时间戳',
    
    -- 索引
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_name (name)
);
```

#### 2.1.5 指标与方案关联表 (pcb_indicator_scheme_relation)

```sql
CREATE TABLE pcb_indicator_scheme_relation (
    -- 主键
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 外键
    indicator_id INTEGER NOT NULL COMMENT '指标ID',
    scheme_id INTEGER NOT NULL COMMENT '方案ID',
    
    -- 关联属性
    relevance_level VARCHAR(20) DEFAULT 'high' COMMENT '关联度(high/medium/low)',
    priority INTEGER DEFAULT 1 COMMENT '优先级(1-10)',
    
    -- 时间戳
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (indicator_id) REFERENCES pcb_indicators(id) ON DELETE CASCADE,
    FOREIGN KEY (scheme_id) REFERENCES pcb_schemes(id) ON DELETE CASCADE,
    
    -- 索引
    UNIQUE INDEX idx_indicator_scheme (indicator_id, scheme_id),
    INDEX idx_indicator (indicator_id),
    INDEX idx_scheme (scheme_id)
);
```

#### 2.1.6 企业选定方案表 (pcb_enterprise_schemes)

```sql
CREATE TABLE pcb_enterprise_schemes (
    -- 主键
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 外键
    enterprise_id INTEGER NOT NULL COMMENT '企业ID',
    scheme_id INTEGER NOT NULL COMMENT '方案ID',
    indicator_id INTEGER COMMENT '对应的指标ID',
    
    -- 实施信息
    status VARCHAR(50) DEFAULT 'planned' COMMENT '实施状态(planned/in-progress/completed)',
    planned_start_date DATE COMMENT '计划开始日期',
    planned_end_date DATE COMMENT '计划结束日期',
    actual_start_date DATE COMMENT '实际开始日期',
    actual_end_date DATE COMMENT '实际结束日期',
    
    -- 实施效果
    actual_investment DECIMAL(15,2) COMMENT '实际投资(万元)',
    actual_benefit TEXT COMMENT '实际效果描述',
    
    -- 备注
    remark TEXT COMMENT '备注',
    
    -- 时间戳
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (enterprise_id) REFERENCES pcb_enterprises(id) ON DELETE CASCADE,
    FOREIGN KEY (scheme_id) REFERENCES pcb_schemes(id),
    FOREIGN KEY (indicator_id) REFERENCES pcb_indicators(id),
    
    -- 索引
    INDEX idx_enterprise (enterprise_id),
    INDEX idx_status (status)
);
```

#### 2.1.7 预审核数据表 (pcb_pre_audit_data)

```sql
CREATE TABLE pcb_pre_audit_data (
    -- 主键
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 外键
    enterprise_id INTEGER NOT NULL COMMENT '企业ID',
    
    -- 生产情况(JSON格式存储详细数据)
    production_info TEXT COMMENT '企业总体生产情况(JSON)',
    raw_materials TEXT COMMENT '原辅材料使用情况(JSON)',
    process_equipment TEXT COMMENT '主要工艺及装备使用(JSON)',
    
    -- 资源消耗(JSON格式)
    resource_consumption TEXT COMMENT '资源能源消耗(JSON)',
    
    -- 污染防治(JSON格式)
    pollution_control TEXT COMMENT '污染防治(JSON)',
    solid_waste TEXT COMMENT '工业固体废物管理(JSON)',
    self_monitoring TEXT COMMENT '自行监测情况(JSON)',
    
    -- 提交状态
    status VARCHAR(50) DEFAULT 'draft' COMMENT '状态(draft/submitted/approved)',
    submitted_at DATETIME COMMENT '提交时间',
    approved_at DATETIME COMMENT '审批时间',
    
    -- 时间戳
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (enterprise_id) REFERENCES pcb_enterprises(id) ON DELETE CASCADE,
    
    -- 索引
    UNIQUE INDEX idx_enterprise (enterprise_id),
    INDEX idx_status (status)
);
```

#### 2.1.8 审核报告表 (pcb_audit_reports)

```sql
CREATE TABLE pcb_audit_reports (
    -- 主键
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- 外键
    enterprise_id INTEGER NOT NULL COMMENT '企业ID',
    
    -- 报告内容
    report_number VARCHAR(50) UNIQUE COMMENT '报告编号',
    title VARCHAR(200) COMMENT '报告标题',
    content TEXT COMMENT '报告内容(富文本/Markdown)',
    
    -- 报告总结
    summary TEXT COMMENT '审核总结',
    recommendations TEXT COMMENT '改进建议',
    
    -- 评分信息
    total_score DECIMAL(5,2) COMMENT '总分',
    overall_level VARCHAR(20) COMMENT '综合等级',
    
    -- 报告状态
    status VARCHAR(50) DEFAULT 'draft' COMMENT '状态(draft/finalized/published)',
    
    -- 审核人员
    auditor_name VARCHAR(100) COMMENT '主审核员',
    audit_team TEXT COMMENT '审核组成员(JSON)',
    
    -- 日期
    audit_date DATE COMMENT '审核日期',
    report_date DATE COMMENT '报告日期',
    
    -- 时间戳
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- 外键约束
    FOREIGN KEY (enterprise_id) REFERENCES pcb_enterprises(id) ON DELETE CASCADE,
    
    -- 索引
    INDEX idx_enterprise (enterprise_id),
    INDEX idx_status (status),
    INDEX idx_report_number (report_number)
);
```

### 2.2 数据库初始化SQL脚本

```sql
-- 初始化64项指标数据
INSERT INTO pcb_indicators (id, name, category, type, unit, weight, is_limiting, sort_order) VALUES
-- 1-6: 生产工艺与装备要求
(1, '基本要求', '生产工艺与装备要求', 'qualitative', NULL, 1.5, 0, 1),
(2, '机械加工及辅助设施', '生产工艺与装备要求', 'qualitative', NULL, 1.5, 0, 2),
(3, '线路与阻焊图形形成(印刷或感光工艺)', '生产工艺与装备要求', 'qualitative', NULL, 1.5, 0, 3),
(4, '板面清洗', '生产工艺与装备要求', 'qualitative', NULL, 1.5, 0, 4),
(5, '蚀刻', '生产工艺与装备要求', 'qualitative', NULL, 1.5, 0, 5),
(6, '电镀与化学镀', '生产工艺与装备要求', 'qualitative', NULL, 1.5, 0, 6),

-- 7-14: 能源消耗
(7, '刚性印制电路单面板(单位产品电耗)', '能源消耗', 'quantitative', 'kWh/m²', 2.0, 0, 7),
(8, '刚性印制电路双面板(单位产品电耗)', '能源消耗', 'quantitative', 'kWh/m²', 2.0, 0, 8),
(9, '刚性印制电路多层板(2+n)层(单位产品电耗)', '能源消耗', 'quantitative', 'kWh/m²', 2.0, 0, 9),
(10, '刚性印制电路HDI板(2+n)层(单位产品电耗)', '能源消耗', 'quantitative', 'kWh/m²', 2.0, 0, 10),
(11, '挠性印制电路单面板(单位产品电耗)', '能源消耗', 'quantitative', 'kWh/m²', 2.0, 0, 11),
(12, '挠性印制电路双面板(单位产品电耗)', '能源消耗', 'quantitative', 'kWh/m²', 2.0, 0, 12),
(13, '挠性印制电路多层板(2+n)层(单位产品电耗)', '能源消耗', 'quantitative', 'kWh/m²', 2.0, 0, 13),
(14, '挠性印制电路HDI板(2+n)层(单位产品电耗)', '能源消耗', 'quantitative', 'kWh/m²', 2.0, 0, 14),

-- 15-19: 水资源消耗
(15, '单面板(单位产品新鲜水耗)', '水资源消耗', 'quantitative', 'm³/m²', 2.0, 0, 15),
(16, '双面板(单位产品新鲜水耗)', '水资源消耗', 'quantitative', 'm³/m²', 2.0, 0, 16),
(17, '多层板(2+n)层(单位产品新鲜水耗)', '水资源消耗', 'quantitative', 'm³/m²', 2.0, 0, 17),
(18, 'HDI板(2+n)层(单位产品新鲜水耗)', '水资源消耗', 'quantitative', 'm³/m²', 2.0, 0, 18),
(19, '水资源重复利用率', '水资源消耗', 'quantitative', '%', 2.0, 0, 19),

-- ... 其他指标省略(完整的64项)
-- 54-64: 清洁生产管理(含限定性指标)
(54, '*环保法律法规执行情况', '清洁生产管理', 'limiting', NULL, 2.0, 1, 54),
(55, '*产业政策符合性', '清洁生产管理', 'limiting', NULL, 2.0, 1, 55),
(60, '*危险化学品管理', '清洁生产管理', 'limiting', NULL, 2.0, 1, 60),
(62, '*固体废物处理处置', '清洁生产管理', 'limiting', NULL, 2.0, 1, 62);

-- 初始化130项清洁生产方案(来自PCB 清洁生产方案.md)
INSERT INTO pcb_schemes (scheme_number, name, type, problem_solved, description, economic_benefit, environmental_benefit, investment, payback_period) VALUES
('PCB-001', '废水处理系统升级改造', '设备改造', 
 'PCB废水处理系统长期运行导致处理效率下降,设备老化、处理成本高、出水不稳定,同时废水回用率低,处理负荷大。',
 '更换老旧提升泵、潜水泵、电机和搅拌机等设备,改进废水处理工艺采用''二级厌氧+二级好氧''处理系统,在污泥压滤区增设空压机曝气设备降低污泥含水率,更换中水回用系统滤料和渗透膜,完善废气收集系统。',
 '每万平方米线路板节约新鲜水费用0.8万元,减少废水处理成本2.5万元,污泥处置成本降低0.6万元。',
 '每万平方米线路板减少废水排放850吨,COD减排0.09吨,总铜减排0.001吨,污泥减量1.4吨。',
 150.0, 3.5),
 
('PCB-002', '废水分类收集与防泄漏系统改造', '管理优化',
 'PCB生产过程中各类废水收集混乱、跑冒滴漏严重,设施不完善,导致废水处理难度增加,存在环境风险隐患。',
 '对酸碱废水、含铜废水、有机废水分别安装PVC硬管收集系统,在湿法加工区设备下方安装防泄漏托盘并配套应急排水系统,完善地面防腐防渗处理,建立管道标识系统和日常巡检制度。',
 '每万平方米线路板可降低废水处理成本1.2万元,减少原材料流失约0.5万元。',
 '提高废水分质处理效率20%,降低废水站处理负荷25%,减少地面污染风险90%。',
 80.0, 2.5);

-- ... 其他方案数据省略(完整的130项)
```

### 2.3 数据库索引优化

```sql
-- 企业表关键索引
CREATE INDEX idx_enterprises_status_date ON pcb_enterprises(audit_status, created_at DESC);
CREATE INDEX idx_enterprises_city_county ON pcb_enterprises(city, county);

-- 审核结果表复合索引
CREATE INDEX idx_audit_results_composite ON pcb_audit_results(enterprise_id, indicator_id, level);

-- 方案库全文搜索索引(SQLite FTS5)
CREATE VIRTUAL TABLE pcb_schemes_fts USING fts5(
    name, 
    description, 
    content='pcb_schemes', 
    content_rowid='id'
);
```

---

## 3. 前后端交互设计

### 3.1 交互流程图

```
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   前端组件    │         │  API接口层    │         │   数据库层    │
└──────┬───────┘         └──────┬───────┘         └──────┬───────┘
       │                        │                        │
       │  1. 获取企业列表         │                        │
       │───────────────────────>│                        │
       │                        │  查询企业表              │
       │                        │───────────────────────>│
       │                        │<───────────────────────│
       │<───────────────────────│  返回企业数据            │
       │                        │                        │
       │  2. 创建企业            │                        │
       │───────────────────────>│                        │
       │                        │  插入企业记录            │
       │                        │───────────────────────>│
       │                        │<───────────────────────│
       │<───────────────────────│  返回创建结果            │
       │                        │                        │
       │  3. 获取审核指标         │                        │
       │───────────────────────>│                        │
       │                        │  查询指标表              │
       │                        │───────────────────────>│
       │                        │<───────────────────────│
       │<───────────────────────│  返回64项指标            │
       │                        │                        │
       │  4. 提交审核结果         │                        │
       │───────────────────────>│                        │
       │                        │  批量更新审核结果表       │
       │                        │───────────────────────>│
       │                        │  更新企业审核状态         │
       │                        │───────────────────────>│
       │                        │<───────────────────────│
       │<───────────────────────│  返回审核汇总            │
       │                        │                        │
       │  5. 获取推荐方案         │                        │
       │───────────────────────>│                        │
       │                        │  查询指标方案关联表       │
       │                        │───────────────────────>│
       │                        │  查询方案库              │
       │                        │───────────────────────>│
       │                        │<───────────────────────│
       │<───────────────────────│  返回推荐方案列表         │
```

### 3.2 数据交互格式

#### 3.2.1 企业列表数据格式

**请求:**
```http
GET /api/v1/pcb/enterprises?search=深圳&city=深圳市&page=1&page_size=20
```

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "total": 50,
    "page": 1,
    "page_size": 20,
    "items": [
      {
        "id": 1,
        "name": "深圳市XX电路板有限公司",
        "city": "深圳市",
        "county": "宝安区",
        "scale": "中型",
        "annual_output": 50000.00,
        "audit_status": "in-progress",
        "audit_score": 85.5,
        "audit_level": "II级",
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-03-20T15:45:00"
      }
    ]
  }
}
```

#### 3.2.2 审核指标数据格式

**请求:**
```http
GET /api/v1/pcb/enterprises/1/audit/indicators
```

**响应:**
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "indicators": [
      {
        "id": 1,
        "name": "基本要求",
        "category": "生产工艺与装备要求",
        "type": "qualitative",
        "weight": 1.5,
        "is_limiting": false,
        "current_value": null,
        "level": "II级",
        "score": 80.0,
        "recommended_schemes": [
          {
            "id": 15,
            "name": "自动化清洁生产线改造",
            "label": "自动化清洁生产线改造",
            "value": 15,
            "preview": {
              "type": "工艺改进",
              "problemSolved": "现有生产线设备老化,自动化程度低...",
              "description": "引进全自动水平沉铜线替代传统龙门沉铜线...",
              "economicBenefit": "每万平方米线路板节约原材料成本4.2万元...",
              "environmentalBenefit": "每万平方米线路板减少用水量180吨..."
            }
          }
        ]
      }
    ]
  }
}
```

#### 3.2.3 提交审核结果格式

**请求:**
```http
POST /api/v1/pcb/enterprises/1/audit/submit
Content-Type: application/json

{
  "indicators": [
    {
      "indicator_id": 1,
      "current_value": null,
      "level": "II级",
      "score": 80.0,
      "remark": "设备较为先进,但仍有改进空间"
    },
    {
      "indicator_id": 7,
      "current_value": 125.5,
      "level": "II级",
      "score": 80.0,
      "remark": "单位电耗符合II级标准"
    }
  ],
  "selected_schemes": [
    {
      "indicator_id": 1,
      "scheme_id": 15
    },
    {
      "indicator_id": 7,
      "scheme_id": 22
    }
  ],
  "auditor_name": "张三",
  "audit_date": "2024-03-20"
}
```

**响应:**
```json
{
  "code": 200,
  "message": "审核结果提交成功",
  "data": {
    "enterprise_id": 1,
    "total_score": 85.5,
    "overall_level": "II级",
    "improvement_items": 15,
    "limiting_indicators": 0,
    "audit_date": "2024-03-20T16:30:00"
  }
}
```

---

## 4. 核心功能实现方案

### 4.1 企业信息CRUD实现

#### 4.1.1 前端实现(Vue 3)

```javascript
// web/src/api/modules/pcb.js
import { request } from '@/utils'

export const pcbApi = {
  // 获取企业列表
  getEnterpriseList: (params) => {
    return request.get('/api/v1/pcb/enterprises', { params })
  },
  
  // 获取企业详情
  getEnterpriseDetail: (id) => {
    return request.get(`/api/v1/pcb/enterprises/${id}`)
  },
  
  // 创建企业
  createEnterprise: (data) => {
    return request.post('/api/v1/pcb/enterprises', data)
  },
  
  // 更新企业
  updateEnterprise: (id, data) => {
    return request.put(`/api/v1/pcb/enterprises/${id}`, data)
  },
  
  // 删除企业
  deleteEnterprise: (id) => {
    return request.delete(`/api/v1/pcb/enterprises/${id}`)
  }
}
```

#### 4.1.2 后端实现(FastAPI)

```python
# app/api/v1/pcb/enterprise.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.core.dependency import get_db
from app.schemas.pcb import EnterpriseCreate, EnterpriseUpdate, EnterpriseResponse, EnterpriseList
from app.controllers.pcb.enterprise import EnterpriseController

router = APIRouter()

@router.get("/", response_model=EnterpriseList)
async def get_enterprise_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    city: Optional[str] = None,
    audit_status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取PCB企业列表
    
    参数:
    - page: 页码
    - page_size: 每页数量
    - search: 搜索关键词(企业名称)
    - city: 所属地市
    - audit_status: 审核状态
    """
    skip = (page - 1) * page_size
    total, items = EnterpriseController.get_list(
        db, 
        skip=skip, 
        limit=page_size, 
        search=search,
        city=city,
        audit_status=audit_status
    )
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }

@router.get("/{enterprise_id}", response_model=EnterpriseResponse)
async def get_enterprise_detail(
    enterprise_id: int,
    db: Session = Depends(get_db)
):
    """获取PCB企业详情"""
    enterprise = EnterpriseController.get_by_id(db, enterprise_id)
    if not enterprise:
        raise HTTPException(status_code=404, detail="企业不存在")
    return enterprise

@router.post("/", response_model=EnterpriseResponse)
async def create_enterprise(
    enterprise: EnterpriseCreate,
    db: Session = Depends(get_db)
):
    """创建PCB企业"""
    return EnterpriseController.create(db, enterprise)

@router.put("/{enterprise_id}", response_model=EnterpriseResponse)
async def update_enterprise(
    enterprise_id: int,
    enterprise: EnterpriseUpdate,
    db: Session = Depends(get_db)
):
    """更新PCB企业信息"""
    updated = EnterpriseController.update(db, enterprise_id, enterprise)
    if not updated:
        raise HTTPException(status_code=404, detail="企业不存在")
    return updated

@router.delete("/{enterprise_id}")
async def delete_enterprise(
    enterprise_id: int,
    db: Session = Depends(get_db)
):
    """删除PCB企业(软删除)"""
    deleted = EnterpriseController.delete(db, enterprise_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="企业不存在")
    return {"message": "删除成功"}
```

```python
# app/controllers/pcb/enterprise.py
from sqlalchemy.orm = Session
from sqlalchemy import or_
from app.models.pcb import PCBEnterprise
from app.schemas.pcb import EnterpriseCreate, EnterpriseUpdate
from datetime import datetime

class EnterpriseController:
    @staticmethod
    def get_list(
        db: Session, 
        skip: int = 0, 
        limit: int = 20,
        search: str = None,
        city: str = None,
        audit_status: str = None
    ):
        """获取企业列表"""
        query = db.query(PCBEnterprise).filter(PCBEnterprise.deleted_at.is_(None))
        
        # 搜索条件
        if search:
            query = query.filter(PCBEnterprise.name.like(f"%{search}%"))
        if city:
            query = query.filter(PCBEnterprise.city == city)
        if audit_status:
            query = query.filter(PCBEnterprise.audit_status == audit_status)
        
        # 统计总数
        total = query.count()
        
        # 分页查询
        items = query.order_by(PCBEnterprise.created_at.desc()).offset(skip).limit(limit).all()
        
        return total, items
    
    @staticmethod
    def get_by_id(db: Session, enterprise_id: int):
        """根据ID获取企业"""
        return db.query(PCBEnterprise).filter(
            PCBEnterprise.id == enterprise_id,
            PCBEnterprise.deleted_at.is_(None)
        ).first()
    
    @staticmethod
    def create(db: Session, enterprise: EnterpriseCreate):
        """创建企业"""
        db_enterprise = PCBEnterprise(**enterprise.dict())
        db.add(db_enterprise)
        db.commit()
        db.refresh(db_enterprise)
        return db_enterprise
    
    @staticmethod
    def update(db: Session, enterprise_id: int, enterprise: EnterpriseUpdate):
        """更新企业"""
        db_enterprise = EnterpriseController.get_by_id(db, enterprise_id)
        if not db_enterprise:
            return None
        
        # 更新字段
        for field, value in enterprise.dict(exclude_unset=True).items():
            setattr(db_enterprise, field, value)
        
        db_enterprise.updated_at = datetime.now()
        db.commit()
        db.refresh(db_enterprise)
        return db_enterprise
    
    @staticmethod
    def delete(db: Session, enterprise_id: int):
        """软删除企业"""
        db_enterprise = EnterpriseController.get_by_id(db, enterprise_id)
        if not db_enterprise:
            return False
        
        db_enterprise.deleted_at = datetime.now()
        db.commit()
        return True
```

### 4.2 指标审核功能实现

#### 4.2.1 前端组件实现

```javascript
// web/src/views/cloud-audit/pcb/enterprise-detail/audit.vue (核心逻辑)

// 获取审核数据
const fetchAuditData = async () => {
  try {
    loading.value = true
    
    // 1. 获取指标定义
    const indicatorsResponse = await pcbApi.getIndicators()
    const indicators = indicatorsResponse.data
    
    // 2. 获取企业的审核结果
    const resultsResponse = await pcbApi.getAuditResults(props.enterpriseId)
    const results = resultsResponse.data || []
    
    // 3. 合并指标定义和审核结果
    const mergedData = indicators.map(indicator => {
      const result = results.find(r => r.indicator_id === indicator.id)
      return {
        ...indicator,
        current_value: result?.current_value || null,
        level: result?.level || null,
        score: result?.score || 0,
        remark: result?.remark || ''
      }
    })
    
    // 4. 为每个指标加载推荐方案
    for (const indicator of mergedData) {
      if (indicator.level && indicator.level !== 'I级') {
        const schemesResponse = await pcbApi.getRecommendedSchemes(
          props.enterpriseId,
          indicator.id
        )
        indicator.recommendedSchemes = schemesResponse.data || []
      }
    }
    
    // 5. 构建树形结构
    auditTreeData.value = buildTreeData(mergedData)
    
    // 6. 计算汇总
    calculateSummary()
    
  } catch (error) {
    console.error('获取审核数据失败:', error)
    window.$message.error('获取审核数据失败')
  } finally {
    loading.value = false
  }
}

// 提交审核结果
const handleSubmitAudit = async () => {
  try {
    loading.value = true
    
    // 1. 收集所有指标的审核结果
    const indicators = []
    auditTreeData.value.forEach(category => {
      if (category.children) {
        category.children.forEach(indicator => {
          indicators.push({
            indicator_id: indicator.id,
            current_value: indicator.current_value,
            level: indicator.level,
            score: indicator.score,
            remark: indicator.remark || ''
          })
        })
      }
    })
    
    // 2. 收集选定的方案
    const selected_schemes = []
    auditTreeData.value.forEach(category => {
      if (category.children) {
        category.children.forEach(indicator => {
          if (indicator.selectedSchemes && indicator.selectedSchemes.length > 0) {
            indicator.selectedSchemes.forEach(schemeId => {
              selected_schemes.push({
                indicator_id: indicator.id,
                scheme_id: schemeId
              })
            })
          }
        })
      }
    })
    
    // 3. 提交数据
    const auditData = {
      indicators,
      selected_schemes,
      auditor_name: '当前用户', // 从用户信息获取
      audit_date: new Date().toISOString().split('T')[0]
    }
    
    const response = await pcbApi.submitAuditResults(props.enterpriseId, auditData)
    
    window.$message.success('审核结果提交成功')
    
    // 4. 更新汇总信息
    summary.value = response.data
    
  } catch (error) {
    console.error('提交审核结果失败:', error)
    window.$message.error('提交审核结果失败')
  } finally {
    loading.value = false
  }
}
```

#### 4.2.2 后端API实现

```python
# app/api/v1/pcb/audit.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.dependency import get_db
from app.schemas.pcb import AuditSubmit, AuditResultResponse
from app.controllers.pcb.audit import AuditController

router = APIRouter()

@router.get("/enterprises/{enterprise_id}/audit/indicators")
async def get_audit_indicators(
    enterprise_id: int,
    db: Session = Depends(get_db)
):
    """获取审核指标列表"""
    return AuditController.get_indicators(db, enterprise_id)

@router.get("/enterprises/{enterprise_id}/audit/results")
async def get_audit_results(
    enterprise_id: int,
    db: Session = Depends(get_db)
):
    """获取企业的审核结果"""
    return AuditController.get_results(db, enterprise_id)

@router.post("/enterprises/{enterprise_id}/audit/submit")
async def submit_audit_results(
    enterprise_id: int,
    audit_data: AuditSubmit,
    db: Session = Depends(get_db)
):
    """提交审核结果"""
    return AuditController.submit_audit(db, enterprise_id, audit_data)

@router.get("/enterprises/{enterprise_id}/audit/schemes/{indicator_id}")
async def get_recommended_schemes(
    enterprise_id: int,
    indicator_id: int,
    db: Session = Depends(get_db)
):
    """获取指定指标的推荐方案"""
    return AuditController.get_recommended_schemes(db, enterprise_id, indicator_id)
```

```python
# app/controllers/pcb/audit.py
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.models.pcb import PCBIndicator, PCBAuditResult, PCBScheme, PCBIndicatorSchemeRelation, PCBEnterpriseScheme, PCBEnterprise
from app.schemas.pcb import AuditSubmit
from datetime import datetime

class AuditController:
    @staticmethod
    def get_indicators(db: Session, enterprise_id: int):
        """获取所有审核指标"""
        indicators = db.query(PCBIndicator).order_by(PCBIndicator.sort_order).all()
        
        # 获取企业的审核结果
        results = db.query(PCBAuditResult).filter(
            PCBAuditResult.enterprise_id == enterprise_id
        ).all()
        
        # 合并数据
        result_map = {r.indicator_id: r for r in results}
        
        indicator_list = []
        for indicator in indicators:
            result = result_map.get(indicator.id)
            indicator_dict = {
                "id": indicator.id,
                "name": indicator.name,
                "category": indicator.category,
                "type": indicator.type,
                "unit": indicator.unit,
                "weight": float(indicator.weight) if indicator.weight else 1.0,
                "is_limiting": indicator.is_limiting,
                "current_value": float(result.current_value) if result and result.current_value else None,
                "level": result.level if result else None,
                "score": float(result.score) if result and result.score else 0,
                "remark": result.remark if result else ""
            }
            indicator_list.append(indicator_dict)
        
        return {"code": 200, "message": "success", "data": indicator_list}
    
    @staticmethod
    def get_results(db: Session, enterprise_id: int):
        """获取企业的审核结果"""
        results = db.query(PCBAuditResult).filter(
            PCBAuditResult.enterprise_id == enterprise_id
        ).all()
        
        result_list = []
        for result in results:
            result_dict = {
                "indicator_id": result.indicator_id,
                "current_value": float(result.current_value) if result.current_value else None,
                "level": result.level,
                "score": float(result.score) if result.score else 0,
                "remark": result.remark or ""
            }
            result_list.append(result_dict)
        
        return {"code": 200, "message": "success", "data": result_list}
    
    @staticmethod
    def submit_audit(db: Session, enterprise_id: int, audit_data: AuditSubmit):
        """提交审核结果"""
        try:
            # 1. 更新或创建审核结果
            for indicator_data in audit_data.indicators:
                # 查找是否已存在
                existing = db.query(PCBAuditResult).filter(
                    and_(
                        PCBAuditResult.enterprise_id == enterprise_id,
                        PCBAuditResult.indicator_id == indicator_data.indicator_id
                    )
                ).first()
                
                if existing:
                    # 更新
                    existing.current_value = indicator_data.current_value
                    existing.level = indicator_data.level
                    existing.score = indicator_data.score
                    existing.remark = indicator_data.remark
                    existing.auditor_name = audit_data.auditor_name
                    existing.audit_date = datetime.strptime(audit_data.audit_date, '%Y-%m-%d').date()
                    existing.updated_at = datetime.now()
                else:
                    # 创建
                    new_result = PCBAuditResult(
                        enterprise_id=enterprise_id,
                        indicator_id=indicator_data.indicator_id,
                        current_value=indicator_data.current_value,
                        level=indicator_data.level,
                        score=indicator_data.score,
                        remark=indicator_data.remark,
                        auditor_name=audit_data.auditor_name,
                        audit_date=datetime.strptime(audit_data.audit_date, '%Y-%m-%d').date()
                    )
                    db.add(new_result)
            
            # 2. 保存选定的方案
            # 先删除旧的方案关联
            db.query(PCBEnterpriseScheme).filter(
                PCBEnterpriseScheme.enterprise_id == enterprise_id
            ).delete()
            
            # 添加新的方案关联
            for scheme_data in audit_data.selected_schemes:
                enterprise_scheme = PCBEnterpriseScheme(
                    enterprise_id=enterprise_id,
                    scheme_id=scheme_data.scheme_id,
                    indicator_id=scheme_data.indicator_id,
                    status='planned'
                )
                db.add(enterprise_scheme)
            
            # 3. 计算总分和等级
            results = db.query(PCBAuditResult).filter(
                PCBAuditResult.enterprise_id == enterprise_id
            ).all()
            
            total_weighted_score = 0
            total_weight = 0
            improvement_items = 0
            limiting_indicators = 0
            
            for result in results:
                indicator = db.query(PCBIndicator).filter(PCBIndicator.id == result.indicator_id).first()
                if indicator and result.level and result.score:
                    weight = float(indicator.weight) if indicator.weight else 1.0
                    total_weighted_score += float(result.score) * weight
                    total_weight += weight
                    
                    if result.level != 'I级':
                        improvement_items += 1
                    
                    if indicator.is_limiting and result.level == '不达标':
                        limiting_indicators += 1
            
            # 计算加权平均分
            avg_score = total_weighted_score / total_weight if total_weight > 0 else 0
            
            # 确定综合等级
            if avg_score >= 90:
                overall_level = 'I级'
            elif avg_score >= 80:
                overall_level = 'II级'
            elif avg_score >= 60:
                overall_level = 'III级'
            else:
                overall_level = '不达标'
            
            # 限定性指标约束
            if limiting_indicators > 0 and overall_level != '不达标':
                overall_level = 'III级'
            
            # 4. 更新企业审核状态
            enterprise = db.query(PCBEnterprise).filter(PCBEnterprise.id == enterprise_id).first()
            if enterprise:
                enterprise.audit_status = 'completed'
                enterprise.audit_score = avg_score
                enterprise.audit_level = overall_level
                enterprise.updated_at = datetime.now()
            
            db.commit()
            
            return {
                "code": 200,
                "message": "审核结果提交成功",
                "data": {
                    "enterprise_id": enterprise_id,
                    "total_score": round(avg_score, 2),
                    "overall_level": overall_level,
                    "improvement_items": improvement_items,
                    "limiting_indicators": limiting_indicators,
                    "audit_date": audit_data.audit_date
                }
            }
            
        except Exception as e:
            db.rollback()
            raise e
    
    @staticmethod
    def get_recommended_schemes(db: Session, enterprise_id: int, indicator_id: int):
        """获取指定指标的推荐方案"""
        # 查询指标关联的方案
        relations = db.query(PCBIndicatorSchemeRelation).filter(
            PCBIndicatorSchemeRelation.indicator_id == indicator_id
        ).order_by(PCBIndicatorSchemeRelation.priority.desc()).all()
        
        scheme_list = []
        for relation in relations:
            scheme = db.query(PCBScheme).filter(
                and_(
                    PCBScheme.id == relation.scheme_id,
                    PCBScheme.status == 'active',
                    PCBScheme.deleted_at.is_(None)
                )
            ).first()
            
            if scheme:
                scheme_dict = {
                    "value": scheme.id,
                    "label": scheme.name,
                    "preview": {
                        "type": scheme.type,
                        "problemSolved": scheme.problem_solved,
                        "description": scheme.description,
                        "economicBenefit": scheme.economic_benefit,
                        "environmentalBenefit": scheme.environmental_benefit,
                        "investment": float(scheme.investment) if scheme.investment else 0,
                        "paybackPeriod": float(scheme.payback_period) if scheme.payback_period else 0
                    }
                }
                scheme_list.append(scheme_dict)
        
        return {"code": 200, "message": "success", "data": scheme_list}
```

### 4.3 方案库管理实现

#### 4.3.1 前端实现

```javascript
// web/src/views/cloud-audit/pcb/enterprise-detail/scheme-library.vue (核心逻辑)

// 获取方案列表
const fetchSchemes = async () => {
  try {
    loading.value = true
    const response = await pcbApi.getSchemeList({
      page: pagination.page,
      page_size: pagination.pageSize,
      search: queryParams.search,
      type: queryParams.type,
      indicator_id: queryParams.indicatorId
    })
    
    schemes.value = response.data.items
    pagination.total = response.data.total
  } catch (error) {
    console.error('获取方案列表失败:', error)
    window.$message.error('获取方案列表失败')
  } finally {
    loading.value = false
  }
}

// 创建方案
const handleCreateScheme = async (schemeData) => {
  try {
    loading.value = true
    await pcbApi.createScheme(schemeData)
    window.$message.success('方案创建成功')
    showModal.value = false
    fetchSchemes()
  } catch (error) {
    console.error('创建方案失败:', error)
    window.$message.error('创建方案失败')
  } finally {
    loading.value = false
  }
}

// 更新方案
const handleUpdateScheme = async (id, schemeData) => {
  try {
    loading.value = true
    await pcbApi.updateScheme(id, schemeData)
    window.$message.success('方案更新成功')
    showModal.value = false
    fetchSchemes()
  } catch (error) {
    console.error('更新方案失败:', error)
    window.$message.error('更新方案失败')
  } finally {
    loading.value = false
  }
}

// 删除方案
const handleDeleteScheme = async (id) => {
  try {
    await window.$dialog.confirm({
      title: '确认删除',
      content: '确定要删除该方案吗?此操作不可恢复。'
    })
    
    await pcbApi.deleteScheme(id)
    window.$message.success('方案删除成功')
    fetchSchemes()
  } catch (error) {
    if (error) {
      console.error('删除方案失败:', error)
      window.$message.error('删除方案失败')
    }
  }
}
```

#### 4.3.2 后端API实现

```python
# app/api/v1/pcb/scheme.py
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.dependency import get_db
from app.schemas.pcb import SchemeCreate, SchemeUpdate, SchemeResponse, SchemeList
from app.controllers.pcb.scheme import SchemeController

router = APIRouter()

@router.get("/schemes", response_model=SchemeList)
async def get_scheme_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    type: Optional[str] = None,
    indicator_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """获取方案列表"""
    skip = (page - 1) * page_size
    total, items = SchemeController.get_list(
        db,
        skip=skip,
        limit=page_size,
        search=search,
        type=type,
        indicator_id=indicator_id
    )
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": items
    }

@router.post("/schemes", response_model=SchemeResponse)
async def create_scheme(
    scheme: SchemeCreate,
    db: Session = Depends(get_db)
):
    """创建方案"""
    return SchemeController.create(db, scheme)

@router.put("/schemes/{scheme_id}", response_model=SchemeResponse)
async def update_scheme(
    scheme_id: int,
    scheme: SchemeUpdate,
    db: Session = Depends(get_db)
):
    """更新方案"""
    return SchemeController.update(db, scheme_id, scheme)

@router.delete("/schemes/{scheme_id}")
async def delete_scheme(
    scheme_id: int,
    db: Session = Depends(get_db)
):
    """删除方案"""
    SchemeController.delete(db, scheme_id)
    return {"message": "删除成功"}
```

---

## 5. API接口设计

### 5.1 企业管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/pcb/enterprises | 获取企业列表 |
| GET | /api/v1/pcb/enterprises/{id} | 获取企业详情 |
| POST | /api/v1/pcb/enterprises | 创建企业 |
| PUT | /api/v1/pcb/enterprises/{id} | 更新企业 |
| DELETE | /api/v1/pcb/enterprises/{id} | 删除企业 |

### 5.2 审核管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/pcb/indicators | 获取所有指标定义 |
| GET | /api/v1/pcb/enterprises/{id}/audit/indicators | 获取企业审核指标 |
| GET | /api/v1/pcb/enterprises/{id}/audit/results | 获取企业审核结果 |
| POST | /api/v1/pcb/enterprises/{id}/audit/submit | 提交审核结果 |
| GET | /api/v1/pcb/enterprises/{id}/audit/schemes/{indicator_id} | 获取推荐方案 |

### 5.3 方案库接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/pcb/schemes | 获取方案列表 |
| GET | /api/v1/pcb/schemes/{id} | 获取方案详情 |
| POST | /api/v1/pcb/schemes | 创建方案 |
| PUT | /api/v1/pcb/schemes/{id} | 更新方案 |
| DELETE | /api/v1/pcb/schemes/{id} | 删除方案 |
| POST | /api/v1/pcb/schemes/{id}/indicators | 关联指标 |

### 5.4 预审核接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/pcb/enterprises/{id}/pre-audit | 获取预审核数据 |
| POST | /api/v1/pcb/enterprises/{id}/pre-audit | 提交预审核数据 |
| PUT | /api/v1/pcb/enterprises/{id}/pre-audit | 更新预审核数据 |

### 5.5 报告管理接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/v1/pcb/enterprises/{id}/report | 获取审核报告 |
| POST | /api/v1/pcb/enterprises/{id}/report/generate | 生成审核报告 |
| PUT | /api/v1/pcb/enterprises/{id}/report | 更新审核报告 |
| GET | /api/v1/pcb/enterprises/{id}/report/export | 导出报告(PDF/Word) |

---

## 6. 数据流转图

### 6.1 完整审核流程

```
1. 创建企业
   ↓
2. 填写基本信息
   ↓
3. 筹划与组织
   ↓
4. 预审核(填报现状数据)
   ↓
5. 审核(评估64项指标)
   ├─ 自动计算定量指标等级
   ├─ 人工选择定性指标等级
   ├─ 审核限定性指标
   └─ 推荐改进方案
   ↓
6. 选择改进方案
   ↓
7. 生成审核报告
   ↓
8. 导出报告
```

### 6.2 数据关联关系

```
pcb_enterprises (企业表)
    ├── pcb_pre_audit_data (预审核数据)
    ├── pcb_audit_results (审核结果)
    │   └── pcb_indicators (指标定义)
    ├── pcb_enterprise_schemes (企业选定方案)
    │   └── pcb_schemes (方案库)
    └── pcb_audit_reports (审核报告)

pcb_indicators (指标定义)
    └── pcb_indicator_scheme_relation (指标方案关联)
        └── pcb_schemes (方案库)
```

---

## 7. 技术实施建议

### 7.1 开发步骤

#### 阶段一:数据库设计与初始化(1-2天)
1. 创建数据库表结构
2. 初始化64项指标数据
3. 导入130项清洁生产方案
4. 建立指标与方案的关联关系
5. 创建必要的索引

#### 阶段二:企业管理功能(2-3天)
1. 实现企业CRUD的后端API
2. 实现企业列表和详情的前端页面
3. 集成企业创建/编辑表单
4. 测试企业管理功能

#### 阶段三:审核功能核心(3-4天)
1. 实现指标管理后端API
2. 实现审核结果提交后端API
3. 完善前端审核页面
4. 集成64项指标展示和评级
5. 实现自动计算定量指标逻辑
6. 测试审核流程

#### 阶段四:方案库管理(2-3天)
1. 实现方案库CRUD后端API
2. 实现推荐方案接口
3. 完善前端方案库页面
4. 集成方案搜索和筛选
5. 测试方案推荐功能

#### 阶段五:预审核和报告(2-3天)
1. 实现预审核数据管理API
2. 实现报告生成API
3. 完善前端预审核页面
4. 完善前端报告页面
5. 集成报告导出功能

#### 阶段六:测试与优化(2-3天)
1. 功能测试
2. 性能优化
3. 用户体验优化
4. Bug修复

### 7.2 关键技术点

#### 7.2.1 前端技术要点
- **组件复用**:充分利用Naive UI组件,避免重复开发
- **状态管理**:使用Vue 3 Composition API管理组件状态
- **数据缓存**:使用sessionStorage缓存审核进度
- **异步加载**:大量数据分批加载,提升性能

#### 7.2.2 后端技术要点
- **ORM优化**:合理使用SQLAlchemy的懒加载和预加载
- **事务管理**:审核提交使用数据库事务确保数据一致性
- **缓存策略**:指标定义和方案库数据使用Redis缓存
- **日志记录**:记录所有审核操作日志

#### 7.2.3 数据库优化
- **索引优化**:为常用查询字段建立索引
- **JSON字段**:预审核数据使用JSON存储,提高灵活性
- **软删除**:企业和方案使用软删除,保留历史数据
- **归档策略**:定期归档历史审核记录

### 7.3 注意事项

1. **数据一致性**:审核结果提交时要确保企业总分和等级的同步更新
2. **并发控制**:多人同时审核同一企业时需要处理并发冲突
3. **权限控制**:不同角色的用户有不同的操作权限
4. **数据备份**:定期备份数据库,防止数据丢失
5. **性能监控**:监控API响应时间和数据库查询性能

### 7.4 扩展性考虑

1. **多行业支持**:数据库设计可扩展支持其他行业(钢铁、玻璃等)
2. **指标动态配置**:指标定义可通过管理界面动态调整
3. **方案动态更新**:方案库支持持续更新和版本管理
4. **报告模板**:支持自定义报告模板
5. **数据导入导出**:支持批量导入导出企业数据

---

## 总结

本方案提供了PCB行业清洁生产云审核模块的完整数据库设计和前后端交互方案,涵盖了:

1. **8张核心数据库表**:企业表、指标表、审核结果表、方案库表等
2. **完整的API接口设计**:企业管理、审核管理、方案库管理等30+个接口
3. **详细的实现代码**:前端Vue组件和后端FastAPI控制器的核心代码
4. **清晰的数据流转**:从企业创建到审核完成的完整流程
5. **实施路线图**:分6个阶段,预计12-18天完成开发

该方案完全基于前后端分离的架构,支持用户在前端界面对企业信息、审核指标、方案库进行增删改查操作,所有业务逻辑由后端API处理,数据库设计合理,易于扩展和维护。

**建议先按照阶段一创建数据库,然后逐步实现各个功能模块,最后进行集成测试和优化。**


