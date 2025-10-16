<template>
  <div class="resource-consumption-form">
    <n-tabs type="line">
      <n-tab-pane name="energy" tab="能源消耗">
        <div class="form-header">
          <n-space justify="space-between" align="center">
            <h4>能源消耗情况</h4>
            <n-button type="primary" @click="addEnergyRecord">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加记录
            </n-button>
          </n-space>
        </div>
        
        <n-data-table
          :columns="energyColumns"
          :data="formData.energy"
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
          
          <template #type="{ row, index }">
            <n-select
              v-model:value="row.type"
              :options="energyTypeOptions"
              placeholder="选择能源类型"
              size="small"
              style="width: 120px"
            />
          </template>
          
          <template #amount="{ row, index }">
            <n-input-number
              v-model:value="row.amount"
              placeholder="消耗量"
              :min="0"
              :precision="2"
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
          
          <template #action="{ row, index }">
            <n-button
              size="small"
              type="error"
              @click="removeEnergyRecord(index)"
            >
              <template #icon>
                <TheIcon icon="carbon:trash-can" />
              </template>
            </n-button>
          </template>
        </n-data-table>
      </n-tab-pane>
      
      <n-tab-pane name="water" tab="水资源消耗">
        <div class="form-header">
          <n-space justify="space-between" align="center">
            <h4>水资源消耗情况</h4>
            <n-button type="primary" @click="addWaterRecord">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加记录
            </n-button>
          </n-space>
        </div>
        
        <n-data-table
          :columns="waterColumns"
          :data="formData.water"
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
          
          <template #type="{ row, index }">
            <n-select
              v-model:value="row.type"
              :options="waterTypeOptions"
              placeholder="选择水类型"
              size="small"
              style="width: 120px"
            />
          </template>
          
          <template #amount="{ row, index }">
            <n-input-number
              v-model:value="row.amount"
              placeholder="消耗量"
              :min="0"
              :precision="2"
              size="small"
              style="width: 120px"
            />
          </template>
          
          <template #source="{ row, index }">
            <n-input
              v-model:value="row.source"
              placeholder="水源"
              size="small"
              style="width: 100px"
            />
          </template>
          
          <template #action="{ row, index }">
            <n-button
              size="small"
              type="error"
              @click="removeWaterRecord(index)"
            >
              <template #icon>
                <TheIcon icon="carbon:trash-can" />
              </template>
            </n-button>
          </template>
        </n-data-table>
      </n-tab-pane>
      
      <n-tab-pane name="electricity" tab="电力消耗">
        <div class="form-header">
          <n-space justify="space-between" align="center">
            <h4>电力消耗情况</h4>
            <n-button type="primary" @click="addElectricityRecord">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加记录
            </n-button>
          </n-space>
        </div>
        
        <n-data-table
          :columns="electricityColumns"
          :data="formData.electricity"
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
          
          <template #amount="{ row, index }">
            <n-input-number
              v-model:value="row.amount"
              placeholder="消耗量"
              :min="0"
              :precision="2"
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
          
          <template #action="{ row, index }">
            <n-button
              size="small"
              type="error"
              @click="removeElectricityRecord(index)"
            >
              <template #icon>
                <TheIcon icon="carbon:trash-can" />
              </template>
            </n-button>
          </template>
        </n-data-table>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NDataTable, NButton, NInput, NInputNumber, NSelect, NSpace, NTabs, NTabPane } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      energy: [],
      water: [],
      electricity: []
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const yearOptions = [
  { label: '2022', value: 2022 },
  { label: '2023', value: 2023 },
  { label: '2024', value: 2024 }
]

const energyTypeOptions = [
  { label: '煤炭', value: '煤炭' },
  { label: '天然气', value: '天然气' },
  { label: '重油', value: '重油' },
  { label: '柴油', value: '柴油' },
  { label: '焦炉煤气', value: '焦炉煤气' },
  { label: '高炉煤气', value: '高炉煤气' },
  { label: '转炉煤气', value: '转炉煤气' }
]

const waterTypeOptions = [
  { label: '新鲜水', value: '新鲜水' },
  { label: '循环水', value: '循环水' },
  { label: '软化水', value: '软化水' },
  { label: '除盐水', value: '除盐水' }
]

const energyColumns = [
  { title: '年份', key: 'year', width: 100 },
  { title: '能源类型', key: 'type', width: 120 },
  { title: '消耗量', key: 'amount', width: 120 },
  { title: '单位', key: 'unit', width: 80 },
  { title: '操作', key: 'action', width: 80 }
]

const waterColumns = [
  { title: '年份', key: 'year', width: 100 },
  { title: '水类型', key: 'type', width: 120 },
  { title: '消耗量', key: 'amount', width: 120 },
  { title: '水源', key: 'source', width: 100 },
  { title: '操作', key: 'action', width: 80 }
]

const electricityColumns = [
  { title: '年份', key: 'year', width: 100 },
  { title: '消耗量', key: 'amount', width: 120 },
  { title: '单位', key: 'unit', width: 80 },
  { title: '操作', key: 'action', width: 80 }
]

const addEnergyRecord = () => {
  formData.value.energy.push({
    year: 2024,
    type: '',
    amount: null,
    unit: ''
  })
}

const addWaterRecord = () => {
  formData.value.water.push({
    year: 2024,
    type: '',
    amount: null,
    source: ''
  })
}

const addElectricityRecord = () => {
  formData.value.electricity.push({
    year: 2024,
    amount: null,
    unit: ''
  })
}

const removeEnergyRecord = (index) => {
  formData.value.energy.splice(index, 1)
}

const removeWaterRecord = (index) => {
  formData.value.water.splice(index, 1)
}

const removeElectricityRecord = (index) => {
  formData.value.electricity.splice(index, 1)
}
</script>

<style scoped>
.resource-consumption-form {
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
