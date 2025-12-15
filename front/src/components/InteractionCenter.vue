<template>
  <div class="interaction-container">
    <!-- 弹窗提示 -->
    <GlassModal
      :visible="modal.visible"
      :message="modal.message"
      :type="modal.type"
      @close="modal.visible = false"
    />

    <!-- 创建任务弹框 -->
    <TaskCreateModal
      :visible="createModalVisible"
      :task-type="currentTaskType"
      :form-data="currentFormData"
      @close="createModalVisible = false"
      @submit="handleCreateTask"
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
      <!-- 投票 -->
      <div v-if="activeTab === 'poll'" class="tab-pane">
        <div class="create-button-container">
          <button class="btn btn-primary btn-large" @click="openCreateModal('poll')">
            + 创建投票任务
          </button>
        </div>

        <div v-if="pollTasks.length === 0" class="empty-state">
          <p>暂无投票任务</p>
        </div>
        <div v-else>
          <div v-for="task in pollTasks" :key="task.id" class="task-card">
            <div class="task-header">
              <div class="task-title-wrapper">
                <span class="task-type-badge badge-poll">投票</span>
                <h3>{{ task.taskName }}</h3>
              </div>
              <div class="task-controls">
                <button v-if="task.status === 'draft'" class="btn btn-small btn-primary" @click="startTask(task.id)">
                  启动投票
                </button>
                <button v-else-if="task.status === 'active'" class="btn btn-small btn-danger" @click="endTask(task.id)">
                  结束投票
                </button>
                <span class="status" :class="task.status">{{ getStatusLabel(task.status) }}</span>
              </div>
            </div>
            <div v-if="task.status !== 'draft'" class="poll-results">
              <div v-for="option in task.options" :key="option.id" class="poll-option">
                <div class="option-header">
                  <span>{{ option.optionText }}</span>
                  <span class="vote-count">{{ option.voteCount }} 票</span>
                </div>
                <div class="progress-bar">
                  <div class="progress" :style="{ width: option.percentage + '%' }"></div>
                </div>
                <div class="percentage">{{ option.percentage }}%</div>
              </div>
            </div>
            <div v-else class="empty-state compact">
              <p>暂未启动投票</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 提问 -->
      <div v-if="activeTab === 'question'" class="tab-pane">
        <div class="create-button-container">
          <button class="btn btn-primary btn-large" @click="openCreateModal('question')">
            + 创建提问任务
          </button>
        </div>

        <div v-if="questionTasks.length === 0" class="empty-state">
          <p>暂无提问任务</p>
        </div>
        <div v-else>
          <div v-for="task in questionTasks" :key="task.id" class="task-card">
            <div class="task-header">
              <div class="task-title-wrapper">
                <span class="task-type-badge badge-question">提问</span>
                <h3>{{ task.taskName }}</h3>
              </div>
              <div class="task-controls">
                <button v-if="task.status === 'draft'" class="btn btn-small btn-primary" @click="startTask(task.id)">
                  启动提问
                </button>
                <button v-else-if="task.status === 'active'" class="btn btn-small btn-danger" @click="endTask(task.id)">
                  结束提问
                </button>
                <span class="status" :class="task.status">{{ getStatusLabel(task.status) }}</span>
              </div>
            </div>
            <div v-if="task.questions && task.questions.length > 0">
              <div v-for="q in task.questions" :key="q.id" class="question-item">
                <div class="question-text">{{ q.questionText }}</div>
                <div class="question-stats">
                  <span>{{ q.answerCount }} 人回答</span>
                  <span class="q-status">{{ q.status }}</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-state compact">
              <p>暂无问题</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 弹幕 -->
      <div v-if="activeTab === 'barrage'" class="tab-pane">
        <div class="create-button-container">
          <button class="btn btn-primary btn-large" @click="openCreateModal('barrage')">
            + 创建弹幕讨论
          </button>
        </div>

        <div v-if="barrageTasks.length === 0" class="empty-state">
          <p>暂无弹幕任务</p>
        </div>
        <div v-else>
          <div v-for="task in barrageTasks" :key="task.id" class="task-card">
            <div class="task-header">
              <div class="task-title-wrapper">
                <span class="task-type-badge badge-barrage">弹幕</span>
                <h3>{{ task.taskName }}</h3>
              </div>
              <div class="task-controls">
                <button v-if="task.status === 'draft'" class="btn btn-small btn-primary" @click="startTask(task.id)">
                  启动讨论
                </button>
                <button v-else-if="task.status === 'active'" class="btn btn-small btn-danger" @click="endTask(task.id)">
                  结束讨论
                </button>
                <span class="status" :class="task.status">{{ getStatusLabel(task.status) }}</span>
              </div>
            </div>
            <div v-if="task.messages && task.messages.length > 0" class="barrage-viewer">
              <div class="barrage-track">
                <div
                  v-for="(msg, idx) in getBarrageMessages(task)"
                  :key="`msg-${msg.id}-${idx}`"
                  class="barrage-message"
                  :style="{
                    backgroundColor: BARRAGE_COLORS[idx % BARRAGE_COLORS.length],
                    borderLeftColor: BARRAGE_COLORS[idx % BARRAGE_COLORS.length],
                    animationDelay: `${idx * 0.5}s`
                  }"
                >
                  <span class="msg-author">{{ msg.studentName || '匿名' }}：</span>
                  <span class="msg-content">{{ msg.messageText }}</span>
                </div>
              </div>
            </div>
            <div v-else class="empty-state compact">
              <p>暂无弹幕</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 统计 -->
      <div v-if="activeTab === 'stats'" class="tab-pane">
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">总互动数</div>
            <div class="stat-value">{{ totalInteractions }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">参与学生数</div>
            <div class="stat-value">{{ totalParticipants }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">投票任务</div>
            <div class="stat-value">{{ pollTasks.length }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">提问任务</div>
            <div class="stat-value">{{ questionTasks.length }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">弹幕任务</div>
            <div class="stat-value">{{ barrageTasks.length }}</div>
          </div>
        </div>

        <div class="card">
          <div class="card-title">互动任务列表</div>
          <table class="data-table">
            <thead>
              <tr>
                <th>任务名称</th>
                <th>类型</th>
                <th>状态</th>
                <th>参与人数</th>
                <th>创建时间</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="task in allTasks" :key="task.id">
                <td>{{ task.taskName }}</td>
                <td>
                  <span class="badge" :class="'badge-' + task.taskType">
                    {{ getTaskTypeLabel(task.taskType) }}
                  </span>
                </td>
                <td>
                  <span class="status" :class="task.status">{{ getStatusLabel(task.status) }}</span>
                </td>
                <td>{{ task.participationCount }}</td>
                <td>{{ formatDate(task.createdAt) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import GlassModal from './GlassModal.vue'
import TaskCreateModal from './TaskCreateModal.vue'

const activeTab = ref('poll')

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

// 创建任务弹框相关
const createModalVisible = ref(false)
const currentTaskType = ref('poll')
const currentFormData = ref({ taskName: '' })

const openCreateModal = (taskType) => {
  currentTaskType.value = taskType
  currentFormData.value = { taskName: '' }
  createModalVisible.value = true
}

const handleCreateTask = async () => {
  const taskType = currentTaskType.value
  const taskName = currentFormData.value.taskName

  if (!taskName || !taskName.trim()) {
    showModal('请输入一些内容', 'error')
    return
  }

  try {
    const token = localStorage.getItem('token')
    const response = await fetch('/api/interaction/tasks', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        task_name: taskName.trim(),
        task_type: taskType
      })
    })
    
    const result = await response.json()
    if (result.code === 200) {
      // 创建成功后，添加到本地列表
      let newTask = {
        id: result.data.id,
        taskName: taskName.trim(),
        taskType: taskType,
        status: 'draft',
        participationCount: 0,
        createdAt: new Date().toISOString()
      }

      if (taskType === 'poll') {
        newTask.options = [
          { id: 1, optionText: '非常满意', voteCount: 0, percentage: 0, studentId: null },
          { id: 2, optionText: '满意', voteCount: 0, percentage: 0, studentId: null },
          { id: 3, optionText: '一般', voteCount: 0, percentage: 0, studentId: null }
        ]
      } else if (taskType === 'question') {
        newTask.questions = []
      } else if (taskType === 'barrage') {
        newTask.messages = []
      }
      
      // 立即加载新任务的数据
      if (taskType === 'question') {
        await loadQuestions(result.data.id)
      }

      tasks.value.push(newTask)
      const typeLabels = { poll: '投票', question: '提问', barrage: '弹幕' }
      showModal(`${typeLabels[taskType]}任务创建成功`, 'success')
      createModalVisible.value = false
    } else {
      showModal(result.message || '创建失败', 'error')
    }
  } catch (error) {
    showModal('网络错误：' + error.message, 'error')
  }
}

const tasks = ref([])

const tabs = [
  { id: 'poll', label: '投票' },
  { id: 'question', label: '提问' },
  { id: 'barrage', label: '弹幕' },
  { id: 'stats', label: '统计' }
]

const pollTasks = computed(() => tasks.value.filter(t => t.taskType === 'poll'))
const questionTasks = computed(() => tasks.value.filter(t => t.taskType === 'question'))
const barrageTasks = computed(() => tasks.value.filter(t => t.taskType === 'barrage'))
const allTasks = computed(() => tasks.value)

// B站风格弹幕 - 从右往左水平滚动，多轨道显示
const BARRAGE_COLORS = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#95DE64', '#FF85C0', '#40C057']
const BARRAGE_TRACKS_NUM = 4  // 4个独立的滚动轨道

// 轨道消息分配（转换为单轨道子）
const getBarrageMessages = (task) => {
  if (!task || !task.messages || task.messages.length === 0) {
    return []
  }
  // 返回所有消恫，并且重复漂放
  const messages = task.messages
  const result = []
  
  // 同时按顺序显示消恫，为了转在一起，我们重复加入
  for (let i = 0; i < 2; i++) {
    result.push(...messages)
  }
  
  return result
}

const totalInteractions = computed(() => {
  return pollTasks.value.length + questionTasks.value.length + barrageTasks.value.length
})

const totalParticipants = computed(() => {
  const set = new Set()
  tasks.value.forEach(t => {
    if (t.participationCount) {
      set.add(t.id)  // 简单的统计方式：统计有参与人数的任务
    }
  })
  let total = 0
  tasks.value.forEach(t => {
    total += (t.participationCount || 0)
  })
  return total
})

const startTask = async (taskId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/interaction/tasks/${taskId}/start`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    const result = await response.json()
    if (result.code === 200) {
      const task = tasks.value.find(t => t.id === taskId)
      if (task) {
        task.status = 'active'
        task.startTime = new Date().toISOString()
        showModal('互动已启动', 'success')
        
        // 如果是弹幕任务，自动发送模拟消息
        if (task.taskType === 'barrage') {
          setTimeout(async () => {
            await sendMockBarrageMessages()
            await loadBarrageMessages(taskId)
          }, 1000)
        }
      }
    } else {
      showModal(result.message || '启动失败', 'error')
    }
  } catch (error) {
    showModal('网络错误：' + error.message, 'error')
  }
}

const endTask = async (taskId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`/api/interaction/tasks/${taskId}/end`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    const result = await response.json()
    if (result.code === 200) {
      const task = tasks.value.find(t => t.id === taskId)
      if (task) {
        task.status = 'completed'
        task.endTime = new Date().toISOString()
        showModal('互动已结束', 'success')
      }
    } else {
      showModal(result.message || '结束失败', 'error')
    }
  } catch (error) {
    showModal('网络错误：' + error.message, 'error')
  }
}

const getStatusLabel = (status) => {
  const labels = {
    draft: '草稿',
    active: '进行中',
    completed: '已结束'
  }
  return labels[status] || status
}

const getTaskTypeLabel = (type) => {
  const labels = {
    poll: '投票',
    question: '提问',
    barrage: '弹幕'
  }
  return labels[type] || type
}

const formatDate = (dateStr) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 加载所有互动任务
const loadTasks = async () => {
  try {
    console.log('🔄 开始加载互动任务...')
    const token = localStorage.getItem('token')
    console.log('📌 使用Token:', token ? '✅ 已获取' : '❌ 未获取')
    
    const apiUrl = 'http://localhost:5000/api/interaction/tasks'
    console.log('🌐 调用API:', apiUrl)
    const response = await fetch(apiUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    console.log('📡 API响应状态:', response.status, response.statusText)
    const result = await response.json()
    console.log('📋 API返回数据:', result)
    
    if (result.code === 200) {
      console.log('✅ 获取任务成功，共', result.data.length, '个任务')
      const tasksData = result.data.map(t => ({
        id: t.id,
        taskName: t.task_name,
        taskType: t.task_type,
        status: t.status,
        participationCount: t.participation_count || 0,
        createdAt: t.created_at,
        options: [],
        questions: [],
        messages: []
      }))
      tasks.value = tasksData
      console.log('📝 任务列表已更新，当前任务数:', tasks.value.length)
      
      // 加载每个任务的具体数据
      for (const task of tasksData) {
        console.log(`📌 处理任务 ${task.id} (类型: ${task.taskType})`)
        if (task.taskType === 'question') {
          await loadQuestions(task.id)
        } else if (task.taskType === 'barrage') {
          await loadBarrageMessages(task.id)
        }
      }
      console.log('✅ 所有任务数据加载完成')
    } else {
      console.error('❌ API错误:', result.message)
      showModal('API错误: ' + result.message, 'error')
    }
  } catch (error) {
    console.error('❌ 加载任务失败:', error)
    showModal('加载任务失败: ' + error.message, 'error')
  }
}

// 加载提问数据
const loadQuestions = async (taskId) => {
  try {
    console.log(`  📝 加载提问任务 ${taskId} 的题目...`)
    const apiUrl = `http://localhost:5000/api/interaction/questions/${taskId}/list`
    const response = await fetch(apiUrl)
    console.log(`  📡 题目API响应: ${response.status}`)
    const result = await response.json()
    console.log(`  📋 题目数据:`, result)
    
    if (result.code === 200) {
      const task = tasks.value.find(t => t.id === taskId)
      if (task) {
        task.questions = result.data.map(q => ({
          id: q.id,
          questionText: q.question_text,
          status: q.status,
          answerCount: q.answer_count || 0
        }))
        console.log(`  ✅ 提问任务 ${taskId} 加载 ${task.questions.length} 道题目`)
      }
    } else {
      console.error(`  ❌ 加载提问失败:`, result.message)
    }
  } catch (error) {
    console.error(`  ❌ 加载提问异常:`, error)
  }
}

// 加载弹幕消息
const loadBarrageMessages = async (taskId) => {
  try {
    console.log(`  💬 加载弹幕任务 ${taskId} 的消息...`)
    const apiUrl = `http://localhost:5000/api/interaction/barrage/${taskId}/messages`
    const response = await fetch(apiUrl)
    console.log(`  📡 弹幕API响应: ${response.status}`)
    const result = await response.json()
    console.log(`  📋 弹幕数据:`, result)
    
    if (result.code === 200) {
      const task = tasks.value.find(t => t.id === taskId)
      if (task) {
        // 后端已经处理了student_name字段，直接使用
        task.messages = result.data.map(msg => ({
          id: msg.id,
          studentId: msg.student_id,
          studentName: msg.student_name || '匿名',
          messageText: msg.message_text,
          messageColor: msg.message_color || '#333333',
          likeCount: msg.like_count || 0,
          isPinned: msg.is_pinned || 0,
          createdAt: msg.created_at
        }))
        console.log(`  ✅ 弹幕任务 ${taskId} 加载 ${task.messages.length} 条消息`)
      }
    } else {
      console.error(`  ❌ 加载弹幕失败:`, result.message)
    }
  } catch (error) {
    console.error(`  ❌ 加载弹幕异常:`, error)
  }
}

// ... existing code ...

// 立即刷新弹幕消息
const refreshBarrageMessages = async () => {
  for (const barrage of barrageTasks.value) {
    if (barrage.status === 'active') {
      await loadBarrageMessages(barrage.id)
    }
  }
}

onMounted(async () => {
  console.log('🚀 InteractionCenter 组件已挂载')
  // 从数据库加载所有任务
  await loadTasks()
  
  console.log('⏰ 设置弹幕自动刷新计时器（每3秒）')
  // 每3秒加载一次弹幕消息（当任务是active时）
  const barrageInterval = setInterval(async () => {
    await refreshBarrageMessages()
  }, 3000)
  
  return () => {
    console.log('🛑 清理自动刷新计时器')
    clearInterval(barrageInterval)
  }
})
</script>

<style scoped>
.interaction-container {
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

/* 创建按钮容器 */
.create-button-container {
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
}

.btn-large {
  padding: 1rem 2rem;
  font-size: 1rem;
  min-width: 200px;
}
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

/* 表单 */
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
.form-group select,
.form-group textarea {
  padding: 0.75rem;
  border: 1px solid #e8eef5;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s ease;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

/* 按钮 */
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

.task-title-wrapper {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex: 1;
}

.task-header h3 {
  margin: 0;
  font-size: 1.1rem;
  color: #333;
}

.task-type-badge {
  display: inline-block;
  padding: 0.4rem 0.75rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 700;
  white-space: nowrap;
  color: white;
}

.task-type-badge.badge-poll {
  background: linear-gradient(135deg, #a8d4e8 0%, #7ec8e3 100%);
}

.task-type-badge.badge-question {
  background: linear-gradient(135deg, #b3d9f2 0%, #8ac6e8 100%);
}

.task-type-badge.badge-barrage {
  background: linear-gradient(135deg, #a9d1e8 0%, #7ebfe3 100%);
}

.task-controls {
  display: flex;
  gap: 0.5rem;
  align-items: center;
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

.status.draft {
  background: #f0f0f0;
  color: #666;
}

.status.completed {
  background: #51cf66;
  color: white;
}

/* 投票结果 */
.poll-results {
  margin-top: 1rem;
}

.poll-option {
  margin-bottom: 1rem;
}

.option-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 0.5rem;
  font-size: 0.95rem;
  color: #333;
}

.vote-count {
  font-weight: 600;
  color: #4A90E2;
}

.progress-bar {
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.25rem;
}

.progress {
  height: 100%;
  background: linear-gradient(90deg, #4A90E2, #357ABD);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.percentage {
  font-size: 0.8rem;
  color: #999;
}

/* 提问项目 */
.question-item {
  background: #f5f7fa;
  padding: 1rem;
  border-radius: 6px;
  margin-bottom: 0.75rem;
}

.question-text {
  color: #333;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.question-stats {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
  color: #999;
}

.q-status {
  padding: 0.2rem 0.5rem;
  background: white;
  border-radius: 3px;
  color: #4A90E2;
}

/* 弹幕 - B站风格从右往左 */
.barrage-viewer {
  height: 300px;
  overflow: hidden;
  border: 2px solid #e8eef5;
  border-radius: 8px;
  background: linear-gradient(180deg, #f9fafb 0%, #ffffff 100%);
  position: relative;
  display: flex;
  flex-direction: column;
}

.barrage-track {
  flex: 1;
  display: flex;
  align-items: center;
  position: relative;
  overflow: hidden;
  will-change: transform;
}

.barrage-message {
  flex-shrink: 0;
  white-space: nowrap;
  padding: 0.6rem 1.2rem;
  border-radius: 4px;
  margin: 0.3rem;
  height: fit-content;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.12);
  border-left: 3px solid;
  font-size: 0.85rem;
  color: white;
  display: inline-flex;
  align-items: center;
  animation: barrageHorizontal 15s linear infinite;
}

.barrage-message:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transform: scaleY(1.08);
  opacity: 1;
}

.msg-author {
  font-weight: 700;
  font-size: 0.8rem;
  color: white;
  white-space: nowrap;
}

.msg-content {
  color: rgba(255, 255, 255, 0.95);
  font-size: 0.85rem;
  margin-left: 0.4rem;
  white-space: nowrap;
}

/* 丰幕水平滚动动画 - 从右往左 */
@keyframes barrageHorizontal {
  0% {
    transform: translateX(100%);
  }
  100% {
    transform: translateX(calc(-100% - 40px));
  }
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

/* 表格 */
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

/* 徽章 */
.badge {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 3px;
  font-size: 0.8rem;
  font-weight: 600;
}

.badge-poll {
  background: #d1ecf1;
  color: #0c5460;
}

.badge-question {
  background: #cfe2ff;
  color: #084298;
}

.badge-barrage {
  background: #f8d7da;
  color: #842029;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.empty-state.compact {
  padding: 1.5rem;
  color: #999;
}

.tab-pane {
  animation: fadeIn 0.3s ease;
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
</style>
