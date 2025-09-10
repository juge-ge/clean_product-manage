<template>
  <div class="scheme-library">
    <n-card title="清洁生产方案库">
      <template #header-extra>
        <n-button type="primary" @click="showAddModal = true">
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
          <QueryBarItem label="指标名称">
            <n-input v-model:value="queryItems.indicatorName" placeholder="请输入指标名称" />
          </QueryBarItem>
          <QueryBarItem label="方案类型">
            <n-select v-model:value="queryItems.schemeType" :options="schemeTypeOptions" />
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
      <n-form ref="schemeFormRef" :model="schemeForm" :rules="schemeRules">
        <n-form-item label="指标名称" path="indicatorName">
          <n-input v-model:value="schemeForm.indicatorName" placeholder="请输入指标名称" />
        </n-form-item>
        <n-form-item label="方案类型" path="schemeType">
          <n-select
            v-model:value="schemeForm.schemeType"
            :options="schemeTypeOptions"
            placeholder="请选择方案类型"
          />
        </n-form-item>
        <n-form-item label="方案标题" path="title">
          <n-input v-model:value="schemeForm.title" placeholder="请输入方案标题" />
        </n-form-item>
        <n-form-item label="方案描述" path="description">
          <n-input
            v-model:value="schemeForm.description"
            type="textarea"
            placeholder="请输入方案描述"
            :rows="3"
          />
        </n-form-item>
        <n-form-item label="实施方案" path="implementation">
          <n-input
            v-model:value="schemeForm.implementation"
            type="textarea"
            placeholder="请输入实施方案"
            :rows="4"
          />
        </n-form-item>
        <n-form-item label="预期效果" path="expectedEffect">
          <n-input
            v-model:value="schemeForm.expectedEffect"
            type="textarea"
            placeholder="请输入预期效果"
            :rows="3"
          />
        </n-form-item>
        <n-form-item label="投资估算" path="investment">
          <n-input-number
            v-model:value="schemeForm.investment"
            placeholder="请输入投资估算"
            :min="0"
            :precision="2"
          >
            <template #suffix>万元</template>
          </n-input-number>
        </n-form-item>
        <n-form-item label="投资回收期" path="paybackPeriod">
          <n-input-number
            v-model:value="schemeForm.paybackPeriod"
            placeholder="请输入投资回收期"
            :min="0"
            :precision="1"
          >
            <template #suffix>年</template>
          </n-input-number>
        </n-form-item>
      </n-form>
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
import { ref, onMounted } from 'vue'
import { 
  NCard, 
  NButton, 
  NForm, 
  NFormItem,
  NInput,
  NInputNumber,
  NSelect
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import CrudTable from '@/components/table/CrudTable.vue'
import CrudModal from '@/components/table/CrudModal.vue'
import QueryBarItem from '@/components/query-bar/QueryBarItem.vue'
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
const queryItems = ref({
  indicatorName: '',
  schemeType: null
})

// 表单数据
const schemeForm = ref({
  indicatorName: '',
  schemeType: null,
  title: '',
  description: '',
  implementation: '',
  expectedEffect: '',
  investment: null,
  paybackPeriod: null
})

// 选项数据
const schemeTypeOptions = [
  { label: '节能降耗', value: '节能降耗' },
  { label: '污染防治', value: '污染防治' },
  { label: '资源综合利用', value: '资源综合利用' },
  { label: '工艺改进', value: '工艺改进' },
  { label: '设备更新', value: '设备更新' }
]

// 表格列配置
const schemeColumns = [
  {
    title: '指标名称',
    key: 'indicatorName',
    width: 150
  },
  {
    title: '方案类型',
    key: 'schemeType',
    width: 120,
    render: (row) => {
      return h('n-tag', { type: 'info' }, row.schemeType)
    }
  },
  {
    title: '方案标题',
    key: 'title',
    width: 200,
    ellipsis: { tooltip: true }
  },
  {
    title: '投资估算',
    key: 'investment',
    width: 120,
    render: (row) => {
      return h('span', `${row.investment}万元`)
    }
  },
  {
    title: '投资回收期',
    key: 'paybackPeriod',
    width: 120,
    render: (row) => {
      return h('span', `${row.paybackPeriod}年`)
    }
  },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render: (row) => {
      const statusMap = {
        pending: { type: 'default', text: '待实施' },
        'in-progress': { type: 'info', text: '实施中' },
        completed: { type: 'success', text: '已完成' }
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

// 表单验证规则
const schemeRules = {
  indicatorName: { required: true, message: '请输入指标名称', trigger: 'blur' },
  schemeType: { required: true, message: '请选择方案类型', trigger: 'change' },
  title: { required: true, message: '请输入方案标题', trigger: 'blur' },
  description: { required: true, message: '请输入方案描述', trigger: 'blur' },
  implementation: { required: true, message: '请输入实施方案', trigger: 'blur' },
  expectedEffect: { required: true, message: '请输入预期效果', trigger: 'blur' },
  investment: { required: true, message: '请输入投资估算', trigger: 'change' },
  paybackPeriod: { required: true, message: '请输入投资回收期', trigger: 'change' }
}

// 获取方案列表
const getSchemeList = async (params) => {
  try {
    const response = await mockDetailApi.getSchemes(props.enterpriseId)
    return response.data
  } catch (error) {
    console.error('获取方案列表失败:', error)
    window.$message.error('获取方案列表失败')
    return []
  }
}

// 保存方案
const handleSaveScheme = async () => {
  try {
    if (isEdit.value) {
      await mockDetailApi.updateScheme(props.enterpriseId, schemeForm.value.id, schemeForm.value)
      window.$message.success('方案更新成功')
    } else {
      await mockDetailApi.createScheme(props.enterpriseId, schemeForm.value)
      window.$message.success('方案添加成功')
    }
    showAddModal.value = false
    emit('update', schemeForm.value)
  } catch (error) {
    console.error('保存方案失败:', error)
    window.$message.error('保存方案失败')
  }
}

// 编辑方案
const editScheme = (scheme) => {
  isEdit.value = true
  schemeForm.value = { ...scheme }
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

// 导航方法
const goToPrevious = () => {
  emit('navigate', 'audit')
}

const goToNext = () => {
  emit('navigate', 'report')
}

onMounted(() => {
  // 初始化数据
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
