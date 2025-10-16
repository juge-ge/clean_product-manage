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
      
      <CrudTable
        ref="schemeTableRef"
        :columns="schemeColumns"
        :get-data="getSchemeList"
        :query-items="queryItems"
        :scroll-x="1400"
        :bordered="true"
        :single-line="false"
        size="small"
        :pagination="{
          page: 1,
          page_size: 20,
          pageSizes: [10, 20, 50, 100, 200],
          showSizePicker: true,
          prefix({ itemCount }) {
            return `共 ${itemCount} 条`
          }
        }"
      >
        <template #queryBar>
          <QueryBarItem label="方案名称">
            <n-input v-model:value="queryItems.name" placeholder="请输入方案名称" />
          </QueryBarItem>
          <QueryBarItem label="关联指标">
            <n-select
              v-model:value="queryItems.indicatorIds"
              :options="indicatorOptions"
              multiple
              filterable
              clearable
              :placeholder="selectedIndicatorCount > 0 ? `已选择${selectedIndicatorCount}个指标` : '请选择关联指标（支持搜索）'"
              :max-tag-count="2"
              style="width: 350px"
              :render-tag="({ option, handleClose }) => {
                return h('span', {
                  style: 'margin-right: 4px; background: #f0f9ff; border: 1px solid #0ea5e9; border-radius: 4px; padding: 2px 6px; font-size: 12px;'
                }, [
                  h('span', `${option.label}`),
                  h('span', {
                    style: 'margin-left: 4px; cursor: pointer; color: #0ea5e9; font-weight: bold;',
                    onClick: handleClose
                  }, '×')
                ])
              }"
            />
          </QueryBarItem>
        </template>
      </CrudTable>
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
  NTreeSelect,
  NSpace,
  NTooltip
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
import SchemeForm from './components/SchemeForm.vue'
// import { mockDetailApi } from '@/mock/pcb-detail'
import api from '@/api'

defineOptions({ name: '方案库' })

const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

const emit = defineEmits(['update', 'navigate'])

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

// 计算已选择的指标名称
const selectedIndicatorNames = computed(() => {
  return queryItems.value.indicatorIds.map(id => {
    const option = indicatorOptions.value.find(opt => opt.value === id)
    return option ? option.label : `指标${id}`
  })
})

// 扁平化的指标选项列表（用于可搜索下拉框）
const indicatorOptions = ref([
  // 生产工艺与装备要求
  { label: '基本要求', value: 1 },
  { label: '机械加工及辅助设施', value: 2 },
  { label: '线路与阻焊图形形成(印刷或感光工艺)', value: 3 },
  { label: '板面清洗', value: 4 },
  { label: '蚀刻', value: 5 },
  { label: '电镀与化学镀', value: 6 },
  
  // 能源消耗
  { label: '刚性印制电路单面板(单位产品电耗)', value: 7 },
  { label: '刚性印制电路双面板(单位产品电耗)', value: 8 },
  { label: '刚性印制电路多层板(2+n)层(单位产品电耗)', value: 9 },
  { label: '刚性印制电路HDI板(2+n)层(单位产品电耗)', value: 10 },
  { label: '挠性印制电路单面板(单位产品电耗)', value: 11 },
  { label: '挠性印制电路双面板(单位产品电耗)', value: 12 },
  { label: '挠性印制电路多层板(2+n)层(单位产品电耗)', value: 13 },
  { label: '挠性印制电路HDI板(2+n)层(单位产品电耗)', value: 14 },
  
  // 水资源消耗
  { label: '单面板(单位产品新鲜水耗)', value: 15 },
  { label: '双面板(单位产品新鲜水耗)', value: 16 },
  { label: '多层板(2+n)层(单位产品新鲜水耗)', value: 17 },
  { label: 'HDI板(2+n)层(单位产品新鲜水耗)', value: 18 },
  { label: '水资源重复利用率', value: 19 },
  
  // 原/辅料消耗
  { label: '刚性印制电路单面板 覆铜板利用率', value: 20 },
  { label: '刚性印制电路双面板 覆铜板利用率', value: 21 },
  { label: '刚性印制电路多层板(2+n)层覆铜板利用率', value: 22 },
  { label: '刚性印制电路HDI板(2+n)层覆铜板利用率', value: 23 },
  { label: '挠性印制电路单面板覆铜板利用率', value: 24 },
  { label: '挠性印制电路双面板 覆铜板利用率', value: 25 },
  { label: '挠性性印制电路多层板(2+n)层覆铜板利用率', value: 26 },
  { label: '挠性印制电路HDI板(2+n)层覆铜板利用率', value: 27 },
  
  // 资源综合利用
  { label: '金属铜回收率', value: 28 },
  { label: '一般工业固体废物综合利用率', value: 29 },
  
  // 废水的产生与排放
  { label: '单面板废水产生量', value: 30 },
  { label: '双面板废水产生量', value: 31 },
  { label: '多层板(2+n)层废水产生量', value: 32 },
  { label: 'HDI板(2+n)层废水产生量', value: 33 },
  { label: '单面板废水中铜产生量', value: 34 },
  { label: '双面板废水中铜产生量', value: 35 },
  { label: '多层板(2+n)层废水中铜产生量', value: 36 },
  { label: 'HDI板(2+n)层废水中铜产生量', value: 37 },
  { label: '单面板废水中COD产生量', value: 38 },
  { label: '双面板废水废水中COD产生量', value: 39 },
  { label: '多层板(2+n)层废水中 COD 产生量', value: 40 },
  { label: 'HDI板(2+n)层废水中 COD 产生量', value: 41 },
  { label: '废水收集与处理', value: 42 },
  
  // 废气的产生与排放
  { label: '废气收集与处理', value: 43 },
  { label: '废气中颗粒物产生量', value: 44 },
  { label: '废气中VOCs产生量', value: 45 },
  { label: '废气中酸雾产生量', value: 46 },
  
  // 温室气体排放
  { label: '单位产品CO2排放量', value: 47 },
  { label: '单位产品N2O排放量', value: 48 },
  { label: '单位产品CH4排放量', value: 49 },
  
  // 产品特征
  { label: '产品合格率', value: 50 },
  { label: '产品返修率', value: 51 },
  { label: '产品报废率', value: 52 },
  { label: '产品包装材料使用量', value: 53 },
  
  // 清洁生产管理
  { label: '环保法律法规执行情况', value: 54 },
  { label: '环境管理体系认证', value: 55 },
  { label: '清洁生产审核', value: 56 },
  { label: '清洁生产审核', value: 57 },
  { label: '节能管理', value: 58 },
  { label: '环境信息公开', value: 59 },
  { label: '环境风险管控', value: 60 },
  { label: '环境监测', value: 61 },
  { label: '环境应急管理', value: 62 },
  { label: '环境培训', value: 63 },
  { label: '环境投入', value: 64 }
])

// 保留原有的树形结构（用于其他功能）
const indicatorTreeOptions = ref([
  {
    label: '生产工艺与装备要求',
    key: 'process',
    children: [
      { label: '刚性单面板生产工艺', key: '1' },
      { label: '刚性双面板生产工艺', key: '2' },
      { label: '刚性多层板生产工艺', key: '3' },
      { label: '挠性单面板生产工艺', key: '4' },
      { label: '挠性双面板生产工艺', key: '5' },
      { label: '挠性多层板生产工艺', key: '6' }
    ]
  },
  {
    label: '资源能源消耗',
    key: 'resource',
    children: [
      { label: '单位产品电耗', key: '7' },
      { label: '单位产品新鲜水耗', key: '15' },
      { label: '水资源重复利用率', key: '19' },
      { label: '覆铜板利用率', key: '20' },
      { label: '金属铜回收率', key: '28' }
    ]
  },
  {
    label: '污染防治',
    key: 'pollution',
    children: [
      { label: '一般工业固体废物综合利用率', key: '29' },
      { label: '污染物产生量', key: '30' },
      { label: '污染治理设施', key: '42' }
    ]
  },
  {
    label: '环境管理',
    key: 'management',
    children: [
      { label: '温室气体排放', key: '47' },
      { label: '产品特征', key: '50' },
      { label: '环保法律法规执行情况', key: '54' },
      { label: '清洁生产审核', key: '57' },
      { label: '节能管理', key: '58' }
    ]
  }
])

// 表格列配置
const schemeColumns = [
  {
    title: '方案序号',
    key: 'id',
    width: 80,
    align: 'center',
    render: (row) => {
      return h('span', { style: { fontWeight: 'bold', color: '#1890ff', fontSize: '14px' } }, `方案${row.id}`)
    }
  },
  {
    title: '方案名称',
    key: 'name',
    width: 140,
    ellipsis: { tooltip: true },
    render: (row) => {
      return h('span', { style: { fontWeight: '500', fontSize: '14px' } }, row.name)
    }
  },
  {
    title: '解决问题',
    key: 'problemSolved',
    width: 120,
    ellipsis: { tooltip: true },
    render: (row) => {
      return h('span', { style: { fontSize: '14px' } }, row.problemSolved)
    }
  },
  {
    title: '方案简介',
    key: 'description',
    width: 160,
    ellipsis: { tooltip: true },
    render: (row) => {
      return h('span', { style: { fontSize: '14px' } }, row.description)
    }
  },
  {
    title: '经济效益',
    key: 'economicBenefit',
    width: 140,
    ellipsis: { tooltip: true },
    render: (row) => {
      return h('span', { style: { fontSize: '14px' } }, row.economicBenefit)
    }
  },
  {
    title: '环境效益',
    key: 'environmentalBenefit',
    width: 140,
    ellipsis: { tooltip: true },
    render: (row) => {
      return h('span', { style: { fontSize: '14px' } }, row.environmentalBenefit)
    }
  },
  {
    title: '主要应对指标编号',
    key: 'indicatorIds',
    width: 200,
    render: (row) => {
      if (!row.indicatorIds || row.indicatorIds.length === 0) {
        return '暂无指标'
      }
      
      // 显示前3个指标编号，超过3个显示省略号
      const displayIds = row.indicatorIds.slice(0, 3)
      const hasMore = row.indicatorIds.length > 3
      
      return h('div', {
        style: 'display: flex; align-items: center; gap: 4px;'
      }, [
        h('span', {
          style: 'white-space: nowrap; font-size: 12px;'
        }, displayIds.join(', ')),
        hasMore && h('span', {
          style: 'color: #999; font-size: 12px;'
        }, '...'),
        h(NTooltip, {
          trigger: 'hover',
          placement: 'top'
        }, {
          trigger: () => h('span', {
            style: 'cursor: help; color: #1890ff; font-size: 12px; margin-left: 4px;'
          }, '?'),
          default: () => `完整指标编号：${row.indicatorIds.join(', ')}`
        })
      ])
    }
  },
  {
    title: '主要对应指标名称',
    key: 'indicatorNames',
    width: 250,
    render: (row) => {
      if (!row.indicatorNames || row.indicatorNames.length === 0) {
        return '暂无指标'
      }
      
      // 显示前2个指标名称，超过2个显示省略号
      const displayNames = row.indicatorNames.slice(0, 2)
      const hasMore = row.indicatorNames.length > 2
      
      return h('div', {
        style: 'display: flex; align-items: center; gap: 4px;'
      }, [
        h('span', {
          style: 'white-space: nowrap; font-size: 12px;'
        }, displayNames.join(', ')),
        hasMore && h('span', {
          style: 'color: #999; font-size: 12px;'
        }, '...'),
        h(NTooltip, {
          trigger: 'hover',
          placement: 'top'
        }, {
          trigger: () => h('span', {
            style: 'cursor: help; color: #1890ff; font-size: 12px; margin-left: 4px;'
          }, '?'),
          default: () => `完整指标名称：${row.indicatorNames.join(', ')}`
        })
      ])
    }
  },
  {
    title: '操作',
    key: 'action',
    width: 140,
    fixed: 'right',
    render: (row) => {
      return h('div', { 
        style: 'display: flex; gap: 8px; align-items: center;' 
      }, [
        h('n-button', {
          size: 'small',
          type: 'primary',
          onClick: () => editScheme(row)
        }, {
          default: () => [
            h(TheIcon, { icon: 'carbon:edit', size: 14 }),
            ' 编辑'
          ]
        }),
        h('n-button', {
          size: 'small',
          type: 'error',
          onClick: () => deleteScheme(row.id)
        }, {
          default: () => [
            h(TheIcon, { icon: 'carbon:trash-can', size: 14 }),
            ' 删除'
          ]
        })
      ])
    }
  }
]

// 获取方案列表
const getSchemeList = async (params) => {
  try {
    const response = await api.pcb.scheme.getList(params)
    // CrudTable期望的格式：{ data: [], total: number }
    return {
      data: response.data.items || [],
      total: response.data.total || 0
    }
  } catch (error) {
    console.error('获取方案列表失败:', error)
    window.$message.error('获取方案列表失败')
    return { data: [], total: 0 }
  }
}

// 获取指标树数据
const fetchIndicatorTree = async () => {
  try {
    const response = await api.pcb.indicator.getTree()
    indicatorTreeOptions.value = response.data
  } catch (error) {
    console.error('获取指标树失败:', error)
  }
}

// 保存方案
const handleSaveScheme = async () => {
  try {
    const formData = await schemeFormRef.value.validate()
    if (isEdit.value) {
      await api.pcb.scheme.update(currentScheme.value.id, formData)
      window.$message.success('方案更新成功')
    } else {
      await api.pcb.scheme.create(formData)
      window.$message.success('方案添加成功')
    }
    showAddModal.value = false
    resetForm()
    emit('update', formData)
  } catch (error) {
    console.error('保存方案失败:', error)
    window.$message.error('保存方案失败')
  }
}

// 编辑方案
const editScheme = (scheme) => {
  isEdit.value = true
  currentScheme.value = { ...scheme }
  showAddModal.value = true
}

// 删除方案
const deleteScheme = async (schemeId) => {
  try {
    await window.$dialog.confirm({
      title: '确认删除',
      content: '确定要删除该方案吗？此操作不可恢复。'
    })
    await mockDetailApi.deleteScheme(props.enterpriseId, schemeId)
    window.$message.success('删除成功')
  } catch (error) {
    if (error) {
      console.error('删除失败:', error)
      window.$message.error('删除失败')
    }
  }
}

// 重置表单
const resetForm = () => {
  isEdit.value = false
  currentScheme.value = {}
}

// 处理添加按钮点击
const handleAddClick = () => {
  resetForm()
  showAddModal.value = true
}

// 导航方法
const goToPrevious = () => {
  emit('navigate', 'audit')
}

const goToNext = () => {
  emit('navigate', 'report')
}

onMounted(() => {
  fetchIndicatorTree()
  // 手动触发数据加载
  nextTick(() => {
    if (schemeTableRef.value) {
      schemeTableRef.value.handleSearch()
    }
  })
})
</script>

<style scoped>
.scheme-library {
  padding: 16px;
}

:deep(.n-form-item) {
  margin-bottom: 20px;
}

/* 优化选择器样式 */
:deep(.n-select) {
  .n-base-selection {
    border-radius: 6px;
    transition: all 0.3s ease;
  }
  
  .n-base-selection:hover {
    border-color: #0ea5e9;
    box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.1);
  }
  
  .n-base-selection--focused {
    border-color: #0ea5e9;
    box-shadow: 0 0 0 2px rgba(14, 165, 233, 0.2);
  }
}

/* 优化下拉选项样式 */
:deep(.n-select-menu) {
  .n-base-select-option {
    padding: 8px 12px;
    transition: all 0.2s ease;
  }
  
  .n-base-select-option:hover {
    background-color: #f0f9ff;
  }
  
  .n-base-select-option--selected {
    background-color: #e0f2fe;
    color: #0ea5e9;
  }
}

/* 优化搜索框样式 */
:deep(.n-base-selection-input) {
  .n-input {
    border: none;
    box-shadow: none;
  }
}

:deep(.n-form-item-label) {
  width: 120px;
  text-align: right;
  padding-right: 12px;
}

/* 表格样式优化 */
:deep(.n-data-table) {
  font-size: 12px;
}

:deep(.n-data-table .n-data-table-th) {
  font-size: 12px;
  font-weight: 600;
  padding: 8px 4px;
  white-space: nowrap;
}

:deep(.n-data-table .n-data-table-th) {
  font-size: 14px;
  font-weight: 600;
}

:deep(.n-data-table .n-data-table-td) {
  padding: 6px 4px;
  font-size: 12px;
}

/* 操作列按钮样式 */
:deep(.n-data-table .n-data-table-td .n-button) {
  font-size: 12px !important;
  padding: 4px 8px !important;
  height: 28px !important;
  min-width: 60px !important;
  font-weight: 500 !important;
  border-radius: 4px !important;
  display: inline-flex !important;
  align-items: center !important;
  gap: 4px !important;
  border: 1px solid !important;
  cursor: pointer !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1) !important;
}

/* 编辑按钮样式 */
:deep(.n-data-table .n-data-table-td .n-button[type="primary"]) {
  background-color: #1890ff !important;
  border-color: #1890ff !important;
  color: #ffffff !important;
}

:deep(.n-data-table .n-data-table-td .n-button[type="primary"]:hover) {
  background-color: #40a9ff !important;
  border-color: #40a9ff !important;
  box-shadow: 0 2px 4px rgba(24, 144, 255, 0.3) !important;
}

/* 删除按钮样式 */
:deep(.n-data-table .n-data-table-td .n-button[type="error"]) {
  background-color: #ff4d4f !important;
  border-color: #ff4d4f !important;
  color: #ffffff !important;
}

:deep(.n-data-table .n-data-table-td .n-button[type="error"]:hover) {
  background-color: #ff7875 !important;
  border-color: #ff7875 !important;
  box-shadow: 0 2px 4px rgba(255, 77, 79, 0.3) !important;
}

/* 操作列容器样式 */
:deep(.n-data-table .n-data-table-td > div) {
  display: flex !important;
  align-items: center !important;
  gap: 8px !important;
}

/* 确保表格可以水平滚动 */
:deep(.n-data-table-wrapper) {
  overflow-x: auto;
}

/* 表格容器样式 */
:deep(.n-card .n-card__content) {
  padding: 16px;
}

/* 查询栏样式 */
:deep(.n-card .n-card__header) {
  padding: 16px 16px 0 16px;
}
</style>
