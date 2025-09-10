<template>
  <n-form
    ref="formRef"
    :model="formData"
    :rules="rules"
    label-placement="left"
    label-width="120"
    require-mark-placement="right-hanging"
  >
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
      
      <n-form-item-gi label="法人代表" path="legalRepresentative">
        <n-input v-model:value="formData.legalRepresentative" placeholder="请输入法人代表" />
      </n-form-item-gi>
      
      <n-form-item-gi label="联系人" path="contact">
        <n-input v-model:value="formData.contact" placeholder="请输入联系人" />
      </n-form-item-gi>
      
      <n-form-item-gi label="联系电话" path="phone">
        <n-input v-model:value="formData.phone" placeholder="请输入联系电话" />
      </n-form-item-gi>
      
      <n-form-item-gi label="成立日期" path="establishmentDate">
        <n-date-picker
          v-model:value="formData.establishmentDate"
          type="date"
          placeholder="请选择成立日期"
          style="width: 100%"
        />
      </n-form-item-gi>
    </n-grid>

    <n-form-item label="注册地址" path="address">
      <n-input v-model:value="formData.address" placeholder="请输入注册地址" />
    </n-form-item>
    
    <n-form-item label="生产地址" path="productionAddress">
      <n-input v-model:value="formData.productionAddress" placeholder="请输入生产地址" />
    </n-form-item>
  </n-form>
</template>

<script setup>
import { ref, watch } from 'vue'
import { NForm, NFormItem, NFormItemGi, NGrid, NInput, NInputNumber, NSelect, NDatePicker } from 'naive-ui'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  }
})

const formRef = ref(null)
const formData = ref({
  name: '',
  city: '',
  county: '',
  scale: null,
  capital: null,
  annualOutput: null,
  legalRepresentative: '',
  address: '',
  productionAddress: '',
  contact: '',
  phone: '',
  establishmentDate: null
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
  establishmentDate: {
    required: true,
    message: '请选择成立日期',
    trigger: 'change'
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
  }
}

// 监听props.data变化，更新表单数据
watch(() => props.data, (newVal) => {
  if (newVal) {
    formData.value = { ...newVal }
  }
}, { deep: true, immediate: true })

// 暴露方法给父组件
defineExpose({
  formRef,
  formData
})
</script>
