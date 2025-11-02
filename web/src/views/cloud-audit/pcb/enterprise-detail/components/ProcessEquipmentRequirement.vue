<template>
  <div class="process-equipment-requirement">
    <n-space vertical :size="16">
      <n-card title="1. 基本要求" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedBasic" @update:value="onUpdateBasic">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：不采用已淘汰高耗能设备；生产场所整洁，符合安全技术、工业卫生的要求</span></n-checkbox>
              <n-checkbox value="level2" :disabled="!checkedBasic.includes('level3')"><span class="option-text">Ⅱ 级清洁生产水平基准值：工厂布局合理，图形形成、板面清洗、蚀刻和电镀与化学镀有水电计量装置</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedBasic.includes('level2') || !checkedBasic.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：工厂有全面节能节水措施，并有效实施。工厂布局先进，生产设备自动化程度高，有安全、节能工效</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <n-card title="2. 机械加工及辅助设施" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedMechanical" @update:value="onUpdateMechanical">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：有安全防护装置；有吸尘装置</span></n-checkbox>
              <n-checkbox value="level2" :disabled="!checkedMechanical.includes('level3')"><span class="option-text">Ⅱ 级清洁生产水平基准值：有集尘系统回收粉尘；废边料分类回收利用</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedMechanical.includes('level2') || !checkedMechanical.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：高噪声区隔音吸声处理；或有防噪声措施</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <n-card title="3. 线路与阻焊图形形成 (印刷或感光工艺)" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedPrinting" @update:value="onUpdatePrinting">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：用水溶性抗蚀剂、弱碱显影阻焊剂；废料分类、回收</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedPrinting.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：用光固化抗蚀剂、阻焊剂；显影、去膜设备附有有机膜处理装置；配置排气或废气处理系统</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <n-card title="4. 板面清洗" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedCleaning" @update:value="onUpdateCleaning">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：不使用有机清洗剂，清洗液不含络合物</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedCleaning.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：建设生产系统数字化体系，拥有覆盖全厂的信息化控制网络和视频监控系统，搭建实时数据库，实现集生产、能源、环境等于一体的数字化管理</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <n-card title="5. 蚀刻" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedEtching" @update:value="onUpdateEtching">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：应用封闭式自动传送蚀刻装置，蚀刻液不含铬、铁化合物及螯合物，废液集中存放并回收</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedEtching.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：蚀刻机有自动控制与添加、再生循环系统；蚀刻清洗水多级逆流清洗；蚀刻清洗溶液补充添加于蚀刻液中或回收；蚀刻机密封，无溶液与气体泄漏，排风管有阀门；排气有吸收处理装置，控制效果好</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <n-card title="6. 电镀与化学镀" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedPlating" @update:value="onUpdatePlating">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：废液集中存放并回收。配置排气和处理系统</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedPlating.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：除电镀金与化学镀金外，均采用无氰电镀液。除产品特定要求外，不采用铅合金电镀与含氟络合物的电镀液，不采用含铅的焊锡涂层。设备有自动控制装置，清洗水多级逆流回用。配置废气收集和处理系统</span></n-checkbox>
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
      basicRequirements: [],
      mechanicalFacilities: [],
      printingProcess: [],
      cleaning: [],
      etching: [],
      plating: []
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
    const response = await api.auditOptions.getProcessRequirement(props.enterpriseId)
    if (response.data) {
      emit('update:modelValue', {
        basicRequirements: response.data.basicRequirements || [],
        mechanicalFacilities: response.data.mechanicalFacilities || [],
        printingProcess: response.data.printingProcess || [],
        cleaning: response.data.cleaning || [],
        etching: response.data.etching || [],
        plating: response.data.plating || []
      })
    }
  } catch (error) {
    console.error('加载生产工艺与装备要求数据失败:', error)
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
    await api.auditOptions.saveProcessRequirement(props.enterpriseId, {
      basicRequirements: props.modelValue?.basicRequirements || [],
      mechanicalFacilities: props.modelValue?.mechanicalFacilities || [],
      printingProcess: props.modelValue?.printingProcess || [],
      cleaning: props.modelValue?.cleaning || [],
      etching: props.modelValue?.etching || [],
      plating: props.modelValue?.plating || []
    })
    message.success('保存成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadData()
  } catch (error) {
    console.error('保存生产工艺与装备要求数据失败:', error)
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

// 1. 基本要求（I、II、III级）
const checkedBasic = computed({
  get: () => props.modelValue?.basicRequirements || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), basicRequirements: val }
    emit('update:modelValue', next)
  }
})

const onUpdateBasic = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedBasic.value = next
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
  checkedBasic.value = next
}

// 2. 机械加工及辅助设施（I、II、III级）
const checkedMechanical = computed({
  get: () => props.modelValue?.mechanicalFacilities || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), mechanicalFacilities: val }
    emit('update:modelValue', next)
  }
})

const onUpdateMechanical = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedMechanical.value = next
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
  checkedMechanical.value = next
}

// 3. 线路与阻焊图形形成（I、III级）
const checkedPrinting = computed({
  get: () => props.modelValue?.printingProcess || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), printingProcess: val }
    emit('update:modelValue', next)
  }
})

const onUpdatePrinting = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedPrinting.value = next
    return
  }
  if (next.includes('level1') && !next.includes('level3')) {
    next.push('level3')
  }
  if (!next.includes('level3')) {
    next = next.filter(v => v !== 'level1')
  }
  checkedPrinting.value = next
}

// 4. 板面清洗（I、III级）
const checkedCleaning = computed({
  get: () => props.modelValue?.cleaning || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), cleaning: val }
    emit('update:modelValue', next)
  }
})

const onUpdateCleaning = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedCleaning.value = next
    return
  }
  if (next.includes('level1') && !next.includes('level3')) {
    next.push('level3')
  }
  if (!next.includes('level3')) {
    next = next.filter(v => v !== 'level1')
  }
  checkedCleaning.value = next
}

// 5. 蚀刻（I、III级）
const checkedEtching = computed({
  get: () => props.modelValue?.etching || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), etching: val }
    emit('update:modelValue', next)
  }
})

const onUpdateEtching = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedEtching.value = next
    return
  }
  if (next.includes('level1') && !next.includes('level3')) {
    next.push('level3')
  }
  if (!next.includes('level3')) {
    next = next.filter(v => v !== 'level1')
  }
  checkedEtching.value = next
}

// 6. 电镀与化学镀（I、III级）
const checkedPlating = computed({
  get: () => props.modelValue?.plating || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), plating: val }
    emit('update:modelValue', next)
  }
})

const onUpdatePlating = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedPlating.value = next
    return
  }
  if (next.includes('level1') && !next.includes('level3')) {
    next.push('level3')
  }
  if (!next.includes('level3')) {
    next = next.filter(v => v !== 'level1')
  }
  checkedPlating.value = next
}
</script>

<style scoped>
.process-equipment-requirement {
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
