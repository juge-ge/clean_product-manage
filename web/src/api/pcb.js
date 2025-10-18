import { request } from '@/utils'
// import { mockPlanningApi } from '@/mock/pcb-planning'

// PCB企业管理API
export const pcbEnterpriseApi = {
  // 获取企业列表
  getList: (params = {}) => request.get('/pcb/enterprise', { params }),
  
  // 获取企业详情
  getDetail: (id) => request.get(`/pcb/enterprise/${id}`),
  
  // 创建企业
  create: (data) => request.post('/pcb/enterprise', data),
  
  // 更新企业
  update: (id, data) => request.put(`/pcb/enterprise/${id}`, data),
  
  // 删除企业
  delete: (id) => request.delete(`/pcb/enterprise/${id}`)
}

// PCB指标管理API
export const pcbIndicatorApi = {
  // 获取指标列表
  getList: (params = {}) => request.get('/pcb/indicator', { params }),
  
  // 获取指标树
  getTree: () => request.get('/pcb/indicator/tree'),
  
  // 获取限定性指标
  getLimiting: () => request.get('/pcb/indicator/limiting'),
  
  // 获取指标详情
  getDetail: (id) => request.get(`/pcb/indicator/${id}`)
}

// PCB审核结果API
export const pcbAuditApi = {
  // 获取企业审核结果
  getResults: (enterpriseId) => request.get(`/pcb/enterprise/${enterpriseId}/audit`),
  
  // 更新单个指标审核结果
  updateIndicator: (enterpriseId, indicatorId, data) => 
    request.put(`/pcb/enterprise/${enterpriseId}/audit/indicator/${indicatorId}`, data),
  
  // 批量更新审核结果
  batchUpdate: (enterpriseId, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/audit/batch`, data),
  
  // 获取审核汇总
  getSummary: (enterpriseId) => request.get(`/pcb/enterprise/${enterpriseId}/audit/summary`),
  
  // 自动计算审核结果
  autoCalculate: (enterpriseId) => 
    request.post(`/pcb/enterprise/${enterpriseId}/audit/auto-calculate`)
}

// PCB预审核数据API
export const pcbPreAuditApi = {
  // 获取预审核数据
  getData: (enterpriseId) => request.get(`/pcb/enterprise/${enterpriseId}/pre-audit`),
  
  // 保存预审核数据
  saveData: (enterpriseId, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/pre-audit`, data),
  
  // 提交预审核数据
  submitData: (enterpriseId) => 
    request.post(`/pcb/enterprise/${enterpriseId}/pre-audit/submit`)
}

// PCB方案库API
export const pcbSchemeApi = {
  // 获取方案列表
  getList: (params = {}) => request.get('/pcb/scheme', { params }),
  
  // 获取方案详情
  getDetail: (id) => request.get(`/pcb/scheme/${id}`),
  
  // 创建方案
  create: (data) => request.post('/pcb/scheme', data),
  
  // 更新方案
  update: (id, data) => request.put(`/pcb/scheme/${id}`, data),
  
  // 删除方案
  delete: (id) => request.delete(`/pcb/scheme/${id}`),
  
  // 获取指标推荐方案
  getByIndicator: (indicatorId) => request.get(`/pcb/indicator/${indicatorId}/schemes`),
  
  // 获取企业指标推荐方案
  getByEnterpriseIndicator: (enterpriseId, indicatorId) => 
    request.get(`/pcb/enterprise/${enterpriseId}/audit/schemes/${indicatorId}`)
}

// PCB企业方案API
export const pcbEnterpriseSchemeApi = {
  // 获取企业方案列表
  getList: (enterpriseId, params = {}) => 
    request.get(`/pcb/enterprise/${enterpriseId}/scheme`, { params }),
  
  // 企业选择方案
  select: (enterpriseId, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/scheme`, data),
  
  // 更新企业方案
  update: (enterpriseId, schemeId, data) => 
    request.put(`/pcb/enterprise/${enterpriseId}/scheme/${schemeId}`, data)
}

// PCB筹划与组织API
export const pcbPlanningApi = {
  // 获取审核领导小组
  getLeadershipTeam: (enterpriseId) => 
    request.get(`/pcb/enterprise/${enterpriseId}/leadership-team`),
  
  // 添加审核领导小组成员
  addLeadershipMember: (enterpriseId, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/leadership-team`, data),
  
  // 更新审核领导小组成员
  updateLeadershipMember: (enterpriseId, memberId, data) => 
    request.put(`/pcb/enterprise/${enterpriseId}/leadership-team/${memberId}`, data),
  
  // 删除审核领导小组成员
  deleteLeadershipMember: (enterpriseId, memberId) => 
    request.delete(`/pcb/enterprise/${enterpriseId}/leadership-team/${memberId}`),
  
  // 获取清洁生产工作小组
  getWorkTeam: (enterpriseId) => 
    request.get(`/pcb/enterprise/${enterpriseId}/work-team`),
  
  // 添加清洁生产工作小组成员
  addWorkTeamMember: (enterpriseId, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/work-team`, data),
  
  // 更新清洁生产工作小组成员
  updateWorkTeamMember: (enterpriseId, memberId, data) => 
    request.put(`/pcb/enterprise/${enterpriseId}/work-team/${memberId}`, data),
  
  // 删除清洁生产工作小组成员
  deleteWorkTeamMember: (enterpriseId, memberId) => 
    request.delete(`/pcb/enterprise/${enterpriseId}/work-team/${memberId}`),
  
  // 获取工作计划表
  getWorkPlans: (enterpriseId) => 
    request.get(`/pcb/enterprise/${enterpriseId}/work-plans`),
  
  // 创建工作计划
  createWorkPlan: (enterpriseId, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/work-plans`, data),
  
  // 更新工作计划表
  updateWorkPlans: (enterpriseId, data) => 
    request.put(`/pcb/enterprise/${enterpriseId}/work-plans`, data),
  
  // 获取培训记录
  getTrainingRecords: (enterpriseId) => 
    request.get(`/pcb/enterprise/${enterpriseId}/training-records`),
  
  // 添加培训记录
  addTrainingRecord: (enterpriseId, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/training-records`, data),
  
  // 更新培训记录
  updateTrainingRecord: (enterpriseId, recordId, data) => 
    request.put(`/pcb/enterprise/${enterpriseId}/training-records/${recordId}`, data),
  
  // 删除培训记录
  deleteTrainingRecord: (enterpriseId, recordId) => 
    request.delete(`/pcb/enterprise/${enterpriseId}/training-records/${recordId}`)
}

// PCB审核报告API
export const pcbReportApi = {
  // 获取审核报告
  getReport: (enterpriseId) => request.get(`/pcb/enterprise/${enterpriseId}/report`),
  
  // 生成审核报告
  generate: (enterpriseId, params) => 
    request.post(`/pcb/enterprise/${enterpriseId}/report/generate`, null, { params }),
  
  // 提交审核报告
  submit: (enterpriseId) => 
    request.post(`/pcb/enterprise/${enterpriseId}/report/submit`)
}

// PCB企业生产情况数据API
export const pcbProductionApi = {
  // 获取企业生产情况数据
  getData: (enterpriseId) => 
    request.get(`/pcb/enterprise/${enterpriseId}/production-data`),
  
  // 保存企业生产情况数据
  saveData: (enterpriseId, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/production-data`, data),
  
  // 更新企业生产情况数据
  updateData: (enterpriseId, data) => 
    request.put(`/pcb/enterprise/${enterpriseId}/production-data`, data),
  
  // 删除企业生产情况数据
  deleteData: (enterpriseId) => 
    request.delete(`/pcb/enterprise/${enterpriseId}/production-data`)
}

// 原辅材料API
export const rawMaterialApi = {
  // 获取原辅材料列表
  getMaterials: (params = {}) => request.get('/raw-material/materials', { params }),
  
  // 创建原辅材料
  create: (data) => request.post('/raw-material/materials', data),
  
  // 获取原辅材料详情
  getDetail: (id) => request.get(`/raw-material/materials/${id}`),
  
  // 更新原辅材料
  update: (id, data) => request.put(`/raw-material/materials/${id}`, data),
  
  // 删除原辅材料
  delete: (id) => request.delete(`/raw-material/materials/${id}`)
}

// 企业原辅材料使用情况API
export const enterpriseRawMaterialApi = {
  // 获取企业原辅材料使用情况
  getUsage: (enterpriseId, year) => 
    request.get(`/pcb/enterprise/${enterpriseId}/raw-materials`, { 
      params: year ? { year } : {} 
    }),
  
  // 保存企业原辅材料使用情况
  saveUsage: (enterpriseId, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/raw-materials`, data),
  
  // 更新企业原辅材料使用情况
  updateUsage: (enterpriseId, data) => 
    request.put(`/pcb/enterprise/${enterpriseId}/raw-materials`, data),
  
  // 获取企业原辅材料使用统计
  getStatistics: (enterpriseId, year) => 
    request.get(`/pcb/enterprise/${enterpriseId}/raw-materials/statistics`, { 
      params: year ? { year } : {} 
    })
}

// 统一的PCB API对象
export const pcbApi = {
  enterprise: pcbEnterpriseApi,
  indicator: pcbIndicatorApi,
  audit: pcbAuditApi,
  preAudit: pcbPreAuditApi,
  planning: pcbPlanningApi,
  scheme: pcbSchemeApi,
  enterpriseScheme: pcbEnterpriseSchemeApi,
  report: pcbReportApi,
  production: pcbProductionApi,
  rawMaterial: rawMaterialApi,
  enterpriseRawMaterial: enterpriseRawMaterialApi
}

export default pcbApi