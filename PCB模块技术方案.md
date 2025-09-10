# PCB行业清洁生产云审核模块技术方案

## 目录

- [1. 模块概述](#1-模块概述)
- [2. 技术架构](#2-技术架构)
- [3. 路由配置](#3-路由配置)
- [4. 页面组件设计](#4-页面组件设计)
- [5. 数据模型设计](#5-数据模型设计)
- [6. API接口设计](#6-api接口设计)
- [7. 组件开发规范](#7-组件开发规范)
- [8. 开发实施计划](#8-开发实施计划)

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
- 采用前后端分离架构，仅开发前端界面
- 使用Vue原生组件和Naive UI组件库
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
  "图标库": "Carbon Icons",
  "图表库": "ECharts",
  "构建工具": "Vite",
  "CSS框架": "UnoCSS"
}
```

### 2.2 项目结构

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

## 3. 路由配置

### 3.1 PCB模块路由结构

基于现有的 `web/src/router/modules/cloudAudit.js`，扩展PCB模块的路由配置：

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

## 4. 页面组件设计

### 4.1 PCB首页（企业列表管理）

#### 4.1.1 页面结构

```vue
<!-- web/src/views/cloud-audit/pcb/index.vue -->
<template>
  <CommonPage title="PCB行业清洁生产审核">
    <!-- 搜索和操作栏 -->
    <div class="search-bar mb-4">
      <n-space>
        <n-input 
          v-model:value="searchKeyword" 
          placeholder="请输入企业名称"
          clearable
          style="width: 300px"
        />
        <n-button type="primary" @click="showCreateModal = true">
          <template #icon>
            <TheIcon icon="carbon:add" />
          </template>
          创建企业
        </n-button>
      </n-space>
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

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NButton, NInput, NSpace } from 'naive-ui'
import CommonPage from '@/components/page/CommonPage.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import TheIcon from '@/components/icon/TheIcon.vue'
import EnterpriseCard from './components/EnterpriseCard.vue'
import EnterpriseForm from './components/EnterpriseForm.vue'
import { pcbApi } from '@/api/modules/pcb'

defineOptions({ name: 'PCB行业审核' })

const router = useRouter()
const searchKeyword = ref('')
const showCreateModal = ref(false)
const isEdit = ref(false)
const currentEnterprise = ref({})
const enterprises = ref([])

// 获取企业列表
const fetchEnterprises = async () => {
  try {
    const response = await pcbApi.getEnterpriseList({
      search: searchKeyword.value
    })
    enterprises.value = response.data
  } catch (error) {
    console.error('获取企业列表失败:', error)
  }
}

// 查看企业详情
const handleView = (id) => {
  router.push(`/cloud-audit/pcb/${id}/basic-info`)
}

// 编辑企业
const handleEdit = (enterprise) => {
  isEdit.value = true
  currentEnterprise.value = { ...enterprise }
  showCreateModal.value = true
}

// 删除企业
const handleDelete = async (id) => {
  try {
    await $dialog.confirm({
      title: '确认删除',
      content: '确定要删除该企业吗？'
    })
    await pcbApi.deleteEnterprise(id)
    $message.success('删除成功')
    fetchEnterprises()
  } catch (error) {
    console.error('删除失败:', error)
  }
}

// 保存企业
const handleSave = async () => {
  try {
    if (isEdit.value) {
      await pcbApi.updateEnterprise(currentEnterprise.value.id, currentEnterprise.value)
    } else {
      await pcbApi.createEnterprise(currentEnterprise.value)
    }
    $message.success('保存成功')
    showCreateModal.value = false
    fetchEnterprises()
  } catch (error) {
    console.error('保存失败:', error)
  }
}

onMounted(() => {
  fetchEnterprises()
})
</script>

<style scoped>
.enterprise-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}
</style>
```

### 4.2 企业详情页面

#### 4.2.1 整体布局设计

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/index.vue -->
<template>
  <div class="enterprise-detail">
    <!-- 顶部导航栏 -->
    <div class="top-nav mb-4">
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
      class="mb-4"
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

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { NButton, NBreadcrumb, NBreadcrumbItem, NTabs, NTabPane } from 'naive-ui'
import AuditProgress from '../components/AuditProgress.vue'
import BasicInfo from './basic-info.vue'
import Planning from './planning.vue'
import PreAudit from './pre-audit.vue'
import Audit from './audit.vue'
import SchemeLibrary from './scheme-library.vue'
import Report from './report.vue'
import { pcbApi } from '@/api/modules/pcb'

defineOptions({ name: 'PCB企业详情' })

const route = useRoute()
const router = useRouter()
const enterpriseId = computed(() => route.params.id)
const activeTab = ref('basic-info')
const enterprise = ref({})
const currentStep = ref(0)

const auditSteps = [
  { title: '企业信息', description: '基本信息录入' },
  { title: '筹划与组织', description: '审核团队组建' },
  { title: '预审核', description: '数据填报评估' },
  { title: '审核', description: '指标审核' },
  { title: '审核报告', description: '报告生成' },
  { title: '方案库', description: '整改方案' }
]

// 获取企业信息
const fetchEnterprise = async () => {
  try {
    const response = await pcbApi.getEnterpriseDetail(enterpriseId.value)
    enterprise.value = response.data
  } catch (error) {
    console.error('获取企业信息失败:', error)
  }
}

onMounted(() => {
  fetchEnterprise()
})
</script>

<style scoped>
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #e0e0e0;
}
</style>
```

### 4.3 企业卡片组件

```vue
<!-- web/src/views/cloud-audit/pcb/components/EnterpriseCard.vue -->
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
import { NButton, NCard, NTag } from 'naive-ui'

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

### 4.4 审核进度组件

```vue
<!-- web/src/views/cloud-audit/pcb/components/AuditProgress.vue -->
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
import { NSteps, NStep } from 'naive-ui'

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

const status = computed(() => {
  if (props.currentStep === props.steps.length - 1) return 'finish'
  return 'process'
})
</script>

<style scoped>
.audit-progress {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}
</style>
```

### 4.5 预审核模块（核心功能）

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/pre-audit.vue -->
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

<script setup>
import { ref, computed, onMounted } from 'vue'
import { NButton, NCard, NForm, NFormItem, NGrid, NFormItemGridItem, NInputNumber, NStatistic } from 'naive-ui'
import StandardComparison from '../components/StandardComparison.vue'
import { pcbApi } from '@/api/modules/pcb'

defineOptions({ name: 'PCB预审核' })

const props = defineProps({
  enterpriseId: {
    type: String,
    required: true
  }
})

const formData = ref({})
const standards = ref({})
const levelCounts = ref({
  level1: 0,
  level2: 0,
  level3: 0,
  unqualified: 0
})

// 获取预审核数据
const fetchPreAuditData = async () => {
  try {
    const response = await pcbApi.getPreAuditData(props.enterpriseId)
    formData.value = response.data
  } catch (error) {
    console.error('获取预审核数据失败:', error)
  }
}

// 获取审核标准
const fetchStandards = async () => {
  try {
    const response = await pcbApi.getAuditStandards()
    standards.value = response.data
  } catch (error) {
    console.error('获取审核标准失败:', error)
  }
}

// 数据变化处理
const handleDataChange = (key, value) => {
  formData.value[key] = value
  // 实时计算评估结果
  calculateAssessment()
}

// 计算评估结果
const calculateAssessment = () => {
  // 根据标准计算各等级指标数量
  // 这里需要根据具体的评估逻辑实现
}

onMounted(() => {
  fetchPreAuditData()
  fetchStandards()
})
</script>
```

### 4.6 标准对比组件

```vue
<!-- web/src/views/cloud-audit/pcb/components/StandardComparison.vue -->
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
import { computed } from 'vue'
import { NTag } from 'naive-ui'

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

## 5. 数据模型设计

### 5.1 前端数据模型

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

## 6. API接口设计

### 6.1 PCB企业管理API

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

## 7. 组件开发规范

### 7.1 代码规范

- 使用 Vue 3 Composition API
- 组件命名采用 PascalCase
- 文件名采用 kebab-case
- 使用 TypeScript 进行类型检查
- 遵循 ESLint 和 Prettier 规范

### 7.2 组件开发规范

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

### 7.3 API 调用规范

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

### 7.4 错误处理规范

- 所有 API 调用都要进行错误处理
- 使用 `window.$message` 显示用户友好的错误信息
- 记录详细的错误日志用于调试
- 提供重试机制

## 8. 开发实施计划

### 8.1 开发阶段划分

#### 第一阶段：基础框架搭建（1-2天）

- [ ] 创建PCB模块目录结构
- [ ] 配置路由和导航
- [ ] 创建基础页面框架
- [ ] 搭建API接口结构

#### 第二阶段：核心功能开发（3-5天）

- [ ] 企业列表管理页面
- [ ] 企业详情页面布局
- [ ] 企业基本信息模块
- [ ] 审核进度组件

#### 第三阶段：审核流程开发（4-6天）

- [ ] 筹划与组织模块
- [ ] 预审核数据填报模块
- [ ] 标准对比组件
- [ ] 审核模块

#### 第四阶段：高级功能开发（3-4天）

- [ ] 方案库管理
- [ ] 报告生成和编辑
- [ ] 数据导出功能
- [ ] 图表可视化

#### 第五阶段：测试和优化（2-3天）

- [ ] 功能测试
- [ ] 性能优化
- [ ] 用户体验优化
- [ ] 代码审查

### 8.2 开发注意事项

1. **前后端解耦**：所有数据交互通过API接口，不直接操作后端数据
2. **组件复用**：充分利用现有的通用组件（CommonPage、CrudTable、CrudModal等）
3. **响应式设计**：确保在不同屏幕尺寸下都能正常显示
4. **错误处理**：完善的错误处理和用户提示机制
5. **性能优化**：合理使用Vue的响应式特性，避免不必要的重渲染

### 8.3 技术要点

1. **路由管理**：使用Vue Router的嵌套路由实现企业详情的多标签页
2. **状态管理**：使用Pinia管理全局状态，本地状态使用ref/reactive
3. **组件通信**：父子组件通过props/emit，跨组件使用provide/inject
4. **数据验证**：使用Naive UI的表单验证功能
5. **图表展示**：使用ECharts展示审核数据和统计图表9. 单页面应用实现方案

### 9.1 页面布局优化

为了实现在同一页面内完成所有PCB模块的操作，我们需要对页面布局进行优化，采用条件渲染的方式切换不同视图：

```vue
<!-- 优化后的页面布局结构 -->
<template>
  <CommonPage title="PCB行业清洁生产审核">
    <!-- 企业列表视图 -->
    <div v-if="!currentEnterprise" class="enterprise-list">
      <!-- 搜索和操作栏 -->
      <div class="search-bar mb-4">
        <n-space>
          <n-input 
            v-model:value="searchKeyword" 
            placeholder="请输入企业名称/地市/区县"
            clearable
            style="width: 300px"
          />
          <n-button type="primary" @click="showCreateModal = true">
            创建企业
          </n-button>
        </n-space>
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
    </div>

    <!-- 企业详情视图 -->
    <div v-else class="enterprise-detail">
      <!-- 返回按钮和企业名称 -->
      <div class="detail-header mb-4">
        <n-space align="center">
          <n-button @click="handleBack" size="small">返回列表</n-button>
          <n-divider vertical />
          <h3>{{ currentEnterprise.name }}</h3>
        </n-space>
      </div>

      <!-- 审核进度条 -->
      <AuditProgress 
        :current-step="currentStep"
        :steps="auditSteps"
        class="mb-4"
        @step-click="handleStepClick"
      />
  
      <!-- 模块内容区域 -->
      <n-tabs 
        v-model:value="activeTab" 
        type="line"
        @update:value="handleTabChange"
      >
        <n-tab-pane name="basic-info" tab="企业信息">
          <keep-alive>
            <BasicInfo 
              :enterprise-id="currentEnterprise.id" 
              @update="handleInfoUpdate"
            />
          </keep-alive>
        </n-tab-pane>
        <!-- 其他模块标签页 -->
      </n-tabs>
    </div>
  </CommonPage>
</template>
```

### 9.2 状态管理设计

采用Vue 3的组合式API进行状态管理：

```javascript
// 状态定义
const currentEnterprise = ref(null)
const activeTab = ref('basic-info')
const currentStep = ref(0)

// 视图切换逻辑
const handleView = (enterprise) => {
  currentEnterprise.value = enterprise
  activeTab.value = 'basic-info'
  currentStep.value = 0
  // 缓存当前状态
  cacheCurrentState()
}

// 返回列表
const handleBack = () => {
  currentEnterprise.value = null
  activeTab.value = 'basic-info'
  currentStep.value = 0
  clearCache()
}

// 状态缓存管理
const cacheCurrentState = () => {
  sessionStorage.setItem('pcb_current_state', JSON.stringify({
    enterprise: currentEnterprise.value,
    tab: activeTab.value,
    step: currentStep.value
  }))
}

const restoreState = () => {
  const cached = sessionStorage.getItem('pcb_current_state')
  if (cached) {
    const state = JSON.parse(cached)
    currentEnterprise.value = state.enterprise
    activeTab.value = state.tab
    currentStep.value = state.step
  }
}
```

### 9.3 模块导航优化

改进审核进度组件，支持模块直接导航：

```vue
<!-- AuditProgress.vue -->
<template>
  <div class="audit-progress">
    <n-steps
      :current="currentStep"
      :status="status"
      size="small"
    >
      <n-step
        v-for="(step, index) in steps"
        :key="index"
        :title="step.title"
        :description="step.description"
        @click="handleStepClick(step, index)"
        class="cursor-pointer"
      >
        <template #icon>
          <n-icon>
            <component :is="getStepIcon(index)" />
          </n-icon>
        </template>
      </n-step>
    </n-steps>
  </div>
</template>

<script setup>
const emit = defineEmits(['step-click'])

const handleStepClick = (step, index) => {
  emit('step-click', { ...step, index })
}
</script>
```

### 9.4 性能优化策略

1. **组件缓存**：

```vue
<keep-alive>
  <component :is="currentModule" />
</keep-alive>
```

2. **数据预加载**：

```javascript
// 预加载下一个模块的数据
const preloadNextModule = (currentIndex) => {
  const nextModule = auditSteps[currentIndex + 1]
  if (nextModule) {
    fetchModuleData(nextModule.key)
  }
}
```

3. **延迟加载**：

```javascript
// 使用动态导入延迟加载模块
const modules = {
  'basic-info': () => import('./modules/BasicInfo.vue'),
  'planning': () => import('./modules/Planning.vue'),
  'pre-audit': () => import('./modules/PreAudit.vue'),
  // ...其他模块
}
```

### 9.5 用户体验优化

1. **状态保持**：

```javascript
// 使用 URL 查询参数保持状态
const updateUrlState = () => {
  router.push({
    query: {
      ...(currentEnterprise.value ? { id: currentEnterprise.value.id } : {}),
      ...(activeTab.value !== 'basic-info' ? { tab: activeTab.value } : {})
    }
  })
}
```

2. **过渡动画**：

```vue
<template>
  <transition name="fade" mode="out-in">
    <component :is="currentView" />
  </transition>
</template>

<style>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
```

3. **加载状态**：

```javascript
const loading = ref(false)

const switchModule = async (module) => {
  loading.value = true
  try {
    await loadModuleData(module)
  } finally {
    loading.value = false
  }
}
```

### 9.6 实现要点

1. **前后端分离**：

- 所有数据交互通过mock API进行
- 不直接操作后端数据
- 统一的数据接口规范

2. **Vue自带组件使用**：

- 使用 `<component>`动态组件
- 使用 `<transition>`过渡效果
- 使用 `<keep-alive>`缓存组件

3. **状态管理**：

- 使用 `ref`和 `reactive`管理本地状态
- 使用 `provide/inject`进行跨组件通信
- 使用 `sessionStorage`进行状态持久化

4. **错误处理**：

- 统一的错误处理机制
- 友好的错误提示
- 自动重试机制

5. **性能优化**：

- 组件懒加载
- 数据预加载
- 状态缓存

这个优化方案完全基于Vue 3的特性，保持了前后端分离的原则，并充分利用了Vue自带的组件和功能。通过这种方式，我们可以在同一个页面内完成所有PCB模块的操作，提供更流畅的用户体验。

## 总结

本技术方案详细描述了PCB行业清洁生产云审核模块的完整开发方案，包括：

1. **模块架构**：基于Vue 3 + Naive UI的前端架构
2. **功能设计**：涵盖企业管理、审核流程、数据评估、方案库、报告生成等完整功能
3. **技术实现**：详细的路由配置、组件设计、数据模型和API设计
4. **开发规范**：统一的代码规范、组件规范和性能优化指导
5. **实施计划**：分阶段的开发计划和注意事项

该方案确保PCB模块的开发过程规范、高效，最终交付高质量的前端产品，同时保持与现有系统的良好集成。
