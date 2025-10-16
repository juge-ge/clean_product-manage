<template>
  <div class="self-monitoring-form">
    <n-grid :cols="2" :x-gap="24">
      <n-form-item-gi label="废水监测">
        <n-grid :cols="1" :x-gap="12">
          <n-form-item-gi label="监测项目">
            <n-input v-model:value="formData.wastewater.pollutants" placeholder="如：COD、氨氮、总磷、总氮" />
          </n-form-item-gi>
          <n-form-item-gi label="监测频次">
            <n-select
              v-model:value="formData.wastewater.frequency"
              :options="frequencyOptions"
              placeholder="选择监测频次"
            />
          </n-form-item-gi>
          <n-form-item-gi label="达标情况">
            <n-select
              v-model:value="formData.wastewater.compliance"
              :options="complianceOptions"
              placeholder="选择达标情况"
            />
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
      
      <n-form-item-gi label="废气监测">
        <n-grid :cols="1" :x-gap="12">
          <n-form-item-gi label="监测项目">
            <n-input v-model:value="formData.wasteGas.pollutants" placeholder="如：SO₂、NOx、颗粒物" />
          </n-form-item-gi>
          <n-form-item-gi label="监测频次">
            <n-select
              v-model:value="formData.wasteGas.frequency"
              :options="frequencyOptions"
              placeholder="选择监测频次"
            />
          </n-form-item-gi>
          <n-form-item-gi label="达标情况">
            <n-select
              v-model:value="formData.wasteGas.compliance"
              :options="complianceOptions"
              placeholder="选择达标情况"
            />
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
      
      <n-form-item-gi label="噪声监测">
        <n-grid :cols="1" :x-gap="12">
          <n-form-item-gi label="监测点位">
            <n-input-number
              v-model:value="formData.noise.points"
              placeholder="监测点位数量"
              :min="1"
              style="width: 100%"
            />
          </n-form-item-gi>
          <n-form-item-gi label="监测频次">
            <n-select
              v-model:value="formData.noise.frequency"
              :options="frequencyOptions"
              placeholder="选择监测频次"
            />
          </n-form-item-gi>
          <n-form-item-gi label="达标情况">
            <n-select
              v-model:value="formData.noise.compliance"
              :options="complianceOptions"
              placeholder="选择达标情况"
            />
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
    </n-grid>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NFormItemGi, NGrid, NInput, NInputNumber, NSelect } from 'naive-ui'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      wastewater: {
        pollutants: '',
        frequency: '',
        compliance: ''
      },
      wasteGas: {
        pollutants: '',
        frequency: '',
        compliance: ''
      },
      noise: {
        points: null,
        frequency: '',
        compliance: ''
      }
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const frequencyOptions = [
  { label: '连续监测', value: '连续监测' },
  { label: '每日', value: '每日' },
  { label: '每周', value: '每周' },
  { label: '每月', value: '每月' },
  { label: '每季度', value: '每季度' },
  { label: '每半年', value: '每半年' },
  { label: '每年', value: '每年' }
]

const complianceOptions = [
  { label: '达标', value: '达标' },
  { label: '不达标', value: '不达标' },
  { label: '部分达标', value: '部分达标' }
]
</script>

<style scoped>
.self-monitoring-form {
  padding: 16px;
}
</style>
