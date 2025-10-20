<template>
  <div class="typical-cases-container">
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section">
      <n-card :bordered="false" class="search-card">
        <n-space justify="space-between" align="center">
          <n-space>
            <n-input
              v-model:value="searchKeyword"
              placeholder="搜索案例标题、企业名称或关键词"
              style="width: 300px"
              clearable
            >
              <template #prefix>
                <n-icon><i class="mdi mdi-magnify" /></n-icon>
              </template>
            </n-input>
            <n-select
              v-model:value="selectedIndustry"
              placeholder="选择行业"
              style="width: 150px"
              :options="industryOptions"
              clearable
            />
            <n-select
              v-model:value="selectedRegion"
              placeholder="选择地区"
              style="width: 150px"
              :options="regionOptions"
              clearable
            />
            <n-select
              v-model:value="selectedLevel"
              placeholder="案例级别"
              style="width: 150px"
              :options="levelOptions"
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
              导出案例
            </n-button>
            <n-button type="primary" @click="handleAdd">
              <template #icon>
                <n-icon><i class="mdi mdi-plus" /></n-icon>
              </template>
              新增案例
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
            <n-statistic label="总案例数" :value="totalCases">
              <template #prefix>
                <n-icon color="#2080f0"><i class="mdi mdi-book-open-variant" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="国家级案例" :value="nationalCases">
              <template #prefix>
                <n-icon color="#d03050"><i class="mdi mdi-star" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="省级案例" :value="provincialCases">
              <template #prefix>
                <n-icon color="#f0a020"><i class="mdi mdi-star-half-full" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="市级案例" :value="municipalCases">
              <template #prefix>
                <n-icon color="#18a058"><i class="mdi mdi-star-outline" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-section">
      <n-grid :cols="4" :x-gap="16" :y-gap="16">
        <!-- 案例列表 -->
        <n-grid-item :span="3">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">典型案例库</span>
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
              :columns="caseColumns"
              :data="filteredCases"
              :pagination="paginationConfig"
              :bordered="false"
              :row-key="row => row.id"
              @update:checked-row-keys="handleCheck"
            />
          </n-card>
        </n-grid-item>

        <!-- 案例分类统计 -->
        <n-grid-item>
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">案例分类统计</span>
            </template>
            <div class="category-stats">
              <div v-for="category in categoryStats" :key="category.name" class="category-item">
                <div class="category-info">
                  <span class="category-name">{{ category.name }}</span>
                  <span class="category-count">{{ category.count }}</span>
                </div>
                <n-progress
                  :percentage="(category.count / totalCases) * 100"
                  :color="category.color"
                  :show-indicator="false"
                  :height="8"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 行业分布 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">行业分布</span>
            </template>
            <div class="industry-distribution">
              <div v-for="industry in industryStats" :key="industry.name" class="industry-item">
                <div class="industry-info">
                  <span class="industry-name">{{ industry.name }}</span>
                  <span class="industry-count">{{ industry.count }}个</span>
                </div>
                <n-progress
                  :percentage="(industry.count / totalCases) * 100"
                  :color="industry.color"
                  :show-indicator="false"
                  :height="6"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 地区分布 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">地区分布</span>
            </template>
            <div class="region-distribution">
              <div v-for="region in regionStats" :key="region.name" class="region-item">
                <div class="region-info">
                  <span class="region-name">{{ region.name }}</span>
                  <span class="region-count">{{ region.count }}个</span>
                </div>
                <n-progress
                  :percentage="(region.count / totalCases) * 100"
                  :color="region.color"
                  :show-indicator="false"
                  :height="6"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 案例详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" title="案例详情" style="width: 900px">
      <div v-if="selectedCase" class="case-detail">
        <n-tabs type="line" animated>
          <n-tab-pane name="basic" tab="基本信息">
            <n-descriptions :column="2" bordered>
              <n-descriptions-item label="案例标题">
                {{ selectedCase.title }}
              </n-descriptions-item>
              <n-descriptions-item label="案例级别">
                <n-tag :type="getLevelType(selectedCase.level)">{{ selectedCase.level }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="企业名称">
                {{ selectedCase.enterprise }}
              </n-descriptions-item>
              <n-descriptions-item label="所属行业">
                {{ selectedCase.industry }}
              </n-descriptions-item>
              <n-descriptions-item label="所在地区">
                {{ selectedCase.region }}
              </n-descriptions-item>
              <n-descriptions-item label="案例类型">
                {{ selectedCase.type }}
              </n-descriptions-item>
              <n-descriptions-item label="发布时间">
                {{ selectedCase.publishDate }}
              </n-descriptions-item>
              <n-descriptions-item label="浏览次数">
                {{ selectedCase.views }}
              </n-descriptions-item>
            </n-descriptions>
          </n-tab-pane>
          <n-tab-pane name="content" tab="案例内容">
            <div class="case-content">
              <h4>案例背景</h4>
              <p>{{ selectedCase.background }}</p>
              
              <h4>主要措施</h4>
              <ul>
                <li v-for="measure in selectedCase.measures" :key="measure">{{ measure }}</li>
              </ul>
              
              <h4>实施效果</h4>
              <p>{{ selectedCase.effects }}</p>
              
              <h4>经验总结</h4>
              <p>{{ selectedCase.summary }}</p>
            </div>
          </n-tab-pane>
          <n-tab-pane name="files" tab="相关文件">
            <div class="file-list">
              <n-list>
                <n-list-item v-for="file in selectedCase.files" :key="file.name">
                  <n-thing>
                    <template #header>
                      <span class="file-name">{{ file.name }}</span>
                    </template>
                    <template #description>
                      <n-space>
                        <n-tag size="small" type="info">{{ file.type }}</n-tag>
                        <span class="file-size">{{ file.size }}</span>
                        <span class="file-date">{{ file.date }}</span>
                      </n-space>
                    </template>
                    <template #footer>
                      <n-button size="small" type="primary" @click="downloadFile(file)">
                        <template #icon>
                          <n-icon><i class="mdi mdi-download" /></n-icon>
                        </template>
                        下载
                      </n-button>
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

defineOptions({ name: '清洁生产审核典型案例' })

// 响应式数据
const searchKeyword = ref('')
const selectedIndustry = ref(null)
const selectedRegion = ref(null)
const selectedLevel = ref(null)
const showDetailModal = ref(false)
const selectedCase = ref(null)
const checkedRowKeys = ref([])

// 筛选选项
const industryOptions = [
  { label: '钢铁', value: 'steel' },
  { label: '化工', value: 'chemical' },
  { label: '建材', value: 'building' },
  { label: '纺织', value: 'textile' },
  { label: '造纸', value: 'paper' },
  { label: '食品', value: 'food' },
  { label: '电子', value: 'electronics' }
]

const regionOptions = [
  { label: '北京', value: 'beijing' },
  { label: '上海', value: 'shanghai' },
  { label: '广东', value: 'guangdong' },
  { label: '江苏', value: 'jiangsu' },
  { label: '浙江', value: 'zhejiang' },
  { label: '山东', value: 'shandong' }
]

const levelOptions = [
  { label: '国家级', value: 'national' },
  { label: '省级', value: 'provincial' },
  { label: '市级', value: 'municipal' }
]

// 模拟数据
const cases = ref([
  {
    id: 1,
    title: '某钢铁企业清洁生产审核典型案例',
    enterprise: '北京钢铁集团有限公司',
    industry: '钢铁',
    region: '北京',
    level: '国家级',
    type: '技术改造',
    publishDate: '2025-01-10',
    views: 1250,
    background: '该企业通过清洁生产审核，识别出多个清洁生产机会，实施了多项技术改造措施。',
    measures: [
      '采用高效节能设备替代老旧设备',
      '实施废水循环利用系统',
      '优化生产工艺流程',
      '建立能源管理系统'
    ],
    effects: '年节约能源成本500万元，减少废水排放30%，提高生产效率15%。',
    summary: '通过系统性的清洁生产审核，企业实现了经济效益和环境效益的双赢。',
    files: [
      { name: '清洁生产审核报告.pdf', type: 'PDF', size: '2.5MB', date: '2025-01-10' },
      { name: '技术改造方案.docx', type: 'Word', size: '1.2MB', date: '2025-01-10' },
      { name: '效果评估报告.xlsx', type: 'Excel', size: '800KB', date: '2025-01-10' }
    ]
  },
  {
    id: 2,
    title: '某化工企业清洁生产审核实践',
    enterprise: '上海化工股份有限公司',
    industry: '化工',
    region: '上海',
    level: '省级',
    type: '工艺优化',
    publishDate: '2025-01-08',
    views: 980,
    background: '该化工企业通过清洁生产审核，重点优化了生产工艺，减少了污染物排放。',
    measures: [
      '优化反应工艺参数',
      '改进催化剂配方',
      '实施废料回收利用',
      '加强过程控制'
    ],
    effects: '减少原料消耗20%，降低污染物排放40%，年节约成本300万元。',
    summary: '工艺优化是化工企业清洁生产的重要途径，需要系统性的分析和改进。',
    files: [
      { name: '工艺优化方案.pdf', type: 'PDF', size: '1.8MB', date: '2025-01-08' },
      { name: '效果分析报告.docx', type: 'Word', size: '950KB', date: '2025-01-08' }
    ]
  },
  {
    id: 3,
    title: '某建材企业清洁生产审核案例',
    enterprise: '广东建材有限公司',
    industry: '建材',
    region: '广东',
    level: '市级',
    type: '设备更新',
    publishDate: '2025-01-05',
    views: 750,
    background: '该建材企业通过设备更新和技术改造，实现了清洁生产目标。',
    measures: [
      '更新生产设备',
      '改进除尘系统',
      '优化原料配比',
      '实施自动化控制'
    ],
    effects: '提高产品质量，减少粉尘排放50%，降低能耗25%。',
    summary: '设备更新是建材企业清洁生产的重要手段，需要综合考虑技术和经济因素。',
    files: [
      { name: '设备更新方案.pdf', type: 'PDF', size: '2.1MB', date: '2025-01-05' },
      { name: '技术改造报告.docx', type: 'Word', size: '1.1MB', date: '2025-01-05' }
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
const caseColumns = [
  {
    type: 'selection'
  },
  {
    title: '案例标题',
    key: 'title',
    width: 250,
    ellipsis: { tooltip: true }
  },
  {
    title: '企业名称',
    key: 'enterprise',
    width: 200,
    ellipsis: { tooltip: true }
  },
  {
    title: '所属行业',
    key: 'industry',
    width: 100,
    render: (row) => h('n-tag', { size: 'small', type: 'info' }, { default: () => row.industry })
  },
  {
    title: '所在地区',
    key: 'region',
    width: 100
  },
  {
    title: '案例级别',
    key: 'level',
    width: 100,
    render: (row) => h('n-tag', { size: 'small', type: getLevelType(row.level) }, { default: () => row.level })
  },
  {
    title: '案例类型',
    key: 'type',
    width: 120
  },
  {
    title: '发布时间',
    key: 'publishDate',
    width: 120
  },
  {
    title: '浏览次数',
    key: 'views',
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
        onClick: () => editCase(row)
      }, { default: () => '编辑' })
    ]
  }
]

// 计算属性
const totalCases = computed(() => cases.value.length)
const nationalCases = computed(() => cases.value.filter(c => c.level === '国家级').length)
const provincialCases = computed(() => cases.value.filter(c => c.level === '省级').length)
const municipalCases = computed(() => cases.value.filter(c => c.level === '市级').length)

const filteredCases = computed(() => {
  let filtered = cases.value
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(c => 
      c.title.toLowerCase().includes(keyword) || 
      c.enterprise.toLowerCase().includes(keyword)
    )
  }
  
  if (selectedIndustry.value) {
    filtered = filtered.filter(c => c.industry === selectedIndustry.value)
  }
  
  if (selectedRegion.value) {
    filtered = filtered.filter(c => c.region === selectedRegion.value)
  }
  
  if (selectedLevel.value) {
    filtered = filtered.filter(c => c.level === selectedLevel.value)
  }
  
  return filtered
})

const categoryStats = computed(() => {
  const stats = {}
  cases.value.forEach(case_ => {
    stats[case_.type] = (stats[case_.type] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050', '#9c27b0'][index % 5]
  }))
})

const industryStats = computed(() => {
  const stats = {}
  cases.value.forEach(case_ => {
    stats[case_.industry] = (stats[case_.industry] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050', '#9c27b0', '#ff9800', '#4caf50'][index % 7]
  }))
})

const regionStats = computed(() => {
  const stats = {}
  cases.value.forEach(case_ => {
    stats[case_.region] = (stats[case_.region] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050', '#9c27b0', '#ff9800'][index % 6]
  }))
})

// 方法
const handleSearch = () => {
  console.log('搜索案例:', { searchKeyword: searchKeyword.value, selectedIndustry: selectedIndustry.value, selectedRegion: selectedRegion.value, selectedLevel: selectedLevel.value })
}

const handleAdd = () => {
  console.log('新增案例')
}

const handleExport = () => {
  console.log('导出案例')
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

const viewDetail = (case_) => {
  selectedCase.value = case_
  showDetailModal.value = true
}

const editCase = (case_) => {
  console.log('编辑案例:', case_)
}

const downloadFile = (file) => {
  console.log('下载文件:', file.name)
}

const getLevelType = (level) => {
  const levelMap = {
    '国家级': 'error',
    '省级': 'warning',
    '市级': 'info'
  }
  return levelMap[level] || 'default'
}

onMounted(() => {
  console.log('清洁生产审核典型案例模块已加载')
})
</script>

<style scoped>
.typical-cases-container {
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

.industry-distribution,
.region-distribution {
  padding: 16px 0;
}

.industry-item,
.region-item {
  margin-bottom: 12px;
}

.industry-info,
.region-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.industry-name,
.region-name {
  font-size: 13px;
  color: #666;
}

.industry-count,
.region-count {
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.case-detail {
  padding: 16px 0;
}

.case-content h4 {
  margin: 16px 0 8px 0;
  color: #333;
  font-size: 16px;
}

.case-content p {
  margin-bottom: 12px;
  line-height: 1.6;
  color: #666;
}

.case-content ul {
  margin-bottom: 12px;
  padding-left: 20px;
}

.case-content li {
  margin-bottom: 4px;
  line-height: 1.6;
  color: #666;
}

.file-list {
  padding: 16px 0;
}

.file-name {
  font-weight: 500;
  color: #333;
}

.file-size,
.file-date {
  font-size: 12px;
  color: #999;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .typical-cases-container {
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
