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
        <n-progress 
          type="circle" 
          :percentage="summary.totalScore" 
          :color="getProgressColor(summary.totalScore)"
          :stroke-width="8"
        >
          <span class="progress-text">{{ summary.totalScore.toFixed(1) }}分</span>
        </n-progress>
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
  NProgress
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import { mockDetailApi } from '@/mock/pcb-detail'

defineOptions({ name: 'PCB审核' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 数据状态
const loading = ref(false)
const showSchemeModal = ref(false)
const currentSchemes = ref([])

// 审核汇总数据
const summary = ref({
  totalScore: 0,
  overallLevel: '未评估',
  improvementItems: 0,
  limitingIndicators: 0
})

// 审核树数据
const auditTreeData = ref([])

// 64项指标的具体定义
const indicators = [
  // 生产工艺与装备要求 (1-6)
  {
    id: 1,
    name: '刚性单面板生产工艺',
    category: '生产工艺与装备要求',
    type: 'qualitative',
    level: null,
    score: 0
  },
  {
    id: 2,
    name: '刚性双面板生产工艺',
    category: '生产工艺与装备要求',
    type: 'qualitative',
    level: null,
    score: 0
  },
  // ... 其他62项指标
]

// 表格列定义
const columns = [
  {
    title: '序号',
    key: 'id',
    width: 80
  },
  {
    title: '指标名称',
    key: 'name',
    width: 250
  },
  {
    title: '类别',
    key: 'category',
    width: 150
  },
  {
    title: '现状值',
    key: 'currentValue',
    width: 120,
    render: (row) => {
      if (row.type === 'quantitative') {
        return row.currentValue ? `${row.currentValue} ${row.unit || ''}` : '-'
      }
      return '-'
    }
  },
  {
    title: '等级',
    key: 'level',
    width: 120,
    render: (row) => {
      if (row.type === 'qualitative' || row.type === 'limiting') {
        return h(NSelect, {
          value: row.level,
          options: getLevelOptions(row.type),
          placeholder: '请选择等级',
          onUpdateValue: (value) => updateIndicatorLevel(row.id, value)
        })
      } else if (row.type === 'quantitative') {
        const levelType = getLevelType(row.level)
        return h(NTag, { type: levelType }, row.level || '未评估')
      }
      return '-'
    }
  },
  {
    title: '得分',
    key: 'score',
    width: 100,
    render: (row) => {
      return h('span', { class: 'score-text' }, `${row.score || 0}分`)
    }
  },
  {
    title: '改进措施',
    key: 'schemes',
    width: 120,
    render: (row) => {
      if (row.level !== 'I级' && row.recommendedSchemes?.length > 0) {
        return h(NButton, {
          size: 'small',
          type: 'primary',
          onClick: () => showRecommendedSchemes(row.recommendedSchemes)
        }, '查看方案')
      }
      return '-'
    }
  }
]

// 获取等级选项
const getLevelOptions = (type) => {
  if (type === 'limiting') {
    return [
      { label: '符合', value: 'I级' },
      { label: '不符合', value: '不达标' }
    ]
  }
  return [
    { label: 'I级', value: 'I级' },
    { label: 'II级', value: 'II级' },
    { label: 'III级', value: 'III级' },
    { label: '不达标', value: '不达标' }
  ]
}

// 获取等级类型
const getLevelType = (level) => {
  const types = {
    'I级': 'success',
    'II级': 'info', 
    'III级': 'warning',
    '不达标': 'error'
  }
  return types[level] || 'default'
}

// 获取汇总等级标签类型
const getLevelTagType = (level) => {
  return getLevelType(level)
}

// 更新指标等级
const updateIndicatorLevel = async (indicatorId, level) => {
  try {
    const indicator = auditTreeData.value.find(item => item.id === indicatorId)
    if (indicator) {
      indicator.level = level
      indicator.score = calculateScore(level)
      
      // 如果是限定性指标不达标，显示警告
      if (indicator.type === 'limiting' && level === '不达标') {
        window.$dialog.warning({
          title: '限定性指标警告',
          content: '存在限定性指标不达标，总评级不得高于III级',
          positiveText: '确认'
        })
      }
      
      // 更新改进措施
      if (level !== 'I级') {
        indicator.recommendedSchemes = await getRecommendedSchemes(indicatorId)
      } else {
        indicator.recommendedSchemes = []
      }
      
      // 重新计算汇总数据
      calculateSummary()
    }
  } catch (error) {
    console.error('更新指标等级失败:', error)
    window.$message.error('更新指标等级失败')
  }
}

// 计算分数
const calculateScore = (level) => {
  const scores = {
    'I级': 100,
    'II级': 80,
    'III级': 60,
    '不达标': 0
  }
  return scores[level] || 0
}

// 获取推荐方案
const getRecommendedSchemes = async (indicatorId) => {
  try {
    const response = await mockDetailApi.getRecommendedSchemes(props.enterpriseId, indicatorId)
    return response.data
  } catch (error) {
    console.error('获取推荐方案失败:', error)
    return []
  }
}

// 显示推荐方案
const showRecommendedSchemes = (schemes) => {
  currentSchemes.value = schemes
  showSchemeModal.value = true
}

// 计算汇总数据
const calculateSummary = () => {
  const totalScore = auditTreeData.value.reduce((sum, item) => sum + (item.score || 0), 0)
  const avgScore = auditTreeData.value.length > 0 ? totalScore / auditTreeData.value.length : 0
  
  let overallLevel = '未评估'
  if (avgScore >= 90) overallLevel = 'I级'
  else if (avgScore >= 80) overallLevel = 'II级' 
  else if (avgScore >= 60) overallLevel = 'III级'
  else overallLevel = '不达标'
  
  // 检查限定性指标
  const limitingIndicators = auditTreeData.value.filter(item => 
    item.type === 'limiting' && item.level === '不达标'
  ).length
  
  if (limitingIndicators > 0 && overallLevel !== '不达标') {
    overallLevel = 'III级'
  }
  
  const improvementItems = auditTreeData.value.filter(item => 
    item.level && item.level !== 'I级'
  ).length
  
  summary.value = {
    totalScore: avgScore,
    overallLevel,
    improvementItems,
    limitingIndicators
  }
}

// 获取进度条颜色
const getProgressColor = (score) => {
  if (score >= 90) return '#18a058'
  if (score >= 80) return '#2080f0'  
  if (score >= 60) return '#f0a020'
  return '#d03050'
}

// 获取审核数据
const fetchAuditData = async () => {
  try {
    loading.value = true
    const response = await mockDetailApi.getAuditResults(props.enterpriseId)
    auditTreeData.value = response.data || indicators
    calculateSummary()
  } catch (error) {
    console.error('获取审核数据失败:', error)
    window.$message.error('获取审核数据失败')
    auditTreeData.value = indicators
  } finally {
    loading.value = false
  }
}

// 导航方法
const goToPrevious = () => {
  emit('navigate', 'pre-audit')
}

const goToNext = () => {
  emit('navigate', 'scheme-library')
}

onMounted(() => {
  fetchAuditData()
})
</script>

<style scoped>
.audit-page {
  background: #f8f9fa;
}

.audit-chart {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.progress-text {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.chart-legend {
  display: flex;
  justify-content: center;
}

.category-card {
  transition: all 0.3s ease;
}

.category-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.category-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.category-header h5 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.category-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid var(--n-border-color);
}

.category-item:last-child {
  border-bottom: none;
}

.item-name {
  font-size: 14px;
  color: var(--n-text-color);
}

.item-score {
  font-size: 14px;
  font-weight: 600;
  color: var(--n-color-primary);
}

.scheme-content {
  background: var(--n-color-light-hover);
  padding: 12px;
  border-radius: 4px;
  white-space: pre-wrap;
  font-size: 14px;
  line-height: 1.5;
}

.score-text {
  font-weight: 600;
  color: var(--n-color-primary);
}

:deep(.n-statistic) {
  text-align: center;
}

:deep(.n-statistic .n-statistic-value) {
  font-size: 20px;
  font-weight: 600;
}

:deep(.n-statistic .n-statistic-label) {
  font-size: 14px;
  color: var(--n-text-color-secondary);
}
</style>
