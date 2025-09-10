<template>
  <n-card class="enterprise-card" hoverable>
    <div class="card-header">
      <h3>{{ enterprise.name }}</h3>
      <n-tag :type="getStatusType(enterprise.auditStatus)">
        {{ getStatusText(enterprise.auditStatus) }}
      </n-tag>
    </div>
    
    <div class="card-content">
      <p><strong>所属地市：</strong>{{ enterprise.city }}</p>
      <p><strong>所属县：</strong>{{ enterprise.county }}</p>
      <p><strong>规模：</strong>{{ enterprise.scale }}</p>
      <p><strong>年产值：</strong>{{ enterprise.annualOutput }}万元</p>
    </div>
    
    <div class="card-footer">
      <n-button size="small" @click="$emit('view', enterprise.id)">
        查看详情
      </n-button>
      <n-button size="small" type="primary" @click="$emit('edit', enterprise)">
        编辑
      </n-button>
      <n-button size="small" type="error" @click="$emit('delete', enterprise.id)">
        删除
      </n-button>
    </div>
  </n-card>
</template>

<script setup>
import { NButton, NCard, NTag } from 'naive-ui'

defineProps({
  enterprise: {
    type: Object,
    required: true
  }
})

defineEmits(['view', 'edit', 'delete'])

const getStatusType = (status) => {
  const types = {
    pending: 'default',
    'in-progress': 'info',
    completed: 'success'
  }
  return types[status] || 'default'
}

const getStatusText = (status) => {
  const texts = {
    pending: '待审核',
    'in-progress': '审核中',
    completed: '已完成'
  }
  return texts[status] || '未知'
}
</script>

<style scoped>
.enterprise-card {
  transition: all 0.3s ease;
}

.enterprise-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-content p {
  margin: 8px 0;
  color: #666;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 16px;
}
</style>
