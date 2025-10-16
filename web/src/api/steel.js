import { request } from '@/utils'

export default {
  // 钢铁企业列表
  getEnterpriseList: (params = {}) => request.get('/steel/enterprises', { params }),
  getEnterpriseDetail: (id) => request.get(`/steel/enterprises/${id}`),
  createEnterprise: (data = {}) => request.post('/steel/enterprises', data),
  updateEnterprise: (id, data = {}) => request.put(`/steel/enterprises/${id}`, data),
  deleteEnterprise: (id) => request.delete(`/steel/enterprises/${id}`),

  // 审核团队
  getAuditTeam: (enterpriseId) => request.get(`/steel/enterprises/${enterpriseId}/audit-team`),
  createAuditTeamMember: (enterpriseId, data = {}) => request.post(`/steel/enterprises/${enterpriseId}/audit-team`, data),
  updateAuditTeamMember: (enterpriseId, memberId, data = {}) => request.put(`/steel/enterprises/${enterpriseId}/audit-team/${memberId}`, data),
  deleteAuditTeamMember: (enterpriseId, memberId) => request.delete(`/steel/enterprises/${enterpriseId}/audit-team/${memberId}`),

  // 工作计划
  getWorkPlans: (enterpriseId) => request.get(`/steel/enterprises/${enterpriseId}/work-plans`),
  createWorkPlan: (enterpriseId, data = {}) => request.post(`/steel/enterprises/${enterpriseId}/work-plans`, data),
  updateWorkPlan: (enterpriseId, planId, data = {}) => request.put(`/steel/enterprises/${enterpriseId}/work-plans/${planId}`, data),
  deleteWorkPlan: (enterpriseId, planId) => request.delete(`/steel/enterprises/${enterpriseId}/work-plans/${planId}`),

  // 培训记录
  getTrainingRecords: (enterpriseId) => request.get(`/steel/enterprises/${enterpriseId}/training-records`),
  createTrainingRecord: (enterpriseId, data = {}) => request.post(`/steel/enterprises/${enterpriseId}/training-records`, data),
  updateTrainingRecord: (enterpriseId, recordId, data = {}) => request.put(`/steel/enterprises/${enterpriseId}/training-records/${recordId}`, data),
  deleteTrainingRecord: (enterpriseId, recordId) => request.delete(`/steel/enterprises/${enterpriseId}/training-records/${recordId}`),

  // 预审核数据
  getPreAuditData: (enterpriseId) => request.get(`/steel/enterprises/${enterpriseId}/pre-audit`),
  submitPreAuditData: (enterpriseId, data = {}) => request.post(`/steel/enterprises/${enterpriseId}/pre-audit`, data),

  // 审核结果
  getAuditResults: (enterpriseId) => request.get(`/steel/enterprises/${enterpriseId}/audit-results`),
  submitAuditResults: (enterpriseId, data = {}) => request.post(`/steel/enterprises/${enterpriseId}/audit-results`, data),

  // 方案库
  getSchemes: (enterpriseId, params = {}) => request.get(`/steel/enterprises/${enterpriseId}/schemes`, { params }),
  getRecommendedSchemes: (enterpriseId) => request.get(`/steel/enterprises/${enterpriseId}/recommended-schemes`),
  createScheme: (enterpriseId, data = {}) => request.post(`/steel/enterprises/${enterpriseId}/schemes`, data),
  updateScheme: (enterpriseId, schemeId, data = {}) => request.put(`/steel/enterprises/${enterpriseId}/schemes/${schemeId}`, data),
  deleteScheme: (enterpriseId, schemeId) => request.delete(`/steel/enterprises/${enterpriseId}/schemes/${schemeId}`),

  // 报告生成
  generateReport: (enterpriseId) => request.post(`/steel/enterprises/${enterpriseId}/generate-report`),
  getReport: (enterpriseId) => request.get(`/steel/enterprises/${enterpriseId}/report`),
  exportReport: (enterpriseId, format = 'pdf') => request.get(`/steel/enterprises/${enterpriseId}/export-report`, { 
    params: { format },
    responseType: 'blob'
  })
}
