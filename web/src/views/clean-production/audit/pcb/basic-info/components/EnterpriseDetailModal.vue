<template>
  <n-modal
    v-model:show="showModal"
    preset="card"
    title="企业详细信息"
    size="large"
    :bordered="false"
    style="width: 800px"
    @close="handleClose"
  >
    <div v-if="enterprise" class="enterprise-detail">
      <div class="detail-header">
        <h2 class="enterprise-title">{{ enterprise.name }}</h2>
        <div class="enterprise-meta">
          <span class="meta-item">
            <n-icon><svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M12,11.5A2.5,2.5 0 0,1 9.5,9A2.5,2.5 0 0,1 12,6.5A2.5,2.5 0 0,1 14.5,9A2.5,2.5 0 0,1 12,11.5M12,2A7,7 0 0,0 5,9C5,14.25 12,22 12,22S19,14.25 19,9A7,7 0 0,0 12,2Z" /></svg></n-icon>
            {{ enterprise.city }} {{ enterprise.county }}
          </span>
          <span class="meta-item">
            <n-icon><svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M12,6A6,6 0 0,0 6,12A6,6 0 0,0 12,18A6,6 0 0,0 18,12A6,6 0 0,0 12,6M12,8A4,4 0 0,1 16,12A4,4 0 0,1 12,16A4,4 0 0,1 8,12A4,4 0 0,1 12,8Z" /></svg></n-icon>
            {{ enterprise.scale }}
          </span>
        </div>
      </div>

      <div class="detail-content">
        <div class="info-grid">
          <div class="info-item">
            <label class="info-label">所属地市</label>
            <span class="info-value">{{ enterprise.city }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">所属县</label>
            <span class="info-value">{{ enterprise.county }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">名称</label>
            <span class="info-value">{{ enterprise.name }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">规模</label>
            <span class="info-value">{{ enterprise.scale }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">注册资本（万元）</label>
            <span class="info-value">{{ enterprise.registeredCapital.toLocaleString() }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">年产值（万元）</label>
            <span class="info-value">{{ enterprise.annualOutput.toLocaleString() }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">年销售额（万元）</label>
            <span class="info-value">{{ enterprise.annualSales.toLocaleString() }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">法人代表</label>
            <span class="info-value">{{ enterprise.legalRepresentative }}</span>
          </div>
          
          <div class="info-item full-width">
            <label class="info-label">地址（注册地址、生产地址）</label>
            <span class="info-value">{{ enterprise.registeredAddress }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">邮编</label>
            <span class="info-value">{{ enterprise.postalCode }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">联系人</label>
            <span class="info-value">{{ enterprise.contactPerson }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">联系电话</label>
            <span class="info-value">{{ enterprise.contactPhone }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">建厂时间</label>
            <span class="info-value">{{ enterprise.establishmentTime }}</span>
          </div>
          
          <div class="info-item">
            <label class="info-label">所属行业</label>
            <span class="info-value">{{ enterprise.industry }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-else class="loading-container">
      <n-spin size="large" />
    </div>

    <template #footer>
      <div class="modal-footer">
        <n-button @click="handleClose">关闭</n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { NModal, NIcon, NButton, NSpin } from 'naive-ui'
import { mockEnterprises } from '../data/mockData.js'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  enterpriseId: {
    type: Number,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:show'])

// 响应式数据
const showModal = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const enterprise = ref(null)

// 监听enterpriseId变化，加载对应企业数据
watch(() => props.enterpriseId, (newId) => {
  if (newId) {
    loadEnterpriseData(newId)
  }
}, { immediate: true })

// 方法
const loadEnterpriseData = (id) => {
  // 模拟异步加载
  setTimeout(() => {
    enterprise.value = mockEnterprises.find(ent => ent.id === id) || null
  }, 100)
}

const handleClose = () => {
  showModal.value = false
  enterprise.value = null
}
</script>

<style scoped>
.enterprise-detail {
  padding: 0;
}

.detail-header {
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #f0f0f0;
}

.enterprise-title {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin: 0 0 12px 0;
}

.enterprise-meta {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #666;
  font-size: 14px;
}

.detail-content {
  max-height: 500px;
  overflow-y: auto;
}

.info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-item.full-width {
  grid-column: 1 / -1;
}

.info-label {
  font-weight: 500;
  color: #666;
  font-size: 14px;
  margin: 0;
}

.info-value {
  color: #333;
  font-size: 14px;
  line-height: 1.4;
  word-break: break-all;
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .enterprise-meta {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
