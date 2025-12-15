<template>
  <div class="attendance-container">
    <!-- 弹窗提示 -->
    <GlassModal
      :visible="modal.visible"
      :message="modal.message"
      :type="modal.type"
      @close="modal.visible = false"
    />

    <!-- Tab 导航 -->
    <div class="tab-navigation">
      <div
        v-for="tab in tabs"
        :key="tab.id"
        :class="['tab-item', { active: activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
      </div>
    </div>

    <!-- Tab 内容 -->
    <div class="tab-content">
      <!-- 创建考勤任务 -->
      <div v-if="activeTab === 'create'" class="tab-pane">
        <div class="card">
          <div class="card-title">创建考勤任务</div>
          <form class="form-grid">
            <div class="form-group">
              <label>任务名称 *</label>
              <input v-model="newTask.taskName" type="text" placeholder="如：2025-12-07 第三节课" />
            </div>
            <div class="form-group">
              <label>班级名称</label>
              <input v-model="newTask.className" type="text" placeholder="班级名称" />
            </div>
            <div class="form-group">
              <label>课程名称</label>
              <input v-model="newTask.subject" type="text" placeholder="课程名称" />
            </div>
            <div class="form-group">
              <label>预期出勤人数</label>
              <input v-model.number="newTask.expectedCount" type="number" placeholder="0" />
            </div>
          </form>
          <div class="form-group full-width">
            <label>备注</label>
            <textarea v-model="newTask.notes" placeholder="任务备注" rows="3"></textarea>
          </div>
          <button class="btn btn-primary" @click="createTask">创建任务</button>
        </div>
      </div>

      <!-- 进行中的考勤 -->
      <div v-if="activeTab === 'active'" class="tab-pane">
        <div v-if="activeTasks.length === 0" class="empty-state">
          <p>暂无进行中的考勤任务</p>
        </div>
        <div v-else>
          <div v-for="task in activeTasks" :key="task.id" class="task-card">
            <div class="task-header">
              <h3>{{ task.taskName }}</h3>
              <span class="status active">进行中</span>
            </div>
            <div class="task-info">
              <p><strong>班级:</strong> {{ task.className || '-' }}</p>
              <p><strong>课程:</strong> {{ task.subject || '-' }}</p>
              <p><strong>出勤:</strong> {{ task.actualCount }} / {{ task.expectedCount }}</p>
            </div>
            
            <!-- 进行中的任务展示更多详情 -->
            <div class="task-progress">
              <div class="progress-item">
                <span class="progress-label">出勤进度</span>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: (task.actualCount / Math.max(task.expectedCount, 1)) * 100 + '%' }"></div>
                </div>
                <span class="progress-percent">{{ Math.round((task.actualCount / Math.max(task.expectedCount, 1)) * 100) }}%</span>
              </div>
            </div>
            
            <!-- 实时签到学生列表 -->
            <div class="task-checkin-list">
              <h4>已签到学生 ({{ task.actualCount }})</h4>
              <div class="checkin-students">
                <div v-for="(student, idx) in getTaskStudents(task.id).slice(0, 5)" :key="idx" class="student-badge">
                  {{ student }}
                </div>
                <div v-if="getTaskStudents(task.id).length > 5" class="more-badge">
                  +{{ getTaskStudents(task.id).length - 5 }} 人
                </div>
              </div>
            </div>
            
            <!-- 任务状态统计 -->
            <div class="task-stats">
              <div class="stat">
                <span class="stat-label">开始时间</span>
                <span class="stat-value">{{ task.startTime ? formatTime(task.startTime) : '未开始' }}</span>
              </div>
              <div class="stat">
                <span class="stat-label">持续时间</span>
                <span class="stat-value">{{ calculateDuration(task.startTime) }}</span>
              </div>
              <div class="stat">
                <span class="stat-label">未到人数</span>
                <span class="stat-value">{{ Math.max(0, task.expectedCount - task.actualCount) }}</span>
              </div>
            </div>
            
            <div class="task-actions">
              <button class="btn btn-small btn-secondary" @click="viewTaskDetails(task.id)">查看详情</button>
              <button class="btn btn-small btn-danger" @click="endTask(task.id)">结束考勤</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 历史记录 -->
      <div v-if="activeTab === 'history'" class="tab-pane">
        <div v-if="historyTasks.length === 0" class="empty-state">
          <p>暂无历史考勤记录</p>
        </div>
        <div v-else>
          <table class="data-table">
            <thead>
              <tr>
                <th>任务名称</th>
                <th>班级</th>
                <th>课程</th>
                <th>出勤人数</th>
                <th>操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in historyTasks" :key="task.id">
                <td>{{ task.taskName }}</td>
                <td>{{ task.className || '-' }}</td>
                <td>{{ task.subject || '-' }}</td>
                <td>{{ task.actualCount }} / {{ task.expectedCount }}</td>
                <td>
                  <button class="btn btn-tiny" @click="viewTaskDetails(task.id)">详情</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- 统计分析 -->
      <div v-if="activeTab === 'stats'" class="tab-pane">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">总考勤次数</div>
            <div class="stat-value">{{ totalAttendanceTasks }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">平均出勤率</div>
            <div class="stat-value">{{ avgAttendanceRate }}%</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">今月出勤率</div>
            <div class="stat-value">{{ currentMonthRate }}%</div>
          </div>
        </div>

        <div class="card" style="margin-top: 2rem">
          <div class="card-title">学生出勤统计</div>
          <table class="data-table">
            <thead>
              <tr>
                <th>学生名称</th>
                <th>出勤次数</th>
                <th>缺勤次数</th>
                <th>出勤率</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="stat in attendanceStats" :key="stat.studentId">
                <td>{{ stat.studentName }}</td>
                <td>{{ stat.presentCount }}</td>
                <td>{{ stat.absentCount }}</td>
                <td>
                  <div class="progress-bar">
                    <div class="progress" :style="{ width: stat.rate + '%' }"></div>
                  </div>
                  {{ stat.rate }}%
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 任务详情模态框 -->
    <div v-if="showDetailModal" class="modal-overlay" @click="showDetailModal = false">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h3>考勤详情</h3>
          <button class="close-btn" @click="showDetailModal = false">✕</button>
        </div>
        <div class="modal-body">
          <div v-if="selectedTask" class="task-detail">
            <h4>{{ selectedTask.taskName }}</h4>
            <div class="detail-info">
              <p><strong>状态:</strong> <span class="status" :class="selectedTask.status">{{ selectedTask.status }}</span></p>
              <p><strong>班级:</strong> {{ selectedTask.className || '-' }}</p>
              <p><strong>课程:</strong> {{ selectedTask.subject || '-' }}</p>
              <p><strong>创建时间:</strong> {{ formatDate(selectedTask.createdAt) }}</p>
            </div>

            <h4 style="margin-top: 1.5rem">学生签到情况</h4>
            <table class="data-table compact">
              <thead>
                <tr>
                  <th>学生名称</th>
                  <th>签到方式</th>
                  <th>签到时间</th>
                  <th>状态</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="record in taskRecords" :key="record.recordId">
                  <td>{{ record.studentName }}</td>
                  <td>{{ record.checkInMethod === 'qr_code' ? '二维码' : '手动' }}</td>
                  <td>{{ record.checkInTime ? formatDate(record.checkInTime) : '-' }}</td>
                  <td>
                    <span v-if="record.isPresent === 1" class="badge badge-success">出勤</span>
                    <span v-else class="badge badge-danger">缺勤</span>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import GlassModal from './GlassModal.vue'

const activeTab = ref('create')
const showDetailModal = ref(false)
const selectedTask = ref(null)
const taskRecords = ref([])

const modal = ref({
  visible: false,
  message: '',
  type: 'info'
})

const showModal = (message, type = 'info') => {
  modal.value = {
    visible: true,
    message,
    type
  }
}

const newTask = ref({
  taskName: '',
  className: '',
  subject: '',
  expectedCount: 0,
  notes: ''
})

const tasks = ref([])
const attendanceStats = ref([])

const tabs = [
  { id: 'create', label: '创建任务' },
  { id: 'active', label: '进行中' },
  { id: 'history', label: '历史记录' },
  { id: 'stats', label: '统计分析' }
]

const activeTasks = computed(() => tasks.value.filter(t => t.status === 'in_progress'))
const historyTasks = computed(() => tasks.value.filter(t => t.status === 'completed'))
const totalAttendanceTasks = computed(() => tasks.value.length)
const avgAttendanceRate = computed(() => {
  if (attendanceStats.value.length === 0) return 0
  const avg = attendanceStats.value.reduce((sum, s) => sum + s.rate, 0) / attendanceStats.value.length
  return Math.round(avg)
})
const currentMonthRate = computed(() => {
  const currentMonthStats = attendanceStats.value.filter(s => {
    const date = new Date()
    return date.getMonth() === date.getMonth()
  })
  if (currentMonthStats.length === 0) return 0
  const avg = currentMonthStats.reduce((sum, s) => sum + s.rate, 0) / currentMonthStats.length
  return Math.round(avg)
})

const createTask = async () => {
  if (!newTask.value.taskName) {
    showModal('请输入任务名称', 'error')
    return
  }

  try {
    // 调用后端 API 创建考勤任务
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/attendance/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        task_name: newTask.value.taskName,
        class_name: newTask.value.className,
        subject: newTask.value.subject,
        expected_count: newTask.value.expectedCount || 0,
        notes: newTask.value.notes
      })
    })

    if (response.ok) {
      const data = await response.json()
      const task = {
        id: data.data.id,
        taskName: newTask.value.taskName,
        className: newTask.value.className,
        subject: newTask.value.subject,
        expectedCount: newTask.value.expectedCount || 0,
        actualCount: 0,
        status: 'pending',
        notes: newTask.value.notes,
        createdAt: new Date().toISOString()
      }
      tasks.value.push(task)
      showModal('考勤任务创建成功', 'success')
      
      // 重置表单
      newTask.value = {
        taskName: '',
        className: '',
        subject: '',
        expectedCount: 0,
        notes: ''
      }
    } else {
      showModal('创建失败，请稍后再试', 'error')
    }
  } catch (error) {
    showModal('创建失败: ' + error.message, 'error')
  }
}

const endTask = async (taskId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/attendance/tasks/${taskId}/end`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      const task = tasks.value.find(t => t.id === taskId)
      if (task) {
        task.status = 'completed'
        task.endTime = new Date().toISOString()
        showModal('考勤已结束', 'success')
      }
    } else {
      showModal('结束失败，请稍后再试', 'error')
    }
  } catch (error) {
    showModal('结束失败: ' + error.message, 'error')
  }
}

const viewTaskDetails = async (taskId) => {
  selectedTask.value = tasks.value.find(t => t.id === taskId)
  if (selectedTask.value) {
    // 模拟获取任务记录
    taskRecords.value = [
      { recordId: 1, studentId: 1, studentName: '张浩', checkInMethod: 'qr_code', checkInTime: new Date().toISOString(), isPresent: 1 },
      { recordId: 2, studentId: 2, studentName: '李莉', checkInMethod: 'qr_code', checkInTime: new Date().toISOString(), isPresent: 1 },
      { recordId: 3, studentId: 3, studentName: '王军', checkInMethod: 'manual', checkInTime: new Date().toISOString(), isPresent: 1 },
      { recordId: 4, studentId: 4, studentName: '陈玲', checkInMethod: 'qr_code', checkInTime: null, isPresent: 0 }
    ]
    showDetailModal.value = true
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', { 
    year: 'numeric', 
    month: '2-digit', 
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatTime = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', { 
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  })
}

const calculateDuration = (startTime) => {
  if (!startTime) return '-'
  const start = new Date(startTime)
  const now = new Date()
  const diff = now - start
  const minutes = Math.floor(diff / 60000)
  if (minutes < 1) return '< 1分钟'
  if (minutes < 60) return `${minutes}分钟`
  const hours = Math.floor(minutes / 60)
  const mins = minutes % 60
  return `${hours}小时${mins}分钟`
}

const getTaskStudents = (taskId) => {
  // 模拟前端写死的学生签到列表
  const studentMap = {
    1: ['张浩', '李莉', '王军', '陈玲', '刘芳', '周明', '吴涛'],
    2: ['何梦瑶', '吕晨', '施雨涵', '郭强', '林晓雯'],
    3: ['李莉', '王军', '陈玲', '刘芳', '周明', '吴涛', '朱丽', '钱伟', '孙娜']
  }
  return studentMap[taskId] || []
}

onMounted(() => {
  // 模拟初始数据
  tasks.value = [
    {
      id: 2,
      taskName: '2025-12-09 第二节课',
      className: '232099',
      subject: '物理',
      expectedCount: 18,
      actualCount: 13,
      status: 'in_progress',
      startTime: new Date(Date.now() - 15 * 60000).toISOString(),
      createdAt: new Date().toISOString()
    },
    {
      id: 1,
      taskName: '2025-12-07 第一节课',
      className: '高二(1)班',
      subject: '数学',
      expectedCount: 16,
      actualCount: 15,
      status: 'completed',
      createdAt: new Date().toISOString()
    }
  ]

  // 模拟学生出勤统计
  attendanceStats.value = [
    { studentId: 1, studentName: '张浩', presentCount: 8, absentCount: 1, rate: 89 },
    { studentId: 2, studentName: '李莉', presentCount: 9, absentCount: 0, rate: 100 },
    { studentId: 3, studentName: '王军', presentCount: 6, absentCount: 3, rate: 67 },
    { studentId: 4, studentName: '陈玲', presentCount: 9, absentCount: 0, rate: 100 }
  ]
})
</script>

<style scoped>
.attendance-container {
  width: 100%;
  padding: 0;
  background: transparent;
  min-height: 100%;
}

/* Tab 导航 */
.tab-navigation {
  display: flex;
  gap: 0;
  margin-bottom: 1.5rem;
  border-bottom: 2px solid #e8eef5;
}

.tab-item {
  padding: 1rem 1.5rem;
  cursor: pointer;
  color: #666;
  font-weight: 500;
  border-bottom: 3px solid transparent;
  transition: all 0.3s ease;
  margin-bottom: -2px;
}

.tab-item:hover {
  color: #4A90E2;
}

.tab-item.active {
  color: #4A90E2;
  border-bottom-color: #4A90E2;
}

/* 卡片样式 */
.card {
  background: transparent;
  padding: 0;
  margin-bottom: 1.5rem;
}

.card-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #e8eef5;
}

/* 表单样式 */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 500;
  color: #333;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #e8eef5;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

/* 按钮样式 */
.btn {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.btn-secondary {
  background: #f5f5f5;
  color: #333;
  border: 1px solid #e8eef5;
}

.btn-secondary:hover {
  background: #e8eef5;
}

.btn-danger {
  background: #ff6b6b;
  color: white;
}

.btn-danger:hover {
  background: #ff5252;
}

.btn-small {
  padding: 0.5rem 1rem;
  font-size: 0.85rem;
}

.btn-tiny {
  padding: 0.4rem 0.8rem;
  font-size: 0.8rem;
  background: #4A90E2;
  color: white;
}

/* 任务卡片 */
.task-card {
  background: white;
  border: 1px solid #e8eef5;
  border-radius: 8px;
  padding: 1.5rem;
  margin-bottom: 1rem;
  transition: all 0.3s ease;
}

.task-card:hover {
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.15);
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f0f0f0;
}

.task-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.status {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status.active {
  background: #4A90E2;
  color: white;
}

.status.completed {
  background: #51cf66;
  color: white;
}

.task-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1rem;
}

.task-info p {
  margin: 0;
  color: #666;
  font-size: 0.95rem;
}

.task-actions {
  display: flex;
  gap: 0.5rem;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.stat-card {
  background: white;
  border: 1px solid #e8eef5;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
}

.stat-label {
  color: #666;
  font-size: 0.9rem;
  margin-bottom: 0.5rem;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #4A90E2;
}

/* 表格样式 */
.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.data-table thead {
  background: #f5f7fa;
}

.data-table th {
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #e8eef5;
}

.data-table td {
  padding: 0.75rem;
  border-bottom: 1px solid #f0f0f0;
  color: #666;
}

.data-table tr:hover {
  background: #fafbfc;
}

.data-table.compact td {
  padding: 0.5rem 0.75rem;
  font-size: 0.9rem;
}

/* 进度条 */
.progress-bar {
  display: inline-block;
  width: 100px;
  height: 6px;
  background: #f0f0f0;
  border-radius: 3px;
  overflow: hidden;
  margin-right: 0.5rem;
  vertical-align: middle;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #4A90E2, #357ABD);
  border-radius: 3px;
  transition: width 0.3s ease;
}

/* 徽章 */
.badge {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 3px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge-success {
  background: #d4edda;
  color: #155724;
}

.badge-danger {
  background: #f8d7da;
  color: #721c24;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
}

/* 模态框 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 0;
  max-width: 600px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid #e8eef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #999;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.task-detail h4 {
  margin: 1rem 0 0.5rem 0;
  font-size: 1rem;
  color: #333;
}

.task-detail h4:first-child {
  margin-top: 0;
}

.detail-info p {
  margin: 0.5rem 0;
  color: #666;
  font-size: 0.95rem;
}

.detail-info strong {
  color: #333;
}

/* 任务进行中的展示样式 */
.task-progress {
  margin: 1rem 0;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.05) 0%, rgba(74, 144, 226, 0.02) 100%);
  border-radius: 6px;
  border-left: 4px solid #4A90E2;
}

.progress-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.progress-label {
  font-weight: 600;
  color: #333;
  min-width: 70px;
  font-size: 0.9rem;
}

.progress-bar {
  flex: 1;
  height: 8px;
  background: #e8eef5;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4A90E2 0%, #357ABD 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-percent {
  color: #4A90E2;
  font-weight: 600;
  min-width: 40px;
  text-align: right;
  font-size: 0.9rem;
}

/* 已签到学生列表 */
.task-checkin-list {
  margin: 1rem 0;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(82, 196, 26, 0.05) 0%, rgba(82, 196, 26, 0.02) 100%);
  border-radius: 6px;
  border-left: 4px solid #52c41a;
}

.task-checkin-list h4 {
  margin: 0 0 0.8rem 0;
  font-size: 0.95rem;
  color: #333;
  font-weight: 600;
}

.checkin-students {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.student-badge {
  display: inline-block;
  background: linear-gradient(135deg, #52c41a 0%, #45a918 100%);
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 16px;
  font-size: 0.85rem;
  font-weight: 500;
  white-space: nowrap;
}

.more-badge {
  display: inline-block;
  background: #f0f0f0;
  color: #666;
  padding: 0.3rem 0.8rem;
  border-radius: 16px;
  font-size: 0.85rem;
  font-weight: 500;
}

/* 任务统计 */
.task-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin: 1rem 0;
  padding: 1rem;
  background: linear-gradient(135deg, rgba(255, 193, 7, 0.05) 0%, rgba(255, 193, 7, 0.02) 100%);
  border-radius: 6px;
  border-left: 4px solid #ffc107;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-label {
  font-size: 0.85rem;
  color: #999;
  font-weight: 500;
}

.stat-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
}
</style>
