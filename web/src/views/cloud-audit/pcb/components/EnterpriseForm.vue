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
      
      <n-form-item-gi label="统一社会信用代码" path="unifiedSocialCreditCode">
        <n-input v-model:value="formData.unifiedSocialCreditCode" placeholder="请输入统一社会信用代码" />
      </n-form-item-gi>
      
      <n-form-item-gi label="所属地市" path="region">
        <n-input v-model:value="formData.region" placeholder="请输入所属地市" />
      </n-form-item-gi>
      
      <n-form-item-gi label="所属县" path="district">
        <n-input v-model:value="formData.district" placeholder="请输入所属县" />
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
      
      <n-form-item-gi label="行业类型" path="industryType">
        <n-input v-model:value="formData.industryType" placeholder="请输入行业类型" />
      </n-form-item-gi>
    </n-grid>

    <n-form-item label="注册地址" path="address">
      <n-input v-model:value="formData.address" placeholder="请输入注册地址" />
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
  },
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
