<template>
  <div class="technology-integration-container">
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section">
      <n-card :bordered="false" class="search-card">
        <n-space justify="space-between" align="center">
          <n-space>
            <n-input
              v-model:value="searchKeyword"
              placeholder="搜索技术名称、关键词或应用领域"
              style="width: 300px"
              clearable
            >
              <template #prefix>
                <n-icon><i class="mdi mdi-magnify" /></n-icon>
              </template>
            </n-input>
            <n-select
              v-model:value="selectedCategory"
              placeholder="技术分类"
              style="width: 150px"
              :options="categoryOptions"
              clearable
            />
            <n-select
              v-model:value="selectedIndustry"
              placeholder="适用行业"
              style="width: 150px"
              :options="industryOptions"
              clearable
            />
            <n-select
              v-model:value="selectedMaturity"
              placeholder="技术成熟度"
              style="width: 150px"
              :options="maturityOptions"
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
              导出技术
            </n-button>
            <n-button type="primary" @click="handleAdd">
              <template #icon>
                <n-icon><i class="mdi mdi-plus" /></n-icon>
              </template>
              新增技术
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
            <n-statistic label="总技术数" :value="totalTechnologies">
              <template #prefix>
                <n-icon color="#2080f0"><i class="mdi mdi-cog" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="成熟技术" :value="matureTechnologies">
              <template #prefix>
                <n-icon color="#18a058"><i class="mdi mdi-check-circle" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="示范技术" :value="demonstrationTechnologies">
              <template #prefix>
                <n-icon color="#f0a020"><i class="mdi mdi-star" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="应用案例" :value="totalApplications">
              <template #prefix>
                <n-icon color="#d03050"><i class="mdi mdi-application" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-section">
      <n-grid :cols="4" :x-gap="16" :y-gap="16">
        <!-- 技术列表 -->
        <n-grid-item :span="3">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">清洁生产技术库</span>
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
              :columns="technologyColumns"
              :data="filteredTechnologies"
              :pagination="paginationConfig"
              :bordered="false"
              :row-key="row => row.id"
              @update:checked-row-keys="handleCheck"
            />
          </n-card>
        </n-grid-item>

        <!-- 技术分类统计 -->
        <n-grid-item>
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">技术分类统计</span>
            </template>
            <div class="category-stats">
              <div v-for="category in categoryStats" :key="category.name" class="category-item">
                <div class="category-info">
                  <span class="category-name">{{ category.name }}</span>
                  <span class="category-count">{{ category.count }}</span>
                </div>
                <n-progress
                  :percentage="(category.count / totalTechnologies) * 100"
                  :color="category.color"
                  :show-indicator="false"
                  :height="8"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 技术成熟度分布 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">技术成熟度分布</span>
            </template>
            <div class="maturity-distribution">
              <div v-for="maturity in maturityStats" :key="maturity.name" class="maturity-item">
                <div class="maturity-info">
                  <span class="maturity-name">{{ maturity.name }}</span>
                  <span class="maturity-count">{{ maturity.count }}项</span>
                </div>
                <n-progress
                  :percentage="(maturity.count / totalTechnologies) * 100"
                  :color="maturity.color"
                  :show-indicator="false"
                  :height="6"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 适用行业分布 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">适用行业分布</span>
            </template>
            <div class="industry-distribution">
              <div v-for="industry in industryStats" :key="industry.name" class="industry-item">
                <div class="industry-info">
                  <span class="industry-name">{{ industry.name }}</span>
                  <span class="industry-count">{{ industry.count }}项</span>
                </div>
                <n-progress
                  :percentage="(industry.count / totalTechnologies) * 100"
                  :color="industry.color"
                  :show-indicator="false"
                  :height="6"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 技术详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" title="技术详情" style="width: 900px">
      <div v-if="selectedTechnology" class="technology-detail">
        <n-tabs type="line" animated>
          <n-tab-pane name="basic" tab="基本信息">
            <n-descriptions :column="2" bordered>
              <n-descriptions-item label="技术名称">
                {{ selectedTechnology.name }}
              </n-descriptions-item>
              <n-descriptions-item label="技术分类">
                <n-tag :type="getCategoryType(selectedTechnology.category)">{{ selectedTechnology.category }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="适用行业">
                {{ selectedTechnology.industry }}
              </n-descriptions-item>
              <n-descriptions-item label="技术成熟度">
                <n-tag :type="getMaturityType(selectedTechnology.maturity)">{{ selectedTechnology.maturity }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="技术来源">
                {{ selectedTechnology.source }}
              </n-descriptions-item>
              <n-descriptions-item label="应用案例数">
                {{ selectedTechnology.applications }}
              </n-descriptions-item>
              <n-descriptions-item label="节能效果">
                {{ selectedTechnology.energySaving }}
              </n-descriptions-item>
              <n-descriptions-item label="减排效果">
                {{ selectedTechnology.emissionReduction }}
              </n-descriptions-item>
            </n-descriptions>
          </n-tab-pane>
          <n-tab-pane name="description" tab="技术描述">
            <div class="technology-description">
              <h4>技术原理</h4>
              <p>{{ selectedTechnology.principle }}</p>
              
              <h4>技术特点</h4>
              <ul>
                <li v-for="feature in selectedTechnology.features" :key="feature">{{ feature }}</li>
              </ul>
              
              <h4>应用条件</h4>
              <p>{{ selectedTechnology.conditions }}</p>
              
              <h4>投资估算</h4>
              <p>{{ selectedTechnology.investment }}</p>
            </div>
          </n-tab-pane>
          <n-tab-pane name="cases" tab="应用案例">
            <div class="case-list">
              <n-list>
                <n-list-item v-for="case_ in selectedTechnology.cases" :key="case_.id">
                  <n-thing>
                    <template #header>
                      <span class="case-name">{{ case_.name }}</span>
                    </template>
                    <template #description>
                      <n-space>
                        <n-tag size="small" type="info">{{ case_.industry }}</n-tag>
                        <span class="case-location">{{ case_.location }}</span>
                        <span class="case-date">{{ case_.date }}</span>
                      </n-space>
                    </template>
                    <template #footer>
                      <p class="case-effect">{{ case_.effect }}</p>
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

defineOptions({ name: '清洁生产技术集成' })

// 响应式数据
const searchKeyword = ref('')
const selectedCategory = ref(null)
const selectedIndustry = ref(null)
const selectedMaturity = ref(null)
const showDetailModal = ref(false)
const selectedTechnology = ref(null)
const checkedRowKeys = ref([])

// 筛选选项
const categoryOptions = [
  { label: '节能技术', value: 'energy_saving' },
  { label: '减排技术', value: 'emission_reduction' },
  { label: '资源综合利用', value: 'resource_utilization' },
  { label: '清洁工艺', value: 'clean_process' },
  { label: '末端治理', value: 'end_treatment' }
]

const industryOptions = [
  { label: '钢铁', value: 'steel' },
  { label: '化工', value: 'chemical' },
  { label: '建材', value: 'building' },
  { label: '纺织', value: 'textile' },
  { label: '造纸', value: 'paper' },
  { label: '食品', value: 'food' },
  { label: '电子', value: 'electronics' }
]

const maturityOptions = [
  { label: '成熟技术', value: 'mature' },
  { label: '示范技术', value: 'demonstration' },
  { label: '研发技术', value: 'development' }
]

// 模拟数据
const technologies = ref([
  {
    id: 1,
    name: '高效节能电机技术',
    category: '节能技术',
    industry: '钢铁',
    maturity: '成熟技术',
    source: '清华大学',
    applications: 15,
    energySaving: '20-30%',
    emissionReduction: '15-25%',
    principle: '采用高效永磁同步电机，提高电机效率，降低能耗。',
    features: [
      '效率高，节能效果显著',
      '运行稳定，维护成本低',
      '适应性强，应用范围广'
    ],
    conditions: '适用于各类工业电机应用场景',
    investment: '投资回收期2-3年',
    cases: [
      { id: 1, name: '某钢铁企业电机改造项目', industry: '钢铁', location: '北京', date: '2024', effect: '年节约电费200万元' },
      { id: 2, name: '某化工企业节能改造', industry: '化工', location: '上海', date: '2023', effect: '节能率25%，减排效果显著' }
    ]
  },
  {
    id: 2,
    name: '烟气脱硫脱硝技术',
    category: '减排技术',
    industry: '化工',
    maturity: '成熟技术',
    source: '中科院',
    applications: 25,
    energySaving: '5-10%',
    emissionReduction: '80-90%',
    principle: '采用湿法脱硫和SCR脱硝技术，有效去除烟气中的SO2和NOx。',
    features: [
      '脱除效率高',
      '技术成熟可靠',
      '运行成本相对较低'
    ],
    conditions: '适用于燃煤锅炉和工业炉窑',
    investment: '投资回收期3-4年',
    cases: [
      { id: 3, name: '某电厂烟气治理项目', industry: '电力', location: '广东', date: '2024', effect: 'SO2减排90%，NOx减排85%' }
    ]
  },
  {
    id: 3,
    name: '工业废水零排放技术',
    category: '资源综合利用',
    industry: '纺织',
    maturity: '示范技术',
    source: '环保部',
    applications: 8,
    energySaving: '10-15%',
    emissionReduction: '95%以上',
    principle: '采用膜分离、蒸发结晶等技术，实现废水零排放。',
    features: [
      '实现废水零排放',
      '回收有用物质',
      '环境效益显著'
    ],
    conditions: '适用于高浓度有机废水处理',
    investment: '投资回收期4-5年',
    cases: [
      { id: 4, name: '某纺织企业废水零排放项目', industry: '纺织', location: '江苏', date: '2023', effect: '实现废水零排放，年节约水费50万元' }
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
const technologyColumns = [
  {
    type: 'selection'
  },
  {
    title: '技术名称',
    key: 'name',
    width: 200,
    ellipsis: { tooltip: true }
  },
  {
    title: '技术分类',
    key: 'category',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: getCategoryType(row.category) }, { default: () => row.category })
  },
  {
    title: '适用行业',
    key: 'industry',
    width: 100,
    render: (row) => h('n-tag', { size: 'small', type: 'info' }, { default: () => row.industry })
  },
  {
    title: '技术成熟度',
    key: 'maturity',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: getMaturityType(row.maturity) }, { default: () => row.maturity })
  },
  {
    title: '技术来源',
    key: 'source',
    width: 120
  },
  {
    title: '应用案例数',
    key: 'applications',
    width: 120
  },
  {
    title: '节能效果',
    key: 'energySaving',
    width: 100
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
        onClick: () => editTechnology(row)
      }, { default: () => '编辑' })
    ]
  }
]

// 计算属性
const totalTechnologies = computed(() => technologies.value.length)
const matureTechnologies = computed(() => technologies.value.filter(t => t.maturity === '成熟技术').length)
const demonstrationTechnologies = computed(() => technologies.value.filter(t => t.maturity === '示范技术').length)
const totalApplications = computed(() => technologies.value.reduce((sum, t) => sum + t.applications, 0))

const filteredTechnologies = computed(() => {
  let filtered = technologies.value
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(t => 
      t.name.toLowerCase().includes(keyword) || 
      t.category.toLowerCase().includes(keyword) ||
      t.industry.toLowerCase().includes(keyword)
    )
  }
  
  if (selectedCategory.value) {
    filtered = filtered.filter(t => t.category === selectedCategory.value)
  }
  
  if (selectedIndustry.value) {
    filtered = filtered.filter(t => t.industry === selectedIndustry.value)
  }
  
  if (selectedMaturity.value) {
    filtered = filtered.filter(t => t.maturity === selectedMaturity.value)
  }
  
  return filtered
})

const categoryStats = computed(() => {
  const stats = {}
  technologies.value.forEach(technology => {
    stats[technology.category] = (stats[technology.category] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050', '#9c27b0'][index % 5]
  }))
})

const maturityStats = computed(() => {
  const stats = {}
  technologies.value.forEach(technology => {
    stats[technology.maturity] = (stats[technology.maturity] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#18a058', '#f0a020', '#d03050'][index % 3]
  }))
})

const industryStats = computed(() => {
  const stats = {}
  technologies.value.forEach(technology => {
    stats[technology.industry] = (stats[technology.industry] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050', '#9c27b0', '#ff9800', '#4caf50'][index % 7]
  }))
})

// 方法
const handleSearch = () => {
  console.log('搜索技术:', { searchKeyword: searchKeyword.value, selectedCategory: selectedCategory.value, selectedIndustry: selectedIndustry.value, selectedMaturity: selectedMaturity.value })
}

const handleAdd = () => {
  console.log('新增技术')
}

const handleExport = () => {
  console.log('导出技术')
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

const viewDetail = (technology) => {
  selectedTechnology.value = technology
  showDetailModal.value = true
}

const editTechnology = (technology) => {
  console.log('编辑技术:', technology)
}

const getCategoryType = (category) => {
  const categoryMap = {
    '节能技术': 'success',
    '减排技术': 'warning',
    '资源综合利用': 'info',
    '清洁工艺': 'error',
    '末端治理': 'default'
  }
  return categoryMap[category] || 'default'
}

const getMaturityType = (maturity) => {
  const maturityMap = {
    '成熟技术': 'success',
    '示范技术': 'warning',
    '研发技术': 'info'
  }
  return maturityMap[maturity] || 'default'
}

onMounted(() => {
  console.log('清洁生产技术集成模块已加载')
})
</script>

<style scoped>
.technology-integration-container {
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

.maturity-distribution,
.industry-distribution {
  padding: 16px 0;
}

.maturity-item,
.industry-item {
  margin-bottom: 12px;
}

.maturity-info,
.industry-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.maturity-name,
.industry-name {
  font-size: 13px;
  color: #666;
}

.maturity-count,
.industry-count {
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.technology-detail {
  padding: 16px 0;
}

.technology-description h4 {
  margin: 16px 0 8px 0;
  color: #333;
  font-size: 16px;
}

.technology-description p {
  margin-bottom: 12px;
  line-height: 1.6;
  color: #666;
}

.technology-description ul {
  margin-bottom: 12px;
  padding-left: 20px;
}

.technology-description li {
  margin-bottom: 4px;
  line-height: 1.6;
  color: #666;
}

.case-list {
  padding: 16px 0;
}

.case-name {
  font-weight: 500;
  color: #333;
}

.case-location,
.case-date {
  font-size: 12px;
  color: #999;
}

.case-effect {
  margin-top: 8px;
  font-size: 14px;
  color: #666;
  line-height: 1.5;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .technology-integration-container {
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
