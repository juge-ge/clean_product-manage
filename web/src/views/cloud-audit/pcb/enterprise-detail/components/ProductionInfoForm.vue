<template>
  <div class="production-info-form">
    <!-- 1. 近三年产品产量 -->
    <div class="section">
      <div class="section-header">
        <h3 class="section-title">近三年产品产量</h3>
        <n-button type="primary" @click="addProductOutputRow">
          <template #icon>
            <TheIcon icon="carbon:add" />
          </template>
          添加产品产量记录
        </n-button>
      </div>
      <n-data-table
        :columns="productOutputColumns"
        :data="productOutputData"
        :pagination="false"
        :bordered="true"
        class="data-table"
      >
        <template #empty>
          <div class="empty-state">
            <span>暂无数据，请点击上方按钮添加记录</span>
          </div>
        </template>
      </n-data-table>
          </div>

    <!-- 2. 企业近三年合格率 -->
    <div class="section">
      <div class="section-header">
        <h3 class="section-title">企业近三年合格率</h3>
        <n-button type="primary" @click="addQualificationRateRow">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
          添加合格率记录
            </n-button>
          </div>
      <n-data-table
        :columns="qualificationRateColumns"
        :data="qualificationRateData"
        :pagination="false"
        :bordered="true"
        class="data-table"
      >
        <template #empty>
          <div class="empty-state">
            <span>暂无数据，请点击上方按钮添加记录</span>
          </div>
        </template>
      </n-data-table>
          </div>

    <!-- 3. 企业近三年产值情况 -->
    <div class="section">
      <div class="section-header">
        <h3 class="section-title">企业近三年产值情况</h3>
        <n-button type="primary" @click="addOutputValueRow">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
          添加产值记录
            </n-button>
      </div>
      <n-data-table
        :columns="outputValueColumns"
        :data="outputValueData"
        :pagination="false"
        :bordered="true"
        class="data-table"
      >
        <template #empty>
          <div class="empty-state">
            <span>暂无数据，请点击上方按钮添加记录</span>
          </div>
      </template>
      </n-data-table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, h } from 'vue'
import { 
  NDataTable, NButton, NSelect, NInput, NInputNumber, NSpace
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      productOutput: [],
      qualificationRate: [],
      outputValue: []
    })
  }
})

const emit = defineEmits(['update:modelValue'])

// 枚举选项
const typeOptions = [
  { label: '刚性', value: 'rigid' },
  { label: '挠性', value: 'flexible' }
]

const rigidProductOptions = [
  { label: '刚性单面板', value: 'rigid_single', defaultLayers: 1 },
  { label: '刚性双面板', value: 'rigid_double', defaultLayers: 2 },
  { label: '刚性多面板', value: 'rigid_multilayer', defaultLayers: null },
  { label: '刚性HDI板', value: 'rigid_hdi', defaultLayers: null }
]

const flexibleProductOptions = [
  { label: '挠性单面板', value: 'flexible_single', defaultLayers: 1 },
  { label: '挠性双面板', value: 'flexible_double', defaultLayers: 2 },
  { label: '挠性多面板', value: 'flexible_multilayer', defaultLayers: null },
  { label: '挠性HDI板', value: 'flexible_hdi', defaultLayers: null }
]

const unitOptions = [
  { label: 'm²', value: 'm2' }
]

const yearOptions = Array.from({ length: 10 }, (_, i) => {
  const year = new Date().getFullYear() - 5 + i
  return { label: year.toString(), value: year.toString() }
})

const outputValueUnitOptions = [
  { label: '万元', value: 'wan_yuan' }
]

const layerOptions = Array.from({ length: 30 }, (_, i) => ({
  label: `${i + 1}层`,
  value: i + 1
}))

// 计算属性
const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

// 数据
const productOutputData = computed({
  get: () => formData.value.productOutput || [],
  set: (value) => {
    formData.value.productOutput = value
  }
})

const qualificationRateData = computed({
  get: () => formData.value.qualificationRate || [],
  set: (value) => {
    formData.value.qualificationRate = value
  }
})

const outputValueData = computed({
  get: () => formData.value.outputValue || [],
  set: (value) => {
    formData.value.outputValue = value
  }
})

// 表格列定义
const productOutputColumns = [
  {
    title: '类型',
    key: 'type',
    width: 100,
    render: (row, index) => {
      return h(NSelect, {
        value: row.type,
        'onUpdate:value': (value) => {
          productOutputData.value[index].type = value
          // 重置主要产品选项
          productOutputData.value[index].mainProduct = null
          productOutputData.value[index].layers = null
        },
        options: typeOptions,
        placeholder: '请选择类型'
      })
    }
  },
  {
    title: '主要产品',
    key: 'mainProduct',
    width: 150,
    render: (row, index) => {
      const options = row.type === 'rigid' ? rigidProductOptions : flexibleProductOptions
      return h(NSelect, {
        value: row.mainProduct,
        'onUpdate:value': (value) => {
          productOutputData.value[index].mainProduct = value
          // 设置默认层数
          const selectedProduct = options.find(opt => opt.value === value)
          if (selectedProduct && selectedProduct.defaultLayers) {
            productOutputData.value[index].layers = selectedProduct.defaultLayers
          } else {
            productOutputData.value[index].layers = null
          }
        },
        options: options,
        placeholder: '请选择产品',
        disabled: !row.type
      })
    }
  },
  {
    title: '单位',
    key: 'unit',
    width: 100,
    render: (row, index) => {
      return h(NSelect, {
        value: row.unit,
        'onUpdate:value': (value) => {
          productOutputData.value[index].unit = value
        },
        options: unitOptions,
        placeholder: '请选择单位'
      })
    }
  },
  {
    title: '年份',
    key: 'year',
    width: 100,
    render: (row, index) => {
      return h(NSelect, {
        value: row.year,
        'onUpdate:value': (value) => {
          productOutputData.value[index].year = value
        },
        options: yearOptions,
        placeholder: '请选择年份'
      })
    }
  },
  {
    title: '产量',
    key: 'output',
    width: 120,
    render: (row, index) => {
      return h(NInputNumber, {
        value: row.output,
        'onUpdate:value': (value) => {
          productOutputData.value[index].output = value
        },
        placeholder: '请输入产量',
        min: 0,
        precision: 2
      })
    }
  },
  {
    title: '层数',
    key: 'layers',
    width: 100,
    render: (row, index) => {
      const selectedProduct = row.type === 'rigid' 
        ? rigidProductOptions.find(opt => opt.value === row.mainProduct)
        : flexibleProductOptions.find(opt => opt.value === row.mainProduct)
      
      if (selectedProduct && selectedProduct.defaultLayers) {
        return h('span', selectedProduct.defaultLayers + '层')
      }
      
      return h(NSelect, {
        value: row.layers,
        'onUpdate:value': (value) => {
          productOutputData.value[index].layers = value
        },
        options: layerOptions,
        placeholder: '请选择层数',
        disabled: !row.mainProduct || (selectedProduct && selectedProduct.defaultLayers)
      })
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    render: (row, index) => {
      return h(NSpace, [
        h(NButton, {
          size: 'small',
          type: 'error',
          onClick: () => removeProductOutputRow(index)
        }, { default: () => '删除' })
      ])
    }
  }
]

const qualificationRateColumns = [
  {
    title: '年份',
    key: 'year',
    width: 120,
    render: (row, index) => {
      return h(NSelect, {
        value: row.year,
        'onUpdate:value': (value) => {
          qualificationRateData.value[index].year = value
        },
        options: yearOptions,
        placeholder: '请选择年份'
      })
    }
  },
  {
    title: '合格率(%)',
    key: 'rate',
    width: 150,
    render: (row, index) => {
      return h(NInputNumber, {
        value: row.rate,
        'onUpdate:value': (value) => {
          qualificationRateData.value[index].rate = value
        },
        placeholder: '请输入合格率',
        min: 0,
        max: 100,
        precision: 2,
        suffix: '%',
        style: { width: '120px' }
      })
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    render: (row, index) => {
      return h(NSpace, [
        h(NButton, {
          size: 'small',
          type: 'error',
          onClick: () => removeQualificationRateRow(index)
        }, { default: () => '删除' })
      ])
    }
  }
]

const outputValueColumns = [
  {
    title: '年份',
    key: 'year',
    width: 120,
    render: (row, index) => {
      return h(NSelect, {
        value: row.year,
        'onUpdate:value': (value) => {
          outputValueData.value[index].year = value
        },
        options: yearOptions,
        placeholder: '请选择年份'
      })
    }
  },
  {
    title: '单位',
    key: 'unit',
    width: 100,
    render: (row, index) => {
      return h(NSelect, {
        value: row.unit,
        'onUpdate:value': (value) => {
          outputValueData.value[index].unit = value
        },
        options: outputValueUnitOptions,
        placeholder: '请选择单位'
      })
    }
  },
  {
    title: '年产值',
    key: 'annualOutputValue',
    width: 150,
    render: (row, index) => {
      return h(NInputNumber, {
        value: row.annualOutputValue,
        'onUpdate:value': (value) => {
          outputValueData.value[index].annualOutputValue = value
        },
        placeholder: '请输入年产值',
        min: 0,
        precision: 2
      })
    }
  },
  {
    title: '所得税',
    key: 'incomeTax',
    width: 150,
    render: (row, index) => {
      return h(NInputNumber, {
        value: row.incomeTax,
        'onUpdate:value': (value) => {
          outputValueData.value[index].incomeTax = value
        },
        placeholder: '请输入所得税',
        min: 0,
        precision: 2
      })
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    render: (row, index) => {
      return h(NSpace, [
        h(NButton, {
          size: 'small',
          type: 'error',
          onClick: () => removeOutputValueRow(index)
        }, { default: () => '删除' })
      ])
    }
  }
]

// 方法
const addProductOutputRow = () => {
  productOutputData.value.push({
    type: null,
    mainProduct: null,
    unit: null,
    year: null,
    output: null,
    layers: null
  })
}

const removeProductOutputRow = (index) => {
  productOutputData.value.splice(index, 1)
}

const addQualificationRateRow = () => {
  qualificationRateData.value.push({
    year: null,
    rate: null
  })
}

const removeQualificationRateRow = (index) => {
  qualificationRateData.value.splice(index, 1)
}

const addOutputValueRow = () => {
  outputValueData.value.push({
    year: null,
    unit: 'wan_yuan',
    annualOutputValue: null,
    incomeTax: null
  })
}

const removeOutputValueRow = (index) => {
  outputValueData.value.splice(index, 1)
}

// 确保数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    if (!newVal.productOutput) {
      newVal.productOutput = []
    }
    if (!newVal.qualificationRate) {
      newVal.qualificationRate = []
    }
    if (!newVal.outputValue) {
      newVal.outputValue = []
    }
    
    // 如果表格为空，添加一条空白记录
    if (newVal.productOutput.length === 0) {
      newVal.productOutput.push({
        type: null,
        mainProduct: null,
        unit: null,
        year: null,
        output: null,
        layers: null
      })
    }
    
    if (newVal.qualificationRate.length === 0) {
      newVal.qualificationRate.push({
        year: null,
        rate: null
      })
    }
    
    if (newVal.outputValue.length === 0) {
      newVal.outputValue.push({
        year: null,
        unit: 'wan_yuan',
        annualOutputValue: null,
        incomeTax: null
      })
    }
  }
}, { immediate: true, deep: true })
</script>

<style scoped>
.production-info-form {
  padding: 16px 0;
}

.section {
  margin-bottom: 32px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
  padding-bottom: 8px;
  border-bottom: 2px solid #ff8c00;
}

.data-table {
  margin-bottom: 16px;
}

.empty-state {
  text-align: center;
  padding: 40px 20px;
  color: #999;
}

.empty-state .n-button {
  margin-top: 16px;
}

/* 表格标题加粗 */
:deep(.n-data-table .n-data-table-th) {
  font-weight: 600;
}

/* 表格标题文字加粗 */
:deep(.n-data-table .n-data-table-th .n-data-table-th__content) {
  font-weight: 600;
}
</style>




