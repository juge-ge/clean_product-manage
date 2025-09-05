import Layout from '@/layout/index.vue'

export default {
  path: '/technology-integration',
  name: 'TechnologyIntegration',
  component: Layout,
  meta: { 
    title: '清洁生产技术集成',
    icon: 'mdi:cog-transfer',
    order: 3
  },
  children: [
    {
      path: 'industry-technology',
      name: 'IndustryTechnology',
      component: () => import('@/views/technology-integration/industry-technology/index.vue'),
      meta: { 
        title: '行业技术库',
        icon: 'mdi:database'
      }
    },
    {
      path: 'simulation',
      name: 'Simulation',
      component: () => import('@/views/technology-integration/simulation/index.vue'),
      meta: { 
        title: '模拟评估',
        icon: 'mdi:chart-line'
      }
    }
  ]
}
