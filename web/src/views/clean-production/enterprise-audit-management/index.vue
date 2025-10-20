<template>
  <div class="enterprise-audit-container">
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section">
      <n-card :bordered="false" class="search-card">
        <n-space justify="space-between" align="center">
          <n-space>
            <n-input
              v-model:value="searchKeyword"
              placeholder="搜索企业名称或统一社会信用代码"
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
              v-model:value="selectedStatus"
              placeholder="审核状态"
              style="width: 150px"
              :options="statusOptions"
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
              导出
            </n-button>
            <n-button type="primary" @click="handleAdd">
              <template #icon>
                <n-icon><i class="mdi mdi-plus" /></n-icon>
              </template>
              新增企业
            </n-button>
          </n-space>
        </n-space>
      </n-card>
    </div>

    <!-- 统计概览 -->
    <div class="stats-section">
      <n-grid :cols="5" :x-gap="16">
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="总企业数" :value="totalEnterprises">
              <template #prefix>
                <n-icon color="#2080f0"><i class="mdi mdi-domain" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="待审核" :value="pendingAudits">
              <template #prefix>
                <n-icon color="#f0a020"><i class="mdi mdi-clock-outline" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="审核中" :value="auditing">
              <template #prefix>
                <n-icon color="#18a058"><i class="mdi mdi-play-circle" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="已完成" :value="completedAudits">
              <template #prefix>
                <n-icon color="#36ad6a"><i class="mdi mdi-check-circle" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="不合格" :value="failedAudits">
              <template #prefix>
                <n-icon color="#d03050"><i class="mdi mdi-close-circle" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-section">
      <n-grid :cols="4" :x-gap="16" :y-gap="16">
        <!-- 企业列表 -->
        <n-grid-item :span="3">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">企业审核管理</span>
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
              :columns="enterpriseColumns"
              :data="filteredEnterprises"
              :pagination="paginationConfig"
              :bordered="false"
              :row-key="row => row.id"
              @update:checked-row-keys="handleCheck"
            />
          </n-card>
        </n-grid-item>

        <!-- 审核进度统计 -->
        <n-grid-item>
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">审核进度统计</span>
            </template>
            <div class="progress-stats">
              <div v-for="status in auditStatusStats" :key="status.name" class="status-item">
                <div class="status-info">
                  <span class="status-name">{{ status.name }}</span>
                  <span class="status-count">{{ status.count }}</span>
                </div>
                <n-progress
                  :percentage="(status.count / totalEnterprises) * 100"
                  :color="status.color"
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
                  <span class="industry-count">{{ industry.count }}家</span>
                </div>
                <n-progress
                  :percentage="(industry.count / totalEnterprises) * 100"
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
                  <span class="region-count">{{ region.count }}家</span>
                </div>
                <n-progress
                  :percentage="(region.count / totalEnterprises) * 100"
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

    <!-- 企业详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" title="企业详情" style="width: 800px">
      <div v-if="selectedEnterprise" class="enterprise-detail">
        <n-tabs type="line" animated>
          <n-tab-pane name="basic" tab="基本信息">
            <n-descriptions :column="2" bordered>
              <n-descriptions-item label="企业名称">
                {{ selectedEnterprise.name }}
              </n-descriptions-item>
              <n-descriptions-item label="统一社会信用代码">
                {{ selectedEnterprise.creditCode }}
              </n-descriptions-item>
              <n-descriptions-item label="所属行业">
                {{ selectedEnterprise.industry }}
              </n-descriptions-item>
              <n-descriptions-item label="所在地区">
                {{ selectedEnterprise.region }}
              </n-descriptions-item>
              <n-descriptions-item label="企业规模">
                {{ selectedEnterprise.scale }}
              </n-descriptions-item>
              <n-descriptions-item label="联系人">
                {{ selectedEnterprise.contact }}
              </n-descriptions-item>
              <n-descriptions-item label="联系电话">
                {{ selectedEnterprise.phone }}
              </n-descriptions-item>
              <n-descriptions-item label="审核状态">
                <n-tag :type="getStatusType(selectedEnterprise.status)">{{ selectedEnterprise.statusText }}</n-tag>
              </n-descriptions-item>
            </n-descriptions>
          </n-tab-pane>
          <n-tab-pane name="audit" tab="审核信息">
            <n-descriptions :column="2" bordered>
              <n-descriptions-item label="审核开始时间">
                {{ selectedEnterprise.auditStartDate }}
              </n-descriptions-item>
              <n-descriptions-item label="预计完成时间">
                {{ selectedEnterprise.expectedEndDate }}
              </n-descriptions-item>
              <n-descriptions-item label="审核机构">
                {{ selectedEnterprise.auditOrg }}
              </n-descriptions-item>
              <n-descriptions-item label="审核专家">
                {{ selectedEnterprise.auditExpert }}
              </n-descriptions-item>
              <n-descriptions-item label="审核进度">
                <n-progress :percentage="selectedEnterprise.progress" />
              </n-descriptions-item>
              <n-descriptions-item label="审核结果">
                <n-tag v-if="selectedEnterprise.result" :type="getResultType(selectedEnterprise.result)">
                  {{ selectedEnterprise.result }}
                </n-tag>
                <span v-else>-</span>
              </n-descriptions-item>
            </n-descriptions>
          </n-tab-pane>
        </n-tabs>
      </div>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'

defineOptions({ name: '企业清洁生产审核管理' })

// 响应式数据
const searchKeyword = ref('')
const selectedIndustry = ref(null)
const selectedStatus = ref(null)
const selectedRegion = ref(null)
const showDetailModal = ref(false)
const selectedEnterprise = ref(null)
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

const statusOptions = [
  { label: '待审核', value: 'pending' },
  { label: '审核中', value: 'auditing' },
  { label: '已完成', value: 'completed' },
  { label: '不合格', value: 'failed' }
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
const enterprises = ref([
  {
    id: 1,
    name: '北京钢铁集团有限公司',
    creditCode: '91110000123456789X',
    industry: '钢铁',
    region: '北京',
    scale: '大型',
    contact: '张经理',
    phone: '010-12345678',
    status: 'auditing',
    statusText: '审核中',
    auditStartDate: '2025-01-01',
    expectedEndDate: '2025-03-31',
    auditOrg: '中国清洁生产中心',
    auditExpert: '李专家',
    progress: 65,
    result: null
  },
  {
    id: 2,
    name: '上海化工股份有限公司',
    creditCode: '91310000987654321Y',
    industry: '化工',
    region: '上海',
    scale: '中型',
    contact: '王总',
    phone: '021-87654321',
    status: 'completed',
    statusText: '已完成',
    auditStartDate: '2024-10-01',
    expectedEndDate: '2024-12-31',
    auditOrg: '上海环境科学研究院',
    auditExpert: '陈专家',
    progress: 100,
    result: '合格'
  },
  {
    id: 3,
    name: '广东建材有限公司',
    creditCode: '91440000111222333Z',
    industry: '建材',
    region: '广东',
    scale: '小型',
    contact: '刘主任',
    phone: '020-11111111',
    status: 'pending',
    statusText: '待审核',
    auditStartDate: null,
    expectedEndDate: null,
    auditOrg: null,
    auditExpert: null,
    progress: 0,
    result: null
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
const enterpriseColumns = [
  {
    type: 'selection'
  },
  {
    title: '企业名称',
    key: 'name',
    width: 200,
    ellipsis: { tooltip: true }
  },
  {
    title: '统一社会信用代码',
    key: 'creditCode',
    width: 180,
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
    title: '企业规模',
    key: 'scale',
    width: 100
  },
  {
    title: '审核状态',
    key: 'status',
    width: 120,
    render: (row) => h('n-tag', { size: 'small', type: getStatusType(row.status) }, { default: () => row.statusText })
  },
  {
    title: '审核进度',
    key: 'progress',
    width: 120,
    render: (row) => h('n-progress', { percentage: row.progress, size: 'small' })
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
        onClick: () => editEnterprise(row)
      }, { default: () => '编辑' })
    ]
  }
]

// 计算属性
const totalEnterprises = computed(() => enterprises.value.length)
const pendingAudits = computed(() => enterprises.value.filter(e => e.status === 'pending').length)
const auditing = computed(() => enterprises.value.filter(e => e.status === 'auditing').length)
const completedAudits = computed(() => enterprises.value.filter(e => e.status === 'completed').length)
const failedAudits = computed(() => enterprises.value.filter(e => e.status === 'failed').length)

const filteredEnterprises = computed(() => {
  let filtered = enterprises.value
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    filtered = filtered.filter(e => 
      e.name.toLowerCase().includes(keyword) || 
      e.creditCode.toLowerCase().includes(keyword)
    )
  }
  
  if (selectedIndustry.value) {
    filtered = filtered.filter(e => e.industry === selectedIndustry.value)
  }
  
  if (selectedStatus.value) {
    filtered = filtered.filter(e => e.status === selectedStatus.value)
  }
  
  if (selectedRegion.value) {
    filtered = filtered.filter(e => e.region === selectedRegion.value)
  }
  
  return filtered
})

const auditStatusStats = computed(() => [
  { name: '待审核', count: pendingAudits.value, color: '#f0a020' },
  { name: '审核中', count: auditing.value, color: '#18a058' },
  { name: '已完成', count: completedAudits.value, color: '#36ad6a' },
  { name: '不合格', count: failedAudits.value, color: '#d03050' }
])

const industryStats = computed(() => {
  const stats = {}
  enterprises.value.forEach(enterprise => {
    stats[enterprise.industry] = (stats[enterprise.industry] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050', '#9c27b0', '#ff9800', '#4caf50'][index % 7]
  }))
})

const regionStats = computed(() => {
  const stats = {}
  enterprises.value.forEach(enterprise => {
    stats[enterprise.region] = (stats[enterprise.region] || 0) + 1
  })
  return Object.entries(stats).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050', '#9c27b0', '#ff9800'][index % 6]
  }))
})

// 方法
const handleSearch = () => {
  console.log('搜索企业:', { searchKeyword: searchKeyword.value, selectedIndustry: selectedIndustry.value, selectedStatus: selectedStatus.value, selectedRegion: selectedRegion.value })
}

const handleAdd = () => {
  console.log('新增企业')
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

const viewDetail = (enterprise) => {
  selectedEnterprise.value = enterprise
  showDetailModal.value = true
}

const editEnterprise = (enterprise) => {
  console.log('编辑企业:', enterprise)
}

const getStatusType = (status) => {
  const statusMap = {
    pending: 'warning',
    auditing: 'info',
    completed: 'success',
    failed: 'error'
  }
  return statusMap[status] || 'default'
}

const getResultType = (result) => {
  return result === '合格' ? 'success' : 'error'
}

onMounted(() => {
  console.log('企业清洁生产审核管理模块已加载')
})
</script>

<style scoped>
.enterprise-audit-container {
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

.progress-stats {
  padding: 16px 0;
}

.status-item {
  margin-bottom: 16px;
}

.status-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.status-name {
  font-size: 14px;
  color: #666;
}

.status-count {
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

.enterprise-detail {
  padding: 16px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .enterprise-audit-container {
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
