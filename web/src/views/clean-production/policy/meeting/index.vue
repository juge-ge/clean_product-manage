<template>
  <div class="meeting-container">
    <!-- 首页模式 -->
    <div v-if="displayMode === 'home'">
      <!-- 搜索框 -->
      <div class="search-wrapper">
        <n-input-group style="width: 300px">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索会议和视频"
            clearable
            class="search-input"
          />
          <n-button type="primary" @click="handleSearch" style="padding: 0 24px">
            搜索
          </n-button>
        </n-input-group>
      </div>

      <!-- 双栏布局 -->
      <div class="meeting-grid mt-4">
        <!-- 会议信息 -->
        <div class="meeting-column">
          <n-card :bordered="false" class="meeting-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">清洁生产会议</span>
                <n-button text type="primary" @click="goToList('meetings')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <div class="card-content">
              <meeting-card
                v-for="item in meetings.slice(0, 3)"
                :key="item.id"
                :meeting="item"
                @click="goToDetail"
                @view-detail="goToDetail"
                @view-agenda="handleViewAgenda"
                @download="handleDownload"
                class="card-item"
              />
            </div>
          </n-card>
        </div>

        <!-- 宣传视频 -->
        <div class="meeting-column">
          <n-card :bordered="false" class="meeting-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">清洁生产宣传</span>
                <n-button text type="primary" @click="goToList('videos')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <div class="card-content">
              <div class="video-list">
                <div 
                  v-for="item in videos.slice(0, 3)" 
                  :key="item.id"
                  class="video-item"
                  @click="goToVideoDetail(item)"
                >
                  <div class="video-thumbnail">
                    <img :src="item.thumbnail" :alt="item.title" />
                    <div class="video-overlay">
                      <n-icon size="24" color="white">
                        <i class="mdi mdi-play" />
                      </n-icon>
                    </div>
                    <div class="video-duration">{{ formatDuration(item.duration) }}</div>
                  </div>
                  <div class="video-info">
                    <h4 class="video-title">{{ item.title }}</h4>
                    <p class="video-description">{{ item.description }}</p>
                    <div class="video-meta">
                      <span class="view-count">{{ item.viewCount }} 次观看</span>
                      <span class="publish-date">{{ item.publishDate }}</span>
                    </div>
                    <div class="video-tags" v-if="item.tags && item.tags.length">
                      <n-tag 
                        v-for="tag in item.tags.slice(0, 2)" 
                        :key="tag"
                        size="small"
                        type="info"
                        class="tag-item"
                      >
                        {{ tag }}
                      </n-tag>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </n-card>
        </div>
      </div>
    </div>

    <!-- 列表模式（仅保留视频列表，移除会议筛选相关内容） -->
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
                返回会议与宣传
              </n-button>
            </n-space>
            <n-space>
              <!-- 移除NSelect筛选器 -->
              <n-input
                v-model:value="searchKeyword"
                placeholder="请输入关键词搜索"
                style="width: 200px"
              />
              <n-button type="primary" @click="handleSearch">搜索</n-button>
            </n-space>
          </n-space>
        </template>

        <!-- 视频列表 -->
        <div v-if="currentListType === 'videos'" class="video-grid">
          <div 
            v-for="item in getFilteredVideos()" 
            :key="item.id"
            class="video-card"
            @click="goToVideoDetail(item)"
          >
            <div class="video-thumbnail">
              <img :src="item.thumbnail" :alt="item.title" />
              <div class="video-overlay">
                <n-icon size="32" color="white">
                  <i class="mdi mdi-play" />
                </n-icon>
              </div>
              <div class="video-duration">{{ formatDuration(item.duration) }}</div>
              <div class="video-category" v-if="item.category">
                <n-tag size="small" type="info">{{ item.category }}</n-tag>
              </div>
            </div>
            <div class="video-info">
              <h4 class="video-title">{{ item.title }}</h4>
              <p class="video-description">{{ item.description }}</p>
              <div class="video-meta">
                <div class="meta-item">
                  <n-icon size="14" color="#999">
                    <i class="mdi mdi-eye" />
                  </n-icon>
                  <span>{{ item.viewCount }} 次观看</span>
                </div>
                <div class="meta-item">
                  <n-icon size="14" color="#999">
                    <i class="mdi mdi-calendar" />
                  </n-icon>
                  <span>{{ item.publishDate }}</span>
                </div>
              </div>
              <div class="video-tags" v-if="item.tags && item.tags.length">
                <n-tag 
                  v-for="tag in item.tags.slice(0, 3)" 
                  :key="tag"
                  size="small"
                  type="info"
                  class="tag-item"
                >
                  {{ tag }}
                </n-tag>
              </div>
            </div>
          </div>
        </div>

        <!-- 会议列表（简化版，无筛选功能） -->
        <meeting-list
          v-if="currentListType === 'meetings'"
          :data="getFilteredMeetings()"
          :total="getTotalCount()"
          :page-size="pageSize"
          @item-click="goToDetail"
          @page-change="handlePageChange"
          @page-size-change="handlePageSizeChange"
        />
      </n-card>
    </div>

    <!-- 会议详情弹窗 -->
    <meeting-detail-modal
      v-model:show="showMeetingDetailModal"
      :meeting-id="currentMeetingId"
    />

    <!-- 视频播放弹窗 -->
    <n-modal
      v-model:show="showVideoModal"
      class="video-modal"
      preset="card"
      style="max-width: 1000px"
      :title="currentVideo?.title"
      size="huge"
    >
      <video-player
        v-if="currentVideo"
        :video-url="currentVideo.videoUrl"
        :title="currentVideo.title"
        :description="currentVideo.description"
        :thumbnail="currentVideo.thumbnail"
        :duration="currentVideo.duration"
        :category="currentVideo.category"
        :tags="currentVideo.tags"
        :view-count="currentVideo.viewCount"
        :publish-date="currentVideo.publishDate"
        :is-recommended="currentVideo.isRecommended"
        @view-count-update="handleVideoViewCountUpdate"
      />
    </n-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MeetingCard from './components/MeetingCard.vue'
import MeetingList from './components/MeetingList.vue'
import MeetingDetailModal from './components/MeetingDetailModal.vue'
import VideoPlayer from './components/VideoPlayer.vue'
import { mockMeetingApi } from './data/mockData.js'
// 仅保留必要组件，移除NSelect相关导入
import { NInputGroup, NInput, NButton, NIcon, NCard, NSpace, NTag, NModal } from 'naive-ui'

// 使用项目自带的图标
const arrowRightIcon = 'mdi-arrow-right'

const searchKeyword = ref('')
// 移除filterType相关变量

// 数据状态
const meetings = ref([])
const videos = ref([])

// 显示详情弹窗
const showMeetingDetailModal = ref(false)
const currentMeetingId = ref(null)

// 视频播放弹窗
const showVideoModal = ref(false)
const currentVideo = ref(null)

// 控制显示模式：'home' 为首页，'list' 为列表页
const displayMode = ref('home')
const currentListType = ref('') // 当前显示的类型

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)

// 加载数据
const loadData = async () => {
  try {
    // 加载会议数据
    const meetingResponse = await mockMeetingApi.getMeetingList({ pageSize: 3 })
    meetings.value = meetingResponse.data.list

    // 加载视频数据
    const videoResponse = await mockMeetingApi.getVideoList({ pageSize: 3 })
    videos.value = videoResponse.data.list
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const goToDetail = (meeting) => {
  currentMeetingId.value = meeting.id
  showMeetingDetailModal.value = true
}

const goToVideoDetail = (video) => {
  currentVideo.value = video
  showVideoModal.value = true
}

const handleViewAgenda = (meeting) => {
  console.log('查看议程:', meeting.title)
}

const handleDownload = (meeting) => {
  console.log('下载资料:', meeting.title)
}

const handleVideoViewCountUpdate = () => {
  if (currentVideo.value) {
    mockMeetingApi.updateVideoViewCount(currentVideo.value.id)
    currentVideo.value.viewCount += 1
  }
}

// 切换到列表显示模式
const goToList = (type) => {
  currentListType.value = type
  displayMode.value = 'list'
  currentPage.value = 1 // 重置分页
  // 移除filterType重置
}

// 搜索处理
const handleSearch = () => {
  if (searchKeyword.value.trim()) {
    currentListType.value = 'search'
    displayMode.value = 'list'
    currentPage.value = 1
  }
}

// 移除过滤处理函数handleFilterChange

// 返回首页
const goHome = () => {
  displayMode.value = 'home'
  currentListType.value = ''
  searchKeyword.value = ''
  // 移除filterType重置
  currentPage.value = 1
}

// 获取列表标题
const getListTitle = () => {
  if (currentListType.value === 'meetings') return '清洁生产会议'
  if (currentListType.value === 'videos') return '清洁生产宣传'
  if (currentListType.value === 'search') return '搜索结果'
  return '会议与宣传'
}

// 获取过滤后的会议列表（移除类型过滤）
const getFilteredMeetings = () => {
  let data = meetings.value
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    data = data.filter(item => 
      item.title.toLowerCase().includes(keyword) ||
      item.summary.toLowerCase().includes(keyword) ||
      item.organizer.toLowerCase().includes(keyword)
    )
  }
  
  // 移除类型过滤逻辑
  
  // 分页处理
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return data.slice(start, end)
}

// 获取过滤后的视频列表
const getFilteredVideos = () => {
  let data = videos.value
  
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    data = data.filter(item => 
      item.title.toLowerCase().includes(keyword) ||
      item.description.toLowerCase().includes(keyword) ||
      item.tags.some(tag => tag.toLowerCase().includes(keyword))
    )
  }
  
  // 分页处理
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return data.slice(start, end)
}

// 获取总数（移除类型过滤）
const getTotalCount = () => {
  if (currentListType.value === 'meetings') {
    let data = meetings.value
    if (searchKeyword.value) {
      const keyword = searchKeyword.value.toLowerCase()
      data = data.filter(item => 
        item.title.toLowerCase().includes(keyword) ||
        item.summary.toLowerCase().includes(keyword) ||
        item.organizer.toLowerCase().includes(keyword)
      )
    }
    return data.length
  } else if (currentListType.value === 'videos') {
    let data = videos.value
    if (searchKeyword.value) {
      const keyword = searchKeyword.value.toLowerCase()
      data = data.filter(item => 
        item.title.toLowerCase().includes(keyword) ||
        item.description.toLowerCase().includes(keyword) ||
        item.tags.some(tag => tag.toLowerCase().includes(keyword))
      )
    }
    return data.length
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

const formatDuration = (seconds) => {
  if (!seconds || seconds === 0) return '00:00'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}

// 组件挂载时加载数据
onMounted(() => {
  loadData()
})
</script>

<style scoped>
/* 样式部分保持不变 */
.meeting-container {
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

.meeting-grid {
  display: flex;
  gap: 12px;
  position: relative;
}

.meeting-grid::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  border-left: 1px dashed #e5e5e5;
  transform: translateX(-50%);
}

.meeting-column {
  flex: 1;
}

.meeting-card {
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
  gap: 16px;
}

.card-item {
  margin-bottom: 16px;
}

.card-item:last-child {
  margin-bottom: 0;
}

.video-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.video-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.video-item:hover {
  border-color: var(--primary-color);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.video-thumbnail {
  position: relative;
  width: 120px;
  height: 80px;
  flex-shrink: 0;
  border-radius: 6px;
  overflow: hidden;
}

.video-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.3s ease;
}

.video-item:hover .video-overlay {
  background-color: rgba(0, 0, 0, 0.5);
}

.video-duration {
  position: absolute;
  bottom: 4px;
  right: 4px;
  background-color: rgba(0, 0, 0, 0.7);
  color: white;
  font-size: 11px;
  padding: 2px 4px;
  border-radius: 3px;
}

.video-info {
  flex: 1;
  min-width: 0;
}

.video-title {
  font-size: 14px;
  font-weight: 500;
  color: #333;
  margin: 0 0 4px 0;
  line-height: 1.3;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.video-description {
  font-size: 12px;
  color: #666;
  line-height: 1.4;
  margin: 0 0 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-meta {
  display: flex;
  gap: 12px;
  margin-bottom: 6px;
  font-size: 11px;
  color: #999;
}

.video-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-item {
  font-size: 10px;
  padding: 1px 4px;
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.video-card {
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s ease;
}

.video-card:hover {
  border-color: var(--primary-color);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.video-card .video-thumbnail {
  width: 100%;
  height: 180px;
  position: relative;
}

.video-category {
  position: absolute;
  top: 8px;
  left: 8px;
}

.video-card .video-info {
  padding: 12px;
}

.video-card .video-title {
  font-size: 16px;
  margin-bottom: 8px;
  white-space: normal;
  -webkit-line-clamp: 2;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-card .video-description {
  font-size: 13px;
  margin-bottom: 12px;
  -webkit-line-clamp: 3;
}

.video-card .video-meta {
  margin-bottom: 8px;
}

.video-card .meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #999;
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