<template>
  <div class="login-container">
    <!-- 爱錯误提示弹窗 -->
    <div v-if="showErrorModal" class="modal-overlay">
      <div class="error-modal">
        <div class="error-icon">!</div>
        <h2 class="error-title">提示</h2>
        <p class="error-message">{{ errorMessage }}</p>
      </div>
    </div>

    <!-- 左侧登录表单区域 -->
    <div class="login-left">
      <div class="login-box">
        <!-- 标题和描述 -->
        <div class="welcome-section">
          <h2 class="welcome-title">教学助手系统登录</h2>
        </div>

        <!-- 登录表单 -->
        <form @submit.prevent="handleLogin" class="login-form">
          <!-- 用户身份选择 -->
          <div class="form-group">
            <label class="form-label">用户身份</label>
            <div class="identity-radio-group">
              <label class="radio-item">
                <input
                  type="radio"
                  v-model="loginForm.identity"
                  value="student"
                  name="identity"
                />
                <span class="radio-label">学生</span>
              </label>
              <label class="radio-item">
                <input
                  type="radio"
                  v-model="loginForm.identity"
                  value="teacher"
                  name="identity"
                />
                <span class="radio-label">教师</span>
              </label>
            </div>
          </div>

          <!-- 用户名 -->
          <div class="form-group">
            <label for="username" class="form-label">{{ loginForm.identity === 'student' ? '学号' : '教师工号' }}</label>
            <input
                id="username"
                v-model="loginForm.username"
                type="text"
                class="form-input"
                :placeholder="loginForm.identity === 'student' ? '请输入学号' : '请输入教师工号'"
                required
            />
          </div>

          <!-- 密码 -->
          <div class="form-group">
            <label for="password" class="form-label">密码</label>
            <div class="password-container">
              <input
                  id="password"
                  v-model="loginForm.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="请输入密码"
                  required
              />
              <button
                  type="button"
                  class="show-password-btn"
                  @click="showPassword = !showPassword"
              >
                {{ showPassword ? '隐藏' : '显示' }}
              </button>
            </div>
          </div>

          <!-- 登录按钮 -->
          <button type="submit" class="login-btn">登 录</button>
        </form>

        <!-- 辅助链接 -->
        <div class="helper-links">
          <router-link to="/forgot-password" class="helper-link">忘记密码?</router-link>
        </div>

        <!-- 注册入口 -->
        <div class="signup-section">
          <p class="signup-text">还没有账户?
            <router-link to="/register" class="signup-link">申请新账户</router-link>
          </p>
        </div>

        <!-- 帮助信息 -->
        <div class="help-section">
          <p class="help-text">需要帮助? 联系 <a href="#" class="help-link">技术支持</a></p>
        </div>
      </div>
    </div>

    <!-- 右侧教学功能展示区域 -->
    <div class="login-right">
      <div class="quick-access">
        <h3 class="quick-title">核心功能</h3>
        <div class="quick-items">
          <div class="quick-item">
            <div class="quick-icon">资料管理</div>
            <p class="quick-desc">管理课程文件和资料</p>
          </div>
          <div class="quick-item">
            <div class="quick-icon">考勤管理</div>
            <p class="quick-desc">学生签到和统计</p>
          </div>
          <div class="quick-item">
            <div class="quick-icon">成绩分析</div>
            <p class="quick-desc">成绩录入和分析</p>
          </div>
          <div class="quick-item">
            <div class="quick-icon">课堂互动</div>
            <p class="quick-desc">实时投票和提问</p>
          </div>
        </div>
      </div>

      <div class="app-section">
        <div class="app-benefits">
          <div class="benefit-item">
            <span class="benefit-icon"> </span>
            <span>实时掌握学生状态</span>
          </div>
          <div class="benefit-item">
            <span class="benefit-icon"> </span>
            <span>智能分析学情数据</span>
          </div>
          <div class="benefit-item">
            <span class="benefit-icon"> </span>
            <span>增强课堂互动体验</span>
          </div>
        </div>
      </div>

      <div class="app-section">
        <h3 class="app-title">下载应用</h3>
        <div class="app-buttons">
          <div class="app-button">
            <img src="../img/google_play_store_badge_en.svg" alt="安卓版下载">
            <span>安卓版</span>
          </div>
          <div class="app-button">
            <img src="../img/app_store_badge_en.svg" alt="IOS版下载">
            <span>iOS版</span>
          </div>
        </div>
      </div>

    </div>

    <!-- 页脚 -->

  </div>
</template>

<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'

const router = useRouter()
const showPassword = ref(false)
const showErrorModal = ref(false)
const errorMessage = ref('')
const loginForm = ref({
  identity: 'teacher',
  username: '',
  password: ''
})

const handleLogin = async () => {
  if (!loginForm.value.identity) {
    showError('请选择用户身份')
    return
  }
  if (!loginForm.value.username || !loginForm.value.password) {
    showError('请输入用户名和密码')
    return
  }
  
  try {
    const response = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        identity: loginForm.value.identity,
        username: loginForm.value.username,
        password: loginForm.value.password
      })
    })

    const data = await response.json()

    if (data.code === 200 && data.data) {
      // 存储登录状态到本地存储
      localStorage.setItem('userId', data.data.id.toString())
      localStorage.setItem('token', data.data.token)
      localStorage.setItem('user', JSON.stringify({
        id: data.data.id,
        identity: data.data.identity,
        username: data.data.username,
        token: data.data.token,
        subject: data.data.subject,
        fullname: data.data.fullname
      }))

      // 延迟跳转
      setTimeout(() => {
        // 根据用户身份跳转到不同页面
        if (data.data.identity === 'teacher') {
          router.push('/dashboard')
        } else {
          router.push('/')
        }
      }, 500)
    } else {
      showError(data.message || '登录失败')
    }
  } catch (error) {
    showError('网络错误，请检查服务器连接')
    console.error('Login error:', error)
  }
}

const showError = (message) => {
  errorMessage.value = message
  showErrorModal.value = true
  setTimeout(() => {
    showErrorModal.value = false
  }, 3000)
}
</script>

<style scoped>
.login-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-left {
  flex: 1.5;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-box {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(74, 144, 226, 0.15);
  padding: 4rem;
  width: 100%;
  max-width: 550px;
  animation: slideInLeft 0.5s ease-out;
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.logo-section {
  text-align: center;
  margin-bottom: 2rem;
}

.hospital-logo {
  font-size: 4rem;
  margin-bottom: 0.5rem;
}

.hospital-name {
  font-size: 1.5rem;
  color: #4A90E2;
  font-weight: bold;
  margin: 0;
}

.welcome-section {
  text-align: center;
  margin-bottom: 2rem;
}

.welcome-title {
  font-size: 1.8rem;
  color: #333;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.welcome-subtitle {
  color: #999;
  font-size: 0.95rem;
  margin: 0;
}

.login-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  color: #333;
  font-weight: 500;
  margin-bottom: 0.5rem;
}

.form-input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.identity-radio-group {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1rem;
}

.radio-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 0;
  cursor: pointer;
  font-size: 0.95rem;
  color: #333;
  user-select: none;
  flex: 1;
}

.radio-item input[type="radio"] {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  width: 100%;
  height: 100%;
}

.radio-item input[type="radio"] + .radio-label {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  padding: 0.7rem 1.5rem;
  font-weight: 600;
  border: 2px solid #ddd;
  border-radius: 8px;
  background: white;
  transition: all 0.3s ease;
  color: #666;
  cursor: pointer;
}

.radio-item input[type="radio"]:hover + .radio-label {
  border-color: #4A90E2;
  background: rgba(74, 144, 226, 0.05);
}

.radio-item input[type="radio"]:checked + .radio-label {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border-color: #4A90E2;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.radio-label {
  margin: 0;
}

.password-container {
  position: relative;
  display: flex;
  align-items: center;
}

.password-container .form-input {
  flex: 1;
}

.show-password-btn {
  position: absolute;
  right: 12px;
  background: none;
  border: none;
  color: #4A90E2;
  font-size: 0.85rem;
  cursor: pointer;
  font-weight: 600;
  transition: color 0.2s ease;
}

.show-password-btn:hover {
  color: #2E5FA3;
}

.login-btn {
  width: 100%;
  padding: 0.9rem;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(74, 144, 226, 0.3);
}

.login-btn:active {
  transform: translateY(0);
}

.helper-links {
  text-align: center;
  margin-bottom: 1.5rem;
}

.helper-link {
  color: #4A90E2;
  text-decoration: none;
  font-size: 0.9rem;
  transition: color 0.2s ease;
}

.helper-link:hover {
  color: #2E5FA3;
  text-decoration: underline;
}

.signup-section {
  text-align: center;
  padding: 1.5rem 0;
  border-top: 1px solid #f0f0f0;
}

.signup-text {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.signup-link {
  color: #4A90E2;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.signup-link:hover {
  color: #2E5FA3;
  text-decoration: underline;
}

.help-section {
  text-align: center;
  padding-top: 1rem;
}

.help-text {
  color: #999;
  font-size: 0.85rem;
  margin: 0;
}

.help-link {
  color: #4A90E2;
  text-decoration: none;
  transition: color 0.2s ease;
}

.help-link:hover {
  color: #2E5FA3;
  text-decoration: underline;
}

.login-right {
  flex: 0.5;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 1.5rem;
  color: white;
  animation: slideInRight 0.5s ease-out;
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.quick-access {
  margin-bottom: 3rem;
  text-align: center;
  width: 100%;
}

.quick-title {
  font-size: 1.5rem;
  margin: 0 0 1.5rem 0;
  font-weight: 600;
}

.quick-items {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.quick-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
  padding: 1.2rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(5px);
}

.quick-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-4px);
}

.quick-icon {
  font-size: 1.8rem;
  font-weight: 600;
}

.quick-desc {
  font-size: 0.85rem;
  margin: 0.5rem 0 0 0;
  opacity: 0.9;
}

.app-section {
  text-align: center;
  width: 100%;
}

.app-title {
  font-size: 1.5rem;
  margin: 0 0 1.5rem 0;
  font-weight: 600;
}

.app-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
}

.app-benefits {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  transition: all 0.2s ease;
  backdrop-filter: blur(5px);
}

.benefit-item:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateX(8px);
}

.benefit-icon {
  font-size: 1.2rem;
  font-weight: bold;
  flex-shrink: 0;
}

.benefit-item span:last-child {
  font-size: 0.95rem;
  font-weight: 500;
}

/* 错误弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(3px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.error-modal {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2.5rem 2rem;
  text-align: center;
  max-width: 320px;
  box-shadow: 0 20px 60px rgba(244, 67, 54, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  animation: slideUp 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.error-icon {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #F44336 0%, #D32F2F 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
  margin: 0 auto 1.2rem;
  animation: scaleIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 10px 30px rgba(244, 67, 54, 0.3);
  font-weight: bold;
}

@keyframes scaleIn {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}

.error-title {
  font-size: 1.5rem;
  color: #333;
  margin: 0 0 0.6rem 0;
  font-weight: 700;
}

.error-message {
  font-size: 1rem;
  color: #F44336;
  margin: 0;
  line-height: 1.5;
}

.login-footer {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  text-align: center;
  padding: 1.5rem;
  color: #999;
  font-size: 0.85rem;
  background: rgba(255, 255, 255, 0.5);
}

.login-footer p {
  margin: 0;
}

/* 响应式 */
@media (max-width: 1024px) {
  .login-container {
    flex-direction: column;
  }

  .login-left,
  .login-right {
    flex: 1;
  }

  .login-right {
    padding: 2rem;
  }

  .quick-items {
    grid-template-columns: repeat(4, 1fr);
  }

  .app-buttons {
    gap: 1rem;
  }
}

@media (max-width: 768px) {
  .login-box {
    padding: 2rem;
    max-width: 100%;
  }

  .login-right {
    padding: 1.5rem;
  }

  .quick-items {
    grid-template-columns: repeat(2, 1fr);
  }

  .app-buttons {
    flex-direction: column;
  }

  .login-footer {
    font-size: 0.75rem;
    padding: 1rem;
  }
}

.app-title {
  font-size: 1.3rem;
  margin: 30px 0 1.5rem 0;
  font-weight: 600;
}

.app-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
}

.app-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
  padding: 1.2rem 1.8rem;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(5px);
}

.app-button:hover {
  background: rgba(255, 255, 255, 0.2);
  transform: translateY(-4px);
}

.app-icon {
  font-size: 2.5rem;
}

.app-button span:last-child {
  font-size: 0.9rem;
  font-weight: 500;
}


@media (max-width: 480px) {
  .login-box {
    padding: 1.5rem;
  }

  .hospital-name {
    font-size: 1.2rem;
  }

  .welcome-title {
    font-size: 1.4rem;
  }

  .quick-items {
    gap: 1rem;
  }

  .quick-item {
    padding: 0.8rem;
  }
}
</style>