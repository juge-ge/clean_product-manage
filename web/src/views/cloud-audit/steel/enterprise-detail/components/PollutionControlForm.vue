<template>
  <div class="pollution-control-form">
    <n-grid :cols="2" :x-gap="24">
      <n-form-item-gi label="废水处理">
        <n-grid :cols="1" :x-gap="12">
          <n-form-item-gi label="处理工艺">
            <n-input v-model:value="formData.wastewater.treatment" placeholder="如：生化处理+深度处理" />
          </n-form-item-gi>
          <n-form-item-gi label="处理能力">
            <n-input-number
              v-model:value="formData.wastewater.capacity"
              placeholder="处理能力"
              :min="0"
              :precision="2"
            >
              <template #suffix>m³/d</template>
            </n-input-number>
          </n-form-item-gi>
          <n-form-item-gi label="处理工艺描述">
            <n-input
              v-model:value="formData.wastewater.process"
              type="textarea"
              placeholder="如：A/O+MBR"
              :rows="2"
            />
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
      
      <n-form-item-gi label="废气处理">
        <n-grid :cols="1" :x-gap="12">
          <n-form-item-gi label="处理工艺">
            <n-input v-model:value="formData.wasteGas.treatment" placeholder="如：脱硫脱硝除尘" />
          </n-form-item-gi>
          <n-form-item-gi label="处理设施">
            <n-input v-model:value="formData.wasteGas.facilities" placeholder="如：SCR+湿法脱硫+电除尘" />
          </n-form-item-gi>
          <n-form-item-gi label="处理效率">
            <n-input-number
              v-model:value="formData.wasteGas.efficiency"
              placeholder="处理效率"
              :min="0"
              :max="100"
              :precision="1"
            >
              <template #suffix>%</template>
            </n-input-number>
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
      
      <n-form-item-gi label="固废处理">
        <n-grid :cols="1" :x-gap="12">
          <n-form-item-gi label="处理方式">
            <n-input v-model:value="formData.solidWaste.treatment" placeholder="如：综合利用" />
          </n-form-item-gi>
          <n-form-item-gi label="综合利用率">
            <n-input-number
              v-model:value="formData.solidWaste.utilization"
              placeholder="综合利用率"
              :min="0"
              :max="100"
              :precision="1"
            >
              <template #suffix>%</template>
            </n-input-number>
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
    </n-grid>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NFormItemGi, NGrid, NInput, NInputNumber } from 'naive-ui'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      wastewater: {
        treatment: '',
        capacity: null,
        process: ''
      },
      wasteGas: {
        treatment: '',
        facilities: '',
        efficiency: null
      },
      solidWaste: {
        treatment: '',
        utilization: null
      }
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})
</script>

<style scoped>
.pollution-control-form {
  padding: 16px;
}
</style>
