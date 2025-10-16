<template>
  <div class="regulation-tabs">
    <n-tabs v-model:value="activeTab" type="line" animated>
      <n-tab-pane 
        v-for="tab in tabs" 
        :key="tab.key" 
        :name="tab.key"
        :tab="tab.label"
      >
        <template #tab>
          <n-icon><i :class="tab.icon" /></n-icon>
          {{ tab.label }}
        </template>
        <regulation-list 
          :category="tab.key" 
          :search-keyword="searchKeyword"
          @search="handleSearch"
          @item-click="handleItemClick"
        />
      </n-tab-pane>
    </n-tabs>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import RegulationList from './RegulationList.vue'
import { regulationTabs } from '../data/mockData.js'

const props = defineProps({
  modelValue: {
    type: String,
    default: 'national'
  },
  searchKeyword: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['update:modelValue', 'search', 'item-click'])

const activeTab = ref(props.modelValue)
const tabs = regulationTabs

const handleSearch = (keyword) => {
  emit('search', keyword)
}

const handleItemClick = (item) => {
  emit('item-click', item)
}

// 监听activeTab变化
watch(activeTab, (newValue) => {
  emit('update:modelValue', newValue)
})

// 监听props变化
watch(() => props.modelValue, (newValue) => {
  activeTab.value = newValue
})
</script>

<style scoped>
.regulation-tabs {
  width: 100%;
}

:deep(.n-tabs-nav) {
  margin-bottom: 16px;
}

:deep(.n-tabs-tab) {
  font-size: 14px;
  font-weight: 500;
}

:deep(.n-tabs-tab .n-icon) {
  margin-right: 6px;
}

:deep(.n-tabs-content) {
  padding: 0;
}
</style>
