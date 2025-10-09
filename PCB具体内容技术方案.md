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
    <n-spin :show="loading">
      <!-- 审核结果总览 -->
      <n-card title="审核结果总览" class="mb-4">
        <!-- 汇总统计 -->
        <n-grid :cols="4" :x-gap="16" class="mb-4">
          <n-gi>
            <n-statistic 
              label="最终得分" 
              :value="summary.totalScore ? summary.totalScore.toFixed(2) : '0.00'" 
            />
          </n-gi>
          <n-gi>
            <n-statistic label="综合等级">
              <n-tag :type="getLevelTagType(summary.overallLevel)">
                {{ summary.overallLevel || '待评估' }}
              </n-tag>
            </n-statistic>
          </n-gi>
          <n-gi>
            <n-statistic label="待改进项数" :value="summary.improvementItems || 0" />
          </n-gi>
          <n-gi>
            <n-statistic label="限定性指标" :value="summary.limitingIndicators || 0" />
          </n-gi>
        </n-grid>
        
        <!-- ECharts 雷达图 -->
        <div ref="radarChart" style="width: 100%; height: 300px;"></div>
      </n-card>

      <!-- 审核操作栏 -->
      <n-card title="审核操作" class="mb-4">
        <n-space>
          <n-button type="primary" @click="handleAutoCalculate">
            <template #icon>
              <TheIcon icon="carbon:calculator" />
            </template>
            自动计算评估
          </n-button>
          <n-button @click="handleResetAudit">
            <template #icon>
              <TheIcon icon="carbon:reset" />
            </template>
            重置审核
          </n-button>
          <n-button type="success" @click="handleSubmitAudit" :disabled="!canSubmit">
            <template #icon>
              <TheIcon icon="carbon:checkmark" />
            </template>
            提交审核结果
          </n-button>
        </n-space>
      </n-card>

      <!-- 详细审核表 -->
      <n-card title="64项指标详细审核">
        <n-data-table
          :columns="columns"
          :data="auditTreeData"
          :row-key="row => row.id"
          default-expand-all
          :pagination="false"
          :loading="tableLoading"
        >
          <!-- 指标名称列 -->
          <template #name="{ row }">
            <div class="indicator-name">
              <span v-if="row.isLimiting" class="limiting-indicator">*</span>
              {{ row.name }}
            </div>
          </template>
          
          <!-- 当前值列 -->
          <template #currentValue="{ row }">
            <span v-if="row.currentValue !== null">
              {{ formatValue(row.currentValue, row.unit) }}
            </span>
            <span v-else class="text-gray-400">-</span>
          </template>
          
          <!-- 评级列 -->
          <template #level="{ row }">
            <component 
              :is="getIndicatorComponent(row)" 
              :row="row"
              @update="handleIndicatorUpdate"
            />
          </template>
          
          <!-- 推荐方案列 -->
          <template #schemes="{ row }">
            <n-button 
              v-if="row.recommendedSchemes && row.recommendedSchemes.length > 0"
              size="small" 
              type="info"
              @click="showRecommendedSchemes(row)"
            >
              查看方案({{ row.recommendedSchemes.length }})
            </n-button>
            <span v-else class="text-gray-400">-</span>
          </template>
        </n-data-table>
      </n-card>
      
      <!-- 推荐方案弹窗 -->
      <n-modal v-model:show="showSchemeModal" preset="card" title="推荐改进方案" style="width: 800px">
        <div v-if="currentSchemes && currentSchemes.length > 0">
          <n-list>
            <n-list-item v-for="scheme in currentSchemes" :key="scheme.id">
              <n-thing>
                <template #header>
                  <n-space>
                    <span>{{ scheme.name }}</span>
                    <n-tag size="small" type="info">{{ scheme.type }}</n-tag>
                  </n-space>
                </template>
                <template #description>
                  <div class="scheme-details">
                    <p><strong>方案描述：</strong>{{ scheme.description }}</p>
                    <p><strong>实施方案：</strong>{{ scheme.implementation }}</p>
                    <p><strong>预期效果：</strong>{{ scheme.expectedEffect }}</p>
                    <n-space>
                      <n-tag type="success">投资：{{ scheme.investment }}万元</n-tag>
                      <n-tag type="warning">回收期：{{ scheme.paybackPeriod }}年</n-tag>
                    </n-space>
                  </div>
                </template>
              </n-thing>
            </n-list-item>
          </n-list>
        </div>
        <n-empty v-else description="暂无推荐方案" />
      </n-modal>
    </n-spin>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { 
  NCard, NGrid, NGi, NStatistic, NTag, NButton, NSpace, 
  NDataTable, NModal, NList, NListItem, NThing, NEmpty,
  useMessage, useDialog
} from 'naive-ui'
import { TheIcon } from '@/components/icon'
import { auditApi } from '@/api/modules/pcb-audit'
import { processAuditData, auditLogic } from '@/utils/pcb-audit-logic'
import * as echarts from 'echarts'

defineOptions({ name: 'PCBAudit' })

const route = useRoute()
const message = useMessage()
const dialog = useDialog()

// 响应式数据
const loading = ref(false)
const tableLoading = ref(false)
const showSchemeModal = ref(false)
const currentSchemes = ref([])
const preAuditData = ref({})
const auditResults = ref([])
const summary = ref({
  totalScore: 0,
  overallLevel: '',
  improvementItems: 0,
  limitingIndicators: 0
})

// 计算属性
const enterpriseId = computed(() => route.params.id)

const auditTreeData = computed(() => {
  const treeData = []
  const categoryMap = new Map()
  
  // 按类别分组
  auditResults.value.forEach(item => {
    if (!categoryMap.has(item.category)) {
      categoryMap.set(item.category, {
        id: `category-${item.category}`,
        name: item.category,
        children: [],
        isCategory: true
      })
    }
    categoryMap.get(item.category).children.push(item)
  })
  
  // 构建树形结构
  categoryMap.forEach(category => {
    treeData.push(category)
  })
  
  return treeData
})

const canSubmit = computed(() => {
  return auditResults.value.every(item => item.level && item.level !== '待评估')
})

// 表格列配置
const columns = [
  {
    title: '指标名称',
    key: 'name',
    width: 200,
    tree: true
  },
  {
    title: '当前值',
    key: 'currentValue',
    width: 120
  },
  {
    title: '评级',
    key: 'level',
    width: 150
  },
  {
    title: '推荐方案',
    key: 'schemes',
    width: 120
  }
]

// 方法定义
const fetchPreAuditData = async () => {
  try {
    loading.value = true
    const response = await auditApi.getPreAuditData(enterpriseId.value)
    preAuditData.value = response.data
    processAuditResults()
  } catch (error) {
    console.error('获取预审核数据失败:', error)
    message.error('获取预审核数据失败')
  } finally {
    loading.value = false
  }
}

const processAuditResults = () => {
  auditResults.value = processAuditData(preAuditData.value)
  calculateSummary()
  nextTick(() => {
    initRadarChart()
  })
}

const calculateSummary = () => {
  const results = auditResults.value
  let totalScore = 0
  let improvementItems = 0
  let limitingIndicators = 0
  
  results.forEach(item => {
    if (item.level === 'I级') totalScore += 4
    else if (item.level === 'II级') totalScore += 3
    else if (item.level === 'III级') totalScore += 2
    else if (item.level === '不达标') totalScore += 1
    
    if (item.level !== 'I级' && item.level !== '待评估') {
      improvementItems++
    }
    
    if (item.isLimiting) {
      limitingIndicators++
    }
  })
  
  const averageScore = results.length > 0 ? totalScore / results.length : 0
  let overallLevel = '不达标'
  
  if (averageScore >= 3.5) overallLevel = 'I级'
  else if (averageScore >= 2.5) overallLevel = 'II级'
  else if (averageScore >= 1.5) overallLevel = 'III级'
  
  summary.value = {
    totalScore: averageScore,
    overallLevel,
    improvementItems,
    limitingIndicators
  }
}

const getLevelTagType = (level) => {
  const types = {
    'I级': 'success',
    'II级': 'info',
    'III级': 'warning',
    '不达标': 'error'
  }
  return types[level] || 'default'
}

const getIndicatorComponent = (row) => {
  const category = auditLogic[row.categoryKey]
  if (!category) return 'div'
  
  if (category.type === 'qualitative') {
    return 'QualitativeIndicator'
  } else if (category.type === 'quantitative') {
    return 'QuantitativeIndicator'
  } else if (category.type === 'mixed') {
    if (row.type === 'limiting') {
      return 'LimitingIndicator'
    } else if (row.type === 'quantitative') {
      return 'QuantitativeIndicator'
    } else {
      return 'QualitativeIndicator'
    }
  }
  return 'div'
}

const handleIndicatorUpdate = async (indicatorId, level) => {
  try {
    await auditApi.updateIndicatorLevel(enterpriseId.value, indicatorId, level)
    
    // 更新本地数据
    const indicator = auditResults.value.find(item => item.id === indicatorId)
    if (indicator) {
      indicator.level = level
      calculateSummary()
    }
    
    message.success('指标评级更新成功')
  } catch (error) {
    console.error('更新指标评级失败:', error)
    message.error('更新指标评级失败')
  }
}

const handleAutoCalculate = async () => {
  try {
    tableLoading.value = true
    processAuditResults()
    message.success('自动计算完成')
  } catch (error) {
    console.error('自动计算失败:', error)
    message.error('自动计算失败')
  } finally {
    tableLoading.value = false
  }
}

const handleResetAudit = () => {
  dialog.warning({
    title: '确认重置',
    content: '确定要重置所有审核结果吗？此操作不可撤销。',
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      auditResults.value.forEach(item => {
        item.level = '待评估'
      })
      calculateSummary()
      message.success('审核结果已重置')
    }
  })
}

const handleSubmitAudit = async () => {
  try {
    loading.value = true
    const auditData = {
      enterpriseId: enterpriseId.value,
      indicators: auditResults.value,
      summary: summary.value,
      auditDate: new Date().toISOString()
    }
    
    await auditApi.submitAuditResult(enterpriseId.value, auditData)
    message.success('审核结果提交成功')
  } catch (error) {
    console.error('提交审核结果失败:', error)
    message.error('提交审核结果失败')
  } finally {
    loading.value = false
  }
}

const showRecommendedSchemes = (row) => {
  currentSchemes.value = row.recommendedSchemes || []
  showSchemeModal.value = true
}

const formatValue = (value, unit) => {
  if (value === null || value === undefined) return '-'
  return `${value.toFixed(2)}${unit || ''}`
}

const initRadarChart = () => {
  const chartDom = document.getElementById('radarChart')
  if (!chartDom) return
  
  const myChart = echarts.init(chartDom)
  
  const categories = auditResults.value.map(item => item.category)
  const uniqueCategories = [...new Set(categories)]
  
  const option = {
    title: {
      text: '审核结果雷达图',
      left: 'center'
    },
    tooltip: {},
    radar: {
      indicator: uniqueCategories.map(category => ({
        name: category,
        max: 4
      }))
    },
    series: [{
      name: '审核结果',
      type: 'radar',
      data: [{
        value: uniqueCategories.map(category => {
          const categoryItems = auditResults.value.filter(item => item.category === category)
          const avgScore = categoryItems.reduce((sum, item) => {
            const score = item.level === 'I级' ? 4 : item.level === 'II级' ? 3 : item.level === 'III级' ? 2 : 1
            return sum + score
          }, 0) / categoryItems.length
          return avgScore || 0
        }),
        name: '当前评级'
      }]
    }]
  }
  
  myChart.setOption(option)
}

// 生命周期
onMounted(() => {
  fetchPreAuditData()
})
</script>

<style scoped>
.audit-page {
  min-height: 100vh;
}

.indicator-name {
  display: flex;
  align-items: center;
}

.limiting-indicator {
  color: #ff4d4f;
  font-weight: bold;
  margin-right: 4px;
}

.scheme-details p {
  margin: 8px 0;
  line-height: 1.5;
}

.text-gray-400 {
  color: #9ca3af;
}
</style>
```

### 3.2 64项指标审核逻辑

```javascript
// web/src/utils/pcb-audit-logic.js
export const auditLogic = {
  // 指标1-6: 生产工艺与装备要求（定性判断）
  processEquipment: {
    type: 'qualitative',
    indicators: [
      { id: 1, name: '基本要求', category: '生产工艺与装备要求' },
      { id: 2, name: '机械加工及辅助设施', category: '生产工艺与装备要求' },
      { id: 3, name: '线路与阻焊图形形成(印刷或感光工艺)', category: '生产工艺与装备要求' },
      { id: 4, name: '板面清洗', category: '生产工艺与装备要求' },
      { id: 5, name: '蚀刻', category: '生产工艺与装备要求' },
      { id: 6, name: '电镀与化学镀', category: '生产工艺与装备要求' }
    ],
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

  // 指标7-14: 能源消耗 - 单位产品电耗（定量计算与自动评估）
  energyConsumption: {
    type: 'quantitative',
    indicators: [
      { id: 7, name: '刚性印制电路单面板(单位产品电耗)', category: '能源消耗' },
      { id: 8, name: '刚性印制电路双面板(单位产品电耗)', category: '能源消耗' },
      { id: 9, name: '刚性印制电路多层板(2+n)层(单位产品电耗)', category: '能源消耗' },
      { id: 10, name: '刚性印制电路HDI板(2+n)层(单位产品电耗)', category: '能源消耗' },
      { id: 11, name: '挠性印制电路单面板(单位产品电耗)', category: '能源消耗' },
      { id: 12, name: '挠性印制电路双面板(单位产品电耗)', category: '能源消耗' },
      { id: 13, name: '挠性印制电路多层板(2+n)层(单位产品电耗)', category: '能源消耗' },
      { id: 14, name: '挠性印制电路HDI板(2+n)层(单位产品电耗)', category: '能源消耗' }
    ],
    formula: '总电耗 / 总产量',
    standards: {
      rigidSingle: { level1: 100, level2: 150, level3: 200 },
      rigidDouble: { level1: 120, level2: 180, level3: 240 },
      rigidMultilayer: { level1: 150, level2: 220, level3: 300 },
      rigidHDI: { level1: 180, level2: 260, level3: 350 },
      flexibleSingle: { level1: 80, level2: 120, level3: 160 },
      flexibleDouble: { level1: 100, level2: 150, level3: 200 },
      flexibleMultilayer: { level1: 120, level2: 180, level3: 240 },
      flexibleHDI: { level1: 150, level2: 220, level3: 300 }
    },
    calculate: (preAuditData, productType) => {
      const totalPower = preAuditData.resourceConsumption.electricity
        .filter(item => item.type === productType)
        .reduce((sum, item) => sum + item.amount, 0)
      const totalOutput = preAuditData.productionInfo.output['2023'][productType] || 0
      return totalPower / totalOutput
    },
    evaluate: (value, productType) => {
      const standard = auditLogic.energyConsumption.standards[productType]
      if (value <= standard.level1) return 'I级'
      if (value <= standard.level2) return 'II级'
      if (value <= standard.level3) return 'III级'
      return '不达标'
    }
  },

  // 指标15-19: 水资源消耗（定量计算与自动评估）
  waterConsumption: {
    type: 'quantitative',
    indicators: [
      { id: 15, name: '单面板(单位产品新鲜水耗)', category: '水资源消耗' },
      { id: 16, name: '双面板(单位产品新鲜水耗)', category: '水资源消耗' },
      { id: 17, name: '多层板(2+n)层(单位产品新鲜水耗)', category: '水资源消耗' },
      { id: 18, name: 'HDI板(2+n)层(单位产品新鲜水耗)', category: '水资源消耗' },
      { id: 19, name: '水资源重复利用率', category: '水资源消耗' }
    ],
    standards: {
      single: { level1: 0.8, level2: 1.2, level3: 1.6 },
      double: { level1: 1.0, level2: 1.5, level3: 2.0 },
      multilayer: { level1: 1.2, level2: 1.8, level3: 2.4 },
      hdi: { level1: 1.5, level2: 2.2, level3: 3.0 },
      reuseRate: { level1: 80, level2: 60, level3: 40 }
    },
    calculate: (preAuditData, indicatorId) => {
      if (indicatorId === 19) {
        // 水资源重复利用率
        return preAuditData.pollutionControl.waterReuseRate[0]?.rate || 0
      } else {
        // 单位产品新鲜水耗
        const productType = getProductTypeByIndicatorId(indicatorId)
        const totalWater = preAuditData.resourceConsumption.water
          .filter(item => item.type === productType)
          .reduce((sum, item) => sum + item.amount, 0)
        const totalOutput = preAuditData.productionInfo.output['2023'][productType] || 0
        return totalWater / totalOutput
      }
    },
    evaluate: (value, indicatorId) => {
      if (indicatorId === 19) {
        const standard = auditLogic.waterConsumption.standards.reuseRate
        if (value >= standard.level1) return 'I级'
        if (value >= standard.level2) return 'II级'
        if (value >= standard.level3) return 'III级'
        return '不达标'
      } else {
        const productType = getProductTypeByIndicatorId(indicatorId)
        const standard = auditLogic.waterConsumption.standards[productType]
        if (value <= standard.level1) return 'I级'
        if (value <= standard.level2) return 'II级'
        if (value <= standard.level3) return 'III级'
        return '不达标'
      }
    }
  },

  // 指标20-27: 原/辅料消耗 - 覆铜板利用率（定量计算与自动评估）
  rawMaterialConsumption: {
    type: 'quantitative',
    indicators: [
      { id: 20, name: '刚性印制电路单面板 覆铜板利用率', category: '原/辅料消耗' },
      { id: 21, name: '刚性印制电路双面板 覆铜板利用率', category: '原/辅料消耗' },
      { id: 22, name: '刚性印制电路多层板(2+n)层覆铜板利用率', category: '原/辅料消耗' },
      { id: 23, name: '刚性印制电路HDI板(2+n)层覆铜板利用率', category: '原/辅料消耗' },
      { id: 24, name: '挠性印制电路单面板覆铜板利用率', category: '原/辅料消耗' },
      { id: 25, name: '挠性印制电路双面板 覆铜板利用率', category: '原/辅料消耗' },
      { id: 26, name: '挠性性印制电路多层板(2+n)层覆铜板利用率', category: '原/辅料消耗' },
      { id: 27, name: '挠性印制电路HDI板(2+n)层覆铜板利用率', category: '原/辅料消耗' }
    ],
    standards: {
      rigidSingle: { level1: 95, level2: 90, level3: 85 },
      rigidDouble: { level1: 92, level2: 87, level3: 82 },
      rigidMultilayer: { level1: 90, level2: 85, level3: 80 },
      rigidHDI: { level1: 88, level2: 83, level3: 78 },
      flexibleSingle: { level1: 93, level2: 88, level3: 83 },
      flexibleDouble: { level1: 91, level2: 86, level3: 81 },
      flexibleMultilayer: { level1: 89, level2: 84, level3: 79 },
      flexibleHDI: { level1: 87, level2: 82, level3: 77 }
    },
    calculate: (preAuditData, productType) => {
      const materialData = preAuditData.rawMaterials
        .find(item => item.name.includes('覆铜板') && item.type === productType)
      if (!materialData) return 0
      return (materialData.netUsage / materialData.totalInput) * 100
    },
    evaluate: (value, productType) => {
      const standard = auditLogic.rawMaterialConsumption.standards[productType]
      if (value >= standard.level1) return 'I级'
      if (value >= standard.level2) return 'II级'
      if (value >= standard.level3) return 'III级'
      return '不达标'
    }
  },

  // 指标28-29: 资源综合利用（定量自动评估）
  resourceUtilization: {
    type: 'quantitative',
    indicators: [
      { id: 28, name: '金属铜回收率', category: '资源综合利用' },
      { id: 29, name: '一般工业固体废物综合利用率', category: '资源综合利用' }
    ],
    standards: {
      copperRecovery: { level1: 95, level2: 90, level3: 85 },
      solidWasteUtilization: { level1: 90, level2: 80, level3: 70 }
    },
    calculate: (preAuditData, indicatorId) => {
      if (indicatorId === 28) {
        return preAuditData.pollutionControl.copperRecovery[0]?.rate || 0
      } else {
        return preAuditData.solidWaste.general[0]?.utilizationRate || 0
      }
    },
    evaluate: (value, indicatorId) => {
      const standard = indicatorId === 28 
        ? auditLogic.resourceUtilization.standards.copperRecovery
        : auditLogic.resourceUtilization.standards.solidWasteUtilization
      if (value >= standard.level1) return 'I级'
      if (value >= standard.level2) return 'II级'
      if (value >= standard.level3) return 'III级'
      return '不达标'
    }
  },

  // 指标30-46: 污染物产生与排放（定量计算与自动评估 + 定性判断）
  pollutionEmission: {
    type: 'mixed',
    indicators: [
      // 废水产生量 (30-33)
      { id: 30, name: '单面板废水产生量', category: '废水的产生与排放', type: 'quantitative' },
      { id: 31, name: '双面板废水产生量', category: '废水的产生与排放', type: 'quantitative' },
      { id: 32, name: '多层板(2+n)层废水产生量', category: '废水的产生与排放', type: 'quantitative' },
      { id: 33, name: 'HDI板(2+n)层废水产生量', category: '废水的产生与排放', type: 'quantitative' },
      // 废水中铜产生量 (34-37)
      { id: 34, name: '单面板废水中铜产生量', category: '废水的产生与排放', type: 'quantitative' },
      { id: 35, name: '双面板废水中铜产生量', category: '废水的产生与排放', type: 'quantitative' },
      { id: 36, name: '多层板(2+n)层废水中铜产生量', category: '废水的产生与排放', type: 'quantitative' },
      { id: 37, name: 'HDI板(2+n)层废水中铜产生量', category: '废水的产生与排放', type: 'quantitative' },
      // 废水中COD产生量 (38-41)
      { id: 38, name: '单面板废水中COD产生量', category: '废水的产生与排放', type: 'quantitative' },
      { id: 39, name: '双面板废水废水中COD产生量', category: '废水的产生与排放', type: 'quantitative' },
      { id: 40, name: '多层板(2+n)层废水中 COD 产生量', category: '废水的产生与排放', type: 'quantitative' },
      { id: 41, name: 'HDI板(2+n)层废水中 COD 产生量', category: '废水的产生与排放', type: 'quantitative' },
      // 污染治理设施 (42-46)
      { id: 42, name: '废水收集与处理', category: '废水的产生与排放', type: 'qualitative' },
      { id: 43, name: '废气收集与处理', category: '废气的产生与排放', type: 'qualitative' },
      { id: 44, name: '一般固体废物收集与处理', category: '固体废物的产生与排放', type: 'qualitative' },
      { id: 45, name: '危险废物收集与处理', category: '固体废物的产生与排放', type: 'qualitative' },
      { id: 46, name: '噪声', category: '噪声的产生与排放', type: 'qualitative' }
    ],
    standards: {
      wastewater: { level1: 0.5, level2: 0.8, level3: 1.2 },
      copperInWastewater: { level1: 0.1, level2: 0.2, level3: 0.3 },
      codInWastewater: { level1: 0.3, level2: 0.5, level3: 0.8 }
    },
    calculate: (preAuditData, indicatorId) => {
      if (indicatorId >= 42) return null // 定性指标不需要计算
      
      const productType = getProductTypeByIndicatorId(indicatorId)
      const pollutantType = getPollutantTypeByIndicatorId(indicatorId)
      
      const emissionData = preAuditData.pollutionControl.waterEmission
        .find(item => item.type === productType && item.pollutant === pollutantType)
      
      if (!emissionData) return 0
      const totalOutput = preAuditData.productionInfo.output['2023'][productType] || 0
      return emissionData.amount / totalOutput
    },
    evaluate: (value, indicatorId) => {
      if (indicatorId >= 42) {
        // 定性指标，返回默认选项
        return auditLogic.processEquipment.options
      }
      
      const pollutantType = getPollutantTypeByIndicatorId(indicatorId)
      const standard = auditLogic.pollutionEmission.standards[pollutantType]
      if (value <= standard.level1) return 'I级'
      if (value <= standard.level2) return 'II级'
      if (value <= standard.level3) return 'III级'
      return '不达标'
    }
  },

  // 指标47-49: 温室气体排放（定量/定性混合评估）
  greenhouseGasEmission: {
    type: 'mixed',
    indicators: [
      { id: 47, name: '碳减排管理', category: '温室气体排放', type: 'qualitative' },
      { id: 48, name: '单位产值碳排放量', category: '温室气体排放', type: 'qualitative' },
      { id: 49, name: '碳排放强度', category: '温室气体排放', type: 'quantitative' }
    ],
    standards: {
      carbonIntensity: { level1: 0.5, level2: 0.8, level3: 1.2 }
    },
    calculate: (preAuditData, indicatorId) => {
      if (indicatorId === 49) {
        const totalEmission = preAuditData.greenhouseGasEmission?.totalEmission || 0
        const totalOutput = preAuditData.productionInfo.output['2023']
        const totalValue = Object.values(totalOutput).reduce((sum, val) => sum + val, 0)
        return totalEmission / totalValue
      }
      return null
    },
    evaluate: (value, indicatorId) => {
      if (indicatorId === 49) {
        const standard = auditLogic.greenhouseGasEmission.standards.carbonIntensity
        if (value <= standard.level1) return 'I级'
        if (value <= standard.level2) return 'II级'
        if (value <= standard.level3) return 'III级'
        return '不达标'
      }
      return auditLogic.processEquipment.options
    }
  },

  // 指标50-53: 产品特征（定性判断 - 符合性检查）
  productCharacteristics: {
    type: 'qualitative',
    indicators: [
      { id: 50, name: '使用无毒无害或低毒低害的生产辅助材料', category: '产品特征' },
      { id: 51, name: '包装', category: '产品特征' },
      { id: 52, name: '有害物质限制使用', category: '产品特征' },
      { id: 53, name: '产品性能', category: '产品特征' }
    ],
    options: [
      { value: 'I级', label: 'I级', description: '完全符合要求' },
      { value: 'II级', label: 'II级', description: '基本符合要求' },
      { value: 'III级', label: 'III级', description: '部分符合要求' },
      { value: '不达标', label: '不达标', description: '不符合要求' }
    ],
    render: (row) => {
      return h('n-checkbox-group', {
        value: row.checkedItems,
        options: getProductCharacteristicOptions(row.id),
        onUpdateValue: (value) => updateProductCharacteristic(row.id, value)
      })
    }
  },

  // 指标54-64: 清洁生产管理（混合类型）
  cleanProductionManagement: {
    type: 'mixed',
    indicators: [
      { id: 54, name: '*环保法律法规执行情况', category: '清洁生产管理', type: 'limiting' },
      { id: 55, name: '*产业政策符合性', category: '清洁生产管理', type: 'limiting' },
      { id: 56, name: '清洁生产管理', category: '清洁生产管理', type: 'qualitative' },
      { id: 57, name: '清洁生产审核', category: '清洁生产管理', type: 'quantitative' },
      { id: 58, name: '节能管理', category: '清洁生产管理', type: 'quantitative' },
      { id: 59, name: '污染物排放监测', category: '清洁生产管理', type: 'qualitative' },
      { id: 60, name: '*危险化学品管理', category: '清洁生产管理', type: 'limiting' },
      { id: 61, name: '计量器具配备情况', category: '清洁生产管理', type: 'qualitative' },
      { id: 62, name: '*固体废物处理处置', category: '清洁生产管理', type: 'limiting' },
      { id: 63, name: '土壤污染隐患排查', category: '清洁生产管理', type: 'qualitative' },
      { id: 64, name: '运输方式', category: '清洁生产管理', type: 'quantitative' }
    ],
    standards: {
      auditCompletion: { level1: 90, level2: 70, level3: 50 },
      energyManagement: { level1: 90, level2: 70, level3: 50 },
      newEnergyVehicle: { level1: 80, level2: 60, level3: 40 }
    },
    calculate: (preAuditData, indicatorId) => {
      switch (indicatorId) {
        case 57:
          return preAuditData.cleanProductionManagement?.auditCompletion || 0
        case 58:
          return preAuditData.cleanProductionManagement?.energyManagement || 0
        case 64:
          return preAuditData.cleanProductionManagement?.newEnergyVehicleRatio || 0
        default:
          return null
      }
    },
    evaluate: (value, indicatorId) => {
      if (indicatorId === 54 || indicatorId === 55 || indicatorId === 60 || indicatorId === 62) {
        // 限定性指标
        return h('n-switch', {
          value: value,
          onUpdateValue: (val) => {
            if (!val) {
              window.$dialog.warning({
                title: '限定性指标警告',
                content: '该指标不达标，总评级不得高于III级',
                positiveText: '确认'
              })
            }
            updateIndicatorLevel(indicatorId, val ? 'I级' : '不达标')
          }
        })
      }
      
      if (indicatorId === 57 || indicatorId === 58 || indicatorId === 64) {
        // 定量指标
        const standardKey = indicatorId === 57 ? 'auditCompletion' 
          : indicatorId === 58 ? 'energyManagement' : 'newEnergyVehicle'
        const standard = auditLogic.cleanProductionManagement.standards[standardKey]
        if (value >= standard.level1) return 'I级'
        if (value >= standard.level2) return 'II级'
        if (value >= standard.level3) return 'III级'
        return '不达标'
      }
      
      // 定性指标
      return auditLogic.processEquipment.options
    }
  }
}

// 审核数据处理函数
export const processAuditData = (preAuditData) => {
  const auditResults = []
  
  // 处理所有64项指标
  Object.keys(auditLogic).forEach((categoryKey) => {
    const category = auditLogic[categoryKey]
    
    category.indicators.forEach((indicator) => {
      let currentValue = null
      let level = null
      
      if (category.type === 'quantitative' || category.type === 'mixed') {
        // 定量指标或混合指标
        if (indicator.type === 'quantitative') {
          currentValue = category.calculate(preAuditData, indicator.id)
          level = category.evaluate(currentValue, indicator.id)
        } else if (indicator.type === 'qualitative') {
          level = '待评估'
        } else if (indicator.type === 'limiting') {
          level = '待评估'
        }
      } else if (category.type === 'qualitative') {
        // 定性指标
        level = '待评估'
      }
      
      auditResults.push({
        id: indicator.id,
        name: indicator.name,
        category: indicator.category,
        type: indicator.type || category.type,
        currentValue: currentValue,
        level: level,
        recommendedSchemes: level !== 'I级' && level !== '待评估' 
          ? getRecommendedSchemes(indicator.id, level) 
          : []
      })
    })
  })
  
  return auditResults.sort((a, b) => a.id - b.id)
}

// 辅助函数：根据指标ID获取产品类型
export const getProductTypeByIndicatorId = (indicatorId) => {
  const productTypeMap = {
    7: 'rigidSingle', 8: 'rigidDouble', 9: 'rigidMultilayer', 10: 'rigidHDI',
    11: 'flexibleSingle', 12: 'flexibleDouble', 13: 'flexibleMultilayer', 14: 'flexibleHDI',
    15: 'single', 16: 'double', 17: 'multilayer', 18: 'hdi',
    20: 'rigidSingle', 21: 'rigidDouble', 22: 'rigidMultilayer', 23: 'rigidHDI',
    24: 'flexibleSingle', 25: 'flexibleDouble', 26: 'flexibleMultilayer', 27: 'flexibleHDI',
    30: 'single', 31: 'double', 32: 'multilayer', 33: 'hdi',
    34: 'single', 35: 'double', 36: 'multilayer', 37: 'hdi',
    38: 'single', 39: 'double', 40: 'multilayer', 41: 'hdi'
  }
  return productTypeMap[indicatorId] || null
}

// 辅助函数：根据指标ID获取污染物类型
export const getPollutantTypeByIndicatorId = (indicatorId) => {
  if (indicatorId >= 30 && indicatorId <= 33) return 'wastewater'
  if (indicatorId >= 34 && indicatorId <= 37) return 'copperInWastewater'
  if (indicatorId >= 38 && indicatorId <= 41) return 'codInWastewater'
  return null
}

// 辅助函数：获取产品特征选项
export const getProductCharacteristicOptions = (indicatorId) => {
  const optionsMap = {
    50: [
      { label: '使用无毒无害材料', value: 'non-toxic' },
      { label: '使用低毒低害材料', value: 'low-toxic' },
      { label: '材料符合环保要求', value: 'eco-friendly' }
    ],
    51: [
      { label: '包装减量化', value: 'reduced-packaging' },
      { label: '可回收包装', value: 'recyclable' },
      { label: '环保包装材料', value: 'eco-packaging' }
    ],
    52: [
      { label: '不使用有害物质', value: 'no-hazardous' },
      { label: '符合RoHS标准', value: 'rohs-compliant' },
      { label: '符合REACH法规', value: 'reach-compliant' }
    ],
    53: [
      { label: '产品性能优良', value: 'excellent-performance' },
      { label: '产品可靠性高', value: 'high-reliability' },
      { label: '产品寿命长', value: 'long-lifespan' }
    ]
  }
  return optionsMap[indicatorId] || []
}
```

### 3.3 指标审核组件设计

#### 3.3.1 定性指标组件

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/components/QualitativeIndicator.vue -->
<template>
  <n-select
    :value="row.level"
    :options="options"
    placeholder="请选择评级"
    @update:value="handleUpdate"
    :disabled="disabled"
  >
    <template #option="{ option }">
      <div>
        <div>{{ option.label }}</div>
        <div class="text-xs text-gray-500">{{ option.description }}</div>
      </div>
    </template>
  </n-select>
</template>

<script setup>
import { computed } from 'vue'
import { NSelect } from 'naive-ui'

const props = defineProps({
  row: {
    type: Object,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update'])

const options = [
  { value: 'I级', label: 'I级', description: '采用国际先进工艺和设备' },
  { value: 'II级', label: 'II级', description: '采用国内先进工艺和设备' },
  { value: 'III级', label: 'III级', description: '采用一般工艺和设备' },
  { value: '不达标', label: '不达标', description: '工艺和设备落后' }
]

const handleUpdate = (value) => {
  emit('update', props.row.id, value)
}
</script>
```

#### 3.3.2 定量指标组件

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/components/QuantitativeIndicator.vue -->
<template>
  <div class="quantitative-indicator">
    <div class="value-display">
      <span class="current-value">{{ formatValue(row.currentValue, row.unit) }}</span>
      <n-tag 
        :type="getLevelTagType(row.level)" 
        size="small"
        class="ml-2"
      >
        {{ row.level || '待评估' }}
      </n-tag>
    </div>
    <n-button 
      size="small" 
      type="primary" 
      @click="showManualOverride"
      :disabled="disabled"
    >
      手动调整
    </n-button>
    
    <!-- 手动调整弹窗 -->
    <n-modal v-model:show="showOverrideModal" preset="card" title="手动调整评级" style="width: 400px">
      <n-form :model="overrideForm" :rules="overrideRules" ref="formRef">
        <n-form-item label="当前值" path="currentValue">
          <n-input-number
            v-model:value="overrideForm.currentValue"
            :min="0"
            :precision="2"
            :disabled="true"
          />
        </n-form-item>
        <n-form-item label="评级" path="level">
          <n-select
            v-model:value="overrideForm.level"
            :options="options"
            placeholder="请选择评级"
          />
        </n-form-item>
        <n-form-item label="调整原因" path="reason">
          <n-input
            v-model:value="overrideForm.reason"
            type="textarea"
            placeholder="请输入调整原因"
            :rows="3"
          />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showOverrideModal = false">取消</n-button>
          <n-button type="primary" @click="handleOverride">确认</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { NSelect, NTag, NButton, NModal, NForm, NFormItem, NInputNumber, NInput, NSpace } from 'naive-ui'

const props = defineProps({
  row: {
    type: Object,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update'])

const showOverrideModal = ref(false)
const formRef = ref(null)

const overrideForm = ref({
  currentValue: null,
  level: '',
  reason: ''
})

const overrideRules = {
  level: [
    { required: true, message: '请选择评级', trigger: 'change' }
  ],
  reason: [
    { required: true, message: '请输入调整原因', trigger: 'blur' }
  ]
}

const options = [
  { value: 'I级', label: 'I级' },
  { value: 'II级', label: 'II级' },
  { value: 'III级', label: 'III级' },
  { value: '不达标', label: '不达标' }
]

const formatValue = (value, unit) => {
  if (value === null || value === undefined) return '-'
  return `${value.toFixed(2)}${unit || ''}`
}

const getLevelTagType = (level) => {
  const types = {
    'I级': 'success',
    'II级': 'info',
    'III级': 'warning',
    '不达标': 'error'
  }
  return types[level] || 'default'
}

const showManualOverride = () => {
  overrideForm.value = {
    currentValue: props.row.currentValue,
    level: props.row.level || '',
    reason: ''
  }
  showOverrideModal.value = true
}

const handleOverride = async () => {
  try {
    await formRef.value?.validate()
    emit('update', props.row.id, overrideForm.value.level, overrideForm.value.reason)
    showOverrideModal.value = false
  } catch (error) {
    console.error('表单验证失败:', error)
  }
}
</script>

<style scoped>
.quantitative-indicator {
  display: flex;
  align-items: center;
  gap: 8px;
}

.value-display {
  display: flex;
  align-items: center;
}

.current-value {
  font-weight: 500;
  color: #333;
}
</style>
```

#### 3.3.3 限定性指标组件

```vue
<!-- web/src/views/cloud-audit/pcb/enterprise-detail/components/LimitingIndicator.vue -->
<template>
  <div class="limiting-indicator">
    <n-switch
      :value="isCompliant"
      @update:value="handleSwitchChange"
      :disabled="disabled"
    >
      <template #checked>
        <span class="text-green-600">达标</span>
      </template>
      <template #unchecked>
        <span class="text-red-600">不达标</span>
      </template>
    </n-switch>
    <n-tooltip trigger="hover" v-if="!isCompliant">
      <template #trigger>
        <n-icon class="ml-1 text-red-500 cursor-pointer">
          <TheIcon icon="carbon:warning" />
        </n-icon>
      </template>
      <span>限定性指标不达标，总评级不得高于III级</span>
    </n-tooltip>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NSwitch, NTooltip, NIcon } from 'naive-ui'
import { TheIcon } from '@/components/icon'
import { useDialog } from 'naive-ui'

const props = defineProps({
  row: {
    type: Object,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update'])
const dialog = useDialog()

const isCompliant = computed(() => {
  return props.row.level === 'I级'
})

const handleSwitchChange = (value) => {
  if (!value) {
    // 不达标时显示警告
    dialog.warning({
      title: '限定性指标警告',
      content: '该指标不达标，总评级不得高于III级。确定要继续吗？',
      positiveText: '确认',
      negativeText: '取消',
      onPositiveClick: () => {
        emit('update', props.row.id, '不达标')
      }
    })
  } else {
    emit('update', props.row.id, 'I级')
  }
}
</script>

<style scoped>
.limiting-indicator {
  display: flex;
  align-items: center;
}
</style>
```

### 3.4 改进措施推荐逻辑

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
    implementation: scheme.implementation,
    expectedEffect: scheme.expectedEffect,
    investment: scheme.investment,
    paybackPeriod: scheme.paybackPeriod,
    type: scheme.type
  }))
}

// 方案库数据（示例）
const schemeLibrary = [
  {
    id: 1,
    name: '高效电镀工艺优化',
    type: '工艺改进',
    description: '采用脉冲电镀技术，提高电镀效率，降低能耗',
    implementation: '1. 采购脉冲电镀设备\n2. 培训操作人员\n3. 调整工艺参数',
    expectedEffect: '电耗降低15%，生产效率提升10%',
    investment: 50,
    paybackPeriod: 2.5,
    indicatorIds: [7, 8, 9, 10, 11, 12, 13, 14]
  },
  {
    id: 2,
    name: '废水回用系统',
    type: '设备改造',
    description: '建设废水深度处理回用系统，提高水资源利用率',
    implementation: '1. 设计回用系统\n2. 采购处理设备\n3. 建设回用管网',
    expectedEffect: '新鲜水消耗降低30%，废水回用率达到80%',
    investment: 120,
    paybackPeriod: 3.2,
    indicatorIds: [15, 16, 17, 18, 19]
  },
  {
    id: 3,
    name: '覆铜板优化切割',
    type: '工艺改进',
    description: '优化覆铜板切割工艺，减少边角料浪费',
    implementation: '1. 优化切割方案\n2. 改进切割设备\n3. 建立边角料回收机制',
    expectedEffect: '覆铜板利用率提升8%，材料成本降低5%',
    investment: 25,
    paybackPeriod: 1.8,
    indicatorIds: [20, 21, 22, 23, 24, 25, 26, 27]
  }
]
```

### 3.5 审核API接口设计

```javascript
// web/src/api/modules/pcb-audit.js
import { request } from '@/utils'

export const auditApi = {
  // 获取预审核数据
  getPreAuditData: (enterpriseId) => request.get(`/api/v1/pcb/enterprise/${enterpriseId}/pre-audit`),
  
  // 获取审核标准
  getAuditStandards: () => request.get('/api/v1/pcb/audit/standards'),
  
  // 获取审核结果
  getAuditResult: (enterpriseId) => request.get(`/api/v1/pcb/enterprise/${enterpriseId}/audit`),
  
  // 更新单个指标评级
  updateIndicatorLevel: (enterpriseId, indicatorId, level, reason = null) => 
    request.put(`/api/v1/pcb/enterprise/${enterpriseId}/audit/indicator/${indicatorId}`, {
      level,
      reason
    }),
  
  // 批量更新指标评级
  batchUpdateIndicators: (enterpriseId, indicators) => 
    request.put(`/api/v1/pcb/enterprise/${enterpriseId}/audit/indicators`, {
      indicators
    }),
  
  // 自动计算评估
  autoCalculate: (enterpriseId) => 
    request.post(`/api/v1/pcb/enterprise/${enterpriseId}/audit/auto-calculate`),
  
  // 提交审核结果
  submitAuditResult: (enterpriseId, auditData) => 
    request.post(`/api/v1/pcb/enterprise/${enterpriseId}/audit/submit`, auditData),
  
  // 获取推荐方案
  getRecommendedSchemes: (enterpriseId, indicatorId) => 
    request.get(`/api/v1/pcb/enterprise/${enterpriseId}/audit/schemes/${indicatorId}`),
  
  // 获取审核历史
  getAuditHistory: (enterpriseId) => 
    request.get(`/api/v1/pcb/enterprise/${enterpriseId}/audit/history`),
  
  // 导出审核报告
  exportAuditReport: (enterpriseId, format = 'pdf') => 
    request.get(`/api/v1/pcb/enterprise/${enterpriseId}/audit/export`, {
      params: { format },
      responseType: 'blob'
    })
}

// 审核数据模型
export const AuditDataModel = {
  enterpriseId: String,
  indicators: [
    {
      id: Number,
      name: String,
      category: String,
      currentValue: Number,
      unit: String,
      level: String, // 'I级', 'II级', 'III级', '不达标', '待评估'
      isLimiting: Boolean,
      recommendedSchemes: [
        {
          id: Number,
          name: String,
          type: String,
          description: String,
          implementation: String,
          expectedEffect: String,
          investment: Number,
          paybackPeriod: Number
        }
      ]
    }
  ],
  summary: {
    totalScore: Number,
    overallLevel: String,
    improvementItems: Number,
    limitingIndicators: Number
  },
  auditDate: String,
  auditor: String,
  status: String // 'draft', 'submitted', 'approved'
}
```

### 3.6 审核数据处理工具函数

```javascript
// web/src/utils/pcb-audit-utils.js
import { auditLogic } from './pcb-audit-logic'
import { getRecommendedSchemes } from './scheme-recommendation'

// 处理审核数据
export const processAuditData = (preAuditData) => {
  const auditResults = []
  
  // 处理所有64项指标
  Object.keys(auditLogic).forEach((categoryKey) => {
    const category = auditLogic[categoryKey]
    
    category.indicators.forEach((indicator) => {
      let currentValue = null
      let level = null
      
      // 根据指标类型计算当前值和评级
      if (category.type === 'quantitative') {
        currentValue = category.calculate(preAuditData, indicator.id)
        level = category.evaluate(currentValue, indicator.id)
      } else if (category.type === 'qualitative') {
        // 定性指标需要人工评估，初始为待评估
        level = '待评估'
      } else if (category.type === 'mixed') {
        if (indicator.type === 'quantitative') {
          currentValue = category.calculate(preAuditData, indicator.id)
          level = category.evaluate(currentValue, indicator.id)
        } else {
          level = '待评估'
        }
      }
      
      // 获取推荐方案
      const recommendedSchemes = getRecommendedSchemes(indicator.id, level)
      
      auditResults.push({
        id: indicator.id,
        name: indicator.name,
        category: indicator.category,
        categoryKey,
        currentValue,
        unit: getUnitByIndicatorId(indicator.id),
        level,
        isLimiting: indicator.isLimiting || false,
        type: indicator.type || 'qualitative',
        recommendedSchemes
      })
    })
  })
  
  return auditResults
}

// 根据指标ID获取单位
const getUnitByIndicatorId = (indicatorId) => {
  const unitMap = {
    // 能源消耗指标
    7: 'kWh/m²', 8: 'kWh/m²', 9: 'kWh/m²', 10: 'kWh/m²',
    11: 'kWh/m²', 12: 'kWh/m²', 13: 'kWh/m²', 14: 'kWh/m²',
    
    // 水资源消耗指标
    15: 'm³/m²', 16: 'm³/m²', 17: 'm³/m²', 18: 'm³/m²',
    19: '%',
    
    // 原/辅料消耗指标
    20: '%', 21: '%', 22: '%', 23: '%', 24: '%', 25: '%', 26: '%', 27: '%',
    
    // 资源综合利用指标
    28: '%', 29: '%',
    
    // 废水产生与排放指标
    30: 'm³/m²', 31: 'mg/L', 32: 'mg/L', 33: 'mg/L', 34: 'mg/L',
    35: 'mg/L', 36: 'mg/L', 37: 'mg/L', 38: 'mg/L', 39: 'mg/L',
    40: 'mg/L', 41: 'mg/L', 42: 'mg/L',
    
    // 废气产生与排放指标
    43: 'mg/m³',
    
    // 固体废物产生与排放指标
    44: 'kg/m²', 45: '%',
    
    // 噪声产生与排放指标
    46: 'dB(A)',
    
    // 温室气体排放指标
    47: 'tCO2e/m²', 48: 'tCO2e/m²', 49: 'tCO2e/m²',
    
    // 产品特征指标
    50: 'μm', 51: 'μm', 52: 'μm', 53: 'μm',
    
    // 清洁生产管理指标
    54: '%', 55: '%', 56: '%', 57: '%', 58: '%', 59: '%', 60: '%', 61: '%', 62: '%', 63: '%', 64: '%'
  }
  
  return unitMap[indicatorId] || ''
}

// 验证审核数据完整性
export const validateAuditData = (auditResults) => {
  const errors = []
  
  // 检查所有指标是否都已评级
  const unratedIndicators = auditResults.filter(item => !item.level || item.level === '待评估')
  if (unratedIndicators.length > 0) {
    errors.push(`还有${unratedIndicators.length}个指标未完成评级`)
  }
  
  // 检查限定性指标
  const limitingIndicators = auditResults.filter(item => item.isLimiting)
  const nonCompliantLimiting = limitingIndicators.filter(item => item.level !== 'I级')
  if (nonCompliantLimiting.length > 0) {
    errors.push(`有${nonCompliantLimiting.length}个限定性指标不达标`)
  }
  
  return {
    isValid: errors.length === 0,
    errors
  }
}

// 计算综合得分
export const calculateOverallScore = (auditResults) => {
  let totalScore = 0
  let validCount = 0
  
  auditResults.forEach(item => {
    if (item.level && item.level !== '待评估') {
      const score = getScoreByLevel(item.level)
      totalScore += score
      validCount++
    }
  })
  
  return validCount > 0 ? totalScore / validCount : 0
}

// 根据评级获取分数
const getScoreByLevel = (level) => {
  const scoreMap = {
    'I级': 4,
    'II级': 3,
    'III级': 2,
    '不达标': 1
  }
  return scoreMap[level] || 0
}

// 根据分数获取综合等级
export const getOverallLevel = (score) => {
  if (score >= 3.5) return 'I级'
  if (score >= 2.5) return 'II级'
  if (score >= 1.5) return 'III级'
  return '不达标'
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
      { label: '基本要求', key: '1' },
      { label: '机械加工及辅助设施', key: '2' },
      { label: '线路与阻焊图形形成(印刷或感光工艺)', key: '3' },
      { label: '板面清洗', key: '4' },
      { label: '蚀刻', key: '5' },
      { label: '电镀与化学镀', key: '6' }
    ]
  },
  {
    label: '能源消耗',
    key: 'energy',
    children: [
      { label: '刚性印制电路单面板(单位产品电耗)', key: '7' },
      { label: '刚性印制电路双面板(单位产品电耗)', key: '8' },
      { label: '刚性印制电路多层板(2+n)层(单位产品电耗)', key: '9' },
      { label: '刚性印制电路HDI板(2+n)层(单位产品电耗)', key: '10' },
      { label: '挠性印制电路单面板(单位产品电耗)', key: '11' },
      { label: '挠性印制电路双面板(单位产品电耗)', key: '12' },
      { label: '挠性印制电路多层板(2+n)层(单位产品电耗)', key: '13' },
      { label: '挠性印制电路HDI板(2+n)层(单位产品电耗)', key: '14' }
    ]
  },
  {
    label: '水资源消耗',
    key: 'water',
    children: [
      { label: '单面板(单位产品新鲜水耗)', key: '15' },
      { label: '双面板(单位产品新鲜水耗)', key: '16' },
      { label: '多层板(2+n)层(单位产品新鲜水耗)', key: '17' },
      { label: 'HDI板(2+n)层(单位产品新鲜水耗)', key: '18' },
      { label: '水资源重复利用率', key: '19' }
    ]
  },
  {
    label: '原/辅料消耗',
    key: 'material',
    children: [
      { label: '刚性印制电路单面板 覆铜板利用率', key: '20' },
      { label: '刚性印制电路双面板 覆铜板利用率', key: '21' },
      { label: '刚性印制电路多层板(2+n)层覆铜板利用率', key: '22' },
      { label: '刚性印制电路HDI板(2+n)层覆铜板利用率', key: '23' },
      { label: '挠性印制电路单面板覆铜板利用率', key: '24' },
      { label: '挠性印制电路双面板 覆铜板利用率', key: '25' },
      { label: '挠性性印制电路多层板(2+n)层覆铜板利用率', key: '26' },
      { label: '挠性印制电路HDI板(2+n)层覆铜板利用率', key: '27' }
    ]
  },
  {
    label: '资源综合利用',
    key: 'utilization',
    children: [
      { label: '金属铜回收率', key: '28' },
      { label: '一般工业固体废物综合利用率', key: '29' }
    ]
  },
  {
    label: '废水的产生与排放',
    key: 'wastewater',
    children: [
      { label: '单面板废水产生量', key: '30' },
      { label: '双面板废水产生量', key: '31' },
      { label: '多层板(2+n)层废水产生量', key: '32' },
      { label: 'HDI板(2+n)层废水产生量', key: '33' },
      { label: '单面板废水中铜产生量', key: '34' },
      { label: '双面板废水中铜产生量', key: '35' },
      { label: '多层板(2+n)层废水中铜产生量', key: '36' },
      { label: 'HDI板(2+n)层废水中铜产生量', key: '37' },
      { label: '单面板废水中COD产生量', key: '38' },
      { label: '双面板废水废水中COD产生量', key: '39' },
      { label: '多层板(2+n)层废水中 COD 产生量', key: '40' },
      { label: 'HDI板(2+n)层废水中 COD 产生量', key: '41' },
      { label: '废水收集与处理', key: '42' }
    ]
  },
  {
    label: '废气的产生与排放',
    key: 'wastegas',
    children: [
      { label: '废气收集与处理', key: '43' }
    ]
  },
  {
    label: '固体废物的产生与排放',
    key: 'solidwaste',
    children: [
      { label: '一般固体废物收集与处理', key: '44' },
      { label: '危险废物收集与处理', key: '45' }
    ]
  },
  {
    label: '噪声的产生与排放',
    key: 'noise',
    children: [
      { label: '噪声', key: '46' }
    ]
  },
  {
    label: '温室气体排放',
    key: 'greenhouse',
    children: [
      { label: '碳减排管理', key: '47' },
      { label: '单位产值碳排放量', key: '48' },
      { label: '碳排放强度', key: '49' }
    ]
  },
  {
    label: '产品特征',
    key: 'product',
    children: [
      { label: '使用无毒无害或低毒低害的生产辅助材料', key: '50' },
      { label: '包装', key: '51' },
      { label: '有害物质限制使用', key: '52' },
      { label: '产品性能', key: '53' }
    ]
  },
  {
    label: '清洁生产管理',
    key: 'management',
    children: [
      { label: '*环保法律法规执行情况', key: '54' },
      { label: '*产业政策符合性', key: '55' },
      { label: '清洁生产管理', key: '56' },
      { label: '清洁生产审核', key: '57' },
      { label: '节能管理', key: '58' },
      { label: '污染物排放监测', key: '59' },
      { label: '*危险化学品管理', key: '60' },
      { label: '计量器具配备情况', key: '61' },
      { label: '*固体废物处理处置', key: '62' },
      { label: '土壤污染隐患排查', key: '63' },
      { label: '运输方式', key: '64' }
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







