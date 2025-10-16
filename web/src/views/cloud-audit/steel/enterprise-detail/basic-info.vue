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
          
          <n-form-item-gi label="年产钢量" path="annualOutput">
            <n-input-number
              v-model:value="formData.annualOutput"
              placeholder="请输入年产钢量"
              :min="0"
              :precision="2"
            >
              <template #suffix>万吨</template>
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
          
          <n-form-item-gi label="生产能力" path="productionCapacity">
            <n-input-number
              v-model:value="formData.productionCapacity"
              placeholder="请输入生产能力"
              :min="0"
              :precision="2"
            >
              <template #suffix>万吨/年</template>
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

      <n-card title="钢铁行业信息">
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi label="建厂时间" path="establishmentDate">
            <n-date-picker
              v-model:value="formData.establishmentDate"
              type="date"
              placeholder="请选择建厂时间"
              style="width: 100%"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="所属行业" path="industry">
            <n-input
              v-model:value="formData.industry"
              placeholder="请输入所属行业"
              disabled
              value="钢铁制造"
            />
          </n-form-item-gi>
        </n-grid>
        
        <n-form-item label="主要产品" path="mainProducts">
          <n-input 
            v-model:value="formData.mainProducts" 
            placeholder="如：螺纹钢、线材、中厚板等"
            type="textarea"
            :rows="3"
          />
        </n-form-item>
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
import { ref, onMounted, watch } from 'vue'
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
import TheIcon from '@/components/icon/TheIcon.vue'
import { mockApi } from '@/mock/steel'

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  },
  enterprise: {
    type: Object,
    default: () => ({})
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
  productionCapacity: null,
  legalRepresentative: '',
  address: '',
  productionAddress: '',
  contact: '',
  phone: '',
  postalCode: '',
  establishmentDate: null,
  industry: '钢铁制造',
  mainProducts: ''
})

const scaleOptions = [
  { label: '特大型', value: '特大型' },
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
    message: '请输入年产钢量',
    trigger: 'change'
  },
  annualSales: {
    required: true,
    message: '请输入年销售额',
    trigger: 'change'
  },
  productionCapacity: {
    required: true,
    message: '请输入生产能力',
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
    message: '请选择建厂时间',
    trigger: 'change'
  }
}

// 获取企业信息
const fetchEnterpriseInfo = async () => {
  try {
    // 如果已经有企业数据，直接使用
    if (props.enterprise && Object.keys(props.enterprise).length > 0) {
      const data = { ...props.enterprise }
      // 转换日期字符串为时间戳
      if (data.establishmentDate && typeof data.establishmentDate === 'string') {
        data.establishmentDate = new Date(data.establishmentDate).getTime()
      }
      formData.value = data
      return
    }

    // 否则从API获取
    const response = await mockApi.getEnterpriseDetail(props.enterpriseId)
    const data = response.data
    // 转换日期字符串为时间戳
    if (data.establishmentDate && typeof data.establishmentDate === 'string') {
      data.establishmentDate = new Date(data.establishmentDate).getTime()
    }
    formData.value = data
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

// 监听企业数据变化
watch(() => props.enterprise, (newEnterprise) => {
  if (newEnterprise && Object.keys(newEnterprise).length > 0) {
    const data = { ...newEnterprise }
    // 转换日期字符串为时间戳
    if (data.establishmentDate && typeof data.establishmentDate === 'string') {
      data.establishmentDate = new Date(data.establishmentDate).getTime()
    }
    formData.value = data
  }
}, { immediate: true, deep: true })

onMounted(() => {
  fetchEnterpriseInfo()
})
</script>

<style scoped>
.basic-info {
  padding: 16px;
}
</style>
