<template>
  <div class="product-characteristics">
    <n-space vertical :size="16">
      <n-card title="1. 使用无毒无害或低毒低害的生产辅助材料" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedAuxiliaryMaterial" @update:value="onUpdateAuxiliaryMaterial">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">Ⅰ 级清洁生产水平基准值：不得使用氢氟氯化碳(HCFCs)、1,1,1-三氯乙烷(C2H3Cl3)、三氯乙烯(C2HCl3)、溴丙烷(C3H7Br)、二氯乙烷(CH3CHCl2)、二氯甲烷(CH2Cl2)、三氯甲烷(CHCl3)、四氯化碳(CCl4)、正己烷(C6H14)、甲苯(C7H8)、二甲苯(C6H4(CH3)2)等物质作为清洗剂。使用光固化抗蚀剂、阻焊剂除电镀金、银与化学镀金外,均采用无氰电镀液除产品特定要求外,不使用铅合金电镀与含氟络合物的电镀液,不采用含铅的焊锡涂层原辅材料中有害物质应满足《电器电子产品有害物质限制使用管理办法》要求。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <n-card title="2. 包装" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedPackaging" @update:value="onUpdatePackaging">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">Ⅰ 级清洁生产水平基准值：不得使用氢氟氯化碳(HCFCs)作为发泡剂;符合GB/T 16716.1 关于包装的通用要求, 包括包装的减量化、重复使用、回收利用、重金属含量和最终处理方面的要求, 并满足GB/T 31268 关于限制商品过度包装的要求。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <n-card title="3. 有害物质限制使用" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedHazardousSubstance" @update:value="onUpdateHazardousSubstance">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">符合</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
          <div class="hazardous-table-wrapper">
            <div class="table-title">Ⅰ 级清洁生产水平基准值：</div>
            <n-data-table
              :columns="hazardousSubstanceColumns"
              :data="hazardousSubstanceData"
              :pagination="false"
              :bordered="true"
              size="small"
              class="hazardous-table"
            />
          </div>
        </n-space>
      </n-card>

      <n-card title="4. 产品性能" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedProductPerformance" @update:value="onUpdateProductPerformance">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">Ⅰ 级清洁生产水平基准值：应达到或超过产品规定的技术要求。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>
    </n-space>
    
    <!-- 提交按钮 -->
    <div style="text-align: left; padding-top: 16px;">
      <n-button 
        type="primary" 
        :loading="loading"
        @click="submitData"
      >
        <template #icon>
          <TheIcon icon="carbon:checkmark" />
        </template>
        提交
      </n-button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { NCard, NCheckboxGroup, NCheckbox, NSpace, NDataTable, NButton, useMessage } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api/pcb'

const message = useMessage()
const loading = ref(false)

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      auxiliaryMaterial: [],
      packaging: [],
      hazardousSubstance: [],
      productPerformance: []
    })
  },
  enterpriseId: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])

// 加载数据
const loadData = async () => {
  if (!props.enterpriseId) return
  
  loading.value = true
  try {
    const response = await api.auditOptions.getProductCharacteristics(props.enterpriseId)
    if (response.data) {
      emit('update:modelValue', {
        auxiliaryMaterial: response.data.auxiliaryMaterial || [],
        packaging: response.data.packaging || [],
        hazardousSubstance: response.data.hazardousSubstance || [],
        productPerformance: response.data.productPerformance || []
      })
    }
  } catch (error) {
    console.error('加载产品特征数据失败:', error)
    message.error('加载数据失败: ' + (error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

// 提交数据
const submitData = async () => {
  if (!props.enterpriseId) {
    message.warning('企业ID不能为空')
    return
  }
  
  loading.value = true
  try {
    await api.auditOptions.saveProductCharacteristics(props.enterpriseId, {
      auxiliaryMaterial: props.modelValue?.auxiliaryMaterial || [],
      packaging: props.modelValue?.packaging || [],
      hazardousSubstance: props.modelValue?.hazardousSubstance || [],
      productPerformance: props.modelValue?.productPerformance || []
    })
    message.success('保存成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadData()
  } catch (error) {
    console.error('保存产品特征数据失败:', error)
    message.error('保存失败: ' + (error.message || '未知错误'))
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (props.enterpriseId) {
    loadData()
  }
})

watch(() => props.enterpriseId, (newId) => {
  if (newId) {
    loadData()
  }
})

// 有害物质限制使用表格数据
const hazardousSubstanceData = [
  { name: '铅及其化合物(Pb)', limit: '≤1000mg/kg' },
  { name: '镉及其化合物(Cd)', limit: '≤100mg/kg' },
  { name: '汞及其化合物(Hg)', limit: '≤1000mg/kg' },
  { name: '六价铬化合物(Cr(VI))', limit: '≤1000mg/kg' },
  { name: '多溴联苯(PBB)', limit: '≤1000mg/kg' },
  { name: '多溴二苯醚(PBDE)', limit: '≤1000mg/kg' },
  { name: '邻苯二甲酸二(2-乙基己基)酯(DEHP)', limit: '≤1000mg/kg' },
  { name: '邻苯二甲酸丁苄酯(BBP)', limit: '≤1000mg/kg' },
  { name: '邻苯二甲酸二丁酯(DBP)', limit: '≤1000mg/kg' },
  { name: '邻苯二甲酸二异丁酯(DIBP)', limit: '≤1000mg/kg' }
]

const hazardousSubstanceColumns = [
  {
    title: '物质名称',
    key: 'name',
    width: 280
  },
  {
    title: '限值',
    key: 'limit',
    width: 150
  }
]

// 1. 使用无毒无害或低毒低害的生产辅助材料（只有Ⅰ级和不符合）
const checkedAuxiliaryMaterial = computed({
  get: () => props.modelValue?.auxiliaryMaterial || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), auxiliaryMaterial: val }
    emit('update:modelValue', next)
  }
})

const onUpdateAuxiliaryMaterial = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedAuxiliaryMaterial.value = next
}

// 2. 包装（只有Ⅰ级和不符合）
const checkedPackaging = computed({
  get: () => props.modelValue?.packaging || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), packaging: val }
    emit('update:modelValue', next)
  }
})

const onUpdatePackaging = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedPackaging.value = next
}

// 3. 有害物质限制使用（只有Ⅰ级和不符合）
const checkedHazardousSubstance = computed({
  get: () => props.modelValue?.hazardousSubstance || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), hazardousSubstance: val }
    emit('update:modelValue', next)
  }
})

const onUpdateHazardousSubstance = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedHazardousSubstance.value = next
}

// 4. 产品性能（只有Ⅰ级和不符合）
const checkedProductPerformance = computed({
  get: () => props.modelValue?.productPerformance || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), productPerformance: val }
    emit('update:modelValue', next)
  }
})

const onUpdateProductPerformance = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedProductPerformance.value = next
}
</script>

<style scoped>
.product-characteristics {
  padding: 16px 0;
}

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

.basic-card :deep(.n-card-header__main) {
  font-weight: 700;
}

.option-text {
  font-size: 15px;
}

.hazardous-table-wrapper {
  margin: 12px 0 20px 0;
  padding: 16px;
  background-color: #fafafa;
  border-radius: 6px;
  border: 1px solid #e0e0e6;
}

.table-title {
  font-weight: 600;
  font-size: 14px;
  color: #333;
  margin-bottom: 12px;
}

.hazardous-table {
  background-color: #fff;
}

.hazardous-table :deep(.n-data-table-th) {
  background-color: #f5f5f5;
  font-weight: 600;
  text-align: center;
}

.hazardous-table :deep(.n-data-table-td) {
  text-align: left;
  padding: 12px 16px;
}
</style>

