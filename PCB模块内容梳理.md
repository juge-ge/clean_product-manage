# PCB行业清洁生产云审核模块开发文档

## 目录

- [1. 模块概述](#1-模块概述)
- [2. 技术架构](#2-技术架构)
- [3. 功能模块设计](#3-功能模块设计)
- [4. 路由配置](#4-路由配置)
- [5. API接口设计](#5-api接口设计)
- [6. 数据模型设计](#6-数据模型设计)
- [7. 组件设计](#7-组件设计)
- [8. 页面设计规范](#8-页面设计规范)
- [9. 开发规范](#9-开发规范)

## 1. 模块概述

### 1.1 模块定位
PCB行业清洁生产云审核模块是清洁生产云审核系统的重要组成部分，专门针对印制电路板（PCB）制造企业的清洁生产审核需求设计，提供标准化的在线审核流程管理。

### 1.2 核心功能
- **企业信息管理**：PCB企业基本信息的录入、编辑、查看和删除
- **审核流程管理**：完整的审核流程跟踪，包括筹划与组织、预审核、审核、报告生成等
- **数据填报与评估**：基于《印制电路板企业清洁生产评价指标》的实时数据评估
- **方案库管理**：清洁生产整改方案的增删改查
- **报告生成**：自动生成可编辑的审核评估报告

### 1.3 技术特点
- 基于Vue 3 + Composition API开发
- 采用前后端分离架构
- 支持实时数据验证和等级评估
- 响应式设计，支持多端访问
- 模块化组件设计，便于维护和扩展

## 2. 技术架构

### 2.1 前端技术栈
```javascript
{
  "框架": "Vue 3.x + Composition API",
  "UI组件库": "Naive UI",
  "状态管理": "Pinia",
  "路由管理": "Vue Router 4.x",
  "HTTP客户端": "Axios",
  "图标库": "Carbon Icons / Material Design Icons",
  "图表库": "ECharts",
  "构建工具": "Vite",
  "CSS框架": "UnoCSS"
}
```

### 2.2 后端技术栈
```python
{
  "Web框架": "FastAPI",
  "数据库": "SQLite",
  "ORM": "SQLAlchemy",
  "数据验证": "Pydantic",
  "认证": "JWT"
}
```

### 2.3 项目结构
```
web/src/views/cloud-audit/pcb/
├── index.vue                    # PCB模块首页（企业列表）
├── enterprise-detail/           # 企业详情页面
│   ├── index.vue               # 企业详情布局
│   ├── basic-info.vue          # 企业基本信息
│   ├── planning.vue            # 筹划与组织
│   ├── pre-audit.vue           # 预审核
│   ├── audit.vue               # 审核
│   ├── scheme-library.vue      # 方案库
│   └── report.vue              # 审核报告
└── components/                 # PCB模块专用组件
    ├── EnterpriseCard.vue      # 企业卡片组件
    ├── AuditProgress.vue       # 审核进度组件
    ├── DataInputForm.vue       # 数据输入表单
    ├── StandardComparison.vue  # 标准对比组件
    └── ReportEditor.vue        # 报告编辑器
```

## 3. 功能模块设计

### 3.1 PCB首页（企业列表管理）

#### 3.1.1 功能描述
- 以卡片网格形式展示所有PCB企业
- 提供企业搜索和筛选功能
- 支持企业的增删改查操作
- 显示企业审核状态和进度

#### 3.1.2 页面布局
```vue
<template>
  <CommonPage title="PCB行业清洁生产审核">
    <!-- 搜索和操作栏 -->
    <div class="search-bar">
      <n-input 
        v-model:value="searchKeyword" 
        placeholder="请输入企业名称"
        clearable
      />
      <n-button type="primary" @click="showCreateModal = true">
        创建企业
      </n-button>
    </div>
    
    <!-- 企业卡片网格 -->
    <div class="enterprise-grid">
      <EnterpriseCard 
        v-for="enterprise in enterprises"
        :key="enterprise.id"
        :enterprise="enterprise"
        @view="handleView"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>
    
    <!-- 创建/编辑企业弹窗 -->
    <CrudModal
      v-model:visible="showCreateModal"
      :title="isEdit ? '编辑企业' : '创建企业'"
      @save="handleSave"
    >
      <EnterpriseForm ref="formRef" :data="currentEnterprise" />
    </CrudModal>
  </CommonPage>
</template>
```

#### 3.1.3 企业卡片组件设计
```vue
<!-- EnterpriseCard.vue -->
<template>
  <n-card class="enterprise-card" hoverable>
    <div class="card-header">
      <h3>{{ enterprise.name }}</h3>
      <n-tag :type="getStatusType(enterprise.auditStatus)">
        {{ getStatusText(enterprise.auditStatus) }}
      </n-tag>
    </div>
    
    <div class="card-content">
      <p><strong>所属地市：</strong>{{ enterprise.city }}</p>
      <p><strong>所属县：</strong>{{ enterprise.county }}</p>
      <p><strong>规模：</strong>{{ enterprise.scale }}</p>
      <p><strong>年产值：</strong>{{ enterprise.annualOutput }}万元</p>
    </div>
    
    <div class="card-footer">
      <n-button size="small" @click="$emit('view', enterprise.id)">
        查看详情
      </n-button>
      <n-button size="small" type="primary" @click="$emit('edit', enterprise)">
        编辑
      </n-button>
      <n-button size="small" type="error" @click="$emit('delete', enterprise.id)">
        删除
      </n-button>
    </div>
  </n-card>
</template>
```

### 3.2 企业详情页面

#### 3.2.1 整体布局设计
```vue
<template>
  <div class="enterprise-detail">
    <!-- 顶部导航栏 -->
    <div class="top-nav">
      <n-breadcrumb>
        <n-breadcrumb-item @click="$router.push('/cloud-audit/pcb')">
          PCB行业审核
        </n-breadcrumb-item>
        <n-breadcrumb-item>{{ enterprise.name }}</n-breadcrumb-item>
      </n-breadcrumb>
      <n-button @click="$router.push('/cloud-audit/pcb')">
        退出
      </n-button>
    </div>
    
    <!-- 审核进度条 -->
    <AuditProgress 
      :current-step="currentStep"
      :steps="auditSteps"
    />
    
    <!-- 模块导航 -->
    <n-tabs v-model:value="activeTab" type="line">
      <n-tab-pane name="basic-info" tab="企业信息">
        <BasicInfo :enterprise-id="enterpriseId" />
      </n-tab-pane>
      <n-tab-pane name="planning" tab="筹划与组织">
        <Planning :enterprise-id="enterpriseId" />
      </n-tab-pane>
      <n-tab-pane name="pre-audit" tab="预审核">
        <PreAudit :enterprise-id="enterpriseId" />
      </n-tab-pane>
      <n-tab-pane name="audit" tab="审核">
        <Audit :enterprise-id="enterpriseId" />
      </n-tab-pane>
      <n-tab-pane name="scheme-library" tab="方案库">
        <SchemeLibrary :enterprise-id="enterpriseId" />
      </n-tab-pane>
      <n-tab-pane name="report" tab="审核报告">
        <Report :enterprise-id="enterpriseId" />
      </n-tab-pane>
    </n-tabs>
  </div>
</template>
```

#### 3.2.2 审核进度组件
```vue
<!-- AuditProgress.vue -->
<template>
  <div class="audit-progress">
    <n-steps :current="currentStep" :status="status">
      <n-step 
        v-for="(step, index) in steps" 
        :key="index"
        :title="step.title"
        :description="step.description"
      />
    </n-steps>
  </div>
</template>

<script setup>
const props = defineProps({
  currentStep: {
    type: Number,
    default: 0
  },
  steps: {
    type: Array,
    default: () => [
      { title: '企业信息', description: '基本信息录入' },
      { title: '筹划与组织', description: '审核团队组建' },
      { title: '预审核', description: '数据填报评估' },
      { title: '审核', description: '指标审核' },
      { title: '审核报告', description: '报告生成' },
      { title: '方案库', description: '整改方案' }
    ]
  }
})
</script>
```

### 3.3 企业基本信息模块

#### 3.3.1 数据字段设计
```javascript
const enterpriseFields = {
  // 基本信息
  name: { label: '企业名称', type: 'input', required: true },
  city: { label: '所属地市', type: 'select', required: true },
  county: { label: '所属县', type: 'select', required: true },
  scale: { label: '规模', type: 'select', options: ['大型', '中型', '小型'] },
  
  // 财务信息
  capital: { label: '注册资本（万元）', type: 'number', required: true },
  annualOutput: { label: '年产值（万元）', type: 'number', required: true },
  annualSales: { label: '年销售额（万元）', type: 'number', required: true },
  
  // 联系信息
  legalRepresentative: { label: '法人代表', type: 'input', required: true },
  address: { label: '注册地址', type: 'textarea', required: true },
  productionAddress: { label: '生产地址', type: 'textarea', required: true },
  postalCode: { label: '邮编', type: 'input' },
  contact: { label: '联系人', type: 'input', required: true },
  phone: { label: '联系电话', type: 'input', required: true },
  
  // 其他信息
  establishmentDate: { label: '建厂时间', type: 'date', required: true },
  industry: { label: '所属行业', type: 'input', default: 'PCB制造' }
}
```

### 3.4 筹划与组织模块

#### 3.4.1 功能设计
- **审核工作组**：在线组建审核团队成员
- **工作计划**：制定审核工作计划和时间节点
- **宣传与培训**：记录宣传培训活动

```vue
<template>
  <div class="planning-module">
    <n-card title="审核工作组" class="mb-4">
      <n-button type="primary" @click="showAddMemberModal = true">
        添加成员
      </n-button>
      <n-data-table :columns="memberColumns" :data="auditTeam" />
    </n-card>
    
    <n-card title="工作计划" class="mb-4">
      <n-button type="primary" @click="showPlanModal = true">
        制定计划
      </n-button>
      <n-timeline>
        <n-timeline-item 
          v-for="plan in workPlans"
          :key="plan.id"
          :title="plan.title"
          :content="plan.description"
          :time="plan.deadline"
        />
      </n-timeline>
    </n-card>
    
    <n-card title="宣传与培训">
      <n-button type="primary" @click="showTrainingModal = true">
        添加培训记录
      </n-button>
      <n-data-table :columns="trainingColumns" :data="trainingRecords" />
    </n-card>
  </div>
</template>
```

### 3.5 预审核模块（核心功能）

#### 3.5.1 数据填报界面设计
```vue
<template>
  <div class="pre-audit-module">
    <n-card title="PCB企业清洁生产数据填报">
      <n-form ref="formRef" :model="formData" :rules="rules">
        <n-grid :cols="2" :x-gap="24">
          <!-- 产能产量数据 -->
          <n-form-item-grid-item label="单位产品电耗（kWh/m²）">
            <n-input-number 
              v-model:value="formData.unitPowerConsumption"
              @update:value="handleDataChange('unitPowerConsumption', $event)"
            />
            <StandardComparison 
              :value="formData.unitPowerConsumption"
              :standard="standards.unitPowerConsumption"
              class="mt-2"
            />
          </n-form-item-grid-item>
          
          <n-form-item-grid-item label="废水产生量（m³/m²）">
            <n-input-number 
              v-model:value="formData.wastewaterGeneration"
              @update:value="handleDataChange('wastewaterGeneration', $event)"
            />
            <StandardComparison 
              :value="formData.wastewaterGeneration"
              :standard="standards.wastewaterGeneration"
              class="mt-2"
            />
          </n-form-item-grid-item>
          
          <!-- 更多数据字段... -->
        </n-grid>
      </n-form>
    </n-card>
    
    <!-- 评估结果汇总 -->
    <n-card title="评估结果汇总" class="mt-4">
      <n-grid :cols="4" :x-gap="16">
        <n-statistic label="I级指标" :value="levelCounts.level1" />
        <n-statistic label="II级指标" :value="levelCounts.level2" />
        <n-statistic label="III级指标" :value="levelCounts.level3" />
        <n-statistic label="不达标指标" :value="levelCounts.unqualified" />
      </n-grid>
    </n-card>
  </div>
</template>
```

#### 3.5.2 标准对比组件
```vue
<!-- StandardComparison.vue -->
<template>
  <div class="standard-comparison">
    <n-tag 
      :type="getLevelType(level)"
      :bordered="false"
      size="small"
    >
      {{ getLevelText(level) }}
    </n-tag>
    <span class="ml-2 text-sm text-gray-500">
      标准值：{{ standard.value }} {{ standard.unit }}
    </span>
  </div>
</template>

<script setup>
const props = defineProps({
  value: Number,
  standard: Object
})

const level = computed(() => {
  if (!props.value || !props.standard) return 'unknown'
  
  const { value } = props
  const { level1, level2, level3 } = props.standard
  
  if (value <= level1) return 'level1'
  if (value <= level2) return 'level2'
  if (value <= level3) return 'level3'
  return 'unqualified'
})

const getLevelType = (level) => {
  const types = {
    level1: 'success',
    level2: 'info',
    level3: 'warning',
    unqualified: 'error',
    unknown: 'default'
  }
  return types[level] || 'default'
}

const getLevelText = (level) => {
  const texts = {
    level1: 'I级',
    level2: 'II级',
    level3: 'III级',
    unqualified: '不达标',
    unknown: '未评估'
  }
  return texts[level] || '未知'
}
</script>
```

### 3.6 审核模块

#### 3.6.1 审核界面设计
```vue
<template>
  <div class="audit-module">
    <n-card title="PCB企业清洁生产审核">
      <n-tabs type="line">
        <n-tab-pane 
          v-for="category in auditCategories"
          :key="category.id"
          :name="category.id"
          :tab="category.name"
        >
          <n-data-table
            :columns="getAuditColumns(category.id)"
            :data="getAuditData(category.id)"
            :row-key="row => row.id"
          >
            <template #action="{ row }">
              <n-button 
                size="small" 
                type="primary"
                @click="showSchemeModal(row)"
              >
                查看方案
              </n-button>
              <n-button 
                size="small" 
                type="info"
                @click="editScheme(row)"
              >
                编辑方案
              </n-button>
            </template>
          </n-data-table>
        </n-tab-pane>
      </n-tabs>
      
      <div class="mt-4 text-center">
        <n-button 
          type="primary" 
          size="large"
          :disabled="!canGenerateReport"
          @click="generateReport"
        >
          生成评估报告
        </n-button>
      </div>
    </n-card>
  </div>
</template>
```

### 3.7 清洁生产方案库

#### 3.7.1 方案管理界面
```vue
<template>
  <div class="scheme-library">
    <n-card title="清洁生产方案库">
      <template #header-extra>
        <n-button type="primary" @click="showAddModal = true">
          添加方案
        </n-button>
      </template>
      
      <CrudTable
        :columns="schemeColumns"
        :get-data="getSchemeList"
        :query-items="queryItems"
      >
        <template #queryBar>
          <QueryBarItem label="指标名称">
            <n-input v-model:value="queryItems.indicatorName" placeholder="请输入指标名称" />
          </QueryBarItem>
          <QueryBarItem label="方案类型">
            <n-select v-model:value="queryItems.schemeType" :options="schemeTypeOptions" />
          </QueryBarItem>
        </template>
      </CrudTable>
    </n-card>
    
    <!-- 添加/编辑方案弹窗 -->
    <CrudModal
      v-model:visible="showAddModal"
      :title="isEdit ? '编辑方案' : '添加方案'"
      @save="handleSaveScheme"
    >
      <SchemeForm ref="schemeFormRef" :data="currentScheme" />
    </CrudModal>
  </div>
</template>
```

### 3.8 审核评估报告

#### 3.8.1 报告生成和编辑
```vue
<template>
  <div class="report-module">
    <n-card title="PCB企业清洁生产审核评估报告">
      <template #header-extra>
        <n-space>
          <n-button @click="previewReport">预览报告</n-button>
          <n-button type="primary" @click="exportReport('pdf')">导出PDF</n-button>
          <n-button type="primary" @click="exportReport('word')">导出Word</n-button>
        </n-space>
      </template>
      
      <ReportEditor
        ref="editorRef"
        v-model:content="reportContent"
        :enterprise-data="enterpriseData"
        :audit-data="auditData"
        :scheme-data="schemeData"
      />
    </n-card>
  </div>
</template>
```

## 4. 路由配置

### 4.1 PCB模块路由结构
```javascript
// web/src/router/modules/cloudAudit.js (更新PCB部分)
{
  path: 'pcb',
  name: 'PCB',
  component: () => import('@/views/cloud-audit/pcb/index.vue'),
  meta: { 
    title: 'PCB行业审核',
    icon: 'carbon:chip'
  },
  children: [
    {
      path: ':id',
      name: 'PCBEnterpriseDetail',
      component: () => import('@/views/cloud-audit/pcb/enterprise-detail/index.vue'),
      meta: { 
        title: '企业详情',
        hideInMenu: true
      },
      children: [
        {
          path: 'basic-info',
          name: 'PCBBasicInfo',
          component: () => import('@/views/cloud-audit/pcb/enterprise-detail/basic-info.vue'),
          meta: { title: '企业信息' }
        },
        {
          path: 'planning',
          name: 'PCBPlanning',
          component: () => import('@/views/cloud-audit/pcb/enterprise-detail/planning.vue'),
          meta: { title: '筹划与组织' }
        },
        {
          path: 'pre-audit',
          name: 'PCBPreAudit',
          component: () => import('@/views/cloud-audit/pcb/enterprise-detail/pre-audit.vue'),
          meta: { title: '预审核' }
        },
        {
          path: 'audit',
          name: 'PCBAudit',
          component: () => import('@/views/cloud-audit/pcb/enterprise-detail/audit.vue'),
          meta: { title: '审核' }
        },
        {
          path: 'scheme-library',
          name: 'PCBSchemeLibrary',
          component: () => import('@/views/cloud-audit/pcb/enterprise-detail/scheme-library.vue'),
          meta: { title: '方案库' }
        },
        {
          path: 'report',
          name: 'PCBReport',
          component: () => import('@/views/cloud-audit/pcb/enterprise-detail/report.vue'),
          meta: { title: '审核报告' }
        }
      ]
    }
  ]
}
```

## 5. API接口设计

### 5.1 PCB企业管理API
```javascript
// web/src/api/modules/pcb.js
import { request } from '@/utils'

export const pcbApi = {
  // 企业列表管理
  getEnterpriseList: (params) => request.get('/api/v1/pcb/enterprise', { params }),
  getEnterpriseDetail: (id) => request.get(`/api/v1/pcb/enterprise/${id}`),
  createEnterprise: (data) => request.post('/api/v1/pcb/enterprise', data),
  updateEnterprise: (id, data) => request.put(`/api/v1/pcb/enterprise/${id}`, data),
  deleteEnterprise: (id) => request.delete(`/api/v1/pcb/enterprise/${id}`),
  
  // 筹划与组织
  getAuditTeam: (enterpriseId) => request.get(`/api/v1/pcb/enterprise/${enterpriseId}/team`),
  addTeamMember: (enterpriseId, data) => request.post(`/api/v1/pcb/enterprise/${enterpriseId}/team`, data),
  updateTeamMember: (enterpriseId, memberId, data) => request.put(`/api/v1/pcb/enterprise/${enterpriseId}/team/${memberId}`, data),
  deleteTeamMember: (enterpriseId, memberId) => request.delete(`/api/v1/pcb/enterprise/${enterpriseId}/team/${memberId}`),
  
  getWorkPlans: (enterpriseId) => request.get(`/api/v1/pcb/enterprise/${enterpriseId}/plans`),
  createWorkPlan: (enterpriseId, data) => request.post(`/api/v1/pcb/enterprise/${enterpriseId}/plans`, data),
  updateWorkPlan: (enterpriseId, planId, data) => request.put(`/api/v1/pcb/enterprise/${enterpriseId}/plans/${planId}`, data),
  
  getTrainingRecords: (enterpriseId) => request.get(`/api/v1/pcb/enterprise/${enterpriseId}/training`),
  createTrainingRecord: (enterpriseId, data) => request.post(`/api/v1/pcb/enterprise/${enterpriseId}/training`, data),
  
  // 预审核数据
  getPreAuditData: (enterpriseId) => request.get(`/api/v1/pcb/enterprise/${enterpriseId}/pre-audit`),
  submitPreAuditData: (enterpriseId, data) => request.post(`/api/v1/pcb/enterprise/${enterpriseId}/pre-audit`, data),
  getAuditStandards: () => request.get('/api/v1/pcb/standards'),
  
  // 审核
  getAuditData: (enterpriseId) => request.get(`/api/v1/pcb/enterprise/${enterpriseId}/audit`),
  submitAuditResult: (enterpriseId, data) => request.post(`/api/v1/pcb/enterprise/${enterpriseId}/audit`, data),
  
  // 方案库
  getSchemeList: (params) => request.get('/api/v1/pcb/scheme', { params }),
  getSchemeDetail: (id) => request.get(`/api/v1/pcb/scheme/${id}`),
  createScheme: (data) => request.post('/api/v1/pcb/scheme', data),
  updateScheme: (id, data) => request.put(`/api/v1/pcb/scheme/${id}`, data),
  deleteScheme: (id) => request.delete(`/api/v1/pcb/scheme/${id}`),
  
  // 报告生成
  generateReport: (enterpriseId) => request.get(`/api/v1/pcb/enterprise/${enterpriseId}/report`),
  updateReport: (enterpriseId, data) => request.put(`/api/v1/pcb/enterprise/${enterpriseId}/report`, data),
  exportReport: (enterpriseId, format) => request.get(`/api/v1/pcb/enterprise/${enterpriseId}/report/export`, { 
    params: { format },
    responseType: 'blob'
  })
}
```

### 5.2 后端API接口规范
```python
# app/api/v1/pcb/enterprise.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependency import get_db
from app.schemas.pcb import EnterpriseCreate, EnterpriseUpdate, EnterpriseResponse
from app.controllers.pcb import EnterpriseController

router = APIRouter()

@router.get("/", response_model=List[EnterpriseResponse])
async def get_enterprise_list(
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取PCB企业列表"""
    return EnterpriseController.get_list(db, skip=skip, limit=limit, search=search)

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
    return EnterpriseController.update(db, enterprise_id, enterprise)

@router.delete("/{enterprise_id}")
async def delete_enterprise(
    enterprise_id: int,
    db: Session = Depends(get_db)
):
    """删除PCB企业"""
    EnterpriseController.delete(db, enterprise_id)
    return {"message": "删除成功"}
```

## 6. 数据模型设计

### 6.1 前端数据模型
```javascript
// web/src/types/pcb.js
export const EnterpriseModel = {
  id: Number,
  name: String,
  city: String,
  county: String,
  scale: String,
  capital: Number,
  annualOutput: Number,
  annualSales: Number,
  legalRepresentative: String,
  address: String,
  productionAddress: String,
  postalCode: String,
  contact: String,
  phone: String,
  establishmentDate: String,
  industry: String,
  auditStatus: String, // 'pending', 'in-progress', 'completed'
  createdAt: String,
  updatedAt: String
}

export const PreAuditDataModel = {
  enterpriseId: Number,
  unitPowerConsumption: Number,
  wastewaterGeneration: Number,
  solidWasteGeneration: Number,
  energyConsumption: Number,
  waterConsumption: Number,
  chemicalConsumption: Number,
  // 更多指标...
  assessmentResults: {
    level1Count: Number,
    level2Count: Number,
    level3Count: Number,
    unqualifiedCount: Number
  }
}

export const AuditSchemeModel = {
  id: Number,
  indicatorName: String,
  schemeType: String,
  title: String,
  description: String,
  implementation: String,
  expectedEffect: String,
  investment: Number,
  paybackPeriod: Number,
  createdAt: String,
  updatedAt: String
}
```

### 6.2 后端数据模型
```python
# app/models/pcb.py
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class PCBEnterprise(Base):
    __tablename__ = "pcb_enterprises"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="企业名称")
    city = Column(String(100), nullable=False, comment="所属地市")
    county = Column(String(100), nullable=False, comment="所属县")
    scale = Column(String(50), comment="规模")
    capital = Column(Float, comment="注册资本（万元）")
    annual_output = Column(Float, comment="年产值（万元）")
    annual_sales = Column(Float, comment="年销售额（万元）")
    legal_representative = Column(String(100), comment="法人代表")
    address = Column(Text, comment="注册地址")
    production_address = Column(Text, comment="生产地址")
    postal_code = Column(String(10), comment="邮编")
    contact = Column(String(100), comment="联系人")
    phone = Column(String(20), comment="联系电话")
    establishment_date = Column(DateTime, comment="建厂时间")
    industry = Column(String(100), default="PCB制造", comment="所属行业")
    audit_status = Column(String(50), default="pending", comment="审核状态")
    
    # 关联关系
    audit_team = relationship("PCBAuditTeam", back_populates="enterprise")
    work_plans = relationship("PCBWorkPlan", back_populates="enterprise")
    pre_audit_data = relationship("PCBPreAuditData", back_populates="enterprise")
    audit_results = relationship("PCBAuditResult", back_populates="enterprise")

class PCBPreAuditData(Base):
    __tablename__ = "pcb_pre_audit_data"
    
    id = Column(Integer, primary_key=True, index=True)
    enterprise_id = Column(Integer, ForeignKey("pcb_enterprises.id"))
    unit_power_consumption = Column(Float, comment="单位产品电耗（kWh/m²）")
    wastewater_generation = Column(Float, comment="废水产生量（m³/m²）")
    solid_waste_generation = Column(Float, comment="固体废物产生量（kg/m²）")
    energy_consumption = Column(Float, comment="综合能耗（kgce/m²）")
    water_consumption = Column(Float, comment="新鲜水消耗量（m³/m²）")
    chemical_consumption = Column(Float, comment="化学品消耗量（kg/m²）")
    
    # 评估结果
    level1_count = Column(Integer, default=0, comment="I级指标数量")
    level2_count = Column(Integer, default=0, comment="II级指标数量")
    level3_count = Column(Integer, default=0, comment="III级指标数量")
    unqualified_count = Column(Integer, default=0, comment="不达标指标数量")
    
    enterprise = relationship("PCBEnterprise", back_populates="pre_audit_data")

class PCBAuditScheme(Base):
    __tablename__ = "pcb_audit_schemes"
    
    id = Column(Integer, primary_key=True, index=True)
    indicator_name = Column(String(200), nullable=False, comment="指标名称")
    scheme_type = Column(String(100), comment="方案类型")
    title = Column(String(200), nullable=False, comment="方案标题")
    description = Column(Text, comment="方案描述")
    implementation = Column(Text, comment="实施方案")
    expected_effect = Column(Text, comment="预期效果")
    investment = Column(Float, comment="投资估算（万元）")
    payback_period = Column(Float, comment="投资回收期（年）")
```

## 7. 组件设计

### 7.1 通用组件规范
```vue
<!-- 企业卡片组件 -->
<template>
  <n-card class="enterprise-card" hoverable>
    <div class="card-header">
      <h3>{{ enterprise.name }}</h3>
      <n-tag :type="getStatusType(enterprise.auditStatus)">
        {{ getStatusText(enterprise.auditStatus) }}
      </n-tag>
    </div>
    
    <div class="card-content">
      <p><strong>所属地市：</strong>{{ enterprise.city }}</p>
      <p><strong>所属县：</strong>{{ enterprise.county }}</p>
      <p><strong>规模：</strong>{{ enterprise.scale }}</p>
      <p><strong>年产值：</strong>{{ enterprise.annualOutput }}万元</p>
    </div>
    
    <div class="card-footer">
      <n-button size="small" @click="$emit('view', enterprise.id)">
        查看详情
      </n-button>
      <n-button size="small" type="primary" @click="$emit('edit', enterprise)">
        编辑
      </n-button>
      <n-button size="small" type="error" @click="$emit('delete', enterprise.id)">
        删除
      </n-button>
    </div>
  </n-card>
</template>

<script setup>
defineProps({
  enterprise: {
    type: Object,
    required: true
  }
})

defineEmits(['view', 'edit', 'delete'])

const getStatusType = (status) => {
  const types = {
    pending: 'default',
    'in-progress': 'info',
    completed: 'success'
  }
  return types[status] || 'default'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待审核',
    'in-progress': '审核中',
    completed: '已完成'
  }
  return texts[status] || '未知'
}
</script>

<style scoped>
.enterprise-card {
  transition: all 0.3s ease;
}

.enterprise-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-content p {
  margin: 8px 0;
  color: #666;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
}
</style>
```

### 7.2 数据输入表单组件
```vue
<!-- DataInputForm.vue -->
<template>
  <n-form ref="formRef" :model="formData" :rules="rules">
    <n-grid :cols="2" :x-gap="24">
      <n-form-item-grid-item 
        v-for="field in fields"
        :key="field.key"
        :label="field.label"
        :path="field.key"
      >
        <component
          :is="getFieldComponent(field.type)"
          v-model:value="formData[field.key]"
          v-bind="getFieldProps(field)"
          @update:value="handleFieldChange(field.key, $event)"
        />
        
        <!-- 标准对比显示 -->
        <StandardComparison
          v-if="field.showComparison && formData[field.key]"
          :value="formData[field.key]"
          :standard="getStandard(field.key)"
          class="mt-2"
        />
      </n-form-item-grid-item>
    </n-grid>
  </n-form>
</template>

<script setup>
const props = defineProps({
  fields: {
    type: Array,
    required: true
  },
  modelValue: {
    type: Object,
    required: true
  },
  standards: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue', 'fieldChange'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const getFieldComponent = (type) => {
  const components = {
    input: 'n-input',
    number: 'n-input-number',
    select: 'n-select',
    date: 'n-date-picker',
    textarea: 'n-input'
  }
  return components[type] || 'n-input'
}

const getFieldProps = (field) => {
  const props = {}
  if (field.options) props.options = field.options
  if (field.placeholder) props.placeholder = field.placeholder
  if (field.min !== undefined) props.min = field.min
  if (field.max !== undefined) props.max = field.max
  return props
}

const handleFieldChange = (key, value) => {
  emit('fieldChange', { key, value })
}
</script>
```

## 8. 页面设计规范

### 8.1 布局规范
- 使用 `CommonPage` 组件作为页面容器
- 采用卡片式布局，每个功能模块独立成卡片
- 使用 `n-grid` 实现响应式布局
- 保持统一的间距和边距

### 8.2 交互规范
- 所有操作按钮使用 `n-button` 组件
- 表单验证使用 `n-form` 和 `n-form-item`
- 数据展示使用 `n-data-table` 或 `n-card`
- 弹窗操作使用 `CrudModal` 组件

### 8.3 样式规范
```scss
// PCB模块专用样式
.pcb-module {
  .enterprise-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
  }
  
  .audit-progress {
    margin: 20px 0;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 8px;
  }
  
  .data-input-section {
    .form-item {
      margin-bottom: 20px;
    }
    
    .standard-comparison {
      margin-top: 8px;
      padding: 8px;
      background: #f0f0f0;
      border-radius: 4px;
    }
  }
  
  .scheme-library {
    .scheme-item {
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 16px;
      
      &:hover {
        border-color: #1890ff;
        box-shadow: 0 2px 8px rgba(24, 144, 255, 0.1);
      }
    }
  }
}
```

## 9. 开发规范

### 9.1 代码规范
- 使用 Vue 3 Composition API
- 组件命名采用 PascalCase
- 文件名采用 kebab-case
- 使用 TypeScript 进行类型检查
- 遵循 ESLint 和 Prettier 规范

### 9.2 组件开发规范
```vue
<template>
  <!-- 模板内容 -->
</template>

<script setup>
// 1. 导入依赖
import { ref, computed, watch, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'

// 2. 定义 Props
const props = defineProps({
  // props 定义
})

// 3. 定义 Emits
const emit = defineEmits(['event1', 'event2'])

// 4. 响应式数据
const data = ref('')

// 5. 计算属性
const computedValue = computed(() => {
  // 计算逻辑
})

// 6. 方法定义
const handleClick = () => {
  // 处理逻辑
}

// 7. 生命周期
onMounted(() => {
  // 初始化逻辑
})
</script>

<style scoped>
/* 组件样式 */
</style>
```

### 9.3 API 调用规范
```javascript
// 使用 async/await 处理异步操作
const fetchData = async () => {
  try {
    loading.value = true
    const response = await pcbApi.getEnterpriseList(params.value)
    data.value = response.data
  } catch (error) {
    console.error('获取数据失败:', error)
    window.$message.error('获取数据失败')
  } finally {
    loading.value = false
  }
}
```

### 9.4 错误处理规范
- 所有 API 调用都要进行错误处理
- 使用 `window.$message` 显示用户友好的错误信息
- 记录详细的错误日志用于调试
- 提供重试机制

### 9.5 性能优化规范
- 使用 `v-memo` 优化列表渲染
- 合理使用 `computed` 和 `watch`
- 避免在模板中使用复杂计算
- 使用懒加载加载组件

## 10. 部署和测试

### 10.1 开发环境启动
```bash
# 前端开发
cd web
npm install
npm run dev

# 后端开发
cd app
pip install -r requirements.txt
python run.py
```

### 10.2 构建部署
```bash
# 前端构建
cd web
npm run build

# 后端部署
# 使用 Docker 或直接部署
```

### 10.3 测试规范
- 单元测试：使用 Vitest 测试组件逻辑
- 集成测试：测试 API 接口
- E2E 测试：使用 Playwright 测试用户流程

---

## 总结

本开发文档详细描述了PCB行业清洁生产云审核模块的完整设计方案，包括：

1. **模块架构**：基于Vue 3 + FastAPI的前后端分离架构
2. **功能设计**：涵盖企业管理、审核流程、数据评估、方案库、报告生成等完整功能
3. **技术实现**：详细的路由配置、API设计、数据模型和组件设计
4. **开发规范**：统一的代码规范、组件规范和性能优化指导

该文档为PCB模块的开发提供了完整的技术指导，确保开发过程规范、高效，最终交付高质量的产品。



