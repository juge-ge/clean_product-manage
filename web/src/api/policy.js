import { request } from '@/utils'

export const policyApi = {
  // 动态信息相关
  getDynamicList: (params) => request.get('/api/v1/policy/dynamic', { params }),
  getDynamicDetail: (id) => request.get(`/api/v1/policy/dynamic/${id}`),
  searchDynamics: (params) => request.get('/api/v1/policy/dynamic/search', { params }),
  getDynamicByType: (type, params) => request.get(`/api/v1/policy/dynamic/type/${type}`, { params }),
  
  // 法规政策相关
  getRegulationList: (params) => request.get('/api/v1/policy/regulation', { params }),
  getRegulationDetail: (id) => request.get(`/api/v1/policy/regulation/${id}`),
  getRegulationByCategory: (category, params) => request.get(`/api/v1/policy/regulation/category/${category}`, { params }),
  downloadRegulation: (id) => request.get(`/api/v1/policy/regulation/${id}/download`, { responseType: 'blob' }),
  searchRegulations: (params) => request.get('/api/v1/policy/regulation/search', { params }),
  
  // 能力建设相关
  getPersonnelList: (params) => request.get('/api/v1/policy/personnel', { params }),
  getPersonnelDetail: (id) => request.get(`/api/v1/policy/personnel/${id}`),
  getPersonnelByType: (type, params) => request.get(`/api/v1/policy/personnel/type/${type}`, { params }),
  searchPersonnel: (params) => request.get('/api/v1/policy/personnel/search', { params }),
  contactPersonnel: (id, data) => request.post(`/api/v1/policy/personnel/${id}/contact`, data),
  
  // 会议与宣传相关
  getMeetingList: (params) => request.get('/api/v1/policy/meeting', { params }),
  getMeetingDetail: (id) => request.get(`/api/v1/policy/meeting/${id}`),
  getVideoList: (params) => request.get('/api/v1/policy/video', { params }),
  getVideoDetail: (id) => request.get(`/api/v1/policy/video/${id}`),
  updateVideoViewCount: (id) => request.post(`/api/v1/policy/video/${id}/view`),
  searchMeetings: (params) => request.get('/api/v1/policy/meeting/search', { params }),
  searchVideos: (params) => request.get('/api/v1/policy/video/search', { params }),
  downloadMeetingAttachment: (meetingId, attachmentId) => request.get(`/api/v1/policy/meeting/${meetingId}/attachment/${attachmentId}/download`, { responseType: 'blob' })
}

export default policyApi
