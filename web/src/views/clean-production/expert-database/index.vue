<template>
  <div class="expert-database-container">
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section">
      <n-card :bordered="false" class="search-card">
        <n-space justify="space-between" align="center">
          <n-space>
            <n-input
              v-model:value="searchKeyword"
              placeholder="搜索专家姓名、专业领域或关键词"
              style="width: 300px"
              clearable
            >
              <template #prefix>
                <n-icon><i class="mdi mdi-magnify" /></n-icon>
              </template>
            </n-input>
            <n-select
              v-model:value="selectedSpecialty"
              placeholder="专业领域"
              style="width: 150px"
              :options="specialtyOptions"
              clearable
            />
            <n-select
              v-model:value="selectedLevel"
              placeholder="专家级别"
              style="width: 150px"
              :options="levelOptions"
              clearable
            />
            <n-select
              v-model:value="selectedRegion"
              placeholder="所在地区"
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
              导出专家
            </n-button>
            <n-button type="primary" @click="handleAdd">
              <template #icon>
                <n-icon><i class="mdi mdi-plus" /></n-icon>
              </template>
              新增专家
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
            <n-statistic label="总专家数" :value="totalExperts">
              <template #prefix>
                <n-icon color="#2080f0"><i class="mdi mdi-account-group" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="国家级专家" :value="nationalExperts">
              <template #prefix>
                <n-icon color="#d03050"><i class="mdi mdi-star" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="省级专家" :value="provincialExperts">
              <template #prefix>
                <n-icon color="#f0a020"><i class="mdi mdi-star-half-full" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="活跃专家" :value="activeExperts">
              <template #prefix>
                <n-icon color="#18a058"><i class="mdi mdi-account-check" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-section">
      <n-grid :cols="4" :x-gap="16" :y-gap="16">
        <!-- 专家列表 -->
        <n-grid-item :span="3">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">专家库管理</span>
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
              :columns="expertColumns"
              :data="filteredExperts"
              :pagination="paginationConfig"
              :bordered="false"
              :row-key="row => row.id"
              @update:checked-row-keys="handleCheck"
            />
          </n-card>
        </n-grid-item>

        <!-- 专业领域分布 -->
        <n-grid-item>
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">专业领域分布</span>
            </template>
            <div class="specialty-stats">
              <div v-for="specialty in specialtyStats" :key="specialty.name" class="specialty-item">
                <div class="specialty-info">
                  <span class="specialty-name">{{ specialty.name }}</span>
                  <span class="specialty-count">{{ specialty.count }}</span>
                </div>
                <n-progress
                  :percentage="(specialty.count / totalExperts) * 100"
                  :color="specialty.color"
                  :show-indicator="false"
                  :height="8"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 专家级别分布 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">专家级别分布</span>
            </template>
            <div class="level-distribution">
              <div v-for="level in levelStats" :key="level.name" class="level-item">
                <div class="level-info">
                  <span class="level-name">{{ level.name }}</span>
                  <span class="level-count">{{ level.count }}人</span>
                </div>
                <n-progress
                  :percentage="(level.count / totalExperts) * 100"
                  :color="level.color"
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
                  <span class="region-count">{{ region.count }}人</span>
                </div>
                <n-progress
                  :percentage="(region.count / totalExperts) * 100"
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

    <!-- 专家详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" title="专家详情" style="width: 800px">
      <div v-if="selectedExpert" class="expert-detail">
        <n-tabs type="line" animated>
          <n-tab-pane name="basic" tab="基本信息">
            <n-descriptions :column="2" bordered>
              <n-descriptions-item label="姓名">
                {{ selectedExpert.name }}
              </n-descriptions-item>
              <n-descriptions-item label="性别">
                {{ selectedExpert.gender }}
              </n-descriptions-item>
              <n-descriptions-item label="年龄">
                {{ selectedExpert.age }}岁
              </n-descriptions-item>
              <n-descriptions-item label="专家级别">
                <n-tag :type="getLevelType(selectedExpert.level)">{{ selectedExpert.level }}</n-tag>
              </n-descriptions-item>
              <n-descriptions-item label="专业领域">
                {{ selectedExpert.specialty }}
              </n-descriptions-item>
              <n-descriptions-item label="工作单位">
                {{ selectedExpert.organization }}
              </n-descriptions-item>
              <n-descriptions-item label="职务">
                {{ selectedExpert.position }}
              </n-descriptions-item>
              <n-descriptions-item label="联系电话">
                {{ selectedExpert.phone }}
              </n-descriptions-item>
              <n-descriptions-item label="邮箱">
                {{ selectedExpert.email }}
              </n-descriptions-item>
              <n-descriptions-item label="所在地区">
                {{ selectedExpert.region }}
              </n-descriptions-item>
            </n-descriptions>
          </n-tab-pane>
          <n-tab-pane name="experience" tab="工作经历">
            <div class="experience-list">
              <n-timeline>
                <n-timeline-item
                  v-for="exp in selectedExpert.experience"
                  :key="exp.id"
                  :title="exp.title"
                  :content="exp.description"
                  :time="exp.period"
                />
              </n-timeline>
            </div>
          </n-tab-pane>
          <n-tab-pane name="projects" tab="参与项目">
            <div class="project-list">
              <n-list>
                <n-list-item v-for="project in selectedExpert.projects" :key="project.id">
                  <n-thing>
                    <template #header>
                      <span class="project-name">{{ project.name }}</span>
                    </template>
                    <template #description>
                      <n-space>
                        <n-tag size="small" type="info">{{ project.type }}</n-tag>
                        <span class="project-period">{{ project.period }}</span>
                        <span class="project-role">{{ project.role }}</span>
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

defineOptions({ name: '专家库' })

// 响应式数据
const searchKeyword = ref('')
const selectedSpecialty = ref(null)
const selectedLevel = ref(null)
const selectedRegion = ref(null)
const showDetailModal = ref(false)
const selectedExpert = ref(null)
const checkedRowKeys = ref([])

// 筛选选项
const specialtyOptions = [
  { label: '清洁生产', value: 'clean_production' },
  { label: '环境工程', value: 'environmental_engineering' },
  { label: '化学工程', value: 'chemical_engineering' },
  { label: '机械工程', value: 'mechanical_engineering' },
  { label: '能源工程', value: 'energy_engineering' },
  { label: '材料科学', value: 'materials_science' }
]

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
const experts = ref([
  {
    id: 1,
    name: '张教授',
    gender: '男',
    age: 45,
    level: '国家级',
    specialty: '清洁生产',
    organization: '清华大学环境学院',
    position: '教授',
    phone: '010-12345678',
    email: 'zhang@tsinghua.edu.cn',
    region: '北京',
    status: 'active',
    experience: [
      { id: 1, title: '清华大学环境学院教授', description: '主要从事清洁生产技术研究', period: '2015-至今' },
      { id: 2, title: '中科院环境科学研究所研究员', description: '从事环境工程技术研究', period: '2010-2015' }
    ],
    projects: [
      { id: 1, name: '钢铁行业清洁生产审核', type: '审核项目', period: '2024-2025', role: '首席专家' },
      { id: 2, name: '化工企业清洁生产技术改造', type: '技术改造', period: '2023-2024', role: '技术顾问' }
    ]
  },
  {
    id: 2,
    name: '李博士',
    gender: '女',
    age: 38,
    level: '省级',
    specialty: '环境工程',
    organization: '上海交通大学环境科学与工程学院',
    position: '副教授',
    phone: '021-87654321',
    email: 'li@sjtu.edu.cn',
    region: '上海',
    status: 'active',
    experience: [
      { id: 3, title: '上海交通大学副教授', description: '主要从事环境工程技术研究', period: '2018-至今' }
    ],
    projects: [
      { id: 3, name: '工业园区环境管理', type: '管理咨询', period: '2024', role: '项目负责人' }
    ]
  },
  {
    id: 3,
    name: '王工程师',
    gender: '男',
    age: 42,
    level: '市级',
    specialty: '化学工程',
    organization: '广东省环境科学研究院',
    position: '高级工程师',
    phone: '020-11111111',
    email: 'wang@gdepb.gov.cn',
    region: '广东',
    status: 'active',
    experience: [
      { id: 4, title: '广东省环境科学研究院高级工程师', description: '主要从事化学工程研究', period: '2016-至今' }
    ],
    projects: [
      { id: 4, name: '化工企业清洁生产审核', type: '审核项目', period: '2023-2024', role: '技术专家' }
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
const expertColumns = [
  {
    type: 'selection'
  },
  {
    title: '姓名',
    key: 'name',
    width: 100
  },
  {
    title: '性别',
    key: 'gender',
    width: 80
  },
  {
    title: '年龄',
    key: 'age',
    width: 80
  },
  {
    title: '专家级别',
    key: 'level',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: getLevelType(row.level) }, { default: () => row.level })
  },
  {
    title: '专业领域',
    key: 'specialty',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: 'info' }, { default: () => row.specialty })
  },
  {
    title: '工作单位',
    key: 'organization',
    width: 200,
    ellipsis: { tooltip: true }
  },
  {
    title: '职务',
    key: 'position',
    width: 120
  },
  {
    title: '所在地区',
    key: 'region',
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
        onClick: () => editExpert(row)
      }, { default: () => '编辑' })
    ]
  }
]

// 计算属性
const totalExperts = computed(() => experts.value.length)
const nationalExperts = computed(() => experts.value.filter(e => e.level === '国家级').length)
const provincialExperts = computed(() => experts.value.filter(e => e.level === '省级').length)
const activeExperts = computed(() => experts.value.filter(e => e.status === 'active').length)

const filteredExperts = computed(() => {
  let filtered = experts.value
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(e => 
      e.name.toLowerCase().includes(keyword) || 
      e.specialty.toLowerCase().includes(keyword) ||
      e.organization.toLowerCase().includes(keyword)
    )
  }
  
  if (selectedSpecialty.value) {
    filtered = filtered.filter(e => e.specialty === selectedSpecialty.value)
  }
  
  if (selectedLevel.value) {
    filtered = filtered.filter(e => e.level === selectedLevel.value)
  }
  
  if (selectedRegion.value) {
    filtered = filtered.filter(e => e.region === selectedRegion.value)
  }
  
  return filtered
})

const specialtyStats = computed(() => {
  const stats = {}
  experts.value.forEach(expert => {
    stats[expert.specialty] = (stats[expert.specialty] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050', '#9c27b0', '#ff9800'][index % 6]
  }))
})

const levelStats = computed(() => {
  const stats = {}
  experts.value.forEach(expert => {
    stats[expert.level] = (stats[expert.level] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#d03050', '#f0a020', '#18a058'][index % 3]
  }))
})

const regionStats = computed(() => {
  const stats = {}
  experts.value.forEach(expert => {
    stats[expert.region] = (stats[expert.region] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050', '#9c27b0', '#ff9800'][index % 6]
  }))
})

// 方法
const handleSearch = () => {
  console.log('搜索专家:', { searchKeyword: searchKeyword.value, selectedSpecialty: selectedSpecialty.value, selectedLevel: selectedLevel.value, selectedRegion: selectedRegion.value })
}

const handleAdd = () => {
  console.log('新增专家')
}

const handleExport = () => {
  console.log('导出专家')
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

const viewDetail = (expert) => {
  selectedExpert.value = expert
  showDetailModal.value = true
}

const editExpert = (expert) => {
  console.log('编辑专家:', expert)
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
  console.log('专家库模块已加载')
})
</script>

<style scoped>
.expert-database-container {
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

.specialty-stats {
  padding: 16px 0;
}

.specialty-item {
  margin-bottom: 16px;
}

.specialty-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.specialty-name {
  font-size: 14px;
  color: #666;
}

.specialty-count {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.level-distribution,
.region-distribution {
  padding: 16px 0;
}

.level-item,
.region-item {
  margin-bottom: 12px;
}

.level-info,
.region-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.level-name,
.region-name {
  font-size: 13px;
  color: #666;
}

.level-count,
.region-count {
  font-size: 13px;
  font-weight: 600;
  color: #333;
}

.expert-detail {
  padding: 16px 0;
}

.experience-list,
.project-list {
  padding: 16px 0;
}

.project-name {
  font-weight: 500;
  color: #333;
}

.project-period,
.project-role {
  font-size: 12px;
  color: #999;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .expert-database-container {
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
