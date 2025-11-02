<template>
  <div class="clean-production-management">
    <n-space vertical :size="16">
      <!-- 1. 环保法律法规执行情况（只有Ⅰ级） -->
      <n-card title="1. 环保法律法规执行情况" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedEnvironmentalLaw" @update:value="onUpdateEnvironmentalLaw">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">Ⅰ 级清洁生产水平基准值：符合国家和地方有关环境法律、法规,企业污染物排放总量及能源消耗总量满足国家及地方政府相关标准,满足环评批复、环保"三同时"制度、总量控制和排污许可证管理要求。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 2. 产业政策符合性（只有Ⅰ级和Ⅲ级） -->
      <n-card title="2. 产业政策符合性" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedIndustrialPolicy" @update:value="onUpdateIndustrialPolicy">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：生产规模符合国家和地方。不采用国家明令淘汰类的生产工艺、装备,不生产国家禁止类产品。</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedIndustrialPolicy.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：生产规模符合国家和地方相关产业政策,不采用国家限制、淘汰类的生产工艺、装备,不生产国家限制、淘汰类的产品。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 3. 清洁生产管理（只有Ⅰ级） -->
      <n-card title="3. 清洁生产管理" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedCleanProductionManagement" @update:value="onUpdateCleanProductionManagement">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">Ⅰ 级清洁生产水平基准值：按照GB/T 24001建立并运行环境管理体系,建有专门负责清洁生产的领导机构,各成员单位及主管人员职责分工明确;有健全的清洁生产管理制度和奖励管理办法,有执行情况检查记录;制定有清洁生产工作规划及年度工作计划,对规划、计划提出的目标、指标、清洁生产方案,认真组织落实;资源、能源、环保设施运行统计台账齐全;建立、制定环境突发性事件应急预案(预案要通过相应环保部门备案)并定期演练。按行业无组织排放监管的相关政策要求,加强对无组织排放的防控措施,减少生产过程无组织排放。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 4. 清洁生产审核（Ⅰ、Ⅱ、Ⅲ级） -->
      <n-card title="4. 清洁生产审核" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedCleanProductionAudit" @update:value="onUpdateCleanProductionAudit">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：按政府规定要求,制订清洁生产审核工作计划,原料及生产全流程中部分生产工序定期开展清洁生产审核活动,中、高费方案实施率≥50%。</span></n-checkbox>
              <n-checkbox value="level2" :disabled="!checkedCleanProductionAudit.includes('level3')"><span class="option-text">Ⅱ 级清洁生产水平基准值：按政府规定要求,制订清洁生产审核工作计划,对原料及生产全流程定期开展清洁生产审核活动,中、高费方案实施率≥60%。</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedCleanProductionAudit.includes('level2') || !checkedCleanProductionAudit.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：按政府规定要求,制订清洁生产审核工作计划,对原料及生产全流程定期开展清洁生产审核活动,中、高费方案实施率≥80%。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 5. 节能管理（Ⅰ、Ⅱ、Ⅲ级） -->
      <n-card title="5. 节能管理" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedEnergyManagement" @update:value="onUpdateEnergyManagement">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：按国家规定要求,组织开展节能评估与能源审计工作,实施节能改造项目完成率≥50%。</span></n-checkbox>
              <n-checkbox value="level2" :disabled="!checkedEnergyManagement.includes('level3')"><span class="option-text">Ⅱ 级清洁生产水平基准值：按国家规定要求,组织开展节能评估与能源审计工作,实施节能改造项目完成率≥70%。</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedEnergyManagement.includes('level2') || !checkedEnergyManagement.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：按国家规定要求,组织开展节能评估与能源审计工作,实施节能改造项目完成率≥90%。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">均不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 6. 污染物排放监测（只有Ⅰ级） -->
      <n-card title="6. 污染物排放监测" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedEmissionMonitoring" @update:value="onUpdateEmissionMonitoring">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">Ⅰ 级清洁生产水平基准值：满足国家相关监测技术规范要求;按照排污许可证规定的自行监测方案自行或委托第三方监测机构开展监测工作,安排专人专职对监测数据进行记录、整理、统计和分析,公开自行监测信息。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 7. 危险化学品管理（只有Ⅰ级） -->
      <n-card title="7. 危险化学品管理" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedChemicalManagement" @update:value="onUpdateChemicalManagement">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">Ⅰ 级清洁生产水平基准值：符合《危险化学品安全管理条例》相关要求。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 8. 计量器具配备情况（只有Ⅰ级） -->
      <n-card title="8. 计量器具配备情况" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedMeasurementEquipment" @update:value="onUpdateMeasurementEquipment">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">Ⅰ 级清洁生产水平基准值：计量器具配备满足符合国家标准GB17167、GB24789三级计量配备要求。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 9. 固体废物处理处置（只有Ⅰ级） -->
      <n-card title="9. 固体废物处理处置" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedSolidWasteDisposal" @update:value="onUpdateSolidWasteDisposal">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">Ⅰ 级清洁生产水平基准值：通过当地环保主管部门组织的危险废物规范化管理考核,综合评估结果为"达标"。按照GB 18599 相关规定对暂时不利用或者不能利用的一般工业固体废物进行贮存或处置。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 10. 土壤污染隐患排查（只有Ⅰ级） -->
      <n-card title="10. 土壤污染隐患排查" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedSoilPollutionRisk" @update:value="onUpdateSoilPollutionRisk">
            <n-space vertical>
              <n-checkbox value="level1"><span class="option-text">Ⅰ 级清洁生产水平基准值：属于土壤污染重点监管单位的企业应参照国家有关技术规范,建立土壤污染隐患排查制度,保证持续有效防止有毒有害物质渗漏、流失、扬散。</span></n-checkbox>
              <n-checkbox value="none"><span class="option-text">不符合</span></n-checkbox>
            </n-space>
          </n-checkbox-group>
        </n-space>
      </n-card>

      <!-- 11. 运输方式（Ⅰ、Ⅱ、Ⅲ级） -->
      <n-card title="11. 运输方式" size="small" class="sub-module basic-card">
        <n-space vertical>
          <n-checkbox-group :value="checkedTransportMode" @update:value="onUpdateTransportMode">
            <n-space vertical>
              <n-checkbox value="level3"><span class="option-text">Ⅲ 级清洁生产水平基准值：物料公路运输和厂内运输车辆全部使用达到国五及以上排放标准的重型载货车辆(含燃气)，或新能源汽车比例不低于50%，其他车辆达到国四排放标准；厂内非道路移动机械全部达到国三及以上排放标准或使用新能源机械比例不低于50%。</span></n-checkbox>
              <n-checkbox value="level2" :disabled="!checkedTransportMode.includes('level3')"><span class="option-text">Ⅱ 级清洁生产水平基准值：物料公路运输和厂内运输车辆全部使用达到国五及以上排放标准的重型载货车辆(含燃气)，或新能源汽车比例不低于70%，其他车辆达到国四排放标准；厂内非道路移动机械全部达到国三及以上排放标准或使用新能源机械比例不低于70%。</span></n-checkbox>
              <n-checkbox value="level1" :disabled="!checkedTransportMode.includes('level2') || !checkedTransportMode.includes('level3')"><span class="option-text">Ⅰ 级清洁生产水平基准值：物料公路运输和厂内运输车辆全部使用达到国五及以上排放标准的重型载货车辆(含燃气)或新能源汽车；厂内非道路移动机械全部达到国三及以上排放标准或使用新能源机械。</span></n-checkbox>
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
      environmentalLaw: [],
      industrialPolicy: [],
      cleanProductionManagement: [],
      cleanProductionAudit: [],
      energyManagement: [],
      emissionMonitoring: [],
      chemicalManagement: [],
      measurementEquipment: [],
      solidWasteDisposal: [],
      soilPollutionRisk: [],
      transportMode: []
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
    const response = await api.auditOptions.getCleanProductionManagement(props.enterpriseId)
    if (response.data) {
      emit('update:modelValue', {
        environmentalLaw: response.data.environmentalLaw || [],
        industrialPolicy: response.data.industrialPolicy || [],
        cleanProductionManagement: response.data.cleanProductionManagement || [],
        cleanProductionAudit: response.data.cleanProductionAudit || [],
        energyManagement: response.data.energyManagement || [],
        emissionMonitoring: response.data.emissionMonitoring || [],
        chemicalManagement: response.data.chemicalManagement || [],
        measurementEquipment: response.data.measurementEquipment || [],
        solidWasteDisposal: response.data.solidWasteDisposal || [],
        soilPollutionRisk: response.data.soilPollutionRisk || [],
        transportMode: response.data.transportMode || []
      })
    }
  } catch (error) {
    console.error('加载清洁生产管理数据失败:', error)
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
    await api.auditOptions.saveCleanProductionManagement(props.enterpriseId, {
      environmentalLaw: props.modelValue?.environmentalLaw || [],
      industrialPolicy: props.modelValue?.industrialPolicy || [],
      cleanProductionManagement: props.modelValue?.cleanProductionManagement || [],
      cleanProductionAudit: props.modelValue?.cleanProductionAudit || [],
      energyManagement: props.modelValue?.energyManagement || [],
      emissionMonitoring: props.modelValue?.emissionMonitoring || [],
      chemicalManagement: props.modelValue?.chemicalManagement || [],
      measurementEquipment: props.modelValue?.measurementEquipment || [],
      solidWasteDisposal: props.modelValue?.solidWasteDisposal || [],
      soilPollutionRisk: props.modelValue?.soilPollutionRisk || [],
      transportMode: props.modelValue?.transportMode || []
    })
    message.success('保存成功')
    await new Promise(resolve => setTimeout(resolve, 300))
    await loadData()
  } catch (error) {
    console.error('保存清洁生产管理数据失败:', error)
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

// 1. 环保法律法规执行情况（只有Ⅰ级和不符合）
const checkedEnvironmentalLaw = computed({
  get: () => props.modelValue?.environmentalLaw || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), environmentalLaw: val }
    emit('update:modelValue', next)
  }
})

const onUpdateEnvironmentalLaw = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedEnvironmentalLaw.value = next
}

// 2. 产业政策符合性（只有Ⅰ级和Ⅲ级）
const checkedIndustrialPolicy = computed({
  get: () => props.modelValue?.industrialPolicy || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), industrialPolicy: val }
    emit('update:modelValue', next)
  }
})

const onUpdateIndustrialPolicy = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedIndustrialPolicy.value = next
    return
  }
  // Ⅰ级必须先满足Ⅲ级
  if (next.includes('level1') && !next.includes('level3')) {
    next.push('level3')
  }
  // 取消Ⅲ级时自动取消Ⅰ级
  if (!next.includes('level3')) {
    next = next.filter(v => v !== 'level1')
  }
  checkedIndustrialPolicy.value = next
}

// 3. 清洁生产管理（只有Ⅰ级和不符合）
const checkedCleanProductionManagement = computed({
  get: () => props.modelValue?.cleanProductionManagement || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), cleanProductionManagement: val }
    emit('update:modelValue', next)
  }
})

const onUpdateCleanProductionManagement = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedCleanProductionManagement.value = next
}

// 4. 清洁生产审核（Ⅰ、Ⅱ、Ⅲ级）
const checkedCleanProductionAudit = computed({
  get: () => props.modelValue?.cleanProductionAudit || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), cleanProductionAudit: val }
    emit('update:modelValue', next)
  }
})

const onUpdateCleanProductionAudit = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedCleanProductionAudit.value = next
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
  checkedCleanProductionAudit.value = next
}

// 5. 节能管理（Ⅰ、Ⅱ、Ⅲ级）
const checkedEnergyManagement = computed({
  get: () => props.modelValue?.energyManagement || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), energyManagement: val }
    emit('update:modelValue', next)
  }
})

const onUpdateEnergyManagement = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedEnergyManagement.value = next
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
  checkedEnergyManagement.value = next
}

// 6. 污染物排放监测（只有Ⅰ级和不符合）
const checkedEmissionMonitoring = computed({
  get: () => props.modelValue?.emissionMonitoring || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), emissionMonitoring: val }
    emit('update:modelValue', next)
  }
})

const onUpdateEmissionMonitoring = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedEmissionMonitoring.value = next
}

// 7. 危险化学品管理（只有Ⅰ级和不符合）
const checkedChemicalManagement = computed({
  get: () => props.modelValue?.chemicalManagement || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), chemicalManagement: val }
    emit('update:modelValue', next)
  }
})

const onUpdateChemicalManagement = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedChemicalManagement.value = next
}

// 8. 计量器具配备情况（只有Ⅰ级和不符合）
const checkedMeasurementEquipment = computed({
  get: () => props.modelValue?.measurementEquipment || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), measurementEquipment: val }
    emit('update:modelValue', next)
  }
})

const onUpdateMeasurementEquipment = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedMeasurementEquipment.value = next
}

// 9. 固体废物处理处置（只有Ⅰ级和不符合）
const checkedSolidWasteDisposal = computed({
  get: () => props.modelValue?.solidWasteDisposal || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), solidWasteDisposal: val }
    emit('update:modelValue', next)
  }
})

const onUpdateSolidWasteDisposal = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedSolidWasteDisposal.value = next
}

// 10. 土壤污染隐患排查（只有Ⅰ级和不符合）
const checkedSoilPollutionRisk = computed({
  get: () => props.modelValue?.soilPollutionRisk || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), soilPollutionRisk: val }
    emit('update:modelValue', next)
  }
})

const onUpdateSoilPollutionRisk = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none') && next.includes('level1')) {
    next = next.filter(v => v !== 'level1')
  }
  if (next.includes('level1') && next.includes('none')) {
    next = next.filter(v => v !== 'none')
  }
  checkedSoilPollutionRisk.value = next
}

// 11. 运输方式（Ⅰ、Ⅱ、Ⅲ级）
const checkedTransportMode = computed({
  get: () => props.modelValue?.transportMode || [],
  set: (val) => {
    const next = { ...(props.modelValue || {}), transportMode: val }
    emit('update:modelValue', next)
  }
})

const onUpdateTransportMode = (vals) => {
  let next = Array.isArray(vals) ? [...vals] : []
  if (next.includes('none')) {
    next = ['none']
    checkedTransportMode.value = next
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
  checkedTransportMode.value = next
}
</script>

<style scoped>
.clean-production-management {
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

