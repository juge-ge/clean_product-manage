<template>
  <div class="greenhouse-gas-emission">
    <n-space vertical :size="16">
      <n-card title="1. 碳减排管理" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedCarbonManagement" @update:value="onUpdateCarbonManagement">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：定期开展碳盘查</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedCarbonManagement.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：定期开展主要产品碳足迹评价和碳盘查</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <n-card title="2. 单位产值碳排放量" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedEmissionPerOutput" @update:value="onUpdateEmissionPerOutput">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：识别、计算并提供改进方案</span></n-checkbox>
              <n-checkbox value="level2" :disabled="!checkedEmissionPerOutput.includes('level3')"><span class="option-text">Ⅱ 级清洁生产水平基准值：与上年度相比指标改善</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedEmissionPerOutput.includes('level2') || !checkedEmissionPerOutput.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：近三年指标持续改善</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <n-card title="3. 碳排放强度" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedEmissionIntensity" @update:value="onUpdateEmissionIntensity">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：2.677 t/万元</span></n-checkbox>
              <n-checkbox value="level2" :disabled="!checkedEmissionIntensity.includes('level3')"><span class="option-text">Ⅱ 级清洁生产水平基准值：1.71 t/万元</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedEmissionIntensity.includes('level2') || !checkedEmissionIntensity.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：0.628 t/万元</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
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
import { NCard, NCheckboxGroup, NCheckbox, NSpace, NButton, useMessage } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api/pcb'

const message = useMessage()
const loading = ref(false)

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      carbonManagement: [],
      emissionPerOutput: [],
      emissionIntensity: []
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
    const response = await api.auditOptions.getGreenhouseGasEmission(props.enterpriseId)
    if (response.data) {
      emit('update:modelValue', {
        carbonManagement: response.data.carbonManagement || [],
        emissionPerOutput: response.data.emissionPerOutput || [],
        emissionIntensity: response.data.emissionIntensity || []
      })
    }
  } catch (error) {
    console.error('加载温室气体排放数据失败:', error)
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
    await api.auditOptions.saveGreenhouseGasEmission(props.enterpriseId, {
      carbonManagement: props.modelValue?.carbonManagement || [],
      emissionPerOutput: props.modelValue?.emissionPerOutput || [],
      emissionIntensity: props.modelValue?.emissionIntensity || []
    })
    message.success('保存成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadData()
  } catch (error) {
    console.error('保存温室气体排放数据失败:', error)
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

// 1. 碳减排管理（I、III级，跳过II级）
const checkedCarbonManagement = computed({
  get: () => props.modelValue?.carbonManagement || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), carbonManagement: val }
    emit('update:modelValue', next)
  }
})

const onUpdateCarbonManagement = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedCarbonManagement.value = next
    return
  }
  if (next.includes('level1') && !next.includes('level3')) {
    next.push('level3')
  }
  if (!next.includes('level3')) {
    next = next.filter(v => v !== 'level1')
  }
  checkedCarbonManagement.value = next
}

// 2. 单位产值碳排放量（I、II、III级）
const checkedEmissionPerOutput = computed({
  get: () => props.modelValue?.emissionPerOutput || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), emissionPerOutput: val }
    emit('update:modelValue', next)
  }
})

const onUpdateEmissionPerOutput = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedEmissionPerOutput.value = next
    return
  }
  if (next.includes('level1')) {
    if (!next.includes('level2')) next.push('level2')
    if (!next.includes('level3')) next.push('level3')
  }
  if (next.includes('level2') && !next.includes('level3')) {
    next.push('level3')
  }
  if (!next.includes('level3')) {
    next = next.filter(v => v !== 'level2' && v !== 'level1')
  }
  if (!next.includes('level2')) {
    next = next.filter(v => v !== 'level1')
  }
  checkedEmissionPerOutput.value = next
}

// 3. 碳排放强度（I、II、III级）
const checkedEmissionIntensity = computed({
  get: () => props.modelValue?.emissionIntensity || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), emissionIntensity: val }
    emit('update:modelValue', next)
  }
})

const onUpdateEmissionIntensity = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedEmissionIntensity.value = next
    return
  }
  if (next.includes('level1')) {
    if (!next.includes('level2')) next.push('level2')
    if (!next.includes('level3')) next.push('level3')
  }
  if (next.includes('level2') && !next.includes('level3')) {
    next.push('level3')
  }
  if (!next.includes('level3')) {
    next = next.filter(v => v !== 'level2' && v !== 'level1')
  }
  if (!next.includes('level2')) {
    next = next.filter(v => v !== 'level1')
  }
  checkedEmissionIntensity.value = next
}
</script>

<style scoped>
.greenhouse-gas-emission {
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
</style>

