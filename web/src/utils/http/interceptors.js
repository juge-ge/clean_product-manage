import { getToken } from '@/utils'
import { resolveResError } from './helpers'
import { useUserStore } from '@/store'

export function reqResolve(config) {
  // 处理不需要token的请求
  if (config.noNeedToken) {
    return config
  }

  const token = getToken()
  if (token) {
    // 设置token到请求头
    config.headers.token = token
    // 同时设置Authorization头以兼容
    config.headers.Authorization = `Bearer ${token}`
  }

  // 兜底：JSON写请求若未显式设置Content-Type，自动补全
  const method = (config.method || 'get').toLowerCase()
  const isWrite = method === 'post' || method === 'put' || method === 'patch'
  // 若为 FormData，允许浏览器自动设置 multipart 边界；仅在非 FormData 且未显式设置时兜底为 application/json
  const isFormData = typeof FormData !== 'undefined' && config.data instanceof FormData
  if (
    isWrite &&
    !isFormData &&
    !config.headers['Content-Type'] &&
    !config.headers['content-type']
  ) {
    config.headers['Content-Type'] = 'application/json'
  }
  
  console.log('🔑 请求头设置:', {
    url: config.url,
    hasToken: !!token,
    headers: config.headers
  })

  return config
}

export function reqReject(error) {
  return Promise.reject(error)
}

export function resResolve(response) {
  const { data } = response
  
  // 如果响应成功但没有data，返回整个response
  if (!data) {
    return Promise.resolve(response)
  }

  // 仅当返回体含有 code 字段时，才按业务码校验；否则直接透传
  if (Object.prototype.hasOwnProperty.call(data, 'code')) {
    if (data.code !== 200) {
      const code = data.code
      const message = resolveResError(code, data.msg)
      window.$message?.error(message)
      return Promise.reject({ code, message, data })
    }
    return Promise.resolve(data)
  }

  // 无业务code结构的接口，直接返回原始data
  return Promise.resolve(data)
}

export async function resReject(error) {
  // 处理请求被取消的情况
  if (error.name === 'CanceledError') {
    return Promise.reject(error)
  }

  // 处理网络错误
  if (!error.response) {
    const message = '网络连接失败，请检查网络设置'
    window.$message?.error(message)
    return Promise.reject({ message, error })
  }

  const { data, status } = error.response

  // 处理401未授权
  if (status === 401 || data?.code === 401) {
    const userStore = useUserStore()
    await userStore.logout()
    window.$message?.error('登录已过期，请重新登录')
    return Promise.reject({ code: 401, message: '未授权', error })
  }

  // 处理其他错误
  const code = data?.code ?? status
  const message = resolveResError(code, data?.msg ?? error.message)
  window.$message?.error(message)
  
  return Promise.reject({
    code,
    message,
    error: data || error.response
  })
}