<template>
  <div class="enterprise-basic-info">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <h1 class="page-title">PCB</h1>
        <div class="tab-container">
          <div class="tab active">企业列表</div>
        </div>
      </div>
      <div class="header-right">
        <n-input
          v-model:value="searchKeyword"
          placeholder="搜索"
          class="search-input"
          @input="handleSearch"
        >
          <template #suffix>
            <n-icon>
              <svg viewBox="0 0 24 24" width="16" height="16">
                <path fill="currentColor" d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
              </svg>
            </n-icon>
          </template>
        </n-input>
      </div>
    </div>

    <!-- 企业卡片网格 -->
    <div class="enterprise-grid">
      <!-- 创建企业卡片 -->
      <div class="enterprise-card create-card" @click="showCreateModal = true">
        <div class="create-icon">+</div>
        <div class="create-text">点击创建企业</div>
      </div>

      <!-- 企业信息卡片 -->
      <div
        v-for="enterprise in paginatedEnterprises"
        :key="enterprise.id"
        class="enterprise-card"
      >
        <div class="enterprise-name">{{ enterprise.name }}</div>
        <div class="enterprise-address">{{ enterprise.address }}</div>
        <div class="enterprise-actions">
          <n-button
            type="error"
            size="small"
            @click="handleDelete(enterprise.id)"
          >
            删除
          </n-button>
          <n-button
            type="info"
            size="small"
            @click="showDetailModal(enterprise.id)"
          >
            详情
          </n-button>
          <n-button
            type="primary"
            size="small"
            @click="showEditModal(enterprise.id)"
          >
            编辑
          </n-button>
        </div>
      </div>
    </div>

    <!-- 分页 -->
    <div class="pagination-container">
      <n-pagination
        v-model:page="currentPage"
        :page-size="pageSize"
        :item-count="filteredEnterprises.length"
        show-size-picker
        :page-sizes="[8, 16, 24]"
        @update:page="handlePageChange"
        @update:page-size="handlePageSizeChange"
      />
    </div>

    <!-- 详情模态框 -->
    <EnterpriseDetailModal
      v-model:show="showDetail"
      :enterprise-id="selectedEnterpriseId"
    />

    <!-- 表单模态框 -->
    <EnterpriseFormModal
      v-model:show="showCreateModal"
      mode="create"
      @success="handleFormSuccess"
    />

    <EnterpriseFormModal
      v-model:show="showEditModal"
      mode="edit"
      :enterprise-id="selectedEnterpriseId"
      @success="handleFormSuccess"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { NInput, NIcon, NButton, NPagination } from 'naive-ui'
import EnterpriseDetailModal from './components/EnterpriseDetailModal.vue'
import EnterpriseFormModal from './components/EnterpriseFormModal.vue'
import { mockEnterprises } from './data/mockData.js'

// 响应式数据
const searchKeyword = ref('')
const currentPage = ref(1)
const pageSize = ref(8)
const enterprises = ref([])

// 模态框状态
const showDetail = ref(false)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const selectedEnterpriseId = ref(null)

// 计算属性
const filteredEnterprises = computed(() => {
  if (!searchKeyword.value) {
    return enterprises.value
  }
  return enterprises.value.filter(enterprise =>
    enterprise.name.toLowerCase().includes(searchKeyword.value.toLowerCase())
  )
})

const paginatedEnterprises = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredEnterprises.value.slice(start, end)
})

// 方法
const handleSearch = () => {
  currentPage.value = 1 // 搜索时重置到第一页
}

const handlePageChange = (page) => {
  currentPage.value = page
}

const handlePageSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
}

const showDetailModal = (id) => {
  selectedEnterpriseId.value = id
  showDetail.value = true
}

const showEditModal = (id) => {
  selectedEnterpriseId.value = id
  showEditModal.value = true
}

const handleDelete = (id) => {
  // 这里可以添加确认对话框
  enterprises.value = enterprises.value.filter(enterprise => enterprise.id !== id)
}

const handleFormSuccess = () => {
  // 表单提交成功后的处理
  showCreateModal.value = false
  showEditModal.value = false
}

// 初始化数据
onMounted(() => {
  enterprises.value = [...mockEnterprises]
})
</script>

<style scoped>
.enterprise-basic-info {
  padding: 20px;
  background: #f5f5f5;
  min-height: calc(100vh - 60px);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.page-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  color: #333;
}

.tab-container {
  display: flex;
}

.tab {
  padding: 8px 16px;
  background: #f0f0f0;
  border-radius: 4px;
  font-size: 14px;
  color: #666;
  cursor: pointer;
}

.tab.active {
  background: #1890ff;
  color: white;
}

.search-input {
  width: 200px;
}

.enterprise-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.enterprise-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
  cursor: pointer;
}

.enterprise-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.create-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  border: 2px dashed #d9d9d9;
  background: #fafafa;
}

.create-card:hover {
  border-color: #1890ff;
  background: #f0f8ff;
}

.create-icon {
  font-size: 32px;
  color: #999;
  margin-bottom: 8px;
}

.create-text {
  color: #666;
  font-size: 14px;
}

.enterprise-name {
  font-weight: bold;
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
  line-height: 1.4;
}

.enterprise-address {
  color: #666;
  font-size: 14px;
  line-height: 1.4;
  margin-bottom: 16px;
  flex: 1;
}

.enterprise-actions {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}

.pagination-container {
  display: flex;
  justify-content: center;
  background: white;
  padding: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .enterprise-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}

@media (max-width: 768px) {
  .enterprise-grid {
    grid-template-columns: 1fr;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .header-left {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .search-input {
    width: 100%;
  }
}
</style>
