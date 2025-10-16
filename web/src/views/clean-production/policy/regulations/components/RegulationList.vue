<template>
  <div class="regulation-list">
    <div class="list-header">
      <div class="header-left">
        <n-space>
          <n-input
            v-model:value="searchKeyword"
            placeholder="请输入关键词搜索"
            style="width: 200px"
            clearable
            @keyup.enter="handleSearch"
            @clear="handleClear"
          />
          <n-button type="primary" @click="handleSearch">
            <template #icon>
              <n-icon><i class="mdi mdi-magnify" /></n-icon>
            </template>
            搜索
          </n-button>
        </n-space>
      </div>
      <div class="header-right">
        <n-space>
          <span class="total-count">共{{ total }}条</span>
        </n-space>
      </div>
    </div>
    
    <n-list hoverable clickable>
      <n-list-item 
        v-for="(item, index) in data" 
        :key="item.id || index"
        @click="handleItemClick(item)"
        class="list-item"
      >
        <div class="list-item-content">
          <div class="title-section">
            <a href="javascript:;" class="item-title" @click.stop="handleItemClick(item)">
              {{ item.title }}
            </a>
            <div class="title-tags">
              <n-tag 
                :type="getLevelTagType(item.level)" 
                size="small" 
                class="level-tag"
              >
                {{ getLevelLabel(item.level) }}
              </n-tag>
              <template v-if="item.isImportant">
                <n-tag type="error" size="small" class="important-tag">重要</n-tag>
              </template>
            </div>
          </div>
          <div class="summary-section">
            <p class="item-summary">{{ item.summary }}</p>
          </div>
          <div class="meta-section">
            <div class="meta-left">
              <span class="source">{{ item.source }}</span>
              <span class="publish-date">发布：{{ item.publishDate }}</span>
              <span v-if="item.effectiveDate" class="effective-date">生效：{{ item.effectiveDate }}</span>
              <template v-if="item.province">
                <span class="province">地区：{{ item.province }}</span>
              </template>
            </div>
            <div class="meta-right">
              <div class="stats">
                <div class="stat-item">
                  <n-icon size="14" color="#999">
                    <i class="mdi mdi-eye" />
                  </n-icon>
                  <span class="view-count">{{ item.viewCount }}</span>
                </div>
                <div class="stat-item">
                  <n-icon size="14" color="#999">
                    <i class="mdi mdi-download" />
                  </n-icon>
                  <span class="download-count">{{ item.downloadCount }}</span>
                </div>
              </div>
            </div>
          </div>
          <div v-if="item.tags && item.tags.length" class="tags-section">
            <n-tag 
              v-for="tag in item.tags.slice(0, 5)" 
              :key="tag"
              size="small"
              type="info"
              class="tag-item"
            >
              {{ tag }}
            </n-tag>
          </div>
        </div>
      </n-list-item>
    </n-list>
    
    <div class="list-footer" v-if="showPagination">
      <n-pagination
        v-model:page="currentPage"
        :page-size="pageSize"
        :item-count="total"
        show-quick-jumper
        show-size-picker
        :page-sizes="[10, 20, 30, 50]"
        @update:page="handlePageChange"
        @update:page-size="handlePageSizeChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { mockRegulationApi } from '../data/mockData.js'

const props = defineProps({
  category: {
    type: String,
    required: true
  },
  searchKeyword: {
    type: String,
    default: ''
  },
  showPagination: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['search', 'item-click'])

const data = ref([])
const total = ref(0)
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(10)
const searchKeyword = ref(props.searchKeyword)

const getLevelTagType = (level) => {
  const typeMap = {
    national: 'error',
    provincial: 'warning'
  }
  return typeMap[level] || 'default'
}

const getLevelLabel = (level) => {
  const labelMap = {
    national: '国家级',
    provincial: '省级'
  }
  return labelMap[level] || '未知'
}

const loadData = async () => {
  loading.value = true
  try {
    const response = await mockRegulationApi.getRegulationByCategory(props.category, {
      page: currentPage.value,
      pageSize: pageSize.value,
      search: searchKeyword.value
    })
    data.value = response.data.list
    total.value = response.data.total
  } catch (error) {
    console.error('加载法规数据失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  loadData()
  emit('search', searchKeyword.value)
}

const handleClear = () => {
  searchKeyword.value = ''
  handleSearch()
}

const handleItemClick = (item) => {
  emit('item-click', item)
}

const handlePageChange = (page) => {
  currentPage.value = page
  loadData()
}

const handlePageSizeChange = (newPageSize) => {
  pageSize.value = newPageSize
  currentPage.value = 1
  loadData()
}

// 监听category变化
watch(() => props.category, () => {
  currentPage.value = 1
  searchKeyword.value = ''
  loadData()
})

// 监听searchKeyword变化
watch(() => props.searchKeyword, (newValue) => {
  searchKeyword.value = newValue
  handleSearch()
})

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.regulation-list {
  width: 100%;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding: 0 4px;
}

.total-count {
  font-size: 14px;
  color: #666;
  font-weight: 500;
}

.list-item {
  border-bottom: 1px dashed #e5e5e5;
  transition: all 0.3s ease;
}

.list-item:hover {
  background-color: #f8f9fa;
}

.list-item:last-child {
  border-bottom: none;
}

.list-item-content {
  width: 100%;
  padding: 12px 0;
}

.title-section {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  gap: 12px;
}

.item-title {
  font-size: 16px;
  font-weight: 500;
  color: #333;
  text-decoration: none;
  flex: 1;
  line-height: 1.4;
}

.item-title:hover {
  color: var(--primary-color);
}

.title-tags {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.level-tag {
  font-size: 11px;
  padding: 2px 6px;
}

.important-tag {
  font-size: 11px;
  padding: 2px 6px;
}

.summary-section {
  margin-bottom: 8px;
}

.item-summary {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.meta-left {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 12px;
  color: #999;
  flex-wrap: wrap;
}

.source {
  font-weight: 500;
  color: #666;
}

.publish-date,
.effective-date,
.province {
  color: #999;
}

.meta-right {
  display: flex;
  align-items: center;
}

.stats {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #999;
}

.view-count,
.download-count {
  font-size: 12px;
}

.tags-section {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.tag-item {
  font-size: 11px;
  padding: 2px 6px;
}

.list-footer {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e5e5;
  display: flex;
  justify-content: center;
}

:deep(.n-list-item) {
  padding: 0 16px;
}

:deep(.n-list-item:hover) {
  background-color: #f8f9fa;
}
</style>
