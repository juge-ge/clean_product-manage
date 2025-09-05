import Layout from '@/layout/index.vue'

export default {
  path: '/smart-decision',
  name: 'SmartDecision',
  component: Layout,
  meta: { 
    title: '清洁生产智慧决策',
    icon: 'mdi:brain',
    order: 4
  },
  children: [
    {
      path: 'enterprise-distribution',
      name: 'EnterpriseDistribution',
      component: () => import('@/views/smart-decision/enterprise-distribution/index.vue'),
      meta: { 
        title: '企业分布图谱',
        icon: 'mdi:map'
      }
    },
    {
      path: 'audit-effect',
      name: 'AuditEffect',
      component: () => import('@/views/smart-decision/audit-effect/index.vue'),
      meta: { 
        title: '清洁生产审核成效图谱',
        icon: 'mdi:chart-line'
      }
    }
  ]
}
