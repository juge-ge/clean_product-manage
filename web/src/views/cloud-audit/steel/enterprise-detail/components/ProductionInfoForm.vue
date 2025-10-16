<template>
  <div class="production-info-form">
    <n-form-item label="年产钢量（万吨）">
      <n-input-number 
        v-model:value="formData.capacity"
        placeholder="请输入年产钢量"
        :min="0"
        :precision="2"
        style="width: 200px"
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
          <n-form-item-gi label="粗钢产量（万吨）">
            <n-input-number 
              v-model:value="formData.output[year].crudeSteel"
              placeholder="请输入产量"
              :min="0"
              :precision="2"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="钢材产量（万吨）">
            <n-input-number 
              v-model:value="formData.output[year].steelProducts"
              placeholder="请输入产量"
              :min="0"
              :precision="2"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="生铁产量（万吨）">
            <n-input-number 
              v-model:value="formData.output[year].pigIron"
              placeholder="请输入产量"
              :min="0"
              :precision="2"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="焦炭产量（万吨）">
            <n-input-number 
              v-model:value="formData.output[year].coke"
              placeholder="请输入产量"
              :min="0"
              :precision="2"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="烧结矿产量（万吨）">
            <n-input-number 
              v-model:value="formData.output[year].sinterOre"
              placeholder="请输入产量"
              :min="0"
              :precision="2"
            />
          </n-form-item-gi>
          
          <n-form-item-gi label="球团矿产量（万吨）">
            <n-input-number 
              v-model:value="formData.output[year].pellet"
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
import { computed } from 'vue'
import { NFormItem, NInputNumber, NTabs, NTabPane, NGrid, NFormItemGi } from 'naive-ui'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      capacity: null,
      output: {
        '2022': {
          crudeSteel: null,
          steelProducts: null,
          pigIron: null,
          coke: null,
          sinterOre: null,
          pellet: null
        },
        '2023': {
          crudeSteel: null,
          steelProducts: null,
          pigIron: null,
          coke: null,
          sinterOre: null,
          pellet: null
        },
        '2024': {
          crudeSteel: null,
          steelProducts: null,
          pigIron: null,
          coke: null,
          sinterOre: null,
          pellet: null
        }
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
</script>

<style scoped>
.production-info-form {
  padding: 16px;
}
</style>
