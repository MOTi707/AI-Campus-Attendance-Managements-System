<template>
  <div class="home-page">
    <!-- 导航头部 -->
    <header class="navbar">
      <div class="navbar-container">
        <router-link to="/" class="logo-link">
          <div class="logo-section">
            <div class="logo-icon">教</div>
            <span class="logo-text">教学智能助手</span>
          </div>
        </router-link>

        <nav class="nav-links">
          <a href="#hero" class="nav-link">首页</a>
          <a href="#grades" class="nav-link">功能演示</a>
          <a href="#about" class="nav-link">关于我们</a>
        </nav>

        <div class="action-buttons">
          <router-link to="/login" class="btn-nav-link">
            <button class="btn-login">登录</button>
          </router-link>
          <router-link to="/register" class="btn-nav-link">
            <button class="btn-register">注册</button>
          </router-link>
        </div>
      </div>
    </header>

    <!-- 右侧浮动导航栏 -->
    <nav class="floating-nav">
      <div class="nav-container">
        <div
            v-for="(item, index) in navItems"
            :key="item.id"
            class="nav-item-wrapper"
        >
          <button
              :class="['nav-item', { active: activeSection === item.id }]"
              @click="scrollToSection(item.id)"
              :title="item.label"
          >
            <span class="nav-dot">{{ item.icon }}</span>
            <span class="nav-label">{{ item.label }}</span>
          </button>

          <div v-if="index < navItems.length - 1" class="nav-divider"></div>
        </div>
      </div>
    </nav>


    <section id="hero" class="banner-hero-section">

      <div class="banner-hero-content">
        <h1 class="banner-hero-title">教学智能助手</h1>
        <p class="banner-hero-subtitle">
          赋能教师，智慧教学。一站式解决资料管理、考勤跟踪和成绩分析
        </p>

        <div class="banner-hero-features">
          <div class="banner-feature-item">
            <span>资料管理</span>
          </div>
          <div class="banner-feature-item">
            <span>考勤管理</span>
          </div>
          <div class="banner-feature-item">
            <span>成绩分析</span>
          </div>
        </div>

        <div class="banner-hero-buttons">
          <router-link to="/login" class="banner-btn-link">
            <button class="btn-primary">开始使用</button>
          </router-link>
          <button class="btn-secondary" @click="scrollToSection('grades')">效果演示</button>
        </div>
      </div>

      <div class="hero-right">
      <img
        src="../assets/ai-initiative-page-header_v1r3-1200x775.jpg"
        alt="AI Initiative"
        class="hero-image"
      />
    </div>


      <div class="floating-blobs"></div>
    </section>


    <!-- 成绩分析演示 (第一个) -->
    <section id="grades" class="demo-section">
      <div class="section-header">
        <h2 class="section-title">数据智能分析</h2>
        <p class="section-subtitle">自动统计学生成绩，生成详细分析报表，支持趋势预测，助力教学决策</p>
      </div>
      <div class="demo-container">
        <div class="demo-grid">
          <div class="demo-info">
            <div class="stat-box">
              <div class="stat-item">
                <div class="stat-number">{{ mockData.grades.averageScore }}</div>
                <div class="stat-label">平均分</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ mockData.grades.passRate }}</div>
                <div class="stat-label">及格率</div>
              </div>
            </div>

            <div class="score-range">
              <div class="list-title">成绩分布</div>
              <div
                  v-for="dist in mockData.grades.distribution"
                  :key="dist.range"
                  class="distribution-item"
              >
                <span class="range-label">{{ dist.range }}</span>
                <div class="range-bar">
                  <div class="bar-fill" :style="{ width: (dist.count / 20) * 100 + '%' }"></div>
                </div>
                <span class="range-count">{{ dist.count }}人</span>
              </div>
            </div>
          </div>

          <div class="demo-visual grades-visual">
            <div class="chart-container">
              <div class="chart-title">成绩趋势图</div>
              <svg class="trend-chart" viewBox="0 0 300 150">
                <polyline points="10,120 50,90 90,75 130,85 170,60 210,70 250,40"
                          stroke="#87CEEB" stroke-width="3" fill="none" vector-effect="non-scaling-stroke"/>
                <circle cx="10" cy="120" r="4" fill="#4A90E2"/>
                <circle cx="50" cy="90" r="4" fill="#4A90E2"/>
                <circle cx="90" cy="75" r="4" fill="#4A90E2"/>
                <circle cx="130" cy="85" r="4" fill="#4A90E2"/>
                <circle cx="170" cy="60" r="4" fill="#4A90E2"/>
                <circle cx="210" cy="70" r="4" fill="#4A90E2"/>
                <circle cx="250" cy="40" r="4" fill="#4A90E2"/>
                <line x1="0" y1="140" x2="300" y2="140" stroke="#ddd" stroke-width="1"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 资料管理演示 (第二个) -->
    <section id="materials" class="demo-section">
      <div class="section-header">
        <h2 class="section-title">智能资料管理</h2>
        <p class="section-subtitle">轻松管理课程资料，支持多种文件格式，自动分类归档，快速检索查找</p>
      </div>
      <div class="demo-container">
        <div class="demo-grid">
          <div class="demo-info">
            <div class="stat-box">
              <div class="stat-item">
                <div class="stat-number">{{ mockData.materials.totalFiles }}</div>
                <div class="stat-label">课程文件</div>
              </div>
            </div>

            <div class="category-list">
              <div class="category-title">文件分类</div>
              <div class="categories">
                <span
                    v-for="cat in mockData.materials.categories"
                    :key="cat"
                    class="category-tag"
                >
                  {{ cat }}
                </span>
              </div>
            </div>

            <div class="recent-files">
              <div class="list-title">最近文件</div>
              <div
                  v-for="file in mockData.materials.recentFiles"
                  :key="file.name"
                  class="file-item"
              >
                <span class="file-name">{{ file.name }}</span>
                <span class="file-meta">{{ file.size }} · {{ file.date }}</span>
              </div>
            </div>
          </div>

          <div class="demo-visual materials-visual">
            <div class="visual-card">
              <div class="card-header">文件库</div>
              <div class="file-icons">
                <div class="file-icon">文</div>
                <div class="file-icon">表</div>
                <div class="file-icon">页</div>
                <div class="file-icon">夹</div>
                <div class="file-icon">盒</div>
              </div>
              <div class="upload-area">
                <div class="upload-text">拖拽文件到此处上传</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 考勤管理演示 (第三个) -->
    <section id="attendance" class="demo-section">
      <div class="section-header">
        <h2 class="section-title">实时考勤管理</h2>
        <p class="section-subtitle">一键发起考勤任务，学生扫码快速签到，实时生成考勤报表，数据精准可靠</p>
      </div>
      <div class="demo-container">
        <div class="demo-grid">
          <div class="demo-info">
            <div class="stat-box">
              <div class="stat-item">
                <div class="stat-number">{{ mockData.attendance.attendanceRate }}</div>
                <div class="stat-label">出勤率</div>
              </div>
              <div class="stat-item">
                <div class="stat-number">{{ mockData.attendance.presentToday }}/{{
                    mockData.attendance.totalStudents
                  }}
                </div>
                <div class="stat-label">今日到课</div>
              </div>
            </div>

            <div class="recent-records">
              <div class="list-title">最近签到</div>
              <div
                  v-for="record in mockData.attendance.recentRecords"
                  :key="record.name"
                  class="record-item"
              >
                <span class="record-name">{{ record.name }}</span>
                <span class="record-time">{{ record.time }}</span>
                <span :class="['record-status', record.status === '准时' ? 'on-time' : 'late']">
                  {{ record.status }}
                </span>
              </div>
            </div>
          </div>

          <div class="demo-visual attendance-visual">
            <div class="attendance-display">
              <div class="qr-code-box">
                <div class="qr-code-title">扫码签到</div>
                <div class="qr-code-placeholder">
                  <div class="qr-pattern"></div>
                </div>
                <div class="qr-code-hint">学生使用手机扫描</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 关于我们部分 -->
    <section id="about" class="about-section">
      <div class="section-header">
        <h2 class="section-title">关于我们</h2>
        <p class="section-subtitle">打造教育智能化解决方案，赋能全球教师</p>
      </div>
      <div class="about-container">
        <div class="about-card">
          <div class="about-icon">🎯</div>
          <h3>我们的使命</h3>
          <p>通过智能化技术，帮助教师简化教学流程，提升教学效率，让教师有更多精力投入到教学创新中。</p>
        </div>
        <div class="about-card">
          <div class="about-icon">💡</div>
          <h3>我们的愿景</h3>
          <p>成为全球领先的教育智能助手平台，为数百万教师提供高效、可靠、易用的教学管理工具。</p>
        </div>
        <div class="about-card">
          <div class="about-icon">🌟</div>
          <h3>我们的价值观</h3>
          <p>以用户为中心，不断创新，追求卓越。致力于为教师打造最具价值的教学伙伴。</p>
        </div>
      </div>
    </section>

    <!-- 页脚 -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-container">
          <div class="footer-section">
            <div class="footer-logo">
              <div class="logo-icon">智</div>
              <div>
                <div class="logo-name">教学智能助手</div>
                <p class="logo-tagline">赋能教师，智慧教学</p>
              </div>
            </div>
            <p class="footer-description">
              一站式教学管理解决方案，提供资料管理、考勤统计、成绩分析等核心功能，
              帮助教师高效工作，提升教学效率。
            </p>
          </div>

          <div
              v-for="(links, category) in footerLinks"
              :key="category"
              class="footer-section"
          >
            <h4 class="footer-section-title">{{ category }}</h4>
            <ul class="footer-links">
              <li v-for="link in links" :key="link">
                <a href="#" class="footer-link">{{ link }}</a>
              </li>
            </ul>
          </div>
        </div>

        <div class="footer-bottom">
          <div class="footer-copyright">
            <p>Copyright {{ currentYear }} 教学智能助手. All rights reserved.</p>
          </div>

          <div class="footer-social">
            <a href="#" class="social-link">GitHub</a>
            <a href="#" class="social-link">微博</a>
            <a href="#" class="social-link">微信</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>





<script setup>
import {ref, onMounted, onUnmounted} from 'vue'

const activeSection = ref('hero')

// 导航栏数据
const navItems = [
  {id: 'hero', label: '顶部', icon: '●'},
  {id: 'grades', label: '成绩', icon: '●'},
  {id: 'materials', label: '资料', icon: '●'},
  {id: 'attendance', label: '考勤', icon: '●'}
]

// 演示数据
const mockData = {
  materials: {
    totalFiles: 248,
    categories: ['教案', '课件', '作业', '考卷', '资料'],
    recentFiles: [
      {name: '第1章-教学设计.ppt', size: '2.4MB', date: '2024-01-15'},
      {name: '第2章-讲义.pdf', size: '1.8MB', date: '2024-01-14'},
      {name: '第3章-习题.docx', size: '0.9MB', date: '2024-01-13'}
    ]
  },
  attendance: {
    totalStudents: 45,
    presentToday: 42,
    attendanceRate: '93.3%',
    recentRecords: [
      {name: '张三', time: '09:00', status: '准时'},
      {name: '李四', time: '09:05', status: '迟到'},
      {name: '王五', time: '09:00', status: '准时'}
    ]
  },
  grades: {
    averageScore: 82.5,
    highestScore: 98,
    lowestScore: 55,
    passRate: '88.9%',
    distribution: [
      {range: '90-100', count: 12},
      {range: '80-89', count: 18},
      {range: '70-79', count: 10},
      {range: '60-69', count: 4},
      {range: '0-59', count: 1}
    ]
  }
}

// 页脚数据
const currentYear = new Date().getFullYear()
const footerLinks = {
  产品: ['功能介绍', '定价方案', '更新日志'],
  支持: ['帮助文档', '联系我们', '反馈建议'],
  关于: ['公司简介', '加入我们', '媒体报道']
}

// 导航功能
const scrollToSection = (sectionId) => {
  activeSection.value = sectionId
  const element = document.getElementById(sectionId)
  if (element) {
    element.scrollIntoView({behavior: 'smooth'})
  }
}

const handleScroll = () => {
  const sections = navItems.map(item => ({
    id: item.id,
    element: document.getElementById(item.id)
  })).filter(item => item.element)

  let closestSection = 'hero'
  let closestDistance = Infinity

  sections.forEach(section => {
    const rect = section.element.getBoundingClientRect()
    const distance = Math.abs(rect.top - 100)
    if (distance < closestDistance) {
      closestDistance = distance
      closestSection = section.id
    }
  })

  activeSection.value = closestSection
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>







<style scoped>
/* 全局样式 */
.home-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f0f4f8 0%, #e8f0f8 100%);
}

/* 导航栏 */
.navbar {
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(173, 216, 230, 0.3);
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.05);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-link {
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.logo-link:hover .logo-icon {
  transform: scale(1.1) rotate(5deg);
}

.logo-link:hover .logo-text {
  transform: scale(1.05);
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.logo-icon {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #87CEEB 0%, #ADD8E6 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  color: white;
}

.logo-text {
  font-size: 1.3rem;
  font-weight: 600;
  color: #333;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: #555;
  text-decoration: none;
  font-size: 1rem;
  font-weight: 500;
  transition: color 0.3s ease;
  position: relative;
}

.nav-link:hover {
  color: #87CEEB;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, #87CEEB, #4A90E2);
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 100%;
}

.action-buttons {
  display: flex;
  gap: 1rem;
}

.btn-nav-link {
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-login,
.btn-register {
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-login {
  background: transparent;
  color: #87CEEB;
  border: 2px solid #87CEEB;
}

.btn-login:hover {
  background: #87CEEB;
  color: white;
  box-shadow: 0 4px 15px rgba(135, 206, 235, 0.3);
}

.btn-register {
  background: linear-gradient(135deg, #87CEEB 0%, #4A90E2 100%);
  color: white;
  box-shadow: 0 4px 15px rgba(135, 206, 235, 0.3);
}

.btn-register:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(135, 206, 235, 0.4);
}

/* 右侧浮动导航栏 */
.floating-nav {
  position: fixed;
  right: 1.5rem;
  top: 50%;
  transform: translateY(-50%);
  z-index: 50;
  background: rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
  border-left: 2px solid rgba(135, 206, 235, 0.3);
  border-radius: 20px 0 0 20px;
  padding: 1.5rem 0.8rem;
  pointer-events: auto;
}

.nav-container {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.nav-item-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.3rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.6rem 0.5rem;
  border-radius: 10px;
  transition: all 0.3s ease;
  text-align: center;
  color: #666;
  font-weight: 600;
  font-size: 1.2rem;
}

.nav-item:hover {
  background: rgba(135, 206, 235, 0.15);
  color: #4A90E2;
}


.nav-dot {
  font-size: 1.2rem;
  display: block;
  color: #87CEEB;
  transition: all 0.3s ease;
}

.nav-item.active .nav-dot {
  color: #4A90E2;
  transform: scale(1.2);
}

.nav-label {
  font-size: 1rem;
  white-space: nowrap;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.nav-divider {
  width: 2px;
  height: 20px;
  background: linear-gradient(180deg, rgba(135, 206, 235, 0), rgba(135, 206, 235, 0.5) 50%, rgba(135, 206, 235, 0));
  margin: 0.3rem 0;
  align-self: center;
  border-radius: 1px;
}

/* 导航栏样式 */
/* 轮播区域（事件需要符合系统） */
.banner-hero-section {
  width: 100%;
  height: 100vh;
  max-width: none;
  margin: 0;
  padding: 8rem 4rem 8rem 4rem;
  display: grid;
  grid-template-columns: 2fr 2fr;
  gap: 0rem;

  justify-items: center;
  position: relative;


}

.banner-hero-content {
  z-index: 2;
  max-width: 550px;
  animation: slideInLeft 0.8s ease-out;

}

.banner-hero-title {
  font-size: 4.5rem;
  font-weight: 900;
  margin-bottom: 1.5rem;
  line-height: 1.1;
  background: linear-gradient(135deg, #4A90E2 0%, #87CEEB 30%, #2E5C8A 70%, #4A90E2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 10px rgba(135, 206, 235, 0.3);
  letter-spacing: -1px;
}

.banner-hero-subtitle {
  font-size: 1.5rem;
  color: #555;
  margin-bottom: 3rem;
  line-height: 1.8;
  font-weight: 500;
}

.banner-hero-features {
  display: flex;
  gap: 3rem;
  margin-bottom: 3rem;
  flex-wrap: wrap;
}

.banner-feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: #4A90E2;
  padding: 1rem 1.5rem;
  background: rgba(135, 206, 235, 0.1);
  border-radius: 20px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.banner-feature-item:hover {
  background: rgba(135, 206, 235, 0.2);
  transform: translateX(8px);
}

.banner-hero-buttons {
  display: flex;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.banner-btn-link {
  text-decoration: none;
  transition: all 0.3s ease;
}

.btn-primary,
.btn-secondary {
  padding: 1.2rem 3rem;
  border: none;
  border-radius: 35px;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  letter-spacing: 0.5px;
}

.btn-primary {
  background: linear-gradient(135deg, #87CEEB 0%, #4A90E2 50%, #2E5C8A 100%);
  color: white;
  box-shadow: 0 8px 25px rgba(74, 144, 226, 0.4), 0 0 30px rgba(135, 206, 235, 0.2);
  border: none;
}

.btn-primary:hover {
  transform: translateY(-4px) scale(1.05);
  box-shadow: 0 15px 40px rgba(74, 144, 226, 0.6), 0 0 40px rgba(135, 206, 235, 0.3);
}

.btn-primary:active {
  transform: translateY(-2px) scale(1.02);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.85);
  color: #4A90E2;
  border: 3px solid #87CEEB;
  box-shadow: 0 4px 15px rgba(135, 206, 235, 0.2);
}

.btn-secondary:hover {
  background: white;
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(135, 206, 235, 0.3);
  border-color: #4A90E2;
}
@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(30px, -20px) scale(1.1);
  }
  50% {
    transform: translate(20px, 20px) scale(1.15);
  }
  75% {
    transform: translate(-20px, 10px) scale(1.05);
  }
}

@keyframes slideInLeft {
  from {
    opacity: 0;
    transform: translateX(-50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideInRight {
  from {
    opacity: 0;
    transform: translateX(50px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 演示区域 */
.demo-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 5rem 2rem 4rem 2rem;
  scroll-margin-top: 80px;
}

.section-header {
  text-align: center;
  margin-bottom: 3rem;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #333;
  margin-bottom: 1rem;
  background: linear-gradient(135deg, #4A90E2 0%, #87CEEB 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-subtitle {
  font-size: 1.1rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
}

.demo-container {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 2px solid rgba(173, 216, 230, 0.3);
  overflow: hidden;
  padding: 2rem;
}

.demo-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  align-items: center;
}

.stat-box {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.stat-item {
  background: rgba(135, 206, 235, 0.1);
  padding: 1rem;
  border-radius: 15px;
  flex: 1;
  min-width: 120px;
}

.stat-number {
  font-size: 1.8rem;
  font-weight: 800;
  color: #4A90E2;
}

.stat-label {
  font-size: 0.9rem;
  color: #666;
  margin-top: 0.3rem;
}

.category-list,
.recent-files,
.recent-records,
.score-range {
  margin-bottom: 1.5rem;
}

.category-title,
.list-title {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.8rem;
}

.categories {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.category-tag {
  background: rgba(135, 206, 235, 0.15);
  color: #4A90E2;
  padding: 0.4rem 0.9rem;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 500;
}

.file-item,
.record-item,
.distribution-item {
  padding: 0.8rem;
  background: rgba(240, 244, 248, 0.8);
  border-radius: 10px;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.file-name,
.record-name,
.range-label {
  font-weight: 600;
  color: #333;
}

.file-meta,
.record-time {
  font-size: 0.85rem;
  color: #999;
}

.record-status {
  padding: 0.3rem 0.8rem;
  border-radius: 10px;
  font-size: 0.85rem;
  font-weight: 600;
}

.range-bar {
  flex: 1;
  height: 6px;
  background: rgba(173, 216, 230, 0.3);
  border-radius: 3px;
  margin: 0 0.8rem;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #87CEEB, #4A90E2);
  border-radius: 3px;
}

.range-count {
  font-size: 0.85rem;
  color: #666;
  min-width: 40px;
  text-align: right;
}

.demo-visual {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background: linear-gradient(135deg, rgba(135, 206, 235, 0.1) 0%, rgba(173, 216, 230, 0.1) 100%);
  border-radius: 15px;
}

.visual-card {
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(173, 216, 230, 0.3);
  border-radius: 15px;
  padding: 2rem;
  width: 100%;
}

.card-header {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1rem;
  padding-bottom: 0.8rem;
  border-bottom: 2px solid rgba(135, 206, 235, 0.3);
}

.file-icons {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}

.file-icon {
  font-size: 2rem;
  text-align: center;
  padding: 0.8rem;
  background: rgba(135, 206, 235, 0.1);
  border-radius: 10px;
  font-weight: bold;
  color: #4A90E2;
}

.upload-area {
  background: rgba(135, 206, 235, 0.05);
  border: 2px dashed #87CEEB;
  border-radius: 10px;
  padding: 2rem;
  text-align: center;
}

.upload-text {
  color: #87CEEB;
  font-weight: 600;
}

.attendance-display {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.qr-code-box {
  text-align: center;
}

.qr-code-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1rem;
}

.qr-code-placeholder {
  width: 150px;
  height: 150px;
  background: white;
  border: 2px solid rgba(173, 216, 230, 0.5);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.qr-pattern {
  width: 120px;
  height: 120px;
  background: linear-gradient(45deg, #4A90E2 25%, transparent 25%, transparent 75%, #4A90E2 75%, #4A90E2),
  linear-gradient(45deg, #4A90E2 25%, transparent 25%, transparent 75%, #4A90E2 75%, #4A90E2);
  background-size: 20px 20px;
  background-position: 0 0, 10px 10px;
  background-color: white;
}

.qr-code-hint {
  font-size: 0.9rem;
  color: #999;
}

.chart-container {
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
}

.chart-title {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1rem;
}

.trend-chart {
  width: 100%;
  height: auto;
}

/* 页脚 */
.footer {
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.05) 0%, rgba(135, 206, 235, 0.05) 100%);
  border-top: 1px solid rgba(173, 216, 230, 0.3);
  margin-top: 3rem;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
}

.footer-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
  padding-bottom: 3rem;
  border-bottom: 1px solid rgba(173, 216, 230, 0.2);
}

.footer-section {
  display: flex;
  flex-direction: column;
}

.footer-logo {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.footer-logo .logo-icon {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #87CEEB 0%, #4A90E2 100%);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.8rem;
  font-weight: bold;
  color: white;
  flex-shrink: 0;
}

.logo-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
}

.logo-tagline {
  font-size: 0.85rem;
  color: #999;
  margin: 0.3rem 0 0 0;
}

.footer-description {
  font-size: 0.95rem;
  color: #666;
  line-height: 1.6;
}

.footer-section-title {
  font-size: 1rem;
  font-weight: 700;
  color: #333;
  margin-bottom: 1rem;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 0.8rem;
}

.footer-link {
  color: #666;
  text-decoration: none;
  font-size: 0.95rem;
  transition: color 0.3s ease;
  position: relative;
}

.footer-link:hover {
  color: #4A90E2;
}

.footer-link::before {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 0;
  height: 2px;
  background: #4A90E2;
  transition: width 0.3s ease;
}

.footer-link:hover::before {
  width: 100%;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 2rem;
}

.footer-copyright p {
  color: #999;
  font-size: 0.9rem;
  margin: 0;
}

.footer-social {
  display: flex;
  gap: 1.5rem;
}

.social-link {
  color: #666;
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  transition: color 0.3s ease;
}

.social-link:hover {
  color: #4A90E2;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .floating-nav {
    right: 1rem;
  }

  .nav-item {
    font-size: 0.9rem;
  }

  .nav-label {
    font-size: 0.85rem;
  }
}

@media (max-width: 1024px) {
  .banner-hero-section {
    grid-template-columns: 1fr;
    padding: 4rem 2rem;
    gap: 3rem;
  }

  .banner-hero-title {
    font-size: 3.5rem;
  }

  .banner-hero-subtitle {
    font-size: 1.3rem;
  }

  .demo-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }

  .demo-visual {
    min-height: 250px;
  }
}

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    gap: 1rem;
  }

  .nav-links {
    order: 3;
    width: 100%;
    gap: 1rem;
    flex-direction: column;
  }

  .action-buttons {
    width: 100%;
    flex-direction: column;
  }

  .btn-login,
  .btn-register {
    width: 100%;
  }

  .floating-nav {
    display: none;
  }

  .banner-hero-section {
    padding: 2rem 1rem;
    gap: 2rem;
  }

  .banner-hero-title {
    font-size: 2rem;
  }

  .banner-hero-subtitle {
    font-size: 1rem;
  }

  .banner-hero-features {
    gap: 1rem;
  }

  .banner-hero-buttons {
    flex-direction: column;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
  }

  .demo-section {
    padding: 3rem 1.5rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .demo-container {
    padding: 1.5rem;
  }

  .stat-box {
    flex-direction: column;
  }

  .stat-item {
    min-width: 100%;
  }

  .file-icons {
    grid-template-columns: repeat(3, 1fr);
  }

  .footer-content {
    padding: 2rem 1.5rem;
  }

  .footer-container {
    gap: 1.5rem;
    margin-bottom: 2rem;
    padding-bottom: 2rem;
  }

  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }

  .footer-social {
    justify-content: center;
  }
}

/* 关于我们部分 */
.about-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: 5rem 2rem 4rem 2rem;
  scroll-margin-top: 80px;
}

.about-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 3rem;
}

.about-card {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 2rem;
  text-align: center;
  border: 2px solid rgba(173, 216, 230, 0.3);
  transition: all 0.3s ease;
  animation: slideUp 0.6s ease-out;
}

.about-card:nth-child(1) {
  animation-delay: 0.1s;
}

.about-card:nth-child(2) {
  animation-delay: 0.2s;
}

.about-card:nth-child(3) {
  animation-delay: 0.3s;
}

.about-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 40px rgba(74, 144, 226, 0.2);
  border-color: rgba(74, 144, 226, 0.5);
}

.about-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: inline-block;
}

.about-card h3 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1rem;
  font-weight: 700;
}

.about-card p {
  color: #666;
  line-height: 1.6;
  font-size: 1rem;
}


.floating-blobs {
  position: fixed; /* 或者 absolute，根据你布局选 */
  inset: 0;
  pointer-events: none; /* 不挡点击 */
  z-index: 0; /* 放在内容最底层 */
  overflow: hidden;
}

/* 6 个超梦幻漂浮光点（可随意增减） */
.floating-blobs::before,
.floating-blobs::after,
.floating-blobs span,
.floating-blobs i,
.floating-blobs em,
.floating-blobs strong {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(120px); /* 越大越柔光，100~150px 都好看 */
  opacity: 0.6;
  animation: float 18s infinite ease-in-out;
}

/* 光点1 - 橙黄 */
.floating-blobs::before {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(255, 154, 60, 0.55) 0%, transparent 70%);
  top: 10%;
  left: 5%;
  animation-delay: 0s;
}

/* 光点2 - 紫罗兰 */
.floating-blobs::after {
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(136, 84, 255, 0.5) 0%, transparent 70%);
  top: 50%;
  left: 70%;
  animation-delay: 4s;
}

/* 光点3 - 天蓝 */
.floating-blobs span {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(80, 180, 255, 0.55) 0%, transparent 70%);
  top: 70%;
  left: 15%;
  animation-delay: 8s;
}

/* 光点4 - 薄荷绿 */
.floating-blobs i {
  width: 700px;
  height: 700px;
  background: radial-gradient(circle, rgba(99, 255, 163, 0.45) 0%, transparent 70%);
  top: 20%;
  left: 60%;
  animation-delay: 12s;
}

/* 光点5 - 粉红 */
.floating-blobs em {
  width: 550px;
  height: 550px;
  background: radial-gradient(circle, rgba(255, 108, 180, 0.5) 0%, transparent 70%);
  top: 60%;
  left: 50%;
  animation-delay: 2s;
}

/* 光点6 - 深紫（与你主题色一致） */
.floating-blobs strong {
  width: 650px;
  height: 650px;
  background: radial-gradient(circle, rgba(102, 86, 234, 0.55) 0%, transparent 70%);
  top: 30%;
  left: 80%;
  animation-delay: 10s;
}



.hero-right {
display: flex;
  justify-content: center;     /* 水平居中 */
  align-items: flex-start;     /* 关键：改为顶部对齐 → 图片整体上移 */
}

.hero-image {
  max-width: 600px;            /* 最大不超过 600px，超大屏也不爆屏 */
  transition: transform 0.4s ease;
}

@keyframes float {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  25% {
    transform: translate(20vw, -30vh) scale(1.1);
  }
  50% {
    transform: translate(-15vw, 20vh) scale(0.9);
  }
  75% {
    transform: translate(10vw, 25vh) scale(1.15);
  }
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

/* 响应式 不可列类 */
@media (max-width: 768px) {
  .about-container {
    grid-template-columns: 1fr;
  }
}
</style>