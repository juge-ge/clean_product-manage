<template>
  <div class="capability-container">
    <!-- 首页模式 -->
    <div v-if="displayMode === 'home'">
      <!-- 搜索框 -->
      <div class="search-wrapper">
        <n-input-group style="width: 300px">
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索人员信息"
            clearable
            class="search-input"
          />
          <n-button type="primary" @click="handleSearch" style="padding: 0 24px">
            搜索
          </n-button>
        </n-input-group>
      </div>

      <!-- 双栏布局 -->
      <div class="capability-grid mt-4">
        <!-- 咨询人员 -->
        <div class="capability-column">
          <n-card :bordered="false" class="capability-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">咨询人员</span>
                <n-button text type="primary" @click="goToList('consultant')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <div class="card-content">
              <personnel-card
                v-for="item in consultantPersonnel.slice(0, 3)"
                :key="item.id"
                :personnel="item"
                @click="goToDetail"
                @contact="handleContact"
                @view-detail="goToDetail"
                class="card-item"
              />
            </div>
          </n-card>
        </div>

        <!-- 管理人员 -->
        <div class="capability-column">
          <n-card :bordered="false" class="capability-card">
            <template #header>
              <div class="card-header">
                <span class="header-title">管理人员</span>
                <n-button text type="primary" @click="goToList('manager')" class="header-action">
                  查看更多 <n-icon><i class="mdi" :class="arrowRightIcon" /></n-icon>
                </n-button>
              </div>
            </template>
            <div class="card-content">
              <personnel-card
                v-for="item in managerPersonnel.slice(0, 3)"
                :key="item.id"
                :personnel="item"
                @click="goToDetail"
                @contact="handleContact"
                @view-detail="goToDetail"
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
                返回能力建设
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

        <personnel-list
          :data="getFilteredPersonnel()"
          :total="getTotalCount()"
          :page-size="pageSize"
          @item-click="goToDetail"
          @contact="handleContact"
          @view-detail="goToDetail"
          @page-change="handlePageChange"
          @page-size-change="handlePageSizeChange"
        />
      </n-card>
    </div>

    <!-- 详情弹窗 -->
    <personnel-detail-modal
      v-model:show="showDetailModal"
      :personnel-id="currentPersonnelId"
      @contact="handleContact"
    />

    <!-- 联系确认弹窗 -->
    <n-modal v-model:show="showContactModal" preset="dialog" title="联系确认">
      <div class="contact-confirm">
        <p>确定要联系 <strong>{{ currentPersonnel?.name }}</strong> 吗？</p>
        <div class="contact-info" v-if="currentPersonnel">
          <div class="contact-item" v-if="currentPersonnel.phone">
            <n-icon size="16" color="#666">
              <i class="mdi mdi-phone" />
            </n-icon>
            <span>电话：{{ currentPersonnel.phone }}</span>
          </div>
          <div class="contact-item" v-if="currentPersonnel.email">
            <n-icon size="16" color="#666">
              <i class="mdi mdi-email" />
            </n-icon>
            <span>邮箱：{{ currentPersonnel.email }}</span>
          </div>
        </div>
      </div>
      <template #action>
        <n-space>
          <n-button @click="showContactModal = false">取消</n-button>
          <n-button type="primary" @click="confirmContact">确定联系</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import PersonnelCard from './components/PersonnelCard.vue'
import PersonnelList from './components/PersonnelList.vue'
import PersonnelDetailModal from './components/PersonnelDetailModal.vue'
import { mockPersonnelApi } from './data/mockData.js'

// 使用项目自带的图标
const arrowRightIcon = 'mdi-arrow-right'

const searchKeyword = ref('')

// 数据状态
const consultantPersonnel = ref([])
const managerPersonnel = ref([])

// 显示详情弹窗
const showDetailModal = ref(false)
const currentPersonnelId = ref(null)

// 联系确认弹窗
const showContactModal = ref(false)
const currentPersonnel = ref(null)

// 控制显示模式：'home' 为首页，'list' 为列表页
const displayMode = ref('home')
const currentListType = ref('') // 当前显示的类型

// 分页相关
const currentPage = ref(1)
const pageSize = ref(10)

// 加载数据
const loadData = async () => {
  try {
    // 加载咨询人员
    const consultantResponse = await mockPersonnelApi.getPersonnelByType('consultant', { pageSize: 3 })
    consultantPersonnel.value = consultantResponse.data.list

    // 加载管理人员
    const managerResponse = await mockPersonnelApi.getPersonnelByType('manager', { pageSize: 3 })
    managerPersonnel.value = managerResponse.data.list
  } catch (error) {
    console.error('加载人员数据失败:', error)
  }
}

const goToDetail = (personnel) => {
  currentPersonnelId.value = personnel.id
  showDetailModal.value = true
}

const handleContact = (personnel) => {
  currentPersonnel.value = personnel
  showContactModal.value = true
}

const confirmContact = () => {
  // 实现联系功能
  console.log('联系人员:', currentPersonnel.value?.name)
  showContactModal.value = false
  // 这里可以集成电话、邮件等功能
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
  if (currentListType.value === 'consultant') return '咨询人员'
  if (currentListType.value === 'manager') return '管理人员'
  if (currentListType.value === 'search') return '搜索结果'
  return '人员列表'
}

// 获取过滤后的人员列表
const getFilteredPersonnel = () => {
  let personnel = []
  
  if (currentListType.value === 'consultant') {
    personnel = consultantPersonnel.value
  } else if (currentListType.value === 'manager') {
    personnel = managerPersonnel.value
  } else if (currentListType.value === 'search') {
    // 搜索逻辑：合并所有人员并过滤
    const allPersonnel = [...consultantPersonnel.value, ...managerPersonnel.value]
    const keyword = searchKeyword.value.toLowerCase()
    personnel = allPersonnel.filter(item => 
      item.name.toLowerCase().includes(keyword) ||
      item.organization.toLowerCase().includes(keyword) ||
      item.specialties.some(specialty => specialty.toLowerCase().includes(keyword))
    )
  }
  
  // 分页处理
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return personnel.slice(start, end)
}

// 获取总数
const getTotalCount = () => {
  if (currentListType.value === 'consultant') return consultantPersonnel.value.length
  if (currentListType.value === 'manager') return managerPersonnel.value.length
  if (currentListType.value === 'search') {
    const allPersonnel = [...consultantPersonnel.value, ...managerPersonnel.value]
    const keyword = searchKeyword.value.toLowerCase()
    return allPersonnel.filter(item => 
      item.name.toLowerCase().includes(keyword) ||
      item.organization.toLowerCase().includes(keyword) ||
      item.specialties.some(specialty => specialty.toLowerCase().includes(keyword))
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
.capability-container {
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

.capability-grid {
  display: flex;
  gap: 12px;
  position: relative;
}

.capability-grid::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  border-left: 1px dashed #e5e5e5;
  transform: translateX(-50%);
}

.capability-column {
  flex: 1;
}

.capability-card {
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

.contact-confirm {
  padding: 16px 0;
}

.contact-info {
  margin-top: 16px;
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
  font-size: 14px;
  color: #666;
}

.contact-item:last-child {
  margin-bottom: 0;
}

:deep(.n-card-header) {
  padding: 12px 16px 8px;
}

:deep(.n-card__content) {
  padding: 0 16px 16px;
}
</style>
