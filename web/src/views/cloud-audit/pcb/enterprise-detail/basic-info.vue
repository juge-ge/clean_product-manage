<template>
  <div class="basic-info">
    <n-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-placement="left"
      label-width="140"
      require-mark-placement="right-hanging"
    >
      <n-card class="info-card mb-4" :bordered="false">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:building" class="header-icon" />
              <span class="header-title">基本信息</span>
            </div>
          </div>
        </template>
        <n-grid :cols="2" :x-gap="24" :y-gap="16">
          <n-form-item-gi label="企业名称" path="name">
            <n-input 
              v-model:value="formData.name" 
              placeholder="请输入企业名称"
              class="modern-input"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="统一社会信用代码" path="unifiedSocialCreditCode">
            <n-input 
              v-model:value="formData.unifiedSocialCreditCode" 
              placeholder="请输入统一社会信用代码"
              class="modern-input"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="所属地市" path="region">
            <n-input 
              v-model:value="formData.region" 
              placeholder="请输入所属地市"
              class="modern-input"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="所属县" path="district">
            <n-input 
              v-model:value="formData.district" 
              placeholder="请输入所属县"
              class="modern-input"
            />
          </n-form-item-gi>
        </n-grid>
      </n-card>

      <n-card class="info-card mb-4" :bordered="false">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:money" class="header-icon" />
              <span class="header-title">财务信息</span>
            </div>
          </div>
        </template>
        <n-grid :cols="2" :x-gap="24" :y-gap="16">
          <n-form-item-gi label="注册资本" path="capital">
            <n-input-number
              v-model:value="formData.capital"
              placeholder="请输入注册资本"
              :min="0"
              :precision="2"
              class="modern-input"
            >
              <template #suffix>万元</template>
            </n-input-number>
          </n-form-item-gi>
          
          <n-form-item-gi label="年产能" path="capacity">
            <n-input-number
              v-model:value="formData.capacity"
              placeholder="请输入年产能"
              :min="0"
              :precision="2"
              class="modern-input"
            >
              <template #suffix>万m²</template>
            </n-input-number>
          </n-form-item-gi>
        </n-grid>
      </n-card>

      <n-card class="info-card mb-4" :bordered="false">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:phone" class="header-icon" />
              <span class="header-title">联系信息</span>
            </div>
          </div>
        </template>
        <n-grid :cols="2" :x-gap="24" :y-gap="16">
          <n-form-item-gi label="法人代表" path="legalRepresentative">
            <n-input 
              v-model:value="formData.legalRepresentative" 
              placeholder="请输入法人代表"
              class="modern-input"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="联系人" path="contactPerson">
            <n-input 
              v-model:value="formData.contactPerson" 
              placeholder="请输入联系人"
              class="modern-input"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="联系电话" path="contactPhone">
            <n-input 
              v-model:value="formData.contactPhone" 
              placeholder="请输入联系电话"
              class="modern-input"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="联系邮箱" path="contactEmail">
            <n-input 
              v-model:value="formData.contactEmail" 
              placeholder="请输入联系邮箱"
              class="modern-input"
            />
          </n-form-item-gi>
        </n-grid>

        <n-form-item label="注册地址" path="address" class="mt-4">
          <n-input 
            v-model:value="formData.address" 
            placeholder="请输入注册地址"
            class="modern-input"
          />
        </n-form-item>
      </n-card>

      <n-card class="info-card" :bordered="false">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:industry" class="header-icon" />
              <span class="header-title">其他信息</span>
            </div>
          </div>
        </template>
        <n-grid :cols="2" :x-gap="24" :y-gap="16">
          <n-form-item-gi label="行业类型" path="industryType">
            <n-input
              v-model:value="formData.industryType"
              placeholder="请输入行业类型"
              class="modern-input"
            />
          </n-form-item-gi>
        </n-grid>
      </n-card>

      <div class="form-actions">
        <n-space justify="center" size="large">
          <n-button 
            @click="resetForm" 
            class="action-button"
            size="large"
          >
            <template #icon>
              <TheIcon icon="carbon:reset" />
            </template>
            重置
          </n-button>
          <n-button 
            type="primary" 
            @click="handleSubmit"
            class="action-button primary-button"
            size="large"
          >
            <template #icon>
              <TheIcon icon="carbon:save" />
            </template>
            保存
          </n-button>
        </n-space>
      </div>
    </n-form>

    <!-- 模块导航按钮 -->
    <div class="module-navigation mt-4">
      <n-space justify="space-between">
        <n-button disabled>
          <template #icon>
            <TheIcon icon="carbon:arrow-left" />
          </template>
          企业信息
        </n-button>
        <n-button type="primary" @click="goToNext">
          筹划与组织
          <template #icon>
            <TheIcon icon="carbon:arrow-right" />
          </template>
        </n-button>
      </n-space>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  NForm, 
  NFormItem, 
  NFormItemGi,
  NGrid, 
  NCard,
  NInput, 
  NInputNumber,
  NSelect,
  NDatePicker,
  NButton,
  NSpace
} from 'naive-ui'
import api from '@/api'

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

const formRef = ref(null)
const formData = ref({
  name: '',
  unifiedSocialCreditCode: '',
  region: '',
  district: '',
  capital: null,
  capacity: null,
  legalRepresentative: '',
  contactPerson: '',
  contactPhone: '',
  contactEmail: '',
  industryType: '',
  address: ''
})

const rules = {
  name: {
    required: true,
    message: '请输入企业名称',
    trigger: 'blur'
  },
  region: {
    required: true,
    message: '请输入所属地市',
    trigger: 'blur'
  },
  district: {
    required: true,
    message: '请输入所属县',
    trigger: 'blur'
  },
  legalRepresentative: {
    required: true,
    message: '请输入法人代表',
    trigger: 'blur'
  },
  contactPerson: {
    required: true,
    message: '请输入联系人',
    trigger: 'blur'
  },
  contactPhone: {
    required: true,
    message: '请输入联系电话',
    trigger: 'blur'
  },
  address: {
    required: true,
    message: '请输入注册地址',
    trigger: 'blur'
  }
}

// 获取企业信息（真实API）
const fetchEnterpriseInfo = async () => {
  try {
    const response = await api.pcb.enterprise.getDetail(props.enterpriseId)
    // 将后端字段映射到前端表单字段
    const backendData = response.data
    formData.value = {
      name: backendData.name || '',
      unifiedSocialCreditCode: backendData.unified_social_credit_code || '',
      region: backendData.region || '',
      district: backendData.district || '',
      capital: backendData.capital || null,
      capacity: backendData.capacity || null,
      legalRepresentative: backendData.legal_representative || '',
      contactPerson: backendData.contact_person || '',
      contactPhone: backendData.contact_phone || '',
      contactEmail: backendData.contact_email || '',
      industryType: backendData.industry_type || '',
      address: backendData.address || ''
    }
  } catch (error) {
    console.error('获取企业信息失败:', error)
    window.$message.error('获取企业信息失败')
  }
}

// 字段映射与清洗
const buildEnterprisePayload = (raw) => {
  if (!raw) return {}
  const trim = v => typeof v === 'string' ? v.trim() : v;
  const toNumber = (v) => {
    if (v === null || v === undefined || v === '') return undefined
    const n = Number(v)
    return Number.isFinite(n) ? n : undefined
  }
  return {
    name: trim(raw.name),
    unified_social_credit_code: trim(raw.unifiedSocialCreditCode),
    region: trim(raw.region),
    district: trim(raw.district),
    address: trim(raw.address),
    legal_representative: trim(raw.legalRepresentative),
    contact_person: trim(raw.contactPerson),
    contact_phone: raw.contactPhone ? String(raw.contactPhone).trim() : undefined,
    contact_email: trim(raw.contactEmail),
    industry_type: trim(raw.industryType),
    capital: toNumber(raw.capital),
    capacity: toNumber(raw.capacity),
  }
}

// 提交表单（真实API）
const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    const payload = buildEnterprisePayload(formData.value)
    await api.pcb.enterprise.update(props.enterpriseId, payload)
    window.$message.success('保存成功')
    emit('update', formData.value)
  } catch (error) {
    console.error('保存失败:', error)
    window.$message.error('保存失败')
  }
}

// 重置表单
const resetForm = () => {
  formRef.value?.restoreValidation()
  fetchEnterpriseInfo()
}

// 导航到下一个模块
const goToNext = () => {
  emit('navigate', 'planning')
}

onMounted(() => {
  fetchEnterpriseInfo()
})
</script>

<style scoped>
.basic-info {
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

/* 卡片样式 */
.info-card {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.info-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
}

/* 卡片头部样式 */
.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  font-size: 20px;
  color: #1890ff;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-title {
  font-size: 18px;
  font-weight: 600;
  color: #2c3e50;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 输入框样式 */
.modern-input {
  border-radius: 8px;
  transition: all 0.3s ease;
}

.modern-input :deep(.n-input__input-el) {
  border-radius: 8px;
  border: 2px solid #e8f4fd;
  transition: all 0.3s ease;
}

.modern-input :deep(.n-input__input-el:focus) {
  border-color: #1890ff;
  box-shadow: 0 0 0 3px rgba(24, 144, 255, 0.1);
}

.modern-input :deep(.n-input-number) {
  border-radius: 8px;
}

.modern-input :deep(.n-input-number .n-input__input-el) {
  border-radius: 8px;
  border: 2px solid #e8f4fd;
  transition: all 0.3s ease;
}

.modern-input :deep(.n-input-number .n-input__input-el:focus) {
  border-color: #1890ff;
  box-shadow: 0 0 0 3px rgba(24, 144, 255, 0.1);
}

/* 表单标签样式 */
:deep(.n-form-item-label) {
  font-weight: 500;
  color: #2c3e50;
}

/* 按钮样式 */
.form-actions {
  margin-top: 32px;
  padding: 24px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.action-button {
  border-radius: 12px;
  padding: 12px 24px;
  font-weight: 500;
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.primary-button {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  color: white;
}

.primary-button:hover {
  background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
}

/* 模块导航样式 */
.module-navigation {
  margin-top: 24px;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .basic-info {
    padding: 12px;
  }
  
  .header-title {
    font-size: 16px;
  }
  
  .form-actions {
    padding: 16px;
  }
  
  .action-button {
    padding: 10px 20px;
  }
}

/* 动画效果 */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.info-card {
  animation: fadeInUp 0.6s ease-out;
}

.info-card:nth-child(1) { animation-delay: 0.1s; }
.info-card:nth-child(2) { animation-delay: 0.2s; }
.info-card:nth-child(3) { animation-delay: 0.3s; }
.info-card:nth-child(4) { animation-delay: 0.4s; }
</style>
