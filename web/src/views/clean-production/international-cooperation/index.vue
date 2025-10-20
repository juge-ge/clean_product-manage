<template>
  <div class="international-cooperation-container">
    <n-card title="国际合作" :bordered="false">
      <template #header-extra>
        <n-space>
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索合作项目"
            style="width: 200px"
            clearable
          />
          <n-button type="primary" @click="handleSearch">搜索</n-button>
          <n-button @click="handleAdd">新增合作</n-button>
        </n-space>
      </template>

      <n-data-table
        :columns="columns"
        :data="cooperations"
        :pagination="paginationConfig"
        :bordered="false"
      />
    </n-card>
  </div>
</template>

<script setup>
import { ref, h } from 'vue'

defineOptions({ name: '国际合作' })

const searchKeyword = ref('')

const paginationConfig = {
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50]
}

const columns = [
  {
    title: '项目名称',
    key: 'name',
    width: 200
  },
  {
    title: '合作国家',
    key: 'country',
    width: 120
  },
  {
    title: '合作类型',
    key: 'type',
    width: 120
  },
  {
    title: '开始时间',
    key: 'startDate',
    width: 120
  },
  {
    title: '结束时间',
    key: 'endDate',
    width: 120
  },
  {
    title: '项目状态',
    key: 'status',
    width: 100
  },
  {
    title: '负责人',
    key: 'manager',
    width: 100
  },
  {
    title: '操作',
    key: 'actions',
    width: 150,
    render: (row) => [
      h('n-button', {
        size: 'small',
        type: 'primary',
        style: 'margin-right: 8px',
        onClick: () => viewDetail(row)
      }, { default: () => '查看' }),
      h('n-button', {
        size: 'small',
        type: 'info',
        onClick: () => editCooperation(row)
      }, { default: () => '编辑' })
    ]
  }
]

const cooperations = ref([
  {
    id: 1,
    name: '中美清洁生产技术交流项目',
    country: '美国',
    type: '技术交流',
    startDate: '2024-01-01',
    endDate: '2024-12-31',
    status: '进行中',
    manager: '张专家'
  },
  {
    id: 2,
    name: '中德环保技术合作项目',
    country: '德国',
    type: '技术合作',
    startDate: '2023-06-01',
    endDate: '2025-05-31',
    status: '进行中',
    manager: '李专家'
  },
  {
    id: 3,
    name: '中日清洁生产培训项目',
    country: '日本',
    type: '人员培训',
    startDate: '2023-03-01',
    endDate: '2023-12-31',
    status: '已完成',
    manager: '王专家'
  }
])

const handleSearch = () => {
  console.log('搜索合作项目:', searchKeyword.value)
}

const handleAdd = () => {
  console.log('新增合作项目')
}

const viewDetail = (cooperation) => {
  console.log('查看合作详情:', cooperation)
}

const editCooperation = (cooperation) => {
  console.log('编辑合作项目:', cooperation)
}
</script>

<style scoped>
.international-cooperation-container {
  padding: 16px;
}
</style>
