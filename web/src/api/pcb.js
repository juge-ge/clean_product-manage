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
  
  // 保存模块数据
  saveModuleData: (enterpriseId, moduleName, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/pre-audit/module/${moduleName}`, data),
  
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

// 资源能源消耗API
export const resourceConsumptionApi = {
  // 获取所有资源能源消耗数据
  getAllData: (enterpriseId) => 
    request.get(`/resource-consumption/enterprise/${enterpriseId}/all-data`),
  
  // 保存所有资源能源消耗数据
  saveAllData: (enterpriseId, data) => 
    request.post(`/resource-consumption/enterprise/${enterpriseId}/all-data`, data),
  
  // 删除所有资源能源消耗数据
  deleteAllData: (enterpriseId) => 
    request.delete(`/resource-consumption/enterprise/${enterpriseId}/all-data`),
  
  // 用水消耗相关API
  water: {
    // 获取用水分类列表
    getCategories: (enterpriseId) => 
      request.get(`/resource-consumption/enterprise/${enterpriseId}/water-categories`),
    
    // 创建用水分类
    createCategory: (enterpriseId, data) => 
      request.post(`/resource-consumption/enterprise/${enterpriseId}/water-categories`, data),
    
    // 更新用水分类
    updateCategory: (categoryId, data) => 
      request.put(`/resource-consumption/water-categories/${categoryId}`, data),
    
    // 删除用水分类
    deleteCategory: (categoryId) => 
      request.delete(`/resource-consumption/water-categories/${categoryId}`),
    
    // 获取用水记录列表
    getRecords: (enterpriseId, params = {}) => 
      request.get(`/resource-consumption/enterprise/${enterpriseId}/water-records`, { params }),
    
    // 创建用水记录
    createRecord: (enterpriseId, data) => 
      request.post(`/resource-consumption/enterprise/${enterpriseId}/water-records`, data)
  },
  
  // 用电消耗相关API
  electricity: {
    // 获取用电记录列表
    getRecords: (enterpriseId, params = {}) => 
      request.get(`/resource-consumption/enterprise/${enterpriseId}/electricity-records`, { params }),
    
    // 创建用电记录
    createRecord: (enterpriseId, data) => 
      request.post(`/resource-consumption/enterprise/${enterpriseId}/electricity-records`, data),
    
    // 更新用电记录
    updateRecord: (recordId, data) => 
      request.put(`/resource-consumption/electricity-records/${recordId}`, data)
  },
  
  // 天然气消耗相关API
  gas: {
    // 获取天然气记录列表
    getRecords: (enterpriseId, params = {}) => 
      request.get(`/resource-consumption/enterprise/${enterpriseId}/gas-records`, { params }),
    
    // 创建天然气记录
    createRecord: (enterpriseId, data) => 
      request.post(`/resource-consumption/enterprise/${enterpriseId}/gas-records`, data),
    
    // 更新天然气记录
    updateRecord: (recordId, data) => 
      request.put(`/resource-consumption/gas-records/${recordId}`, data),
    
    // 删除天然气记录
    deleteRecord: (recordId) => 
      request.delete(`/resource-consumption/gas-records/${recordId}`)
  },
  
  // 汇总数据相关API
  summary: {
    // 获取汇总数据
    getSummary: (enterpriseId, year) => 
      request.get(`/resource-consumption/enterprise/${enterpriseId}/summary`, { 
        params: year ? { year } : {} 
      }),
    
    // 计算汇总数据
    calculateSummary: (enterpriseId, year) => 
      request.post(`/resource-consumption/enterprise/${enterpriseId}/summary/calculate`, null, { 
        params: { year } 
      })
  }
}

// PCB工艺装备API
export const pcbProcessEquipmentApi = {
  // 获取所有设备数据
  getAllData: (enterpriseId) => 
    request.get(`/process-equipment/enterprise/${enterpriseId}/all-data`),
  
  // 保存所有设备数据
  saveAllData: (enterpriseId, data) => 
    request.post(`/process-equipment/enterprise/${enterpriseId}/all-data`, data),
  
  // 删除所有设备数据
  deleteAllData: (enterpriseId) => 
    request.delete(`/process-equipment/enterprise/${enterpriseId}/all-data`)
}

// PCB污染防治API
export const pcbPollutionControlApi = {
  // 获取所有污染防治数据
  getAllData: (enterpriseId) => 
    request.get(`/pollution-control/enterprise/${enterpriseId}/all-data`),
  
  // 保存所有污染防治数据
  saveAllData: (enterpriseId, data) => 
    request.post(`/pollution-control/enterprise/${enterpriseId}/all-data`, data),
  
  // 删除所有污染防治数据
  deleteAllData: (enterpriseId) => 
    request.delete(`/pollution-control/enterprise/${enterpriseId}/all-data`)
}

// PCB固体废物管理API
export const pcbSolidWasteApi = {
  // 获取所有固体废物数据
  getAllData: (enterpriseId) => 
    request.get(`/solid-waste/enterprise/${enterpriseId}/all-data`),
  
  // 保存所有固体废物数据
  saveAllData: (enterpriseId, data) => 
    request.post(`/solid-waste/enterprise/${enterpriseId}/all-data`, data),
  
  // 删除所有固体废物数据
  deleteAllData: (enterpriseId) => 
    request.delete(`/solid-waste/enterprise/${enterpriseId}/all-data`)
}

// PCB自行监测API
export const pcbSelfMonitoringApi = {
  // 获取所有自行监测数据
  getAllData: (enterpriseId) => 
    request.get(`/self-monitoring/enterprise/${enterpriseId}/all-data`),
  
  // 保存所有自行监测数据
  saveAllData: (enterpriseId, data) => 
    request.post(`/self-monitoring/enterprise/${enterpriseId}/all-data`, data),
  
  // 删除所有自行监测数据
  deleteAllData: (enterpriseId) => 
    request.delete(`/self-monitoring/enterprise/${enterpriseId}/all-data`)
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
  enterpriseRawMaterial: enterpriseRawMaterialApi,
  resourceConsumption: resourceConsumptionApi,
  processEquipment: pcbProcessEquipmentApi,
  pollutionControl: pcbPollutionControlApi,
  solidWaste: pcbSolidWasteApi,
  selfMonitoring: pcbSelfMonitoringApi
}

export default pcbApi