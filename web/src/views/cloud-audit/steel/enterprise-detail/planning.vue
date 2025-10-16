<template>
  <div class="planning-page p-4">
    <n-spin :show="loading">
      <!-- 审核工作组 -->
      <n-card class="mb-4 audit-team-card">
        <template #header>
          <div class="card-header">
            <div class="header-left">
              <TheIcon icon="carbon:user-multiple" class="header-icon" />
              <span class="header-title">审核工作组</span>
            </div>
            <n-button type="primary" @click="showAddMemberModal = true" class="add-button">
              <template #icon>
                <TheIcon icon="carbon:add" />
              </template>
              添加成员
            </n-button>
          </div>
        </template>
        
        <div class="table-container">
          <n-data-table
            :columns="memberColumns"
            :data="auditTeam"
            :pagination="false"
            :loading="teamLoading"
            :bordered="false"
            :single-line="false"
            class="member-table"
          >
            <template #role="{ row }">
              <n-tag 
                :type="getRoleTagType(row.role)"
                :bordered="false"
                size="small"
                class="role-tag"
              >
                <template #icon>
                  <TheIcon :icon="getRoleIcon(row.role)" />
                </template>
                {{ getRoleText(row.role) }}
              </n-tag>
            </template>
            <template #action="{ row }">
              <n-space size="small">
                <n-button 
                  size="small" 
                  type="info" 
                  @click="editMember(row)"
                  class="action-button"
                >
                  <template #icon>
                    <TheIcon icon="carbon:edit" />
                  </template>
                  编辑
                </n-button>
                <n-button 
                  size="small" 
                  type="error" 
                  @click="deleteMember(row.id)"
                  class="action-button"
                >
                  <template #icon>
                    <TheIcon icon="carbon:trash-can" />
                  </template>
                  删除
                </n-button>
              </n-space>
            </template>
          </n-data-table>
        </div>
      </n-card>

      <!-- 工作计划 -->
      <n-card title="工作计划" class="mb-4">
        <template #header-extra>
          <n-button type="primary" @click="showAddPlanModal = true">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            制定计划
          </n-button>
        </template>
        
        <n-timeline>
          <n-timeline-item 
            v-for="plan in workPlans"
            :key="plan.id"
            :title="plan.title"
            :content="plan.description"
            :time="`${plan.startDate} - ${plan.endDate}`"
            :type="getPlanTimelineType(plan.status)"
          >
            <template #header>
              <n-space align="center">
                <span>{{ plan.title }}</span>
                <n-tag :type="getStatusTagType(plan.status)">
                  {{ getStatusText(plan.status) }}
                </n-tag>
                <n-progress 
                  :percentage="plan.progress" 
                  :type="getProgressType(plan.progress)"
                  style="width: 100px"
                />
              </n-space>
            </template>
          </n-timeline-item>
        </n-timeline>
      </n-card>

      <!-- 宣传与培训 -->
      <n-card title="宣传与培训">
        <template #header-extra>
          <n-button type="primary" @click="showAddTrainingModal = true">
            <template #icon>
              <TheIcon icon="carbon:add" />
            </template>
            添加培训记录
          </n-button>
        </template>
        
        <n-data-table
          :columns="trainingColumns"
          :data="trainingRecords"
          :pagination="false"
          :loading="trainingLoading"
        >
          <template #action="{ row }">
            <n-space>
              <n-button size="small" @click="editTraining(row)">编辑</n-button>
              <n-button size="small" type="error" @click="deleteTraining(row.id)">删除</n-button>
            </n-space>
          </template>
        </n-data-table>
      </n-card>
    </n-spin>

    <!-- 添加/编辑成员弹窗 -->
    <n-modal v-model:show="showAddMemberModal" preset="card" title="添加审核成员" style="width: 600px">
      <n-form ref="memberFormRef" :model="memberForm" :rules="memberRules">
        <n-form-item label="姓名" path="name">
          <n-input v-model:value="memberForm.name" placeholder="请输入姓名" />
        </n-form-item>
        <n-form-item label="职位" path="position">
          <n-input v-model:value="memberForm.position" placeholder="请输入职位" />
        </n-form-item>
        <n-form-item label="部门" path="department">
          <n-input v-model:value="memberForm.department" placeholder="请输入部门" />
        </n-form-item>
        <n-form-item label="联系电话" path="phone">
          <n-input v-model:value="memberForm.phone" placeholder="请输入联系电话" />
        </n-form-item>
        <n-form-item label="邮箱" path="email">
          <n-input v-model:value="memberForm.email" placeholder="请输入邮箱" />
        </n-form-item>
        <n-form-item label="角色" path="role">
          <n-select
            v-model:value="memberForm.role"
            :options="roleOptions"
            placeholder="请选择角色"
          />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddMemberModal = false">取消</n-button>
          <n-button type="primary" @click="saveMember">保存</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 添加/编辑计划弹窗 -->
    <n-modal v-model:show="showAddPlanModal" preset="card" title="制定工作计划" style="width: 600px">
      <n-form ref="planFormRef" :model="planForm" :rules="planRules">
        <n-form-item label="计划标题" path="title">
          <n-input v-model:value="planForm.title" placeholder="请输入计划标题" />
        </n-form-item>
        <n-form-item label="计划描述" path="description">
          <n-input
            v-model:value="planForm.description"
            type="textarea"
            placeholder="请输入计划描述"
            :rows="3"
          />
        </n-form-item>
        <n-form-item label="开始日期" path="startDate">
          <n-date-picker
            v-model:value="planForm.startDate"
            type="date"
            placeholder="请选择开始日期"
          />
        </n-form-item>
        <n-form-item label="结束日期" path="endDate">
          <n-date-picker
            v-model:value="planForm.endDate"
            type="date"
            placeholder="请选择结束日期"
          />
        </n-form-item>
        <n-form-item label="进度" path="progress">
          <n-slider v-model:value="planForm.progress" :min="0" :max="100" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddPlanModal = false">取消</n-button>
          <n-button type="primary" @click="savePlan">保存</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 添加/编辑培训记录弹窗 -->
    <n-modal v-model:show="showAddTrainingModal" preset="card" title="添加培训记录" style="width: 600px">
      <n-form ref="trainingFormRef" :model="trainingForm" :rules="trainingRules">
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
        <n-form-item label="参与人数" path="participants">
          <n-input-number
            v-model:value="trainingForm.participants"
            :min="1"
            placeholder="请输入参与人数"
          />
        </n-form-item>
        <n-form-item label="培训时长(小时)" path="duration">
          <n-input-number
            v-model:value="trainingForm.duration"
            :min="0.5"
            :step="0.5"
            placeholder="请输入培训时长"
          />
        </n-form-item>
        <n-form-item label="培训内容" path="content">
          <n-input
            v-model:value="trainingForm.content"
            type="textarea"
            placeholder="请输入培训内容"
            :rows="3"
          />
        </n-form-item>
        <n-form-item label="培训讲师" path="instructor">
          <n-input v-model:value="trainingForm.instructor" placeholder="请输入培训讲师" />
        </n-form-item>
      </n-form>
      <template #footer>
        <n-space justify="end">
          <n-button @click="showAddTrainingModal = false">取消</n-button>
          <n-button type="primary" @click="saveTraining">保存</n-button>
        </n-space>
      </template>
    </n-modal>

    <!-- 模块导航按钮 -->
    <div class="module-navigation mt-4">
      <n-space justify="space-between">
        <n-button @click="goToPrevious">
          <template #icon>
            <TheIcon icon="carbon:arrow-left" />
          </template>
          企业信息
        </n-button>
        <n-button type="primary" @click="goToNext">
          预审核
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
  NCard, NButton, NDataTable, NTimeline, NTimelineItem, NModal, NForm, NFormItem, 
  NInput, NSelect, NDatePicker, NSlider, NInputNumber, NSpace, NTag, NProgress,
  NSpin, useMessage, useDialog
} from 'naive-ui'
import TheIcon from '@/components/icon/TheIcon.vue'
import { mockDetailApi } from '@/mock/steel-detail'

defineOptions({ name: '钢铁筹划与组织' })

const props = defineProps({
  enterpriseId: {
    type: String,
    required: true
  }
})

const emit = defineEmits(['navigate'])

const message = useMessage()
const dialog = useDialog()

// 导航函数
const goToPrevious = () => {
  emit('navigate', 'basic-info')
}

const goToNext = () => {
  emit('navigate', 'pre-audit')
}

// 响应式数据
const loading = ref(false)
const teamLoading = ref(false)
const trainingLoading = ref(false)

const auditTeam = ref([])
const workPlans = ref([])
const trainingRecords = ref([])

// 弹窗状态
const showAddMemberModal = ref(false)
const showAddPlanModal = ref(false)
const showAddTrainingModal = ref(false)

// 表单数据
const memberForm = ref({
  name: '',
  position: '',
  department: '',
  phone: '',
  email: '',
  role: ''
})

const planForm = ref({
  title: '',
  description: '',
  startDate: null,
  endDate: null,
  progress: 0
})

const trainingForm = ref({
  title: '',
  date: null,
  participants: null,
  duration: null,
  content: '',
  instructor: ''
})

// 表格列定义
const memberColumns = [
  { title: '姓名', key: 'name', width: 100 },
  { title: '职位', key: 'position', width: 120 },
  { title: '部门', key: 'department', width: 120 },
  { title: '联系电话', key: 'phone', width: 130 },
  { title: '邮箱', key: 'email', width: 180 },
  { title: '角色', key: 'role', width: 100 },
  { title: '操作', key: 'action', width: 120 }
]

const trainingColumns = [
  { title: '培训标题', key: 'title', width: 200 },
  { title: '培训日期', key: 'date', width: 120 },
  { title: '参与人数', key: 'participants', width: 100 },
  { title: '培训时长', key: 'duration', width: 100 },
  { title: '培训内容', key: 'content', width: 200 },
  { title: '培训讲师', key: 'instructor', width: 120 },
  { title: '操作', key: 'action', width: 120 }
]

// 选项数据
const roleOptions = [
  { label: '组长', value: '组长' },
  { label: '专家', value: '专家' },
  { label: '审核员', value: '审核员' }
]

// 表单验证规则
const memberRules = {
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  position: [{ required: true, message: '请输入职位', trigger: 'blur' }],
  department: [{ required: true, message: '请输入部门', trigger: 'blur' }],
  phone: [{ required: true, message: '请输入联系电话', trigger: 'blur' }],
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
}

const planRules = {
  title: [{ required: true, message: '请输入计划标题', trigger: 'blur' }],
  description: [{ required: true, message: '请输入计划描述', trigger: 'blur' }],
  startDate: [{ required: true, message: '请选择开始日期', trigger: 'change' }],
  endDate: [{ required: true, message: '请选择结束日期', trigger: 'change' }]
}

const trainingRules = {
  title: [{ required: true, message: '请输入培训标题', trigger: 'blur' }],
  date: [{ required: true, message: '请选择培训日期', trigger: 'change' }],
  participants: [{ required: true, message: '请输入参与人数', trigger: 'blur' }],
  duration: [{ required: true, message: '请输入培训时长', trigger: 'blur' }],
  content: [{ required: true, message: '请输入培训内容', trigger: 'blur' }],
  instructor: [{ required: true, message: '请输入培训讲师', trigger: 'blur' }]
}

// 方法定义
const fetchAuditTeam = async () => {
  try {
    teamLoading.value = true
    const response = await mockDetailApi.getAuditTeam(props.enterpriseId)
    auditTeam.value = response.data || []
  } catch (error) {
    console.error('获取审核团队失败:', error)
    message.error('获取审核团队失败')
  } finally {
    teamLoading.value = false
  }
}

const fetchWorkPlans = async () => {
  try {
    const response = await mockDetailApi.getWorkPlans(props.enterpriseId)
    workPlans.value = response.data || []
  } catch (error) {
    console.error('获取工作计划失败:', error)
    message.error('获取工作计划失败')
  }
}

const fetchTrainingRecords = async () => {
  try {
    trainingLoading.value = true
    const response = await mockDetailApi.getTrainingRecords(props.enterpriseId)
    trainingRecords.value = response.data || []
  } catch (error) {
    console.error('获取培训记录失败:', error)
    message.error('获取培训记录失败')
  } finally {
    trainingLoading.value = false
  }
}

const saveMember = async () => {
  try {
    // 模拟保存
    const newMember = {
      id: Date.now(),
      ...memberForm.value
    }
    auditTeam.value.push(newMember)
    showAddMemberModal.value = false
    resetMemberForm()
    message.success('成员添加成功')
  } catch (error) {
    console.error('保存成员失败:', error)
    message.error('保存成员失败')
  }
}

const savePlan = async () => {
  try {
    // 模拟保存
    const newPlan = {
      id: Date.now(),
      ...planForm.value,
      status: planForm.value.progress === 100 ? 'completed' : 
              planForm.value.progress > 0 ? 'in-progress' : 'pending'
    }
    workPlans.value.push(newPlan)
    showAddPlanModal.value = false
    resetPlanForm()
    message.success('计划添加成功')
  } catch (error) {
    console.error('保存计划失败:', error)
    message.error('保存计划失败')
  }
}

const saveTraining = async () => {
  try {
    // 模拟保存
    const newTraining = {
      id: Date.now(),
      ...trainingForm.value
    }
    trainingRecords.value.push(newTraining)
    showAddTrainingModal.value = false
    resetTrainingForm()
    message.success('培训记录添加成功')
  } catch (error) {
    console.error('保存培训记录失败:', error)
    message.error('保存培训记录失败')
  }
}

const editMember = (member) => {
  memberForm.value = { ...member }
  showAddMemberModal.value = true
}

const editTraining = (training) => {
  trainingForm.value = { ...training }
  showAddTrainingModal.value = true
}

const deleteMember = (id) => {
  dialog.warning({
    title: '确认删除',
    content: '确定要删除该成员吗？',
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      auditTeam.value = auditTeam.value.filter(member => member.id !== id)
      message.success('删除成功')
    }
  })
}

const deleteTraining = (id) => {
  dialog.warning({
    title: '确认删除',
    content: '确定要删除该培训记录吗？',
    positiveText: '确认',
    negativeText: '取消',
    onPositiveClick: () => {
      trainingRecords.value = trainingRecords.value.filter(training => training.id !== id)
      message.success('删除成功')
    }
  })
}

const resetMemberForm = () => {
  memberForm.value = {
    name: '',
    position: '',
    department: '',
    phone: '',
    email: '',
    role: ''
  }
}

const resetPlanForm = () => {
  planForm.value = {
    title: '',
    description: '',
    startDate: null,
    endDate: null,
    progress: 0
  }
}

const resetTrainingForm = () => {
  trainingForm.value = {
    title: '',
    date: null,
    participants: null,
    duration: null,
    content: '',
    instructor: ''
  }
}

// 辅助函数
const getRoleTagType = (role) => {
  const types = {
    '组长': 'success',
    '专家': 'info',
    '审核员': 'warning'
  }
  return types[role] || 'default'
}

const getRoleText = (role) => {
  return role || '未设置'
}

const getRoleIcon = (role) => {
  const icons = {
    '组长': 'carbon:user-role',
    '专家': 'carbon:user-certification',
    '审核员': 'carbon:user'
  }
  return icons[role] || 'carbon:user'
}

const getStatusTagType = (status) => {
  const types = {
    'completed': 'success',
    'in-progress': 'info',
    'pending': 'warning'
  }
  return types[status] || 'default'
}

const getStatusText = (status) => {
  const texts = {
    'completed': '已完成',
    'in-progress': '进行中',
    'pending': '待开始'
  }
  return texts[status] || '未知'
}

const getPlanTimelineType = (status) => {
  const types = {
    'completed': 'success',
    'in-progress': 'info',
    'pending': 'default'
  }
  return types[status] || 'default'
}

const getProgressType = (progress) => {
  if (progress >= 100) return 'success'
  if (progress >= 50) return 'info'
  return 'warning'
}

// 生命周期
onMounted(() => {
  fetchAuditTeam()
  fetchWorkPlans()
  fetchTrainingRecords()
})
</script>

<style scoped>
.planning-page {
  min-height: 100vh;
  background: #f8f9fa;
}

/* 审核工作组卡片样式 */
.audit-team-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e8eaec;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 8px;
}

.header-icon {
  color: #1890ff;
  font-size: 18px;
}

.header-title {
  font-size: 16px;
  font-weight: 600;
  color: #262626;
}

.add-button {
  border-radius: 6px;
  font-weight: 500;
}

.table-container {
  margin-top: 16px;
}

.member-table {
  border-radius: 8px;
  overflow: hidden;
}

.member-table :deep(.n-data-table-th) {
  background: #fafafa;
  font-weight: 600;
  color: #262626;
  border-bottom: 1px solid #e8eaec;
}

.member-table :deep(.n-data-table-td) {
  border-bottom: 1px solid #f0f0f0;
  padding: 12px 16px;
}

.member-table :deep(.n-data-table-tr:hover .n-data-table-td) {
  background: #f8f9fa;
}

.role-tag {
  border-radius: 4px;
  font-weight: 500;
}

.action-button {
  border-radius: 4px;
  font-weight: 500;
}

/* 工作计划卡片样式 */
.work-plan-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e8eaec;
}

/* 培训记录卡片样式 */
.training-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e8eaec;
}
</style>
