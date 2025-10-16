// 会议与宣传Mock数据
const mockMeetingData = [
  {
    id: 1,
    title: '2025年全国清洁生产工作会议',
    content: '会议将总结2024年清洁生产工作，部署2025年重点任务，交流各地经验做法，推动清洁生产工作再上新台阶。\n\n会议议程：\n1. 开幕式及领导讲话\n2. 2024年清洁生产工作总结\n3. 2025年清洁生产工作部署\n4. 经验交流发言\n5. 分组讨论\n6. 会议总结',
    summary: '总结2024年工作，部署2025年任务，交流各地经验做法，推动清洁生产工作再上新台阶。',
    startDate: '2025-03-15',
    endDate: '2025-03-17',
    location: '北京国际会议中心',
    organizer: '生态环境部',
    type: 'conference',
    status: 'upcoming',
    participants: 500,
    attachments: [
      { name: '会议议程.pdf', url: '/files/meeting-agenda-2025.pdf' },
      { name: '参会须知.pdf', url: '/files/meeting-guide-2025.pdf' }
    ],
    agenda: [
      { time: '09:00', topic: '开幕式', speaker: '部长' },
      { time: '10:00', topic: '工作报告', speaker: '司长' },
      { time: '11:00', topic: '经验交流', speaker: '各省代表' },
      { time: '14:00', topic: '分组讨论', speaker: '全体参会人员' },
      { time: '16:00', topic: '会议总结', speaker: '副部长' }
    ],
    speakers: ['部长', '司长', '副部长', '各省代表']
  },
  {
    id: 2,
    title: '清洁生产审核技术培训会',
    content: '为提高清洁生产审核人员技术水平，规范审核流程，提升审核质量，特举办此次培训会。\n\n培训内容：\n1. 清洁生产审核基础知识\n2. 审核流程和方法\n3. 技术方案制定\n4. 审核报告编写\n5. 案例分析',
    summary: '为提高清洁生产审核人员技术水平，规范审核流程，提升审核质量，特举办此次培训会。',
    startDate: '2025-02-20',
    endDate: '2025-02-22',
    location: '上海国际会议中心',
    organizer: '中国清洁生产中心',
    type: 'training',
    status: 'upcoming',
    participants: 200,
    attachments: [
      { name: '培训大纲.pdf', url: '/files/training-outline.pdf' }
    ],
    agenda: [
      { time: '09:00', topic: '清洁生产基础知识', speaker: '张教授' },
      { time: '10:30', topic: '审核流程和方法', speaker: '李专家' },
      { time: '14:00', topic: '技术方案制定', speaker: '王工程师' },
      { time: '15:30', topic: '审核报告编写', speaker: '赵研究员' }
    ],
    speakers: ['张教授', '李专家', '王工程师', '赵研究员']
  },
  {
    id: 3,
    title: '清洁生产技术交流会',
    content: '会议将展示最新的清洁生产技术成果，促进技术交流与合作，推动清洁生产技术产业化应用。\n\n交流内容：\n1. 清洁生产技术成果展示\n2. 技术交流与讨论\n3. 产学研合作洽谈\n4. 技术转移对接',
    summary: '展示最新的清洁生产技术成果，促进技术交流与合作，推动清洁生产技术产业化应用。',
    startDate: '2025-01-25',
    endDate: '2025-01-26',
    location: '深圳会展中心',
    organizer: '中国环境科学学会',
    type: 'meeting',
    status: 'completed',
    participants: 300,
    attachments: [
      { name: '会议纪要.pdf', url: '/files/meeting-summary.pdf' },
      { name: '技术成果汇编.pdf', url: '/files/technology-achievements.pdf' }
    ],
    agenda: [
      { time: '09:00', topic: '技术成果展示', speaker: '各企业代表' },
      { time: '10:30', topic: '技术交流讨论', speaker: '专家学者' },
      { time: '14:00', topic: '产学研合作洽谈', speaker: '全体参会人员' },
      { time: '16:00', topic: '技术转移对接', speaker: '技术转移机构' }
    ],
    speakers: ['各企业代表', '专家学者', '技术转移机构']
  }
]

const mockVideoData = [
  {
    id: 1,
    title: '清洁生产基础知识培训',
    description: '全面介绍清洁生产的基本概念、原理和方法，适合初学者和从业人员学习。内容包括清洁生产的定义、发展历程、基本原理、实施步骤等。',
    videoUrl: '/videos/clean-production-basics.mp4',
    thumbnail: '/thumbnails/basics.jpg',
    duration: 3600, // 60分钟
    category: '培训',
    tags: ['基础知识', '培训', '清洁生产'],
    viewCount: 2500,
    publishDate: '2025-01-10',
    isRecommended: true
  },
  {
    id: 2,
    title: '清洁生产审核流程详解',
    description: '详细介绍清洁生产审核的完整流程，包括审核准备、现状调研、方案制定、实施评估等各个环节的具体操作方法。',
    videoUrl: '/videos/audit-process.mp4',
    thumbnail: '/thumbnails/audit.jpg',
    duration: 4800, // 80分钟
    category: '培训',
    tags: ['审核流程', '培训', '操作方法'],
    viewCount: 1800,
    publishDate: '2025-01-08',
    isRecommended: true
  },
  {
    id: 3,
    title: '清洁生产技术案例分享',
    description: '通过实际案例分析，展示清洁生产技术在各个行业的应用效果，包括化工、钢铁、建材、纺织等行业的成功案例。',
    videoUrl: '/videos/technology-cases.mp4',
    thumbnail: '/thumbnails/cases.jpg',
    duration: 5400, // 90分钟
    category: '案例',
    tags: ['技术案例', '行业应用', '成功案例'],
    viewCount: 3200,
    publishDate: '2025-01-05',
    isRecommended: false
  },
  {
    id: 4,
    title: '清洁生产政策解读',
    description: '深入解读最新的清洁生产政策法规，帮助企业和从业人员了解政策要求，把握发展机遇。',
    videoUrl: '/videos/policy-interpretation.mp4',
    thumbnail: '/thumbnails/policy.jpg',
    duration: 2700, // 45分钟
    category: '政策',
    tags: ['政策解读', '法规', '发展机遇'],
    viewCount: 1500,
    publishDate: '2025-01-03',
    isRecommended: false
  },
  {
    id: 5,
    title: '清洁生产技术创新发展',
    description: '介绍清洁生产技术的最新发展趋势，包括绿色技术、循环经济、智能制造等前沿技术的应用。',
    videoUrl: '/videos/technology-innovation.mp4',
    thumbnail: '/thumbnails/innovation.jpg',
    duration: 4200, // 70分钟
    category: '技术',
    tags: ['技术创新', '发展趋势', '前沿技术'],
    viewCount: 2100,
    publishDate: '2025-01-01',
    isRecommended: true
  }
]

export const mockMeetingApi = {
  getMeetingList: (params) => {
    const { page = 1, pageSize = 10, search = '', type = '', status = '' } = params
    let data = mockMeetingData
    
    if (search) {
      data = data.filter(item => 
        item.title.includes(search) || 
        item.summary.includes(search) ||
        item.organizer.includes(search)
      )
    }
    
    if (type) {
      data = data.filter(item => item.type === type)
    }
    
    if (status) {
      data = data.filter(item => item.status === status)
    }
    
    const start = (page - 1) * pageSize
    const end = start + pageSize
    
    return Promise.resolve({
      data: {
        list: data.slice(start, end),
        total: data.length,
        page,
        pageSize
      }
    })
  },

  getMeetingDetail: (id) => {
    const item = mockMeetingData.find(item => item.id === parseInt(id))
    return Promise.resolve({ data: item })
  },

  getVideoList: (params) => {
    const { page = 1, pageSize = 10, search = '', category = '', isRecommended = null } = params
    let data = mockVideoData
    
    if (search) {
      data = data.filter(item => 
        item.title.includes(search) || 
        item.description.includes(search) ||
        item.tags.some(tag => tag.includes(search))
      )
    }
    
    if (category) {
      data = data.filter(item => item.category === category)
    }
    
    if (isRecommended !== null) {
      data = data.filter(item => item.isRecommended === isRecommended)
    }
    
    const start = (page - 1) * pageSize
    const end = start + pageSize
    
    return Promise.resolve({
      data: {
        list: data.slice(start, end),
        total: data.length,
        page,
        pageSize
      }
    })
  },

  getVideoDetail: (id) => {
    const item = mockVideoData.find(item => item.id === parseInt(id))
    return Promise.resolve({ data: item })
  },

  updateVideoViewCount: (id) => {
    const item = mockVideoData.find(item => item.id === parseInt(id))
    if (item) {
      item.viewCount += 1
    }
    return Promise.resolve({ data: { success: true } })
  }
}

export default {
  meetings: mockMeetingData,
  videos: mockVideoData
}
