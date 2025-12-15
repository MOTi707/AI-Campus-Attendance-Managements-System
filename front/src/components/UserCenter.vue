<template>
  <div class="user-center-container">
    <!-- 左侧导航 -->
    <div class="sidebar">
      <div class="user-info">
        <div class="avatar">
          <span class="avatar-text">{{ username.charAt(0).toUpperCase() || '教' }}</span>
        </div>
        <h3 class="username">{{ username || '教师用户' }}</h3>
        <p class="user-email">{{ fullname || '未設置' }}</p>
      </div>
      
      <nav class="nav-menu">
        <a 
          href="#" 
          class="nav-item" 
          :class="{ active: activeTab === 'dashboard' }"
          @click.prevent="activeTab = 'dashboard'"
        >
          <i class="nav-icon">●</i>
          教幦上传
        </a>
        <a 
          href="#" 
          class="nav-item" 
          :class="{ active: activeTab === 'materials' }"
          @click.prevent="activeTab = 'materials'"
        >
          <i class="nav-icon">●</i>
          资料管理
        </a>
        <a 
          href="#" 
          class="nav-item" 
          :class="{ active: activeTab === 'attendance' }"
          @click.prevent="activeTab = 'attendance'"
        >
          <i class="nav-icon">●</i>
          考勤管理
        </a>
        <a 
          href="#" 
          class="nav-item" 
          :class="{ active: activeTab === 'grades' }"
          @click.prevent="activeTab = 'grades'"
        >
          <i class="nav-icon">●</i>
          成绩分析
        </a>
        <a 
          href="#" 
          class="nav-item" 
          :class="{ active: activeTab === 'profile' }"
          @click.prevent="activeTab = 'profile'"
        >
          <i class="nav-icon">●</i>
          个人設置
        </a>
      </nav>
      
      <button class="logout-btn" @click="handleLogout">
        <i class="nav-icon">●</i>
        退出登录
      </button>
    </div>
    
    <!-- 右侧内容区域 -->
    <div class="main-content">
      <!-- 教学上传上传上传 -->
      <div v-if="activeTab === 'dashboard'" class="content-section">
        <h2 class="section-title">教学上传上传上传</h2>
        <div class="dashboard-grid">
          <div class="stats-card">
            <div class="stats-icon">教</div>
            <div class="stats-content">
              <div class="stats-label">幼子数</div>
              <div class="stats-value">1048</div>
            </div>
          </div>
          <div class="stats-card">
            <div class="stats-icon">课</div>
            <div class="stats-content">
              <div class="stats-label">课元数量</div>
              <div class="stats-value">56</div>
            </div>
          </div>
          <div class="stats-card">
            <div class="stats-icon">书</div>
            <div class="stats-content">
              <div class="stats-label">资料文档</div>
              <div class="stats-value">243</div>
            </div>
          </div>
          <div class="stats-card">
            <div class="stats-icon">表</div>
            <div class="stats-content">
              <div class="stats-label">考勤任务</div>
              <div class="stats-value">24</div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 资料管理 -->
      <div v-if="activeTab === 'materials'" class="content-section">
        <h2 class="section-title">资料管理</h2>
        <div class="materials-container">
          <div class="material-item">
            <div class="material-icon">文</div>
            <div class="material-info">
              <p class="material-name">正弦函数的思想.docx</p>
              <p class="material-date">2025-01-15</p>
            </div>
            <button class="material-action">下载</button>
          </div>
          <div class="material-item">
            <div class="material-icon">页</div>
            <div class="material-info">
              <p class="material-name">三角函数第一课时.pptx</p>
              <p class="material-date">2025-01-14</p>
            </div>
            <button class="material-action">下载</button>
          </div>
          <div class="material-item">
            <div class="material-icon">表</div>
            <div class="material-info">
              <p class="material-name">第三章作业詳詳.xlsx</p>
              <p class="material-date">2025-01-13</p>
            </div>
            <button class="material-action">下载</button>
          </div>
        </div>
      </div>
      
      <!-- 考勤管理 -->
      <div v-if="activeTab === 'attendance'" class="content-section">
        <h2 class="section-title">考勤管理</h2>
        <div class="attendance-container">
          <div class="attendance-stats">
            <div class="stat-box">
              <div class="stat-label">最近出出率</div>
              <div class="stat-value">92.5%</div>
              <div class="stat-bar">
                <div class="stat-fill" style="width: 92.5%"></div>
              </div>
            </div>
            <div class="stat-box">
              <div class="stat-label">本月出校率</div>
              <div class="stat-value">95.0%</div>
              <div class="stat-bar">
                <div class="stat-fill" style="width: 95%"></div>
              </div>
            </div>
          </div>
          <div class="attendance-records">
            <h4>最近签到记录</h4>
            <div v-for="record in attendanceRecords" :key="record.date" class="attendance-record">
              <span class="record-date">{{ record.date }}</span>
              <span :class="['record-status', record.status === 'on-time' ? 'on-time' : 'late']">
                {{ record.status === 'on-time' ? '上课' : '迟到' }}
              </span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 成绩分析 -->
      <div v-if="activeTab === 'grades'" class="content-section">
        <h2 class="section-title">成绩分析</h2>
        <div class="grades-container">
          <div class="grades-stats">
            <div class="grade-stat">
              <div class="grade-label">平均分数</div>
              <div class="grade-value">82</div>
            </div>
            <div class="grade-stat">
              <div class="grade-label">最高分</div>
              <div class="grade-value">95</div>
            </div>
            <div class="grade-stat">
              <div class="grade-label">最低分</div>
              <div class="grade-value">68</div>
            </div>
            <div class="grade-stat">
              <div class="grade-label">及格率</div>
              <div class="grade-value">88%</div>
            </div>
          </div>
          <div class="grades-list">
            <h4>最近考试成绩</h4>
            <div v-for="grade in gradesList" :key="grade.subject" class="grade-item">
              <span class="grade-subject">{{ grade.subject }}</span>
              <span class="grade-score">{{ grade.score }}分</span>
            </div>
          </div>
        </div>
      </div>
      
      <!-- 个人設置 -->
      <div v-if="activeTab === 'profile'" class="content-section">
        <h2 class="section-title">个人信息</h2>
        <div class="profile-form">
          <div class="form-group">
            <label class="form-label">教师工号</label>
            <div class="form-value">{{ username || '未設置' }}</div>
          </div>
          
          <div class="form-group">
            <label class="form-label">姓名</label>
            <div class="form-value">{{ fullname || '未設置' }}</div>
          </div>
          
          <!-- 授课科目 - 可编辑 -->
          <div class="form-group">
            <label class="form-label">授课科目</label>
            <select 
              v-if="isEditing" 
              v-model="editForm.subject" 
              class="form-input form-select"
            >
              <option value="">请选择科目</option>
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
            <div v-else class="form-value">{{ subject || '未設置' }}</div>
          </div>
          
          <div class="form-actions">
            <button 
              v-if="!isEditing" 
              class="btn btn-primary" 
              @click="startEdit"
            >
              编辑信息
            </button>
            <template v-else>
              <button class="btn btn-success" @click="saveProfile">保存</button>
              <button class="btn btn-secondary" @click="cancelEdit">取消</button>
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const activeTab = ref('dashboard')
const isEditing = ref(false)

// 用户信息
const username = ref('')
const fullname = ref('')
const subject = ref('')

// 编辑表单
const editForm = ref({
  subject: ''
})

// 考勤数据
const attendanceRecords = ref([
  { date: '2025-01-20', status: 'on-time' },
  { date: '2025-01-19', status: 'on-time' },
  { date: '2025-01-18', status: 'on-time' },
  { date: '2025-01-17', status: 'late' },
  { date: '2025-01-16', status: 'on-time' }
])

// 成绩数据
const gradesList = ref([
  { subject: '第一次月考', score: 85 },
  { subject: '第二次月考', score: 88 },
  { subject: '期中考试', score: 92 },
  { subject: '期末考试', score: 78 }
])

// 开始编辑
const startEdit = () => {
  isEditing.value = true
  editForm.value.subject = subject.value
}

// 取消编辑
const cancelEdit = () => {
  isEditing.value = false
  editForm.value.subject = subject.value
}

// 保存个人信息
const saveProfile = async () => {
  if (editForm.value.subject !== subject.value) {
    subject.value = editForm.value.subject
  }
  
  ElMessage.success('信息更新成功')
  isEditing.value = false
}

// 退出登录
const handleLogout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    localStorage.removeItem('user')
    ElMessage.success('退出登录成功')
    router.push('/login')
  }).catch(() => {
    // 取消退出
  })
}

// 检查登录状态
const checkLogin = () => {
  const user = localStorage.getItem('user')
  if (!user) {
    return true
  }
  
  try {
    const userData = JSON.parse(user)
    return userData.token
  } catch (e) {
    return null
  }
}

// 获取用户信息
const fetchUserProfile = async () => {
  username.value = localStorage.getItem('teacherUsername') || '张老师'
  fullname.value = '张明'
  subject.value = '数学'
  
  // 初始化编辑表单
  editForm.value.subject = subject.value
}

onMounted(() => {
  checkLogin()
  fetchUserProfile()
})
</script>

<style scoped>
.user-center-container {
  display: flex;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.sidebar {
  width: 280px;
  background: white;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
  padding: 2rem 0;
  display: flex;
  flex-direction: column;
}

.user-info {
  text-align: center;
  padding: 0 1.5rem 2rem;
  border-bottom: 1px solid #eee;
  margin-bottom: 1rem;
}

.avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.avatar-text {
  color: white;
  font-size: 2rem;
  font-weight: bold;
}

.username {
  font-size: 1.3rem;
  color: #333;
  margin: 0.5rem 0;
}

.user-email {
  color: #666;
  font-size: 0.9rem;
  margin: 0;
}

.nav-menu {
  flex: 1;
  padding: 0 1rem;
}

.nav-item {
  display: flex;
  align-items: center;
  padding: 1rem 1.5rem;
  text-decoration: none;
  color: #666;
  font-size: 1rem;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.nav-item:hover {
  background: #f5f7fa;
  color: #4A90E2;
}

.nav-item.active {
  background: #4A90E2;
  color: white;
}

.nav-icon {
  margin-right: 0.8rem;
  font-size: 1.2rem;
}

.logout-btn {
  background: none;
  border: none;
  padding: 1rem 1.5rem;
  text-align: left;
  color: #666;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 8px;
  margin: 0 1rem;
  display: flex;
  align-items: center;
}

.logout-btn:hover {
  background: #f5f7fa;
  color: #ff4d4f;
}

.main-content {
  flex: 1;
  padding: 2rem;
}

.section-title {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 2rem;
  font-weight: 600;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stats-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.stats-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.stats-icon {
  width: 60px;
  height: 60px;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.8rem;
  font-weight: 600;
  flex-shrink: 0;
}

.stats-content {
  flex: 1;
}

.stats-label {
  color: #999;
  font-size: 0.85rem;
  margin-bottom: 0.3rem;
}

.stats-value {
  color: #333;
  font-size: 1.5rem;
  font-weight: 600;
}

.materials-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.material-item {
  background: white;
  border-radius: 8px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.material-item:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transform: translateY(-2px);
}

.material-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  flex-shrink: 0;
}

.material-info {
  flex: 1;
}

.material-name {
  margin: 0;
  color: #333;
  font-weight: 500;
}

.material-date {
  margin: 0.3rem 0 0 0;
  color: #999;
  font-size: 0.85rem;
}

.material-action {
  padding: 0.5rem 1rem;
  background: #4A90E2;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.material-action:hover {
  background: #357ABD;
  transform: scale(1.05);
}

.attendance-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.attendance-stats {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.stat-box {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  color: #4A90E2;
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.stat-bar {
  width: 100%;
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.stat-fill {
  height: 100%;
  background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%);
  transition: width 0.3s ease;
}

.attendance-records {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.attendance-records h4 {
  margin: 0 0 1rem 0;
  color: #333;
}

.attendance-record {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.8rem;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.record-date {
  color: #666;
  font-size: 0.9rem;
}

.record-status {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.record-status.on-time {
  background: #e8f5e9;
  color: #2e7d32;
}

.record-status.late {
  background: #fff8e1;
  color: #f57f17;
}

.grades-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

.grades-stats {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.grade-stat {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 5px 20px rgba(74, 144, 226, 0.2);
}

.grade-label {
  font-size: 0.85rem;
  opacity: 0.9;
  margin-bottom: 0.5rem;
}

.grade-value {
  font-size: 2rem;
  font-weight: 600;
}

.grades-list {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.grades-list h4 {
  margin: 0 0 1rem 0;
  color: #333;
}

.grade-item {
  display: flex;
  justify-content: space-between;
  padding: 0.8rem;
  background: #f8f9fa;
  border-radius: 6px;
  margin-bottom: 0.5rem;
}

.grade-subject {
  color: #333;
  font-weight: 500;
}

.grade-score {
  color: #4A90E2;
  font-weight: 600;
}

.profile-form {
  max-width: 600px;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-value {
  padding: 0.8rem;
  background: #f8f9fa;
  border-radius: 6px;
  color: #333;
  font-size: 1rem;
}

.form-input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
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

.form-input:disabled {
  background: #f8f9fa;
  cursor: not-allowed;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: #4A90E2;
  color: white;
}

.btn-primary:hover {
  background: #357ABD;
  transform: translateY(-2px);
}

.btn-success {
  background: #52c41a;
  color: white;
}

.btn-success:hover {
  background: #389e0d;
  transform: translateY(-2px);
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background: #d9d9d9;
  transform: translateY(-2px);
}

.btn-danger {
  background: #ff4d4f;
  color: white;
}

.btn-danger:hover {
  background: #d9363e;
  transform: translateY(-2px);
}
</style>
