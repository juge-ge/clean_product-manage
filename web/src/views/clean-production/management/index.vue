<template>
  <AppPage :show-footer="false">
    <div flex-1>
      <n-card rounded-10>
        <div flex items-center justify-between>
          <div flex items-center>
            <TheIcon icon="carbon:enterprise" :size="24" class="mr-10" />
            <h2 text-20 font-semibold>企业信息管理</h2>
          </div>
          <n-space :size="12" :wrap="false">
            <n-button type="primary" @click="handleAdd">
              <TheIcon icon="material-symbols:add" :size="18" class="mr-5" />
              新增企业
            </n-button>
          </n-space>
        </div>
      </n-card>

      <n-card
        title="企业列表"
        size="small"
        :segmented="true"
        mt-15
        rounded-10
      >
        <template #header-extra>
          <n-button text type="primary">更多</n-button>
        </template>
        
        <!-- 企业信息表格 -->
        <n-data-table
          :columns="columns"
          :data="tableData"
          :pagination="pagination"
          :bordered="false"
          striped
        />
      </n-card>
    </div>
  </AppPage>
</template>

<script setup>
import { h, ref } from 'vue'
import { NButton, NTag, NSpace } from 'naive-ui'
import { renderIcon } from '@/utils'

defineOptions({ name: '企业信息管理' })

// 表格数据
const tableData = ref([
  {
    id: 1,
    name: '环保科技有限公司',
    code: 'EP001',
    type: '制造业',
    address: '北京市朝阳区',
    contact: '张经理',
    phone: '13800138000',
    status: 'active',
    createTime: '2024-01-15'
  },
  {
    id: 2,
    name: '绿色能源集团',
    code: 'EP002',
    type: '能源业',
    address: '上海市浦东新区',
    contact: '李总监',
    phone: '13900139000',
    status: 'active',
    createTime: '2024-01-20'
  },
  {
    id: 3,
    name: '清洁生产示范企业',
    code: 'EP003',
    type: '化工业',
    address: '广州市天河区',
    contact: '王主任',
    phone: '13700137000',
    status: 'inactive',
    createTime: '2024-01-25'
  }
])

// 分页配置
const pagination = ref({
  page: 1,
  pageSize: 10,
  showSizePicker: true,
  pageSizes: [10, 20, 30, 40],
  onChange: (page) => {
    pagination.value.page = page
  },
  onUpdatePageSize: (pageSize) => {
    pagination.value.pageSize = pageSize
    pagination.value.page = 1
  }
})

// 表格列配置
const columns = [
  {
    title: '企业名称',
    key: 'name',
    width: 200
  },
  {
    title: '企业编码',
    key: 'code',
    width: 120
  },
  {
    title: '企业类型',
    key: 'type',
    width: 120
  },
  {
    title: '地址',
    key: 'address',
    width: 200
  },
  {
    title: '联系人',
    key: 'contact',
    width: 120
  },
  {
    title: '联系电话',
    key: 'phone',
    width: 140
  },
  {
    title: '状态',
    key: 'status',
    width: 100,
    render(row) {
      return h(
        NTag,
        {
          type: row.status === 'active' ? 'success' : 'error',
          size: 'small'
        },
        { default: () => row.status === 'active' ? '正常' : '停用' }
      )
    }
  },
  {
    title: '创建时间',
    key: 'createTime',
    width: 120
  },
  {
    title: '操作',
    key: 'actions',
    width: 200,
    render(row) {
      return h(NSpace, { size: 'small' }, {
        default: () => [
          h(
            NButton,
            {
              size: 'small',
              type: 'primary',
              onClick: () => handleEdit(row)
            },
            { default: () => '编辑' }
          ),
          h(
            NButton,
            {
              size: 'small',
              type: 'error',
              onClick: () => handleDelete(row)
            },
            { default: () => '删除' }
          )
        ]
      })
    }
  }
]

// 操作方法
function handleAdd() {
  $message.info('新增企业功能')
}

function handleEdit(row) {
  $message.info(`编辑企业：${row.name}`)
}

function handleDelete(row) {
  $message.info(`删除企业：${row.name}`)
}
</script>

