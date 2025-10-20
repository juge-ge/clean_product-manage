<template>
  <div class="meetings-publicity-container">
    <!-- 搜索和筛选区域 -->
    <div class="search-filter-section">
      <n-card :bordered="false" class="search-card">
        <n-space justify="space-between" align="center">
          <n-space>
            <n-input
              v-model:value="searchKeyword"
              placeholder="搜索会议或宣传活动"
              style="width: 300px"
              clearable
            >
              <template #prefix>
                <n-icon><i class="mdi mdi-magnify" /></n-icon>
              </template>
            </n-input>
            <n-select
              v-model:value="selectedType"
              placeholder="选择类型"
              style="width: 150px"
              :options="typeOptions"
              clearable
            />
            <n-select
              v-model:value="selectedStatus"
              placeholder="选择状态"
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
          <n-button type="primary" @click="handleAdd">
            <template #icon>
              <n-icon><i class="mdi mdi-plus" /></n-icon>
            </template>
            新建活动
          </n-button>
        </n-space>
      </n-card>
    </div>

    <!-- 统计卡片区域 -->
    <div class="stats-section">
      <n-grid :cols="4" :x-gap="16">
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="总活动数" :value="totalActivities">
              <template #prefix>
                <n-icon color="#2080f0"><i class="mdi mdi-calendar-multiple" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="进行中" :value="ongoingActivities">
              <template #prefix>
                <n-icon color="#18a058"><i class="mdi mdi-play-circle" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="已完成" :value="completedActivities">
              <template #prefix>
                <n-icon color="#f0a020"><i class="mdi mdi-check-circle" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
        <n-grid-item>
          <n-card :bordered="false" class="stat-card">
            <n-statistic label="参与人数" :value="totalParticipants">
              <template #prefix>
                <n-icon color="#d03050"><i class="mdi mdi-account-group" /></n-icon>
              </template>
            </n-statistic>
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 主要内容区域 -->
    <div class="content-section">
      <n-grid :cols="3" :x-gap="16" :y-gap="16">
        <!-- 即将举行的活动 -->
        <n-grid-item :span="2">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">即将举行的活动</span>
                <n-button text type="primary" @click="viewAllUpcoming">
                  查看全部 <n-icon><i class="mdi mdi-arrow-right" /></n-icon>
                </n-button>
              </div>
            </template>
            <n-list hoverable clickable>
              <n-list-item v-for="item in upcomingActivities" :key="item.id" @click="viewDetail(item)">
                <n-thing>
                  <template #header>
                    <div class="activity-header">
                      <span class="activity-title">{{ item.title }}</span>
                      <n-tag :type="getStatusType(item.status)" size="small">{{ item.statusText }}</n-tag>
                    </div>
                  </template>
                  <template #description>
                    <n-space align="center">
                      <n-icon><i class="mdi mdi-calendar" /></n-icon>
                      <span>{{ item.date }}</span>
                      <n-icon><i class="mdi mdi-clock" /></n-icon>
                      <span>{{ item.time }}</span>
                      <n-icon><i class="mdi mdi-map-marker" /></n-icon>
                      <span>{{ item.location }}</span>
                    </n-space>
                  </template>
                  <template #footer>
                    <n-space>
                      <n-tag size="small" type="info">{{ item.type }}</n-tag>
                      <span class="participant-count">{{ item.participants }}人参与</span>
                    </n-space>
                  </template>
                </n-thing>
              </n-list-item>
            </n-list>
          </n-card>
        </n-grid-item>

        <!-- 活动类型分布 -->
        <n-grid-item>
          <n-card :bordered="false" class="content-card">
            <template #header>
              <span class="header-title">活动类型分布</span>
            </template>
            <div class="chart-container">
              <div v-for="type in activityTypes" :key="type.name" class="type-item">
                <div class="type-info">
                  <span class="type-name">{{ type.name }}</span>
                  <span class="type-count">{{ type.count }}</span>
                </div>
                <n-progress
                  :percentage="(type.count / totalActivities) * 100"
                  :color="type.color"
                  :show-indicator="false"
                  :height="8"
                />
              </div>
            </div>
          </n-card>
        </n-grid-item>

        <!-- 最近活动 -->
        <n-grid-item :span="3">
          <n-card :bordered="false" class="content-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">最近活动</span>
                <n-button text type="primary" @click="viewAllRecent">
                  查看全部 <n-icon><i class="mdi mdi-arrow-right" /></n-icon>
                </n-button>
              </div>
            </template>
            <n-data-table
              :columns="recentColumns"
              :data="recentActivities"
              :pagination="false"
              :bordered="false"
              size="small"
            />
          </n-card>
        </n-grid-item>
      </n-grid>
    </div>

    <!-- 活动详情弹窗 -->
    <n-modal v-model:show="showDetailModal" preset="card" title="活动详情" style="width: 600px">
      <div v-if="selectedActivity" class="activity-detail">
        <n-descriptions :column="2" bordered>
          <n-descriptions-item label="活动标题">
            {{ selectedActivity.title }}
          </n-descriptions-item>
          <n-descriptions-item label="活动类型">
            <n-tag :type="getTypeColor(selectedActivity.type)">{{ selectedActivity.type }}</n-tag>
          </n-descriptions-item>
          <n-descriptions-item label="活动时间">
            {{ selectedActivity.date }} {{ selectedActivity.time }}
          </n-descriptions-item>
          <n-descriptions-item label="活动地点">
            {{ selectedActivity.location }}
          </n-descriptions-item>
          <n-descriptions-item label="参与人数">
            {{ selectedActivity.participants }}人
          </n-descriptions-item>
          <n-descriptions-item label="活动状态">
            <n-tag :type="getStatusType(selectedActivity.status)">{{ selectedActivity.statusText }}</n-tag>
          </n-descriptions-item>
          <n-descriptions-item label="活动描述" :span="2">
            {{ selectedActivity.description }}
          </n-descriptions-item>
        </n-descriptions>
      </div>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

defineOptions({ name: '会议与宣传' })

// 响应式数据
const searchKeyword = ref('')
const selectedType = ref(null)
const selectedStatus = ref(null)
const showDetailModal = ref(false)
const selectedActivity = ref(null)

// 筛选选项
const typeOptions = [
  { label: '会议', value: 'meeting' },
  { label: '培训', value: 'training' },
  { label: '宣传', value: 'publicity' },
  { label: '展览', value: 'exhibition' }
]

const statusOptions = [
  { label: '即将开始', value: 'upcoming' },
  { label: '进行中', value: 'ongoing' },
  { label: '已完成', value: 'completed' },
  { label: '已取消', value: 'cancelled' }
]

// 模拟数据
const activities = ref([
  {
    id: 1,
    title: '2025年清洁生产审核评估工作会议',
    type: '会议',
    date: '2025-01-15',
    time: '09:00-12:00',
    location: '北京国际会议中心',
    participants: 120,
    status: 'upcoming',
    statusText: '即将开始',
    description: '总结2024年清洁生产审核评估工作，部署2025年重点工作任务。'
  },
  {
    id: 2,
    title: '清洁生产技术培训研讨会',
    type: '培训',
    date: '2025-01-20',
    time: '14:00-17:00',
    location: '上海科技馆',
    participants: 80,
    status: 'upcoming',
    statusText: '即将开始',
    description: '针对清洁生产新技术、新工艺进行专题培训。'
  },
  {
    id: 3,
    title: '绿色制造宣传周活动',
    type: '宣传',
    date: '2025-01-10',
    time: '全天',
    location: '深圳市民中心',
    participants: 200,
    status: 'ongoing',
    statusText: '进行中',
    description: '宣传绿色制造理念，推广清洁生产技术。'
  },
  {
    id: 4,
    title: '清洁生产成果展览会',
    type: '展览',
    date: '2025-01-05',
    time: '09:00-18:00',
    location: '广州国际会展中心',
    participants: 500,
    status: 'completed',
    statusText: '已完成',
    description: '展示清洁生产审核评估成果，促进技术交流。'
  }
])

// 计算属性
const totalActivities = computed(() => activities.value.length)
const ongoingActivities = computed(() => activities.value.filter(a => a.status === 'ongoing').length)
const completedActivities = computed(() => activities.value.filter(a => a.status === 'completed').length)
const totalParticipants = computed(() => activities.value.reduce((sum, a) => sum + a.participants, 0))

const upcomingActivities = computed(() => 
  activities.value.filter(a => a.status === 'upcoming').slice(0, 5)
)

const recentActivities = computed(() => 
  activities.value.filter(a => a.status === 'completed' || a.status === 'ongoing').slice(0, 10)
)

const activityTypes = computed(() => {
  const types = {}
  activities.value.forEach(activity => {
    types[activity.type] = (types[activity.type] || 0) + 1
  })
  return Object.entries(types).map(([name, count], index) => ({
    name,
    count,
    color: ['#2080f0', '#18a058', '#f0a020', '#d03050'][index % 4]
  }))
})

// 表格列定义
const recentColumns = [
  {
    title: '活动名称',
    key: 'title',
    ellipsis: { tooltip: true }
  },
  {
    title: '类型',
    key: 'type',
    width: 80,
    render: (row) => h('n-tag', { size: 'small', type: getTypeColor(row.type) }, { default: () => row.type })
  },
  {
    title: '时间',
    key: 'date',
    width: 120
  },
  {
    title: '地点',
    key: 'location',
    width: 150,
    ellipsis: { tooltip: true }
  },
  {
    title: '参与人数',
    key: 'participants',
    width: 100
  },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render: (row) => h('n-tag', { size: 'small', type: getStatusType(row.status) }, { default: () => row.statusText })
  }
]

// 方法
const handleSearch = () => {
  console.log('搜索:', { searchKeyword: searchKeyword.value, selectedType: selectedType.value, selectedStatus: selectedStatus.value })
}

const handleAdd = () => {
  console.log('新建活动')
}

const viewDetail = (activity) => {
  selectedActivity.value = activity
  showDetailModal.value = true
}

const viewAllUpcoming = () => {
  console.log('查看全部即将举行的活动')
}

const viewAllRecent = () => {
  console.log('查看全部最近活动')
}

const getStatusType = (status) => {
  const statusMap = {
    upcoming: 'info',
    ongoing: 'success',
    completed: 'warning',
    cancelled: 'error'
  }
  return statusMap[status] || 'default'
}

const getTypeColor = (type) => {
  const typeMap = {
    '会议': 'info',
    '培训': 'success',
    '宣传': 'warning',
    '展览': 'error'
  }
  return typeMap[type] || 'default'
}

onMounted(() => {
  console.log('会议与宣传模块已加载')
})
</script>

<style scoped>
.meetings-publicity-container {
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

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.activity-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  flex: 1;
  margin-right: 12px;
}

.chart-container {
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

.participant-count {
  font-size: 12px;
  color: #999;
}

.activity-detail {
  padding: 16px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .meetings-publicity-container {
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
