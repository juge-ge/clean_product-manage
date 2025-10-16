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
      <n-card title="基本信息" class="mb-4">
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi label="企业名称" path="name">
            <n-input v-model:value="formData.name" placeholder="请输入企业名称" />
          </n-form-item-gi>
          
          <n-form-item-gi label="统一社会信用代码" path="unifiedSocialCreditCode">
            <n-input v-model:value="formData.unifiedSocialCreditCode" placeholder="请输入统一社会信用代码" />
          </n-form-item-gi>
          
          <n-form-item-gi label="所属地市" path="region">
            <n-input v-model:value="formData.region" placeholder="请输入所属地市" />
          </n-form-item-gi>
          
          <n-form-item-gi label="所属县" path="district">
            <n-input v-model:value="formData.district" placeholder="请输入所属县" />
          </n-form-item-gi>
        </n-grid>
      </n-card>

      <n-card title="财务信息" class="mb-4">
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi label="注册资本" path="capital">
            <n-input-number
              v-model:value="formData.capital"
              placeholder="请输入注册资本"
              :min="0"
              :precision="2"
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
            >
              <template #suffix>万m²</template>
            </n-input-number>
          </n-form-item-gi>
        </n-grid>
      </n-card>

      <n-card title="联系信息" class="mb-4">
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi label="法人代表" path="legalRepresentative">
            <n-input v-model:value="formData.legalRepresentative" placeholder="请输入法人代表" />
          </n-form-item-gi>
          
          <n-form-item-gi label="联系人" path="contactPerson">
            <n-input v-model:value="formData.contactPerson" placeholder="请输入联系人" />
          </n-form-item-gi>
          
          <n-form-item-gi label="联系电话" path="contactPhone">
            <n-input v-model:value="formData.contactPhone" placeholder="请输入联系电话" />
          </n-form-item-gi>
          
          <n-form-item-gi label="联系邮箱" path="contactEmail">
            <n-input v-model:value="formData.contactEmail" placeholder="请输入联系邮箱" />
          </n-form-item-gi>
        </n-grid>

        <n-form-item label="注册地址" path="address">
          <n-input v-model:value="formData.address" placeholder="请输入注册地址" />
        </n-form-item>
      </n-card>

      <n-card title="其他信息">
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi label="行业类型" path="industryType">
            <n-input
              v-model:value="formData.industryType"
              placeholder="请输入行业类型"
            />
          </n-form-item-gi>
        </n-grid>
      </n-card>

      <div class="flex justify-center mt-4">
        <n-space>
          <n-button @click="resetForm">重置</n-button>
          <n-button type="primary" @click="handleSubmit">保存</n-button>
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
  padding: 16px;
}
</style>
