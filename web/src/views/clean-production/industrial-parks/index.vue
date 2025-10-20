<template>
  <div class="industrial-parks-container">
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section">
      <n-card :bordered="false" class="search-card">
        <n-space justify="space-between" align="center">
          <n-space>
            <n-input
              v-model:value="searchKeyword"
              placeholder="搜索园区名称或关键词"
              style="width: 300px"
              clearable
            >
              <template #prefix>
                <n-icon><i class="mdi mdi-magnify" /></n-icon>
              </template>
            </n-input>
            <n-select
              v-model:value="selectedLevel"
              placeholder="园区级别"
              style="width: 150px"
              :options="levelOptions"
              clearable
            />
            <n-select
              v-model:value="selectedRegion"
              placeholder="选择地区"
              style="width: 150px"
              :options="regionOptions"
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
              新增园区
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
            <n-statistic label="总园区数" :value="totalParks">
              <template #prefix>
                <n-icon color="#2080f0"><i class="mdi mdi-domain" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="国家级园区" :value="nationalParks">
              <template #prefix>
                <n-icon color="#d03050"><i class="mdi mdi-star" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="省级园区" :value="provincialParks">
              <template #prefix>
                <n-icon color="#f0a020"><i class="mdi mdi-star-half-full" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="入驻企业" :value="totalEnterprises">
              <template #prefix>
                <n-icon color="#18a058"><i class="mdi mdi-office-building" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-section">
      <n-grid :cols="4" :x-gap="16" :y-gap="16">
        <!-- 园区列表 -->
        <n-grid-item :span="3">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">工业园区管理</span>
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
              :columns="parkColumns"
              :data="filteredParks"
              :pagination="paginationConfig"
              :bordered="false"
              :row-key="row => row.id"
              @update:checked-row-keys="handleCheck"
            />
          </n-card>
        </n-grid-item>

        <!-- 园区级别分布 -->
        <n-grid-item>
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">园区级别分布</span>
            </template>
            <div class="level-stats">
              <div v-for="level in levelStats" :key="level.name" class="level-item">
                <div class="level-info">
                  <span class="level-name">{{ level.name }}</span>
                  <span class="level-count">{{ level.count }}</span>
                </div>
                <n-progress
                  :percentage="(level.count / totalParks) * 100"
                  :color="level.color"
                  :show-indicator="false"
                  :height="8"
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
                  :percentage="(region.count / totalParks) * 100"
                  :color="region.color"
                  :show-indicator="false"
                  :height="6"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 园区规模分布 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">园区规模分布</span>
            </template>
            <div class="scale-distribution">
              <div v-for="scale in scaleStats" :key="scale.name" class="scale-item">
                <div class="scale-info">
                  <span class="scale-name">{{ scale.name }}</span>
                  <span class="scale-count">{{ scale.count }}个</span>
                </div>
                <n-progress
                  :percentage="(scale.count / totalParks) * 100"
                  :color="scale.color"
                  :show-indicator="false"
                  :height="6"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 园区详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" title="园区详情" style="width: 800px">
      <div v-if="selectedPark" class="park-detail">
        <n-tabs type="line" animated>
          <n-tab-pane name="basic" tab="基本信息">
            <n-descriptions :column="2" bordered>
              <n-descriptions-item label="园区名称">
                {{ selectedPark.name }}
              </n-descriptions-item>
              <n-descriptions-item label="园区级别">
                <n-tag :type="getLevelType(selectedPark.level)">{{ selectedPark.level }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="所在地区">
                {{ selectedPark.region }}
              </n-descriptions-item>
              <n-descriptions-item label="园区规模">
                {{ selectedPark.scale }}
              </n-descriptions-item>
              <n-descriptions-item label="占地面积">
                {{ selectedPark.area }}
              </n-descriptions-item>
              <n-descriptions-item label="入驻企业数">
                {{ selectedPark.enterpriseCount }}
              </n-descriptions-item>
              <n-descriptions-item label="主导产业">
                {{ selectedPark.mainIndustry }}
              </n-descriptions-item>
              <n-descriptions-item label="成立时间">
                {{ selectedPark.establishDate }}
              </n-descriptions-item>
            </n-descriptions>
          </n-tab-pane>
          <n-tab-pane name="enterprises" tab="入驻企业">
            <div class="enterprise-list">
              <n-list>
                <n-list-item v-for="enterprise in selectedPark.enterprises" :key="enterprise.id">
                  <n-thing>
                    <template #header>
                      <span class="enterprise-name">{{ enterprise.name }}</span>
                    </template>
                    <template #description>
                      <n-space>
                        <n-tag size="small" type="info">{{ enterprise.industry }}</n-tag>
                        <span class="enterprise-scale">{{ enterprise.scale }}</span>
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

defineOptions({ name: '工业园区' })

// 响应式数据
const searchKeyword = ref('')
const selectedLevel = ref(null)
const selectedRegion = ref(null)
const showDetailModal = ref(false)
const selectedPark = ref(null)
const checkedRowKeys = ref([])

// 筛选选项
const levelOptions = [
  { label: '国家级', value: 'national' },
  { label: '省级', value: 'provincial' },
  { label: '市级', value: 'municipal' }
]

const regionOptions = [
  { label: '北京', value: 'beijing' },
  { label: '上海', value: 'shanghai' },
  { label: '广东', value: 'guangdong' },
  { label: '江苏', value: 'jiangsu' },
  { label: '浙江', value: 'zhejiang' },
  { label: '山东', value: 'shandong' }
]

// 模拟数据
const parks = ref([
  {
    id: 1,
    name: '北京经济技术开发区',
    level: '国家级',
    region: '北京',
    scale: '大型',
    area: '60平方公里',
    enterpriseCount: 1200,
    mainIndustry: '电子信息、生物医药',
    establishDate: '1992-10-01',
    enterprises: [
      { id: 1, name: '北京钢铁集团有限公司', industry: '钢铁', scale: '大型', status: '正常运营' },
      { id: 2, name: '北京化工股份有限公司', industry: '化工', scale: '中型', status: '正常运营' }
    ]
  },
  {
    id: 2,
    name: '上海张江高科技园区',
    level: '国家级',
    region: '上海',
    scale: '大型',
    area: '25平方公里',
    enterpriseCount: 800,
    mainIndustry: '生物医药、集成电路',
    establishDate: '1992-07-01',
    enterprises: [
      { id: 3, name: '上海生物技术有限公司', industry: '生物医药', scale: '中型', status: '正常运营' }
    ]
  },
  {
    id: 3,
    name: '深圳高新技术产业园区',
    level: '省级',
    region: '广东',
    scale: '大型',
    area: '11.5平方公里',
    enterpriseCount: 600,
    mainIndustry: '电子信息、新能源',
    establishDate: '1996-09-01',
    enterprises: [
      { id: 4, name: '深圳电子科技有限公司', industry: '电子', scale: '大型', status: '正常运营' }
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
const parkColumns = [
  {
    type: 'selection'
  },
  {
    title: '园区名称',
    key: 'name',
    width: 200,
    ellipsis: { tooltip: true }
  },
  {
    title: '园区级别',
    key: 'level',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: getLevelType(row.level) }, { default: () => row.level })
  },
  {
    title: '所在地区',
    key: 'region',
    width: 100
  },
  {
    title: '园区规模',
    key: 'scale',
    width: 100
  },
  {
    title: '占地面积',
    key: 'area',
    width: 120
  },
  {
    title: '入驻企业数',
    key: 'enterpriseCount',
    width: 120
  },
  {
    title: '主导产业',
    key: 'mainIndustry',
    width: 150,
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
        onClick: () => editPark(row)
      }, { default: () => '编辑' })
    ]
  }
]

// 计算属性
const totalParks = computed(() => parks.value.length)
const nationalParks = computed(() => parks.value.filter(p => p.level === '国家级').length)
const provincialParks = computed(() => parks.value.filter(p => p.level === '省级').length)
const totalEnterprises = computed(() => parks.value.reduce((sum, p) => sum + p.enterpriseCount, 0))

const filteredParks = computed(() => {
  let filtered = parks.value
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(p => 
      p.name.toLowerCase().includes(keyword) || 
      p.mainIndustry.toLowerCase().includes(keyword)
    )
  }
  
  if (selectedLevel.value) {
    filtered = filtered.filter(p => p.level === selectedLevel.value)
  }
  
  if (selectedRegion.value) {
    filtered = filtered.filter(p => p.region === selectedRegion.value)
  }
  
  return filtered
})

const levelStats = computed(() => {
  const stats = {}
  parks.value.forEach(park => {
    stats[park.level] = (stats[park.level] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#d03050', '#f0a020', '#18a058'][index % 3]
  }))
})

const regionStats = computed(() => {
  const stats = {}
  parks.value.forEach(park => {
    stats[park.region] = (stats[park.region] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050', '#9c27b0', '#ff9800'][index % 6]
  }))
})

const scaleStats = computed(() => {
  const stats = {}
  parks.value.forEach(park => {
    stats[park.scale] = (stats[park.scale] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020'][index % 3]
  }))
})

// 方法
const handleSearch = () => {
  console.log('搜索园区:', { searchKeyword: searchKeyword.value, selectedLevel: selectedLevel.value, selectedRegion: selectedRegion.value })
}

const handleAdd = () => {
  console.log('新增园区')
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

const viewDetail = (park) => {
  selectedPark.value = park
  showDetailModal.value = true
}

const editPark = (park) => {
  console.log('编辑园区:', park)
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
  console.log('工业园区模块已加载')
})
</script>

<style scoped>
.industrial-parks-container {
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

.level-stats {
  padding: 16px 0;
}

.level-item {
  margin-bottom: 16px;
}

.level-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.level-name {
  font-size: 14px;
  color: #666;
}

.level-count {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.region-distribution,
.scale-distribution {
  padding: 16px 0;
}

.region-item,
.scale-item {
  margin-bottom: 12px;
}

.region-info,
.scale-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.region-name,
.scale-name {
  font-size: 13px;
  color: #666;
}

.region-count,
.scale-count {
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.park-detail {
  padding: 16px 0;
}

.enterprise-list {
  padding: 16px 0;
}

.enterprise-name {
  font-weight: 500;
  color: #333;
}

.enterprise-scale,
.enterprise-status {
  font-size: 12px;
  color: #999;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .industrial-parks-container {
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
