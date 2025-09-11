<template>
  <div class="pollution-control-form">
    <n-space vertical :size="16">
      <!-- 金属铜回收量 -->
      <n-card title="金属铜回收量" size="small">
        <n-data-table
          :columns="recoveryColumns"
          :data="formData.copperRecovery"
          :pagination="false"
        />
        <n-button type="primary" size="small" class="mt-2" @click="addRecoveryRow">
          添加数据
        </n-button>
      </n-card>

      <!-- 工业用水重复利用率 -->
      <n-card title="工业用水重复利用率" size="small">
        <n-data-table
          :columns="reuseRateColumns"
          :data="formData.waterReuseRate"
          :pagination="false"
        />
        <n-button type="primary" size="small" class="mt-2" @click="addReuseRateRow">
          添加数据
        </n-button>
      </n-card>

      <!-- 废气排放 -->
      <n-card title="废气排放处理" size="small">
        <n-data-table
          :columns="gasEmissionColumns"
          :data="formData.gasEmission"
          :pagination="false"
        />
        <n-button type="primary" size="small" class="mt-2" @click="addGasEmissionRow">
          添加数据
        </n-button>
      </n-card>

      <!-- 废水排放 -->
      <n-card title="废水排放处理" size="small">
        <n-data-table
          :columns="waterEmissionColumns"
          :data="formData.waterEmission"
          :pagination="false"
        />
        <n-button type="primary" size="small" class="mt-2" @click="addWaterEmissionRow">
          添加数据
        </n-button>
      </n-card>
    </n-space>
  </div>
</template>

<script setup>
import { computed, h } from 'vue'
import { 
  NSpace,
  NCard,
  NDataTable, 
  NButton, 
  NInput,
  NInputNumber, 
  NSelect 
} from 'naive-ui'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      copperRecovery: [],
      waterReuseRate: [],
      gasEmission: [],
      waterEmission: []
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

// 铜回收量表格列
const recoveryColumns = [
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
    title: '回收量（kg）', 
    key: 'amount', 
    width: 150,
    render: (row) => h(NInputNumber, {
      value: row.amount,
      min: 0,
      precision: 2,
      onUpdateValue: (value) => { row.amount = value }
    })
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeRecoveryRow(index)
    }, () => '删除')
  }
]

// 水重复利用率表格列
const reuseRateColumns = [
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
    title: '利用率（%）', 
    key: 'rate', 
    width: 150,
    render: (row) => h(NInputNumber, {
      value: row.rate,
      min: 0,
      max: 100,
      precision: 2,
      onUpdateValue: (value) => { row.rate = value }
    })
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeReuseRateRow(index)
    }, () => '删除')
  }
]

// 废气排放表格列
const gasEmissionColumns = [
  { 
    title: '工艺名称', 
    key: 'process', 
    width: 120,
    render: (row) => h(NInput, {
      value: row.process,
      placeholder: "如：蚀刻",
      onUpdateValue: (value) => { row.process = value }
    })
  },
  { 
    title: '分类', 
    key: 'category', 
    width: 120,
    render: (row) => h(NInput, {
      value: row.category,
      placeholder: "如：酸性废气",
      onUpdateValue: (value) => { row.category = value }
    })
  },
  { 
    title: '处理方式', 
    key: 'method', 
    width: 150,
    render: (row) => h(NInput, {
      value: row.method,
      placeholder: "如：碱液喷淋",
      onUpdateValue: (value) => { row.method = value }
    })
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeGasEmissionRow(index)
    }, () => '删除')
  }
]

// 废水排放表格列
const waterEmissionColumns = [
  { 
    title: '工艺名称', 
    key: 'process', 
    width: 120,
    render: (row) => h(NInput, {
      value: row.process,
      placeholder: "如：电镀",
      onUpdateValue: (value) => { row.process = value }
    })
  },
  { 
    title: '分类', 
    key: 'category', 
    width: 120,
    render: (row) => h(NInput, {
      value: row.category,
      placeholder: "如：含铜废水",
      onUpdateValue: (value) => { row.category = value }
    })
  },
  { 
    title: '处理方式', 
    key: 'method', 
    width: 150,
    render: (row) => h(NInput, {
      value: row.method,
      placeholder: "如：化学沉淀",
      onUpdateValue: (value) => { row.method = value }
    })
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => h(NButton, {
      size: "small",
      type: "error",
      onClick: () => removeWaterEmissionRow(index)
    }, () => '删除')
  }
]

// 添加数据行方法
const addRecoveryRow = () => {
  formData.value.copperRecovery.push({
    id: Date.now(),
    year: 2023,
    amount: null
  })
}

const addReuseRateRow = () => {
  formData.value.waterReuseRate.push({
    id: Date.now(),
    year: 2023,
    rate: null
  })
}

const addGasEmissionRow = () => {
  formData.value.gasEmission.push({
    id: Date.now(),
    process: '',
    category: '',
    method: ''
  })
}

const addWaterEmissionRow = () => {
  formData.value.waterEmission.push({
    id: Date.now(),
    process: '',
    category: '',
    method: ''
  })
}

// 删除数据行方法
const removeRecoveryRow = (index) => {
  formData.value.copperRecovery.splice(index, 1)
}

const removeReuseRateRow = (index) => {
  formData.value.waterReuseRate.splice(index, 1)
}

const removeGasEmissionRow = (index) => {
  formData.value.gasEmission.splice(index, 1)
}

const removeWaterEmissionRow = (index) => {
  formData.value.waterEmission.splice(index, 1)
}
</script>

<style scoped>
.pollution-control-form {
  padding: 16px 0;
}
</style>

