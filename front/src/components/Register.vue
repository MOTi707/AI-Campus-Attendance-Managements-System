<template>
  <div class="register-container">
    <!-- 左侧平台成效展示区域 -->
    <div class="login-right">
      <div class="quick-access">
        <h3 class="quick-title">为什么选择我们</h3>
        <div class="quick-items">
          <div class="quick-item">
            <p class="quick-desc">完整的资料管理系统</p>
          </div>
          <div class="quick-item">
            <p class="quick-desc">实时考勤管理</p>
          </div>
          <div class="quick-item">
            <p class="quick-desc">智能成绩分析工具</p>
          </div>
          <div class="quick-item">
            <p class="quick-desc">丰富的课堂互动功能</p>
          </div>
        </div>
      </div>

      <div class="app-section">
        <h3 class="app-title">平台优势</h3>
        <div class="app-benefits">
          <div class="benefit-item">
            <span class="benefit-num">01</span>
            <div>
              <p class="benefit-title"> 提高教学效率</p>
              <p class="benefit-desc">一体化资料管理，节省教师时间</p>
            </div>
          </div>

          <div class="benefit-item">
            <span class="benefit-num">02</span>
            <div>
              <p class="benefit-title">优化教学策略</p>
              <p class="benefit-desc">数据调查分析，改进教学方法</p>
            </div>
          </div>
        </div>

         <h3 class="app-title">&nbsp;</h3>
         <h3 class="app-title">&nbsp;</h3>

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

    <!-- 成功注册弹窗 -->
    <div v-if="showSuccessModal" class="modal-overlay">
      <div class="success-modal">
        <div class="success-icon">✓</div>
        <h2 class="success-title">注册成功</h2>
        <p class="success-message">恭喜您成功注册！</p>
        <p class="success-hint">即将为您跳转到登录页面...</p>
        <div class="loading-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>
    </div>

    <!-- 错误提示弹窗 -->
    <div v-if="showErrorModal" class="modal-overlay">
      <div class="error-modal">
        <div class="error-icon">!</div>
        <h2 class="error-title">提示</h2>
        <p class="error-message">{{ errorMessage }}</p>
      </div>
    </div>

    <!-- 右侧注册表单区域 -->
    <div class="register-right">
      <div class="register-box">
        <!-- 标题和描述 -->
        <div class="welcome-section">
          <h2 class="welcome-title">教师注册</h2>
          <p class="welcome-subtitle">加入教学智能助手平台</p>
        </div>

        <!-- 注册表单 -->
        <form @submit.prevent="handleRegister" class="register-form">
          <!-- 教师工号 -->
          <div class="form-group">
            <label for="username" class="form-label">教师工号</label>
            <input
                id="username"
                v-model="registerForm.username"
                type="text"
                class="form-input"
                placeholder="请输入教师工号"
                required
            />
          </div>

          <!-- 姓名 -->
          <div class="form-group">
            <label for="fullname" class="form-label">姓名</label>
            <input
                id="fullname"
                v-model="registerForm.fullname"
                type="text"
                class="form-input"
                placeholder="请输入您的姓名"
                required
            />
          </div>

          <!-- 授课科目（下拉选择） -->
          <div class="form-group">
            <label for="subject" class="form-label">授课科目</label>
            <select
                id="subject"
                v-model="registerForm.subject"
                class="form-input form-select"
                required
            >
              <option value="">请选择授课科目</option>
              <option value="语文">语文</option>
              <option value="数学">数学</option>
              <option value="英语">英语</option>
              <option value="物理">物理</option>
              <option value="化学">化学</option>
              <option value="生物">生物</option>
              <option value="政治">政治</option>
              <option value="历史">历史</option>
              <option value="地理">地理</option>
              <option value="信息技术">信息技术</option>
              <option value="体育">体育</option>
              <option value="音乐">音乐</option>
              <option value="美术">美术</option>
            </select>
          </div>

          <!-- 密码 -->
          <div class="form-group">
            <label for="password" class="form-label">密码</label>
            <div class="password-container">
              <input
                  id="password"
                  v-model="registerForm.password"
                  :type="showPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="请设置密码 (至少6位)"
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

          <!-- 确认密码 -->
          <div class="form-group">
            <label for="confirm-password" class="form-label">确认密码</label>
            <div class="password-container">
              <input
                  id="confirm-password"
                  v-model="registerForm.confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  class="form-input"
                  placeholder="请再次输入密码"
                  required
              />
              <button
                  type="button"
                  class="show-password-btn"
                  @click="showConfirmPassword = !showConfirmPassword"
              >
                {{ showConfirmPassword ? '隐藏' : '显示' }}
              </button>
            </div>
          </div>

          <!-- 服务条款勾选 -->
          <div class="form-group checkbox">
            <input
                id="terms"
                v-model="registerForm.agreeTerms"
                type="checkbox"
                required
            />
            <label for="terms" class="checkbox-label">
              我已阅读并同意 <a href="#" class="terms-link">服务条款</a> 和 <a href="#" class="terms-link">隐私政策</a>
            </label>
          </div>

          <!-- 注册按钮 -->
          <button type="submit" class="register-btn" :disabled="loading">{{ loading ? '注册中...' : '注 册' }}</button>
        </form>

        <!-- 登录入口 -->
        <div class="login-section">
          <p class="login-text">已有账户?
            <router-link to="/login" class="login-link">立即登录</router-link>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import {useRouter} from 'vue-router'
import {ElMessage} from 'element-plus'

const router = useRouter()
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)
const showSuccessModal = ref(false)
const showErrorModal = ref(false)
const errorMessage = ref('')

const registerForm = ref({
  username: '',
  fullname: '',
  subject: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

const handleRegister = async () => {
  // 验证字段
  if (!registerForm.value.username) {
    showError('请输入教师工号')
    return
  }
  if (!registerForm.value.fullname) {
    showError('请输入姓名')
    return
  }
  if (!registerForm.value.subject) {
    showError('请选择授课科目')
    return
  }
  if (registerForm.value.password.length < 6) {
    showError('密码至少需要6位')
    return
  }
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    showError('两次输入的密码不一致')
    return
  }
  if (!registerForm.value.agreeTerms) {
    showError('请同意服务条款和隐私政策')
    return
  }

  // 调用后端注册接口
  loading.value = true
  try {
    const response = await fetch('http://localhost:5000/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        identity: 'teacher',
        username: registerForm.value.username,
        fullname: registerForm.value.fullname,
        password: registerForm.value.password,
        subject: registerForm.value.subject
      })
    })

    const data = await response.json()

    if (data.code === 200 || data.code === 201) {
      showSuccessModal.value = true
      // 延迟跳转到登录页
      setTimeout(() => {
        router.push('/login')
      }, 2500)
    } else {
      showError(data.message || '注册失败')
    }
  } catch (error) {
    showError('网络错误，请检查服务器连接')
    console.error('Register error:', error)
  } finally {
    loading.value = false
  }
}

const showError = (message) => {
  errorMessage.value = message
  showErrorModal.value = true
  setTimeout(() => {
    showErrorModal.value = false
  }, 3000)
}

onMounted(() => {
  // 组件挂载时的初始化逻辑
})
</script>

<style scoped>
.register-container {
  display: flex;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.register-right {
  flex: 1.5;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  animation: slideInRight 0.5s ease-out;
}

.register-box {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(74, 144, 226, 0.15);
  padding: 3rem;
  width: 100%;
  max-width: 450px;
  max-height: 90vh;
  overflow-y: auto;
}

.register-box::-webkit-scrollbar {
  width: 6px;
}

.register-box::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.register-box::-webkit-scrollbar-thumb {
  background: #4A90E2;
  border-radius: 3px;
}

.register-box::-webkit-scrollbar-thumb:hover {
  background: #357ABD;
}

.welcome-section {
  text-align: center;
  margin-bottom: 1.5rem;
}

.welcome-title {
  font-size: 1.6rem;
  color: #333;
  margin: 0 0 0.3rem 0;
  font-weight: 600;
}

.welcome-subtitle {
  color: #999;
  font-size: 0.9rem;
  margin: 0;
}

.register-form {
  margin-bottom: 1.5rem;
}

.form-group {
  margin-bottom: 1rem;
}

.form-label {
  display: block;
  font-size: 0.85rem;
  color: #333;
  font-weight: 500;
  margin-bottom: 0.4rem;
}

.form-input {
  width: 100%;
  padding: 0.6rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-select {
  cursor: pointer;
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%234A90E2' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6 9 12 15 18 9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 0.6rem center;
  background-size: 1.3em 1.3em;
  padding-right: 2rem;
}

.form-input:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
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
  right: 10px;
  background: none;
  border: none;
  color: #4A90E2;
  font-size: 0.75rem;
  cursor: pointer;
  font-weight: 600;
  transition: color 0.2s ease;
}

.show-password-btn:hover {
  color: #2E5FA3;
}

.form-group.checkbox {
  margin-bottom: 1.5rem;
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
}

.form-group.checkbox input {
  margin-top: 0.3rem;
  cursor: pointer;
}

.checkbox-label {
  font-size: 0.85rem;
  color: #666;
  cursor: pointer;
}

.terms-link {
  color: #4A90E2;
  text-decoration: none;
  transition: color 0.2s ease;
}

.terms-link:hover {
  color: #2E5FA3;
  text-decoration: underline;
}

.register-btn {
  width: 100%;
  padding: 0.8rem;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.2s ease;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(74, 144, 226, 0.3);
}

.register-btn:active:not(:disabled) {
  transform: translateY(0);
}

.register-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.login-section {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
}

.login-text {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.login-link {
  color: #4A90E2;
  text-decoration: none;
  font-weight: 600;
  transition: color 0.2s ease;
}

.login-link:hover {
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
  padding: 3rem;
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
  font-size: 1.3rem;
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
  gap: 0.6rem;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  backdrop-filter: blur(5px);
}

.quick-item:hover {
  background: rgba(255, 255, 255, 0.25);
  transform: translateY(-4px);
}

.quick-desc {
  font-size: 0.8rem;
  text-align: center;
  line-height: 1.3;
  opacity: 0.95;
}

.app-section {
  text-align: center;
  width: 100%;
}

.app-title {
  font-size: 1.3rem;
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
  gap: 1rem;
}

.benefit-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
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

.benefit-num {
  font-size: 1.4rem;
  font-weight: bold;
  flex-shrink: 0;
  min-width: 2.5rem;
}

.benefit-title {
  font-size: 0.95rem;
  font-weight: 600;
  margin: 0;
}

.benefit-desc {
  font-size: 0.8rem;
  margin: 0.3rem 0 0 0;
  opacity: 0.9;
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

.app-button img {
  max-width: 150px;
  height: auto;
}

.app-button span:last-child {
  font-size: 0.9rem;
  font-weight: 500;
}

/* 成功弹窗样式 */
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

.success-modal {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 3rem 2.5rem;
  text-align: center;
  max-width: 380px;
  box-shadow: 0 20px 60px rgba(74, 144, 226, 0.2);
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

.success-icon {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  color: white;
  margin: 0 auto 1.5rem;
  animation: scaleIn 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  box-shadow: 0 10px 30px rgba(74, 144, 226, 0.3);
}

@keyframes scaleIn {
  from {
    transform: scale(0);
  }
  to {
    transform: scale(1);
  }
}

.success-title {
  font-size: 1.8rem;
  color: #333;
  margin: 0 0 0.8rem 0;
  font-weight: 700;
}

.success-message {
  font-size: 1.1rem;
  color: #4A90E2;
  margin: 0 0 0.5rem 0;
  font-weight: 500;
}

.success-hint {
  font-size: 0.95rem;
  color: #999;
  margin: 0 0 1.5rem 0;
  line-height: 1.5;
}

.loading-dots {
  display: flex;
  justify-content: center;
  gap: 0.5rem;
}

.loading-dots span {
  width: 10px;
  height: 10px;
  background: #4A90E2;
  border-radius: 50%;
  animation: bounce 1.4s infinite;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

.loading-dots span:nth-child(3) {
  animation-delay: 0s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* 错误弹窗样式 */
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
</style>
