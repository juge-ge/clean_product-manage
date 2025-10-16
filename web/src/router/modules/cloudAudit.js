import Layout from '@/layout/index.vue'

export default {
  path: '/cloud-audit',
  name: 'CloudAudit',
  component: Layout,
  meta: { 
    title: '清洁生产云审核',
    icon: 'carbon:cloud',
    order: 2
  },
  children: [
    // 钢铁行业审核
    {
      path: 'steel',
      name: 'Steel',
      component: () => import('@/views/cloud-audit/steel/index.vue'),
      meta: { 
        title: '钢铁行业审核',
        icon: 'carbon:industry'
      }
    },
    // 钢铁企业详情
    {
      path: 'steel/:id',
      name: 'SteelDetail',
      component: () => import('@/views/cloud-audit/steel/enterprise-detail/index.vue'),
      meta: { 
        title: '钢铁企业详情',
        hidden: true
      }
    },
    // 平板玻璃行业审核
    {
      path: 'glass',
      name: 'Glass',
      component: () => import('@/views/cloud-audit/glass/index.vue'),
      meta: { 
        title: '平板玻璃行业审核',
        icon: 'mdi:glass-wine'
      }
    },
    // 焦化行业审核
    {
      path: 'coking',
      name: 'Coking',
      component: () => import('@/views/cloud-audit/coking/index.vue'),
      meta: { 
        title: '焦化行业审核',
        icon: 'carbon:chemistry'
      }
    },
    // PCB行业审核
    {
      path: 'pcb',
      name: 'PCB',
      component: () => import('@/views/cloud-audit/pcb/index.vue'),
      meta: { 
        title: 'PCB行业审核',
        icon: 'carbon:chip'
      }
    },
    // 家具行业审核
    {
      path: 'furniture',
      name: 'Furniture',
      component: () => import('@/views/cloud-audit/furniture/index.vue'),
      meta: { 
        title: '家具行业审核',
        icon: 'mdi:sofa'
      }
    },
    // 汽修行业审核
    {
      path: 'auto-repair',
      name: 'AutoRepair',
      component: () => import('@/views/cloud-audit/auto-repair/index.vue'),
      meta: { 
        title: '汽修行业审核',
        icon: 'carbon:car'
      }
    }
  ]
}
