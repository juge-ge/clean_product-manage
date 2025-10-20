<template>
  <div class="industry-container">
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section">
      <n-card :bordered="false" class="search-card">
        <n-space justify="space-between" align="center">
          <n-space>
            <n-input
              v-model:value="searchKeyword"
              placeholder="搜索行业名称或关键词"
              style="width: 300px"
              clearable
            >
              <template #prefix>
                <n-icon><i class="mdi mdi-magnify" /></n-icon>
              </template>
            </n-input>
            <n-select
              v-model:value="selectedCategory"
              placeholder="行业分类"
              style="width: 150px"
              :options="categoryOptions"
              clearable
            />
            <n-select
              v-model:value="selectedStatus"
              placeholder="发展状态"
              style="width: 150px"
              :options="statusOptions"
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
              导出数据
            </n-button>
            <n-button type="primary" @click="handleAdd">
              <template #icon>
                <n-icon><i class="mdi mdi-plus" /></n-icon>
              </template>
              新增行业
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
            <n-statistic label="总行业数" :value="totalIndustries">
              <template #prefix>
                <n-icon color="#2080f0"><i class="mdi mdi-factory" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="重点行业" :value="keyIndustries">
              <template #prefix>
                <n-icon color="#d03050"><i class="mdi mdi-star" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="传统行业" :value="traditionalIndustries">
              <template #prefix>
                <n-icon color="#f0a020"><i class="mdi mdi-cog" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="新兴行业" :value="emergingIndustries">
              <template #prefix>
                <n-icon color="#18a058"><i class="mdi mdi-lightning-bolt" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-section">
      <n-grid :cols="4" :x-gap="16" :y-gap="16">
        <!-- 行业列表 -->
        <n-grid-item :span="3">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">行业管理</span>
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
              :columns="industryColumns"
              :data="filteredIndustries"
              :pagination="paginationConfig"
              :bordered="false"
              :row-key="row => row.id"
              @update:checked-row-keys="handleCheck"
            />
          </n-card>
        </n-grid-item>

        <!-- 行业分类统计 -->
        <n-grid-item>
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">行业分类统计</span>
            </template>
            <div class="category-stats">
              <div v-for="category in categoryStats" :key="category.name" class="category-item">
                <div class="category-info">
                  <span class="category-name">{{ category.name }}</span>
                  <span class="category-count">{{ category.count }}</span>
                </div>
                <n-progress
                  :percentage="(category.count / totalIndustries) * 100"
                  :color="category.color"
                  :show-indicator="false"
                  :height="8"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 发展状态分布 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">发展状态分布</span>
            </template>
            <div class="status-distribution">
              <div v-for="status in statusStats" :key="status.name" class="status-item">
                <div class="status-info">
                  <span class="status-name">{{ status.name }}</span>
                  <span class="status-count">{{ status.count }}个</span>
                </div>
                <n-progress
                  :percentage="(status.count / totalIndustries) * 100"
                  :color="status.color"
                  :show-indicator="false"
                  :height="6"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 清洁生产水平分布 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">清洁生产水平分布</span>
            </template>
            <div class="level-distribution">
              <div v-for="level in levelStats" :key="level.name" class="level-item">
                <div class="level-info">
                  <span class="level-name">{{ level.name }}</span>
                  <span class="level-count">{{ level.count }}个</span>
                </div>
                <n-progress
                  :percentage="(level.count / totalIndustries) * 100"
                  :color="level.color"
                  :show-indicator="false"
                  :height="6"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 行业详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" title="行业详情" style="width: 800px">
      <div v-if="selectedIndustry" class="industry-detail">
        <n-tabs type="line" animated>
          <n-tab-pane name="basic" tab="基本信息">
            <n-descriptions :column="2" bordered>
              <n-descriptions-item label="行业名称">
                {{ selectedIndustry.name }}
              </n-descriptions-item>
              <n-descriptions-item label="行业分类">
                <n-tag :type="getCategoryType(selectedIndustry.category)">{{ selectedIndustry.category }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="发展状态">
                <n-tag :type="getStatusType(selectedIndustry.status)">{{ selectedIndustry.status }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="清洁生产水平">
                <n-tag :type="getLevelType(selectedIndustry.level)">{{ selectedIndustry.level }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="企业数量">
                {{ selectedIndustry.enterpriseCount }}
              </n-descriptions-item>
              <n-descriptions-item label="年产值">
                {{ selectedIndustry.output }}
              </n-descriptions-item>
              <n-descriptions-item label="主要产品">
                {{ selectedIndustry.products }}
              </n-descriptions-item>
              <n-descriptions-item label="技术特点">
                {{ selectedIndustry.technology }}
              </n-descriptions-item>
            </n-descriptions>
          </n-tab-pane>
          <n-tab-pane name="analysis" tab="行业分析">
            <div class="industry-analysis">
              <h4>行业概况</h4>
              <p>{{ selectedIndustry.overview }}</p>
              
              <h4>清洁生产现状</h4>
              <div class="clean-production-status">
                <n-grid :cols="2" :x-gap="16">
                  <n-grid-item>
                    <n-card title="关键指标" size="small">
                      <div v-for="indicator in selectedIndustry.indicators" :key="indicator.name" class="indicator-item">
                        <span class="indicator-name">{{ indicator.name }}</span>
                        <span class="indicator-value">{{ indicator.value }}</span>
                      </div>
                    </n-card>
                  </n-grid-item>
                  <n-grid-item>
                    <n-card title="主要问题" size="small">
                      <ul>
                        <li v-for="problem in selectedIndustry.problems" :key="problem">{{ problem }}</li>
                      </ul>
                    </n-card>
                  </n-grid-item>
                </n-grid>
              </div>
              
              <h4>发展建议</h4>
              <ul>
                <li v-for="suggestion in selectedIndustry.suggestions" :key="suggestion">{{ suggestion }}</li>
              </ul>
            </div>
          </n-tab-pane>
          <n-tab-pane name="enterprises" tab="相关企业">
            <div class="enterprise-list">
              <n-list>
                <n-list-item v-for="enterprise in selectedIndustry.enterprises" :key="enterprise.id">
                  <n-thing>
                    <template #header>
                      <span class="enterprise-name">{{ enterprise.name }}</span>
                    </template>
                    <template #description>
                      <n-space>
                        <n-tag size="small" type="info">{{ enterprise.scale }}</n-tag>
                        <span class="enterprise-location">{{ enterprise.location }}</span>
                        <span class="enterprise-status">{{ enterprise.status }}</span>
                      </n-space>
                    </template>
                  </n-thing>
                </n-list-item>
              </n-list>
            </div>
          </n-tab-pane>
        </n-tabs>
      </div>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'

defineOptions({ name: '行业' })

// 响应式数据
const searchKeyword = ref('')
const selectedCategory = ref(null)
const selectedStatus = ref(null)
const showDetailModal = ref(false)
const selectedIndustry = ref(null)
const checkedRowKeys = ref([])

// 筛选选项
const categoryOptions = [
  { label: '重工业', value: 'heavy' },
  { label: '轻工业', value: 'light' },
  { label: '高新技术', value: 'high_tech' },
  { label: '服务业', value: 'service' }
]

const statusOptions = [
  { label: '快速发展', value: 'rapid' },
  { label: '稳定发展', value: 'stable' },
  { label: '转型升级', value: 'transformation' },
  { label: '衰退调整', value: 'decline' }
]

// 模拟数据
const industries = ref([
  {
    id: 1,
    name: '钢铁行业',
    category: '重工业',
    status: '转型升级',
    level: '中等',
    enterpriseCount: 1200,
    output: '8.5万亿元',
    products: '钢材、铁合金、金属制品',
    technology: '高炉炼铁、转炉炼钢、连铸连轧',
    overview: '钢铁行业是国民经济的基础产业，在国民经济中占有重要地位。近年来，随着环保要求的提高，钢铁行业正在向绿色化、智能化方向发展。',
    indicators: [
      { name: '能耗水平', value: '85%' },
      { name: '水耗水平', value: '90%' },
      { name: '固废利用率', value: '95%' },
      { name: '清洁生产审核率', value: '80%' }
    ],
    problems: [
      '能耗水平偏高',
      '污染物排放量大',
      '资源利用效率有待提高',
      '清洁生产技术推广不足'
    ],
    suggestions: [
      '推广高效节能技术',
      '加强污染物治理',
      '提高资源综合利用水平',
      '完善清洁生产管理体系'
    ],
    enterprises: [
      { id: 1, name: '北京钢铁集团有限公司', scale: '大型', location: '北京', status: '正常运营' },
      { id: 2, name: '上海钢铁股份有限公司', scale: '大型', location: '上海', status: '正常运营' }
    ]
  },
  {
    id: 2,
    name: '化工行业',
    category: '重工业',
    status: '稳定发展',
    level: '较高',
    enterpriseCount: 800,
    output: '6.2万亿元',
    products: '基础化工原料、精细化工产品',
    technology: '催化反应、分离提纯、聚合反应',
    overview: '化工行业是国民经济的重要支柱产业，为其他行业提供基础原料和材料。在清洁生产方面，化工行业通过技术创新和工艺改进，不断提高资源利用效率。',
    indicators: [
      { name: '能耗水平', value: '75%' },
      { name: '水耗水平', value: '80%' },
      { name: '固废利用率', value: '85%' },
      { name: '清洁生产审核率', value: '90%' }
    ],
    problems: [
      '部分工艺技术落后',
      '环保设施投入不足',
      '危险废物处理压力大',
      '清洁生产技术更新慢'
    ],
    suggestions: [
      '加快技术升级改造',
      '加大环保投入',
      '完善危险废物处理体系',
      '推广先进清洁生产技术'
    ],
    enterprises: [
      { id: 3, name: '上海化工股份有限公司', scale: '大型', location: '上海', status: '正常运营' },
      { id: 4, name: '广东化工有限公司', scale: '中型', location: '广东', status: '正常运营' }
    ]
  },
  {
    id: 3,
    name: '电子信息行业',
    category: '高新技术',
    status: '快速发展',
    level: '高',
    enterpriseCount: 1500,
    output: '12.8万亿元',
    products: '电子元器件、通信设备、计算机',
    technology: '集成电路设计、精密制造、自动化生产',
    overview: '电子信息行业是战略性新兴产业，技术更新快，产品附加值高。在清洁生产方面，电子信息行业注重绿色制造和循环经济。',
    indicators: [
      { name: '能耗水平', value: '60%' },
      { name: '水耗水平', value: '70%' },
      { name: '固废利用率', value: '90%' },
      { name: '清洁生产审核率', value: '95%' }
    ],
    problems: [
      '部分企业环保意识不强',
      '电子废物处理复杂',
      '清洁生产技术标准不统一',
      '绿色供应链建设滞后'
    ],
    suggestions: [
      '加强环保宣传教育',
      '完善电子废物回收体系',
      '制定统一技术标准',
      '推进绿色供应链建设'
    ],
    enterprises: [
      { id: 5, name: '深圳电子科技有限公司', scale: '大型', location: '深圳', status: '正常运营' },
      { id: 6, name: '北京信息技术有限公司', scale: '中型', location: '北京', status: '正常运营' }
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
const industryColumns = [
  {
    type: 'selection'
  },
  {
    title: '行业名称',
    key: 'name',
    width: 150,
    ellipsis: { tooltip: true }
  },
  {
    title: '行业分类',
    key: 'category',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: getCategoryType(row.category) }, { default: () => row.category })
  },
  {
    title: '发展状态',
    key: 'status',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: getStatusType(row.status) }, { default: () => row.status })
  },
  {
    title: '清洁生产水平',
    key: 'level',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: getLevelType(row.level) }, { default: () => row.level })
  },
  {
    title: '企业数量',
    key: 'enterpriseCount',
    width: 100
  },
  {
    title: '年产值',
    key: 'output',
    width: 120
  },
  {
    title: '主要产品',
    key: 'products',
    width: 200,
    ellipsis: { tooltip: true }
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
        onClick: () => editIndustry(row)
      }, { default: () => '编辑' })
    ]
  }
]

// 计算属性
const totalIndustries = computed(() => industries.value.length)
const keyIndustries = computed(() => industries.value.filter(i => i.level === '高').length)
const traditionalIndustries = computed(() => industries.value.filter(i => i.category === '重工业' || i.category === '轻工业').length)
const emergingIndustries = computed(() => industries.value.filter(i => i.category === '高新技术').length)

const filteredIndustries = computed(() => {
  let filtered = industries.value
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(i => 
      i.name.toLowerCase().includes(keyword) || 
      i.products.toLowerCase().includes(keyword)
    )
  }
  
  if (selectedCategory.value) {
    filtered = filtered.filter(i => i.category === selectedCategory.value)
  }
  
  if (selectedStatus.value) {
    filtered = filtered.filter(i => i.status === selectedStatus.value)
  }
  
  return filtered
})

const categoryStats = computed(() => {
  const stats = {}
  industries.value.forEach(industry => {
    stats[industry.category] = (stats[industry.category] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050'][index % 4]
  }))
})

const statusStats = computed(() => {
  const stats = {}
  industries.value.forEach(industry => {
    stats[industry.status] = (stats[industry.status] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#18a058', '#f0a020', '#d03050', '#9c27b0'][index % 4]
  }))
})

const levelStats = computed(() => {
  const stats = {}
  industries.value.forEach(industry => {
    stats[industry.level] = (stats[industry.level] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#d03050', '#f0a020', '#18a058'][index % 3]
  }))
})

// 方法
const handleSearch = () => {
  console.log('搜索行业:', { searchKeyword: searchKeyword.value, selectedCategory: selectedCategory.value, selectedStatus: selectedStatus.value })
}

const handleAdd = () => {
  console.log('新增行业')
}

const handleExport = () => {
  console.log('导出数据')
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

const viewDetail = (industry) => {
  selectedIndustry.value = industry
  showDetailModal.value = true
}

const editIndustry = (industry) => {
  console.log('编辑行业:', industry)
}

const getCategoryType = (category) => {
  const categoryMap = {
    '重工业': 'error',
    '轻工业': 'warning',
    '高新技术': 'success',
    '服务业': 'info'
  }
  return categoryMap[category] || 'default'
}

const getStatusType = (status) => {
  const statusMap = {
    '快速发展': 'success',
    '稳定发展': 'info',
    '转型升级': 'warning',
    '衰退调整': 'error'
  }
  return statusMap[status] || 'default'
}

const getLevelType = (level) => {
  const levelMap = {
    '高': 'success',
    '中等': 'warning',
    '较低': 'error'
  }
  return levelMap[level] || 'default'
}

onMounted(() => {
  console.log('行业模块已加载')
})
</script>

<style scoped>
.industry-container {
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

.category-stats {
  padding: 16px 0;
}

.category-item {
  margin-bottom: 16px;
}

.category-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.category-name {
  font-size: 14px;
  color: #666;
}

.category-count {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.status-distribution,
.level-distribution {
  padding: 16px 0;
}

.status-item,
.level-item {
  margin-bottom: 12px;
}

.status-info,
.level-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.status-name,
.level-name {
  font-size: 13px;
  color: #666;
}

.status-count,
.level-count {
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.industry-detail {
  padding: 16px 0;
}

.industry-analysis h4 {
  margin: 16px 0 8px 0;
  color: #333;
  font-size: 16px;
}

.industry-analysis p {
  margin-bottom: 12px;
  line-height: 1.6;
  color: #666;
}

.industry-analysis ul {
  margin-bottom: 12px;
  padding-left: 20px;
}

.industry-analysis li {
  margin-bottom: 4px;
  line-height: 1.6;
  color: #666;
}

.clean-production-status {
  margin: 16px 0;
}

.indicator-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  padding: 4px 0;
}

.indicator-name {
  font-size: 14px;
  color: #666;
}

.indicator-value {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.enterprise-list {
  padding: 16px 0;
}

.enterprise-name {
  font-weight: 500;
  color: #333;
}

.enterprise-location,
.enterprise-status {
  font-size: 12px;
  color: #999;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .industry-container {
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
