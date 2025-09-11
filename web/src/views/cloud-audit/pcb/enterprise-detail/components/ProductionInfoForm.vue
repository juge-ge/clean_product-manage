<template>
  <div class="production-info-form">
    <n-form-item label="产能（万m²/年）">
      <n-input-number 
        v-model:value="formData.capacity"
        placeholder="请输入年产能"
        :min="0"
        :precision="2"
      />
    </n-form-item>
    
    <n-tabs type="line" class="mt-4">
      <n-tab-pane 
        v-for="year in years" 
        :key="year" 
        :name="year" 
        :tab="`${year}年产量`"
      >
        <n-grid :cols="2" :x-gap="24">
          <n-form-item-gi 
            v-for="type in productionTypes" 
            :key="type.key"
            :label="`${type.label}（万m²）`"
          >
            <n-input-number 
              v-model:value="formData.output[year][type.key]"
              placeholder="请输入产量"
              :min="0"
              :precision="2"
            />
          </n-form-item-gi>
        </n-grid>
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup>
import { computed, watch } from 'vue'
import { NFormItem, NInputNumber, NTabs, NTabPane, NGrid, NFormItemGi } from 'naive-ui'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      capacity: null,
      output: {
        '2022': {},
        '2023': {},
        '2024': {}
      }
    })
  }
})

const emit = defineEmits(['update:modelValue'])

const formData = computed({
  get: () => props.modelValue,
  set: (value) => emit('update:modelValue', value)
})

const years = ['2022', '2023', '2024']
const productionTypes = [
  { key: 'rigidSingle', label: '刚性单面板' },
  { key: 'rigidDouble', label: '刚性双面板' },
  { key: 'rigidMultilayer', label: '刚性多层板' },
  { key: 'flexibleSingle', label: '挠性单面板' },
  { key: 'flexibleDouble', label: '挠性双面板' },
  { key: 'flexibleMultilayer', label: '挠性多层板' }
]

// 确保输出数据结构完整
watch(() => props.modelValue, (newVal) => {
  if (newVal) {
    years.forEach(year => {
      if (!newVal.output[year]) {
        newVal.output[year] = {}
      }
      productionTypes.forEach(type => {
        if (!(type.key in newVal.output[year])) {
          newVal.output[year][type.key] = null
        }
      })
    })
  }
}, { immediate: true, deep: true })
</script>

<style scoped>
.production-info-form {
  padding: 16px 0;
}
</style>

