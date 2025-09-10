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
          
          <n-form-item-gi label="所属地市" path="city">
            <n-input v-model:value="formData.city" placeholder="请输入所属地市" />
          </n-form-item-gi>
          
          <n-form-item-gi label="所属县" path="county">
            <n-input v-model:value="formData.county" placeholder="请输入所属县" />
          </n-form-item-gi>
          
          <n-form-item-gi label="企业规模" path="scale">
            <n-select
              v-model:value="formData.scale"
              :options="scaleOptions"
              placeholder="请选择企业规模"
            />
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
          
          <n-form-item-gi label="年产值" path="annualOutput">
            <n-input-number
              v-model:value="formData.annualOutput"
              placeholder="请输入年产值"
              :min="0"
              :precision="2"
            >
              <template #suffix>万元</template>
            </n-input-number>
          </n-form-item-gi>
          
          <n-form-item-gi label="年销售额" path="annualSales">
            <n-input-number
              v-model:value="formData.annualSales"
              placeholder="请输入年销售额"
              :min="0"
              :precision="2"
            >
              <template #suffix>万元</template>
            </n-input-number>
          </n-form-item-gi>
        </n-grid>
      </n-card>

      <n-card title="联系信息" class="mb-4">
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi label="法人代表" path="legalRepresentative">
            <n-input v-model:value="formData.legalRepresentative" placeholder="请输入法人代表" />
          </n-form-item-gi>
          
          <n-form-item-gi label="联系人" path="contact">
            <n-input v-model:value="formData.contact" placeholder="请输入联系人" />
          </n-form-item-gi>
          
          <n-form-item-gi label="联系电话" path="phone">
            <n-input v-model:value="formData.phone" placeholder="请输入联系电话" />
          </n-form-item-gi>
          
          <n-form-item-gi label="邮政编码" path="postalCode">
            <n-input v-model:value="formData.postalCode" placeholder="请输入邮政编码" />
          </n-form-item-gi>
        </n-grid>

        <n-form-item label="注册地址" path="address">
          <n-input v-model:value="formData.address" placeholder="请输入注册地址" />
        </n-form-item>
        
        <n-form-item label="生产地址" path="productionAddress">
          <n-input v-model:value="formData.productionAddress" placeholder="请输入生产地址" />
        </n-form-item>
      </n-card>

      <n-card title="其他信息">
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi label="成立日期" path="establishmentDate">
            <n-date-picker
              v-model:value="formData.establishmentDate"
              type="date"
              placeholder="请选择成立日期"
              style="width: 100%"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="所属行业" path="industry">
            <n-input
              v-model:value="formData.industry"
              placeholder="请输入所属行业"
              disabled
              value="PCB制造"
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
import { mockApi } from '@/mock/pcb'

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
  city: '',
  county: '',
  scale: null,
  capital: null,
  annualOutput: null,
  annualSales: null,
  legalRepresentative: '',
  address: '',
  productionAddress: '',
  contact: '',
  phone: '',
  postalCode: '',
  establishmentDate: null,
  industry: 'PCB制造'
})

const scaleOptions = [
  { label: '大型', value: '大型' },
  { label: '中型', value: '中型' },
  { label: '小型', value: '小型' }
]

const rules = {
  name: {
    required: true,
    message: '请输入企业名称',
    trigger: 'blur'
  },
  city: {
    required: true,
    message: '请输入所属地市',
    trigger: 'blur'
  },
  county: {
    required: true,
    message: '请输入所属县',
    trigger: 'blur'
  },
  scale: {
    required: true,
    message: '请选择企业规模',
    trigger: 'change'
  },
  capital: {
    required: true,
    message: '请输入注册资本',
    trigger: 'change'
  },
  annualOutput: {
    required: true,
    message: '请输入年产值',
    trigger: 'change'
  },
  legalRepresentative: {
    required: true,
    message: '请输入法人代表',
    trigger: 'blur'
  },
  contact: {
    required: true,
    message: '请输入联系人',
    trigger: 'blur'
  },
  phone: {
    required: true,
    message: '请输入联系电话',
    trigger: 'blur'
  },
  address: {
    required: true,
    message: '请输入注册地址',
    trigger: 'blur'
  },
  productionAddress: {
    required: true,
    message: '请输入生产地址',
    trigger: 'blur'
  },
  establishmentDate: {
    required: true,
    message: '请选择成立日期',
    trigger: 'change'
  }
}

// 获取企业信息
const fetchEnterpriseInfo = async () => {
  try {
    const response = await mockApi.getEnterpriseDetail(props.enterpriseId)
    formData.value = response.data
  } catch (error) {
    console.error('获取企业信息失败:', error)
    window.$message.error('获取企业信息失败')
  }
}

// 提交表单
const handleSubmit = async () => {
  try {
    await formRef.value?.validate()
    await mockApi.updateEnterprise(props.enterpriseId, formData.value)
    window.$message.success('保存成功')
    emit('update', formData.value)
  } catch (error) {
    if (error?.message) {
      console.error('保存失败:', error)
      window.$message.error('保存失败')
    }
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
