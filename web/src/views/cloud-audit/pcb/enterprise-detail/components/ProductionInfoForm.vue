<template>
  <div class="production-info-form">
    <!-- 1. 近三年产品产量 -->
    <div class="section sub-module">
      <div class="section-header">
        <h3 class="section-title">近三年产品产量</h3>
        <n-space>
          <div class="year-range-selector">
            <n-text strong>年份范围：</n-text>
            <n-select
              v-model:value="selectedProductYearRange"
              :options="yearRangeOptions"
              style="width: 200px"
              @update:value="onProductYearRangeChange"
            />
          </div>
          <n-button type="primary" @click="addProductOutputRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加产品产量记录
          </n-button>
        </n-space>
      </div>
      <n-data-table
        :columns="getProductOutputColumns()"
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
      <div class="table-footer">
        <n-button 
          type="primary" 
          @click="submitProductOutput"
          :loading="productOutputSubmitting"
        >
          <template #icon>
            <TheIcon icon="carbon:checkmark" />
          </template>
          提交
        </n-button>
      </div>
          </div>

    <!-- 2. 企业近三年合格率 -->
    <div class="section sub-module">
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
      <div class="table-footer">
        <n-button 
          type="primary" 
          @click="submitQualificationRate"
          :loading="qualificationRateSubmitting"
        >
          <template #icon>
            <TheIcon icon="carbon:checkmark" />
          </template>
          提交
        </n-button>
      </div>
          </div>

    <!-- 3. 企业近三年产值情况 -->
    <div class="section sub-module">
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
      <div class="table-footer">
        <n-button 
          type="primary" 
          @click="submitOutputValue"
          :loading="outputValueSubmitting"
        >
          <template #icon>
            <TheIcon icon="carbon:checkmark" />
          </template>
          提交
        </n-button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, h, onMounted } from 'vue'
import { 
  NDataTable, NButton, NSelect, NInput, NInputNumber, NSpace, NText
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      productOutput: [],
      qualificationRate: [],
      outputValue: []
    })
  },
  enterpriseId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

// 提交状态
const productOutputSubmitting = ref(false)
const qualificationRateSubmitting = ref(false)
const outputValueSubmitting = ref(false)

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

// 年份范围选项（与资源能源消耗模块保持一致）
const yearRangeOptions = [
  { label: '2022-2024', value: '2022-2024' },
  { label: '2021-2023', value: '2021-2023' },
  { label: '2020-2022', value: '2020-2022' }
]

const selectedProductYearRange = ref('2022-2024')

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

// 表格列定义（年份动态列 + 总计）
const getProductOutputColumns = () => {
  const baseColumns = [
    {
      title: '类型',
      key: 'type',
      width: 100,
      render: (row, index) => {
        return h(NSelect, {
          value: row.type,
          'onUpdate:value': (value) => {
            productOutputData.value[index].type = value
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
    }
  ]

  const yearRange = selectedProductYearRange.value.split('-')
  const startYear = parseInt(yearRange[0])
  const endYear = parseInt(yearRange[1])
  const yearColumns = []
  for (let year = startYear; year <= endYear; year++) {
    yearColumns.push({
      title: `${year}年产量`,
      key: `output_${year}`,
      width: 120,
      render: (row, index) => {
        return h(NInputNumber, {
          value: row[`output_${year}`],
          'onUpdate:value': (value) => {
            productOutputData.value[index][`output_${year}`] = value
          },
          placeholder: '请输入产量',
          min: 0,
          precision: 2
        })
      }
    })
  }

  // 层数列需位于单位与年份列之间
  const layersColumn = {
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
  }


  const totalColumn = {
    title: '总计',
    key: 'total',
    width: 120,
    render: (row) => {
      let sum = 0
      for (let year = startYear; year <= endYear; year++) {
        const v = Number(row[`output_${year}`] || 0)
        if (!isNaN(v)) sum += v
      }
      return h('span', sum.toFixed(2))
    }
  }

  const averageColumn = {
    title: '平均产量',
    key: 'average',
    width: 120,
    render: (row) => {
      let sum = 0
      for (let year = startYear; year <= endYear; year++) {
        const v = Number(row[`output_${year}`] || 0)
        if (!isNaN(v)) sum += v
      }
      const avg = sum / 3
      return h('span', avg.toFixed(2))
    }
  }

  const actionColumn = {
    title: '操作',
    key: 'actions',
    width: 100,
    render: (row, index) => {
      return h(NSpace, [
        h(NButton, {
          size: 'small',
          type: 'error',
          onClick: () => removeProductOutputRow(index)
        }, () => '删除')
      ])
    }
  }

  // 顺序：类型、主要产品、单位、层数、[年份列...]、总计、平均产量、操作（年份范围选择器位于表头右上角）
  return [...baseColumns, layersColumn, ...yearColumns, totalColumn, averageColumn, actionColumn]
}

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
        }, () => '删除')
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
        }, () => '删除')
      ])
    }
  }
]

// 方法
const addProductOutputRow = () => {
  const row = {
    type: null,
    mainProduct: null,
    unit: null,
    layers: null
  }
  const [start, end] = selectedProductYearRange.value.split('-').map(y => parseInt(y))
  for (let y = start; y <= end; y++) {
    row[`output_${y}`] = null
  }
  productOutputData.value.push(row)
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
      const [s, e] = selectedProductYearRange.value.split('-').map(y => parseInt(y))
      const init = { type: null, mainProduct: null, unit: null, layers: null }
      for (let y = s; y <= e; y++) init[`output_${y}`] = null
      newVal.productOutput.push(init)
    }
    
    // 初始化时根据年份范围生成合格率与产值的三行并填好年份
    if (newVal.qualificationRate.length === 0 || newVal.qualificationRate.length !== 3) {
      const [s, e] = selectedProductYearRange.value.split('-').map(y => parseInt(y))
      const years = []
      for (let y = s; y <= e; y++) years.push(y.toString())
      newVal.qualificationRate = years.map(y => ({ year: y, rate: null }))
    }
    
    if (newVal.outputValue.length === 0 || newVal.outputValue.length !== 3) {
      const [s2, e2] = selectedProductYearRange.value.split('-').map(y => parseInt(y))
      const years2 = []
      for (let y = s2; y <= e2; y++) years2.push(y.toString())
      newVal.outputValue = years2.map(y => ({ year: y, unit: 'wan_yuan', annualOutputValue: null, incomeTax: null }))
    }
  }
}, { immediate: true, deep: true })

// 事件
const onProductYearRangeChange = async () => {
  // 年份范围变化时，重新获取数据（这样可以确保从后端获取最新数据）
  if (props.enterpriseId) {
    await fetchData()
  } else {
    // 如果没有企业ID，仅更新本地数据结构
  const [start, end] = selectedProductYearRange.value.split('-').map(y => parseInt(y))
  const years = []
  for (let y = start; y <= end; y++) years.push(y.toString())

  // 合格率：构建三行并预填年份，尽量保留已有rate
  const existingRateByYear = new Map((qualificationRateData.value || []).map(r => [r.year, r.rate]))
  const newQualification = years.map(y => ({ year: y, rate: existingRateByYear.get(y) ?? null }))
  qualificationRateData.value = newQualification

  // 产值：构建三行并预填年份，尽量保留已有值与单位
  const existingValueByYear = new Map((outputValueData.value || []).map(r => [r.year, r]))
  const newOutputValue = years.map(y => {
    const prev = existingValueByYear.get(y)
    return {
      year: y,
      unit: prev?.unit ?? 'wan_yuan',
      annualOutputValue: prev?.annualOutputValue ?? null,
      incomeTax: prev?.incomeTax ?? null
    }
  })
  outputValueData.value = newOutputValue
  }
}

// 数据获取功能
const fetchData = async () => {
  if (!props.enterpriseId) return
  
  try {
    const yearRange = selectedProductYearRange.value
    
    // 获取近三年产品产量
    try {
      const productOutputRes = await api.pcb.production.getThreeYearsProductOutput(
        props.enterpriseId, 
        yearRange
      )
      if (productOutputRes && productOutputRes.data && Array.isArray(productOutputRes.data)) {
        // 确保字段名正确映射
        productOutputData.value = productOutputRes.data.map(item => ({
          type: item.type || null,
          mainProduct: item.mainProduct || item.main_product || null,  // 兼容两种字段名
          unit: item.unit || null,
          layers: item.layers || null,
          ...(Object.keys(item).reduce((acc, key) => {
            if (key.startsWith('output_')) {
              acc[key] = item[key]
            }
            return acc
          }, {}))
        }))
      } else {
        // 如果没有数据，保持现有数据或初始化为空数组
        if (!productOutputData.value || productOutputData.value.length === 0) {
          productOutputData.value = []
        }
      }
    } catch (e) {
      console.warn('获取产品产量数据失败:', e)
    }
    
    // 获取近三年合格率
    try {
      const qualificationRateRes = await api.pcb.production.getThreeYearsQualificationRate(
        props.enterpriseId,
        yearRange
      )
      if (qualificationRateRes && qualificationRateRes.data && Array.isArray(qualificationRateRes.data)) {
        qualificationRateData.value = qualificationRateRes.data
      } else {
        // 如果没有数据，根据年份范围初始化
        if (!qualificationRateData.value || qualificationRateData.value.length === 0) {
          const [start, end] = yearRange.split('-').map(y => parseInt(y))
          const years = []
          for (let y = start; y <= end; y++) years.push(y.toString())
          qualificationRateData.value = years.map(y => ({ year: y, rate: null }))
        }
      }
    } catch (e) {
      console.warn('获取合格率数据失败:', e)
    }
    
    // 获取近三年产值
    try {
      const outputValueRes = await api.pcb.production.getThreeYearsOutputValue(
        props.enterpriseId,
        yearRange
      )
      if (outputValueRes && outputValueRes.data && Array.isArray(outputValueRes.data)) {
        // 确保字段名正确映射，并处理数值
        outputValueData.value = outputValueRes.data.map(item => {
          // 处理年产值：确保数值正确
          let annualValue = null
          if (item.annualOutputValue !== null && item.annualOutputValue !== undefined) {
            annualValue = typeof item.annualOutputValue === 'number' ? item.annualOutputValue : parseFloat(item.annualOutputValue)
            if (isNaN(annualValue)) annualValue = null
          } else if (item.annual_output_value !== null && item.annual_output_value !== undefined) {
            annualValue = typeof item.annual_output_value === 'number' ? item.annual_output_value : parseFloat(item.annual_output_value)
            if (isNaN(annualValue)) annualValue = null
          }
          
          // 处理所得税：确保数值正确
          let incomeTaxValue = null
          if (item.incomeTax !== null && item.incomeTax !== undefined) {
            incomeTaxValue = typeof item.incomeTax === 'number' ? item.incomeTax : parseFloat(item.incomeTax)
            if (isNaN(incomeTaxValue)) incomeTaxValue = null
          } else if (item.income_tax !== null && item.income_tax !== undefined) {
            incomeTaxValue = typeof item.income_tax === 'number' ? item.income_tax : parseFloat(item.income_tax)
            if (isNaN(incomeTaxValue)) incomeTaxValue = null
          }
          
          return {
            year: item.year || null,
            unit: item.unit || 'wan_yuan',
            annualOutputValue: annualValue,
            incomeTax: incomeTaxValue
          }
        })
        
        // 如果后端返回的数据不足3条，补充默认数据
        const [start, end] = yearRange.split('-').map(y => parseInt(y))
        const expectedYears = []
        for (let y = start; y <= end; y++) expectedYears.push(y.toString())
        
        // 检查是否所有年份都有数据
        const existingYears = new Set(outputValueData.value.map(item => item.year))
        for (const year of expectedYears) {
          if (!existingYears.has(year)) {
            outputValueData.value.push({
              year: year,
              unit: 'wan_yuan',
              annualOutputValue: null,
              incomeTax: null
            })
          }
        }
        
        // 按年份排序
        outputValueData.value.sort((a, b) => {
          const yearA = parseInt(a.year) || 0
          const yearB = parseInt(b.year) || 0
          return yearA - yearB
        })
      } else {
        // 如果没有数据，根据年份范围初始化
        const [start, end] = yearRange.split('-').map(y => parseInt(y))
        const years = []
        for (let y = start; y <= end; y++) years.push(y.toString())
        outputValueData.value = years.map(y => ({ 
          year: y, 
          unit: 'wan_yuan', 
          annualOutputValue: null, 
          incomeTax: null 
        }))
      }
    } catch (e) {
      console.warn('获取产值数据失败:', e)
      // 如果获取失败，也初始化默认数据
      const [start, end] = selectedProductYearRange.value.split('-').map(y => parseInt(y))
      const years = []
      for (let y = start; y <= end; y++) years.push(y.toString())
      outputValueData.value = years.map(y => ({ 
        year: y, 
        unit: 'wan_yuan', 
        annualOutputValue: null, 
        incomeTax: null 
      }))
    }
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

// 提交产品产量
const submitProductOutput = async () => {
  if (!props.enterpriseId) {
    window.$message.warning('企业ID不能为空')
    return
  }
  
  // 数据验证
  if (!productOutputData.value || productOutputData.value.length === 0) {
    window.$message.warning('请至少添加一条产品产量记录')
    return
  }
  
  // 检查必填字段
  for (const item of productOutputData.value) {
    if (!item.type || !item.mainProduct || !item.unit) {
      window.$message.warning('请完整填写产品类型、主要产品和单位')
      return
    }
  }
  
  try {
    productOutputSubmitting.value = true
    const yearRange = selectedProductYearRange.value
    
    // 转换数据格式，确保字段名正确
    const items = productOutputData.value.map(item => {
      const result = {
        type: item.type,
        main_product: item.mainProduct,
        unit: item.unit,
        layers: item.layers
      }
      // 添加动态年份字段
      const [start, end] = yearRange.split('-').map(y => parseInt(y))
      for (let year = start; year <= end; year++) {
        result[`output_${year}`] = item[`output_${year}`] || null
      }
      return result
    })
    
    await api.pcb.production.saveThreeYearsProductOutput(
      props.enterpriseId,
      yearRange,
      items
    )
    
    window.$message.success('产品产量提交成功')
    
    // 重新获取数据以刷新显示
    await fetchData()
  } catch (error) {
    console.error('提交产品产量失败:', error)
    window.$message.error('提交产品产量失败: ' + (error.message || '未知错误'))
  } finally {
    productOutputSubmitting.value = false
  }
}

// 提交合格率
const submitQualificationRate = async () => {
  if (!props.enterpriseId) {
    window.$message.warning('企业ID不能为空')
    return
  }
  
  // 数据验证
  if (!qualificationRateData.value || qualificationRateData.value.length === 0) {
    window.$message.warning('请至少添加一条合格率记录')
    return
  }
  
  // 检查必填字段
  for (const item of qualificationRateData.value) {
    if (!item.year) {
      window.$message.warning('请完整填写年份')
      return
    }
  }
  
  try {
    qualificationRateSubmitting.value = true
    const yearRange = selectedProductYearRange.value
    
    // 转换数据格式
    const items = qualificationRateData.value.map(item => ({
      year: item.year,
      rate: item.rate || null
    }))
    
    await api.pcb.production.saveThreeYearsQualificationRate(
      props.enterpriseId,
      yearRange,
      items
    )
    
    window.$message.success('合格率提交成功')
    
    // 重新获取数据以刷新显示
    await fetchData()
  } catch (error) {
    console.error('提交合格率失败:', error)
    window.$message.error('提交合格率失败: ' + (error.message || '未知错误'))
  } finally {
    qualificationRateSubmitting.value = false
  }
}

// 提交产值
const submitOutputValue = async () => {
  if (!props.enterpriseId) {
    window.$message.warning('企业ID不能为空')
    return
  }
  
  // 数据验证
  if (!outputValueData.value || outputValueData.value.length === 0) {
    window.$message.warning('请至少添加一条产值记录')
    return
  }
  
  // 检查必填字段
  for (const item of outputValueData.value) {
    if (!item.year || !item.unit) {
      window.$message.warning('请完整填写年份和单位')
      return
    }
  }
  
  try {
    outputValueSubmitting.value = true
    const yearRange = selectedProductYearRange.value
    
    // 先打印原始数据
    console.log('提交前 - outputValueData.value:', JSON.parse(JSON.stringify(outputValueData.value)))
    
    // 转换数据格式 - 重要：使用 ?? 而不是 ||，因为0是有效值
    const items = outputValueData.value.map((item, idx) => {
      // 处理年产值：0是有效值，只有null/undefined才转为null
      let annualValue = item.annualOutputValue
      console.log(`处理第${idx}条数据 - 原始annualOutputValue:`, annualValue, '类型:', typeof annualValue)
      
      if (annualValue === '' || annualValue === undefined) {
        annualValue = null
      } else if (annualValue !== null && annualValue !== undefined) {
        // 确保是数字类型
        annualValue = typeof annualValue === 'number' ? annualValue : parseFloat(annualValue)
        if (isNaN(annualValue)) annualValue = null
      }
      
      // 处理所得税：0是有效值，只有null/undefined才转为null
      let incomeTax = item.incomeTax
      console.log(`处理第${idx}条数据 - 原始incomeTax:`, incomeTax, '类型:', typeof incomeTax)
      
      if (incomeTax === '' || incomeTax === undefined) {
        incomeTax = null
      } else if (incomeTax !== null && incomeTax !== undefined) {
        // 确保是数字类型
        incomeTax = typeof incomeTax === 'number' ? incomeTax : parseFloat(incomeTax)
        if (isNaN(incomeTax)) incomeTax = null
      }
      
      const result = {
        year: item.year,
        unit: item.unit,
        annualOutputValue: annualValue,
        incomeTax: incomeTax
      }
      console.log(`处理后的第${idx}条数据:`, result)
      return result
    })
    
    console.log('提交产值数据（最终）:', JSON.stringify(items, null, 2))  // 调试日志
    
    const response = await api.pcb.production.saveThreeYearsOutputValue(
      props.enterpriseId,
      yearRange,
      items
    )
    
    console.log('保存产值响应:', response)  // 调试日志
    
    window.$message.success('产值提交成功')
    
    // 延迟一下再获取数据，确保数据库已更新
    await new Promise(resolve => setTimeout(resolve, 300))
    
    // 重新获取数据以刷新显示
    await fetchData()
    
    console.log('刷新后的产值数据:', outputValueData.value)  // 调试日志
  } catch (error) {
    console.error('提交产值失败:', error)
    window.$message.error('提交产值失败: ' + (error.message || '未知错误'))
  } finally {
    outputValueSubmitting.value = false
  }
}

onMounted(async () => {
  // 首次挂载时，同步年份到其他两个模块并获取数据
  await onProductYearRangeChange()
})
</script>

<style scoped>
.production-info-form {
  padding: 16px 0;
}

.section {
  margin-bottom: 32px;
  padding: 16px;
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
  display: inline-block;
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

/* 表格模块样式 */
.sub-module {
  border: 1px solid #e0e0e6;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.sub-module:hover {
  border-color: #18a058;
  box-shadow: 0 2px 8px rgba(24, 160, 88, 0.15);
}

/* 表标题样式 */
.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin: 0;
  padding-bottom: 8px;
  display: inline-block;
  border-bottom: 2px solid #ff8c00;
}

/* 表格底部提交按钮样式 */
.table-footer {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  padding: 12px 0;
  margin-top: 8px;
}
</style>




