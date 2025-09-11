# PCB行业清洁生产云审核模块具体内容技术方案

## 目录

- [1. 模块概述](#1-模块概述)
- [2. 预审核模块详细设计](#2-预审核模块详细设计)
- [3. 审核模块详细设计](#3-审核模块详细设计)
- [4. 方案库模块详细设计](#4-方案库模块详细设计)
- [5. API接口详细设计](#5-api接口详细设计)
- [6. 数据模型详细设计](#6-数据模型详细设计)
- [7. 组件开发规范](#7-组件开发规范)
- [8. 实施计划](#8-实施计划)

## 1. 模块概述

### 1.1 技术架构
- **前端框架**: Vue 3 + Composition API
- **UI组件库**: Naive UI
- **状态管理**: Pinia
- **路由管理**: Vue Router 4.x
- **HTTP客户端**: Axios
- **图标库**: Carbon Icons
- **构建工具**: Vite
- **CSS框架**: UnoCSS

### 1.2 开发原则
- **前后端解耦**: 所有数据交互通过API接口，不直接操作后端数据
- **组件化设计**: 优先复用通用组件，创建专用业务组件
- **响应式设计**: 支持多端访问，确保用户体验一致
- **模块化开发**: 每个功能模块独立开发，便于维护和扩展

## 2. 预审核模块详细设计

### 2.1 页面布局重构

基于PCB具体内容指南，预审核模块需要完全重构，采用折叠面板布局：

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/pre-audit.vue -->
<template>
  <div class="pre-audit-page p-4">
    <n-spin :show="loading">
      <n-form ref="formRef" :model="formData">
        <n-collapse default-expanded-names="1" accordion>
          <n-collapse-item title="1. 企业总体生产情况" name="1">
            <ProductionInfoForm v-model="formData.productionInfo" />
          </n-collapse-item>
          <n-collapse-item title="2. 原辅材料使用情况" name="2">
            <RawMaterialForm v-model="formData.rawMaterials" />
          </n-collapse-item>
          <n-collapse-item title="3. 主要工艺及装备使用" name="3">
            <ProcessEquipmentForm v-model="formData.processEquipment" />
          </n-collapse-item>
          <n-collapse-item title="4. 资源能源消耗" name="4">
            <ResourceConsumptionForm v-model="formData.resourceConsumption" />
          </n-collapse-item>
          <n-collapse-item title="5. 污染防治" name="5">
            <PollutionControlForm v-model="formData.pollutionControl" />
          </n-collapse-item>
          <n-collapse-item title="6. 工业固体废物管理" name="6">
            <SolidWasteForm v-model="formData.solidWaste" />
          </n-collapse-item>
          <n-collapse-item title="7. 自行监测情况" name="7">
            <SelfMonitoringForm v-model="formData.selfMonitoring" />
          </n-collapse-item>
        </n-collapse>
      </n-form>
      <n-space justify="center" class="mt-6">
        <n-button @click="handleSaveDraft">保存草稿</n-button>
        <n-button type="primary" @click="handleSubmit">提交审核</n-button>
      </n-space>
    </n-spin>
  </div>
</template>
```

### 2.2 核心子组件设计

#### 2.2.1 企业总体生产情况组件

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/components/ProductionInfoForm.vue -->
<template>
  <div class="production-info-form">
    <n-form-item label="产能（万m²/年）">
      <n-input-number 
        v-model:value="formData.capacity"
        placeholder="请输入年产能"
        :min="0"
        :precision="2"
      />
    </n-form-item>
    
    <n-tabs type="line" class="mt-4">
      <n-tab-pane 
        v-for="year in years" 
        :key="year" 
        :name="year" 
        :tab="`${year}年产量`"
      >
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi 
            v-for="type in productionTypes" 
            :key="type.key"
            :label="type.label"
          >
            <n-input-number 
              v-model:value="formData.output[year][type.key]"
              placeholder="请输入产量"
              :min="0"
              :precision="2"
            />
          </n-form-item-gi>
        </n-grid>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { NFormItem, NInputNumber, NTabs, NTabPane, NGrid, NFormItemGi } from 'naive-ui'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      capacity: null,
      output: {
        '2022': {},
        '2023': {},
        '2024': {}
      }
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const years = ['2022', '2023', '2024']
const productionTypes = [
  { key: 'rigidSingle', label: '刚性单面板' },
  { key: 'rigidDouble', label: '刚性双面板' },
  { key: 'rigidMultilayer', label: '刚性多层板' },
  { key: 'flexibleSingle', label: '挠性单面板' },
  { key: 'flexibleDouble', label: '挠性双面板' },
  { key: 'flexibleMultilayer', label: '挠性多层板' }
]
</script>
```

#### 2.2.2 原辅材料使用情况组件

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/components/RawMaterialForm.vue -->
<template>
  <div class="raw-material-form">
    <n-data-table
      :columns="columns"
      :data="formData"
      :row-key="row => row.id"
      :pagination="false"
    >
      <template #year="{ row, index }">
        <n-select
          v-model:value="row.year"
          :options="yearOptions"
          placeholder="选择年份"
        />
      </template>
      <template #name="{ row, index }">
        <n-input
          v-model:value="row.name"
          placeholder="请输入材料名称"
        />
      </template>
      <template #unit="{ row, index }">
        <n-select
          v-model:value="row.unit"
          :options="unitOptions"
          placeholder="选择单位"
        />
      </template>
      <template #process="{ row, index }">
        <n-select
          v-model:value="row.process"
          :options="processOptions"
          placeholder="选择工序"
        />
      </template>
      <template #amount="{ row, index }">
        <n-input-number
          v-model:value="row.amount"
          placeholder="请输入用量"
          :min="0"
          :precision="2"
        />
      </template>
      <template #state="{ row, index }">
        <n-select
          v-model:value="row.state"
          :options="stateOptions"
          placeholder="选择状态"
        />
      </template>
      <template #voc="{ row, index }">
        <n-input-number
          v-model:value="row.voc"
          placeholder="请输入VOC含量"
          :min="0"
          :precision="2"
        />
      </template>
      <template #action="{ row, index }">
        <n-button 
          size="small" 
          type="error"
          @click="removeRow(index)"
        >
          删除
        </n-button>
      </template>
    </n-data-table>
    
    <n-button type="primary" class="mt-4" @click="addRow">
      添加一行
    </n-button>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { NDataTable, NButton, NInput, NInputNumber, NSelect } from 'naive-ui'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const columns = [
  { title: '年份', key: 'year', width: 100 },
  { title: '材料名称', key: 'name', width: 150 },
  { title: '单位', key: 'unit', width: 80 },
  { title: '工序', key: 'process', width: 120 },
  { title: '用量', key: 'amount', width: 120 },
  { title: '状态', key: 'state', width: 100 },
  { title: 'VOC含量(%)', key: 'voc', width: 120 },
  { title: '操作', key: 'action', width: 80 }
]

const yearOptions = [
  { label: '2022', value: 2022 },
  { label: '2023', value: 2023 },
  { label: '2024', value: 2024 }
]

const unitOptions = [
  { label: 'm²', value: 'm²' },
  { label: 'kg', value: 'kg' },
  { label: 'L', value: 'L' },
  { label: 't', value: 't' }
]

const processOptions = [
  { label: '开料', value: '开料' },
  { label: '钻孔', value: '钻孔' },
  { label: '电镀', value: '电镀' },
  { label: '蚀刻', value: '蚀刻' },
  { label: '阻焊', value: '阻焊' },
  { label: '丝印', value: '丝印' }
]

const stateOptions = [
  { label: '固体', value: '固体' },
  { label: '液体', value: '液体' },
  { label: '气体', value: '气体' }
]

const addRow = () => {
  formData.value.push({
    id: Date.now(),
    year: 2023,
    name: '',
    unit: '',
    process: '',
    amount: null,
    state: '',
    voc: 0
  })
}

const removeRow = (index) => {
  formData.value.splice(index, 1)
}
</script>
```

### 2.3 数据模型设计

```javascript
// web/src/types/pcb-pre-audit.js
export const PreAuditDataModel = {
  // 企业总体生产情况
  productionInfo: {
    capacity: Number, // 产能（万m²/年）
    output: {
      '2022': {
        rigidSingle: Number,
        rigidDouble: Number,
        rigidMultilayer: Number,
        flexibleSingle: Number,
        flexibleDouble: Number,
        flexibleMultilayer: Number
      },
      '2023': { /* 同上 */ },
      '2024': { /* 同上 */ }
    }
  },
  
  // 原辅材料使用情况
  rawMaterials: [
    {
      id: Number,
      year: Number,
      name: String,
      unit: String,
      process: String,
      amount: Number,
      state: String,
      voc: Number
    }
  ],
  
  // 主要工艺及装备使用
  processEquipment: {
    rigid: {
      single: { line: String, process: String, equipment: String },
      double: { line: String, process: String, equipment: String },
      multilayer: { line: String, process: String, equipment: String }
    },
    flexible: {
      single: { line: String, process: String, equipment: String },
      double: { line: String, process: String, equipment: String },
      multilayer: { line: String, process: String, equipment: String }
    }
  },
  
  // 资源能源消耗
  resourceConsumption: {
    water: [
      { year: Number, type: String, amount: Number, source: String }
    ],
    electricity: [
      { year: Number, type: String, amount: Number, source: String }
    ],
    gas: [
      { year: Number, type: String, amount: Number, source: String }
    ]
  },
  
  // 污染防治
  pollutionControl: {
    copperRecovery: [
      { year: Number, amount: Number }
    ],
    waterReuseRate: [
      { year: Number, rate: Number }
    ],
    gasEmission: [
      { process: String, category: String, method: String }
    ],
    waterEmission: [
      { process: String, category: String, method: String }
    ]
  },
  
  // 工业固体废物管理
  solidWaste: {
    general: [
      { year: Number, name: String, type: String, amount: Number }
    ],
    hazardous: [
      { year: Number, name: String, type: String, code: String, amount: Number }
    ]
  },
  
  // 自行监测情况
  selfMonitoring: {
    organizedGas: {
      item: String,
      concentration: Number,
      point: String,
      standard: String,
      reportFileId: String
    },
    wastewater: {
      item: String,
      concentration: Number,
      point: String,
      standard: String,
      reportFileId: String
    },
    noise: {
      item: String,
      level: Number,
      point: String,
      standard: String,
      reportFileId: String
    }
  }
}
```

## 3. 审核模块详细设计

### 3.1 页面布局重构

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/audit.vue -->
<template>
  <div class="audit-page p-4">
    <n-card title="审核结果总览" class="mb-4">
      <!-- 汇总统计 -->
      <n-grid :cols="4" :x-gap="16" class="mb-4">
        <n-gi><n-statistic label="最终得分" :value="summary.totalScore.toFixed(2)" /></n-gi>
        <n-gi><n-statistic label="综合等级">
          <n-tag :type="getLevelTagType(summary.overallLevel)">{{ summary.overallLevel }}</n-tag>
        </n-statistic></n-gi>
        <n-gi><n-statistic label="待改进项数" :value="summary.improvementItems" /></n-gi>
        <n-gi><n-statistic label="限定性指标" :value="summary.limitingIndicators" /></n-gi>
      </n-grid>
      <!-- ECharts 雷达图 -->
      <div ref="radarChart" style="width: 100%; height: 300px;"></div>
    </n-card>

    <!-- 详细审核表 -->
    <n-data-table
      :columns="columns"
      :data="auditTreeData"
      :row-key="row => row.id"
      default-expand-all
      :pagination="false"
    />
    
    <!-- 推荐方案弹窗 -->
    <n-modal v-model:show="showSchemeModal">
      <n-card style="width: 600px" title="推荐改进方案">
        <div v-for="scheme in currentSchemes" :key="scheme.id" class="mb-2">
          <strong>{{ scheme.name }}:</strong> {{ scheme.description }}
        </div>
      </n-card>
    </n-modal>
  </div>
</template>
```

### 3.2 64项指标审核逻辑

```javascript
// web/src/utils/pcb-audit-logic.js
export const auditLogic = {
  // 指标1-6: 生产工艺与装备要求（定性判断）
  processEquipment: {
    type: 'qualitative',
    options: [
      { value: 'I级', label: 'I级', description: '采用国际先进工艺和设备' },
      { value: 'II级', label: 'II级', description: '采用国内先进工艺和设备' },
      { value: 'III级', label: 'III级', description: '采用一般工艺和设备' },
      { value: '不达标', label: '不达标', description: '工艺和设备落后' }
    ],
    render: (row) => {
      return h('n-select', {
        value: row.level,
        options: auditLogic.processEquipment.options,
        onUpdateValue: (value) => updateIndicatorLevel(row.id, value)
      })
    }
  },

  // 指标7-14: 单位产品电耗（定量计算与自动评估）
  unitPowerConsumption: {
    type: 'quantitative',
    formula: '总电耗 / 总产量',
    standards: {
      rigid: { level1: 100, level2: 150, level3: 200 },
      flexible: { level1: 80, level2: 120, level3: 160 }
    },
    calculate: (preAuditData) => {
      const totalPower = preAuditData.resourceConsumption.electricity
        .reduce((sum, item) => sum + item.amount, 0)
      const totalOutput = Object.values(preAuditData.productionInfo.output['2023'])
        .reduce((sum, output) => sum + output, 0)
      return totalPower / totalOutput
    },
    evaluate: (value, productType) => {
      const standard = auditLogic.unitPowerConsumption.standards[productType]
      if (value <= standard.level1) return 'I级'
      if (value <= standard.level2) return 'II级'
      if (value <= standard.level3) return 'III级'
      return '不达标'
    }
  },

  // 指标54: 环保法律法规执行情况（限定性指标）
  environmentalCompliance: {
    type: 'limiting',
    isCompliant: false,
    render: (row) => {
      return h('n-switch', {
        value: row.isCompliant,
        onUpdateValue: (value) => {
          if (!value) {
            window.$dialog.warning({
              title: '限定性指标警告',
              content: '环保法律法规执行情况不达标，总评级不得高于III级',
              positiveText: '确认'
            })
          }
          updateIndicatorLevel(row.id, value ? 'I级' : '不达标')
        }
      })
    }
  }
}

// 审核数据处理函数
export const processAuditData = (preAuditData) => {
  const auditResults = []
  
  // 处理定量指标
  Object.keys(auditLogic).forEach((key, index) => {
    const logic = auditLogic[key]
    if (logic.type === 'quantitative') {
      const value = logic.calculate(preAuditData)
      const level = logic.evaluate(value)
      auditResults.push({
        id: index + 1,
        name: getIndicatorName(index + 1),
        currentValue: value,
        level: level,
        recommendedSchemes: getRecommendedSchemes(index + 1, level)
      })
    }
  })
  
  return auditResults
}
```

### 3.3 改进措施推荐逻辑

```javascript
// web/src/utils/scheme-recommendation.js
export const getRecommendedSchemes = (indicatorId, level) => {
  if (level === 'I级') return []
  
  // 从方案库中获取关联该指标的方案
  const schemes = schemeLibrary.filter(scheme => 
    scheme.indicatorIds.includes(indicatorId)
  )
  
  return schemes.map(scheme => ({
    id: scheme.id,
    name: scheme.name,
    description: scheme.description,
    investment: scheme.investment,
    paybackPeriod: scheme.paybackPeriod
  }))
}
```

## 4. 方案库模块详细设计

### 4.1 页面布局优化

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/scheme-library.vue -->
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
          <QueryBarItem label="方案名称">
            <n-input v-model:value="queryItems.name" placeholder="请输入方案名称" />
          </QueryBarItem>
          <QueryBarItem label="关联指标">
            <n-tree-select 
              v-model:value="queryItems.indicatorIds"
              :options="indicatorTreeOptions"
              multiple
              checkable
              placeholder="请选择关联指标"
            />
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

### 4.2 方案表单组件

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/components/SchemeForm.vue -->
<template>
  <n-form ref="formRef" :model="formData" :rules="rules">
    <n-form-item label="方案名称" path="name">
      <n-input v-model:value="formData.name" placeholder="请输入方案名称" />
    </n-form-item>
    
    <n-form-item label="方案类型" path="type">
      <n-select
        v-model:value="formData.type"
        :options="typeOptions"
        placeholder="请选择方案类型"
      />
    </n-form-item>
    
    <n-form-item label="关联指标" path="indicatorIds">
      <n-tree-select
        v-model:value="formData.indicatorIds"
        :options="indicatorTreeOptions"
        multiple
        checkable
        placeholder="请选择关联指标"
      />
    </n-form-item>
    
    <n-form-item label="方案描述" path="description">
      <n-input
        v-model:value="formData.description"
        type="textarea"
        placeholder="请输入方案描述"
        :rows="3"
      />
    </n-form-item>
    
    <n-form-item label="实施方案" path="implementation">
      <n-input
        v-model:value="formData.implementation"
        type="textarea"
        placeholder="请输入实施方案"
        :rows="4"
      />
    </n-form-item>
    
    <n-form-item label="预期效果" path="expectedEffect">
      <n-input
        v-model:value="formData.expectedEffect"
        type="textarea"
        placeholder="请输入预期效果"
        :rows="3"
      />
    </n-form-item>
    
    <n-form-item label="投资估算" path="investment">
      <n-input-number
        v-model:value="formData.investment"
        placeholder="请输入投资估算"
        :min="0"
        :precision="2"
      >
        <template #suffix>万元</template>
      </n-input-number>
    </n-form-item>
    
    <n-form-item label="投资回收期" path="paybackPeriod">
      <n-input-number
        v-model:value="formData.paybackPeriod"
        placeholder="请输入投资回收期"
        :min="0"
        :precision="1"
      >
        <template #suffix>年</template>
      </n-input-number>
    </n-form-item>
  </n-form>
</template>
```

### 4.3 指标树数据结构

```javascript
// web/src/data/pcb-indicators.js
export const indicatorTreeData = [
  {
    label: '生产工艺与装备要求',
    key: 'process',
    children: [
      { label: '刚性单面板生产工艺', key: '1' },
      { label: '刚性双面板生产工艺', key: '2' },
      { label: '刚性多层板生产工艺', key: '3' },
      { label: '挠性单面板生产工艺', key: '4' },
      { label: '挠性双面板生产工艺', key: '5' },
      { label: '挠性多层板生产工艺', key: '6' }
    ]
  },
  {
    label: '资源能源消耗',
    key: 'resource',
    children: [
      { label: '单位产品电耗', key: '7' },
      { label: '单位产品新鲜水耗', key: '15' },
      { label: '水资源重复利用率', key: '19' }
    ]
  },
  {
    label: '污染防治',
    key: 'pollution',
    children: [
      { label: '金属铜回收率', key: '28' },
      { label: '一般工业固体废物综合利用率', key: '29' },
      { label: '污染物产生量', key: '30' }
    ]
  }
]
```

## 5. API接口详细设计

### 5.1 预审核模块API

```javascript
// web/src/api/modules/pcb-pre-audit.js
export const preAuditApi = {
  // 获取预审核数据
  getPreAuditData: (enterpriseId) => 
    request.get(`/api/v1/pcb/enterprise/${enterpriseId}/pre-audit`),
  
  // 保存预审核数据
  savePreAuditData: (enterpriseId, data) => 
    request.post(`/api/v1/pcb/enterprise/${enterpriseId}/pre-audit`, data),
  
  // 提交预审核数据
  submitPreAuditData: (enterpriseId, data) => 
    request.put(`/api/v1/pcb/enterprise/${enterpriseId}/pre-audit/submit`, data),
  
  // 获取审核标准
  getAuditStandards: () => 
    request.get('/api/v1/pcb/standards'),
  
  // 文件上传
  uploadFile: (file) => 
    request.post('/api/v1/upload', file, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
}
```

### 5.2 审核模块API

```javascript
// web/src/api/modules/pcb-audit.js
export const auditApi = {
  // 获取审核数据
  getAuditData: (enterpriseId) => 
    request.get(`/api/v1/pcb/enterprise/${enterpriseId}/audit`),
  
  // 更新指标评级
  updateIndicatorLevel: (enterpriseId, indicatorId, level) => 
    request.put(`/api/v1/pcb/enterprise/${enterpriseId}/audit/indicator/${indicatorId}`, { level }),
  
  // 提交审核结果
  submitAuditResult: (enterpriseId, data) => 
    request.post(`/api/v1/pcb/enterprise/${enterpriseId}/audit/submit`, data),
  
  // 获取推荐方案
  getRecommendedSchemes: (enterpriseId, indicatorId) => 
    request.get(`/api/v1/pcb/enterprise/${enterpriseId}/audit/recommendations/${indicatorId}`),
  
  // 生成审核报告
  generateReport: (enterpriseId) => 
    request.get(`/api/v1/pcb/enterprise/${enterpriseId}/audit/report`)
}
```

### 5.3 方案库模块API

```javascript
// web/src/api/modules/pcb-scheme.js
export const schemeApi = {
  // 获取方案列表
  getSchemeList: (params) => 
    request.get('/api/v1/pcb/scheme', { params }),
  
  // 获取方案详情
  getSchemeDetail: (id) => 
    request.get(`/api/v1/pcb/scheme/${id}`),
  
  // 创建方案
  createScheme: (data) => 
    request.post('/api/v1/pcb/scheme', data),
  
  // 更新方案
  updateScheme: (id, data) => 
    request.put(`/api/v1/pcb/scheme/${id}`, data),
  
  // 删除方案
  deleteScheme: (id) => 
    request.delete(`/api/v1/pcb/scheme/${id}`),
  
  // 获取指标树数据
  getIndicatorTree: () => 
    request.get('/api/v1/pcb/indicators/tree'),
  
  // 根据指标获取关联方案
  getSchemesByIndicator: (indicatorId) => 
    request.get(`/api/v1/pcb/scheme/by-indicator/${indicatorId}`)
}
```

## 6. 数据模型详细设计

### 6.1 预审核数据模型

```javascript
// web/src/types/pcb-pre-audit.js
export const PreAuditDataModel = {
  enterpriseId: Number,
  productionInfo: {
    capacity: Number,
    output: Object
  },
  rawMaterials: Array,
  processEquipment: Object,
  resourceConsumption: Object,
  pollutionControl: Object,
  solidWaste: Object,
  selfMonitoring: Object,
  status: String, // 'draft', 'submitted', 'approved'
  createdAt: String,
  updatedAt: String
}
```

### 6.2 审核数据模型

```javascript
// web/src/types/pcb-audit.js
export const AuditDataModel = {
  enterpriseId: Number,
  indicators: [
    {
      id: Number,
      name: String,
      category: String,
      currentValue: Number,
      level: String, // 'I级', 'II级', 'III级', '不达标'
      score: Number,
      comment: String,
      recommendedSchemes: Array
    }
  ],
  summary: {
    totalScore: Number,
    overallLevel: String,
    improvementItems: Number,
    limitingIndicators: Number
  },
  status: String, // 'pending', 'in-progress', 'completed'
  auditorId: Number,
  auditDate: String,
  createdAt: String,
  updatedAt: String
}
```

### 6.3 方案库数据模型

```javascript
// web/src/types/pcb-scheme.js
export const SchemeModel = {
  id: Number,
  name: String,
  type: String,
  description: String,
  implementation: String,
  expectedEffect: String,
  investment: Number,
  paybackPeriod: Number,
  indicatorIds: Array,
  status: String, // 'active', 'inactive'
  createdAt: String,
  updatedAt: String
}
```

## 7. 组件开发规范

### 7.1 组件命名规范

- 组件文件使用 PascalCase：`ProductionInfoForm.vue`
- 组件名使用 PascalCase：`ProductionInfoForm`
- 组件目录使用 kebab-case：`enterprise-detail/`

### 7.2 组件结构规范

```vue
<template>
  <!-- 模板内容 -->
</template>

<script setup>
// 1. 导入依赖
import { ref, computed, watch, onMounted } from 'vue'
import { NButton, NInput } from 'naive-ui'

// 2. 定义组件名
defineOptions({ name: 'ComponentName' })

// 3. 定义 Props
const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

// 4. 定义 Emits
const emit = defineEmits(['update:modelValue', 'change'])

// 5. 响应式数据
const formData = ref({})

// 6. 计算属性
const computedValue = computed(() => {
  // 计算逻辑
})

// 7. 方法定义
const handleChange = () => {
  // 处理逻辑
}

// 8. 生命周期
onMounted(() => {
  // 初始化逻辑
})
</script>

<style scoped>
/* 组件样式 */
</style>
```

### 7.3 错误处理规范

```javascript
// 统一的错误处理
const handleApiCall = async (apiFunction, ...args) => {
  try {
    loading.value = true
    const response = await apiFunction(...args)
    return response.data
  } catch (error) {
    console.error('API调用失败:', error)
    window.$message.error(error.message || '操作失败')
    throw error
  } finally {
    loading.value = false
  }
}
```

## 8. 实施计划

### 8.1 开发阶段划分

#### 第一阶段：预审核模块重构（3-4天）
- [ ] 创建折叠面板布局
- [ ] 开发7个子表单组件
- [ ] 实现数据验证和保存
- [ ] 集成文件上传功能

#### 第二阶段：审核模块重构（4-5天）
- [ ] 实现64项指标审核逻辑
- [ ] 开发自动评估算法
- [ ] 集成ECharts雷达图
- [ ] 实现改进措施推荐

#### 第三阶段：方案库模块优化（2-3天）
- [ ] 优化方案管理界面
- [ ] 实现指标关联功能
- [ ] 完善搜索和筛选

#### 第四阶段：集成测试（2-3天）
- [ ] 模块间数据流转测试
- [ ] 用户体验优化
- [ ] 性能优化
- [ ] 错误处理完善

### 8.2 技术要点

1. **前后端解耦**：所有数据交互通过API接口
2. **组件复用**：充分利用现有通用组件
3. **状态管理**：使用Vue 3 Composition API
4. **性能优化**：合理使用缓存和懒加载
5. **用户体验**：提供友好的错误提示和加载状态

### 8.3 质量保证

1. **代码规范**：遵循ESLint和Prettier规范
2. **组件测试**：编写单元测试
3. **集成测试**：测试模块间交互
4. **用户测试**：收集用户反馈并优化

---

## 总结

本技术方案详细规划了PCB行业清洁生产云审核模块的预审核、审核、方案库三大核心模块的具体实现方案。通过严格的前后端解耦、组件化设计和模块化开发，确保系统的高可维护性和可扩展性。方案遵循Vue 3最佳实践，充分利用Naive UI组件库，为用户提供流畅的审核体验。

