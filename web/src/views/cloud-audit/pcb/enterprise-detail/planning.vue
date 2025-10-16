<template>
  <div class="planning-page p-4">
    <n-spin :show="loading">
      <!-- 1. 清洁生产审核领导小组 -->
      <n-card class="mb-4 leadership-team-card">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:user-multiple" class="header-icon" />
              <span class="header-title">清洁生产审核领导小组</span>
            </div>
            <div class="header-actions">
              <n-button type="primary" @click="showAddLeadershipModal = true">
                <template #icon>
                  <TheIcon icon="carbon:add" />
                </template>
                添加成员
              </n-button>
            </div>
          </div>
        </template>
        
        <n-data-table
          :columns="leadershipColumns"
          :data="leadershipTeam"
          :loading="leadershipLoading"
          :pagination="false"
          :bordered="true"
          class="leadership-table"
        />
      </n-card>
      
      <!-- 2. 清洁生产工作小组 -->
      <n-card class="mb-4 work-team-card">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:group" class="header-icon" />
              <span class="header-title">清洁生产工作小组</span>
            </div>
            <div class="header-actions">
              <n-button type="primary" @click="showAddWorkTeamModal = true">
                <template #icon>
                  <TheIcon icon="carbon:add" />
                </template>
                添加成员
              </n-button>
            </div>
          </div>
        </template>
        
        <n-data-table
          :columns="workTeamColumns"
          :data="workTeam"
          :loading="workTeamLoading"
          :pagination="false"
          :bordered="true"
          class="work-team-table"
        />
      </n-card>
      
      <!-- 3. 工作计划表 -->
      <n-card class="mb-4 work-plan-container">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:calendar" class="header-icon" />
              <span class="header-title">工作计划表</span>
            </div>
            <div class="header-actions">
              <n-button type="primary" @click="showWorkPlanModal = true">
                <template #icon>
                  <TheIcon icon="carbon:edit" />
                </template>
                编辑计划
              </n-button>
            </div>
          </div>
        </template>
        
        <!-- 工作计划表主视图（两列网格布局） -->
        <div class="work-plan-grid">
          <div 
            v-for="(plan, index) in workPlans" 
            :key="plan.id"
            class="work-plan-card"
            :class="`stage-${plan.stage_order}`"
          >
            <div class="card-header">
              <div class="stage-icon" :class="`icon-${plan.stage_order}`">
                <TheIcon :icon="getStageIcon(plan.stage_order)" />
              </div>
              <div class="stage-info">
                <div class="stage-number">第{{ plan.stage_order }}阶段</div>
                <div class="stage-title">{{ plan.stage }}</div>
              </div>
            </div>
            <div class="card-content">
              <div class="work-content">{{ plan.work_content }}</div>
              <div class="stage-details">
                <div class="detail-row">
                  <span class="detail-label">计划时间:</span>
                  <span class="detail-value">{{ formatDateRange(plan.planned_start_date, plan.planned_end_date) }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">责任部门:</span>
                  <span class="detail-value">{{ plan.responsible_department }}</span>
                </div>
                <div class="detail-row" v-if="plan.actual_start_date">
                  <span class="detail-label">完成时间:</span>
                  <span class="detail-value">{{ formatDateRange(plan.actual_start_date, plan.actual_end_date) }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </n-card>
      
      <!-- 4. 宣传与培训 -->
      <n-card class="mb-4 training-container">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:education" class="header-icon" />
              <span class="header-title">宣传与培训</span>
            </div>
            <div class="header-actions">
              <!-- 会议图片上传 -->
              <n-upload
                :file-list="meetingImages"
                @change="handleMeetingImageChange"
                @remove="handleMeetingImageRemove"
                :max="5"
                accept="image/*"
                class="meeting-image-upload"
              >
                <n-button size="small" type="info">
                  <template #icon>
                    <TheIcon icon="carbon:camera" />
                  </template>
                  上传会议图片
                </n-button>
              </n-upload>
              
              <n-button type="primary" @click="showAddTrainingModal = true">
                <template #icon>
                  <TheIcon icon="carbon:add" />
                </template>
                添加培训记录
              </n-button>
            </div>
          </div>
        </template>
        
        <div class="training-records">
          <div 
            v-for="record in trainingRecords" 
            :key="record.id"
            class="training-card"
          >
            <div class="training-header">
              <h3 class="training-title">{{ record.title }}</h3>
              <div class="training-meta">
                <span class="training-date">{{ formatDate(record.date) }}</span>
                <span class="training-duration">{{ record.duration }}分钟</span>
                <span class="training-participants">{{ record.participants }}人参与</span>
              </div>
            </div>
            
            <div class="training-content">
              <p class="training-description">{{ record.content }}</p>
              <div class="training-details">
                <div class="detail-item">
                  <span class="detail-label">培训讲师:</span>
                  <span class="detail-value">{{ record.instructor }}</span>
                </div>
                <div class="detail-item">
                  <span class="detail-label">培训地点:</span>
                  <span class="detail-value">{{ record.location }}</span>
                </div>
              </div>
            </div>
            
            <div class="training-actions">
              <n-space>
                <n-button size="small" @click="editTraining(record)">编辑</n-button>
                <n-button size="small" type="error" @click="deleteTraining(record.id)">删除</n-button>
              </n-space>
            </div>
          </div>
        </div>
      </n-card>
    </n-spin>

    <!-- 添加领导小组成员模态框 -->
    <n-modal
      v-model:show="showAddLeadershipModal"
      preset="card"
      title="添加领导小组成员"
      size="medium"
      :bordered="false"
    >
      <n-form
        ref="leadershipFormRef"
        :model="leadershipForm"
        :rules="leadershipRules"
        label-placement="left"
        label-width="100px"
      >
        <n-form-item label="姓名" path="name">
          <n-input v-model:value="leadershipForm.name" placeholder="请输入姓名" />
        </n-form-item>
        <n-form-item label="职位" path="position">
          <n-input v-model:value="leadershipForm.position" placeholder="请输入职位" />
        </n-form-item>
        <n-form-item label="部门" path="department">
          <n-input v-model:value="leadershipForm.department" placeholder="请输入部门" />
        </n-form-item>
        <n-form-item label="角色" path="role">
          <n-select
            v-model:value="leadershipForm.role"
            :options="leadershipRoleOptions"
            placeholder="请选择角色"
          />
        </n-form-item>
        <n-form-item label="职责" path="responsibilities">
          <n-input
            v-model:value="leadershipForm.responsibilities"
            type="textarea"
            placeholder="请输入职责描述"
          />
        </n-form-item>
        <n-form-item label="联系电话" path="phone">
          <n-input v-model:value="leadershipForm.phone" placeholder="请输入联系电话" />
        </n-form-item>
      </n-form>
      
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddLeadershipModal = false">取消</n-button>
          <n-button type="primary" @click="saveLeadershipMember">保存</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 添加工作小组成员模态框 -->
    <n-modal
      v-model:show="showAddWorkTeamModal"
      preset="card"
      title="添加工作小组成员"
      size="medium"
      :bordered="false"
    >
      <n-form
        ref="workTeamFormRef"
        :model="workTeamForm"
        :rules="workTeamRules"
        label-placement="left"
        label-width="100px"
      >
        <n-form-item label="姓名" path="name">
          <n-input v-model:value="workTeamForm.name" placeholder="请输入姓名" />
        </n-form-item>
        <n-form-item label="职位" path="position">
          <n-input v-model:value="workTeamForm.position" placeholder="请输入职位" />
        </n-form-item>
        <n-form-item label="部门" path="department">
          <n-input v-model:value="workTeamForm.department" placeholder="请输入部门" />
        </n-form-item>
        <n-form-item label="角色" path="role">
          <n-select
            v-model:value="workTeamForm.role"
            :options="workTeamRoleOptions"
            placeholder="请选择角色"
          />
        </n-form-item>
        <n-form-item label="职责" path="responsibilities">
          <n-input
            v-model:value="workTeamForm.responsibilities"
            type="textarea"
            placeholder="请输入职责描述"
          />
        </n-form-item>
        <n-form-item label="联系电话" path="phone">
          <n-input v-model:value="workTeamForm.phone" placeholder="请输入联系电话" />
        </n-form-item>
      </n-form>
      
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddWorkTeamModal = false">取消</n-button>
          <n-button type="primary" @click="saveWorkTeamMember">保存</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 编辑工作计划表模态框 -->
    <n-modal
      v-model:show="showWorkPlanModal"
      preset="card"
      title="编辑工作计划表"
      size="huge"
      :bordered="false"
      style="width: 90%"
    >
      <div class="work-plan-edit-container">
        <div class="edit-actions mb-4">
          <n-button type="primary" @click="addWorkPlanStage">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加阶段
          </n-button>
        </div>
        
        <n-data-table
          :columns="workPlanEditColumns"
          :data="workPlanStages"
          :pagination="false"
          :bordered="true"
          class="work-plan-edit-table"
        />
        
        <div class="modal-actions mt-4">
          <n-space justify="end">
            <n-button @click="showWorkPlanModal = false">取消</n-button>
            <n-button type="primary" @click="saveWorkPlans">保存</n-button>
          </n-space>
        </div>
      </div>
    </n-modal>

    <!-- 添加培训记录模态框 -->
    <n-modal
      v-model:show="showAddTrainingModal"
      preset="card"
      title="添加培训记录"
      size="large"
      :bordered="false"
    >
      <n-form
        ref="trainingFormRef"
        :model="trainingForm"
        :rules="trainingRules"
        label-placement="left"
        label-width="100px"
      >
        <n-form-item label="培训标题" path="title">
          <n-input v-model:value="trainingForm.title" placeholder="请输入培训标题" />
        </n-form-item>
        <n-form-item label="培训日期" path="date">
          <n-date-picker
            v-model:value="trainingForm.date"
            type="date"
            placeholder="请选择培训日期"
          />
        </n-form-item>
        <n-form-item label="培训时长" path="duration">
          <n-input-number
            v-model:value="trainingForm.duration"
            placeholder="请输入培训时长（分钟）"
            :min="1"
          />
        </n-form-item>
        <n-form-item label="参与人数" path="participants">
          <n-input-number
            v-model:value="trainingForm.participants"
            placeholder="请输入参与人数"
            :min="1"
          />
        </n-form-item>
        <n-form-item label="培训内容" path="content">
          <n-input
            v-model:value="trainingForm.content"
            type="textarea"
            placeholder="请输入培训内容"
          />
        </n-form-item>
        <n-form-item label="培训讲师" path="instructor">
          <n-input v-model:value="trainingForm.instructor" placeholder="请输入培训讲师" />
        </n-form-item>
        <n-form-item label="培训地点" path="location">
          <n-input v-model:value="trainingForm.location" placeholder="请输入培训地点" />
        </n-form-item>
      </n-form>
      
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddTrainingModal = false">取消</n-button>
          <n-button type="primary" @click="saveTraining">保存</n-button>
        </n-space>
      </template>
    </n-modal>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, h } from 'vue'
import { NInput, NDatePicker, NInputNumber, NButton, NTag, NSpace, NSelect } from 'naive-ui'
import { useMessage, useDialog } from 'naive-ui'
import api from '@/api'

// Props
const props = defineProps({
  enterpriseId: {
    type: [String, Number],
    required: true
  }
})

// 消息提示
const message = useMessage()
const dialog = useDialog()

// 基础数据
const loading = ref(false)
const enterpriseId = computed(() => props.enterpriseId)

// 领导小组数据
const leadershipTeam = ref([])
const leadershipLoading = ref(false)
const showAddLeadershipModal = ref(false)
const leadershipForm = ref({
  name: '',
  position: '',
  department: '',
  role: '',
  responsibilities: '',
  phone: ''
})

// 工作小组数据
const workTeam = ref([])
const workTeamLoading = ref(false)
const showAddWorkTeamModal = ref(false)
const workTeamForm = ref({
  name: '',
  position: '',
  department: '',
  role: '',
  responsibilities: '',
  phone: ''
})

// 工作计划数据
const workPlans = ref([])
const workPlanStages = ref([])
const workPlanLoading = ref(false)
const showWorkPlanModal = ref(false)

// 培训记录数据
const trainingRecords = ref([])
const trainingLoading = ref(false)
const showAddTrainingModal = ref(false)
const trainingForm = ref({
  title: '',
  date: null,
  duration: null,
  participants: null,
  content: '',
  instructor: '',
  location: ''
})
const meetingImages = ref([])

// 渲染函数定义
const renderRoleTag = (row) => {
  const roleConfig = {
    '组长': { type: 'success', text: '组长' },
    '副组长': { type: 'info', text: '副组长' },
    '成员': { type: 'default', text: '成员' }
  }
  const config = roleConfig[row.role] || { type: 'default', text: row.role }
  return h(NTag, { type: config.type }, { default: () => config.text })
}

const renderLeadershipActions = (row) => {
  return h(NSpace, [
    h(NButton, {
      size: 'small',
      type: 'error',
      onClick: () => deleteLeadershipMember(row.id)
    }, { default: () => '删除' })
  ])
}

const renderWorkTeamActions = (row) => {
  return h(NSpace, [
    h(NButton, {
      size: 'small',
      type: 'error',
      onClick: () => deleteWorkTeamMember(row.id)
    }, { default: () => '删除' })
  ])
}

const renderStageOrder = (row, index) => {
  return h('div', { class: 'stage-order-display' }, [
    h('span', { class: 'stage-order-text' }, `第${row.stage_order}阶段`)
  ])
}

const renderStageName = (row, index) => {
  return h(NInput, {
    value: row.stage,
    'onUpdate:value': (value) => {
      workPlanStages.value[index].stage = value
    },
    placeholder: '请输入阶段名称'
  })
}

const renderWorkContent = (row, index) => {
  return h(NInput, {
    value: row.work_content,
    'onUpdate:value': (value) => {
      workPlanStages.value[index].work_content = value
    },
    type: 'textarea',
    placeholder: '请输入工作内容'
  })
}

const renderPlannedStartDate = (row, index) => {
  return h(NDatePicker, {
    value: row.planned_start_date,
    'onUpdate:value': (value) => {
      workPlanStages.value[index].planned_start_date = value
    },
    type: 'date',
    placeholder: '选择开始时间'
  })
}

const renderPlannedEndDate = (row, index) => {
  return h(NDatePicker, {
    value: row.planned_end_date,
    'onUpdate:value': (value) => {
      workPlanStages.value[index].planned_end_date = value
    },
    type: 'date',
    placeholder: '选择结束时间'
  })
}

const renderResponsibleDepartment = (row, index) => {
  return h(NInput, {
    value: row.responsible_department,
    'onUpdate:value': (value) => {
      workPlanStages.value[index].responsible_department = value
    },
    placeholder: '请输入责任部门'
  })
}

const renderActualStartDate = (row, index) => {
  return h(NDatePicker, {
    value: row.actual_start_date,
    'onUpdate:value': (value) => {
      workPlanStages.value[index].actual_start_date = value
    },
    type: 'date',
    placeholder: '选择开始时间'
  })
}

const renderActualEndDate = (row, index) => {
  return h(NDatePicker, {
    value: row.actual_end_date,
    'onUpdate:value': (value) => {
      workPlanStages.value[index].actual_end_date = value
    },
    type: 'date',
    placeholder: '选择结束时间'
  })
}

const renderWorkPlanActions = (row, index) => {
  return h(NSpace, [
    h(NButton, {
      size: 'small',
      type: 'error',
      onClick: () => deleteWorkPlanStage(index)
    }, { default: () => '删除' })
  ])
}

// 表格列定义
const leadershipColumns = [
  { title: '姓名', key: 'name', width: 120 },
  { title: '职位', key: 'position', width: 150 },
  { title: '部门', key: 'department', width: 150 },
  { title: '角色', key: 'role', width: 100, render: renderRoleTag },
  { title: '职责', key: 'responsibilities', ellipsis: { tooltip: true } },
  { title: '联系电话', key: 'phone', width: 150 },
  { title: '操作', key: 'actions', width: 150, render: renderLeadershipActions }
]

const workTeamColumns = [
  { title: '姓名', key: 'name', width: 120 },
  { title: '职位', key: 'position', width: 150 },
  { title: '部门', key: 'department', width: 150 },
  { title: '角色', key: 'role', width: 100, render: renderRoleTag },
  { title: '职责', key: 'responsibilities', ellipsis: { tooltip: true } },
  { title: '联系电话', key: 'phone', width: 150 },
  { title: '操作', key: 'actions', width: 150, render: renderWorkTeamActions }
]

const workPlanEditColumns = [
  { title: '阶段', key: 'stage_order', width: 80, render: renderStageOrder },
  { title: '阶段名称', key: 'stage', width: 200, render: renderStageName },
  { title: '工作内容', key: 'work_content', render: renderWorkContent },
  { title: '计划开始时间', key: 'planned_start_date', width: 150, render: renderPlannedStartDate },
  { title: '计划结束时间', key: 'planned_end_date', width: 150, render: renderPlannedEndDate },
  { title: '责任部门', key: 'responsible_department', width: 150, render: renderResponsibleDepartment },
  { title: '实际开始时间', key: 'actual_start_date', width: 150, render: renderActualStartDate },
  { title: '实际结束时间', key: 'actual_end_date', width: 150, render: renderActualEndDate },
  { title: '操作', key: 'actions', width: 100, render: renderWorkPlanActions }
]

// 表单验证规则
const leadershipRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  position: [
    { required: true, message: '请输入职位', trigger: 'blur' }
  ],
  department: [
    { required: true, message: '请输入部门', trigger: 'blur' }
  ]
}

const workTeamRules = {
  name: [
    { required: true, message: '请输入姓名', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  position: [
    { required: true, message: '请输入职位', trigger: 'blur' }
  ],
  department: [
    { required: true, message: '请输入部门', trigger: 'blur' }
  ]
}

const trainingRules = {
  title: [
    { required: true, message: '请输入培训标题', trigger: 'blur' }
  ],
  date: [
    { required: true, message: '请选择培训日期', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入培训内容', trigger: 'blur' }
  ],
  instructor: [
    { required: true, message: '请输入培训讲师', trigger: 'blur' }
  ],
  location: [
    { required: true, message: '请输入培训地点', trigger: 'blur' }
  ]
}

// 选项数据
const leadershipRoleOptions = [
  { label: '组长', value: '组长' },
  { label: '副组长', value: '副组长' },
  { label: '成员', value: '成员' }
]

const workTeamRoleOptions = [
  { label: '组长', value: '组长' },
  { label: '副组长', value: '副组长' },
  { label: '成员', value: '成员' }
]

// 数据获取方法
const fetchLeadershipTeam = async () => {
  try {
    leadershipLoading.value = true
    const response = await api.pcb.planning.getLeadershipTeam(enterpriseId.value)
    leadershipTeam.value = response.data.items || []
  } catch (error) {
    console.error('获取领导小组失败:', error)
    message.error('获取领导小组失败')
  } finally {
    leadershipLoading.value = false
  }
}

const fetchWorkTeam = async () => {
  try {
    workTeamLoading.value = true
    const response = await api.pcb.planning.getWorkTeam(enterpriseId.value)
    workTeam.value = response.data.items || []
  } catch (error) {
    console.error('获取工作小组失败:', error)
    message.error('获取工作小组失败')
  } finally {
    workTeamLoading.value = false
  }
}

const fetchWorkPlans = async () => {
  try {
    workPlanLoading.value = true
    const response = await api.pcb.planning.getWorkPlans(enterpriseId.value)
    workPlans.value = response.data.items || []
    workPlanStages.value = [...workPlans.value] // 创建可编辑副本
  } catch (error) {
    console.error('获取工作计划失败:', error)
    message.error('获取工作计划失败')
  } finally {
    workPlanLoading.value = false
  }
}

const fetchTrainingRecords = async () => {
  try {
    trainingLoading.value = true
    const response = await api.pcb.planning.getTrainingRecords(enterpriseId.value)
    trainingRecords.value = response.data.items || []
  } catch (error) {
    console.error('获取培训记录失败:', error)
    message.error('获取培训记录失败')
  } finally {
    trainingLoading.value = false
  }
}

// 数据保存方法
const saveLeadershipMember = async () => {
  try {
    await api.pcb.planning.addLeadershipMember(enterpriseId.value, leadershipForm.value)
    message.success('添加成功')
    showAddLeadershipModal.value = false
    resetLeadershipForm()
    await fetchLeadershipTeam()
  } catch (error) {
    console.error('添加领导小组成员失败:', error)
    message.error('添加失败')
  }
}

const saveWorkTeamMember = async () => {
  try {
    await api.pcb.planning.addWorkTeamMember(enterpriseId.value, workTeamForm.value)
    message.success('添加成功')
    showAddWorkTeamModal.value = false
    resetWorkTeamForm()
    await fetchWorkTeam()
  } catch (error) {
    console.error('添加工作小组成员失败:', error)
    message.error('添加失败')
  }
}

const saveWorkPlans = async () => {
  try {
    await api.pcb.planning.updateWorkPlans(enterpriseId.value, workPlanStages.value)
    message.success('保存成功')
    showWorkPlanModal.value = false
    await fetchWorkPlans()
  } catch (error) {
    console.error('保存工作计划失败:', error)
    message.error('保存失败')
  }
}

const saveTraining = async () => {
  try {
    const formData = new FormData()
    Object.keys(trainingForm.value).forEach(key => {
      if (trainingForm.value[key] !== null && trainingForm.value[key] !== '') {
        formData.append(key, trainingForm.value[key])
      }
    })
    
    // 添加图片文件
    meetingImages.value.forEach((file, index) => {
      formData.append(`images[${index}]`, file)
    })
    
    await api.pcb.planning.addTrainingRecord(enterpriseId.value, formData)
    message.success('添加成功')
    showAddTrainingModal.value = false
    resetTrainingForm()
    await fetchTrainingRecords()
  } catch (error) {
    console.error('添加培训记录失败:', error)
    message.error('添加失败')
  }
}

// 工作计划表编辑功能
const addWorkPlanStage = () => {
  const newStage = {
    id: null,
    stage_order: workPlanStages.value.length + 1,
    stage: '',
    work_content: '',
    planned_start_date: null,
    planned_end_date: null,
    responsible_department: '',
    actual_start_date: null,
    actual_end_date: null
  }
  workPlanStages.value.push(newStage)
}

const deleteWorkPlanStage = (index) => {
  workPlanStages.value.splice(index, 1)
  reorderStages()
}

const reorderStages = () => {
  workPlanStages.value.forEach((stage, index) => {
    stage.stage_order = index + 1
  })
}

const getStageIcon = (stageOrder) => {
  const icons = [
    'carbon:settings', 'carbon:search', 'carbon:document', 'carbon:idea',
    'carbon:checkmark', 'carbon:play', 'carbon:renew', 'carbon:document-attachment',
    'carbon:send', 'carbon:location'
  ]
  return icons[stageOrder - 1] || 'carbon:circle'
}

const formatDateRange = (startDate, endDate) => {
  if (!startDate || !endDate) return '-'
  const start = new Date(startDate).toLocaleDateString()
  const end = new Date(endDate).toLocaleDateString()
  return `${start} - ${end}`
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleDateString('zh-CN')
}

// 图片上传处理
const handleMeetingImageChange = (options) => {
  const { fileList } = options
  meetingImages.value = fileList.map(file => file.file)
}

const handleMeetingImageRemove = (options) => {
  const { fileList } = options
  meetingImages.value = fileList.map(file => file.file)
}

// 表单重置
const resetLeadershipForm = () => {
  leadershipForm.value = {
    name: '',
    position: '',
    department: '',
    role: '',
    responsibilities: '',
    phone: ''
  }
}

const resetWorkTeamForm = () => {
  workTeamForm.value = {
    name: '',
    position: '',
    department: '',
    role: '',
    responsibilities: '',
    phone: ''
  }
}

const resetTrainingForm = () => {
  trainingForm.value = {
    title: '',
    date: null,
    duration: null,
    participants: null,
    content: '',
    instructor: '',
    location: ''
  }
}

// 培训记录操作
const editTraining = (record) => {
  trainingForm.value = { ...record }
  showAddTrainingModal.value = true
}

const deleteTraining = async (id) => {
  try {
    await dialog.warning({
      title: '确认删除',
      content: '确定要删除该培训记录吗？',
      positiveText: '确定',
      negativeText: '取消'
    })
    await api.pcb.planning.deleteTrainingRecord(enterpriseId.value, id)
    message.success('删除成功')
    await fetchTrainingRecords()
  } catch (error) {
    if (error) {
      console.error('删除培训记录失败:', error)
      message.error('删除失败')
    }
  }
}

// 删除成员方法
const deleteLeadershipMember = async (id) => {
  try {
    await dialog.warning({
      title: '确认删除',
      content: '确定要删除该成员吗？',
      positiveText: '确定',
      negativeText: '取消'
    })
    await api.pcb.planning.deleteLeadershipMember(enterpriseId.value, id)
    message.success('删除成功')
    await fetchLeadershipTeam()
  } catch (error) {
    if (error) {
      console.error('删除领导小组成员失败:', error)
      message.error('删除失败')
    }
  }
}

const deleteWorkTeamMember = async (id) => {
  try {
    await dialog.warning({
      title: '确认删除',
      content: '确定要删除该成员吗？',
      positiveText: '确定',
      negativeText: '取消'
    })
    await api.pcb.planning.deleteWorkTeamMember(enterpriseId.value, id)
    message.success('删除成功')
    await fetchWorkTeam()
  } catch (error) {
    if (error) {
      console.error('删除工作小组成员失败:', error)
      message.error('删除失败')
    }
  }
}

// 生命周期
onMounted(async () => {
  await Promise.all([
    fetchLeadershipTeam(),
    fetchWorkTeam(),
    fetchWorkPlans(),
    fetchTrainingRecords()
  ])
})
</script>

<style scoped>
.planning-page {
  max-width: 1200px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  font-size: 18px;
  color: #1890ff;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.header-actions {
  display: flex;
  gap: 8px;
}

.meeting-image-upload {
  margin-right: 8px;
}

/* 工作计划表网格样式 */
.work-plan-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.work-plan-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border-left: 4px solid var(--stage-color);
}

.work-plan-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.stage-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 18px;
  margin-right: 12px;
}

.stage-number {
  font-size: 14px;
  color: #666;
  margin-bottom: 4px;
}

.stage-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin-bottom: 12px;
}

.work-content {
  font-size: 16px;
  color: #555;
  line-height: 1.6;
  margin-bottom: 16px;
}

.detail-row {
  display: flex;
  margin-bottom: 8px;
}

.detail-label {
  font-weight: 500;
  color: #666;
  min-width: 80px;
  margin-right: 8px;
}

.detail-value {
  color: #333;
  flex: 1;
}

/* 阶段颜色主题 */
.stage-1 { --stage-color: #ff6b6b; }
.stage-2 { --stage-color: #4ecdc4; }
.stage-3 { --stage-color: #45b7d1; }
.stage-4 { --stage-color: #96ceb4; }
.stage-5 { --stage-color: #feca57; }
.stage-6 { --stage-color: #ff9ff3; }
.stage-7 { --stage-color: #54a0ff; }
.stage-8 { --stage-color: #5f27cd; }
.stage-9 { --stage-color: #00d2d3; }
.stage-10 { --stage-color: #ff9f43; }

.icon-1 { background: #ff6b6b; }
.icon-2 { background: #4ecdc4; }
.icon-3 { background: #45b7d1; }
.icon-4 { background: #96ceb4; }
.icon-5 { background: #feca57; }
.icon-6 { background: #ff9ff3; }
.icon-7 { background: #54a0ff; }
.icon-8 { background: #5f27cd; }
.icon-9 { background: #00d2d3; }
.icon-10 { background: #ff9f43; }

/* 培训记录样式 */
.training-records {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-top: 16px;
}

.training-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border-left: 4px solid #4ecdc4;
}

.training-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.training-header {
  margin-bottom: 16px;
}

.training-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  margin: 0 0 8px 0;
}

.training-meta {
  display: flex;
  gap: 16px;
  font-size: 14px;
  color: #666;
}

.training-content {
  margin-bottom: 16px;
}

.training-description {
  color: #555;
  line-height: 1.6;
  margin-bottom: 12px;
}

.training-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
}

.training-actions {
  border-top: 1px solid #f0f0f0;
  padding-top: 12px;
}

/* 编辑表格样式 */
.work-plan-edit-container {
  max-height: 70vh;
  overflow-y: auto;
}

.work-plan-edit-table {
  margin-bottom: 16px;
}

.stage-order-display {
  text-align: center;
}

.stage-order-text {
  font-weight: 600;
  color: #1890ff;
}
</style>
