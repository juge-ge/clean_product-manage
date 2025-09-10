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
            :pagination="false"
          >
            <template #action="{ row }">
              <n-space>
                <n-button 
                  size="small" 
                  type="primary"
                  @click="handleShowSchemeModal(row)"
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
              </n-space>
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

    <!-- 审核结果汇总 -->
    <n-card title="审核结果汇总" class="mt-4">
      <n-grid :cols="4" :x-gap="16">
        <n-statistic label="总体评分" :value="auditResults.overall.totalScore" suffix="分" />
        <n-statistic label="审核等级" :value="auditResults.overall.level" />
        <n-statistic label="审核状态" :value="auditResults.overall.status" />
        <n-statistic label="审核日期" :value="auditResults.overall.date" />
      </n-grid>
      
      <div class="mt-4">
        <h4>分类评估结果</h4>
        <n-grid :cols="3" :x-gap="16">
          <n-card 
            v-for="category in auditResults.categories"
            :key="category.name"
            class="category-card"
          >
            <div class="category-header">
              <h5>{{ category.name }}</h5>
              <n-tag :type="getCategoryType(category.score)">
                {{ category.score }}分
              </n-tag>
            </div>
            <div class="category-items">
              <div 
                v-for="item in category.items"
                :key="item.name"
                class="category-item"
              >
                <span class="item-name">{{ item.name }}</span>
                <span class="item-score">{{ item.score }}分</span>
              </div>
            </div>
          </n-card>
        </n-grid>
      </div>
    </n-card>

    <!-- 方案详情弹窗 -->
    <CrudModal
      v-model:visible="showSchemeModal"
      title="方案详情"
      :show-footer="false"
    >
      <div v-if="selectedScheme">
        <h4>{{ selectedScheme.title }}</h4>
        <p><strong>方案类型：</strong>{{ selectedScheme.type }}</p>
        <p><strong>方案描述：</strong>{{ selectedScheme.description }}</p>
        <p><strong>实施方案：</strong></p>
        <pre class="scheme-content">{{ selectedScheme.implementation }}</pre>
        <p><strong>预期效果：</strong>{{ selectedScheme.expectedEffect }}</p>
        <p><strong>投资估算：</strong>{{ selectedScheme.investment }}万元</p>
        <p><strong>投资回收期：</strong>{{ selectedScheme.paybackPeriod }}年</p>
      </div>
    </CrudModal>

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
import { ref, computed, onMounted } from 'vue'
import { 
  NCard, 
  NTabs, 
  NTabPane,
  NDataTable,
  NButton,
  NSpace,
  NGrid,
  NStatistic,
  NTag
} from 'naive-ui'
import CrudModal from '@/components/table/CrudModal.vue'
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
const auditResults = ref({
  overall: {
    totalScore: 0,
    level: '',
    status: '',
    date: ''
  },
  categories: []
})

const auditCategories = ref([
  { id: 'production', name: '生产工艺' },
  { id: 'resource', name: '资源消耗' },
  { id: 'environment', name: '环境保护' }
])

const showSchemeModal = ref(false)
const selectedScheme = ref(null)

// 获取审核数据
const fetchAuditData = async () => {
  try {
    const response = await mockDetailApi.getAuditResults(props.enterpriseId)
    auditResults.value = response.data
  } catch (error) {
    console.error('获取审核数据失败:', error)
    window.$message.error('获取审核数据失败')
  }
}

// 获取审核列配置
const getAuditColumns = (categoryId) => {
  const baseColumns = [
    {
      title: '指标名称',
      key: 'name',
      width: 200
    },
    {
      title: '评分',
      key: 'score',
      width: 100,
      render: (row) => {
        return h('span', { class: 'score-text' }, `${row.score}分`)
      }
    },
    {
      title: '评价',
      key: 'comment',
      ellipsis: { tooltip: true }
    }
  ]
  
  if (categoryId === 'production') {
    baseColumns.splice(1, 0, {
      title: '工艺先进性',
      key: 'advanced',
      width: 120,
      render: (row) => {
        return h('n-tag', { type: row.advanced ? 'success' : 'warning' }, 
          row.advanced ? '先进' : '一般')
      }
    })
  }
  
  baseColumns.push({
    title: '操作',
    key: 'action',
    width: 150,
    render: (row) => h('template', { slot: 'action' }, { row })
  })
  
  return baseColumns
}

// 获取审核数据
const getAuditData = (categoryId) => {
  const category = auditResults.value.categories.find(c => c.id === categoryId)
  return category ? category.items : []
}

// 获取分类类型
const getCategoryType = (score) => {
  if (score >= 90) return 'success'
  if (score >= 80) return 'info'
  if (score >= 70) return 'warning'
  return 'error'
}

// 显示方案详情
const handleShowSchemeModal = (row) => {
  selectedScheme.value = {
    title: '电镀生产线节能改造',
    type: '节能降耗',
    description: '通过更换高效整流器、优化电镀参数等措施降低能耗',
    implementation: '1. 更换高效整流器\n2. 优化电镀工艺参数\n3. 安装能耗监测系统',
    expectedEffect: '预计可降低电耗15%，年节约成本50万元',
    investment: 200,
    paybackPeriod: 4
  }
  showSchemeModal.value = true
}

// 编辑方案
const editScheme = (row) => {
  window.$message.info('编辑方案功能待开发')
}

// 生成报告
const generateReport = async () => {
  try {
    await mockDetailApi.generateReport(props.enterpriseId, auditResults.value)
    window.$message.success('评估报告生成成功')
    emit('update', auditResults.value)
  } catch (error) {
    console.error('生成报告失败:', error)
    window.$message.error('生成报告失败')
  }
}

// 是否可以生成报告
const canGenerateReport = computed(() => {
  return auditResults.value.categories.length > 0 && 
         auditResults.value.overall.totalScore > 0
})

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
.audit-module {
  padding: 16px;
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
