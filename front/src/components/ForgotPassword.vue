<template>
  <div class="forgot-password-container">
    <div class="forgot-password-box">
      <router-link to="/login" class="back-link">&larr; 返回登录</router-link>
      


      <div class="welcome-section">
        <h2 class="welcome-title">重置密码</h2>
        <p class="welcome-subtitle">请输入您的邮箱地址</p>
      </div>

      <form @submit.prevent="handleSubmit" class="forgot-form">
        <div class="form-group">
          <label for="email" class="form-label">邮箱地址</label>
          <input
            id="email"
            v-model="email"
            type="email"
            class="form-input"
            placeholder="请输入注册邮箱"
            required
          />
        </div>

        <button type="submit" class="submit-btn">发送重置链接</button>
      </form>

      <div class="help-section">
        <p class="help-text">如需帮助，请联系 <a href="#" class="help-link">客服支持</a></p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const email = ref('')

const handleSubmit = async () => {
  if (!email.value) {
    ElMessage.error('请输入邮箱地址')
    return
  }
  
  try {
    const response = await fetch('/api/auth/forgot-password', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: email.value
      })
    })
    
    const data = await response.json()
    
    if (response.ok && data.code === 200) {
      ElMessage.success('重置链接已发送到您的邮箱，请检查收件箱')
      email.value = ''
    } else {
      ElMessage.error(data.message || '发送失败，请稍后重试')
    }
  } catch (error) {
    ElMessage.error('网络错误，请检查服务器连接')
    console.error('Forgot password error:', error)
  }
}
</script>

<style scoped>
.forgot-password-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  padding: 2rem;
}

.forgot-password-box {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(74, 144, 226, 0.15);
  padding: 3rem;
  width: 100%;
  max-width: 420px;
  position: relative;
  animation: slideInUp 0.5s ease-out;
}

@keyframes slideInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.back-link {
  position: absolute;
  top: 1.5rem;
  left: 1.5rem;
  color: #4A90E2;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.2s ease;
}

.back-link:hover {
  color: #2E5FA3;
}

.logo-section {
  text-align: center;
  margin: 3rem 0 2rem 0;
}

.hospital-logo {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.hospital-name {
  font-size: 1.3rem;
  color: #4A90E2;
  font-weight: bold;
  margin: 0;
}

.welcome-section {
  text-align: center;
  margin-bottom: 2rem;
}

.welcome-title {
  font-size: 1.6rem;
  color: #333;
  margin: 0 0 0.5rem 0;
  font-weight: 600;
}

.welcome-subtitle {
  color: #999;
  font-size: 0.95rem;
  margin: 0;
}

.forgot-form {
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

.submit-btn {
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

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(74, 144, 226, 0.3);
}

.submit-btn:active {
  transform: translateY(0);
}

.help-section {
  text-align: center;
  padding-top: 1rem;
  border-top: 1px solid #f0f0f0;
}

.help-text {
  color: #999;
  font-size: 0.9rem;
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

@media (max-width: 480px) {
  .forgot-password-box {
    padding: 2rem;
  }

  .hospital-name {
    font-size: 1.1rem;
  }

  .welcome-title {
    font-size: 1.3rem;
  }
}
</style>
