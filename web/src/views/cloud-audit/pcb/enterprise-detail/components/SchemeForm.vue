<template>
  <n-form ref="formRef" :model="formData" :rules="rules">
    <n-form-item label="方案名称" path="name">
      <n-input v-model:value="formData.name" placeholder="请输入方案名称" />
    </n-form-item>
    
    <n-form-item label="方案类型" path="type">
      <n-select
        v-model:value="formData.type"
        :options="typeOptions"
        placeholder="请选择方案类型"
      />
    </n-form-item>
    
    <n-form-item label="关联指标" path="indicatorIds">
      <n-tree-select
        v-model:value="formData.indicatorIds"
        :options="indicatorTreeOptions"
        multiple
        checkable
        placeholder="请选择关联指标"
      />
    </n-form-item>
    
    <n-form-item label="方案描述" path="description">
      <n-input
        v-model:value="formData.description"
        type="textarea"
        placeholder="请输入方案描述"
        :rows="3"
      />
    </n-form-item>
    
    <n-form-item label="实施方案" path="implementation">
      <n-input
        v-model:value="formData.implementation"
        type="textarea"
        placeholder="请输入实施方案"
        :rows="4"
      />
    </n-form-item>
    
    <n-form-item label="预期效果" path="expectedEffect">
      <n-input
        v-model:value="formData.expectedEffect"
        type="textarea"
        placeholder="请输入预期效果"
        :rows="3"
      />
    </n-form-item>
    
    <n-form-item label="投资估算" path="investment">
      <n-input-number
        v-model:value="formData.investment"
        placeholder="请输入投资估算"
        :min="0"
        :precision="2"
      >
        <template #suffix>万元</template>
      </n-input-number>
    </n-form-item>
    
    <n-form-item label="投资回收期" path="paybackPeriod">
      <n-input-number
        v-model:value="formData.paybackPeriod"
        placeholder="请输入投资回收期"
        :min="0"
        :precision="1"
      >
        <template #suffix>年</template>
      </n-input-number>
    </n-form-item>
  </n-form>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { 
  NForm, 
  NFormItem, 
  NInput, 
  NInputNumber, 
  NSelect, 
  NTreeSelect 
} from 'naive-ui'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:data'])

// 表单引用
const formRef = ref(null)

// 表单数据
const formData = computed({
  get: () => ({
    name: '',
    type: '',
    indicatorIds: [],
    description: '',
    implementation: '',
    expectedEffect: '',
    investment: null,
    paybackPeriod: null,
    status: 'active',
    ...props.data
  }),
  set: (value) => emit('update:data', value)
})

// 方案类型选项
const typeOptions = [
  { label: '节能降耗', value: '节能降耗' },
  { label: '污染防治', value: '污染防治' },
  { label: '资源综合利用', value: '资源综合利用' },
  { label: '工艺改进', value: '工艺改进' },
  { label: '设备更新', value: '设备更新' }
]

// 指标树选项
const indicatorTreeOptions = ref([
  {
    label: '生产工艺与装备要求',
    key: 'process',
    children: [
      { label: '刚性单面板生产工艺', key: '1' },
      { label: '刚性双面板生产工艺', key: '2' },
      { label: '刚性多层板生产工艺', key: '3' },
      { label: '挠性单面板生产工艺', key: '4' },
      { label: '挠性双面板生产工艺', key: '5' },
      { label: '挠性多层板生产工艺', key: '6' }
    ]
  },
  {
    label: '资源能源消耗',
    key: 'resource',
    children: [
      { label: '单位产品电耗', key: '7' },
      { label: '单位产品新鲜水耗', key: '15' },
      { label: '水资源重复利用率', key: '19' },
      { label: '覆铜板利用率', key: '20' },
      { label: '金属铜回收率', key: '28' }
    ]
  },
  {
    label: '污染防治',
    key: 'pollution',
    children: [
      { label: '一般工业固体废物综合利用率', key: '29' },
      { label: '污染物产生量', key: '30' },
      { label: '污染治理设施', key: '42' }
    ]
  },
  {
    label: '环境管理',
    key: 'management',
    children: [
      { label: '温室气体排放', key: '47' },
      { label: '产品特征', key: '50' },
      { label: '环保法律法规执行情况', key: '54' },
      { label: '清洁生产审核', key: '57' },
      { label: '节能管理', key: '58' }
    ]
  }
])

// 表单验证规则
const rules = {
  name: { required: true, message: '请输入方案名称', trigger: 'blur' },
  type: { required: true, message: '请选择方案类型', trigger: 'change' },
  indicatorIds: { 
    required: true, 
    type: 'array', 
    min: 1, 
    message: '请选择至少一个关联指标', 
    trigger: 'change' 
  },
  description: { required: true, message: '请输入方案描述', trigger: 'blur' },
  implementation: { required: true, message: '请输入实施方案', trigger: 'blur' },
  expectedEffect: { required: true, message: '请输入预期效果', trigger: 'blur' },
  investment: { required: true, message: '请输入投资估算', trigger: 'change' },
  paybackPeriod: { required: true, message: '请输入投资回收期', trigger: 'change' }
}

// 监听数据变化
watch(() => props.data, (newData) => {
  if (newData && Object.keys(newData).length > 0) {
    // 数据已通过 computed 处理
  }
}, { immediate: true, deep: true })

// 验证表单
const validate = async () => {
  await formRef.value?.validate()
  return formData.value
}

// 重置表单
const restoreValidation = () => {
  formRef.value?.restoreValidation()
}

// 暴露方法给父组件
defineExpose({
  validate,
  restoreValidation
})
</script>

<style scoped>
:deep(.n-form-item) {
  margin-bottom: 20px;
}

:deep(.n-form-item-label) {
  width: 120px;
  text-align: right;
  padding-right: 12px;
}
</style>

