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
      
      <!-- 审核进度图表 -->
      <div class="audit-chart">
        <div class="score-circle">
          <n-progress 
            type="circle" 
            :percentage="summary.totalScore" 
            :color="getProgressColor(summary.totalScore)"
            :size="140"
            :stroke-width="10"
          >
            <div class="score-content">
              <div class="score-number">{{ summary.totalScore.toFixed(1) }}分</div>
            </div>
          </n-progress>
        </div>
        <div class="chart-legend mt-4">
          <n-space>
            <n-tag type="success">I级 (≥90分)</n-tag>
            <n-tag type="info">II级 (80-89分)</n-tag>
            <n-tag type="warning">III级 (60-79分)</n-tag>
            <n-tag type="error">不达标 (<60分)</n-tag>
          </n-space>
        </div>
      </div>
    </n-card>

    <!-- 审核操作栏 -->
    <n-card class="mb-4">
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
    <n-card>
      <n-data-table
        :columns="columns"
        :data="auditTreeData"
        :row-key="row => row.key"
        :default-expand-all="true"
        :pagination="false"
        :loading="tableLoading"
        :cascade="false"
      >
      </n-data-table>
    </n-card>
    
    <!-- 推荐方案弹窗 -->
    <n-modal v-model:show="showSchemeModal">
      <n-card style="width: 800px" title="推荐改进方案">
        <div v-for="scheme in currentSchemes" :key="scheme.id" class="scheme-item mb-4">
          <div class="scheme-header">
            <h4>{{ scheme.label }}</h4>
            <n-tag :type="getSchemeTypeTag(scheme.preview.type)" size="small">
              {{ scheme.preview.type }}
            </n-tag>
          </div>
          <div class="scheme-content">
            <p><strong>方案描述：</strong>{{ scheme.preview.description }}</p>
            <p><strong>解决问题：</strong>{{ scheme.preview.problemSolved }}</p>
            <div class="benefits-grid">
              <div class="benefit-item">
                <strong>经济效益：</strong>{{ scheme.preview.economicBenefit }}
              </div>
              <div class="benefit-item">
                <strong>环境效益：</strong>{{ scheme.preview.environmentalBenefit }}
              </div>
              <div class="benefit-item">
                <strong>投资额：</strong>{{ scheme.preview.investment }}
              </div>
              <div class="benefit-item">
                <strong>回收期：</strong>{{ scheme.preview.paybackPeriod }}
              </div>
            </div>
            <p><strong>实施难度：</strong>{{ scheme.preview.implementationDifficulty }}</p>
          </div>
        </div>
      </n-card>
    </n-modal>

    <!-- 模块导航按钮 -->
    <div class="module-navigation mt-4">
      <n-space justify="space-between">
        <n-button @click="goToPrevious">
          <template #icon>
            <TheIcon icon="carbon:arrow-left" />
          </template>
          预审核
        </n-button>
        <n-button type="primary" @click="goToNext">
          方案库
          <template #icon>
            <TheIcon icon="carbon:arrow-right" />
          </template>
        </n-button>
      </n-space>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'
import { 
  NCard, 
  NDataTable,
  NButton,
  NSpace,
  NGrid,
  NGi,
  NStatistic,
  NTag,
  NModal,
  NSelect,
  NProgress,
  NTooltip
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import { mockDetailApi } from '@/mock/steel-detail'
import QualitativeIndicator from './components/QualitativeIndicator.vue'
import QuantitativeIndicator from './components/QuantitativeIndicator.vue'
import LimitingIndicator from './components/LimitingIndicator.vue'

defineOptions({ name: '钢铁审核' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 导航函数
const goToPrevious = () => {
  emit('navigate', 'pre-audit')
}

const goToNext = () => {
  emit('navigate', 'scheme-library')
}

// 数据状态
const loading = ref(false)
const tableLoading = ref(false)
const showSchemeModal = ref(false)
const currentSchemes = ref([])

// 评级选项
const levelOptions = [
  { label: 'I级', value: 'I级' },
  { label: 'II级', value: 'II级' },
  { label: 'III级', value: 'III级' },
  { label: '不达标', value: '不达标' }
]

// 审核汇总数据
const summary = ref({
  totalScore: 0,
  overallLevel: '未评估',
  improvementItems: 0,
  limitingIndicators: 0
})

// 审核树数据
const auditTreeData = ref([])

// 从mock数据中获取指标
const indicators = ref([])

// 表格列定义
const columns = [
  {
    title: '序号',
    key: 'index',
    width: 80,
    align: 'center',
    render: (row) => {
      if (row.isCategory) return row.chineseIndex
      return row.id
    }
  },
  {
    title: '一级指标',
    key: 'primaryIndicator',
    width: 200,
    tree: true,
    render: (row) => {
      if (row.isCategory) {
        // 一级指标行：显示一级指标名称（加粗）
        return h('span', { 
          style: { 
            fontWeight: 'bold',
            fontSize: '14px',
            color: '#262626'
          } 
        }, row.name)
      } else {
        // 二级指标行：显示对应的一级指标名称（不加粗，靠左对齐）
        const parentCategory = auditTreeData.value.find(cat => 
          cat.children && cat.children.some(child => child.id === row.id)
        )
        return parentCategory ? h('span', { 
          style: { 
            textAlign: 'left',
            fontSize: '13px',
            color: '#595959'
          } 
        }, parentCategory.name) : ''
      }
    }
  },
  {
    title: '二级指标',
    key: 'secondaryIndicator',
    width: 250,
    render: (row) => {
      if (row.isCategory) return ''
      return h('div', { class: 'indicator-name' }, [
        row.isLimiting ? h('span', { class: 'limiting-indicator' }, '*') : null,
        row.name
      ])
    }
  },
  {
    title: '当前值',
    key: 'currentValue',
    width: 150,
    render: (row) => {
      if (row.isCategory) return ''
      return h(QuantitativeIndicator, {
        indicator: row,
        onUpdate: (updatedIndicator) => {
          const index = indicators.value.findIndex(indicator => indicator.id === updatedIndicator.id)
          if (index > -1) {
            indicators.value[index] = updatedIndicator
            calculateSummary()
          }
        }
      })
    }
  },
  {
    title: '指标权重',
    key: 'weight',
    width: 100,
    render: (row) => {
      if (row.isCategory) return ''
      return h('span', `${row.weight}%`)
    }
  },
  {
    title: '评级',
    key: 'level',
    width: 120,
    render: (row) => {
      if (row.isCategory) return ''
      return h(NSelect, {
        value: row.level,
        options: levelOptions,
        placeholder: '请选择评级',
        size: 'small',
        style: { width: '100px' },
        onUpdateValue: (value) => handleIndicatorUpdate(row.id, value)
      })
    }
  },
  {
    title: '推荐方案',
    key: 'schemes',
    width: 300,
    render: (row) => {
      if (row.isCategory) return ''
      return h(NSelect, {
        value: row.selectedSchemes,
        options: row.recommendedSchemes,
        placeholder: '选择方案',
        size: 'small',
        style: { width: '250px' },
        clearable: true,
        multiple: true,
        maxTagCount: 2,
        onUpdateValue: (value) => handleIndicatorUpdate(row.id, null, value),
        renderLabel: ({ option }) => {
          return h(NTooltip, {}, {
            trigger: () => h('span', option.label),
            default: () => h('div', { style: 'max-width: 300px; white-space: normal;' }, [
              h('p', `类型: ${option.preview.type}`),
              h('p', `描述: ${option.preview.description}`),
              h('p', `解决问题: ${option.preview.problemSolved}`),
              h('p', `经济效益: ${option.preview.economicBenefit}`),
              h('p', `环境效益: ${option.preview.environmentalBenefit}`),
              h('p', `投资额: ${option.preview.investment}`),
              h('p', `回收期: ${option.preview.paybackPeriod}`),
              h('p', `实施难度: ${option.preview.implementationDifficulty}`)
            ])
          })
        }
      })
    }
  }
]

// 构建树形数据
const buildTreeData = () => {
  const categories = {}
  
  indicators.value.forEach(indicator => {
    if (!categories[indicator.category]) {
      categories[indicator.category] = {
        key: indicator.category,
        name: indicator.category,
        isCategory: true,
        children: []
      }
    }
    categories[indicator.category].children.push({
      key: `indicator-${indicator.id}`,
      ...indicator
    })
  })
  
  return Object.values(categories)
}

// 计算汇总数据
const calculateSummary = () => {
  const totalWeight = indicators.value.reduce((sum, indicator) => sum + indicator.weight, 0)
  const weightedScore = indicators.value.reduce((sum, indicator) => sum + (indicator.score * indicator.weight), 0)
  const totalScore = totalWeight > 0 ? weightedScore / totalWeight : 0
  
  let overallLevel = '不达标'
  if (totalScore >= 90) overallLevel = 'I级'
  else if (totalScore >= 80) overallLevel = 'II级'
  else if (totalScore >= 60) overallLevel = 'III级'
  
  const improvementItems = indicators.value.filter(indicator => 
    indicator.score < 80 && !indicator.isLimiting
  ).length
  
  const limitingIndicators = indicators.value.filter(indicator => 
    indicator.isLimiting && indicator.score < 100
  ).length
  
  summary.value = {
    totalScore,
    overallLevel,
    improvementItems,
    limitingIndicators
  }
}

// 获取等级标签类型
const getLevelTagType = (level) => {
  const types = {
    'I级': 'success',
    'II级': 'info',
    'III级': 'warning',
    '不达标': 'error',
    '符合': 'success',
    '不符合': 'error'
  }
  return types[level] || 'default'
}

// 获取进度条颜色
const getProgressColor = (score) => {
  if (score >= 90) return '#18a058'
  if (score >= 80) return '#2080f0'
  if (score >= 60) return '#f0a020'
  return '#d03050'
}

// 获取方案类型标签颜色
const getSchemeTypeTag = (type) => {
  const typeMap = {
    '工艺改进': 'success',
    '设备升级': 'info',
    '管理优化': 'warning',
    '技术革新': 'error'
  }
  return typeMap[type] || 'default'
}

// 是否可以提交
const canSubmit = computed(() => {
  return indicators.value.every(indicator => indicator.score > 0)
})

// 处理指标更新
const handleIndicatorUpdate = (indicatorId, level, selectedSchemes) => {
  const index = indicators.value.findIndex(indicator => indicator.id === indicatorId)
  if (index > -1) {
    if (level !== undefined) {
      indicators.value[index].level = level
      // 根据等级计算得分
      const scoreMap = { 'I级': 100, 'II级': 80, 'III级': 60, '不达标': 0 }
      indicators.value[index].score = scoreMap[level] || 0
    }
    if (selectedSchemes !== undefined) {
      indicators.value[index].selectedSchemes = selectedSchemes
    }
    calculateSummary()
  }
}

// 自动计算评估
const handleAutoCalculate = () => {
  // 这里可以根据预审核数据自动计算指标值
  window.$message.info('自动计算功能待实现')
}

// 重置审核
const handleResetAudit = () => {
  indicators.value.forEach(indicator => {
    indicator.level = null
    indicator.score = 0
    indicator.currentValue = null
    indicator.selectedSchemes = []
  })
  calculateSummary()
  window.$message.success('审核已重置')
}

// 提交审核结果
const handleSubmitAudit = async () => {
  try {
    loading.value = true
    await mockDetailApi.submitAuditResults(props.enterpriseId, {
      indicators: indicators.value,
      summary: summary.value
    })
    window.$message.success('审核结果提交成功')
    emit('update', { indicators: indicators.value, summary: summary.value })
  } catch (error) {
    console.error('提交审核结果失败:', error)
    window.$message.error('提交审核结果失败')
  } finally {
    loading.value = false
  }
}

// 获取审核数据
const fetchAuditData = async () => {
  try {
    tableLoading.value = true
    const response = await mockDetailApi.getAuditResults(props.enterpriseId)
    const data = response.data
    
    // 从mock数据中获取指标
    indicators.value = [...data]
    
    // 为每个指标加载推荐方案
    for (let indicator of indicators.value) {
      try {
        const schemesResponse = await mockDetailApi.getRecommendedSchemes(props.enterpriseId, indicator.id)
        indicator.recommendedSchemes = schemesResponse.data || []
      } catch (error) {
        console.warn(`获取指标${indicator.id}的推荐方案失败:`, error)
        indicator.recommendedSchemes = []
      }
    }
    
    auditTreeData.value = buildTreeData()
    calculateSummary()
  } catch (error) {
    console.error('获取审核数据失败:', error)
    window.$message.error('获取审核数据失败')
  } finally {
    tableLoading.value = false
  }
}

onMounted(() => {
  auditTreeData.value = buildTreeData()
  calculateSummary()
  fetchAuditData()
})
</script>

<style scoped>
.audit-page {
  min-height: 100vh;
}

.category-name {
  font-weight: 600;
  color: var(--n-text-color);
}

.indicator-name {
  color: var(--n-text-color-secondary);
}

.score-text {
  font-weight: 600;
  color: var(--n-text-color);
}

.audit-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px 0;
}

.score-circle {
  margin-bottom: 16px;
}

.score-content {
  text-align: center;
}

.score-number {
  font-size: 18px;
  font-weight: 600;
  color: var(--n-text-color);
}

.chart-legend {
  text-align: center;
}

/* 方案预览样式 */
.scheme-item {
  border: 1px solid #e8eaec;
  border-radius: 8px;
  padding: 16px;
  background: #fafafa;
}

.scheme-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.scheme-header h4 {
  margin: 0;
  color: #262626;
  font-size: 16px;
  font-weight: 600;
}

.scheme-content p {
  margin: 8px 0;
  line-height: 1.6;
  color: #595959;
}

.benefits-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin: 12px 0;
}

.benefit-item {
  padding: 8px;
  background: white;
  border-radius: 4px;
  border: 1px solid #e8eaec;
  font-size: 14px;
  line-height: 1.5;
}

.benefit-item strong {
  color: #262626;
}
</style>
