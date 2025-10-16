<template>
  <div class="process-equipment-form">
    <n-grid :cols="2" :x-gap="24">
      <n-form-item-gi label="烧结工艺">
        <n-grid :cols="2" :x-gap="12">
          <n-form-item-gi label="生产能力">
            <n-input v-model:value="formData.sintering.capacity" placeholder="如：600万吨/年" />
          </n-form-item-gi>
          <n-form-item-gi label="主要设备">
            <n-input v-model:value="formData.sintering.equipment" placeholder="如：烧结机" />
          </n-form-item-gi>
          <n-form-item-gi label="投产年份">
            <n-input v-model:value="formData.sintering.year" placeholder="如：2015" />
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
      
      <n-form-item-gi label="球团工艺">
        <n-grid :cols="2" :x-gap="12">
          <n-form-item-gi label="生产能力">
            <n-input v-model:value="formData.pelletizing.capacity" placeholder="如：300万吨/年" />
          </n-form-item-gi>
          <n-form-item-gi label="主要设备">
            <n-input v-model:value="formData.pelletizing.equipment" placeholder="如：球团机" />
          </n-form-item-gi>
          <n-form-item-gi label="投产年份">
            <n-input v-model:value="formData.pelletizing.year" placeholder="如：2016" />
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
      
      <n-form-item-gi label="焦化工艺">
        <n-grid :cols="2" :x-gap="12">
          <n-form-item-gi label="生产能力">
            <n-input v-model:value="formData.coking.capacity" placeholder="如：200万吨/年" />
          </n-form-item-gi>
          <n-form-item-gi label="主要设备">
            <n-input v-model:value="formData.coking.equipment" placeholder="如：焦炉" />
          </n-form-item-gi>
          <n-form-item-gi label="投产年份">
            <n-input v-model:value="formData.coking.year" placeholder="如：2014" />
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
      
      <n-form-item-gi label="炼铁工艺">
        <n-grid :cols="2" :x-gap="12">
          <n-form-item-gi label="生产能力">
            <n-input v-model:value="formData.ironMaking.capacity" placeholder="如：500万吨/年" />
          </n-form-item-gi>
          <n-form-item-gi label="主要设备">
            <n-input v-model:value="formData.ironMaking.equipment" placeholder="如：高炉" />
          </n-form-item-gi>
          <n-form-item-gi label="投产年份">
            <n-input v-model:value="formData.ironMaking.year" placeholder="如：2013" />
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
      
      <n-form-item-gi label="炼钢工艺">
        <n-grid :cols="2" :x-gap="12">
          <n-form-item-gi label="生产能力">
            <n-input v-model:value="formData.steelMaking.capacity" placeholder="如：500万吨/年" />
          </n-form-item-gi>
          <n-form-item-gi label="主要设备">
            <n-input v-model:value="formData.steelMaking.equipment" placeholder="如：转炉" />
          </n-form-item-gi>
          <n-form-item-gi label="投产年份">
            <n-input v-model:value="formData.steelMaking.year" placeholder="如：2014" />
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
      
      <n-form-item-gi label="轧钢工艺">
        <n-grid :cols="2" :x-gap="12">
          <n-form-item-gi label="生产能力">
            <n-input v-model:value="formData.rolling.capacity" placeholder="如：450万吨/年" />
          </n-form-item-gi>
          <n-form-item-gi label="主要设备">
            <n-input v-model:value="formData.rolling.equipment" placeholder="如：轧机" />
          </n-form-item-gi>
          <n-form-item-gi label="投产年份">
            <n-input v-model:value="formData.rolling.year" placeholder="如：2015" />
          </n-form-item-gi>
        </n-grid>
      </n-form-item-gi>
    </n-grid>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { NFormItemGi, NGrid, NInput } from 'naive-ui'

const props = defineProps({
  modelValue: {
    type: Object,
    default: () => ({
      sintering: { capacity: '', equipment: '', year: '' },
      pelletizing: { capacity: '', equipment: '', year: '' },
      coking: { capacity: '', equipment: '', year: '' },
      ironMaking: { capacity: '', equipment: '', year: '' },
      steelMaking: { capacity: '', equipment: '', year: '' },
      rolling: { capacity: '', equipment: '', year: '' }
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
.process-equipment-form {
  padding: 16px;
}
</style>
