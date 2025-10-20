<template>
  <div class="smart-decision-container">
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section">
      <n-card :bordered="false" class="search-card">
        <n-space justify="space-between" align="center">
          <n-space>
            <n-input
              v-model:value="searchKeyword"
              placeholder="搜索决策主题、关键词或相关企业"
              style="width: 300px"
              clearable
            >
              <template #prefix>
                <n-icon><i class="mdi mdi-magnify" /></n-icon>
              </template>
            </n-input>
            <n-select
              v-model:value="selectedType"
              placeholder="决策类型"
              style="width: 150px"
              :options="typeOptions"
              clearable
            />
            <n-select
              v-model:value="selectedStatus"
              placeholder="决策状态"
              style="width: 150px"
              :options="statusOptions"
              clearable
            />
            <n-select
              v-model:value="selectedPriority"
              placeholder="优先级"
              style="width: 150px"
              :options="priorityOptions"
              clearable
            />
            <n-button type="primary" @click="handleSearch">
              <template #icon>
                <n-icon><i class="mdi mdi-magnify" /></n-icon>
              </template>
              搜索
            </n-button>
          </n-space>
          <n-space>
            <n-button @click="handleExport">
              <template #icon>
                <n-icon><i class="mdi mdi-download" /></n-icon>
              </template>
              导出报告
            </n-button>
            <n-button type="primary" @click="handleAdd">
              <template #icon>
                <n-icon><i class="mdi mdi-plus" /></n-icon>
              </template>
              新建决策
            </n-button>
          </n-space>
        </n-space>
      </n-card>
    </div>

    <!-- 统计概览 -->
    <div class="stats-section">
      <n-grid :cols="4" :x-gap="16">
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="总决策数" :value="totalDecisions">
              <template #prefix>
                <n-icon color="#2080f0"><i class="mdi mdi-brain" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="待决策" :value="pendingDecisions">
              <template #prefix>
                <n-icon color="#f0a020"><i class="mdi mdi-clock-outline" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="已决策" :value="completedDecisions">
              <template #prefix>
                <n-icon color="#18a058"><i class="mdi mdi-check-circle" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="高优先级" :value="highPriorityDecisions">
              <template #prefix>
                <n-icon color="#d03050"><i class="mdi mdi-alert-circle" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-section">
      <n-grid :cols="4" :x-gap="16" :y-gap="16">
        <!-- 决策列表 -->
        <n-grid-item :span="3">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">智慧决策管理</span>
                <n-space>
                  <n-button size="small" @click="handleBatchOperation">
                    <template #icon>
                      <n-icon><i class="mdi mdi-cog" /></n-icon>
                    </template>
                    批量操作
                  </n-button>
                  <n-button size="small" @click="handleRefresh">
                    <template #icon>
                      <n-icon><i class="mdi mdi-refresh" /></n-icon>
                    </template>
                    刷新
                  </n-button>
                </n-space>
              </div>
            </template>
            
            <n-data-table
              :columns="decisionColumns"
              :data="filteredDecisions"
              :pagination="paginationConfig"
              :bordered="false"
              :row-key="row => row.id"
              @update:checked-row-keys="handleCheck"
            />
          </n-card>
        </n-grid-item>

        <!-- 决策类型分布 -->
        <n-grid-item>
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">决策类型分布</span>
            </template>
            <div class="type-stats">
              <div v-for="type in typeStats" :key="type.name" class="type-item">
                <div class="type-info">
                  <span class="type-name">{{ type.name }}</span>
                  <span class="type-count">{{ type.count }}</span>
                </div>
                <n-progress
                  :percentage="(type.count / totalDecisions) * 100"
                  :color="type.color"
                  :show-indicator="false"
                  :height="8"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 决策状态分布 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">决策状态分布</span>
            </template>
            <div class="status-distribution">
              <div v-for="status in statusStats" :key="status.name" class="status-item">
                <div class="status-info">
                  <span class="status-name">{{ status.name }}</span>
                  <span class="status-count">{{ status.count }}个</span>
                </div>
                <n-progress
                  :percentage="(status.count / totalDecisions) * 100"
                  :color="status.color"
                  :show-indicator="false"
                  :height="6"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 优先级分布 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">优先级分布</span>
            </template>
            <div class="priority-distribution">
              <div v-for="priority in priorityStats" :key="priority.name" class="priority-item">
                <div class="priority-info">
                  <span class="priority-name">{{ priority.name }}</span>
                  <span class="priority-count">{{ priority.count }}个</span>
                </div>
                <n-progress
                  :percentage="(priority.count / totalDecisions) * 100"
                  :color="priority.color"
                  :show-indicator="false"
                  :height="6"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 决策详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" title="决策详情" style="width: 900px">
      <div v-if="selectedDecision" class="decision-detail">
        <n-tabs type="line" animated>
          <n-tab-pane name="basic" tab="基本信息">
            <n-descriptions :column="2" bordered>
              <n-descriptions-item label="决策主题">
                {{ selectedDecision.title }}
              </n-descriptions-item>
              <n-descriptions-item label="决策类型">
                <n-tag :type="getTypeColor(selectedDecision.type)">{{ selectedDecision.type }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="决策状态">
                <n-tag :type="getStatusType(selectedDecision.status)">{{ selectedDecision.status }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="优先级">
                <n-tag :type="getPriorityType(selectedDecision.priority)">{{ selectedDecision.priority }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="创建时间">
                {{ selectedDecision.createTime }}
              </n-descriptions-item>
              <n-descriptions-item label="截止时间">
                {{ selectedDecision.deadline }}
              </n-descriptions-item>
              <n-descriptions-item label="负责人">
                {{ selectedDecision.owner }}
              </n-descriptions-item>
              <n-descriptions-item label="相关企业">
                {{ selectedDecision.enterprise }}
              </n-descriptions-item>
            </n-descriptions>
          </n-tab-pane>
          <n-tab-pane name="analysis" tab="决策分析">
            <div class="decision-analysis">
              <h4>问题描述</h4>
              <p>{{ selectedDecision.problem }}</p>
              
              <h4>数据分析</h4>
              <div class="data-analysis">
                <n-grid :cols="2" :x-gap="16">
                  <n-grid-item>
                    <n-card title="关键指标" size="small">
                      <div v-for="indicator in selectedDecision.indicators" :key="indicator.name" class="indicator-item">
                        <span class="indicator-name">{{ indicator.name }}</span>
                        <span class="indicator-value">{{ indicator.value }}</span>
                      </div>
                    </n-card>
                  </n-grid-item>
                  <n-grid-item>
                    <n-card title="风险评估" size="small">
                      <div v-for="risk in selectedDecision.risks" :key="risk.name" class="risk-item">
                        <span class="risk-name">{{ risk.name }}</span>
                        <n-tag :type="getRiskType(risk.level)" size="small">{{ risk.level }}</n-tag>
                      </div>
                    </n-card>
                  </n-grid-item>
                </n-grid>
              </div>
              
              <h4>建议方案</h4>
              <ul>
                <li v-for="solution in selectedDecision.solutions" :key="solution">{{ solution }}</li>
              </ul>
            </div>
          </n-tab-pane>
          <n-tab-pane name="history" tab="决策历史">
            <div class="decision-history">
              <n-timeline>
                <n-timeline-item
                  v-for="history in selectedDecision.history"
                  :key="history.id"
                  :title="history.title"
                  :content="history.content"
                  :time="history.time"
                  :type="history.type"
                />
              </n-timeline>
            </div>
          </n-tab-pane>
        </n-tabs>
      </div>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'

defineOptions({ name: '清洁生产智慧决策' })

// 响应式数据
const searchKeyword = ref('')
const selectedType = ref(null)
const selectedStatus = ref(null)
const selectedPriority = ref(null)
const showDetailModal = ref(false)
const selectedDecision = ref(null)
const checkedRowKeys = ref([])

// 筛选选项
const typeOptions = [
  { label: '技术决策', value: 'technology' },
  { label: '投资决策', value: 'investment' },
  { label: '管理决策', value: 'management' },
  { label: '环境决策', value: 'environmental' }
]

const statusOptions = [
  { label: '待决策', value: 'pending' },
  { label: '分析中', value: 'analyzing' },
  { label: '已决策', value: 'completed' },
  { label: '已执行', value: 'executed' }
]

const priorityOptions = [
  { label: '高', value: 'high' },
  { label: '中', value: 'medium' },
  { label: '低', value: 'low' }
]

// 模拟数据
const decisions = ref([
  {
    id: 1,
    title: '钢铁企业清洁生产技术升级决策',
    type: '技术决策',
    status: '分析中',
    priority: '高',
    createTime: '2025-01-10',
    deadline: '2025-02-10',
    owner: '张专家',
    enterprise: '北京钢铁集团有限公司',
    problem: '企业现有生产工艺能耗较高，需要选择合适的技术升级方案。',
    indicators: [
      { name: '能耗水平', value: '85%' },
      { name: '减排效果', value: '70%' },
      { name: '投资回报率', value: '15%' }
    ],
    risks: [
      { name: '技术风险', level: '中' },
      { name: '市场风险', level: '低' },
      { name: '资金风险', level: '高' }
    ],
    solutions: [
      '采用高效节能设备',
      '实施工艺优化',
      '建立能源管理系统'
    ],
    history: [
      { id: 1, title: '创建决策任务', content: '由张专家创建', time: '2025-01-10', type: 'info' },
      { id: 2, title: '开始数据分析', content: '开始收集和分析相关数据', time: '2025-01-12', type: 'success' }
    ]
  },
  {
    id: 2,
    title: '化工企业环保投资决策',
    type: '投资决策',
    status: '已决策',
    priority: '中',
    createTime: '2025-01-05',
    deadline: '2025-01-20',
    owner: '李专家',
    enterprise: '上海化工股份有限公司',
    problem: '企业需要投资环保设施，需要评估不同投资方案的效益。',
    indicators: [
      { name: '投资金额', value: '500万元' },
      { name: '预期收益', value: '200万元/年' },
      { name: '回收期', value: '2.5年' }
    ],
    risks: [
      { name: '技术风险', level: '低' },
      { name: '市场风险', level: '中' },
      { name: '政策风险', level: '低' }
    ],
    solutions: [
      '投资废水处理设施',
      '升级废气处理系统',
      '建立环境监测系统'
    ],
    history: [
      { id: 3, title: '创建决策任务', content: '由李专家创建', time: '2025-01-05', type: 'info' },
      { id: 4, title: '完成数据分析', content: '完成投资效益分析', time: '2025-01-15', type: 'success' },
      { id: 5, title: '决策完成', content: '确定投资方案', time: '2025-01-18', type: 'success' }
    ]
  },
  {
    id: 3,
    title: '工业园区环境管理决策',
    type: '管理决策',
    status: '待决策',
    priority: '高',
    createTime: '2025-01-08',
    deadline: '2025-02-08',
    owner: '王专家',
    enterprise: '深圳高新技术产业园区',
    problem: '园区需要制定统一的环境管理策略，提高整体环境绩效。',
    indicators: [
      { name: '环境绩效', value: '75%' },
      { name: '企业满意度', value: '80%' },
      { name: '管理效率', value: '70%' }
    ],
    risks: [
      { name: '管理风险', level: '中' },
      { name: '协调风险', level: '高' },
      { name: '执行风险', level: '中' }
    ],
    solutions: [
      '建立统一环境管理体系',
      '制定环境管理标准',
      '加强环境监测'
    ],
    history: [
      { id: 6, title: '创建决策任务', content: '由王专家创建', time: '2025-01-08', type: 'info' }
    ]
  }
])

// 分页配置
const paginationConfig = {
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50],
  showQuickJumper: true
}

// 表格列定义
const decisionColumns = [
  {
    type: 'selection'
  },
  {
    title: '决策主题',
    key: 'title',
    width: 250,
    ellipsis: { tooltip: true }
  },
  {
    title: '决策类型',
    key: 'type',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: getTypeColor(row.type) }, { default: () => row.type })
  },
  {
    title: '决策状态',
    key: 'status',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: getStatusType(row.status) }, { default: () => row.status })
  },
  {
    title: '优先级',
    key: 'priority',
    width: 100,
    render: (row) => h('n-tag', { size: 'small', type: getPriorityType(row.priority) }, { default: () => row.priority })
  },
  {
    title: '负责人',
    key: 'owner',
    width: 100
  },
  {
    title: '相关企业',
    key: 'enterprise',
    width: 200,
    ellipsis: { tooltip: true }
  },
  {
    title: '创建时间',
    key: 'createTime',
    width: 120
  },
  {
    title: '操作',
    key: 'actions',
    width: 150,
    fixed: 'right',
    render: (row) => [
      h('n-button', {
        size: 'small',
        type: 'primary',
        style: 'margin-right: 8px',
        onClick: () => viewDetail(row)
      }, { default: () => '查看' }),
      h('n-button', {
        size: 'small',
        type: 'info',
        onClick: () => editDecision(row)
      }, { default: () => '编辑' })
    ]
  }
]

// 计算属性
const totalDecisions = computed(() => decisions.value.length)
const pendingDecisions = computed(() => decisions.value.filter(d => d.status === '待决策').length)
const completedDecisions = computed(() => decisions.value.filter(d => d.status === '已决策').length)
const highPriorityDecisions = computed(() => decisions.value.filter(d => d.priority === '高').length)

const filteredDecisions = computed(() => {
  let filtered = decisions.value
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(d => 
      d.title.toLowerCase().includes(keyword) || 
      d.enterprise.toLowerCase().includes(keyword)
    )
  }
  
  if (selectedType.value) {
    filtered = filtered.filter(d => d.type === selectedType.value)
  }
  
  if (selectedStatus.value) {
    filtered = filtered.filter(d => d.status === selectedStatus.value)
  }
  
  if (selectedPriority.value) {
    filtered = filtered.filter(d => d.priority === selectedPriority.value)
  }
  
  return filtered
})

const typeStats = computed(() => {
  const stats = {}
  decisions.value.forEach(decision => {
    stats[decision.type] = (stats[decision.type] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050'][index % 4]
  }))
})

const statusStats = computed(() => {
  const stats = {}
  decisions.value.forEach(decision => {
    stats[decision.status] = (stats[decision.status] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#f0a020', '#18a058', '#36ad6a', '#2080f0'][index % 4]
  }))
})

const priorityStats = computed(() => {
  const stats = {}
  decisions.value.forEach(decision => {
    stats[decision.priority] = (stats[decision.priority] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#d03050', '#f0a020', '#18a058'][index % 3]
  }))
})

// 方法
const handleSearch = () => {
  console.log('搜索决策:', { searchKeyword: searchKeyword.value, selectedType: selectedType.value, selectedStatus: selectedStatus.value, selectedPriority: selectedPriority.value })
}

const handleAdd = () => {
  console.log('新建决策')
}

const handleExport = () => {
  console.log('导出报告')
}

const handleBatchOperation = () => {
  console.log('批量操作:', checkedRowKeys.value)
}

const handleRefresh = () => {
  console.log('刷新数据')
}

const handleCheck = (keys) => {
  checkedRowKeys.value = keys
}

const viewDetail = (decision) => {
  selectedDecision.value = decision
  showDetailModal.value = true
}

const editDecision = (decision) => {
  console.log('编辑决策:', decision)
}

const getTypeColor = (type) => {
  const typeMap = {
    '技术决策': 'info',
    '投资决策': 'success',
    '管理决策': 'warning',
    '环境决策': 'error'
  }
  return typeMap[type] || 'default'
}

const getStatusType = (status) => {
  const statusMap = {
    '待决策': 'warning',
    '分析中': 'info',
    '已决策': 'success',
    '已执行': 'default'
  }
  return statusMap[status] || 'default'
}

const getPriorityType = (priority) => {
  const priorityMap = {
    '高': 'error',
    '中': 'warning',
    '低': 'info'
  }
  return priorityMap[priority] || 'default'
}

const getRiskType = (level) => {
  const riskMap = {
    '高': 'error',
    '中': 'warning',
    '低': 'success'
  }
  return riskMap[level] || 'default'
}

onMounted(() => {
  console.log('清洁生产智慧决策模块已加载')
})
</script>

<style scoped>
.smart-decision-container {
  padding: 16px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

.search-filter-section {
  margin-bottom: 16px;
}

.search-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stats-section {
  margin-bottom: 16px;
}

.stat-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.content-section {
  margin-bottom: 16px;
}

.content-card {
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--primary-color);
  margin-bottom: 16px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.type-stats {
  padding: 16px 0;
}

.type-item {
  margin-bottom: 16px;
}

.type-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.type-name {
  font-size: 14px;
  color: #666;
}

.type-count {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.status-distribution,
.priority-distribution {
  padding: 16px 0;
}

.status-item,
.priority-item {
  margin-bottom: 12px;
}

.status-info,
.priority-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.status-name,
.priority-name {
  font-size: 13px;
  color: #666;
}

.status-count,
.priority-count {
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.decision-detail {
  padding: 16px 0;
}

.decision-analysis h4 {
  margin: 16px 0 8px 0;
  color: #333;
  font-size: 16px;
}

.decision-analysis p {
  margin-bottom: 12px;
  line-height: 1.6;
  color: #666;
}

.decision-analysis ul {
  margin-bottom: 12px;
  padding-left: 20px;
}

.decision-analysis li {
  margin-bottom: 4px;
  line-height: 1.6;
  color: #666;
}

.data-analysis {
  margin: 16px 0;
}

.indicator-item,
.risk-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  padding: 4px 0;
}

.indicator-name,
.risk-name {
  font-size: 14px;
  color: #666;
}

.indicator-value {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.decision-history {
  padding: 16px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .smart-decision-container {
    padding: 8px;
  }
  
  .stats-section .n-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .content-section .n-grid {
    grid-template-columns: 1fr;
  }
}
</style>
