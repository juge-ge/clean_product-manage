<template>
  <CommonPage title="钢铁行业清洁生产审核">
    <div class="steel-enterprise-list">

    <!-- 搜索和操作栏 -->
    <div class="search-bar mb-4">
      <n-space>
        <n-input 
          v-model:value="queryParams.name" 
          placeholder="请输入企业名称/地市/区县"
          clearable
          style="width: 300px"
        />
        <n-button type="primary" @click="handleCreate">
          <template #icon>
            <TheIcon icon="carbon:add" />
          </template>
          创建企业
        </n-button>
      </n-space>
    </div>

    <!-- 企业列表 -->
    <n-spin :show="loading">
      <div class="enterprise-grid">
        <div
          v-for="enterprise in enterpriseList"
          :key="enterprise.id"
          class="enterprise-card"
        >
          <EnterpriseCard
            :enterprise="enterprise"
            @view="handleView"
            @edit="handleEdit"
            @delete="handleDelete"
          />
        </div>
        <div v-if="!loading && enterpriseList.length === 0" class="empty-state">
          <n-empty description="暂无企业数据">
            <template #extra>
              <n-button type="primary" @click="handleCreate">
                创建企业
              </n-button>
            </template>
          </n-empty>
        </div>
      </div>
    </n-spin>

    <!-- 分页 -->
    <div class="pagination" v-if="total > 0">
      <n-pagination
        v-model:page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :page-count="Math.ceil(total / pagination.pageSize)"
        :page-sizes="[10, 20, 50, 100]"
        show-size-picker
        show-quick-jumper
        @update:page="handlePageChange"
        @update:page-size="handlePageSizeChange"
      />
    </div>

    <!-- 企业表单弹窗 -->
    <n-modal v-model:show="formModalVisible" preset="card" title="企业信息" size="huge">
      <EnterpriseForm
        :enterprise="currentEnterprise"
        @submit="handleSubmit"
        @cancel="handleCancel"
      />
    </n-modal>
    </div>
  </CommonPage>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { NButton, NInput, NSelect, NSpace, NPagination, NModal, NIcon, NSpin, NEmpty, useMessage } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import CommonPage from '@/components/page/CommonPage.vue'
import EnterpriseCard from './components/EnterpriseCard.vue'
import EnterpriseForm from './components/EnterpriseForm.vue'
import { mockApi } from '@/mock/steel'
import api from '@/api'

const router = useRouter()
const message = useMessage()

// 响应式数据
const loading = ref(false)
const enterpriseList = ref([])
const total = ref(0)
const formModalVisible = ref(false)
const currentEnterprise = ref(null)

// 查询参数
const queryParams = reactive({
  name: '',
  city: null,
  scale: null,
  auditStatus: null
})

// 分页参数
const pagination = reactive({
  page: 1,
  pageSize: 20
})

// 选项数据
const cityOptions = [
  { label: '北京市', value: '北京市' },
  { label: '上海市', value: '上海市' },
  { label: '广州市', value: '广州市' },
  { label: '深圳市', value: '深圳市' },
  { label: '杭州市', value: '杭州市' },
  { label: '南京市', value: '南京市' },
  { label: '武汉市', value: '武汉市' },
  { label: '成都市', value: '成都市' }
]

const scaleOptions = [
  { label: '大型', value: '大型' },
  { label: '中型', value: '中型' },
  { label: '小型', value: '小型' }
]

const auditStatusOptions = [
  { label: '未开始', value: 'not_started' },
  { label: '进行中', value: 'in_progress' },
  { label: '已完成', value: 'completed' }
]

// 方法
const loadEnterpriseList = async () => {
  loading.value = true
  try {
    const params = {
      search: queryParams.name || ''
    }
    
    // 使用Mock数据，实际项目中应该调用API
    const response = await mockApi.getEnterpriseList(params)
    console.log('企业列表响应:', response)
    enterpriseList.value = response.data || []
    total.value = response.data?.length || 0
    console.log('企业列表数据:', enterpriseList.value)
    
    // 实际API调用示例（注释掉，等后端实现后启用）
    // const response = await api.steel.getEnterpriseList(params)
    // enterpriseList.value = response.data || []
    // total.value = response.total || 0
  } catch (error) {
    console.error('加载企业列表失败:', error)
    message.error('加载企业列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadEnterpriseList()
}

const handleReset = () => {
  Object.assign(queryParams, {
    name: '',
    city: null,
    scale: null,
    auditStatus: null
  })
  pagination.page = 1
  loadEnterpriseList()
}

const handlePageChange = (page) => {
  pagination.page = page
  loadEnterpriseList()
}

const handlePageSizeChange = (pageSize) => {
  pagination.pageSize = pageSize
  pagination.page = 1
  loadEnterpriseList()
}

const handleCreate = () => {
  currentEnterprise.value = null
  formModalVisible.value = true
}

const handleView = (enterprise) => {
  console.log('查看企业:', enterprise)
  if (enterprise && enterprise.id) {
    router.push(`/cloud-audit/steel/${enterprise.id}`)
  } else {
    message.error('企业信息不完整')
  }
}

const handleEdit = (enterprise) => {
  currentEnterprise.value = { ...enterprise }
  formModalVisible.value = true
}

const handleDelete = async (enterprise) => {
  try {
    await mockApi.deleteEnterprise(enterprise.id)
    message.success('删除成功')
    loadEnterpriseList()
  } catch (error) {
    console.error('删除失败:', error)
    message.error('删除失败')
  }
}

const handleSubmit = async (formData) => {
  try {
    if (currentEnterprise.value) {
      // 编辑
      await mockApi.updateEnterprise(currentEnterprise.value.id, formData)
      message.success('更新成功')
    } else {
      // 新增
      await mockApi.createEnterprise(formData)
      message.success('创建成功')
    }
    formModalVisible.value = false
    loadEnterpriseList()
  } catch (error) {
    console.error('提交失败:', error)
    message.error('提交失败')
  }
}

const handleCancel = () => {
  formModalVisible.value = false
  currentEnterprise.value = null
}

// 生命周期
onMounted(() => {
  console.log('钢铁模块页面已挂载，开始加载企业列表')
  loadEnterpriseList()
})
</script>

<style scoped>
.steel-enterprise-list {
  padding: 0;
}

.query-bar {
  margin-bottom: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.action-bar {
  margin-bottom: 16px;
}

.enterprise-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

@media (max-width: 1200px) {
  .enterprise-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .enterprise-grid {
    grid-template-columns: 1fr;
  }
}

.enterprise-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.2s;
}

.enterprise-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>