<template>
  <div class="smart-seating-container">
    <div class="panel-header">
      <h2>🪑 智能座位表</h2>
      <p class="panel-desc">可视化课堂座位安排和学生管理</p>
    </div>

    <!-- 顶部控制区 -->
    <div class="control-panel">
      <div class="left-section">
        <h3>当前学生</h3>
        <div v-if="currentStudent" class="student-card">
          <div class="student-name">{{ currentStudent.fullname }}</div>
          <div class="student-id">ID: {{ currentStudent.id }}</div>
          <div class="student-username">{{ currentStudent.username }}</div>
        </div>
        <div v-else class="student-card empty">
          <div class="empty-text">暂无学生信息</div>
        </div>
      </div>
      
      <div class="right-section">
        <button @click="previousStudent" :disabled="isFinished || !currentStudent" class="btn-nav prev">
          ← 上一位
        </button>
        <button @click="nextStudent" :disabled="isFinished || !currentStudent" class="btn-nav next">
          下一位 →
        </button>
        <button @click="resetSeating" class="btn-action reset">🔄 重置座位</button>
        <button @click="exportSeating" class="btn-action export">📥 导出座位表</button>
      </div>
    </div>

    <!-- 座位表区域 -->
    <div class="seating-area">
      <div class="seating-wrapper">
        <!-- 讲台 -->
        <div class="podium">讲台</div>

        <!-- 三个网格布局 -->
        <div class="grids-container">
          <!-- 左侧网格 -->
          <div class="grid grid-section grid-left">
            <div class="section-title">左侧座位(32)</div>
            <div class="grid-content">
              <div
                v-for="(cell, index) in leftGrid"
                :key="`left-${index}`"
                class="seat"
                :class="{ 'occupied': cell.student, 'selected': isCurrentSeat('left', index), 'disabled': isFinished }"
                @click="assignSeat('left', index)"
                :title="cell.student ? cell.student : '空座位'"
              >
                <div class="seat-label">{{ cell.label }}</div>
                <div v-if="cell.student" class="seat-student">{{ cell.student }}</div>
              </div>
            </div>
          </div>

          <!-- 中间网格 -->
          <div class="grid grid-section grid-middle">
            <div class="section-title">中间座位(48)</div>
            <div class="grid-content">
              <div
                v-for="(cell, index) in middleGrid"
                :key="`middle-${index}`"
                class="seat"
                :class="{ 'occupied': cell.student, 'selected': isCurrentSeat('middle', index), 'disabled': isFinished }"
                @click="assignSeat('middle', index)"
                :title="cell.student ? cell.student : '空座位'"
              >
                <div class="seat-label">{{ cell.label }}</div>
                <div v-if="cell.student" class="seat-student">{{ cell.student }}</div>
              </div>
            </div>
          </div>

          <!-- 右侧网格 -->
          <div class="grid grid-section grid-right">
            <div class="section-title">右侧座位(24)</div>
            <div class="grid-content">
              <div
                v-for="(cell, index) in rightGrid"
                :key="`right-${index}`"
                class="seat"
                :class="{ 'occupied': cell.student, 'selected': isCurrentSeat('right', index), 'disabled': isFinished }"
                @click="assignSeat('right', index)"
                :title="cell.student ? cell.student : '空座位'"
              >
                <div class="seat-label">{{ cell.label }}</div>
                <div v-if="cell.student" class="seat-student">{{ cell.student }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="statistics-panel">
      <div class="stat-item">
        <div class="stat-label">已分配座位</div>
        <div class="stat-value">{{ assignedCount }}/{{ totalStudents }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-label">空座位数</div>
        <div class="stat-value">{{ emptySeatsCount }}</div>
      </div>
      <div class="stat-item">
        <div class="stat-label">占用率</div>
        <div class="stat-value">{{ occupancyRate }}%</div>
      </div>
      <div class="stat-item">
        <div class="stat-label">状态</div>
        <div class="stat-value" :class="isFinished ? 'finished' : 'pending'">
          {{ isFinished ? '已完成' : '进行中' }}
        </div>
      </div>
    </div>

    <!-- 完成提示 -->
    <transition name="bounce">
      <div v-if="isFinished" class="finish-banner">
        <div class="banner-content">
          <div class="banner-icon">✅</div>
          <div class="banner-text">
            <h3>座位分配完成！</h3>
            <p>所有学生已分配座位，座位表已锁定。</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

// 学生列表（从数据库获取）
const students = ref([])
const currentStudent = ref(null)
const isFinished = ref(false)

// 生成网格单元格
const generateGrid = (rows, cols) => {
  const cells = []
  for (let row = 1; row <= rows; row++) {
    for (let col = 1; col <= cols; col++) {
      cells.push({
        label: `${row}-${col}`,
        student: null
      })
    }
  }
  return cells
}

// 初始化三个网格（改为6排）
const leftGrid = ref(generateGrid(6, 4))
const middleGrid = ref(generateGrid(6, 6))
const rightGrid = ref(generateGrid(6, 3))

// 已分配座位的学生集合
const assignedStudents = ref(new Set())
let currentIndex = 0

// 统计信息
const assignedCount = computed(() => assignedStudents.value.size)
const totalStudents = computed(() => students.value.length)
const totalSeats = computed(() => leftGrid.value.length + middleGrid.value.length + rightGrid.value.length)
const emptySeatsCount = computed(() => totalSeats.value - assignedCount.value)
const occupancyRate = computed(() => {
  return totalStudents.value > 0 ? Math.round((assignedCount.value / totalStudents.value) * 100) : 0
})

// 从数据库加载学生列表
const loadStudents = async () => {
  try {
    console.log('🔄 开始加载学生列表...')
    const token = localStorage.getItem('token')
    if (!token) {
      console.error('❌ 未获取到token')
      ElMessage.error('未获取到认证信息，请重新登录')
      return
    }
    
    let response = null
    const urls = [
      'http://localhost:5000/api/seating/students',
      'http://127.0.0.1:5000/api/seating/students',
      '/api/seating/students'
    ]
    
    let lastError = null
    for (const url of urls) {
      try {
        console.log(`📤 尝试连接: ${url}`)
        response = await fetch(url, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        
        console.log(`📡 响应状态 (${url}): ${response.status} ${response.statusText}`)
        
        if (response.ok) {
          console.log(`✅ 成功连接: ${url}`)
          break
        }
      } catch (err) {
        console.warn(`⚠️ ${url} 连接失败:`, err.message)
        lastError = err
      }
    }
    
    if (!response || !response.ok) {
      throw lastError || new Error(`无法连接到服务器 (最后状态: ${response?.status || 'unknown'})`)
    }
    
    const result = await response.json()
    console.log('📊 学生列表数据:', result)
    
    if (result.code === 200) {
      if (result.data && result.data.length > 0) {
        // 将API数据中的'name'字段转换为'fullname'以不破坏页面逻辑
        students.value = result.data.map(s => ({
          id: s.id,
          fullname: s.name
        }))
        if (students.value.length > 0) {
          currentStudent.value = { ...students.value[0] }
        }
        console.log('✅ 已加载学生列表:', students.value.length, '名学生')
        console.log('📋 学生数据样本:', result.data[0])
      } else {
        console.warn('⚠️ API返回空学生列表')
        ElMessage.warning('暂无学生数据，请先添加学生')
        students.value = []
      }
    } else {
      ElMessage.error(result.message || '加载学生列表失败')
      console.error('❌ API错误:', result.message, '完整响应:', result)
    }
  } catch (error) {
    console.error('❌ 加载学生列表错误:', error)
    ElMessage.error('加载学生列表失败: ' + (error.message || '网络错误'))
  }
}

// 切换到下一位学生
const nextStudent = () => {
  if (isFinished.value || students.value.length === 0) return
  
  currentIndex = (currentIndex + 1) % students.value.length
  currentStudent.value = { ...students.value[currentIndex] }
}

// 切换到上一位学生
const previousStudent = () => {
  if (isFinished.value || students.value.length === 0) return
  
  currentIndex = (currentIndex - 1 + students.value.length) % students.value.length
  currentStudent.value = { ...students.value[currentIndex] }
}

// 检查是否为当前学生的座位
const isCurrentSeat = (gridType, index) => {
  if (!currentStudent.value) return false
  
  const targetGrid = gridType === 'left' ? leftGrid.value : gridType === 'middle' ? middleGrid.value : rightGrid.value
  return targetGrid[index].student === currentStudent.value.fullname
}

// 分配座位
const assignSeat = (gridType, index) => {
  if (isFinished.value || !currentStudent.value) return
  
  const targetGrid = gridType === 'left' ? leftGrid.value : gridType === 'middle' ? middleGrid.value : rightGrid.value
  const studentName = currentStudent.value.fullname
  
  // 清除该学生在其他座位的分配
  clearStudentFromAllGrids(studentName)
  
  // 分配座位
  targetGrid[index].student = studentName
  assignedStudents.value.add(studentName)
  
  // 检查是否完成
  checkIfFinished()
  
  // 自动切换到下一位学生
  if (!isFinished.value) {
    nextStudent()
  }
}

// 检查是否完成分配
const checkIfFinished = () => {
  const allAssigned = students.value.every(student => assignedStudents.value.has(student.fullname))
  if (allAssigned) {
    isFinished.value = true
    currentStudent.value = null
    ElMessage.success('所有学生座位分配完成！')
  }
}

// 清除学生在所有网格中的分配
const clearStudentFromAllGrids = (studentName) => {
  leftGrid.value.forEach(cell => {
    if (cell.student === studentName) cell.student = null
  })
  middleGrid.value.forEach(cell => {
    if (cell.student === studentName) cell.student = null
  })
  rightGrid.value.forEach(cell => {
    if (cell.student === studentName) cell.student = null
  })
}

// 重置座位分配（改为6排）
const resetSeating = () => {
  if (confirm('确认要重置所有座位分配吗？')) {
    leftGrid.value = generateGrid(6, 4)
    middleGrid.value = generateGrid(6, 6)
    rightGrid.value = generateGrid(6, 3)
    assignedStudents.value.clear()
    isFinished.value = false
    currentIndex = 0
    if (students.value.length > 0) {
      currentStudent.value = { ...students.value[0] }
    }
    ElMessage.success('座位分配已重置')
  }
}

// 导出座位表
const exportSeating = () => {
  const seatingData = []
  
  leftGrid.value.forEach((cell, idx) => {
    if (cell.student) seatingData.push({ seat: `左-${cell.label}`, student: cell.student })
  })
  middleGrid.value.forEach((cell, idx) => {
    if (cell.student) seatingData.push({ seat: `中-${cell.label}`, student: cell.student })
  })
  rightGrid.value.forEach((cell, idx) => {
    if (cell.student) seatingData.push({ seat: `右-${cell.label}`, student: cell.student })
  })
  
  // 生成CSV（使用BOM以正确显示中文）
  const BOM = '\uFEFF'
  let csvContent = BOM + '座位号,学生姓名\r\n'
  seatingData.forEach(item => {
    csvContent += `${item.seat},${item.student}\r\n`
  })
  
  // 下载
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `座位表_${new Date().toLocaleDateString()}.csv`
  link.click()
  URL.revokeObjectURL(link.href)
  ElMessage.success('座位表已导出')
}

onMounted(() => {
  loadStudents()
}
)
</script>

<style scoped>
.smart-seating-container {
  padding: 0;
}

.panel-header {
  margin-bottom: 0.8rem;
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

/* 控制面板 */
.control-panel {
  background: linear-gradient(135deg, #f5f9ff 0%, #e6f2ff 100%);
  border: 1px solid #d0e8f2;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  flex-wrap: wrap;
}

.left-section {
  flex: 1;
  min-width: 300px;
}

.left-section h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1rem;
  font-weight: 600;
}

.student-card {
  background: white;
  border: 2px solid #4a90e2;
  border-radius: 8px;
  padding: 0.6rem;
  text-align: center;
}

.student-card.empty {
  border-color: #e8eef5;
  color: #999;
}

.student-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #4a90e2;
  margin-bottom: 0.2rem;
}

.student-id,
.student-username {
  font-size: 0.9rem;
  color: #666;
  margin: 0.2rem 0;
}

.empty-text {
  color: #999;
}

.right-section {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.btn-nav,
.btn-action {
  padding: 0.75rem 1.2rem;
  border: none;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.btn-nav {
  background: linear-gradient(135deg, #a8d4e8 0%, #7ec8e3 100%);
  color: white;
}

.btn-nav:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.btn-nav:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-action {
  background: white;
  border: 2px solid #4a90e2;
  color: #4a90e2;
}

.btn-action:hover {
  background: #f0f0f0;
}

.btn-action.reset {
  border-color: #faad14;
  color: #faad14;
}

.btn-action.export {
  border-color: #52c41a;
  color: #52c41a;
}

/* 座位表区域 */
.seating-area {
  background: white;
  border: 1px solid #e8eef5;
  border-radius: 8px;
  padding: 1.2rem;
  margin-bottom: 1rem;
  overflow-x: auto;
}

.seating-wrapper {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.podium {
  text-align: center;
  padding: 0.6rem;
  background: linear-gradient(135deg, #333 0%, #555 100%);
  color: white;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.95rem;
}

.grids-container {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.grid-section {
  flex-shrink: 0;
}

.section-title {
  text-align: center;
  font-weight: 700;
  color: #333;
  margin-bottom: 0.6rem;
  font-size: 0.95rem;
  padding-bottom: 0.3rem;
  border-bottom: 2px solid #4a90e2;
}

.grid-content {
  display: grid;
  gap: 6px;
  padding: 0.8rem;
  background: #fafbfc;
  border-radius: 6px;
}

.grid-left .grid-content {
  grid-template-columns: repeat(4, 80px);
  grid-template-rows: repeat(6, 70px);
}

.grid-middle .grid-content {
  grid-template-columns: repeat(6, 80px);
  grid-template-rows: repeat(6, 70px);
}

.grid-right .grid-content {
  grid-template-columns: repeat(3, 80px);
  grid-template-rows: repeat(6, 70px);
}

.seat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: white;
  border: 2px solid #d0e8f2;
  border-radius: 6px;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  font-size: 0.9rem;
  font-weight: 500;
  color: #666;
}

.seat:hover:not(.disabled) {
  border-color: #4a90e2;
  background: linear-gradient(135deg, #f0f8ff 0%, #e6f2ff 100%);
  transform: scale(1.05);
}

.seat.occupied {
  background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
  color: white;
  border-color: #357abd;
  box-shadow: 0 4px 8px rgba(74, 144, 226, 0.3);
}

.seat.occupied .seat-label {
  color: rgba(255, 255, 255, 0.8);
}

.seat.selected {
  border-color: #52c41a;
  background: #f6ffed;
}

.seat.disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

.seat-label {
  font-size: 0.75rem;
  color: #999;
  margin-bottom: 0.2rem;
}

.seat-student {
  font-size: 0.8rem;
  font-weight: 700;
  white-space: nowrap;
  text-overflow: ellipsis;
  max-width: 100%;
}

/* 统计信息 */
.statistics-panel {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.stat-item {
  background: linear-gradient(135deg, #f5f9ff 0%, #e6f2ff 100%);
  border: 1px solid #d0e8f2;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
}

.stat-label {
  color: #666;
  font-size: 0.85rem;
  margin-bottom: 0.3rem;
}

.stat-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #4a90e2;
}

.stat-value.finished {
  color: #52c41a;
}

.stat-value.pending {
  color: #faad14;
}

/* 完成提示 */
.finish-banner {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  padding: 2rem;
  z-index: 1000;
  max-width: 400px;
}

.banner-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}

.banner-icon {
  font-size: 3rem;
  animation: bounce 0.6s ease-in-out;
}

.banner-text h3 {
  margin: 0;
  color: #333;
  font-size: 1.5rem;
}

.banner-text p {
  margin: 0.5rem 0 0 0;
  color: #666;
  font-size: 0.95rem;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* 转不动画面 */
.bounce-enter-active {
  animation: bounce 0.6s ease-in-out;
}

.bounce-leave-active {
  animation: bounce 0.6s ease-in-out reverse;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .grids-container {
    flex-direction: column;
  }
  
  .control-panel {
    flex-direction: column;
  }
  
  .right-section {
    justify-content: center;
  }
}
</style>
