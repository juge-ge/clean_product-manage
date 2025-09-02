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
import { lStorage, setToken } from '@/utils'
import api from '@/api'
import { addDynamicRoutes } from '@/router'
import { useI18n } from 'vue-i18n'

const router = useRouter()
const { query } = useRoute()
const { t } = useI18n({ useScope: 'global' })

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
const rememberPassword = ref(false)

function handleForgotPassword() {
  $message.info('请联系管理员重置密码')
}

async function handleLogin() {
  const { username, password } = loginInfo.value
  if (!username || !password) {
    $message.warning(t('views.login.message_input_username_password'))
    return
  }
  try {
    loading.value = true
    $message.loading(t('views.login.message_verifying'))
    const res = await api.login({ username, password: password.toString() })
    $message.success(t('views.login.message_login_success'))
    setToken(res.data.access_token)
    await addDynamicRoutes()
    if (query.redirect) {
      const path = query.redirect
      console.log('path', { path, query })
      Reflect.deleteProperty(query, 'redirect')
      router.push({ path, query })
    } else {
      router.push('/')
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
      margin: 80px 0 10px;
      margin-bottom: 30px;
      
      .institute-info {
        text-align: center;

        .institute-logo {
          width: clamp(80px, 6.25vw, 140px);
          height: clamp(80px, 6.25vw, 140px);
          margin-bottom: 30px;
          filter: brightness(1.1);
        }

        .platform-title {
          font-size: clamp(36px, 2.5vw, 56px);
          font-weight: 600;
          background: linear-gradient(120deg, #ffffff, #b2dfdb);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
      }
    }

    .institute-name {
      position: absolute;
      bottom: 5px;
      left: 40px;
      font-size: 14.4px;
      color: #e0f2f1;
      font-weight: 500;
      max-width: 400px;
      line-height: 1.5;
      z-index: 2;
    }

    .feature-cards {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 30px;
      position: relative;
      z-index: 1;
      max-width: 1000px;
      margin: 130px auto 0;

      .feature-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 27px;
        transition: all 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;

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
        bottom: 30px;
        left: 30px;
        font-size: 16px;
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
