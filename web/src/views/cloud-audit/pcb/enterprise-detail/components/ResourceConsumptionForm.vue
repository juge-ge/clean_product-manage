<template>
  <div class="resource-consumption-form">
    <n-tabs type="line">
      <n-tab-pane name="water" tab="水资源消耗">
        <div class="resource-section">
          <n-data-table
            :columns="waterColumns"
            :data="formData.water"
            :row-key="row => row.id"
            :pagination="false"
          />
          <n-button type="primary" class="mt-4" @click="addWaterRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加水资源数据
          </n-button>
        </div>
      </n-tab-pane>
      
      <n-tab-pane name="electricity" tab="电力消耗">
        <div class="resource-section">
          <n-data-table
            :columns="electricityColumns"
            :data="formData.electricity"
            :row-key="row => row.id"
            :pagination="false"
          />
          <n-button type="primary" class="mt-4" @click="addElectricityRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加电力数据
          </n-button>
        </div>
      </n-tab-pane>
      
      <n-tab-pane name="gas" tab="燃气消耗">
        <div class="resource-section">
          <n-data-table
            :columns="gasColumns"
            :data="formData.gas"
            :row-key="row => row.id"
            :pagination="false"
          />
          <n-button type="primary" class="mt-4" @click="addGasRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加燃气数据
          </n-button>
        </div>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup>
import { computed, h } from 'vue'
import { 
  NTabs, 
  NTabPane, 
  NDataTable, 
  NButton, 
  NInput,
  NInputNumber, 
  NSelect 
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      water: [],
      electricity: [],
      gas: []
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

// 水资源表格列
const waterColumns = [
  { 
    title: '年份', 
    key: 'year', 
    width: 100,
    render: (row) => h(NSelect, {
      value: row.year,
      options: yearOptions,
      onUpdateValue: (value) => { row.year = value }
    })
  },
  { 
    title: '类型', 
    key: 'type', 
    width: 150,
    render: (row) => h(NInput, {
      value: row.type,
      placeholder: "如：市政自来水",
      onUpdateValue: (value) => { row.type = value }
    })
  },
  { 
    title: '用量（m³）', 
    key: 'amount', 
    width: 120,
    render: (row) => h(NInputNumber, {
      value: row.amount,
      min: 0,
      precision: 2,
      onUpdateValue: (value) => { row.amount = value }
    })
  },
  { 
    title: '来源', 
    key: 'source', 
    width: 150,
    render: (row) => h(NInput, {
      value: row.source,
      placeholder: "如：市政管网",
      onUpdateValue: (value) => { row.source = value }
    })
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeWaterRow(index)
    }, () => '删除')
  }
]

// 电力表格列
const electricityColumns = [
  { 
    title: '年份', 
    key: 'year', 
    width: 100,
    render: (row) => h(NSelect, {
      value: row.year,
      options: yearOptions,
      onUpdateValue: (value) => { row.year = value }
    })
  },
  { 
    title: '类型', 
    key: 'type', 
    width: 150,
    render: (row) => h(NInput, {
      value: row.type,
      placeholder: "如：市电",
      onUpdateValue: (value) => { row.type = value }
    })
  },
  { 
    title: '用量（kWh）', 
    key: 'amount', 
    width: 120,
    render: (row) => h(NInputNumber, {
      value: row.amount,
      min: 0,
      precision: 2,
      onUpdateValue: (value) => { row.amount = value }
    })
  },
  { 
    title: '来源', 
    key: 'source', 
    width: 150,
    render: (row) => h(NInput, {
      value: row.source,
      placeholder: "如：国家电网",
      onUpdateValue: (value) => { row.source = value }
    })
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeElectricityRow(index)
    }, () => '删除')
  }
]

// 燃气表格列
const gasColumns = [
  { 
    title: '年份', 
    key: 'year', 
    width: 100,
    render: (row) => h(NSelect, {
      value: row.year,
      options: yearOptions,
      onUpdateValue: (value) => { row.year = value }
    })
  },
  { 
    title: '类型', 
    key: 'type', 
    width: 150,
    render: (row) => h(NInput, {
      value: row.type,
      placeholder: "如：天然气",
      onUpdateValue: (value) => { row.type = value }
    })
  },
  { 
    title: '用量（m³）', 
    key: 'amount', 
    width: 120,
    render: (row) => h(NInputNumber, {
      value: row.amount,
      min: 0,
      precision: 2,
      onUpdateValue: (value) => { row.amount = value }
    })
  },
  { 
    title: '来源', 
    key: 'source', 
    width: 150,
    render: (row) => h(NInput, {
      value: row.source,
      placeholder: "如：市政燃气",
      onUpdateValue: (value) => { row.source = value }
    })
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeGasRow(index)
    }, () => '删除')
  }
]

// 添加数据行方法
const addWaterRow = () => {
  formData.value.water.push({
    id: Date.now(),
    year: 2023,
    type: '',
    amount: null,
    source: ''
  })
}

const addElectricityRow = () => {
  formData.value.electricity.push({
    id: Date.now(),
    year: 2023,
    type: '',
    amount: null,
    source: ''
  })
}

const addGasRow = () => {
  formData.value.gas.push({
    id: Date.now(),
    year: 2023,
    type: '',
    amount: null,
    source: ''
  })
}

// 删除数据行方法
const removeWaterRow = (index) => {
  formData.value.water.splice(index, 1)
}

const removeElectricityRow = (index) => {
  formData.value.electricity.splice(index, 1)
}

const removeGasRow = (index) => {
  formData.value.gas.splice(index, 1)
}
</script>

<style scoped>
.resource-consumption-form {
  padding: 16px 0;
}

.resource-section {
  min-height: 200px;
}
</style>

