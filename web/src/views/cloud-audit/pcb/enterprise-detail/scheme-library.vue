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
          pageSize: 20,
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
            <n-tree-select 
              v-model:value="queryItems.indicatorIds"
              :options="indicatorTreeOptions"
              multiple
              checkable
              placeholder="请选择关联指标"
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
import { ref, onMounted, h, nextTick } from 'vue'
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
import { mockDetailApi } from '@/mock/pcb-detail'

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

// 指标树选项
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
    const response = await mockDetailApi.getSchemes(props.enterpriseId, params)
    // CrudTable期望的格式：{ data: [], total: number }
    return {
      data: response.data.list || [],
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
    const response = await mockDetailApi.getIndicatorTree()
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
      await mockDetailApi.updateScheme(props.enterpriseId, currentScheme.value.id, formData)
      window.$message.success('方案更新成功')
    } else {
      await mockDetailApi.createScheme(props.enterpriseId, formData)
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
