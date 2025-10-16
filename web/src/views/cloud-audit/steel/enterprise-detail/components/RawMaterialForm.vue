<template>
  <div class="raw-material-form">
    <div class="form-header">
      <n-space justify="space-between" align="center">
        <h4>原辅材料使用情况</h4>
        <n-button type="primary" @click="addMaterial">
          <template #icon>
            <TheIcon icon="carbon:add" />
          </template>
          添加材料
        </n-button>
      </n-space>
    </div>
    
    <n-data-table
      :columns="columns"
      :data="formData"
      :pagination="false"
      :bordered="true"
      :single-line="false"
      size="small"
    >
      <template #year="{ row, index }">
        <n-select
          v-model:value="row.year"
          :options="yearOptions"
          placeholder="选择年份"
          size="small"
          style="width: 100px"
        />
      </template>
      
      <template #name="{ row, index }">
        <n-select
          v-model:value="row.name"
          :options="materialOptions"
          placeholder="选择材料"
          size="small"
          style="width: 120px"
        />
      </template>
      
      <template #unit="{ row, index }">
        <n-input
          v-model:value="row.unit"
          placeholder="单位"
          size="small"
          style="width: 80px"
        />
      </template>
      
      <template #process="{ row, index }">
        <n-select
          v-model:value="row.process"
          :options="processOptions"
          placeholder="选择工序"
          size="small"
          style="width: 100px"
        />
      </template>
      
      <template #amount="{ row, index }">
        <n-input-number
          v-model:value="row.amount"
          placeholder="用量"
          :min="0"
          :precision="2"
          size="small"
          style="width: 100px"
        />
      </template>
      
      <template #source="{ row, index }">
        <n-input
          v-model:value="row.source"
          placeholder="来源"
          size="small"
          style="width: 100px"
        />
      </template>
      
      <template #quality="{ row, index }">
        <n-input
          v-model:value="row.quality"
          placeholder="质量指标"
          size="small"
          style="width: 120px"
        />
      </template>
      
      <template #action="{ row, index }">
        <n-button
          size="small"
          type="error"
          @click="removeMaterial(index)"
        >
          <template #icon>
            <TheIcon icon="carbon:trash-can" />
          </template>
        </n-button>
      </template>
    </n-data-table>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NDataTable, NButton, NInput, NInputNumber, NSelect, NSpace } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const columns = [
  { title: '年份', key: 'year', width: 100 },
  { title: '材料名称', key: 'name', width: 120 },
  { title: '单位', key: 'unit', width: 80 },
  { title: '工序', key: 'process', width: 100 },
  { title: '用量', key: 'amount', width: 100 },
  { title: '来源', key: 'source', width: 100 },
  { title: '质量指标', key: 'quality', width: 120 },
  { title: '操作', key: 'action', width: 80 }
]

const yearOptions = [
  { label: '2022', value: 2022 },
  { label: '2023', value: 2023 },
  { label: '2024', value: 2024 }
]

const materialOptions = [
  { label: '铁矿石', value: '铁矿石' },
  { label: '焦炭', value: '焦炭' },
  { label: '石灰石', value: '石灰石' },
  { label: '白云石', value: '白云石' },
  { label: '萤石', value: '萤石' },
  { label: '硅石', value: '硅石' },
  { label: '锰矿', value: '锰矿' },
  { label: '废钢', value: '废钢' }
]

const processOptions = [
  { label: '烧结', value: '烧结' },
  { label: '球团', value: '球团' },
  { label: '焦化', value: '焦化' },
  { label: '炼铁', value: '炼铁' },
  { label: '炼钢', value: '炼钢' },
  { label: '轧钢', value: '轧钢' }
]

const addMaterial = () => {
  formData.value.push({
    year: 2024,
    name: '',
    unit: '',
    process: '',
    amount: null,
    source: '',
    quality: ''
  })
}

const removeMaterial = (index) => {
  formData.value.splice(index, 1)
}
</script>

<style scoped>
.raw-material-form {
  padding: 16px;
}

.form-header {
  margin-bottom: 16px;
}

.form-header h4 {
  margin: 0;
  color: var(--n-text-color);
  font-weight: 600;
}
</style>
