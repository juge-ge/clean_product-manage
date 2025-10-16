<template>
  <div class="regulations-container">
    <n-card :bordered="false" class="regulations-card">
      <template #header>
        <div class="card-header">
          <span class="header-title">清洁生产法规政策</span>
          <n-space>
            <n-input
              v-model:value="globalSearchKeyword"
              placeholder="全局搜索法规政策"
              style="width: 200px"
              clearable
              @keyup.enter="handleGlobalSearch"
              @clear="handleGlobalSearchClear"
            />
            <n-button type="primary" @click="handleGlobalSearch">
              <template #icon>
                <n-icon><i class="mdi mdi-magnify" /></n-icon>
              </template>
              搜索
            </n-button>
          </n-space>
        </div>
      </template>

      <regulation-tabs
        v-model="activeTab"
        :search-keyword="globalSearchKeyword"
        @search="handleSearch"
        @item-click="goToDetail"
      />

      <!-- 详情弹窗 -->
      <regulation-detail-modal
        v-model:show="showDetailModal"
        :regulation-id="currentRegulationId"
      />
    </n-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import RegulationTabs from './components/RegulationTabs.vue'
import RegulationDetailModal from './components/RegulationDetailModal.vue'

const activeTab = ref('national')
const globalSearchKeyword = ref('')

// 显示详情弹窗
const showDetailModal = ref(false)
const currentRegulationId = ref(null)

const goToDetail = (item) => {
  currentRegulationId.value = item.id
  showDetailModal.value = true
}

const handleSearch = (keyword) => {
  globalSearchKeyword.value = keyword
}

const handleGlobalSearch = () => {
  // 全局搜索逻辑
  console.log('全局搜索:', globalSearchKeyword.value)
}

const handleGlobalSearchClear = () => {
  globalSearchKeyword.value = ''
  handleGlobalSearch()
}
</script>

<style scoped>
.regulations-container {
  padding: 12px;
}

.regulations-card {
  min-height: 600px;
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
  font-size: 20px;
  font-weight: 600;
  color: #333;
}

:deep(.n-card-header) {
  padding: 16px 20px 12px;
}

:deep(.n-card__content) {
  padding: 0 20px 20px;
}
</style>
