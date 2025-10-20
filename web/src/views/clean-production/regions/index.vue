<template>
  <div class="regions-container">
    <n-card title="区域管理" :bordered="false">
      <template #header-extra>
        <n-space>
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索区域名称"
            style="width: 200px"
            clearable
          />
          <n-button type="primary" @click="handleSearch">搜索</n-button>
          <n-button @click="handleAdd">新增区域</n-button>
        </n-space>
      </template>

      <n-data-table
        :columns="columns"
        :data="regions"
        :pagination="paginationConfig"
        :bordered="false"
      />
    </n-card>
  </div>
</template>

<script setup>
import { ref, h } from 'vue'

defineOptions({ name: '区域' })

const searchKeyword = ref('')

const paginationConfig = {
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50]
}

const columns = [
  {
    title: '区域名称',
    key: 'name',
    width: 150
  },
  {
    title: '区域类型',
    key: 'type',
    width: 120
  },
  {
    title: '所属省份',
    key: 'province',
    width: 120
  },
  {
    title: '企业数量',
    key: 'enterpriseCount',
    width: 100
  },
  {
    title: '园区数量',
    key: 'parkCount',
    width: 100
  },
  {
    title: '负责人',
    key: 'manager',
    width: 100
  },
  {
    title: '联系电话',
    key: 'phone',
    width: 120
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
        onClick: () => editRegion(row)
      }, { default: () => '编辑' })
    ]
  }
]

const regions = ref([
  {
    id: 1,
    name: '北京市',
    type: '直辖市',
    province: '北京',
    enterpriseCount: 1200,
    parkCount: 15,
    manager: '李主任',
    phone: '010-12345678'
  },
  {
    id: 2,
    name: '上海市',
    type: '直辖市',
    province: '上海',
    enterpriseCount: 800,
    parkCount: 12,
    manager: '王主任',
    phone: '021-87654321'
  },
  {
    id: 3,
    name: '深圳市',
    type: '地级市',
    province: '广东',
    enterpriseCount: 600,
    parkCount: 8,
    manager: '刘主任',
    phone: '0755-11111111'
  }
])

const handleSearch = () => {
  console.log('搜索区域:', searchKeyword.value)
}

const handleAdd = () => {
  console.log('新增区域')
}

const viewDetail = (region) => {
  console.log('查看区域详情:', region)
}

const editRegion = (region) => {
  console.log('编辑区域:', region)
}
</script>

<style scoped>
.regions-container {
  padding: 16px;
}
</style>
