<template>
  <div class="notice-container">
    <!-- 首页模式 -->
    <div v-if="displayMode === 'home'">
      <!-- 搜索框 -->
      <div class="search-wrapper">
        <n-input-group style="width: 300px">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索"
            clearable
            class="search-input"
          />
          <n-button type="primary" @click="handleSearch" style="padding: 0 24px">
            搜索
          </n-button>
        </n-input-group>
      </div>

      <!-- 两栏布局 -->
      <div class="notice-grid mt-4">
        <!-- 国家通知公告 -->
        <div class="notice-column">
          <n-card :bordered="false" class="notice-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">国家通知公告</span>
                <n-button text type="primary" @click="goToList('national')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <n-list hoverable clickable>
              <n-list-item v-for="item in nationalNotices.slice(0, 5)" :key="item.id">
                <n-thing>
                  <template #header>
                    <a href="javascript:;" @click="goToDetail(item.id)" class="notice-title">
                      {{ item.title }}
                    </a>
                  </template>
                  <template #description>
                    <n-space align="center">
                      <n-tag size="small" type="info">{{ item.source }}</n-tag>
                      <span class="notice-date">{{ item.publishDate }}</span>
                    </n-space>
                  </template>
                </n-thing>
              </n-list-item>
            </n-list>
          </n-card>
        </div>

        <!-- 各省通知公告 -->
        <div class="notice-column">
          <n-card :bordered="false" class="notice-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">各省通知公告</span>
                <n-button text type="primary" @click="goToList('provincial')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <n-list hoverable clickable>
              <n-list-item v-for="item in provincialNotices.slice(0, 5)" :key="item.id">
                <n-thing>
                  <template #header>
                    <a href="javascript:;" @click="goToDetail(item.id)" class="notice-title">
                      {{ item.title }}
                    </a>
                  </template>
                  <template #description>
                    <n-space>
                      <n-tag size="small" type="success">{{ item.province }}</n-tag>
                      <span class="notice-date">{{ item.publishDate }}</span>
                    </n-space>
                  </template>
                </n-thing>
              </n-list-item>
            </n-list>
          </n-card>
        </div>
      </div>
    </div>

    <!-- 列表模式 -->
    <div v-else-if="displayMode === 'list'">

      <!-- 列表内容 -->
      <n-card class="mt-2">
        <template #header>
          <n-space justify="space-between" align="center">
            <n-space align="center">
              <span class="page-title">{{ getListTitle() }}</span>
              <n-button 
                type="primary" 
                ghost 
                size="small" 
                @click="goHome"
                style="margin-left: 16px"
              >
                返回通知公告
              </n-button>
            </n-space>
            <n-space>
              <n-input
                v-model:value="searchKeyword"
                placeholder="请输入关键词搜索"
                style="width: 200px"
              />
              <n-button type="primary" @click="handleSearch">搜索</n-button>
            </n-space>
          </n-space>
        </template>

        <n-list hoverable clickable>
          <n-list-item v-for="item in getFilteredNotices()" :key="item.id" class="list-item-optimized">
            <div class="list-item-content">
              <div class="title-section">
                <a href="javascript:;" @click="goToDetail(item.id)" class="notice-title">
                  {{ item.title }}
                </a>
                <template v-if="item.province">
                  <n-tag size="small" type="success" class="source-tag">{{ item.province }}</n-tag>
                </template>
                <template v-else>
                  <n-tag size="small" type="info" class="source-tag">{{ item.source }}</n-tag>
                </template>
              </div>
              <div class="date-section">
                <span class="notice-date">{{ item.publishDate }}</span>
              </div>
            </div>
          </n-list-item>
        </n-list>

        <!-- 分页 -->
        <div class="pagination-wrapper">
          <div class="pagination-content">
            <span class="total-count">共{{ getTotalCount() }}条</span>
            <n-pagination
              v-model:page="currentPage"
              :page-size="pageSize"
              :item-count="getTotalCount()"
              show-quick-jumper
              show-size-picker
              :page-sizes="[10, 20, 30, 50]"
              :page-count="Math.ceil(getTotalCount() / pageSize)"
              class="custom-pagination"
            />
          </div>
        </div>
      </n-card>
    </div>

    <!-- 详情弹窗 -->
    <notice-detail-modal
      v-model:show="showDetailModal"
      :notice-id="currentNoticeId"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { usePermissionStore } from '@/store'
import NoticeDetailModal from './components/NoticeDetailModal.vue'

// 使用项目自带的图标
const searchIcon = 'mdi-account-search'
const arrowRightIcon = 'mdi-arrow-right'

const router = useRouter()
const searchKeyword = ref('')

// 生成Mock数据的函数
const generateMockNotices = (type, count = 20) => {
  const notices = []
  const sources = type === 'national' 
    ? ['生态环境部', '国家发改委', '工信部', '财政部', '科技部', '农业农村部', '商务部', '应急管理部']
    : ['湖南省生态环境厅', '江苏省生态环境厅', '浙江省生态环境厅', '广东省生态环境厅', '山东省生态环境厅', '河南省生态环境厅', '四川省生态环境厅', '湖北省生态环境厅']
  
  const titles = type === 'national' 
    ? [
        '关于开展2025年度清洁生产审核评估工作的通知',
        '清洁生产审核评估专家库专家征集公告',
        '关于印发《清洁生产审核评估管理办法》的通知',
        '清洁生产技术创新项目申报指南',
        '清洁生产审核评估标准体系更新通知',
        '清洁生产审核评估专家培训计划',
        '清洁生产审核评估质量提升专项行动',
        '清洁生产审核评估信息化建设方案',
        '清洁生产审核评估国际合作项目',
        '清洁生产审核评估成果展示活动',
        '清洁生产审核评估政策解读培训',
        '清洁生产审核评估技术规范修订',
        '清洁生产审核评估专家考核办法',
        '清洁生产审核评估数据统计报告',
        '清洁生产审核评估典型案例汇编',
        '清洁生产审核评估工作推进会通知',
        '清洁生产审核评估技术交流会议',
        '清洁生产审核评估标准宣贯培训',
        '清洁生产审核评估质量检查通知',
        '清洁生产审核评估工作总结报告'
      ]
    : [
        '湖南省2025年清洁生产审核重点企业名单公示',
        '江苏省清洁生产审核评估专家选拔通知',
        '浙江省清洁生产示范企业认定结果公示',
        '广东省清洁生产审核评估工作部署',
        '山东省清洁生产审核评估专家库建设',
        '河南省清洁生产审核评估质量提升',
        '四川省清洁生产审核评估技术创新',
        '湖北省清洁生产审核评估标准制定',
        '福建省清洁生产审核评估专家培训',
        '安徽省清洁生产审核评估工作推进',
        '江西省清洁生产审核评估质量检查',
        '河北省清洁生产审核评估专家选拔',
        '山西省清洁生产审核评估技术创新',
        '内蒙古清洁生产审核评估工作部署',
        '辽宁省清洁生产审核评估专家库建设',
        '吉林省清洁生产审核评估质量提升',
        '黑龙江省清洁生产审核评估标准制定',
        '陕西省清洁生产审核评估专家培训',
        '甘肃省清洁生产审核评估工作推进',
        '青海省清洁生产审核评估质量检查',
        '宁夏清洁生产审核评估专家选拔'
      ]
  
  for (let i = 0; i < count; i++) {
    const randomMonth = Math.floor(Math.random() * 12) + 1
    const randomDay = Math.floor(Math.random() * 28) + 1
    const randomSource = sources[Math.floor(Math.random() * sources.length)]
    
    notices.push({
      id: type === 'national' ? i + 1 : i + 101,
      title: titles[i],
      publishDate: `2025-${String(randomMonth).padStart(2, '0')}-${String(randomDay).padStart(2, '0')}`,
      source: randomSource,
      province: type === 'provincial' ? randomSource.replace('生态环境厅', '') : undefined
    })
  }
  
  // 按日期排序，最新的在前面
  return notices.sort((a, b) => new Date(b.publishDate) - new Date(a.publishDate))
}

// 生成Mock数据 - 各20条
const nationalNotices = ref(generateMockNotices('national', 20))
const provincialNotices = ref(generateMockNotices('provincial', 20))

// 显示详情弹窗
const showDetailModal = ref(false)
const currentNoticeId = ref(null)

// 控制显示模式：'home' 为首页，'list' 为列表页
const displayMode = ref('home')
const currentListType = ref('') // 当前显示的类型：'national' 或 'provincial'

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10) // 调整为每页显示10条

const goToDetail = (id) => {
  currentNoticeId.value = id
  showDetailModal.value = true
}

// 切换到列表显示模式
const goToList = (type) => {
  console.log('切换到列表模式:', type)
  currentListType.value = type
  displayMode.value = 'list'
  currentPage.value = 1 // 重置分页
}

// 搜索处理
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    console.log('搜索关键词:', searchKeyword.value)
    currentListType.value = 'search'
    displayMode.value = 'list'
    currentPage.value = 1 // 重置分页
  }
}

// 返回首页
const goHome = () => {
  displayMode.value = 'home'
  currentListType.value = ''
  searchKeyword.value = ''
  currentPage.value = 1
}

// 获取列表标题
const getListTitle = () => {
  if (currentListType.value === 'national') return '国家通知公告'
  if (currentListType.value === 'provincial') return '各省通知公告'
  if (currentListType.value === 'search') return '搜索结果'
  return '通知列表'
}

// 获取过滤后的通知列表
const getFilteredNotices = () => {
  let notices = []
  
  if (currentListType.value === 'national') {
    notices = nationalNotices.value
  } else if (currentListType.value === 'provincial') {
    notices = provincialNotices.value
  } else if (currentListType.value === 'search') {
    // 搜索逻辑：合并所有通知并过滤
    const allNotices = [...nationalNotices.value, ...provincialNotices.value]
    const keyword = searchKeyword.value.toLowerCase()
    notices = allNotices.filter(item => 
      item.title.toLowerCase().includes(keyword) ||
      (item.source && item.source.toLowerCase().includes(keyword)) ||
      (item.province && item.province.toLowerCase().includes(keyword))
    )
  }
  
  // 分页处理
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return notices.slice(start, end)
}

// 获取总数
const getTotalCount = () => {
  if (currentListType.value === 'national') return nationalNotices.value.length
  if (currentListType.value === 'provincial') return provincialNotices.value.length
  if (currentListType.value === 'search') {
    const allNotices = [...nationalNotices.value, ...provincialNotices.value]
    const keyword = searchKeyword.value.toLowerCase()
    return allNotices.filter(item => 
      item.title.toLowerCase().includes(keyword) ||
      (item.source && item.source.toLowerCase().includes(keyword)) ||
      (item.province && item.province.toLowerCase().includes(keyword))
    ).length
  }
  return 0
}
</script>

<style scoped>
.notice-container {
  padding: 12px; /* 减少容器内边距 */
}

.search-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 12px; /* 减少搜索框下方间距 */
}

.search-input :deep(.n-input__placeholder) {
  display: flex;
  align-items: center;
  justify-content: center;
}

.notice-grid {
  display: flex;
  gap: 12px;
  position: relative;
}

.notice-grid::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  border-left: 1px dashed #e5e5e5;
  transform: translateX(-50%);
}

.notice-column {
  flex: 1;
}

.notice-card {
  height: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 8px;
  border-bottom: 2px solid var(--primary-color);
  margin-bottom: 8px;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.header-action {
  font-size: 14px;
  color: var(--primary-color);
  cursor: pointer;
  
  &:hover {
    opacity: 0.8;
  }
}

.notice-title {
  color: #333;
  text-decoration: none;
  font-size: 15px; /* 调大字体 */
  display: block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  line-height: 1.4; /* 调整行高 */
}

/* 列表模式下的标题样式 */
.list-item-optimized .notice-title {
  font-size: 14px; /* 列表模式下稍微大一点 */
  line-height: 1.5;
  max-width: 100%;
  white-space: normal; /* 允许换行 */
  word-break: break-word; /* 长单词换行 */
}



.notice-title:hover {
  color: #2080f0;
}

.notice-date {
  color: #999;
  font-size: 11px; /* 调小日期字体 */
}

.view-more {
  text-align: right;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.mt-2 {
  margin-top: 8px; /* 减少上方间距 */
}



/* 列表项样式优化 */
:deep(.n-list-item) {
  padding: 6px 0; /* 进一步减少列表项间距 */
}

:deep(.n-thing-main) {
  padding: 2px 0; /* 进一步减少内容区域间距 */
}

:deep(.n-thing-header) {
  margin-bottom: 4px; /* 减少标题下方间距 */
}

:deep(.n-tag) {
  font-size: 11px; /* 调小标签字体 */
  padding: 2px 6px; /* 减少标签内边距 */
}

/* 优化后的列表项布局 */
.list-item-optimized {
  border-bottom: 1px dashed #e5e5e5;
}

.list-item-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  width: 100%;
  gap: 16px;
}

.title-section {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.source-tag {
  flex-shrink: 0;
  margin-left: 8px;
}

.date-section {
  flex-shrink: 0;
  min-width: 80px;
  text-align: right;
}



.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.pagination-wrapper {
  margin-top: 12px;
  padding: 12px 0;
  border-top: 1px solid #e5e5e5;
}

.pagination-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.total-count {
  font-size: 14px;
  color: #666;
  font-weight: 500;
  flex-shrink: 0;
}

.pagination {
  display: flex;
  justify-content: center;
}

/* 分页组件样式优化 */
:deep(.n-pagination) {
  font-size: 13px; /* 调小分页字体 */
}

:deep(.n-pagination-item) {
  min-width: 28px; /* 减少分页按钮宽度 */
  height: 28px; /* 减少分页按钮高度 */
}

:deep(.n-pagination-item__content) {
  padding: 0 6px; /* 减少分页按钮内边距 */
}

:deep(.n-breadcrumb-item a) {
  color: #666;
  text-decoration: none;
}

:deep(.n-breadcrumb-item a:hover) {
  color: #2080f0;
}
</style>