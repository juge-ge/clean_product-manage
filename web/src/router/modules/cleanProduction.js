import Layout from '@/layout/index.vue'
import RouterView from '@/components/common/RouterView.vue'

export default {
  path: '/clean-production',
  name: 'CleanProduction',
  component: Layout,
  meta: { 
    title: '清洁生产管理',
    icon: 'mdi:factory',
    order: 1
  },
  children: [
    {
      path: 'policy',
      name: 'Policy',
      component: RouterView,
      meta: { 
        title: '清洁生产政策与管理',
        icon: 'mdi:file-document'
      },
      children: [
        {
          path: 'notice',
          name: 'Notice',
          component: () => import('@/views/clean-production/policy/notice/index.vue'),
          meta: { 
            title: '通知公告',
            icon: 'mdi:bell'
          }
        },
        {
          path: 'news',
          name: 'News',
          component: () => import('@/views/clean-production/policy/news/index.vue'),
          meta: { 
            title: '动态信息',
            icon: 'mdi:newspaper-variant'
          }
        },
        {
          path: 'regulations',
          name: 'Regulations',
          component: () => import('@/views/clean-production/policy/regulations/index.vue'),
          meta: { 
            title: '清洁生产法规政策',
            icon: 'mdi:gavel'
          }
        },
        {
          path: 'capability',
          name: 'Capability',
          component: () => import('@/views/clean-production/policy/capability/index.vue'),
          meta: { 
            title: '能力建设',
            icon: 'mdi:school'
          }
        },
        {
          path: 'meeting',
          name: 'Meeting',
          component: () => import('@/views/clean-production/policy/meeting/index.vue'),
          meta: { 
            title: '会议与宣传',
            icon: 'mdi:presentation'
          }
        }
      ]
    },
    {
      path: 'enterprise-audit',
      name: 'EnterpriseAudit',
      component: () => import('@/views/clean-production/enterprise-audit/index.vue'),
      meta: { 
        title: '企业清洁生产审核管理',
        icon: 'mdi:domain'
      }
    },
    {
      path: 'cases',
      name: 'Cases',
      component: RouterView,
      meta: { 
        title: '清洁生产审核典型案例',
        icon: 'mdi:file-star'
      },
      children: [
        {
          path: 'industrial-park',
          name: 'IndustrialPark',
          component: () => import('@/views/clean-production/cases/industrial-park/index.vue'),
          meta: { 
            title: '工业园区',
            icon: 'mdi:factory'
          }
        },
        {
          path: 'industry',
          name: 'Industry',
          component: () => import('@/views/clean-production/cases/industry/index.vue'),
          meta: { 
            title: '行业',
            icon: 'mdi:domain'
          }
        },
        {
          path: 'enterprise',
          name: 'Enterprise',
          component: () => import('@/views/clean-production/cases/enterprise/index.vue'),
          meta: { 
            title: '企业',
            icon: 'mdi:office-building'
          }
        },
        {
          path: 'region',
          name: 'Region',
          component: () => import('@/views/clean-production/cases/region/index.vue'),
          meta: { 
            title: '区域',
            icon: 'mdi:map'
          }
        }
      ]
    },
    {
      path: 'expert-library',
      name: 'ExpertLibrary',
      component: () => import('@/views/clean-production/expert-library/index.vue'),
      meta: { 
        title: '专家库',
        icon: 'mdi:account-tie'
      }
    },
    {
      path: 'international',
      name: 'International',
      component: () => import('@/views/clean-production/international/index.vue'),
      meta: { 
        title: '国际合作',
        icon: 'mdi:earth'
      }
    }
  ]
}