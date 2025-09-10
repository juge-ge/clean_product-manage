// PCB企业数据mock
export const mockEnterprises = [
  {
    id: 1,
    name: '深圳市宏电科技有限公司',
    city: '深圳市',
    county: '宝安区',
    scale: '大型',
    capital: 5000,
    annualOutput: 50000,
    annualSales: 48000,
    legalRepresentative: '张三',
    address: '深圳市宝安区新安街道某工业园A栋',
    productionAddress: '深圳市宝安区新安街道某工业园A栋3-5层',
    postalCode: '518000',
    contact: '李四',
    phone: '0755-12345678',
    establishmentDate: '2010-01-01',
    industry: 'PCB制造',
    auditStatus: 'in-progress',
    createdAt: '2023-01-01',
    updatedAt: '2023-06-15'
  },
  {
    id: 2,
    name: '广州市兴电电路有限公司',
    city: '广州市',
    county: '番禺区',
    scale: '中型',
    capital: 3000,
    annualOutput: 30000,
    annualSales: 28000,
    legalRepresentative: '王五',
    address: '广州市番禺区某工业园B栋',
    productionAddress: '广州市番禺区某工业园B栋1-2层',
    postalCode: '510000',
    contact: '赵六',
    phone: '020-87654321',
    establishmentDate: '2012-05-15',
    industry: 'PCB制造',
    auditStatus: 'pending',
    createdAt: '2023-02-15',
    updatedAt: '2023-06-20'
  },
  {
    id: 3,
    name: '东莞市联电科技股份有限公司',
    city: '东莞市',
    county: '长安镇',
    scale: '大型',
    capital: 8000,
    annualOutput: 80000,
    annualSales: 75000,
    legalRepresentative: '钱七',
    address: '东莞市长安镇某科技园C栋',
    productionAddress: '东莞市长安镇某科技园C栋全栋',
    postalCode: '523000',
    contact: '孙八',
    phone: '0769-98765432',
    establishmentDate: '2008-08-08',
    industry: 'PCB制造',
    auditStatus: 'completed',
    createdAt: '2023-03-01',
    updatedAt: '2023-06-25'
  }
]

// 审核标准mock数据
export const mockStandards = {
  unitPowerConsumption: {
    level1: 100,
    level2: 150,
    level3: 200,
    unit: 'kWh/m²'
  },
  wastewaterGeneration: {
    level1: 0.2,
    level2: 0.3,
    level3: 0.4,
    unit: 'm³/m²'
  },
  solidWasteGeneration: {
    level1: 0.1,
    level2: 0.15,
    level3: 0.2,
    unit: 'kg/m²'
  }
}

// API响应模拟
export const mockApi = {
  getEnterpriseList: (params) => {
    const { search = '' } = params
    let result = [...mockEnterprises]
    if (search) {
      result = result.filter(item => 
        item.name.includes(search) || 
        item.city.includes(search) ||
        item.county.includes(search)
      )
    }
    return Promise.resolve({ data: result })
  },

  getEnterpriseDetail: (id) => {
    const enterprise = mockEnterprises.find(item => item.id === parseInt(id))
    return Promise.resolve({ data: enterprise })
  },

  createEnterprise: (data) => {
    const newEnterprise = {
      ...data,
      id: mockEnterprises.length + 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
    mockEnterprises.push(newEnterprise)
    return Promise.resolve({ data: newEnterprise })
  },

  updateEnterprise: (id, data) => {
    const index = mockEnterprises.findIndex(item => item.id === parseInt(id))
    if (index > -1) {
      mockEnterprises[index] = {
        ...mockEnterprises[index],
        ...data,
        updatedAt: new Date().toISOString()
      }
      return Promise.resolve({ data: mockEnterprises[index] })
    }
    return Promise.reject(new Error('企业不存在'))
  },

  deleteEnterprise: (id) => {
    const index = mockEnterprises.findIndex(item => item.id === parseInt(id))
    if (index > -1) {
      mockEnterprises.splice(index, 1)
      return Promise.resolve({ message: '删除成功' })
    }
    return Promise.reject(new Error('企业不存在'))
  }
}
