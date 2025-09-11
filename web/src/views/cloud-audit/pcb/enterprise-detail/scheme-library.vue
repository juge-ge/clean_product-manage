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
        :columns="schemeColumns"
        :get-data="getSchemeList"
        :query-items="queryItems"
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
import { ref, onMounted, h } from 'vue'
import { 
  NCard, 
  NButton, 
  NInput,
  NTreeSelect,
  NSpace
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
    title: '方案名称',
    key: 'name',
    width: 200,
    ellipsis: { tooltip: true }
  },
  {
    title: '方案类型',
    key: 'type',
    width: 120,
    render: (row) => {
      return h('n-tag', { type: 'info' }, row.type)
    }
  },
  {
    title: '关联指标',
    key: 'indicatorIds',
    width: 150,
    render: (row) => {
      if (row.indicatorIds && row.indicatorIds.length > 0) {
        return h('n-tag', { type: 'default' }, `${row.indicatorIds.length}个指标`)
      }
      return '-'
    }
  },
  {
    title: '投资估算',
    key: 'investment',
    width: 120,
    render: (row) => {
      return h('span', `${row.investment || 0}万元`)
    }
  },
  {
    title: '投资回收期',
    key: 'paybackPeriod',
    width: 120,
    render: (row) => {
      return h('span', `${row.paybackPeriod || 0}年`)
    }
  },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render: (row) => {
      const statusMap = {
        active: { type: 'success', text: '启用' },
        inactive: { type: 'default', text: '禁用' }
      }
      const status = statusMap[row.status] || { type: 'default', text: '未知' }
      return h('n-tag', { type: status.type }, status.text)
    }
  },
  {
    title: '操作',
    key: 'action',
    width: 150,
    render: (row) => {
      return h('n-space', [
        h('n-button', {
          size: 'small',
          type: 'primary',
          onClick: () => editScheme(row)
        }, '编辑'),
        h('n-button', {
          size: 'small',
          type: 'error',
          onClick: () => deleteScheme(row.id)
        }, '删除')
      ])
    }
  }
]

// 获取方案列表
const getSchemeList = async (params) => {
  try {
    const response = await mockDetailApi.getSchemes(props.enterpriseId, params)
    return response.data
  } catch (error) {
    console.error('获取方案列表失败:', error)
    window.$message.error('获取方案列表失败')
    return { list: [], total: 0 }
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
</style>
