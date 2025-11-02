<template>
  <div class="resource-reutilization">
    <n-space vertical :size="16">
      <!-- 1. 水资源消耗 - 水资源重复利用率 -->
      <n-card title="1. 水资源重复利用率" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedWaterReuse" @update:value="onUpdateWaterReuse">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ级清洁生产水平基准值（≥45%）</span></n-checkbox>
              <n-checkbox value="level2" :disabled="!checkedWaterReuse.includes('level3')"><span class="option-text">Ⅱ级清洁生产水平基准值（≥55%）</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedWaterReuse.includes('level2') || !checkedWaterReuse.includes('level3')"><span class="option-text">Ⅰ级清洁生产水平基准值（≥65%）</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 2. 资源综合利用 - 金属铜回收率 -->
      <n-card title="2. 金属铜回收率" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedEtchingRecovery" @update:value="onUpdateEtchingRecovery">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ级清洁生产水平基准值（≥80%）</span></n-checkbox>
              <n-checkbox value="level2" :disabled="!checkedEtchingRecovery.includes('level3')"><span class="option-text">Ⅱ级清洁生产水平基准值（≥88%）</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedEtchingRecovery.includes('level2') || !checkedEtchingRecovery.includes('level3')"><span class="option-text">Ⅰ级清洁生产水平基准值（≥95%）</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 3. 资源综合利用 - 一般工业固体废物综合利用率 -->
      <n-card title="3. 一般工业固体废物综合利用率" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedGeneralSolidUtil" @update:value="onUpdateGeneralSolidUtil">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ级清洁生产水平基准值（≥65%）</span></n-checkbox>
              <n-checkbox value="level2" :disabled="!checkedGeneralSolidUtil.includes('level3')"><span class="option-text">Ⅱ级清洁生产水平基准值（≥73%）</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedGeneralSolidUtil.includes('level2') || !checkedGeneralSolidUtil.includes('level3')"><span class="option-text">Ⅰ级清洁生产水平基准值（≥90%）</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 4. 污染物排放 - 废水收集与处理（只有Ⅰ级/不符合） -->
      <n-card title="4. 废水收集与处理" size="small" class="sub-module basic-card">
        <n-space vertical>
          <div class="desc">① 自动监测：涉及电镀、蚀刻工序的企业应在一类污染物排口和总排口设置自动监测装置。② 稳定达标：一类污染物排口及总排口水污染因子持续稳定达标。</div>
          <n-checkbox-group :value="checkedWastewaterCollection" @update:value="onUpdateWastewaterCollection">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">符合（Ⅰ级）</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 5. 污染物排放 - 废气收集与处理（只有Ⅰ级/不符合） -->
      <n-card title="5. 废气收集与处理" size="small" class="sub-module basic-card">
        <n-space vertical>
          <div class="desc">① 废气分类收集及处理。② 废气筒符合 GB/T 16758 的规定。③ 废气处理设施设计及工艺设置合理，确保各排口污染物因子持续稳定达标。④ 有自动加料调节装置。⑤ 建立废气处理设施运行台帐。</div>
          <n-checkbox-group :value="checkedWasteGasTreatment" @update:value="onUpdateWasteGasTreatment">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">符合（Ⅰ级）</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 6. 固体废物 - 一般固体废物收集与处理（只有Ⅰ级/不符合） -->
      <n-card title="6. 一般固体废物收集与处理" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedGeneralSolidCollection" @update:value="onUpdateGeneralSolidCollection">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">符合（Ⅰ级）：符合《一般工业固体废物贮存和填埋污染控制标准》要求</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 7. 固体废物 - 危险废物收集与处理（只有Ⅰ级/不符合） -->
      <n-card title="7. 危险废物收集与处理" size="small" class="sub-module basic-card">
        <n-space vertical>
          <div class="desc">① 满足《危险废物贮存污染控制标准》规定的防渗标准，符合相关收集、贮存、利用和处置要求。② 建立危险废物管理、台帐记录制度。</div>
          <n-checkbox-group :value="checkedHazardousWasteCollection" @update:value="onUpdateHazardousWasteCollection">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">符合（Ⅰ级）</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 8. 声环境 - 噪声（只有Ⅰ级/不符合） -->
      <n-card title="8. 噪声" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedNoise" @update:value="onUpdateNoise">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">符合（Ⅰ级）：厂界及周边保护目标处噪声值稳定达标</span></n-checkbox>
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
import { NCard, NCheckboxGroup, NCheckbox, NSpace, NButton, useMessage } from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import api from '@/api/pcb'

const message = useMessage()
const loading = ref(false)

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      waterReuse: [],
      etchingRecovery: [],
      generalSolidUtil: [],
      wastewaterCollection: [],
      wasteGasTreatment: [],
      generalSolidCollection: [],
      hazardousWasteCollection: [],
      noise: []
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
    const response = await api.auditOptions.getResourceReutilization(props.enterpriseId)
    if (response.data) {
      emit('update:modelValue', {
        waterReuse: response.data.waterReuse || [],
        etchingRecovery: response.data.etchingRecovery || [],
        generalSolidUtil: response.data.generalSolidUtil || [],
        wastewaterCollection: response.data.wastewaterCollection || [],
        wasteGasTreatment: response.data.wasteGasTreatment || [],
        generalSolidCollection: response.data.generalSolidCollection || [],
        hazardousWasteCollection: response.data.hazardousWasteCollection || [],
        noise: response.data.noise || []
      })
    }
  } catch (error) {
    console.error('加载资源综合利用数据失败:', error)
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
    await api.auditOptions.saveResourceReutilization(props.enterpriseId, {
      waterReuse: props.modelValue?.waterReuse || [],
      etchingRecovery: props.modelValue?.etchingRecovery || [],
      generalSolidUtil: props.modelValue?.generalSolidUtil || [],
      wastewaterCollection: props.modelValue?.wastewaterCollection || [],
      wasteGasTreatment: props.modelValue?.wasteGasTreatment || [],
      generalSolidCollection: props.modelValue?.generalSolidCollection || [],
      hazardousWasteCollection: props.modelValue?.hazardousWasteCollection || [],
      noise: props.modelValue?.noise || []
    })
    message.success('保存成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadData()
  } catch (error) {
    console.error('保存资源综合利用数据失败:', error)
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

// 通用层级更新器（I/II/III+none）
const updateWithLevels = (vals, getter, setter) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) { setter(['none']); return }
  if (next.includes('level1')) {
    if (!next.includes('level2')) next.push('level2')
    if (!next.includes('level3')) next.push('level3')
  }
  if (next.includes('level2') && !next.includes('level3')) next.push('level3')
  if (!next.includes('level3')) next = next.filter(v => v !== 'level2' && v !== 'level1')
  if (!next.includes('level2')) next = next.filter(v => v !== 'level1')
  setter(next)
}

// 1. 水资源重复利用率（I/II/III/none）
const checkedWaterReuse = computed({
  get: () => props.modelValue?.waterReuse || [],
  set: (val) => emit('update:modelValue', { ...(props.modelValue || {}), waterReuse: val })
})
const onUpdateWaterReuse = (vals) => updateWithLevels(vals, () => checkedWaterReuse.value, (v) => checkedWaterReuse.value = v)

// 2. 金属铜回收率（I/II/III/none）
const checkedEtchingRecovery = computed({
  get: () => props.modelValue?.etchingRecovery || [],
  set: (val) => emit('update:modelValue', { ...(props.modelValue || {}), etchingRecovery: val })
})
const onUpdateEtchingRecovery = (vals) => updateWithLevels(vals, () => checkedEtchingRecovery.value, (v) => checkedEtchingRecovery.value = v)

// 3. 一般工业固体废物综合利用率（I/II/III/none）
const checkedGeneralSolidUtil = computed({
  get: () => props.modelValue?.generalSolidUtil || [],
  set: (val) => emit('update:modelValue', { ...(props.modelValue || {}), generalSolidUtil: val })
})
const onUpdateGeneralSolidUtil = (vals) => updateWithLevels(vals, () => checkedGeneralSolidUtil.value, (v) => checkedGeneralSolidUtil.value = v)

// 4. 废水收集与处理（Ⅰ/不符合）
const checkedWastewaterCollection = computed({
  get: () => props.modelValue?.wastewaterCollection || [],
  set: (val) => emit('update:modelValue', { ...(props.modelValue || {}), wastewaterCollection: val })
})
const onUpdateWastewaterCollection = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) next = ['none']
  if (next.includes('level1') && next.includes('none')) next = ['level1']
  checkedWastewaterCollection.value = next
}

// 5. 废气收集与处理（Ⅰ/不符合）
const checkedWasteGasTreatment = computed({
  get: () => props.modelValue?.wasteGasTreatment || [],
  set: (val) => emit('update:modelValue', { ...(props.modelValue || {}), wasteGasTreatment: val })
})
const onUpdateWasteGasTreatment = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) next = ['none']
  if (next.includes('level1') && next.includes('none')) next = ['level1']
  checkedWasteGasTreatment.value = next
}

// 6. 一般固体废物收集与处理（Ⅰ/不符合）
const checkedGeneralSolidCollection = computed({
  get: () => props.modelValue?.generalSolidCollection || [],
  set: (val) => emit('update:modelValue', { ...(props.modelValue || {}), generalSolidCollection: val })
})
const onUpdateGeneralSolidCollection = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) next = ['none']
  if (next.includes('level1') && next.includes('none')) next = ['level1']
  checkedGeneralSolidCollection.value = next
}

// 7. 危险废物收集与处理（Ⅰ/不符合）
const checkedHazardousWasteCollection = computed({
  get: () => props.modelValue?.hazardousWasteCollection || [],
  set: (val) => emit('update:modelValue', { ...(props.modelValue || {}), hazardousWasteCollection: val })
})
const onUpdateHazardousWasteCollection = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) next = ['none']
  if (next.includes('level1') && next.includes('none')) next = ['level1']
  checkedHazardousWasteCollection.value = next
}

// 8. 噪声（Ⅰ/不符合）
const checkedNoise = computed({
  get: () => props.modelValue?.noise || [],
  set: (val) => emit('update:modelValue', { ...(props.modelValue || {}), noise: val })
})
const onUpdateNoise = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) next = ['none']
  if (next.includes('level1') && next.includes('none')) next = ['level1']
  checkedNoise.value = next
}
</script>

<style scoped>
.resource-reutilization {
  padding: 16px 0;
}
.sub-module {
  border: 1px solid #e0e0e6;
  border-radius: 6px;
}
.basic-card :deep(.n-card-header__main) { font-weight: 700; }
.option-text { font-size: 15px; }
.desc { color: #666; font-size: 13px; line-height: 1.6; }
</style>

