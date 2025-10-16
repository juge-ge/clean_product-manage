// 钢铁企业列表Mock数据
const mockEnterprises = [
  {
    id: 1,
    name: '某某钢铁有限公司',
    city: '石家庄市',
    county: '鹿泉区',
    scale: '大型',
    capital: 50000,
    annualOutput: 500,  // 万吨
    annualSales: 250000,
    legalRepresentative: '张三',
    address: '河北省石家庄市鹿泉区工业园区',
    productionAddress: '河北省石家庄市鹿泉区工业园区',
    postalCode: '050200',
    contact: '李四',
    phone: '13800138001',
    establishmentDate: '2010-01-01',
    industry: '钢铁制造',
    productionCapacity: 600,
    mainProducts: '螺纹钢、线材、中厚板',
    auditStatus: 'in-progress',
    createdAt: '2024-01-01T00:00:00Z',
    updatedAt: '2024-01-15T00:00:00Z'
  },
  {
    id: 2,
    name: 'XX钢铁集团股份有限公司',
    city: '唐山市',
    county: '迁安市',
    scale: '特大型',
    capital: 200000,
    annualOutput: 2000,
    annualSales: 1000000,
    legalRepresentative: '王五',
    address: '河北省唐山市迁安市钢城区',
    productionAddress: '河北省唐山市迁安市钢城区',
    postalCode: '064400',
    contact: '赵六',
    phone: '13800138002',
    establishmentDate: '2005-06-01',
    industry: '钢铁制造',
    productionCapacity: 2500,
    mainProducts: '热轧板卷、冷轧板卷、镀锌板',
    auditStatus: 'pending',
    createdAt: '2024-02-01T00:00:00Z',
    updatedAt: '2024-02-10T00:00:00Z'
  },
  {
    id: 3,
    name: '河北钢铁股份有限公司',
    city: '邯郸市',
    county: '武安市',
    scale: '大型',
    capital: 150000,
    annualOutput: 800,
    annualSales: 400000,
    legalRepresentative: '孙七',
    address: '河北省邯郸市武安市工业园区',
    productionAddress: '河北省邯郸市武安市工业园区',
    postalCode: '056300',
    contact: '周八',
    phone: '13800138003',
    establishmentDate: '2008-03-15',
    industry: '钢铁制造',
    productionCapacity: 1000,
    mainProducts: '中厚板、热轧卷板、冷轧卷板',
    auditStatus: 'completed',
    createdAt: '2024-01-15T00:00:00Z',
    updatedAt: '2024-03-01T00:00:00Z'
  }
]

// Mock API
export const mockApi = {
  getEnterpriseList: (params = {}) => {
    const { search = '' } = params
    let filteredData = mockEnterprises
    
    if (search) {
      filteredData = mockEnterprises.filter(e => 
        e.name.includes(search) || 
        e.city.includes(search) || 
        e.county.includes(search)
      )
    }
    
    return Promise.resolve({
      data: filteredData
    })
  },
  
  getEnterpriseDetail: (id) => {
    const enterprise = mockEnterprises.find(e => e.id === parseInt(id))
    return Promise.resolve({
      data: enterprise || {}
    })
  },
  
  createEnterprise: (data) => {
    const newEnterprise = {
      ...data,
      id: mockEnterprises.length + 1,
      auditStatus: 'pending',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
    mockEnterprises.push(newEnterprise)
    return Promise.resolve({
      data: newEnterprise
    })
  },
  
  updateEnterprise: (id, data) => {
    const index = mockEnterprises.findIndex(e => e.id === parseInt(id))
    if (index > -1) {
      mockEnterprises[index] = {
        ...mockEnterprises[index],
        ...data,
        updatedAt: new Date().toISOString()
      }
      return Promise.resolve({
        data: mockEnterprises[index]
      })
    }
    return Promise.reject(new Error('企业不存在'))
  },
  
  deleteEnterprise: (id) => {
    const index = mockEnterprises.findIndex(e => e.id === parseInt(id))
    if (index > -1) {
      mockEnterprises.splice(index, 1)
      return Promise.resolve({
        message: '删除成功'
      })
    }
    return Promise.reject(new Error('企业不存在'))
  }
}
