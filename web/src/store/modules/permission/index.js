import { defineStore } from 'pinia'
import api from '@/api'
import { basicRoutes, businessRoutes } from '@/router'

export const usePermissionStore = defineStore('permission', {
  state() {
    return {
      accessApis: [], // 用户可访问的API列表
    }
  },
  getters: {
    routes() {
      return [...basicRoutes, ...businessRoutes]
    },
    menus() {
      return this.routes.filter(route => route.name && !route.meta?.hidden)
    },
    apis() {
      return this.accessApis
    },
  },
  actions: {
    // 获取用户可访问的API列表
    async getAccessApis() {
      const res = await api.getUserApi()
      this.accessApis = res.data
      return this.accessApis
    },
    // 重置权限状态
    resetPermission() {
      this.$reset()
    },
  },
})