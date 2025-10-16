<template>
  <div class="news-container">
    <!-- 首页模式 -->
    <div v-if="displayMode === 'home'">
      <!-- 搜索框 -->
      <div class="search-wrapper">
        <n-input-group style="width: 300px">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索动态信息"
            clearable
            class="search-input"
          />
          <n-button type="primary" @click="handleSearch" style="padding: 0 24px">
            搜索
          </n-button>
        </n-input-group>
      </div>

      <!-- 三栏布局 -->
      <div class="news-grid mt-4">
        <!-- 国内动态 -->
        <div class="news-column">
          <n-card :bordered="false" class="news-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">国内动态</span>
                <n-button text type="primary" @click="goToList('domestic')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <div class="card-content">
              <dynamic-card
                v-for="item in domesticNews.slice(0, 3)"
                :key="item.id"
                :id="item.id"
                :title="item.title"
                :summary="item.summary"
                :publish-date="item.publishDate"
                :source="item.source"
                :type="item.type"
                :view-count="item.viewCount"
                :tags="item.tags"
                :is-top="item.isTop"
                @click="goToDetail"
                class="card-item"
              />
            </div>
          </n-card>
        </div>

        <!-- 省内动态 -->
        <div class="news-column">
          <n-card :bordered="false" class="news-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">省内动态</span>
                <n-button text type="primary" @click="goToList('provincial')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <div class="card-content">
              <dynamic-card
                v-for="item in provincialNews.slice(0, 3)"
                :key="item.id"
                :id="item.id"
                :title="item.title"
                :summary="item.summary"
                :publish-date="item.publishDate"
                :source="item.source"
                :type="item.type"
                :view-count="item.viewCount"
                :tags="item.tags"
                :is-top="item.isTop"
                @click="goToDetail"
                class="card-item"
              />
            </div>
          </n-card>
        </div>

        <!-- 国外动态 -->
        <div class="news-column">
          <n-card :bordered="false" class="news-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">国外动态</span>
                <n-button text type="primary" @click="goToList('international')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <div class="card-content">
              <dynamic-card
                v-for="item in internationalNews.slice(0, 3)"
                :key="item.id"
                :id="item.id"
                :title="item.title"
                :summary="item.summary"
                :publish-date="item.publishDate"
                :source="item.source"
                :type="item.type"
                :view-count="item.viewCount"
                :tags="item.tags"
                :is-top="item.isTop"
                @click="goToDetail"
                class="card-item"
              />
            </div>
          </n-card>
        </div>
      </div>
    </div>

    <!-- 列表模式 -->
    <div v-else-if="displayMode === 'list'">
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
                返回动态信息
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

        <dynamic-list
          :data="getFilteredNews()"
          :total="getTotalCount()"
          :page-size="pageSize"
          @item-click="goToDetail"
          @page-change="handlePageChange"
          @page-size-change="handlePageSizeChange"
        />
      </n-card>
    </div>

    <!-- 详情弹窗 -->
    <dynamic-detail-modal
      v-model:show="showDetailModal"
      :dynamic-id="currentDynamicId"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import DynamicCard from './components/DynamicCard.vue'
import DynamicList from './components/DynamicList.vue'
import DynamicDetailModal from './components/DynamicDetailModal.vue'
import { mockDynamicApi } from './data/mockData.js'

// 使用项目自带的图标
const arrowRightIcon = 'mdi-arrow-right'

const searchKeyword = ref('')

// 数据状态
const domesticNews = ref([])
const provincialNews = ref([])
const internationalNews = ref([])

// 显示详情弹窗
const showDetailModal = ref(false)
const currentDynamicId = ref(null)

// 控制显示模式：'home' 为首页，'list' 为列表页
const displayMode = ref('home')
const currentListType = ref('') // 当前显示的类型

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)

// 加载数据
const loadData = async () => {
  try {
    // 加载国内动态
    const domesticResponse = await mockDynamicApi.getDynamicByType('domestic', { pageSize: 3 })
    domesticNews.value = domesticResponse.data.list

    // 加载省内动态
    const provincialResponse = await mockDynamicApi.getDynamicByType('provincial', { pageSize: 3 })
    provincialNews.value = provincialResponse.data.list

    // 加载国外动态
    const internationalResponse = await mockDynamicApi.getDynamicByType('international', { pageSize: 3 })
    internationalNews.value = internationalResponse.data.list
  } catch (error) {
    console.error('加载动态数据失败:', error)
  }
}

const goToDetail = (id) => {
  currentDynamicId.value = id
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
  if (currentListType.value === 'domestic') return '国内动态'
  if (currentListType.value === 'provincial') return '省内动态'
  if (currentListType.value === 'international') return '国外动态'
  if (currentListType.value === 'search') return '搜索结果'
  return '动态列表'
}

// 获取过滤后的动态列表
const getFilteredNews = () => {
  let news = []
  
  if (currentListType.value === 'domestic') {
    news = domesticNews.value
  } else if (currentListType.value === 'provincial') {
    news = provincialNews.value
  } else if (currentListType.value === 'international') {
    news = internationalNews.value
  } else if (currentListType.value === 'search') {
    // 搜索逻辑：合并所有动态并过滤
    const allNews = [...domesticNews.value, ...provincialNews.value, ...internationalNews.value]
    const keyword = searchKeyword.value.toLowerCase()
    news = allNews.filter(item => 
      item.title.toLowerCase().includes(keyword) ||
      item.summary.toLowerCase().includes(keyword) ||
      (item.tags && item.tags.some(tag => tag.toLowerCase().includes(keyword)))
    )
  }
  
  // 分页处理
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return news.slice(start, end)
}

// 获取总数
const getTotalCount = () => {
  if (currentListType.value === 'domestic') return domesticNews.value.length
  if (currentListType.value === 'provincial') return provincialNews.value.length
  if (currentListType.value === 'international') return internationalNews.value.length
  if (currentListType.value === 'search') {
    const allNews = [...domesticNews.value, ...provincialNews.value, ...internationalNews.value]
    const keyword = searchKeyword.value.toLowerCase()
    return allNews.filter(item => 
      item.title.toLowerCase().includes(keyword) ||
      item.summary.toLowerCase().includes(keyword) ||
      (item.tags && item.tags.some(tag => tag.toLowerCase().includes(keyword)))
    ).length
  }
  return 0
}

// 分页处理
const handlePageChange = (page) => {
  currentPage.value = page
}

const handlePageSizeChange = (newPageSize) => {
  pageSize.value = newPageSize
  currentPage.value = 1
}

// 组件挂载时加载数据
onMounted(() => {
  loadData()
})
</script>

<style scoped>
.news-container {
  padding: 12px;
}

.search-wrapper {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 12px;
}

.search-input :deep(.n-input__placeholder) {
  display: flex;
  align-items: center;
  justify-content: center;
}

.news-grid {
  display: flex;
  gap: 12px;
  position: relative;
}

.news-grid::after {
  content: '';
  position: absolute;
  left: 33.33%;
  top: 0;
  bottom: 0;
  border-left: 1px dashed #e5e5e5;
}

.news-grid::before {
  content: '';
  position: absolute;
  left: 66.66%;
  top: 0;
  bottom: 0;
  border-left: 1px dashed #e5e5e5;
}

.news-column {
  flex: 1;
}

.news-card {
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
}

.header-action:hover {
  opacity: 0.8;
}

.card-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.card-item {
  margin-bottom: 12px;
}

.card-item:last-child {
  margin-bottom: 0;
}

.mt-2 {
  margin-top: 8px;
}

.mt-4 {
  margin-top: 16px;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

:deep(.n-card-header) {
  padding: 12px 16px 8px;
}

:deep(.n-card__content) {
  padding: 0 16px 16px;
}
</style>
