<template>
  <div class="scheme-form">
    <n-form
      ref="formRef"
      :model="formData"
      :rules="rules"
      label-placement="left"
      label-width="120"
      require-mark-placement="right-hanging"
    >
      <n-grid :cols="2" :x-gap="24">
        <n-form-item-gi label="方案名称" path="name">
          <n-input v-model:value="formData.name" placeholder="请输入方案名称" />
        </n-form-item-gi>
        
        <n-form-item-gi label="方案类型" path="type">
          <n-select
            v-model:value="formData.type"
            :options="typeOptions"
            placeholder="请选择方案类型"
          />
        </n-form-item-gi>
        
        <n-form-item-gi label="投资估算" path="investment">
          <n-input-number
            v-model:value="formData.investment"
            placeholder="请输入投资估算"
            :min="0"
            :precision="2"
          >
            <template #suffix>万元</template>
          </n-input-number>
        </n-form-item-gi>
        
        <n-form-item-gi label="投资回收期" path="paybackPeriod">
          <n-input-number
            v-model:value="formData.paybackPeriod"
            placeholder="请输入投资回收期"
            :min="0"
            :precision="1"
          >
            <template #suffix>年</template>
          </n-input-number>
        </n-form-item-gi>
      </n-grid>
      
      <n-form-item label="方案描述" path="description">
        <n-input
          v-model:value="formData.description"
          type="textarea"
          placeholder="请输入方案描述"
          :rows="3"
        />
      </n-form-item>
      
      <n-form-item label="解决问题" path="problemSolved">
        <n-input
          v-model:value="formData.problemSolved"
          type="textarea"
          placeholder="请输入解决的问题"
          :rows="3"
        />
      </n-form-item>
      
      <n-form-item label="实施方案" path="implementation">
        <n-input
          v-model:value="formData.implementation"
          type="textarea"
          placeholder="请输入实施方案"
          :rows="3"
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
      
      <n-form-item label="经济效益" path="economicBenefit">
        <n-input
          v-model:value="formData.economicBenefit"
          type="textarea"
          placeholder="请输入经济效益"
          :rows="3"
        />
      </n-form-item>
      
      <n-form-item label="环境效益" path="environmentalBenefit">
        <n-input
          v-model:value="formData.environmentalBenefit"
          type="textarea"
          placeholder="请输入环境效益"
          :rows="3"
        />
      </n-form-item>
      
      <n-form-item label="关联指标" path="indicatorIds">
        <n-select
          v-model:value="formData.indicatorIds"
          :options="indicatorOptions"
          multiple
          filterable
          placeholder="请选择关联指标"
          :max-tag-count="3"
        />
      </n-form-item>
      
      <n-form-item label="适用条件" path="applicableConditions">
        <n-input
          v-model:value="formData.applicableConditions"
          type="textarea"
          placeholder="请输入适用条件"
          :rows="2"
        />
      </n-form-item>
      
      <n-form-item label="风险分析" path="riskAnalysis">
        <n-input
          v-model:value="formData.riskAnalysis"
          type="textarea"
          placeholder="请输入风险分析"
          :rows="2"
        />
      </n-form-item>
      
      <n-form-item label="参考案例" path="referenceCase">
        <n-input
          v-model:value="formData.referenceCase"
          type="textarea"
          placeholder="请输入参考案例"
          :rows="2"
        />
      </n-form-item>
    </n-form>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { NForm, NFormItem, NFormItemGi, NGrid, NInput, NInputNumber, NSelect } from 'naive-ui'

const props = defineProps({
  data: {
    type: Object,
    default: () => ({})
  }
})

const emit = defineEmits(['update:modelValue'])

const formRef = ref(null)
const formData = ref({
  name: '',
  type: '',
  description: '',
  problemSolved: '',
  implementation: '',
  expectedEffect: '',
  economicBenefit: '',
  environmentalBenefit: '',
  investment: null,
  paybackPeriod: null,
  indicatorIds: [],
  applicableConditions: '',
  riskAnalysis: '',
  referenceCase: ''
})

const typeOptions = [
  { label: '工艺优化', value: '工艺优化' },
  { label: '设备改造', value: '设备改造' },
  { label: '节能降耗', value: '节能降耗' },
  { label: '污染治理', value: '污染治理' },
  { label: '水处理', value: '水处理' },
  { label: '固废利用', value: '固废利用' },
  { label: '管理优化', value: '管理优化' }
]

const indicatorOptions = [
  // 生产工艺与装备
  { label: '烧结工艺装备', value: 1 },
  { label: '球团工艺装备', value: 2 },
  { label: '炼铁工艺装备', value: 3 },
  { label: '炼钢工艺装备', value: 4 },
  { label: '轧钢工艺装备', value: 5 },
  { label: '能源回收利用装置', value: 6 },
  
  // 资源能源消耗
  { label: '吨钢综合能耗', value: 7 },
  { label: '吨钢电耗', value: 8 },
  { label: '吨钢新水消耗', value: 9 },
  { label: '焦化工序能耗', value: 10 },
  { label: '烧结工序能耗', value: 11 },
  { label: '球团工序能耗', value: 12 },
  { label: '炼铁工序能耗', value: 13 },
  { label: '炼钢工序能耗', value: 14 },
  { label: '轧钢工序能耗', value: 15 },
  { label: '水循环利用率', value: 16 },
  { label: '固体废弃物资源综合利用率', value: 17 },
  
  // 污染物产生
  { label: '吨钢COD产生量', value: 18 },
  { label: '吨钢氨氮产生量', value: 19 },
  { label: '吨钢SO₂产生量', value: 20 },
  { label: '吨钢NOx产生量', value: 21 },
  { label: '吨钢烟粉尘产生量', value: 22 },
  { label: '吨钢废水产生量', value: 23 },
  
  // 废物回收利用
  { label: '废钢利用率', value: 24 },
  { label: '高炉煤气回收利用率', value: 25 },
  { label: '转炉煤气回收利用率', value: 26 },
  { label: '焦炉煤气回收利用率', value: 27 },
  { label: '余热余压利用率', value: 28 },
  
  // 环境管理
  { label: '环保法律法规执行情况', value: 29 },
  { label: '产业政策符合性', value: 30 },
  { label: '清洁生产管理', value: 31 },
  { label: '环境管理体系认证', value: 32 },
  { label: '能源管理体系认证', value: 33 },
  { label: '污染物排放监测', value: 34 },
  { label: '危险废物处置', value: 35 },
  { label: '节能管理', value: 36 },
  { label: '碳排放管理', value: 37 },
  { label: '清洁生产审核', value: 38 }
]

const rules = {
  name: {
    required: true,
    message: '请输入方案名称',
    trigger: 'blur'
  },
  type: {
    required: true,
    message: '请选择方案类型',
    trigger: 'change'
  },
  description: {
    required: true,
    message: '请输入方案描述',
    trigger: 'blur'
  },
  problemSolved: {
    required: true,
    message: '请输入解决的问题',
    trigger: 'blur'
  },
  implementation: {
    required: true,
    message: '请输入实施方案',
    trigger: 'blur'
  },
  expectedEffect: {
    required: true,
    message: '请输入预期效果',
    trigger: 'blur'
  },
  economicBenefit: {
    required: true,
    message: '请输入经济效益',
    trigger: 'blur'
  },
  environmentalBenefit: {
    required: true,
    message: '请输入环境效益',
    trigger: 'blur'
  },
  investment: {
    required: true,
    message: '请输入投资估算',
    trigger: 'change'
  },
  paybackPeriod: {
    required: true,
    message: '请输入投资回收期',
    trigger: 'change'
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

<style scoped>
.scheme-form {
  padding: 16px;
}
</style>
