<template>
  <div class="scheme-library">
    <n-card title="清洁生产方案库">
      <template #header-extra>
        <n-button type="primary" @click="handleAddClick">
          <template #icon>
            <TheIcon icon="carbon:add" />
          </template>
          添加方案
        </n-button>
      </template>
      
      <!-- 查询栏 -->
      <div class="query-bar mb-4">
        <n-space>
          <n-input 
            v-model:value="queryItems.name" 
            placeholder="请输入方案名称"
            clearable
            style="width: 200px"
            @input="handleSearch"
          />
          <n-select
            v-model:value="queryItems.indicatorIds"
            :options="indicatorOptions"
            multiple
            filterable
            clearable
            :placeholder="selectedIndicatorCount > 0 ? `已选择${selectedIndicatorCount}个指标` : '请选择关联指标（支持搜索）'"
            :max-tag-count="2"
            style="width: 350px"
            @update:value="handleSearch"
          />
          <n-button @click="handleReset">重置</n-button>
        </n-space>
      </div>
      
      <!-- 方案表格（带内置滚动） -->
      <div class="scheme-table-container">
        <n-data-table
          ref="schemeTableRef"
          :columns="schemeColumns"
          :data="schemeList"
          :loading="loading"
          :scroll-x="1400"
          :bordered="true"
          :single-line="false"
          size="small"
          :pagination="false"
        />
      </div>
    </n-card>
    
    <!-- 添加/编辑方案弹窗 -->
    <CrudModal
      v-model:visible="showAddModal"
      :title="isEdit ? '编辑方案' : '添加方案'"
      @save="handleSaveScheme"
    >
      <SchemeForm ref="schemeFormRef" :data="currentScheme" />
    </CrudModal>

    <!-- 模块导航按钮 -->
    <div class="module-navigation mt-4">
      <n-space justify="space-between">
        <n-button @click="goToPrevious">
          <template #icon>
            <TheIcon icon="carbon:arrow-left" />
          </template>
          审核
        </n-button>
        <n-button type="primary" @click="goToNext">
          审核报告
          <template #icon>
            <TheIcon icon="carbon:arrow-right" />
          </template>
        </n-button>
      </n-space>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, h, nextTick, computed } from 'vue'
import { 
  NCard, 
  NButton, 
  NInput,
  NSelect,
  NSpace,
  NTooltip
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import SchemeForm from './components/SchemeForm.vue'
import { mockDetailApi } from '@/mock/steel-detail'

defineOptions({ name: '钢铁方案库' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

// 导航函数
const goToPrevious = () => {
  emit('navigate', 'audit')
}

const goToNext = () => {
  emit('navigate', 'report')
}

// 数据状态
const showAddModal = ref(false)
const isEdit = ref(false)
const schemeFormRef = ref(null)
const schemeTableRef = ref(null)
const currentScheme = ref({})

const queryItems = ref({
  name: '',
  indicatorIds: []
})

// 计算已选择的指标数量
const selectedIndicatorCount = computed(() => {
  return queryItems.value.indicatorIds.length
})

// 扁平化的指标选项列表（用于可搜索下拉框）
const indicatorOptions = ref([
  // 生产工艺与装备
  { label: '烧结工艺装备', value: 1 },
  { label: '球团工艺装备', value: 2 },
  { label: '炼铁工艺装备', value: 3 },
  { label: '炼钢工艺装备', value: 4 },
  { label: '轧钢工艺装备', value: 5 },
  { label: '能源回收利用装置', value: 6 },
  
  // 资源能源消耗
  { label: '吨钢综合能耗', value: 7 },
  { label: '吨钢电耗', value: 8 },
  { label: '吨钢新水消耗', value: 9 },
  { label: '焦化工序能耗', value: 10 },
  { label: '烧结工序能耗', value: 11 },
  { label: '球团工序能耗', value: 12 },
  { label: '炼铁工序能耗', value: 13 },
  { label: '炼钢工序能耗', value: 14 },
  { label: '轧钢工序能耗', value: 15 },
  { label: '水循环利用率', value: 16 },
  { label: '固体废弃物资源综合利用率', value: 17 },
  
  // 污染物产生
  { label: '吨钢COD产生量', value: 18 },
  { label: '吨钢氨氮产生量', value: 19 },
  { label: '吨钢SO₂产生量', value: 20 },
  { label: '吨钢NOx产生量', value: 21 },
  { label: '吨钢烟粉尘产生量', value: 22 },
  { label: '吨钢废水产生量', value: 23 },
  
  // 废物回收利用
  { label: '废钢利用率', value: 24 },
  { label: '高炉煤气回收利用率', value: 25 },
  { label: '转炉煤气回收利用率', value: 26 },
  { label: '焦炉煤气回收利用率', value: 27 },
  { label: '余热余压利用率', value: 28 },
  
  // 环境管理
  { label: '环保法律法规执行情况', value: 29 },
  { label: '产业政策符合性', value: 30 },
  { label: '清洁生产管理', value: 31 },
  { label: '环境管理体系认证', value: 32 },
  { label: '能源管理体系认证', value: 33 },
  { label: '污染物排放监测', value: 34 },
  { label: '危险废物处置', value: 35 },
  { label: '节能管理', value: 36 },
  { label: '碳排放管理', value: 37 },
  { label: '清洁生产审核', value: 38 }
])

// 方案列表数据
const schemeList = ref([])
const loading = ref(false)

// 表格列定义
const schemeColumns = [
  { title: '方案名称', key: 'name', width: 200, ellipsis: true },
  { title: '方案类型', key: 'type', width: 120 },
  { title: '投资估算', key: 'investment', width: 120, render: (row) => `${row.investment}万元` },
  { title: '投资回收期', key: 'paybackPeriod', width: 120, render: (row) => `${row.paybackPeriod}年` },
  { title: '方案描述', key: 'description', width: 300, ellipsis: true },
  { title: '解决问题', key: 'problemSolved', width: 200, ellipsis: true },
  { title: '经济效益', key: 'economicBenefit', width: 200, ellipsis: true },
  { title: '环境效益', key: 'environmentalBenefit', width: 200, ellipsis: true },
  { title: '关联指标', key: 'indicatorNames', width: 200, ellipsis: true },
  { 
    title: '操作', 
    key: 'action', 
    width: 150,
    fixed: 'right',
    render: (row) => h('div', { class: 'action-buttons' }, [
      h('n-button', {
        size: 'small',
        type: 'info',
        onClick: () => handleEdit(row)
      }, '编辑'),
      h('n-button', {
        size: 'small',
        type: 'error',
        style: 'margin-left: 8px',
        onClick: () => handleDelete(row.id)
      }, '删除')
    ])
  }
]

// 获取方案列表
const fetchSchemes = async () => {
  try {
    loading.value = true
    const response = await mockDetailApi.getSchemes(props.enterpriseId, {
      name: queryItems.value.name,
      indicatorIds: queryItems.value.indicatorIds
    })
    schemeList.value = response.data.list || []
  } catch (error) {
    console.error('获取方案列表失败:', error)
    window.$message.error('获取方案列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  fetchSchemes()
}

// 重置搜索
const handleReset = () => {
  queryItems.value = {
    name: '',
    indicatorIds: []
  }
  fetchSchemes()
}

// 添加方案
const handleAddClick = () => {
  isEdit.value = false
  currentScheme.value = {}
  showAddModal.value = true
}

// 编辑方案
const handleEdit = (scheme) => {
  isEdit.value = true
  currentScheme.value = { ...scheme }
  showAddModal.value = true
}

// 删除方案
const handleDelete = async (schemeId) => {
  try {
    await window.$dialog.confirm({
      title: '确认删除',
      content: '确定要删除该方案吗？此操作不可恢复。'
    })
    await mockDetailApi.deleteScheme(props.enterpriseId, schemeId)
    window.$message.success('删除成功')
    fetchSchemes()
  } catch (error) {
    if (error) {
      console.error('删除失败:', error)
      window.$message.error('删除失败')
    }
  }
}

// 保存方案
const handleSaveScheme = async () => {
  try {
    const formData = schemeFormRef.value?.formData
    if (!formData) return
    
    if (isEdit.value) {
      await mockDetailApi.updateScheme(props.enterpriseId, currentScheme.value.id, formData)
      window.$message.success('方案更新成功')
    } else {
      await mockDetailApi.createScheme(props.enterpriseId, formData)
      window.$message.success('方案创建成功')
    }
    
    showAddModal.value = false
    fetchSchemes()
  } catch (error) {
    console.error('保存方案失败:', error)
    window.$message.error('保存方案失败')
  }
}

onMounted(() => {
  fetchSchemes()
})
</script>

<style scoped>
.scheme-library {
  padding: 16px;
}

.scheme-table-container {
  margin-bottom: 16px;
  max-height: 600px;
  overflow-y: auto;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
}

.query-bar {
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 16px;
}

/* 优化滚动条样式 */
:deep(.n-data-table .n-data-table-base-table-body) {
  scrollbar-width: thin;
  scrollbar-color: #c1c1c1 #f1f1f1;
}

.action-buttons {
  display: flex;
  align-items: center;
}
</style>
