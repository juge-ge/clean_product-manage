<template>
  <n-modal
    v-model:show="showModal"
    preset="card"
    :title="modalTitle"
    size="large"
    :bordered="false"
    style="width: 800px"
    @close="handleClose"
  >
    <n-form
      ref="formRef"
      :model="formData"
      :rules="formRules"
      label-placement="left"
      label-width="120px"
      require-mark-placement="right-hanging"
    >
      <div class="form-grid">
        <n-form-item label="所属地市" path="city">
          <n-input v-model:value="formData.city" placeholder="请输入所属地市" />
        </n-form-item>
        
        <n-form-item label="所属县" path="county">
          <n-input v-model:value="formData.county" placeholder="请输入所属县" />
        </n-form-item>
        
        <n-form-item label="名称" path="name">
          <n-input v-model:value="formData.name" placeholder="请输入企业名称" />
        </n-form-item>
        
        <n-form-item label="规模" path="scale">
          <n-select
            v-model:value="formData.scale"
            placeholder="请选择企业规模"
            :options="scaleOptions"
          />
        </n-form-item>
        
        <n-form-item label="注册资本（万元）" path="registeredCapital">
          <n-input-number
            v-model:value="formData.registeredCapital"
            placeholder="请输入注册资本"
            :min="0"
            :precision="0"
            style="width: 100%"
          />
        </n-form-item>
        
        <n-form-item label="年产值（万元）" path="annualOutput">
          <n-input-number
            v-model:value="formData.annualOutput"
            placeholder="请输入年产值"
            :min="0"
            :precision="0"
            style="width: 100%"
          />
        </n-form-item>
        
        <n-form-item label="年销售额（万元）" path="annualSales">
          <n-input-number
            v-model:value="formData.annualSales"
            placeholder="请输入年销售额"
            :min="0"
            :precision="0"
            style="width: 100%"
          />
        </n-form-item>
        
        <n-form-item label="法人代表" path="legalRepresentative">
          <n-input v-model:value="formData.legalRepresentative" placeholder="请输入法人代表" />
        </n-form-item>
        
        <n-form-item label="注册地址" path="registeredAddress" class="full-width">
          <n-input
            v-model:value="formData.registeredAddress"
            type="textarea"
            placeholder="请输入注册地址"
            :rows="2"
          />
        </n-form-item>
        
        <n-form-item label="生产地址" path="productionAddress" class="full-width">
          <n-input
            v-model:value="formData.productionAddress"
            type="textarea"
            placeholder="请输入生产地址"
            :rows="2"
          />
        </n-form-item>
        
        <n-form-item label="邮编" path="postalCode">
          <n-input v-model:value="formData.postalCode" placeholder="请输入邮编" />
        </n-form-item>
        
        <n-form-item label="联系人" path="contactPerson">
          <n-input v-model:value="formData.contactPerson" placeholder="请输入联系人" />
        </n-form-item>
        
        <n-form-item label="联系电话" path="contactPhone">
          <n-input v-model:value="formData.contactPhone" placeholder="请输入联系电话" />
        </n-form-item>
        
        <n-form-item label="建厂时间" path="establishmentTime">
          <n-date-picker
            v-model:value="formData.establishmentTime"
            type="date"
            placeholder="请选择建厂时间"
            style="width: 100%"
          />
        </n-form-item>
        
        <n-form-item label="所属行业" path="industry">
          <n-input v-model:value="formData.industry" placeholder="请输入所属行业" />
        </n-form-item>
      </div>
    </n-form>

    <template #footer>
      <div class="modal-footer">
        <n-button @click="handleClose">取消</n-button>
        <n-button type="primary" :loading="submitting" @click="handleSubmit">
          {{ mode === 'create' ? '创建' : '保存' }}
        </n-button>
      </div>
    </template>
  </n-modal>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import {
  NModal,
  NForm,
  NFormItem,
  NInput,
  NSelect,
  NInputNumber,
  NDatePicker,
  NButton
} from 'naive-ui'
import { mockEnterprises } from '../data/mockData.js'

// Props
const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  mode: {
    type: String,
    default: 'create', // 'create' | 'edit'
    validator: (value) => ['create', 'edit'].includes(value)
  },
  enterpriseId: {
    type: Number,
    default: null
  }
})

// Emits
const emit = defineEmits(['update:show', 'success'])

// 响应式数据
const showModal = computed({
  get: () => props.show,
  set: (value) => emit('update:show', value)
})

const formRef = ref(null)
const submitting = ref(false)

// 表单数据
const formData = ref({
  city: '',
  county: '',
  name: '',
  scale: '',
  registeredCapital: null,
  annualOutput: null,
  annualSales: null,
  legalRepresentative: '',
  registeredAddress: '',
  productionAddress: '',
  postalCode: '',
  contactPerson: '',
  contactPhone: '',
  establishmentTime: null,
  industry: ''
})

// 表单验证规则
const formRules = {
  city: { required: true, message: '请输入所属地市', trigger: 'blur' },
  county: { required: true, message: '请输入所属县', trigger: 'blur' },
  name: { required: true, message: '请输入企业名称', trigger: 'blur' },
  scale: { required: true, message: '请选择企业规模', trigger: 'change' },
  registeredCapital: { required: true, message: '请输入注册资本', trigger: 'blur' },
  annualOutput: { required: true, message: '请输入年产值', trigger: 'blur' },
  annualSales: { required: true, message: '请输入年销售额', trigger: 'blur' },
  legalRepresentative: { required: true, message: '请输入法人代表', trigger: 'blur' },
  registeredAddress: { required: true, message: '请输入注册地址', trigger: 'blur' },
  productionAddress: { required: true, message: '请输入生产地址', trigger: 'blur' },
  postalCode: { required: true, message: '请输入邮编', trigger: 'blur' },
  contactPerson: { required: true, message: '请输入联系人', trigger: 'blur' },
  contactPhone: { required: true, message: '请输入联系电话', trigger: 'blur' },
  establishmentTime: { required: true, message: '请选择建厂时间', trigger: 'change' },
  industry: { required: true, message: '请输入所属行业', trigger: 'blur' }
}

// 企业规模选项
const scaleOptions = [
  { label: '大型企业', value: '大型企业' },
  { label: '中型企业', value: '中型企业' },
  { label: '小型企业', value: '小型企业' },
  { label: '微型企业', value: '微型企业' }
]

// 计算属性
const modalTitle = computed(() => {
  return props.mode === 'create' ? '创建企业' : '编辑企业'
})

// 监听enterpriseId变化，加载企业数据
watch(() => props.enterpriseId, (newId) => {
  if (newId && props.mode === 'edit') {
    loadEnterpriseData(newId)
  }
}, { immediate: true })

// 监听show变化，重置表单
watch(() => props.show, (newShow) => {
  if (newShow && props.mode === 'create') {
    resetForm()
  }
})

// 方法
const loadEnterpriseData = (id) => {
  const enterprise = mockEnterprises.find(ent => ent.id === id)
  if (enterprise) {
    formData.value = { ...enterprise }
    // 转换日期格式
    if (enterprise.establishmentTime) {
      formData.value.establishmentTime = new Date(enterprise.establishmentTime).getTime()
    }
  }
}

const resetForm = () => {
  formData.value = {
    city: '',
    county: '',
    name: '',
    scale: '',
    registeredCapital: null,
    annualOutput: null,
    annualSales: null,
    legalRepresentative: '',
    registeredAddress: '',
    productionAddress: '',
    postalCode: '',
    contactPerson: '',
    contactPhone: '',
    establishmentTime: null,
    industry: ''
  }
  
  nextTick(() => {
    formRef.value?.restoreValidation()
  })
}

const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    submitting.value = true
    
    // 模拟提交延迟
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // 这里应该调用API提交数据
    console.log('提交数据:', formData.value)
    
    // 提交成功
    emit('success')
    handleClose()
    
  } catch (error) {
    console.error('表单验证失败:', error)
  } finally {
    submitting.value = false
  }
}

const handleClose = () => {
  showModal.value = false
  resetForm()
}
</script>

<style scoped>
.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.full-width {
  grid-column: 1 / -1;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
