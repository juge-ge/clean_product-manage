<template>
  <div class="page-container">
    <!-- 左侧展示区 -->
    <div class="content-area">
      <div class="platform-info">
        <div class="institute-info">
          <img src="@/assets/logo.png" alt="CRAES Logo" class="institute-logo" />
          <h1 class="platform-title">清洁生产智慧管理平台</h1>
        </div>
      </div>

      <div class="feature-cards">
        <div class="feature-card">
          <h3>环境合规管理</h3>
          <p>确保生产活动符合国家和地方的环保法规</p>
        </div>
        <div class="feature-card">
          <h3>合规报告支持</h3>
          <p>自动生成报告、数据分析、决策支持</p>
        </div>
        <div class="feature-card">
          <h3>精细化管理</h3>
          <p>评估和节能方案、帮助企业降低运营成本</p>
        </div>
      </div>

      <div class="institute-name">
        中国环境科学研究院清洁生产与循环经济研究中心
      </div>
    </div>

    <!-- 右侧登录区 -->
    <div class="login-area">
      <div class="login-card">
        <h2>欢迎登录</h2>
        <div class="login-form">
          <div class="form-item">
            <n-input
              v-model:value="loginInfo.username"
              autofocus
              class="login-input"
              placeholder="请输入用户名"
              :maxlength="20"
            />
          </div>
          
          <div class="form-item">
            <n-input
              v-model:value="loginInfo.password"
              class="login-input"
              type="password"
              show-password-on="mousedown"
              placeholder="请输入密码"
              :maxlength="20"
              @keypress.enter="handleLogin"
            />
          </div>

          <div class="form-options">
            <n-checkbox v-model:value="rememberPassword">记住密码</n-checkbox>
            <n-button text type="primary" size="small" @click="handleForgotPassword">忘记密码？</n-button>
          </div>

          <n-button
            class="login-button"
            type="primary"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </n-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { lStorage, setToken, getToken } from '@/utils'
import api from '@/api'
import { usePermissionStore, useUserStore } from '@/store'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { query } = useRoute()
const { t } = useI18n({ useScope: 'global' })
const permissionStore = usePermissionStore()
const userStore = useUserStore()

const loginInfo = ref({
  username: '',
  password: '',
})

initLoginInfo()

function initLoginInfo() {
  const localLoginInfo = lStorage.get('loginInfo')
  if (localLoginInfo) {
    loginInfo.value.username = localLoginInfo.username || ''
    loginInfo.value.password = localLoginInfo.password || ''
  }
}

const loading = ref(false)
const rememberPassword = ref('')

function handleForgotPassword() {
  $message.info('请联系管理员重置密码')
}

async function handleLogin() {
  console.log('🚀 开始登录流程')
  const { username, password } = loginInfo.value
  
  console.log('👤 检查登录信息:', { 
    hasUsername: !!username, 
    hasPassword: !!password 
  })
  
  if (!username || !password) {
    console.log('⚠️ 用户名或密码为空')
    $message.warning(t('views.login.message_input_username_password'))
    return
  }
  
  try {
    loading.value = true
    console.log('🔄 发起登录请求')
    $message.loading(t('views.login.message_verifying'))
    
    const res = await api.login({ username, password: password.toString() })
    console.log('✅ 登录请求成功:', { 
      username,
      hasToken: !!res.data.access_token,
      responseStatus: res.code,
      tokenValue: res.data.access_token
    })
    
    $message.success(t('views.login.message_login_success'))
    
    // 保存token
    const token = res.data.access_token
    setToken(token)
    console.log('💾 Token已保存:', {
      token: token,
      storedToken: getToken()
    })
    
    try {
      console.log('🔄 开始获取用户信息')
      await userStore.getUserInfo()
      console.log('✅ 用户信息获取成功:', {
        userId: userStore.userId,
        name: userStore.name,
        email: userStore.email
      })

      console.log('🔄 开始获取API权限')
      await permissionStore.getAccessApis()
      console.log('✅ API权限获取成功:', {
        apisCount: permissionStore.apis.length
      })
      
      if (rememberPassword.value) {
        console.log('💾 保存登录信息到本地存储')
        lStorage.set('loginInfo', {
          username: loginInfo.value.username,
          password: loginInfo.value.password,
        })
      }
      
      console.log('⏳ 等待路由准备就绪')
      await nextTick()
      
      const targetPath = query.redirect || '/workbench'
      console.log('🎯 准备路由跳转:', {
        targetPath,
        hasRedirect: !!query.redirect,
        currentRoute: router.currentRoute.value.fullPath
      })
      
      try {
        if (query.redirect) {
          const path = query.redirect
          Reflect.deleteProperty(query, 'redirect')
          console.log('🔄 执行重定向跳转:', { path, query })
          await router.push({ path, query })
        } else {
          console.log('🔄 执行工作台跳转')
          await router.push('/workbench')
        }
        console.log('✅ 路由跳转完成')
      } catch (routerError) {
        console.error('❌ 路由跳转失败:', {
          error: routerError,
          message: routerError.message,
          type: routerError.type,
          stack: routerError.stack
        })
        throw routerError
      }
    } catch (error) {
      console.error('❌ 登录流程失败:', {
        error,
        name: error.name,
        message: error.message,
        stack: error.stack
      })
      $message.error('登录失败，请重试')
      throw error
    }
  } catch (e) {
    console.error('login error', e.error)
  }
  loading.value = false
}
</script>

<style lang="scss" scoped>
.page-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(120deg, #004d40, #00796b);
  overflow: hidden;

  .content-area {
    flex: 1;
    padding: 60px;
    color: white;
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;

    &::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: linear-gradient(45deg, rgba(255, 255, 255, 0.05) 25%, transparent 25%),
                  linear-gradient(-45deg, rgba(255, 255, 255, 0.05) 25%, transparent 25%),
                  linear-gradient(45deg, transparent 75%, rgba(255, 255, 255, 0.05) 75%),
                  linear-gradient(-45deg, transparent 75%, rgba(255, 255, 255, 0.05) 75%);
      background-size: 20px 20px;
      opacity: 0.1;
      z-index: 0;
    }

    .platform-info {
      position: relative;
      z-index: 1;
      margin-bottom: 40px;
      
      .institute-info {
        text-align: center;

        .institute-logo {
          width: 200px;
          height: 80px;
          margin-bottom: 30px;
          filter: brightness(1.1);
          object-fit: contain;
        }

        .platform-title {
          font-size: 42px;
          font-weight: 600;
          background: linear-gradient(120deg, #ffffff, #b2dfdb);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
      }
    }

    .institute-name {
      position: absolute;
      bottom: 20px;
      left: 20px;
      font-size: 14px;
      color: #e0f2f1;
      font-weight: 400;
      max-width: 350px;
      line-height: 1.4;
      z-index: 2;
      opacity: 0.8;
    }

    .feature-cards {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 30px;
      position: relative;
      z-index: 1;
      max-width: 1000px;
      margin: 0 auto;
      margin-top: 100px;

      .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 30px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-top: -15px;

        &:hover {
          transform: translateY(-10px);
          background: rgba(255, 255, 255, 0.15);
          border-color: rgba(255, 255, 255, 0.2);
          box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }

        h3 {
          font-size: 22px;
          margin-bottom: 16px;
          color: #4db6ac;
          font-weight: 500;
        }

        p {
          font-size: 16px;
          line-height: 1.6;
          color: #e0f2f1;
          opacity: 0.9;
        }
      }
    }
  }

  .login-area {
    width: 480px;
    background: rgba(255, 255, 255, 0.95);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    box-shadow: -4px 0 25px rgba(0, 0, 0, 0.15);

    .login-card {
      width: 100%;
      max-width: 360px;
      padding: 40px;

      h2 {
        font-size: 28px;
        color: #004d40;
        text-align: center;
        margin-bottom: 40px;
      }

      .login-form {
        .form-item {
          margin-bottom: 24px;

          .login-input {
            height: 50px;
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.8);
            transition: all 0.3s ease;

            &:hover, &:focus {
              background: white;
              box-shadow: 0 0 0 2px rgba(0, 77, 64, 0.2);
            }
          }
        }

        .form-options {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 24px;
          color: #666;
        }

        .login-button {
          width: 100%;
          height: 50px;
          font-size: 16px;
          border-radius: 8px;
          background: linear-gradient(120deg, #004d40, #00796b);
          transition: all 0.3s ease;
          
          &:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 77, 64, 0.3);
          }
        }
      }
    }
  }
}

@media (max-width: 1200px) {
  .page-container {
    .content-area {
      padding: 40px;

      .feature-cards {
        grid-template-columns: repeat(2, 1fr);
        gap: 20px;
      }

      .institute-name {
        bottom: 15px;
        left: 15px;
        font-size: 12px;
      }
    }
  }
}

@media (max-width: 768px) {
  .page-container {
    flex-direction: column;

    .content-area {
      padding: 30px;
      min-height: auto;

      .platform-info {
        margin-bottom: 40px;

        .institute-info {
          .institute-logo {
            width: 80px;
            height: 80px;
            margin-bottom: 20px;
          }
          
          .platform-title {
            font-size: 32px;
          }
        }
      }

      .feature-cards {
        grid-template-columns: 1fr;
        gap: 15px;

        .feature-card {
          padding: 20px;

          h3 {
            font-size: 20px;
            margin-bottom: 12px;
          }

          p {
            font-size: 14px;
          }
        }
      }

      .institute-name {
        position: relative;
        bottom: auto;
        left: auto;
        text-align: center;
        margin-top: 40px;
        padding: 0 20px;
      }
    }

    .login-area {
      width: 100%;
      padding: 20px;

      .login-card {
        padding: 30px 20px;
      }
    }
  }
}
</style>