<template>
  <div class="solid-waste-form">
    <n-tabs type="line">
      <n-tab-pane name="general" tab="一般固废">
        <div class="form-header">
          <n-space justify="space-between" align="center">
            <h4>一般工业固体废物管理</h4>
            <n-button type="primary" @click="addGeneralWaste">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加记录
            </n-button>
          </n-space>
        </div>
        
        <n-data-table
          :columns="generalColumns"
          :data="formData.general"
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
              :options="generalWasteOptions"
              placeholder="选择固废类型"
              size="small"
              style="width: 120px"
            />
          </template>
          
          <template #type="{ row, index }">
            <n-input
              v-model:value="row.type"
              placeholder="固废类别"
              size="small"
              style="width: 100px"
            />
          </template>
          
          <template #amount="{ row, index }">
            <n-input-number
              v-model:value="row.amount"
              placeholder="产生量"
              :min="0"
              :precision="2"
              size="small"
              style="width: 120px"
            />
          </template>
          
          <template #disposal="{ row, index }">
            <n-select
              v-model:value="row.disposal"
              :options="disposalOptions"
              placeholder="处置方式"
              size="small"
              style="width: 120px"
            />
          </template>
          
          <template #action="{ row, index }">
            <n-button
              size="small"
              type="error"
              @click="removeGeneralWaste(index)"
            >
              <template #icon>
                <TheIcon icon="carbon:trash-can" />
              </template>
            </n-button>
          </template>
        </n-data-table>
      </n-tab-pane>
      
      <n-tab-pane name="hazardous" tab="危险废物">
        <div class="form-header">
          <n-space justify="space-between" align="center">
            <h4>危险废物管理</h4>
            <n-button type="primary" @click="addHazardousWaste">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加记录
            </n-button>
          </n-space>
        </div>
        
        <n-data-table
          :columns="hazardousColumns"
          :data="formData.hazardous"
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
              :options="hazardousWasteOptions"
              placeholder="选择危废类型"
              size="small"
              style="width: 120px"
            />
          </template>
          
          <template #type="{ row, index }">
            <n-input
              v-model:value="row.type"
              placeholder="危废类别"
              size="small"
              style="width: 100px"
            />
          </template>
          
          <template #code="{ row, index }">
            <n-input
              v-model:value="row.code"
              placeholder="危废代码"
              size="small"
              style="width: 100px"
            />
          </template>
          
          <template #amount="{ row, index }">
            <n-input-number
              v-model:value="row.amount"
              placeholder="产生量"
              :min="0"
              :precision="2"
              size="small"
              style="width: 120px"
            />
          </template>
          
          <template #disposal="{ row, index }">
            <n-select
              v-model:value="row.disposal"
              :options="disposalOptions"
              placeholder="处置方式"
              size="small"
              style="width: 120px"
            />
          </template>
          
          <template #action="{ row, index }">
            <n-button
              size="small"
              type="error"
              @click="removeHazardousWaste(index)"
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
      general: [],
      hazardous: []
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

const generalWasteOptions = [
  { label: '钢渣', value: '钢渣' },
  { label: '高炉渣', value: '高炉渣' },
  { label: '转炉渣', value: '转炉渣' },
  { label: '电炉渣', value: '电炉渣' },
  { label: '铁合金渣', value: '铁合金渣' },
  { label: '含铁尘泥', value: '含铁尘泥' },
  { label: '氧化铁皮', value: '氧化铁皮' },
  { label: '废耐火材料', value: '废耐火材料' }
]

const hazardousWasteOptions = [
  { label: '废油', value: '废油' },
  { label: '废酸', value: '废酸' },
  { label: '废碱', value: '废碱' },
  { label: '废催化剂', value: '废催化剂' },
  { label: '废活性炭', value: '废活性炭' },
  { label: '废油漆', value: '废油漆' },
  { label: '废有机溶剂', value: '废有机溶剂' }
]

const disposalOptions = [
  { label: '综合利用', value: '综合利用' },
  { label: '委托处置', value: '委托处置' },
  { label: '焚烧', value: '焚烧' },
  { label: '填埋', value: '填埋' },
  { label: '贮存', value: '贮存' }
]

const generalColumns = [
  { title: '年份', key: 'year', width: 100 },
  { title: '固废名称', key: 'name', width: 120 },
  { title: '固废类别', key: 'type', width: 100 },
  { title: '产生量', key: 'amount', width: 120 },
  { title: '处置方式', key: 'disposal', width: 120 },
  { title: '操作', key: 'action', width: 80 }
]

const hazardousColumns = [
  { title: '年份', key: 'year', width: 100 },
  { title: '危废名称', key: 'name', width: 120 },
  { title: '危废类别', key: 'type', width: 100 },
  { title: '危废代码', key: 'code', width: 100 },
  { title: '产生量', key: 'amount', width: 120 },
  { title: '处置方式', key: 'disposal', width: 120 },
  { title: '操作', key: 'action', width: 80 }
]

const addGeneralWaste = () => {
  formData.value.general.push({
    year: 2024,
    name: '',
    type: '',
    amount: null,
    disposal: ''
  })
}

const addHazardousWaste = () => {
  formData.value.hazardous.push({
    year: 2024,
    name: '',
    type: '',
    code: '',
    amount: null,
    disposal: ''
  })
}

const removeGeneralWaste = (index) => {
  formData.value.general.splice(index, 1)
}

const removeHazardousWaste = (index) => {
  formData.value.hazardous.splice(index, 1)
}
</script>

<style scoped>
.solid-waste-form {
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
