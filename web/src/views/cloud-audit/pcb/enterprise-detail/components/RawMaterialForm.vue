<template>
  <div class="raw-material-form">
    <n-data-table
      :columns="columns"
      :data="formData"
      :row-key="row => row.id"
      :pagination="false"
    />
    
    <n-button type="primary" class="mt-4" @click="addRow">
      <template #icon>
        <TheIcon icon="carbon:add" />
      </template>
      添加一行
    </n-button>
  </div>
</template>

<script setup>
import { computed, h } from 'vue'
import { NDataTable, NButton, NInput, NInputNumber, NSelect } from 'naive-ui'
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
  { 
    title: '年份', 
    key: 'year', 
    width: 100,
    render: (row, index) => {
      return h(NSelect, {
        value: row.year,
        options: yearOptions,
        placeholder: "选择年份",
        onUpdateValue: (value) => {
          row.year = value
        }
      })
    }
  },
  { 
    title: '材料名称', 
    key: 'name', 
    width: 150,
    render: (row, index) => {
      return h(NInput, {
        value: row.name,
        placeholder: "请输入材料名称",
        onUpdateValue: (value) => {
          row.name = value
        }
      })
    }
  },
  { 
    title: '单位', 
    key: 'unit', 
    width: 80,
    render: (row, index) => {
      return h(NSelect, {
        value: row.unit,
        options: unitOptions,
        placeholder: "选择单位",
        onUpdateValue: (value) => {
          row.unit = value
        }
      })
    }
  },
  { 
    title: '工序', 
    key: 'process', 
    width: 120,
    render: (row, index) => {
      return h(NSelect, {
        value: row.process,
        options: processOptions,
        placeholder: "选择工序",
        onUpdateValue: (value) => {
          row.process = value
        }
      })
    }
  },
  { 
    title: '用量', 
    key: 'amount', 
    width: 120,
    render: (row, index) => {
      return h(NInputNumber, {
        value: row.amount,
        placeholder: "请输入用量",
        min: 0,
        precision: 2,
        onUpdateValue: (value) => {
          row.amount = value
        }
      })
    }
  },
  { 
    title: '状态', 
    key: 'state', 
    width: 100,
    render: (row, index) => {
      return h(NSelect, {
        value: row.state,
        options: stateOptions,
        placeholder: "选择状态",
        onUpdateValue: (value) => {
          row.state = value
        }
      })
    }
  },
  { 
    title: 'VOC含量(%)', 
    key: 'voc', 
    width: 120,
    render: (row, index) => {
      return h(NInputNumber, {
        value: row.voc,
        placeholder: "请输入VOC含量",
        min: 0,
        precision: 2,
        onUpdateValue: (value) => {
          row.voc = value
        }
      })
    }
  },
  { 
    title: '操作', 
    key: 'action', 
    width: 80,
    render: (row, index) => {
      return h(NButton, {
        size: "small",
        type: "error",
        onClick: () => removeRow(index)
      }, () => '删除')
    }
  }
]

const yearOptions = [
  { label: '2022', value: 2022 },
  { label: '2023', value: 2023 },
  { label: '2024', value: 2024 }
]

const unitOptions = [
  { label: 'm²', value: 'm²' },
  { label: 'kg', value: 'kg' },
  { label: 'L', value: 'L' },
  { label: 't', value: 't' }
]

const processOptions = [
  { label: '开料', value: '开料' },
  { label: '钻孔', value: '钻孔' },
  { label: '电镀', value: '电镀' },
  { label: '蚀刻', value: '蚀刻' },
  { label: '阻焊', value: '阻焊' },
  { label: '丝印', value: '丝印' }
]

const stateOptions = [
  { label: '固体', value: '固体' },
  { label: '液体', value: '液体' },
  { label: '气体', value: '气体' }
]

const addRow = () => {
  formData.value.push({
    id: Date.now(),
    year: 2023,
    name: '',
    unit: '',
    process: '',
    amount: null,
    state: '',
    voc: 0
  })
}

const removeRow = (index) => {
  formData.value.splice(index, 1)
}
</script>

<style scoped>
.raw-material-form {
  padding: 16px 0;
}
</style>

