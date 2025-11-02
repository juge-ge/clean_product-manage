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
  getSummary: (enterpriseId, userInputOutputs = null) => {
    const params = userInputOutputs ? { user_input_outputs: userInputOutputs } : {}
    return request.get(`/pcb/enterprise/${enterpriseId}/audit/summary`, { params })
  },
  
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
  getReport: (enterpriseId) => 
    request.get(`/pcb/enterprise/${enterpriseId}/report`),
  
  // 生成审核报告
  generateReport: (enterpriseId, data) => 
    request.post(`/pcb/enterprise/${enterpriseId}/report/generate`, data),
  
  // 预览审核报告
  getPreview: (enterpriseId) => 
    request.get(`/pcb/enterprise/${enterpriseId}/report/preview`),
  
  // 导出Word报告
  exportWord: (enterpriseId) => 
    request.get(`/pcb/enterprise/${enterpriseId}/report/download`),
  
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
    request.delete(`/pcb/enterprise/${enterpriseId}/production-data`),
  
  // 获取近三年产品产量
  getThreeYearsProductOutput: (enterpriseId, yearRange) =>
    request.get(`/pcb/enterprise/${enterpriseId}/production/three-years`, {
      params: { year_range: yearRange }
    }),
  
  // 保存近三年产品产量
  saveThreeYearsProductOutput: (enterpriseId, yearRange, items) =>
    request.post(`/pcb/enterprise/${enterpriseId}/production/three-years`, {
      year_range: yearRange,
      items
    }),
  
  // 获取近三年合格率
  getThreeYearsQualificationRate: (enterpriseId, yearRange) =>
    request.get(`/pcb/enterprise/${enterpriseId}/qualification-rate/three-years`, {
      params: { year_range: yearRange }
    }),
  
  // 保存近三年合格率
  saveThreeYearsQualificationRate: (enterpriseId, yearRange, items) =>
    request.post(`/pcb/enterprise/${enterpriseId}/qualification-rate/three-years`, {
      year_range: yearRange,
      items
    }),
  
  // 获取近三年产值
  getThreeYearsOutputValue: (enterpriseId, yearRange) =>
    request.get(`/pcb/enterprise/${enterpriseId}/output-value/three-years`, {
      params: { year_range: yearRange }
    }),
  
  // 保存近三年产值
  saveThreeYearsOutputValue: (enterpriseId, yearRange, items) =>
    request.post(`/pcb/enterprise/${enterpriseId}/output-value/three-years`, {
      year_range: yearRange,
      items
    }),
  
  // 获取近三年原辅材料使用情况
  getThreeYearsRawMaterialUsage: (enterpriseId, yearRange) =>
    request.get(`/pcb/enterprise/${enterpriseId}/raw-materials/three-years`, {
      params: { year_range: yearRange }
    }),
  
  // 保存近三年原辅材料使用情况
  saveThreeYearsRawMaterialUsage: (enterpriseId, yearRange, items) =>
    request.post(`/pcb/enterprise/${enterpriseId}/raw-materials/three-years`, {
      year_range: yearRange,
      items
    }),
  
  // 获取近三年用水情况
  getThreeYearsWaterConsumption: (enterpriseId, yearRange) =>
    request.get(`/pcb/enterprise/${enterpriseId}/consumption/water/three-years`, {
      params: { year_range: yearRange }
    }),
  
  // 保存近三年用水情况
  saveThreeYearsWaterConsumption: (enterpriseId, yearRange, items) =>
    request.post(`/pcb/enterprise/${enterpriseId}/consumption/water/three-years`, {
      year_range: yearRange,
      items
    }),
  
  // 获取近三年用电情况
  getThreeYearsElectricityConsumption: (enterpriseId, yearRange) =>
    request.get(`/pcb/enterprise/${enterpriseId}/consumption/electricity/three-years`, {
      params: { year_range: yearRange }
    }),
  
  // 保存近三年用电情况
  saveThreeYearsElectricityConsumption: (enterpriseId, yearRange, items) =>
    request.post(`/pcb/enterprise/${enterpriseId}/consumption/electricity/three-years`, {
      year_range: yearRange,
      items
    }),
  
  // 获取近三年天然气情况
  getThreeYearsGasConsumption: (enterpriseId, yearRange) =>
    request.get(`/pcb/enterprise/${enterpriseId}/consumption/gas/three-years`, {
      params: { year_range: yearRange }
    }),
  
  // 保存近三年天然气情况
  saveThreeYearsGasConsumption: (enterpriseId, yearRange, items) =>
    request.post(`/pcb/enterprise/${enterpriseId}/consumption/gas/three-years`, {
      year_range: yearRange,
      items
    })
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
  // 获取企业设备信息
  getEquipment: (enterpriseId) => 
    request.get(`/pcb/enterprise/${enterpriseId}/equipment`),
  
  // 保存企业设备信息
  saveEquipment: (enterpriseId, items) => 
    request.post(`/pcb/enterprise/${enterpriseId}/equipment`, { items }),
  
  // 获取所有设备数据（兼容旧接口）
  getAllData: (enterpriseId) => 
    request.get(`/process-equipment/enterprise/${enterpriseId}/all-data`),
  
  // 保存所有设备数据（兼容旧接口）
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
    request.delete(`/pollution-control/enterprise/${enterpriseId}/all-data`),
  
  // 获取废水产生分析
  getWastewaterAnalysis: (enterpriseId) =>
    request.get(`/pollution-control/enterprise/${enterpriseId}/wastewater-analysis`),
  
  // 批量保存废水产生分析
  batchSaveWastewaterAnalysis: (enterpriseId, items) =>
    request.post(`/pollution-control/enterprise/${enterpriseId}/wastewater-analysis/batch`, items),
  
  // 获取废气产生情况
  getWasteGasAnalysis: (enterpriseId) =>
    request.get(`/pollution-control/enterprise/${enterpriseId}/waste-gas-analysis`),
  
  // 批量保存废气产生情况
  batchSaveWasteGasAnalysis: (enterpriseId, items) =>
    request.post(`/pollution-control/enterprise/${enterpriseId}/waste-gas-analysis/batch`, items),
  
  // 获取近三年废水情况统计
  getThreeYearsWastewaterStat: (enterpriseId, yearRange) =>
    request.get(`/pollution-control/enterprise/${enterpriseId}/wastewater-stat/three-years`, {
      params: { year_range: yearRange }
    }),
  
  // 保存近三年废水情况统计
  saveThreeYearsWastewaterStat: (enterpriseId, yearRange, items) =>
    request.post(`/pollution-control/enterprise/${enterpriseId}/wastewater-stat/three-years`, {
      year_range: yearRange,
      items
    })
}

// PCB固体废物管理API
export const pcbSolidWasteApi = {
  // 获取近三年固体废物情况
  getThreeYearsSolidWaste: (enterpriseId, yearRange) =>
    request.get(`/solid-waste/enterprise/${enterpriseId}/three-years`, {
      params: { year_range: yearRange }
    }),
  
  // 保存近三年固体废物情况
  saveThreeYearsSolidWaste: (enterpriseId, yearRange, items) =>
    request.post(`/solid-waste/enterprise/${enterpriseId}/three-years`, {
      year_range: yearRange,
      items
    }),
  
  // 获取所有固体废物数据（保留旧接口）
  getAllData: (enterpriseId) => 
    request.get(`/solid-waste/enterprise/${enterpriseId}/all-data`),
  
  // 保存所有固体废物数据（保留旧接口）
  saveAllData: (enterpriseId, data) => 
    request.post(`/solid-waste/enterprise/${enterpriseId}/all-data`, data),
  
  // 删除所有固体废物数据
  deleteAllData: (enterpriseId) => 
    request.delete(`/solid-waste/enterprise/${enterpriseId}/all-data`)
}

// PCB资源利用API
export const pcbResourceUtilizationApi = {
  // 能源消耗
  getEnergyConsumption: (enterpriseId) =>
    request.get(`/resource-utilization/enterprise/${enterpriseId}/energy-consumption`),
  
  batchSaveEnergyConsumption: (enterpriseId, items) =>
    request.post(`/resource-utilization/enterprise/${enterpriseId}/energy-consumption`, items),
  
  // 新鲜水耗
  getFreshWaterConsumption: (enterpriseId) =>
    request.get(`/resource-utilization/enterprise/${enterpriseId}/fresh-water-consumption`),
  
  batchSaveFreshWaterConsumption: (enterpriseId, items) =>
    request.post(`/resource-utilization/enterprise/${enterpriseId}/fresh-water-consumption`, items),
  
  // 废水总量
  getWastewaterTotalConsumption: (enterpriseId) =>
    request.get(`/resource-utilization/enterprise/${enterpriseId}/wastewater-total-consumption`),
  
  batchSaveWastewaterTotalConsumption: (enterpriseId, items) =>
    request.post(`/resource-utilization/enterprise/${enterpriseId}/wastewater-total-consumption`, items),
  
  // 废水中总铜浓度
  getWastewaterCuConsumption: (enterpriseId) =>
    request.get(`/resource-utilization/enterprise/${enterpriseId}/wastewater-cu-consumption`),
  
  batchSaveWastewaterCuConsumption: (enterpriseId, items) =>
    request.post(`/resource-utilization/enterprise/${enterpriseId}/wastewater-cu-consumption`, items),
  
  // 废水中COD浓度
  getWastewaterCODConsumption: (enterpriseId) =>
    request.get(`/resource-utilization/enterprise/${enterpriseId}/wastewater-cod-consumption`),
  
  batchSaveWastewaterCODConsumption: (enterpriseId, items) =>
    request.post(`/resource-utilization/enterprise/${enterpriseId}/wastewater-cod-consumption`, items),
  
  // 原/辅料消耗（覆铜板）
  getRawMaterialConsumption: (enterpriseId) =>
    request.get(`/resource-utilization/enterprise/${enterpriseId}/raw-material-consumption`),
  
  batchSaveRawMaterialConsumption: (enterpriseId, items) =>
    request.post(`/resource-utilization/enterprise/${enterpriseId}/raw-material-consumption`, items),
}

// PCB审核选项型数据API
export const pcbAuditOptionsApi = {
  // 生产工艺与装备要求
  getProcessRequirement: (enterpriseId) =>
    request.get(`/pcb/enterprise/${enterpriseId}/process-requirement`),
  
  saveProcessRequirement: (enterpriseId, data) =>
    request.post(`/pcb/enterprise/${enterpriseId}/process-requirement`, data),
  
  // 温室气体排放
  getGreenhouseGasEmission: (enterpriseId) =>
    request.get(`/pcb/enterprise/${enterpriseId}/greenhouse-gas-emission`),
  
  saveGreenhouseGasEmission: (enterpriseId, data) =>
    request.post(`/pcb/enterprise/${enterpriseId}/greenhouse-gas-emission`, data),
  
  // 产品特征
  getProductCharacteristics: (enterpriseId) =>
    request.get(`/pcb/enterprise/${enterpriseId}/product-characteristics`),
  
  saveProductCharacteristics: (enterpriseId, data) =>
    request.post(`/pcb/enterprise/${enterpriseId}/product-characteristics`, data),
  
  // 清洁生产管理
  getCleanProductionManagement: (enterpriseId) =>
    request.get(`/pcb/enterprise/${enterpriseId}/clean-production-management`),
  
  saveCleanProductionManagement: (enterpriseId, data) =>
    request.post(`/pcb/enterprise/${enterpriseId}/clean-production-management`, data),
  
  // 资源综合利用
  getResourceReutilization: (enterpriseId) =>
    request.get(`/pcb/enterprise/${enterpriseId}/resource-reutilization`),
  
  saveResourceReutilization: (enterpriseId, data) =>
    request.post(`/pcb/enterprise/${enterpriseId}/resource-reutilization`, data),
}

// PCB自行监测API
export const pcbSelfMonitoringApi = {
  // 获取有组织废气检测记录
  getOrganizedGasBatch: (enterpriseId) =>
    request.get(`/self-monitoring/enterprise/${enterpriseId}/organized-gas/batch`),
  
  // 批量保存有组织废气检测记录
  batchSaveOrganizedGas: (enterpriseId, items) =>
    request.post(`/self-monitoring/enterprise/${enterpriseId}/organized-gas/batch`, items),
  
  // 获取无组织废气检测记录
  getUnorganizedGasBatch: (enterpriseId) =>
    request.get(`/self-monitoring/enterprise/${enterpriseId}/unorganized-gas/batch`),
  
  // 批量保存无组织废气检测记录
  batchSaveUnorganizedGas: (enterpriseId, items) =>
    request.post(`/self-monitoring/enterprise/${enterpriseId}/unorganized-gas/batch`, items),
  
  // 获取废水排放监测记录
  getWastewaterBatch: (enterpriseId) =>
    request.get(`/self-monitoring/enterprise/${enterpriseId}/wastewater/batch`),
  
  // 批量保存废水排放监测记录
  batchSaveWastewater: (enterpriseId, items) =>
    request.post(`/self-monitoring/enterprise/${enterpriseId}/wastewater/batch`, items),
  
  // 获取废气排放监测记录
  getGasEmissionBatch: (enterpriseId) =>
    request.get(`/self-monitoring/enterprise/${enterpriseId}/gas-emission/batch`),
  
  // 批量保存废气排放监测记录
  batchSaveGasEmission: (enterpriseId, items) =>
    request.post(`/self-monitoring/enterprise/${enterpriseId}/gas-emission/batch`, items),
  
  // 获取噪声监测记录
  getNoiseBatch: (enterpriseId) =>
    request.get(`/self-monitoring/enterprise/${enterpriseId}/noise/batch`),
  
  // 批量保存噪声监测记录
  batchSaveNoise: (enterpriseId, items) =>
    request.post(`/self-monitoring/enterprise/${enterpriseId}/noise/batch`, items),
  
  // 获取所有自行监测数据（保留旧接口）
  getAllData: (enterpriseId) => 
    request.get(`/self-monitoring/enterprise/${enterpriseId}/all-data`),
  
  // 保存所有自行监测数据（保留旧接口）
  saveAllData: (enterpriseId, data) => 
    request.post(`/self-monitoring/enterprise/${enterpriseId}/all-data`, data),
  
  // 删除所有自行监测数据
  deleteAllData: (enterpriseId) => 
    request.delete(`/self-monitoring/enterprise/${enterpriseId}/all-data`)
}

// PCB问题及清洁生产方案API
export const pcbProblemSolutionApi = {
  // 获取Ⅱ级及以下问题清单
  getIssues: (enterpriseId) =>
    request.get(`/pcb/problem-solution/enterprise/${enterpriseId}/issues`),
  
  // 暂存问题清单
  saveIssues: (enterpriseId, items) =>
    request.post(`/pcb/problem-solution/enterprise/${enterpriseId}/issues`, items),
  
  // 获取权重计分配置
  getScoringConfig: (enterpriseId) =>
    request.get(`/pcb/problem-solution/enterprise/${enterpriseId}/scoring-config`),
  
  // 保存权重计分配置
  saveScoringConfig: (enterpriseId, config) =>
    request.post(`/pcb/problem-solution/enterprise/${enterpriseId}/scoring-config`, config),
  
  // 获取无/低费方案列表
  getLowCostSchemes: (enterpriseId) =>
    request.get(`/pcb/problem-solution/enterprise/${enterpriseId}/low-cost-schemes`),
  
  // 批量保存无/低费方案
  batchSaveLowCostSchemes: (enterpriseId, schemes) =>
    request.post(`/pcb/problem-solution/enterprise/${enterpriseId}/low-cost-schemes`, schemes),
  
  // 创建单个无/低费方案
  createLowCostScheme: (enterpriseId, scheme) =>
    request.post(`/pcb/problem-solution/enterprise/${enterpriseId}/low-cost-schemes/single`, scheme),
  
  // 获取方案库无/低费方案（根据指标筛选）
  getLibraryLowCostSchemes: (enterpriseId, indicatorIds = null) => {
    let url = `/pcb/problem-solution/enterprise/${enterpriseId}/scheme-library/low-cost`
    if (indicatorIds && indicatorIds.length > 0) {
      // 对于列表参数，需要重复参数名
      const params = indicatorIds.map(id => `indicator_ids=${id}`).join('&')
      url += `?${params}`
    }
    return request.get(url)
  },
  
  // 更新无/低费方案
  updateLowCostScheme: (enterpriseId, schemeId, scheme) =>
    request.put(`/pcb/problem-solution/enterprise/${enterpriseId}/low-cost-schemes/${schemeId}`, scheme),
  
  // 删除无/低费方案
  deleteLowCostScheme: (enterpriseId, schemeId) =>
    request.delete(`/pcb/problem-solution/enterprise/${enterpriseId}/low-cost-schemes/${schemeId}`),
  
  // 从方案库导入无/低费方案（根据方案ID列表）
  importLowCostSchemes: (enterpriseId, schemeIds) =>
    request.post(`/pcb/problem-solution/enterprise/${enterpriseId}/low-cost-schemes/import`, schemeIds),
  
  // 获取中/高费方案列表
  getMediumHighCostSchemes: (enterpriseId, costLevel = null) => {
    const params = costLevel ? { params: { cost_level: costLevel } } : {}
    return request.get(`/pcb/problem-solution/enterprise/${enterpriseId}/medium-high-cost-schemes`, params)
  },
  
  // 批量保存中/高费方案
  batchSaveMediumHighCostSchemes: (enterpriseId, schemes) =>
    request.post(`/pcb/problem-solution/enterprise/${enterpriseId}/medium-high-cost-schemes`, schemes),
  
  // 创建单个中/高费方案
  createMediumHighCostScheme: (enterpriseId, scheme) =>
    request.post(`/pcb/problem-solution/enterprise/${enterpriseId}/medium-high-cost-schemes/single`, scheme),
  
  // 获取方案库中/高费方案（根据指标筛选）
  getLibraryMediumHighCostSchemes: (enterpriseId, indicatorIds = null, costLevel = null) => {
    let url = `/pcb/problem-solution/enterprise/${enterpriseId}/scheme-library/medium-high-cost`
    const queryParams = []
    if (indicatorIds && indicatorIds.length > 0) {
      // 对于列表参数，需要重复参数名
      indicatorIds.forEach(id => queryParams.push(`indicator_ids=${id}`))
    }
    if (costLevel) {
      queryParams.push(`cost_level=${costLevel}`)
    }
    if (queryParams.length > 0) {
      url += `?${queryParams.join('&')}`
    }
    return request.get(url)
  },
  
  // 更新中/高费方案
  updateMediumHighCostScheme: (enterpriseId, schemeId, scheme) =>
    request.put(`/pcb/problem-solution/enterprise/${enterpriseId}/medium-high-cost-schemes/${schemeId}`, scheme),
  
  // 删除中/高费方案
  deleteMediumHighCostScheme: (enterpriseId, schemeId) =>
    request.delete(`/pcb/problem-solution/enterprise/${enterpriseId}/medium-high-cost-schemes/${schemeId}`),
  
  // 从方案库导入中/高费方案（根据方案ID列表和费用等级）
  importMediumHighCostSchemes: (enterpriseId, data) =>
    request.post(`/pcb/problem-solution/enterprise/${enterpriseId}/medium-high-cost-schemes/import`, data)
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
  resourceUtilization: pcbResourceUtilizationApi,
  auditOptions: pcbAuditOptionsApi,
  processEquipment: pcbProcessEquipmentApi,
  pollutionControl: pcbPollutionControlApi,
  solidWaste: pcbSolidWasteApi,
  selfMonitoring: pcbSelfMonitoringApi,
  problemSolution: pcbProblemSolutionApi
}

export default pcbApi