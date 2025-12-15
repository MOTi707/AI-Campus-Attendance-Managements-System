<template>
  <div class="smart-attendance-container">
    <div class="panel-header">
      <h2>智能点到</h2>
      <p class="panel-desc">通过人脸识别自动生成课堂考勤</p>
    </div>

    <!-- 标签页导航 -->
    <div class="tab-nav">
      <div
        v-for="tab in tabs"
        :key="tab.id"
        class="tab-item"
        :class="{ active: activeTab === tab.id }"
        @click="activeTab = tab.id"
      >
        {{ tab.label }}
      </div>
    </div>

    <!-- 标签页内容 -->

    <!-- 1. 上传和识别 -->
    <div v-if="activeTab === 'upload'" class="tab-pane">
      <div class="card">
        <div class="card-title">📸 上传课堂照片</div>
        
        <!-- 文件上传区域 -->
        <div class="upload-area" @click="triggerFileInput" :class="{ 'dragover': isDragging }" @dragover="isDragging = true" @dragleave="isDragging = false" @drop="handleDrop">
          <input
            ref="fileInput"
            type="file"
            accept="image/*"
            style="display: none"
            @change="handleFileSelect"
          />
          <div class="upload-icon">📷</div>
          <p class="upload-text">点击或拖拽上传课堂照片</p>
          <p class="upload-hint">支持 PNG, JPG, JPEG, BMP 格式</p>
        </div>

        <!-- 上传进度 -->
        <div v-if="uploading" class="upload-progress">
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: uploadProgress + '%' }"></div>
          </div>
          <p>上传中... {{ uploadProgress }}%</p>
        </div>

        <!-- 选中的图片预览 -->
        <div v-if="selectedFile && !recognitionResult" class="image-preview">
          <img :src="previewUrl" alt="预览" />
          <div class="button-group">
            <button @click="performRecognition" :disabled="uploading" class="btn-primary">
              {{ uploading ? '处理中...' : '进行人脸识别' }}
            </button>
            <button @click="cancelSelection" class="btn-secondary">取消</button>
          </div>
        </div>
      </div>

      <!-- 识别结果 -->
      <div v-if="recognitionResult" class="card recognition-results">
        <div class="card-title">✨ 识别结果</div>
        
        <!-- 识别的学生列表 -->
        <div v-if="recognitionResult.students.length > 0" class="students-list">
          <h4>📋 识别的学生</h4>
          <div class="student-card" v-for="student in recognitionResult.students" :key="student.student_id">
            <div class="student-info">
              <div class="student-name">{{ student.student_name }}</div>
              <div class="student-id">ID: {{ student.student_id }}</div>
            </div>
            <div class="confidence-badge">{{ student.confidence }}%</div>
          </div>
        </div>

        <!-- 录入考勤按钮 -->
        <div class="action-buttons">
          <button @click="recordAttendance" class="btn-primary">✅ 录入考勤</button>
          <button @click="resetRecognition" class="btn-secondary">↻ 重新识别</button>
        </div>
      </div>
    </div>

    <!-- 2. 学生人脸库管理 -->
    <div v-if="activeTab === 'face-database'" class="tab-pane">
      <div class="card">
        <div class="card-title">👥 学生人脸库管理</div>
        
        <p class="desc-text">为学生添加人脸照片以提高识别准确度。每个学生建议添加2-3张清晰的正脸照片。</p>

        <!-- 学生列表 -->
        <div class="students-grid">
          <div v-for="student in students" :key="student.id" class="student-item">
            <div class="student-avatar">
              <div class="avatar-placeholder">{{ student.fullname.charAt(0) }}</div>
            </div>
            <div class="student-details">
              <h4>{{ student.fullname }}</h4>
              <p>{{ student.username }}</p>
            </div>
            
            <!-- 显示已录入的人脸照片 -->
            <div v-if="studentFaces[student.id] && studentFaces[student.id].length > 0" class="face-gallery">
              <div class="face-thumbnails">
                <div v-for="(face, index) in studentFaces[student.id]" :key="index" class="face-thumbnail-wrapper">
                  <!-- 加载中骨架屏 -->
                  <div v-if="imageLoadStatus[`${student.id}-${index}`] === 'loading'" class="face-thumbnail-skeleton">
                    <div class="skeleton-pulse"></div>
                  </div>
                  <!-- 实际图片 -->
                  <img 
                    v-show="imageLoadStatus[`${student.id}-${index}`] !== 'loading'"
                    :src="'http://localhost:5000' + face.image_url" 
                    :alt="face.student_name"
                    class="face-thumbnail"
                    @load="handleImageLoad(student.id, index)"
                    @error="handleImageError(student.id, index)"
                  />
                  <!-- 加载失败提示 -->
                  <div v-if="imageLoadStatus[`${student.id}-${index}`] === 'error'" class="face-thumbnail-error">
                    <span>加载失败</span>
                  </div>
                  <!-- 删除按鎇 -->
                  <button 
                    v-if="imageLoadStatus[`${student.id}-${index}`] === 'loaded'"
                    class="face-delete-btn"
                    @click="deleteFace(student.id, face.face_path, index)"
                    title="删除这张人脸"
                  >
                    ×
                  </button>
                </div>
              </div>
              <p class="face-count">已录入 {{ studentFaces[student.id].length }} 张人脸</p>
            </div>
            <!-- 加载中状态 -->
            <div v-else-if="facesLoadingStatus[student.id] === 'loading'" class="faces-loading">
              <div class="loading-spinner"></div>
              <p>加载人脸照片中...</p>
            </div>
            <!-- 加载失败 -->
            <div v-else-if="facesLoadingStatus[student.id] === 'error'" class="faces-error">
              <p>加载失败</p>
            </div>
            <!-- 暂无人脸照片（只有当加载完成后才显示） -->
            <div v-else-if="facesLoadingStatus[student.id] === 'success'" class="no-faces">
              <p>暂无人脸照片</p>
            </div>
            
            <button @click="openAddFaceDialog(student)" class="btn-upload">+ 添加人脸</button>
          </div>
        </div>
      </div>
    </div>

    <!-- 3. 考勤记录 -->
    <div v-if="activeTab === 'records'" class="tab-pane">
      <div class="card">
        <div class="card-title">📝 智能点到记录</div>
        
        <div class="records-table">
          <table class="data-table">
            <thead>
              <tr>
                <th>日期</th>
                <th>学生名称</th>
                <th>状态</th>
                <th>识别度</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="record in attendanceRecords" :key="record.id">
                <td>{{ formatDate(record.created_at) }}</td>
                <td>{{ record.student_name }}</td>
                <td>
                  <span class="status-badge" :class="'status-' + record.status">
                    {{ getStatusLabel(record.status) }}
                  </span>
                </td>
                <td>{{ record.confidence || '-' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- 4. 统计信息 -->
    <div v-if="activeTab === 'statistics'" class="tab-pane">
      <div class="card">
        <div class="card-title">📊 智能点到统计</div>
        
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-label">总考勤记录</div>
            <div class="stat-value">{{ statistics.total_records }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">出席</div>
            <div class="stat-value" style="color: #52c41a">{{ statistics.present_count }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">缺席</div>
            <div class="stat-value" style="color: #f5222d">{{ statistics.absent_count }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">迟到</div>
            <div class="stat-value" style="color: #faad14">{{ statistics.late_count }}</div>
          </div>
          <div class="stat-card">
            <div class="stat-label">出席率</div>
            <div class="stat-value" style="color: #4A90E2">{{ statistics.attendance_rate }}%</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 添加人脸对话框 -->
    <div v-if="showAddFaceDialog" class="modal-overlay" @click.self="showAddFaceDialog = false">
      <div class="modal-dialog">
        <div class="modal-header">
          <h3>为 {{ selectedStudent?.fullname }} 添加人脸</h3>
          <button @click="showAddFaceDialog = false" class="modal-close">×</button>
        </div>
        <div class="modal-body">
          <div class="upload-area-small" @click="triggerFaceFileInput">
            <input
              ref="faceFileInput"
              type="file"
              accept="image/*"
              style="display: none"
              @change="handleFaceFileSelect"
            />
            <div class="upload-icon">📷</div>
            <p>点击选择人脸照片</p>
          </div>
          <div v-if="facePreviewUrl" class="face-preview">
            <img :src="facePreviewUrl" alt="预览" />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="submitAddFace" :disabled="!selectedFaceFile" class="btn-primary">
            {{ addingFace ? '上传中...' : '确认上传' }}
          </button>
          <button @click="showAddFaceDialog = false" class="btn-secondary">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const activeTab = ref('upload')
const tabs = [
  { id: 'upload', label: '上传识别' },
  { id: 'face-database', label: '人脸库' },
  { id: 'records', label: '考勤记录' },
  { id: 'statistics', label: '统计' }
]

// 上传相关
const fileInput = ref(null)
const selectedFile = ref(null)
const previewUrl = ref('')
const isDragging = ref(false)
const uploading = ref(false)
const uploadProgress = ref(0)

// 识别结果
const recognitionResult = ref(null)

// 学生相关
const students = ref([])
const studentFaces = ref({}) // 存储每个学生的人脸照片
const facesLoadingStatus = ref({}) // 存储每个学生的加载状态
const imageLoadStatus = ref({}) // 存储每张图片的加载状态

// 考勤记录
const attendanceRecords = ref([])

// 统计数据
const statistics = ref({
  total_records: 0,
  present_count: 0,
  absent_count: 0,
  late_count: 0,
  attendance_rate: 0
})

// 添加人脸相关
const showAddFaceDialog = ref(false)
const selectedStudent = ref(null)
const faceFileInput = ref(null)
const selectedFaceFile = ref(null)
const facePreviewUrl = ref('')
const addingFace = ref(false)

// 方法
const triggerFileInput = () => {
  fileInput.value?.click()
}

const handleFileSelect = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

const handleDrop = (event) => {
  event.preventDefault()
  isDragging.value = false
  
  const file = event.dataTransfer?.files?.[0]
  if (file && file.type.startsWith('image/')) {
    selectedFile.value = file
    previewUrl.value = URL.createObjectURL(file)
  }
}

const cancelSelection = () => {
  selectedFile.value = null
  previewUrl.value = ''
  recognitionResult.value = null
}

const resetRecognition = () => {
  recognitionResult.value = null
  selectedFile.value = null
  previewUrl.value = ''
}

const performRecognition = async () => {
  if (!selectedFile.value) return
  
  uploading.value = true
  uploadProgress.value = 0
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/smart-attendance/upload-and-recognize', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    
    const result = await response.json()
    
    if (result.code === 200) {
      recognitionResult.value = result.data
      ElMessage.success('识别完成')
    } else {
      ElMessage.error(result.message || '识别失败')
    }
  } catch (error) {
    ElMessage.error('识别失败: ' + error.message)
  } finally {
    uploading.value = false
  }
}

const recordAttendance = async () => {
  if (!recognitionResult.value) return
  
  try {
    const token = localStorage.getItem('token')
    const students_data = recognitionResult.value.students.map(s => ({
      student_id: s.student_id,
      attendance_status: 'present',
      confidence: s.confidence
    }))
    
    const response = await fetch('http://localhost:5000/api/smart-attendance/record-attendance', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        students: students_data,
        notes: '通过智能点到记录'
      })
    })
    
    const result = await response.json()
    
    if (result.code === 200) {
      ElMessage.success('考勤已录入')
      resetRecognition()
      fetchAttendanceRecords()
      fetchStatistics()
    } else {
      ElMessage.error(result.message || '录入失败')
    }
  } catch (error) {
    ElMessage.error('录入失败: ' + error.message)
  }
}

const loadStudents = async () => {
  try {
    console.log('🔄 开始加载学生列表...')
    const token = localStorage.getItem('token')
    if (!token) {
      ElMessage.error('未获取到认证信息，请重新登录')
      console.error('❌ 未获取到token')
      return
    }
    
    // ... existing code ...
    
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
        // 将API数据中的'name'字段转换为'fullname'
        students.value = result.data.map(s => ({
          id: s.id,
          fullname: s.name
        }))
        // 加载每个学生的人脸照片
        await loadAllStudentFaces()
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

const loadAllStudentFaces = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    
    // 串行加载（每次一个），遭免一次性加载过上
    for (const student of students.value) {
      facesLoadingStatus.value[student.id] = 'loading'
      try {
        const response = await fetch(`http://localhost:5000/api/smart-attendance/student-faces/${student.id}`, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
          }
        })
        
        if (response.ok) {
          const result = await response.json()
          if (result.code === 200) {
            // 按照result.data的数据捉非一一添加上不上bb
            studentFaces.value[student.id] = result.data
            // 初始化每张图片的加载状态
            result.data.forEach((_, index) => {
              const imageKey = `${student.id}-${index}`
              imageLoadStatus.value[imageKey] = 'loading'
            })
            facesLoadingStatus.value[student.id] = 'success'
          }
        } else {
          facesLoadingStatus.value[student.id] = 'error'
        }
      } catch (error) {
        console.warn(`加载学生 ${student.id} 的人脸照片失败:`, error.message)
        facesLoadingStatus.value[student.id] = 'error'
      }
    }
  } catch (error) {
    console.warn('加载学生人脸照片失败:', error.message)
  }
}

const handleImageLoad = (studentId, index) => {
  const imageKey = `${studentId}-${index}`
  imageLoadStatus.value[imageKey] = 'loaded'
}

const handleImageError = (studentId, index) => {
  const imageKey = `${studentId}-${index}`
  imageLoadStatus.value[imageKey] = 'error'
}

const deleteFace = async (studentId, facePath, index) => {
  // 例子序列加上流程批源謜訊息确认
  const confirmResult = window.confirm(`确定要删除这张人脸么？`)
  if (!confirmResult) return
  
  try {
    const token = localStorage.getItem('token')
    const payloadData = {
      student_id: parseInt(studentId) || studentId,  // 确保是整数
      face_path: String(facePath).trim()  // 确保是字符串
    }
    
    console.log('📤 发送删除请求:', payloadData)  // 调试日志
    
    const response = await fetch('http://localhost:5000/api/smart-attendance/delete-student-face', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payloadData)
    })
    
    const result = await response.json()
    console.log('📥 删除响应:', result)  // 调试日志
    
    if (result.code === 200) {
      ElMessage.success('人脸已删除')
      // 重新加载该学生的人脸照片
      await loadStudentFaces(studentId)
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    console.error('❌ 删除错误:', error)  // 调试日志
    ElMessage.error('删除失败: ' + error.message)
  }
}

const fetchAttendanceRecords = async () => {
  try {
    console.log('🔄 开始加载考勤记录...')
    const token = localStorage.getItem('token')
    if (!token) return
    
    const response = await fetch('http://localhost:5000/api/smart-attendance/attendance-records', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      console.warn('获取考勤记录HTTP错误:', response.status)
      return
    }
    
    const result = await response.json()
    if (result.code === 200) {
      attendanceRecords.value = result.data
      console.log('✅ 考勤记录加载成功')
    }
  } catch (error) {
    console.warn('获取考勤记录失败:', error.message)
  }
}

const fetchStatistics = async () => {
  try {
    console.log('🔄 开始加载统计信息...')
    const token = localStorage.getItem('token')
    if (!token) return
    
    const response = await fetch('http://localhost:5000/api/smart-attendance/statistics', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (!response.ok) {
      console.warn('获取统计信息HTTP错误:', response.status)
      return
    }
    
    const result = await response.json()
    if (result.code === 200) {
      statistics.value = result.data
      console.log('✅ 统计信息加载成功')
    }
  } catch (error) {
    console.warn('获取统计信息失败:', error.message)
  }
}

const openAddFaceDialog = (student) => {
  selectedStudent.value = student
  showAddFaceDialog.value = true
  selectedFaceFile.value = null
  facePreviewUrl.value = ''
}

const triggerFaceFileInput = () => {
  faceFileInput.value?.click()
}

const handleFaceFileSelect = (event) => {
  const file = event.target.files?.[0]
  if (file) {
    selectedFaceFile.value = file
    facePreviewUrl.value = URL.createObjectURL(file)
  }
}

const submitAddFace = async () => {
  if (!selectedFaceFile.value || !selectedStudent.value) return
  
  addingFace.value = true
  
  try {
    const formData = new FormData()
    formData.append('file', selectedFaceFile.value)
    formData.append('student_id', selectedStudent.value.id)
    formData.append('student_name', selectedStudent.value.fullname)
    
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/smart-attendance/add-student-face', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })
    
    const result = await response.json()
    
    if (result.code === 200) {
      ElMessage.success('人脸已添加')
      showAddFaceDialog.value = false
      // 重新加载该学生的人脸照片
      await loadStudentFaces(selectedStudent.value.id)
    } else {
      ElMessage.error(result.message || '添加失败')
    }
  } catch (error) {
    ElMessage.error('添加失败: ' + error.message)
  } finally {
    addingFace.value = false
  }
}

const loadStudentFaces = async (studentId) => {
  try {
    const token = localStorage.getItem('token')
    if (!token) return
    
    facesLoadingStatus.value[studentId] = 'loading'
    
    const response = await fetch(`http://localhost:5000/api/smart-attendance/student-faces/${studentId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    
    if (response.ok) {
      const result = await response.json()
      if (result.code === 200) {
        studentFaces.value[studentId] = result.data
        // 初始化每张图片的加载状态
        result.data.forEach((_, index) => {
          const imageKey = `${studentId}-${index}`
          imageLoadStatus.value[imageKey] = 'loading'
        })
        facesLoadingStatus.value[studentId] = 'success'
      }
    } else {
      facesLoadingStatus.value[studentId] = 'error'
    }
  } catch (error) {
    console.warn(`加载学生 ${studentId} 的人脸照片失败:`, error.message)
    facesLoadingStatus.value[studentId] = 'error'
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const getStatusLabel = (status) => {
  const labels = {
    'present': '出席',
    'absent': '缺席',
    'late': '迟到'
  }
  return labels[status] || status
}

onMounted(() => {
  loadStudents()
  fetchAttendanceRecords()
  fetchStatistics()
})
</script>

<style scoped>
.smart-attendance-container {
  padding: 0;
}

.panel-header {
  margin-bottom: 2rem;
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

/* Tab 导航 */
.tab-nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  border-bottom: 2px solid #e8eef5;
}

.tab-item {
  padding: 1rem 1.5rem;
  cursor: pointer;
  color: #666;
  font-weight: 500;
  position: relative;
  transition: all 0.3s ease;
}

.tab-item:hover {
  color: #4A90E2;
}

.tab-item.active {
  color: #4A90E2;
}

.tab-item.active::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: #4A90E2;
}

/* Tab 内容 */
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

/* 卡片 */
.card {
  background: white;
  border: 1px solid #e8eef5;
  border-radius: 8px;
  padding: 2rem;
  margin-bottom: 2rem;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 1.5rem;
}

.desc-text {
  color: #666;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

/* 上传区域 */
.upload-area {
  border: 2px dashed #b3d8f2;
  border-radius: 8px;
  padding: 3rem 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: #f5f9ff;
  margin-bottom: 1.5rem;
}

.upload-area:hover,
.upload-area.dragover {
  border-color: #4A90E2;
  background: #e6f2ff;
}

.upload-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.upload-text {
  font-size: 1rem;
  color: #333;
  margin: 0.5rem 0;
  font-weight: 500;
}

.upload-hint {
  color: #999;
  font-size: 0.9rem;
  margin: 0;
}

.upload-progress {
  margin-bottom: 1.5rem;
}

.progress-bar {
  height: 8px;
  background: #e8eef5;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4A90E2, #a8d4e8);
  transition: width 0.3s ease;
}

.image-preview {
  text-align: center;
  margin-bottom: 1.5rem;
}

.image-preview img {
  max-width: 100%;
  max-height: 400px;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.button-group {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.upload-area-small {
  border: 2px dashed #b3d8f2;
  border-radius: 8px;
  padding: 2rem 1rem;
  text-align: center;
  cursor: pointer;
  background: #f5f9ff;
  margin-bottom: 1rem;
}

.upload-area-small:hover {
  border-color: #4A90E2;
  background: #e6f2ff;
}

.face-preview {
  margin-bottom: 1rem;
}

.face-preview img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
}

/* 统计卡片 */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #f5f9ff 0%, #e6f2ff 100%);
  border: 1px solid #d0e8f2;
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

/* 学生列表 */
.recognition-results {
  background: #f9fafb;
}

.result-images {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.image-section {
  text-align: center;
}

.image-section h4 {
  color: #333;
  font-size: 1rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.result-image {
  max-width: 100%;
  max-height: 350px;
  border-radius: 8px;
  border: 1px solid #e8eef5;
  box-shadow: 0 2px 8px rgba(74, 144, 226, 0.1);
}

.students-list {
  margin-bottom: 2rem;
}

.students-list h4 {
  color: #333;
  margin-bottom: 1rem;
}

.student-card {
  background: white;
  border: 1px solid #e8eef5;
  border-radius: 6px;
  padding: 1rem;
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.student-info {
  flex: 1;
}

.student-name {
  font-weight: 600;
  color: #333;
}

.student-id {
  font-size: 0.85rem;
  color: #999;
  margin-top: 0.3rem;
}

.confidence-badge {
  background: linear-gradient(135deg, #a8d4e8 0%, #7ec8e3 100%);
  color: white;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
}

.result-image {
  margin-bottom: 2rem;
}

.result-image h4 {
  color: #333;
  margin-bottom: 1rem;
}

.result-image img {
  max-width: 100%;
  border-radius: 8px;
}

/* 学生网格 */
.students-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.student-item {
  background: linear-gradient(135deg, #f5f9ff 0%, #e6f2ff 100%);
  border: 1px solid #d0e8f2;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.face-gallery {
  width: 100%;
  margin: 0.5rem 0;
}

.face-thumbnails {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 0.5rem;
}

.face-thumbnail-wrapper {
  position: relative;
  width: 60px;
  height: 60px;
}

/* 骨架屏加载动画 */
.face-thumbnail-skeleton {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 6px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s infinite;
  border: 2px solid #d0d0d0;
}

.skeleton-pulse {
  width: 100%;
  height: 100%;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.face-thumbnail {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 6px;
  border: 2px solid #4A90E2;
  transition: transform 0.3s ease;
}

.face-thumbnail:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 8px rgba(74, 144, 226, 0.3);
}

/* 删除按鍧 */
.face-delete-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  width: 24px;
  height: 24px;
  background: #ff4d4f;
  border: none;
  border-radius: 50%;
  color: white;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.face-delete-btn:hover {
  background: #ff7875;
  transform: scale(1.2);
  box-shadow: 0 4px 8px rgba(255, 77, 79, 0.3);
}

.face-delete-btn:active {
  transform: scale(0.95);
}

/* 图片加载失败提示 */
.face-thumbnail-error {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 6px;
  border: 2px solid #ff7875;
  background: rgba(255, 200, 200, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  color: #d9534f;
  text-align: center;
  padding: 0.25rem;
}

/* 人脸照片加载中 */
.faces-loading {
  width: 100%;
  padding: 1rem;
  text-align: center;
  background: rgba(135, 206, 235, 0.05);
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.loading-spinner {
  width: 30px;
  height: 30px;
  border: 3px solid rgba(74, 144, 226, 0.2);
  border-top-color: #4A90E2;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
  margin: 0 auto 0.5rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.faces-loading p {
  margin: 0;
  color: #4A90E2;
  font-size: 0.9rem;
  font-weight: 500;
}

/* 加载失败 */
.faces-error {
  width: 100%;
  padding: 0.8rem;
  background: rgba(255, 200, 200, 0.1);
  border: 1px solid #ffcccc;
  border-radius: 8px;
  margin-bottom: 0.5rem;
}

.faces-error p {
  margin: 0;
  color: #d9534f;
  font-size: 0.9rem;
}

.face-count {
  font-size: 0.85rem;
  color: #4A90E2;
  margin: 0;
  font-weight: 500;
}

.no-faces {
  width: 100%;
  padding: 0.5rem;
}

.no-faces p {
  font-size: 0.85rem;
  color: #999;
  margin: 0;
}

.student-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #4A90E2;
  display: flex;
  align-items: center;
  justify-content: center;
}

.avatar-placeholder {
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
}

.student-details h4 {
  margin: 0;
  color: #333;
  font-size: 1rem;
}

.student-details p {
  margin: 0.3rem 0 0 0;
  color: #999;
  font-size: 0.9rem;
}

/* 记录表格 */
.records-table {
  overflow-x: auto;
}

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

.status-badge {
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 3px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-present {
  background: #d4edda;
  color: #155724;
}

.status-absent {
  background: #f8d7da;
  color: #721c24;
}

.status-late {
  background: #fff3cd;
  color: #856404;
}

/* 按钮 */
.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.btn-primary,
.btn-secondary,
.btn-upload {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #a8d4e8 0%, #7ec8e3 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
}

.btn-secondary:hover {
  background: #e0e0e0;
}

.btn-upload {
  background: linear-gradient(135deg, #a8d4e8 0%, #7ec8e3 100%);
  color: white;
  padding: 0.5rem 1rem;
  font-size: 0.9rem;
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

.modal-dialog {
  background: white;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  width: 90%;
  max-width: 400px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e8eef5;
}

.modal-header h3 {
  margin: 0;
  color: #333;
  font-size: 1.1rem;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
}

.modal-close:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e8eef5;
}

.modal-footer .btn-primary,
.modal-footer .btn-secondary {
  flex: 1;
  text-align: center;
}
</style>
