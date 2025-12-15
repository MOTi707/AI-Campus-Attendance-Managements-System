<template>
  <div class="dashboard-container">
    <!-- 头部 -->
    <div class="dashboard-header">
      <h1 class="dashboard-title">教师仪表盘</h1>
      <div class="header-actions">
        <span class="user-info"><span class="teacher-badge">老师</span> {{ currentUser.fullname }}</span>
        <button class="logout-btn" @click="handleLogout">登出</button>
      </div>
    </div>

    <!-- 主容器 -->
    <div class="dashboard-main">
      <!-- 左侧菜单 -->
      <div class="sidebar">
        <div class="menu-title">功能选择</div>
        <div class="menu-items">
          <!-- 核心功能 -->
          <div class="menu-section">
            <div class="section-title">核心功能</div>
            <div
              v-for="item in coreMenuItems"
              :key="item.id"
              :class="['menu-item', { active: activeMenu === item.id }]"
              @click="selectMenu(item.id)"
            >
              <span class="menu-icon">{{ item.icon }}</span>
              <span class="menu-label">{{ item.label }}</span>
            </div>
          </div>

          <!-- AI功能 -->
          <div class="menu-section">
            <div class="section-title">AI功能</div>
            <div
              v-for="item in aiMenuItems"
              :key="item.id"
              :class="['menu-item', { active: activeMenu === item.id }]"
              @click="selectMenu(item.id)"
            >
              <span class="menu-icon">{{ item.icon }}</span>
              <span class="menu-label">{{ item.label }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧内容区 -->
      <div class="content-area">
        <!-- 浮动光点背景特效 -->
        <div class="floating-blobs">
          <span></span>
          <i></i>
          <em></em>
          <strong></strong>
        </div>

        <!-- 课堂考勤 -->
        <div v-if="activeMenu === 'attendance'" class="content-panel">
          <AttendanceManagement />
        </div>

        <!-- 成绩管理 -->
        <div v-if="activeMenu === 'grades'" class="content-panel">
          <GradesManagement />
        </div>

        <!-- 课堂互动 -->
        <div v-if="activeMenu === 'interaction'" class="content-panel">
          <InteractionCenter />
        </div>

        <!-- 自动化资料归类 -->
        <div v-if="activeMenu === 'auto-classify'" class="content-panel">
          <MaterialsCenter />
        </div>

        <!-- 智能问答助手 -->
        <div v-if="activeMenu === 'qa-assistant'" class="content-panel">
          <QAAssistant />
        </div>

        <!-- 智能点到 -->
        <div v-if="activeMenu === 'smart-rollcall'" class="content-panel">
          <SmartAttendance />
        </div>

        <!-- 智能座位表 -->
        <div v-if="activeMenu === 'smart-seating'" class="content-panel">
          <Desk />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import MaterialsCenter from './MaterialsCenter.vue'
import GradesManagement from './GradesManagement.vue'
import AttendanceManagement from './AttendanceManagement.vue'
import InteractionCenter from './InteractionCenter.vue'
import SmartAttendance from './SmartAttendance.vue'
import Desk from './desk.vue'
import QAAssistant from './QAAssistant.vue'

const router = useRouter()
const activeMenu = ref('auto-classify')
const currentUser = ref({
  fullname: '加载中...'
})

const coreMenuItems = [
  { id: 'attendance', label: '课堂考勤', icon: '📋' },
  { id: 'grades', label: '成绩管理', icon: '📊' },
  { id: 'interaction', label: '课堂互动', icon: '💬' }
]

const aiMenuItems = [
  { id: 'auto-classify', label: '自动化资料归类', icon: '🤖' },
  { id: 'qa-assistant', label: '智能问答助手', icon: '🤔' },
  { id: 'smart-rollcall', label: '智能点到', icon: '✋' },
  { id: 'smart-seating', label: '智能座位表', icon: '🪑' }
]

const selectMenu = (menuId) => {
  activeMenu.value = menuId
}

const handleLogout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  localStorage.removeItem('userId')
  ElMessage.success('登出成功')
  router.push('/login')
}

onMounted(() => {
  const userStr = localStorage.getItem('user')
  if (userStr) {
    try {
      const user = JSON.parse(userStr)
      currentUser.value = user
    } catch (e) {
      currentUser.value.fullname = '用户'
    }
  }
})
</script>

<style scoped>
.dashboard-container {
  width: 100%;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  display: flex;
  flex-direction: column;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* 头部 */
.dashboard-header {
  background: white;
  border-bottom: 1px solid #e8eef5;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(74, 144, 226, 0.1);
}

.dashboard-title {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
  font-weight: 600;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.user-info {
  font-size: 0.95rem;
  color: #666;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.teacher-badge {
  background: linear-gradient(135deg, #faad14 0%, #f9a825 100%);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
}

.logout-btn {
  padding: 0.6rem 1.2rem;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

/* 主容器 */
.dashboard-main {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* 左侧菜单 */
.sidebar {
  width: 280px;
  background: white;
  border-right: 1px solid #e8eef5;
  display: flex;
  flex-direction: column;
  padding: 1.5rem 0;
  overflow-y: auto;
  box-shadow: 2px 0 8px rgba(74, 144, 226, 0.08);
}

.menu-title {
  padding: 0 1.5rem 1rem;
  font-size: 0.85rem;
  color: #999;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.menu-section {
  margin-bottom: 1.5rem;
}

.section-title {
  padding: 0.5rem 1.5rem;
  font-size: 0.8rem;
  color: #4A90E2;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.menu-items {
  display: flex;
  flex-direction: column;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  padding: 0.9rem 1.5rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #666;
  font-size: 0.95rem;
  font-weight: 500;
  border-left: 3px solid transparent;
}

.menu-item:hover {
  background: rgba(74, 144, 226, 0.05);
  color: #4A90E2;
}

.menu-item.active {
  background: linear-gradient(90deg, rgba(74, 144, 226, 0.1) 0%, transparent 100%);
  color: #4A90E2;
  border-left-color: #4A90E2;
  font-weight: 600;
}

.menu-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
}

.menu-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 右侧内容区 */
.content-area {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
  position: relative;
}

/* 浮动光点背景特效 */
.floating-blobs {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}

/* 4 个超梅幻漂浮光点 */
.floating-blobs span,
.floating-blobs i,
.floating-blobs em,
.floating-blobs strong {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.6;
  animation: float 18s infinite ease-in-out;
}

/* 光点1 - 天蓟 */
.floating-blobs span {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(80, 180, 255, 0.8) 0%, transparent 70%);
  top: 10%;
  right: 10%;
  animation-delay: 0s;
}

/* 光点2 - 紫罗兰 */
.floating-blobs i {
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(136, 84, 255, 0.7) 0%, transparent 70%);
  top: 40%;
  left: 5%;
  animation-delay: 3s;
}

/* 光点3 */
.floating-blobs em {
  width: 650px;
  height: 650px;
  background: radial-gradient(circle, rgba(99, 255, 163, 0.65) 0%, transparent 70%);
  bottom: 10%;
  right: 15%;
  animation-delay: 6s;
}

/* 光点4 - 深紫 */
.floating-blobs strong {
  width: 750px;
  height: 750px;
  background: radial-gradient(circle, rgba(102, 86, 234, 0.75) 0%, transparent 70%);
  bottom: 20%;
  left: 10%;
  animation-delay: 9s;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(25vw, -35vh) scale(1.15);
  }
  50% {
    transform: translate(-20vw, 25vh) scale(0.85);
  }
  75% {
    transform: translate(15vw, 30vh) scale(1.2);
  }
}

.content-panel {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 12px rgba(74, 144, 226, 0.1);
  backdrop-filter: blur(10px);
  min-height: 100%;
  animation: fadeIn 0.3s ease-in;
  position: relative;
  z-index: 10;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.panel-header {
  margin-bottom: 2rem;
  border-bottom: 1px solid #e8eef5;
  padding-bottom: 1rem;
}

.panel-header h2 {
  margin: 0;
  font-size: 1.6rem;
  color: #333;
  font-weight: 600;
}

.panel-desc {
  margin: 0.5rem 0 0 0;
  color: #999;
  font-size: 0.9rem;
}

.panel-content {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.empty-state {
  text-align: center;
  padding: 3rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  display: block;
}

.empty-state p {
  margin: 0.5rem 0;
  color: #666;
  font-size: 0.95rem;
}

.empty-hint {
  color: #999;
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

/* 滚动条美化 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: rgba(74, 144, 226, 0.3);
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: rgba(74, 144, 226, 0.5);
}

/* 响应式 */
@media (max-width: 1200px) {
  .sidebar {
    width: 220px;
  }

  .menu-label {
    font-size: 0.9rem;
  }
}

@media (max-width: 768px) {
  .dashboard-main {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
    border-right: none;
    border-bottom: 1px solid #e8eef5;
    padding: 1rem 0;
    max-height: 200px;
    overflow-x: auto;
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .menu-section {
    display: flex;
    gap: 0.5rem;
    margin: 0;
  }

  .section-title {
    display: none;
  }

  .content-area {
    padding: 1rem;
  }

  .content-panel {
    padding: 1rem;
  }

  .panel-content {
    min-height: 300px;
  }
}
</style>