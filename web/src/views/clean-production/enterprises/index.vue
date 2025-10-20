<template>
  <div class="enterprises-container">
    <n-card title="企业管理" :bordered="false">
      <template #header-extra>
        <n-space>
          <n-input
            v-model:value="searchKeyword"
            placeholder="搜索企业名称"
            style="width: 200px"
            clearable
          />
          <n-button type="primary" @click="handleSearch">搜索</n-button>
          <n-button @click="handleAdd">新增企业</n-button>
        </n-space>
      </template>

      <n-data-table
        :columns="columns"
        :data="enterprises"
        :pagination="paginationConfig"
        :bordered="false"
      />
    </n-card>
  </div>
</template>

<script setup>
import { ref, h } from 'vue'

defineOptions({ name: '企业' })

const searchKeyword = ref('')

const paginationConfig = {
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 50]
}

const columns = [
  {
    title: '企业名称',
    key: 'name',
    width: 200
  },
  {
    title: '所属行业',
    key: 'industry',
    width: 120
  },
  {
    title: '所在地区',
    key: 'region',
    width: 100
  },
  {
    title: '企业规模',
    key: 'scale',
    width: 100
  },
  {
    title: '联系人',
    key: 'contact',
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
        onClick: () => editEnterprise(row)
      }, { default: () => '编辑' })
    ]
  }
]

const enterprises = ref([
  {
    id: 1,
    name: '北京钢铁集团有限公司',
    industry: '钢铁',
    region: '北京',
    scale: '大型',
    contact: '张经理',
    phone: '010-12345678'
  },
  {
    id: 2,
    name: '上海化工股份有限公司',
    industry: '化工',
    region: '上海',
    scale: '中型',
    contact: '王总',
    phone: '021-87654321'
  },
  {
    id: 3,
    name: '广东建材有限公司',
    industry: '建材',
    region: '广东',
    scale: '小型',
    contact: '刘主任',
    phone: '020-11111111'
  }
])

const handleSearch = () => {
  console.log('搜索企业:', searchKeyword.value)
}

const handleAdd = () => {
  console.log('新增企业')
}

const viewDetail = (enterprise) => {
  console.log('查看企业详情:', enterprise)
}

const editEnterprise = (enterprise) => {
  console.log('编辑企业:', enterprise)
}
</script>

<style scoped>
.enterprises-container {
  padding: 16px;
}
</style>
