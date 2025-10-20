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
      path: 'meetings-publicity',
      name: 'MeetingsPublicity',
      component: () => import('@/views/clean-production/meetings-publicity/index.vue'),
      meta: { 
        title: '会议与宣传',
        icon: 'mdi:presentation'
      }
    },
    {
      path: 'enterprise-audit-management',
      name: 'EnterpriseAuditManagement',
      component: () => import('@/views/clean-production/enterprise-audit-management/index.vue'),
      meta: { 
        title: '企业清洁生产审核管理',
        icon: 'mdi:domain'
      }
    },
    {
      path: 'typical-cases',
      name: 'TypicalCases',
      component: () => import('@/views/clean-production/typical-cases/index.vue'),
      meta: { 
        title: '清洁生产审核典型案例',
        icon: 'mdi:file-star'
      }
    },
    {
      path: 'industrial-parks',
      name: 'IndustrialParks',
      component: () => import('@/views/clean-production/industrial-parks/index.vue'),
      meta: { 
        title: '工业园区',
        icon: 'mdi:factory'
      }
    },
    {
      path: 'industry',
      name: 'Industry',
      component: () => import('@/views/clean-production/industry/index.vue'),
      meta: { 
        title: '行业',
        icon: 'mdi:domain'
      }
    },
    {
      path: 'enterprises',
      name: 'Enterprises',
      component: () => import('@/views/clean-production/enterprises/index.vue'),
      meta: { 
        title: '企业',
        icon: 'mdi:office-building'
      }
    },
    {
      path: 'regions',
      name: 'Regions',
      component: () => import('@/views/clean-production/regions/index.vue'),
      meta: { 
        title: '区域',
        icon: 'mdi:map'
      }
    },
    {
      path: 'expert-database',
      name: 'ExpertDatabase',
      component: () => import('@/views/clean-production/expert-database/index.vue'),
      meta: { 
        title: '专家库',
        icon: 'mdi:account-tie'
      }
    },
    {
      path: 'international-cooperation',
      name: 'InternationalCooperation',
      component: () => import('@/views/clean-production/international-cooperation/index.vue'),
      meta: { 
        title: '国际合作',
        icon: 'mdi:earth'
      }
    },
    {
      path: 'technology-integration',
      name: 'TechnologyIntegration',
      component: () => import('@/views/clean-production/technology-integration/index.vue'),
      meta: { 
        title: '清洁生产技术集成',
        icon: 'mdi:cog'
      }
    },
    {
      path: 'smart-decision',
      name: 'SmartDecision',
      component: () => import('@/views/clean-production/smart-decision/index.vue'),
      meta: { 
        title: '清洁生产智慧决策',
        icon: 'mdi:brain'
      }
    }
  ]
}