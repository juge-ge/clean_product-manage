// 前端路由调试脚本
import { import.meta } from 'vite'

console.log('=== 调试前端路由 ===')

// 测试 vueModules
const vueModules = import.meta.glob('@/views/**/index.vue')
console.log('vueModules keys:', Object.keys(vueModules))

// 检查目标组件
const targetKey = '/src/views/clean-production/audit/pcb/basic-info/index.vue'
console.log('目标组件key:', targetKey)
console.log('目标组件是否存在:', targetKey in vueModules)

// 检查相关组件
const relatedKeys = [
  '/src/views/clean-production/policy/notice/index.vue',
  '/src/views/clean-production/policy/dynamic-info/index.vue'
]

relatedKeys.forEach(key => {
  console.log(`${key}: ${key in vueModules ? '存在' : '不存在'}`)
})

// 测试组件加载
if (targetKey in vueModules) {
  console.log('尝试加载目标组件...')
  vueModules[targetKey]().then(module => {
    console.log('组件加载成功:', module)
  }).catch(error => {
    console.error('组件加载失败:', error)
  })
}
