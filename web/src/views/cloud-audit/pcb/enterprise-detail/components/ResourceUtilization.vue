<template>
  <div class="resource-utilization">
    <n-space vertical :size="24">
      <!-- 能源消耗表格 -->
      <n-card title="能源消耗" size="small" class="sub-module">
        <template #header-extra>
          <n-button tertiary size="small" class="mr-2" @click="showStandardModal = true">
            判断标准
          </n-button>
          <n-button type="primary" size="small" @click="addEnergyRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            新增行
          </n-button>
        </template>
        <n-data-table
          :columns="energyColumns"
          :data="energyData"
          :pagination="false"
          :bordered="true"
          size="small"
          :loading="loadingEnergy"
        />
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingEnergy"
              @click="submitEnergyData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
        <n-modal v-model:show="showStandardModal" preset="card" title="单位产品电耗判断标准" :style="{ width: '900px' }">
          <n-data-table :columns="standardColumns" :data="standardData" :pagination="false" size="small" />
        </n-modal>
      </n-card>

      <!-- 1. 新鲜水耗表格 -->
      <n-card title="新鲜水耗" size="small" class="sub-module">
        <template #header-extra>
          <n-button tertiary size="small" class="mr-2" @click="showFreshWaterStandardModal = true">
            判断标准
          </n-button>
          <n-button type="primary" size="small" @click="addFreshWaterRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            新增行
          </n-button>
        </template>
        <n-data-table
          :columns="freshWaterColumns"
          :data="freshWaterData"
          :pagination="false"
          :bordered="true"
          size="small"
          :loading="loadingFreshWater"
        />
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingFreshWater"
              @click="submitFreshWaterData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
        <n-modal v-model:show="showFreshWaterStandardModal" preset="card" title="单位产品耗水判断标准" :style="{ width: '900px' }">
          <n-data-table :columns="waterStandardColumns" :data="freshWaterStandardData" :pagination="false" size="small" />
        </n-modal>
      </n-card>

      <!-- 2. 废水总量表格 -->
      <n-card title="废水总量" size="small" class="sub-module">
        <template #header-extra>
          <n-button tertiary size="small" class="mr-2" @click="showWastewaterTotalStandardModal = true">
            判断标准
          </n-button>
          <n-button type="primary" size="small" @click="addWastewaterTotalRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            新增行
          </n-button>
        </template>
        <n-data-table
          :columns="wastewaterTotalColumns"
          :data="wastewaterTotalData"
          :pagination="false"
          :bordered="true"
          size="small"
          :loading="loadingWastewaterTotal"
        />
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingWastewaterTotal"
              @click="submitWastewaterTotalData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
        <n-modal v-model:show="showWastewaterTotalStandardModal" preset="card" title="废水产生量判断标准" :style="{ width: '900px' }">
          <n-data-table :columns="waterStandardColumns" :data="wastewaterTotalStandardData" :pagination="false" size="small" />
        </n-modal>
      </n-card>

      <!-- 3. 废水中总铜浓度表格 -->
      <n-card title="废水中总铜浓度" size="small" class="sub-module">
        <template #header-extra>
          <n-button tertiary size="small" class="mr-2" @click="showWastewaterCuStandardModal = true">
            判断标准
          </n-button>
          <n-button type="primary" size="small" @click="addWastewaterCuRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            新增行
          </n-button>
        </template>
        <n-data-table
          :columns="wastewaterCuColumns"
          :data="wastewaterCuData"
          :pagination="false"
          :bordered="true"
          size="small"
          :loading="loadingWastewaterCu"
        />
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingWastewaterCu"
              @click="submitWastewaterCuData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
        <n-modal v-model:show="showWastewaterCuStandardModal" preset="card" title="废水中铜产生量判断标准" :style="{ width: '900px' }">
          <n-data-table :columns="waterStandardColumns" :data="wastewaterCuStandardData" :pagination="false" size="small" />
        </n-modal>
      </n-card>

      <!-- 4. 废水中COD浓度表格 -->
      <n-card title="废水中COD浓度" size="small" class="sub-module">
        <template #header-extra>
          <n-button tertiary size="small" class="mr-2" @click="showWastewaterCODStandardModal = true">
            判断标准
          </n-button>
          <n-button type="primary" size="small" @click="addWastewaterCODRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            新增行
          </n-button>
        </template>
        <n-data-table
          :columns="wastewaterCODColumns"
          :data="wastewaterCODData"
          :pagination="false"
          :bordered="true"
          size="small"
          :loading="loadingWastewaterCOD"
        />
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingWastewaterCOD"
              @click="submitWastewaterCODData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
        <n-modal v-model:show="showWastewaterCODStandardModal" preset="card" title="废水中COD产生量判断标准" :style="{ width: '900px' }">
          <n-data-table :columns="waterStandardColumns" :data="wastewaterCODStandardData" :pagination="false" size="small" />
        </n-modal>
      </n-card>

      <!-- 5. 原/辅料消耗（覆铜板利用率） -->
      <n-card title="原/辅料消耗（覆铜板）" size="small" class="sub-module">
        <template #header-extra>
          <n-button tertiary size="small" class="mr-2" @click="showRawMatStandardModal = true">
            判断标准
          </n-button>
          <n-button type="primary" size="small" @click="addRawMatRow">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            新增行
          </n-button>
        </template>
        <n-data-table
          :columns="rawMaterialColumns"
          :data="rawMaterialData"
          :pagination="false"
          :bordered="true"
          size="small"
          :loading="loadingRawMaterial"
        />
        <template #footer>
          <div style="text-align: left; padding-top: 16px;">
            <n-button 
              type="primary" 
              :loading="loadingRawMaterial"
              @click="submitRawMaterialData"
            >
              <template #icon>
                <TheIcon icon="carbon:checkmark" />
              </template>
              提交
            </n-button>
          </div>
        </template>
        <n-modal v-model:show="showRawMatStandardModal" preset="card" title="覆铜板利用率判断标准" :style="{ width: '980px' }">
          <n-data-table :columns="rawMatStandardColumns" :data="rawMatStandardData" :pagination="false" size="small" />
        </n-modal>
      </n-card>
    </n-space>
  </div>
</template>

<script setup>
import { ref, computed, h, onMounted, watch } from 'vue'
import { NCard, NDataTable, NSelect, NInputNumber, NSpace, NButton, NRadioGroup, NRadio, NModal, useMessage } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api/pcb'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      energyConsumption: [],
      freshWaterConsumption: [],
      wastewaterTotalConsumption: [],
      wastewaterCuConsumption: [],
      wastewaterCODConsumption: [],
      rawMaterialConsumption: []
    })
  },
  enterpriseId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])
const message = useMessage()

// Loading状态
const loadingEnergy = ref(false)
const loadingFreshWater = ref(false)
const loadingWastewaterTotal = ref(false)
const loadingWastewaterCu = ref(false)
const loadingWastewaterCOD = ref(false)
const loadingRawMaterial = ref(false)

// 枚举选项（与1.企业总体生产情况一致）
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

const layerOptions = Array.from({ length: 30 }, (_, i) => ({
  label: `${i + 1}层`,
  value: i + 1
}))

// 评定等级选项
const ratingLevelOptions = [
  { label: 'Ⅰ级', value: 'level1' },
  { label: 'Ⅱ级', value: 'level2' },
  { label: 'Ⅲ级', value: 'level3' },
  { label: '均不符合', value: 'none' }
]

// 数据
const energyData = computed({
  get: () => props.modelValue?.energyConsumption || [],
  set: (value) => {
    const next = { ...(props.modelValue || {}), energyConsumption: value }
    emit('update:modelValue', next)
  }
})

// 水资源消耗数据
const waterData = computed({
  get: () => props.modelValue?.waterConsumption || [],
  set: (value) => {
    const next = { ...(props.modelValue || {}), waterConsumption: value }
    emit('update:modelValue', next)
  }
})

// 判断标准弹窗
const showStandardModal = ref(false)
const standardColumns = [
  { title: '序号', key: 'idx', width: 70 },
  { title: '指标', key: 'indicator', width: 200 },
  { title: '类型', key: 'type', width: 160 },
  { title: '单位', key: 'unit', width: 90 },
  { title: 'Ⅰ级', key: 'level1', width: 160 },
  { title: 'Ⅱ级', key: 'level2', width: 160 },
  { title: 'Ⅲ级', key: 'level3', width: 160 }
]
const standardData = [
  { idx: 7, indicator: '单位产品电耗 (刚性印制电路)', type: '单面板', unit: 'kWh/m²', level1: '≤5', level2: '≤10', level3: '≤25' },
  { idx: 8, indicator: '单位产品电耗 (刚性印制电路)', type: '双面板', unit: 'kWh/m²', level1: '≤10', level2: '≤20', level3: '≤50' },
  { idx: 9, indicator: '单位产品电耗 (刚性印制电路)', type: '多层板 (2+n) 层', unit: 'kWh/m²', level1: '≤ (10+5n)', level2: '≤ (25+10n)', level3: '≤ (55+5n)' },
  { idx: 10, indicator: '单位产品电耗 (挠性/刚挠结合)', type: 'HDI板 (2+n) 层', unit: 'kWh/m²', level1: '≤ (15+10n)', level2: '≤ (30+20n)', level3: '≤ (75+4n)' },
  { idx: 11, indicator: '单位产品电耗 (挠性/刚挠结合)', type: '单面板', unit: 'kWh/m²', level1: '≤10', level2: '≤15', level3: '≤35' },
  { idx: 12, indicator: '单位产品电耗 (挠性/刚挠结合)', type: '双面板', unit: 'kWh/m²', level1: '≤15', level2: '≤25', level3: '≤65' },
  { idx: 13, indicator: '单位产品电耗 (挠性/刚挠结合)', type: '多层板 (2+n) 层', unit: 'kWh/m²', level1: '≤ (15+5n)', level2: '≤ (35+10n)', level3: '≤ (65+5n)' },
  { idx: 14, indicator: '单位产品电耗 (挠性/刚挠结合)', type: 'HDI板 (2+n) 层', unit: 'kWh/m²', level1: '≤ (25+10n)', level2: '≤ (35+20n)', level3: '≤ (75+4n)' }
]

// 计算单位产品消耗量（保留四位有效数字）
const calculateUnitConsumption = (output, electricity) => {
  if (!output || !electricity || output <= 0 || electricity <= 0) {
    return ''
  }
  const result = electricity / output
  // 保留四位有效数字
  if (result === 0) return '0'
  const magnitude = Math.floor(Math.log10(Math.abs(result)))
  const factor = Math.pow(10, 3 - magnitude)
  const rounded = Math.round(result * factor) / factor
  // 格式化输出，确保显示足够的小数位
  const decimalPlaces = Math.max(0, 3 - magnitude)
  return rounded.toFixed(decimalPlaces)
}

const calcByOutput = (total, output) => {
  if (!output || !total || output <= 0 || total <= 0) return ''
  const result = total / output
  if (result === 0) return '0'
  const magnitude = Math.floor(Math.log10(Math.abs(result)))
  const factor = Math.pow(10, 3 - magnitude)
  const rounded = Math.round(result * factor) / factor
  const decimalPlaces = Math.max(0, 3 - magnitude)
  return rounded.toFixed(decimalPlaces)
}

// 按公式：浓度 × 废水总量 / 产量（四位有效数字）
const calcByConcTotalOutput = (concentration, total, output) => {
  if (!output || !concentration || !total || output <= 0 || concentration <= 0 || total <= 0) return ''
  const result = (concentration * total) / output
  if (result === 0) return '0'
  const magnitude = Math.floor(Math.log10(Math.abs(result)))
  const factor = Math.pow(10, 3 - magnitude)
  const rounded = Math.round(result * factor) / factor
  const decimalPlaces = Math.max(0, 3 - magnitude)
  return rounded.toFixed(decimalPlaces)
}

// 覆铜板利用率（两位有效数字，百分比显示）
// 计算公式：产量/覆铜板消耗量 × 100
const calcPercentTwoSig = (consumption, output) => {
  if (!output || !consumption || output <= 0 || consumption <= 0) return ''
  const ratio = output / consumption * 100  // 修改为：产量/消耗量 × 100
  if (ratio === 0) return '0%'
  const magnitude = Math.floor(Math.log10(Math.abs(ratio)))
  const factor = Math.pow(10, 1 - magnitude)
  const rounded = Math.round(ratio * factor) / factor
  const decimalPlaces = Math.max(0, 1 - magnitude)
  return `${rounded.toFixed(decimalPlaces)}%`
}

// 表格列定义
const energyColumns = computed(() => [
  {
    title: '类型',
    key: 'type',
    width: 100,
    render: (row, index) => {
      return h(NSelect, {
        value: row.type,
        'onUpdate:value': (value) => {
          energyData.value[index].type = value
          energyData.value[index].mainProduct = null
          energyData.value[index].layers = null
        },
        options: typeOptions,
        placeholder: '请选择类型'
      })
    }
  },
  {
    title: '产品名称',
    key: 'mainProduct',
    width: 150,
    render: (row, index) => {
      const options = row.type === 'rigid' ? rigidProductOptions : flexibleProductOptions
      return h(NSelect, {
        value: row.mainProduct,
        'onUpdate:value': (value) => {
          energyData.value[index].mainProduct = value
          const selectedProduct = options.find(opt => opt.value === value)
          if (selectedProduct && selectedProduct.defaultLayers) {
            energyData.value[index].layers = selectedProduct.defaultLayers
          } else {
            energyData.value[index].layers = null
          }
        },
        options: options,
        placeholder: '请选择产品',
        disabled: !row.type
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
          energyData.value[index].layers = value
        },
        options: layerOptions,
        placeholder: '请选择层数',
        disabled: !row.mainProduct || (selectedProduct && selectedProduct.defaultLayers)
      })
    }
  },
  {
    title: '产量（m²）',
    key: 'output',
    width: 130,
    render: (row, index) => {
      return h(NInputNumber, {
        value: row.output,
        'onUpdate:value': (value) => {
          energyData.value[index].output = value
        },
        placeholder: '请输入产量',
        min: 0,
        precision: 2,
        showButton: false
      })
    }
  },
  {
    title: '耗电量',
    key: 'electricity',
    width: 130,
    render: (row, index) => {
      return h(NInputNumber, {
        value: row.electricity,
        'onUpdate:value': (value) => {
          energyData.value[index].electricity = value
        },
        placeholder: '请输入耗电量',
        min: 0,
        precision: 2,
        showButton: false
      })
    }
  },
  {
    title: '单位产品消耗量',
    key: 'unitConsumption',
    width: 150,
    render: (row) => {
      const result = calculateUnitConsumption(row.output, row.electricity)
      return h('span', result || '-')
    }
  },
  {
    title: '评定等级',
    key: 'rating',
    width: 220,
    render: (row, index) => {
      return h(NRadioGroup, {
        value: row.rating || null,
        'onUpdate:value': (value) => {
          energyData.value[index].rating = value
        }
      }, {
        default: () => h(NSpace, { vertical: true }, {
          default: () => [
            h(NRadio, { value: 'level1' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅰ级') }),
            h(NRadio, { value: 'level2' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅱ级') }),
            h(NRadio, { value: 'level3' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅲ级') }),
            h(NRadio, { value: 'none' }, { default: () => h('span', { style: 'font-weight:700;' }, '均不符合') })
          ]
        })
      })
    }
  },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    render: (row, index) => {
      return h(NButton, {
        type: 'error',
        size: 'small',
        onClick: () => {
          energyData.value = energyData.value.filter((_, i) => i !== index)
        }
      }, {
        default: () => '删除'
      })
    }
  }
])

// 新增行
const addEnergyRow = () => {
  const cur = Array.isArray(energyData.value) ? energyData.value : []
  energyData.value = [
    ...cur,
    {
      type: null,
      mainProduct: null,
      layers: null,
      output: null,
      electricity: null,
      rating: null
    }
  ]
}

// ================= 水资源消耗 =================
const waterProductOptions = [
  { label: '单面板', value: 'single', defaultLayers: 1 },
  { label: '双面板', value: 'double', defaultLayers: 2 },
  { label: '多层板 (2+n) 层', value: 'multilayer', defaultLayers: null },
  { label: 'HDI板 (2+n) 层', value: 'hdi', defaultLayers: null }
]

// 四个独立表格的数据
const freshWaterData = computed({
  get: () => props.modelValue?.freshWaterConsumption || [],
  set: (value) => {
    const next = { ...(props.modelValue || {}), freshWaterConsumption: value }
    emit('update:modelValue', next)
  }
})

const wastewaterTotalData = computed({
  get: () => props.modelValue?.wastewaterTotalConsumption || [],
  set: (value) => {
    const next = { ...(props.modelValue || {}), wastewaterTotalConsumption: value }
    emit('update:modelValue', next)
  }
})

const wastewaterCuData = computed({
  get: () => props.modelValue?.wastewaterCuConsumption || [],
  set: (value) => {
    const next = { ...(props.modelValue || {}), wastewaterCuConsumption: value }
    emit('update:modelValue', next)
  }
})

const wastewaterCODData = computed({
  get: () => props.modelValue?.wastewaterCODConsumption || [],
  set: (value) => {
    const next = { ...(props.modelValue || {}), wastewaterCODConsumption: value }
    emit('update:modelValue', next)
  }
})

// 原/辅料消耗（覆铜板）数据
const rawMaterialData = computed({
  get: () => props.modelValue?.rawMaterialConsumption || [],
  set: (value) => {
    const next = { ...(props.modelValue || {}), rawMaterialConsumption: value }
    emit('update:modelValue', next)
  }
})

// 标准弹窗
const showFreshWaterStandardModal = ref(false)
const showWastewaterTotalStandardModal = ref(false)
const showWastewaterCuStandardModal = ref(false)
const showWastewaterCODStandardModal = ref(false)

// 标准表格列
const waterStandardColumns = [
  { title: '序号', key: 'idx', width: 70 },
  { title: '产品类型', key: 'type', width: 160 },
  { title: '单位', key: 'unit', width: 90 },
  { title: 'Ⅰ级', key: 'level1', width: 160 },
  { title: 'Ⅱ级', key: 'level2', width: 160 },
  { title: 'Ⅲ级', key: 'level3', width: 160 }
]

// 单位产品耗水标准
const freshWaterStandardData = [
  { idx: 15, type: '单面板', unit: 'm³/m²', level1: '≤0.05', level2: '≤0.07', level3: '≤0.11' },
  { idx: 16, type: '双面板', unit: 'm³/m²', level1: '≤0.14', level2: '≤0.23', level3: '≤0.4' },
  { idx: 17, type: '多层板 (2+n) 层', unit: 'm³/m²', level1: '≤(0.14+0.08n)', level2: '≤(0.23+0.12n)', level3: '≤(0.39+0.15n)' },
  { idx: 18, type: 'HDI板 (2+n) 层', unit: 'm³/m²', level1: '≤(0.16+0.14n)', level2: '≤(0.25+0.18n)', level3: '≤(0.39+0.24n)' }
]

// 废水产生量标准
const wastewaterTotalStandardData = [
  { idx: 30, type: '单面板', unit: 'm³/m²', level1: '≤0.04', level2: '≤0.06', level3: '≤0.09' },
  { idx: 31, type: '双面板', unit: 'm³/m²', level1: '≤0.11', level2: '≤0.22', level3: '≤0.36' },
  { idx: 32, type: '多层板 (2+n) 层', unit: 'm³/m²', level1: '≤(0.11+0.08n)', level2: '≤(0.22+0.11n)', level3: '≤(0.36+0.14n)' },
  { idx: 33, type: 'HDI板 (2+n) 层', unit: 'm³/m²', level1: '≤(0.13+0.13n)', level2: '≤(0.24+0.16n)', level3: '≤(0.36+0.22n)' }
]

// 废水中铜产生量标准
const wastewaterCuStandardData = [
  { idx: 34, type: '单面板', unit: 'g/m²', level1: '≤4', level2: '≤20', level3: '≤50' },
  { idx: 35, type: '双面板', unit: 'g/m²', level1: '≤8', level2: '≤25', level3: '≤60' },
  { idx: 36, type: '多层板 (2+n) 层', unit: 'g/m²', level1: '≤(8+2n)', level2: '≤(20+4n)', level3: '≤(50+8n)' },
  { idx: 37, type: 'HDI板 (2+n) 层', unit: 'g/m²', level1: '≤(10+3n)', level2: '≤(25+5n)', level3: '≤(60+10n)' }
]

// 废水中COD产生量标准（根据用户表格补充，暂用铜的格式）
const wastewaterCODStandardData = [
  { idx: 38, type: '单面板', unit: 'g/m²', level1: '≤10', level2: '≤25', level3: '≤60' },
  { idx: 39, type: '双面板', unit: 'g/m²', level1: '≤15', level2: '≤35', level3: '≤80' },
  { idx: 40, type: '多层板 (2+n) 层', unit: 'g/m²', level1: '≤(15+3n)', level2: '≤(35+5n)', level3: '≤(80+10n)' },
  { idx: 41, type: 'HDI板 (2+n) 层', unit: 'g/m²', level1: '≤(20+4n)', level2: '≤(40+8n)', level3: '≤(90+15n)' }
]

// 覆铜板利用率标准
const rawMatStandardColumns = [
  { title: '序号', key: 'idx', width: 70 },
  { title: '一级指标', key: 'primary', width: 180 },
  { title: '二级指标', key: 'secondary', width: 260 },
  { title: '产品类型', key: 'type', width: 160 },
  { title: '单位', key: 'unit', width: 70 },
  { title: '限值 1', key: 'limit1', width: 140 },
  { title: '限值 2', key: 'limit2', width: 140 },
  { title: '限值 3', key: 'limit3', width: 140 }
]

const rawMatStandardData = [
  { idx: 20, primary: '原/辅料消耗 (0.1)', secondary: '覆铜板利用率 (刚性印制电路) (1)', type: '单面板', unit: '%', limit1: '≥94', limit2: '≥88', limit3: '≥85' },
  { idx: 21, primary: '原/辅料消耗 (0.1)', secondary: '覆铜板利用率 (刚性印制电路) (1)', type: '双面板', unit: '%', limit1: '≥90', limit2: '≥82', limit3: '≥80' },
  { idx: 22, primary: '原/辅料消耗 (0.1)', secondary: '覆铜板利用率 (刚性印制电路) (1)', type: '多层板 (2+n) 层', unit: '%', limit1: '≥(90+2n)', limit2: '≥(82+3n)', limit3: '≥(80+5n)' },
  { idx: 23, primary: '原/辅料消耗 (0.1)', secondary: '覆铜板利用率 (刚性印制电路) (1)', type: 'HDI板 (2+n) 层', unit: '%', limit1: '≥(80+2n)', limit2: '≥(78+3n)', limit3: '≥(75+4n)' },
  { idx: 24, primary: '原/辅料消耗 (0.1)', secondary: '覆铜板利用率 (挠性/刚挠结合) (1)', type: '单面板', unit: '%', limit1: '≥85', limit2: '≥80', limit3: '≥72' },
  { idx: 25, primary: '原/辅料消耗 (0.1)', secondary: '覆铜板利用率 (挠性/刚挠结合) (1)', type: '双面板', unit: '%', limit1: '≥80', limit2: '≥72', limit3: '≥66' },
  { idx: 26, primary: '原/辅料消耗 (0.1)', secondary: '覆铜板利用率 (挠性/刚挠结合) (1)', type: '多层板 (2+n) 层', unit: '%', limit1: '≥(80+2n)', limit2: '≥(72+3n)', limit3: '≥(66+5n)' },
  { idx: 27, primary: '原/辅料消耗 (0.1)', secondary: '覆铜板利用率 (挠性/刚挠结合) (1)', type: 'HDI板 (2+n) 层', unit: '%', limit1: '≥(80+2n)', limit2: '≥(72+3n)', limit3: '≥(66+5n)' }
]

// 通用的基础列定义函数
const createWaterBaseColumns = (dataRef, totalFieldName, totalFieldLabel, unitFieldLabel, unitCalcFieldLabel) => {
  return [
    {
      title: '产品名称',
      key: 'product',
      width: 160,
      render: (row, index) => h(NSelect, {
        value: row.product,
        'onUpdate:value': (value) => {
          dataRef.value[index].product = value
          const selected = waterProductOptions.find(o => o.value === value)
          if (selected && selected.defaultLayers) {
            dataRef.value[index].layers = selected.defaultLayers
          } else {
            dataRef.value[index].layers = null
          }
        },
        options: waterProductOptions,
        placeholder: '请选择产品'
      })
    },
    {
      title: '层数',
      key: 'layers',
      width: 100,
      render: (row, index) => {
        const selected = waterProductOptions.find(o => o.value === row.product)
        if (selected && selected.defaultLayers) {
          return h('span', `${selected.defaultLayers}层`)
        }
        return h(NInputNumber, {
          value: row.layers,
          'onUpdate:value': (value) => { dataRef.value[index].layers = value },
          min: 1,
          precision: 0,
          showButton: false,
          placeholder: '请输入层数',
          disabled: !row.product
        })
      }
    },
    {
      title: '产量（m²）',
      key: 'output',
      width: 130,
      render: (row, index) => h(NInputNumber, {
        value: row.output,
        'onUpdate:value': (value) => { dataRef.value[index].output = value },
        min: 0,
        precision: 2,
        showButton: false,
        placeholder: '请输入产量'
      })
    },
    {
      title: totalFieldLabel,
      key: totalFieldName,
      width: 180,
      render: (row, index) => h(NInputNumber, {
        value: row[totalFieldName],
        'onUpdate:value': (value) => { dataRef.value[index][totalFieldName] = value },
        min: 0,
        precision: 4,
        showButton: false,
        placeholder: '请输入'
      })
    },
    {
      title: unitCalcFieldLabel,
      key: `unit${totalFieldName}`,
      width: 220,
      render: (row) => h('span', { style: 'font-weight: 600;' }, calcByOutput(row[totalFieldName], row.output) || '-')
    },
    {
      title: '评定等级',
      key: 'rating',
      width: 220,
      render: (row, index) => {
        return h(NRadioGroup, {
          value: row.rating || null,
          'onUpdate:value': (value) => {
            dataRef.value[index].rating = value
          }
        }, {
          default: () => h(NSpace, { vertical: true }, {
            default: () => [
              h(NRadio, { value: 'level1' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅰ级') }),
              h(NRadio, { value: 'level2' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅱ级') }),
              h(NRadio, { value: 'level3' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅲ级') }),
              h(NRadio, { value: 'none' }, { default: () => h('span', { style: 'font-weight:700;' }, '均不符合') })
            ]
          })
        })
      }
    },
    {
      title: '操作',
      key: 'actions',
      width: 100,
      render: (row, index) => h(NButton, {
        type: 'error',
        size: 'small',
        onClick: () => {
          dataRef.value = dataRef.value.filter((_, i) => i !== index)
        }
      }, { default: () => '删除' })
    }
  ]
}

// 四个表格的列定义
const freshWaterColumns = computed(() => createWaterBaseColumns(
  freshWaterData,
  'freshWater',
  '新鲜水耗（m³）',
  'm³',
  '单位产品新鲜水耗（m³/m²）'
))

const wastewaterTotalColumns = computed(() => createWaterBaseColumns(
  wastewaterTotalData,
  'wastewaterTotal',
  '废水总量（m³）',
  'm³',
  '单位产品废水量（m³/m²）'
))

const wastewaterCuColumns = computed(() => [
  {
    title: '产品名称', key: 'product', width: 160,
    render: (row, index) => h(NSelect, {
      value: row.product,
      'onUpdate:value': (value) => {
        wastewaterCuData.value[index].product = value
        const selected = waterProductOptions.find(o => o.value === value)
        if (selected && selected.defaultLayers) {
          wastewaterCuData.value[index].layers = selected.defaultLayers
        } else {
          wastewaterCuData.value[index].layers = null
        }
      },
      options: waterProductOptions,
      placeholder: '请选择产品'
    })
  },
  {
    title: '层数', key: 'layers', width: 100,
    render: (row, index) => {
      const selected = waterProductOptions.find(o => o.value === row.product)
      if (selected && selected.defaultLayers) return h('span', `${selected.defaultLayers}层`)
      return h(NInputNumber, {
        value: row.layers,
        'onUpdate:value': (value) => { wastewaterCuData.value[index].layers = value },
        min: 1, precision: 0, showButton: false, placeholder: '请输入层数', disabled: !row.product
      })
    }
  },
  {
    title: '产量（m²）', key: 'output', width: 130,
    render: (row, index) => h(NInputNumber, {
      value: row.output,
      'onUpdate:value': (value) => { wastewaterCuData.value[index].output = value },
      min: 0, precision: 2, showButton: false, placeholder: '请输入产量'
    })
  },
  {
    title: '废水总量（m³）', key: 'wastewaterTotal', width: 160,
    render: (row, index) => h(NInputNumber, {
      value: row.wastewaterTotal,
      'onUpdate:value': (value) => { wastewaterCuData.value[index].wastewaterTotal = value },
      min: 0, precision: 4, showButton: false, placeholder: '请输入'
    })
  },
  {
    title: '废水中总铜浓度（g/m³）', key: 'wastewaterCu', width: 180,
    render: (row, index) => h(NInputNumber, {
      value: row.wastewaterCu,
      'onUpdate:value': (value) => { wastewaterCuData.value[index].wastewaterCu = value },
      min: 0, precision: 4, showButton: false, placeholder: '请输入'
    })
  },
  {
    title: '单位产品废水铜产生量（g/m²）', key: 'unitWastewaterCu', width: 240,
    render: (row) => h('span', { style: 'font-weight: 600;' },
      calcByConcTotalOutput(row.wastewaterCu, row.wastewaterTotal, row.output) || '-')
  },
  {
    title: '评定等级', key: 'rating', width: 220,
    render: (row, index) => h(NRadioGroup, {
      value: row.rating || null,
      'onUpdate:value': (value) => { wastewaterCuData.value[index].rating = value }
    }, {
      default: () => h(NSpace, { vertical: true }, {
        default: () => [
          h(NRadio, { value: 'level1' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅰ级') }),
          h(NRadio, { value: 'level2' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅱ级') }),
          h(NRadio, { value: 'level3' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅲ级') }),
          h(NRadio, { value: 'none' }, { default: () => h('span', { style: 'font-weight:700;' }, '均不符合') })
        ]
      })
    })
  },
  {
    title: '操作', key: 'actions', width: 100,
    render: (row, index) => h(NButton, { type: 'error', size: 'small', onClick: () => {
      wastewaterCuData.value = wastewaterCuData.value.filter((_, i) => i !== index)
    } }, { default: () => '删除' })
  }
])

const wastewaterCODColumns = computed(() => [
  {
    title: '产品名称', key: 'product', width: 160,
    render: (row, index) => h(NSelect, {
      value: row.product,
      'onUpdate:value': (value) => {
        wastewaterCODData.value[index].product = value
        const selected = waterProductOptions.find(o => o.value === value)
        if (selected && selected.defaultLayers) {
          wastewaterCODData.value[index].layers = selected.defaultLayers
        } else {
          wastewaterCODData.value[index].layers = null
        }
      },
      options: waterProductOptions,
      placeholder: '请选择产品'
    })
  },
  {
    title: '层数', key: 'layers', width: 100,
    render: (row, index) => {
      const selected = waterProductOptions.find(o => o.value === row.product)
      if (selected && selected.defaultLayers) return h('span', `${selected.defaultLayers}层`)
      return h(NInputNumber, {
        value: row.layers,
        'onUpdate:value': (value) => { wastewaterCODData.value[index].layers = value },
        min: 1, precision: 0, showButton: false, placeholder: '请输入层数', disabled: !row.product
      })
    }
  },
  {
    title: '产量（m²）', key: 'output', width: 130,
    render: (row, index) => h(NInputNumber, {
      value: row.output,
      'onUpdate:value': (value) => { wastewaterCODData.value[index].output = value },
      min: 0, precision: 2, showButton: false, placeholder: '请输入产量'
    })
  },
  {
    title: '废水总量（m³）', key: 'wastewaterTotal', width: 160,
    render: (row, index) => h(NInputNumber, {
      value: row.wastewaterTotal,
      'onUpdate:value': (value) => { wastewaterCODData.value[index].wastewaterTotal = value },
      min: 0, precision: 4, showButton: false, placeholder: '请输入'
    })
  },
  {
    title: '废水中COD浓度（g/m³）', key: 'wastewaterCOD', width: 180,
    render: (row, index) => h(NInputNumber, {
      value: row.wastewaterCOD,
      'onUpdate:value': (value) => { wastewaterCODData.value[index].wastewaterCOD = value },
      min: 0, precision: 4, showButton: false, placeholder: '请输入'
    })
  },
  {
    title: '单位产品COD产生量（g/m²）', key: 'unitWastewaterCOD', width: 220,
    render: (row) => h('span', { style: 'font-weight: 600;' },
      calcByConcTotalOutput(row.wastewaterCOD, row.wastewaterTotal, row.output) || '-')
  },
  {
    title: '评定等级', key: 'rating', width: 220,
    render: (row, index) => h(NRadioGroup, {
      value: row.rating || null,
      'onUpdate:value': (value) => { wastewaterCODData.value[index].rating = value }
    }, {
      default: () => h(NSpace, { vertical: true }, {
        default: () => [
          h(NRadio, { value: 'level1' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅰ级') }),
          h(NRadio, { value: 'level2' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅱ级') }),
          h(NRadio, { value: 'level3' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅲ级') }),
          h(NRadio, { value: 'none' }, { default: () => h('span', { style: 'font-weight:700;' }, '均不符合') })
        ]
      })
    })
  },
  {
    title: '操作', key: 'actions', width: 100,
    render: (row, index) => h(NButton, { type: 'error', size: 'small', onClick: () => {
      wastewaterCODData.value = wastewaterCODData.value.filter((_, i) => i !== index)
    } }, { default: () => '删除' })
  }
])

// 新增行函数
const addFreshWaterRow = () => {
  const cur = Array.isArray(freshWaterData.value) ? freshWaterData.value : []
  freshWaterData.value = [
    ...cur,
    { product: null, layers: null, output: null, freshWater: null, rating: null }
  ]
}

const addWastewaterTotalRow = () => {
  const cur = Array.isArray(wastewaterTotalData.value) ? wastewaterTotalData.value : []
  wastewaterTotalData.value = [
    ...cur,
    { product: null, layers: null, output: null, wastewaterTotal: null, rating: null }
  ]
}

const addWastewaterCuRow = () => {
  const cur = Array.isArray(wastewaterCuData.value) ? wastewaterCuData.value : []
  wastewaterCuData.value = [
    ...cur,
    { product: null, layers: null, output: null, wastewaterTotal: null, wastewaterCu: null, rating: null }
  ]
}

const addWastewaterCODRow = () => {
  const cur = Array.isArray(wastewaterCODData.value) ? wastewaterCODData.value : []
  wastewaterCODData.value = [
    ...cur,
    { product: null, layers: null, output: null, wastewaterTotal: null, wastewaterCOD: null, rating: null }
  ]
}

// ================= 覆铜板利用率（原/辅料消耗） =================
const showRawMatStandardModal = ref(false)

const rawMaterialColumns = computed(() => [
  {
    title: '类型',
    key: 'type',
    width: 100,
    render: (row, index) => h(NSelect, {
      value: row.type,
      'onUpdate:value': (value) => {
        rawMaterialData.value[index].type = value
        rawMaterialData.value[index].mainProduct = null
        rawMaterialData.value[index].layers = null
      },
      options: typeOptions,
      placeholder: '请选择类型'
    })
  },
  {
    title: '产品名称',
    key: 'mainProduct',
    width: 150,
    render: (row, index) => {
      const options = row.type === 'rigid' ? rigidProductOptions : flexibleProductOptions
      return h(NSelect, {
        value: row.mainProduct,
        'onUpdate:value': (value) => {
          rawMaterialData.value[index].mainProduct = value
          const selectedProduct = options.find(opt => opt.value === value)
          if (selectedProduct && selectedProduct.defaultLayers) {
            rawMaterialData.value[index].layers = selectedProduct.defaultLayers
          } else {
            rawMaterialData.value[index].layers = null
          }
        },
        options: options,
        placeholder: '请选择产品',
        disabled: !row.type
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
        'onUpdate:value': (value) => { rawMaterialData.value[index].layers = value },
        options: layerOptions,
        placeholder: '请选择层数',
        disabled: !row.mainProduct || (selectedProduct && selectedProduct.defaultLayers)
      })
    }
  },
  {
    title: '产量（m²）',
    key: 'output',
    width: 130,
    render: (row, index) => h(NInputNumber, {
      value: row.output,
      'onUpdate:value': (value) => { rawMaterialData.value[index].output = value },
      placeholder: '请输入产量',
      min: 0,
      precision: 2,
      showButton: false
    })
  },
  {
    title: '覆铜板消耗量（m²）',
    key: 'cclConsumption',
    width: 150,
    render: (row, index) => h(NInputNumber, {
      value: row.cclConsumption,
      'onUpdate:value': (value) => { rawMaterialData.value[index].cclConsumption = value },
      placeholder: '请输入消耗量',
      min: 0,
      precision: 2,
      showButton: false
    })
  },
  {
    title: '覆铜板利用率（%）',
    key: 'cclUtilization',
    width: 170,
    render: (row) => h('span', calcPercentTwoSig(row.cclConsumption, row.output) || '-')
  },
  {
    title: '评定等级',
    key: 'rating',
    width: 220,
    render: (row, index) => h(NRadioGroup, {
      value: row.rating || null,
      'onUpdate:value': (value) => { rawMaterialData.value[index].rating = value }
    }, {
      default: () => h(NSpace, { vertical: true }, {
        default: () => [
          h(NRadio, { value: 'level1' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅰ级') }),
          h(NRadio, { value: 'level2' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅱ级') }),
          h(NRadio, { value: 'level3' }, { default: () => h('span', { style: 'font-weight:700;' }, 'Ⅲ级') }),
          h(NRadio, { value: 'none' }, { default: () => h('span', { style: 'font-weight:700;' }, '均不符合') })
        ]
      })
    })
  },
  {
    title: '操作',
    key: 'actions',
    width: 100,
    render: (row, index) => h(NButton, {
      type: 'error', size: 'small', onClick: () => {
        rawMaterialData.value = rawMaterialData.value.filter((_, i) => i !== index)
      }
    }, { default: () => '删除' })
  }
])

const addRawMatRow = () => {
  const cur = Array.isArray(rawMaterialData.value) ? rawMaterialData.value : []
  rawMaterialData.value = [
    ...cur,
    { type: null, mainProduct: null, layers: null, output: null, cclConsumption: null, rating: null }
  ]
}

// ==================== 数据加载函数 ====================

// 加载能源消耗数据
const loadEnergyData = async () => {
  if (!props.enterpriseId) return
  
  loadingEnergy.value = true
  try {
    const response = await api.resourceUtilization.getEnergyConsumption(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      energyData.value = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        type: item.type || '',
        mainProduct: item.mainProduct || '',
        layers: item.layers || 1,
        output: item.output,
        electricity: item.electricity,
        unitConsumption: item.unitConsumption,
        rating: item.rating || null
      }))
    }
  } catch (error) {
    console.error('加载能源消耗数据失败:', error)
    message.error('加载能源消耗数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingEnergy.value = false
  }
}

// 加载新鲜水耗数据
const loadFreshWaterData = async () => {
  if (!props.enterpriseId) return
  
  loadingFreshWater.value = true
  try {
    const response = await api.resourceUtilization.getFreshWaterConsumption(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      freshWaterData.value = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        product: item.product || '',
        layers: item.layers || 1,
        output: item.output,
        freshWater: item.freshWater,
        unitFreshWater: item.unitFreshWater,
        rating: item.rating || null
      }))
    }
  } catch (error) {
    console.error('加载新鲜水耗数据失败:', error)
    message.error('加载新鲜水耗数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingFreshWater.value = false
  }
}

// 加载废水总量数据
const loadWastewaterTotalData = async () => {
  if (!props.enterpriseId) return
  
  loadingWastewaterTotal.value = true
  try {
    const response = await api.resourceUtilization.getWastewaterTotalConsumption(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      wastewaterTotalData.value = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        product: item.product || '',
        layers: item.layers || 1,
        output: item.output,
        wastewaterTotal: item.wastewaterTotal,
        unitWastewater: item.unitWastewater,
        rating: item.rating || null
      }))
    }
  } catch (error) {
    console.error('加载废水总量数据失败:', error)
    message.error('加载废水总量数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingWastewaterTotal.value = false
  }
}

// 加载废水中总铜浓度数据
const loadWastewaterCuData = async () => {
  if (!props.enterpriseId) return
  
  loadingWastewaterCu.value = true
  try {
    const response = await api.resourceUtilization.getWastewaterCuConsumption(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      wastewaterCuData.value = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        product: item.product || '',
        layers: item.layers || 1,
        output: item.output,
        wastewaterTotal: item.wastewaterTotal,
        wastewaterCu: item.wastewaterCu,
        unitWastewaterCu: item.unitWastewaterCu,
        rating: item.rating || null
      }))
    }
  } catch (error) {
    console.error('加载废水中总铜浓度数据失败:', error)
    message.error('加载废水中总铜浓度数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingWastewaterCu.value = false
  }
}

// 加载废水中COD浓度数据
const loadWastewaterCODData = async () => {
  if (!props.enterpriseId) return
  
  loadingWastewaterCOD.value = true
  try {
    const response = await api.resourceUtilization.getWastewaterCODConsumption(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      wastewaterCODData.value = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        product: item.product || '',
        layers: item.layers || 1,
        output: item.output,
        wastewaterTotal: item.wastewaterTotal,
        wastewaterCOD: item.wastewaterCOD,
        unitWastewaterCOD: item.unitWastewaterCOD,
        rating: item.rating || null
      }))
    }
  } catch (error) {
    console.error('加载废水中COD浓度数据失败:', error)
    message.error('加载废水中COD浓度数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingWastewaterCOD.value = false
  }
}

// 加载原/辅料消耗数据
const loadRawMaterialData = async () => {
  if (!props.enterpriseId) return
  
  loadingRawMaterial.value = true
  try {
    const response = await api.resourceUtilization.getRawMaterialConsumption(props.enterpriseId)
    if (response.data && Array.isArray(response.data)) {
      rawMaterialData.value = response.data.map(item => ({
        id: item.id || Date.now() + Math.random(),
        type: item.type || '',
        mainProduct: item.mainProduct || '',
        layers: item.layers || 1,
        output: item.output,
        cclConsumption: item.cclConsumption,
        cclUtilization: item.cclUtilization,
        rating: item.rating || null
      }))
    }
  } catch (error) {
    console.error('加载原/辅料消耗数据失败:', error)
    message.error('加载原/辅料消耗数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingRawMaterial.value = false
  }
}

// ==================== 数据提交函数 ====================

// 提交能源消耗数据
const submitEnergyData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingEnergy.value = true
  try {
    const items = energyData.value
      .filter(row => row.type && row.mainProduct)
      .map(row => ({
        type: row.type,
        mainProduct: row.mainProduct,
        layers: row.layers || 1,
        output: row.output,
        electricity: row.electricity,
        unitConsumption: row.unitConsumption,
        rating: row.rating || null
      }))
    
    await api.resourceUtilization.batchSaveEnergyConsumption(props.enterpriseId, items)
    message.success('能源消耗数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadEnergyData()
  } catch (error) {
    console.error('提交能源消耗数据失败:', error)
    message.error('提交能源消耗数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingEnergy.value = false
  }
}

// 提交新鲜水耗数据
const submitFreshWaterData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingFreshWater.value = true
  try {
    const items = freshWaterData.value
      .filter(row => row.product)
      .map(row => ({
        product: row.product,
        layers: row.layers || 1,
        output: row.output,
        freshWater: row.freshWater,
        unitFreshWater: row.unitFreshWater,
        rating: row.rating || null
      }))
    
    await api.resourceUtilization.batchSaveFreshWaterConsumption(props.enterpriseId, items)
    message.success('新鲜水耗数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadFreshWaterData()
  } catch (error) {
    console.error('提交新鲜水耗数据失败:', error)
    message.error('提交新鲜水耗数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingFreshWater.value = false
  }
}

// 提交废水总量数据
const submitWastewaterTotalData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingWastewaterTotal.value = true
  try {
    const items = wastewaterTotalData.value
      .filter(row => row.product)
      .map(row => ({
        product: row.product,
        layers: row.layers || 1,
        output: row.output,
        wastewaterTotal: row.wastewaterTotal,
        unitWastewater: row.unitWastewater,
        rating: row.rating || null
      }))
    
    await api.resourceUtilization.batchSaveWastewaterTotalConsumption(props.enterpriseId, items)
    message.success('废水总量数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadWastewaterTotalData()
  } catch (error) {
    console.error('提交废水总量数据失败:', error)
    message.error('提交废水总量数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingWastewaterTotal.value = false
  }
}

// 提交废水中总铜浓度数据
const submitWastewaterCuData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingWastewaterCu.value = true
  try {
    const items = wastewaterCuData.value
      .filter(row => row.product)
      .map(row => ({
        product: row.product,
        layers: row.layers || 1,
        output: row.output,
        wastewaterTotal: row.wastewaterTotal,
        wastewaterCu: row.wastewaterCu,
        unitWastewaterCu: row.unitWastewaterCu,
        rating: row.rating || null
      }))
    
    await api.resourceUtilization.batchSaveWastewaterCuConsumption(props.enterpriseId, items)
    message.success('废水中总铜浓度数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadWastewaterCuData()
  } catch (error) {
    console.error('提交废水中总铜浓度数据失败:', error)
    message.error('提交废水中总铜浓度数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingWastewaterCu.value = false
  }
}

// 提交废水中COD浓度数据
const submitWastewaterCODData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingWastewaterCOD.value = true
  try {
    const items = wastewaterCODData.value
      .filter(row => row.product)
      .map(row => ({
        product: row.product,
        layers: row.layers || 1,
        output: row.output,
        wastewaterTotal: row.wastewaterTotal,
        wastewaterCOD: row.wastewaterCOD,
        unitWastewaterCOD: row.unitWastewaterCOD,
        rating: row.rating || null
      }))
    
    await api.resourceUtilization.batchSaveWastewaterCODConsumption(props.enterpriseId, items)
    message.success('废水中COD浓度数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadWastewaterCODData()
  } catch (error) {
    console.error('提交废水中COD浓度数据失败:', error)
    message.error('提交废水中COD浓度数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingWastewaterCOD.value = false
  }
}

// 提交原/辅料消耗数据
const submitRawMaterialData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loadingRawMaterial.value = true
  try {
    const items = rawMaterialData.value
      .filter(row => row.type && row.mainProduct)
      .map(row => {
        // 计算覆铜板利用率：产量/覆铜板消耗量 × 100
        let cclUtilization = null
        if (row.output && row.cclConsumption && row.output > 0 && row.cclConsumption > 0) {
          const ratio = row.output / row.cclConsumption * 100
          // 保留两位有效数字
          if (ratio !== 0) {
            const magnitude = Math.floor(Math.log10(Math.abs(ratio)))
            const factor = Math.pow(10, 1 - magnitude)
            const rounded = Math.round(ratio * factor) / factor
            const decimalPlaces = Math.max(0, 1 - magnitude)
            cclUtilization = parseFloat(rounded.toFixed(decimalPlaces))
          } else {
            cclUtilization = 0
          }
        }
        
        return {
          type: row.type,
          mainProduct: row.mainProduct,
          layers: row.layers || 1,
          output: row.output,
          cclConsumption: row.cclConsumption,
          cclUtilization: cclUtilization,  // 使用计算后的值
          rating: row.rating || null
        }
      })
    
    await api.resourceUtilization.batchSaveRawMaterialConsumption(props.enterpriseId, items)
    message.success('原/辅料消耗数据提交成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadRawMaterialData()
  } catch (error) {
    console.error('提交原/辅料消耗数据失败:', error)
    message.error('提交原/辅料消耗数据失败: ' + (error.message || '未知错误'))
  } finally {
    loadingRawMaterial.value = false
  }
}

// 初始化：每个表格默认一行，并加载数据
onMounted(() => {
  if (props.enterpriseId) {
    loadEnergyData()
    loadFreshWaterData()
    loadWastewaterTotalData()
    loadWastewaterCuData()
    loadWastewaterCODData()
    loadRawMaterialData()
  }
  
  // 如果没有数据，添加默认行
  if (!Array.isArray(energyData.value) || energyData.value.length === 0) addEnergyRow()
  if (!Array.isArray(freshWaterData.value) || freshWaterData.value.length === 0) addFreshWaterRow()
  if (!Array.isArray(wastewaterTotalData.value) || wastewaterTotalData.value.length === 0) addWastewaterTotalRow()
  if (!Array.isArray(wastewaterCuData.value) || wastewaterCuData.value.length === 0) addWastewaterCuRow()
  if (!Array.isArray(wastewaterCODData.value) || wastewaterCODData.value.length === 0) addWastewaterCODRow()
  if (!Array.isArray(rawMaterialData.value) || rawMaterialData.value.length === 0) addRawMatRow()
})

// 监听企业ID变化，重新加载数据
watch(() => props.enterpriseId, (newId) => {
  if (newId) {
    loadEnergyData()
    loadFreshWaterData()
    loadWastewaterTotalData()
    loadWastewaterCuData()
    loadWastewaterCODData()
    loadRawMaterialData()
  }
})

// 保障：父组件在运行期重置/替换 modelValue 时，也能自动补齐默认行
watch(() => props.modelValue, () => {
  if (!Array.isArray(energyData.value) || energyData.value.length === 0) addEnergyRow()
  if (!Array.isArray(freshWaterData.value) || freshWaterData.value.length === 0) addFreshWaterRow()
  if (!Array.isArray(wastewaterTotalData.value) || wastewaterTotalData.value.length === 0) addWastewaterTotalRow()
  if (!Array.isArray(wastewaterCuData.value) || wastewaterCuData.value.length === 0) addWastewaterCuRow()
  if (!Array.isArray(wastewaterCODData.value) || wastewaterCODData.value.length === 0) addWastewaterCODRow()
  if (!Array.isArray(rawMaterialData.value) || rawMaterialData.value.length === 0) addRawMatRow()
}, { immediate: true })
</script>

<style scoped>
.resource-utilization {
  padding: 16px 0;
}

.sub-module {
  border: 1px solid #e0e0e6;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* 卡片标题加粗 */
.sub-module :deep(.n-card-header__main) {
  font-weight: 700;
}

/* 表头加粗 */
.sub-module :deep(.n-data-table-th) {
  font-weight: 700;
}
</style>

