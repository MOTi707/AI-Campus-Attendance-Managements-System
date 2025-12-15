<template>
  <div class="grades-container">

    <!-- 功能卡片导航 -->
    <div class="function-cards">
      <div
        v-for="func in functions"
        :key="func.id"
        :class="['function-card', { active: activeTab === func.id }]"
        @click="activeTab = func.id"
      >
        <div class="card-icon">{{ func.icon }}</div>
        <h3>{{ func.name }}</h3>
        <p>{{ func.description }}</p>
      </div>
    </div>

    <!-- 选项卡内容 -->
    <div class="tab-content">
      <!-- 1. 单条录入 -->
      <div v-if="activeTab === 'add'" class="tab-pane">
        <div class="card">
          <h3 class="card-title">📝 单条成绩录入</h3>
          
          <form class="form-grid">
            <div class="form-group">
              <label>学生</label>
              <select v-model="form.student_id" class="form-control">
                <option value="">请选择学生</option>
                <option v-for="student in students" :key="student.id" :value="student.id">
                  {{ student.name }} ({{ student.username }})
                </option>
              </select>
            </div>

            <div class="form-group">
              <label>科目</label>
              <input v-model="form.subject" type="text" class="form-control" placeholder="输入科目名称">
            </div>

            <div class="form-group">
              <label>成绩</label>
              <input v-model.number="form.score" type="number" class="form-control" placeholder="输入成绩">
            </div>

            <div class="form-group">
              <label>满分</label>
              <input v-model.number="form.full_score" type="number" class="form-control" placeholder="默认100">
            </div>

            <div class="form-group">
              <label>考试日期</label>
              <input v-model="form.exam_date" type="date" class="form-control">
            </div>

            <div class="form-group">
              <label>考试次数</label>
              <input v-model.number="form.exam_number" type="number" class="form-control" placeholder="默认1">
            </div>
          </form>

          <div class="form-group full-width">
            <label>备注</label>
            <textarea v-model="form.notes" class="form-control" placeholder="输入备注信息"></textarea>
          </div>

          <div class="form-actions">
            <button class="btn btn-primary" @click="submitAddScore">
              📤 录入成绩
            </button>
            <button class="btn btn-secondary" @click="resetForm">
              🔄 重置表单
            </button>
          </div>
        </div>
      </div>

      <!-- 2. 批量导入 -->
      <div v-if="activeTab === 'import'" class="tab-pane">
        <div class="card">
          <h3 class="card-title">📊 批量导入成绩</h3>
          
          <div class="upload-section">
            <div class="template-download">
              <span>📥 首先下载Excel导入模板</span>
              <button class="btn btn-outline" @click="downloadTemplate">
                下载模板
              </button>
            </div>

            <div class="upload-area">
              <input
                ref="fileInput"
                type="file"
                class="file-input"
                accept=".xlsx,.xls"
                @change="handleFileSelect"
              >
              <div class="upload-prompt">
                <div class="upload-icon">📤</div>
                <p>点击选择或拖拽上传 Excel 文件</p>
                <span class="upload-hint">支持 .xlsx 和 .xls 格式，最大 10MB</span>
              </div>
            </div>

            <div v-if="selectedFile" class="file-info">
              <p><strong>文件：</strong> {{ selectedFile.name }}</p>
              <p><strong>大小：</strong> {{ formatFileSize(selectedFile.size) }}</p>
            </div>
          </div>

          <div class="form-actions">
            <button
              class="btn btn-primary"
              @click="submitImport"
              :disabled="!selectedFile || isImporting"
            >
              {{ isImporting ? '导入中...' : '📥 导入成绩' }}
            </button>
            <button class="btn btn-secondary" @click="resetImport">
              🔄 清除文件
            </button>
          </div>

          <!-- 导入结果 -->
          <div v-if="importResult" class="import-result">
            <h4>导入结果</h4>
            <div class="result-box" :class="{ 'success': importResult.imported > 0 }">
              <p>✅ 成功导入: <strong>{{ importResult.imported }}</strong> 条</p>
              <p v-if="importResult.error_count > 0">
                ❌ 失败: <strong>{{ importResult.error_count }}</strong> 条
              </p>
            </div>

            <div v-if="importResult.errors && importResult.errors.length > 0" class="error-list">
              <h5>错误详情:</h5>
              <ul>
                <li v-for="(error, idx) in importResult.errors" :key="idx">
                  {{ error }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- 3. 成绩查询 -->
      <div v-if="activeTab === 'query'" class="tab-pane">
        <div class="card">
          <h3 class="card-title">📋 成绩查询</h3>

          <div class="filter-bar">
            <div class="filter-group">
              <label>学生:</label>
              <select v-model="filters.student_id" class="form-control" @change="fetchScores">
                <option value="">全部学生</option>
                <option v-for="student in students" :key="student.id" :value="student.id">
                  {{ student.name }}
                </option>
              </select>
            </div>

            <div class="filter-group">
              <label>科目:</label>
              <select v-model="filters.subject" class="form-control" @change="fetchScores">
                <option value="">全部科目</option>
                <option v-for="subject in subjects" :key="subject" :value="subject">
                  {{ subject }}
                </option>
              </select>
            </div>
          </div>

          <div v-if="scores.length === 0" class="empty-state">
            <div class="empty-icon">📭</div>
            <p>暂无成绩记录</p>
          </div>

          <div v-else class="scores-table">
            <table>
              <thead>
                <tr>
                  <th>学生</th>
                  <th>科目</th>
                  <th>成绩</th>
                  <th>满分</th>
                  <th>百分比</th>
                  <th>考试日期</th>
                  <th>操作</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="score in scores" :key="score.id">
                  <td>{{ getStudentName(score.student_id) }}</td>
                  <td>{{ score.subject }}</td>
                  <td class="score-cell" :class="getScoreClass(score.score)">
                    {{ score.score }}
                  </td>
                  <td>{{ score.full_score }}</td>
                  <td>{{ ((score.score / score.full_score) * 100).toFixed(1) }}%</td>
                  <td>{{ formatDate(score.exam_date) }}</td>
                  <td>
                    <button class="btn-action edit" @click="editScore(score)" title="编辑">✏️</button>
                    <button class="btn-action delete" @click="deleteScore(score.id)" title="删除">🗑️</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- 4. 统计分析 -->
      <div v-if="activeTab === 'analysis'" class="tab-pane">
        <div class="card">
          <h3 class="card-title">📊 统计分析</h3>

          <div class="filter-bar">
            <div class="filter-group">
              <label>科目:</label>
              <select v-model="analysisFilters.subject" class="form-control" @change="fetchStatistics">
                <option value="">全部科目</option>
                <option v-for="subject in subjects" :key="subject" :value="subject">
                  {{ subject }}
                </option>
              </select>
            </div>

            <div class="filter-group">
              <label>学生:</label>
              <select v-model="analysisFilters.student_id" class="form-control" @change="fetchStatistics">
                <option value="">全部学生</option>
                <option v-for="student in students" :key="student.id" :value="student.id">
                  {{ student.name }}
                </option>
              </select>
            </div>
          </div>

          <!-- 统计数据卡片 -->
          <div class="stats-cards">
            <div class="stat-card">
              <div class="stat-label">总数</div>
              <div class="stat-value">{{ statistics.count }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">平均分</div>
              <div class="stat-value">{{ statistics.average }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">最高分</div>
              <div class="stat-value">{{ statistics.max }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">最低分</div>
              <div class="stat-value">{{ statistics.min }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">标准差</div>
              <div class="stat-value">{{ statistics.std_dev }}</div>
            </div>
            <div class="stat-card">
              <div class="stat-label">中位数</div>
              <div class="stat-value">{{ statistics.median }}</div>
            </div>
          </div>

          <!-- 分数段分布 -->
          <div class="charts-container">
            <!-- 1. 分数段分布柱状图 -->
            <div class="chart-box">
              <h4>📊 分数段分布</h4>
              <div class="distribution-chart">
                <div
                  v-for="(count, grade) in statistics.distribution"
                  :key="grade"
                  class="distribution-item"
                >
                  <div class="grade-label">{{ grade }}</div>
                  <div class="bar-container">
                    <div
                      class="bar"
                      :style="{ width: (count / Math.max(...Object.values(statistics.distribution || {})) || 1) * 100 + '%' }"
                      :class="getGradeColor(grade)"
                    ></div>
                  </div>
                  <div class="count">{{ count }}</div>
                </div>
              </div>
            </div>

            <!-- 2. 成绩等级占比饼图 -->
            <div class="chart-box">
              <h4>🥧 成绩等级占比</h4>
              <div class="grade-pie">
                <div
                  v-for="(count, grade) in statistics.distribution"
                  :key="grade"
                  class="pie-item"
                  :style="{ flex: count > 0 ? count : 0.1 }"
                  :class="getGradeColor(grade)"
                  :title="`${grade}: ${count}人 (${calculatePercentage(count)}%)`"
                ></div>
              </div>
              <div class="pie-legend">
                <div v-for="(count, grade) in statistics.distribution" :key="grade" class="legend-item">
                  <span :class="['color', getGradeColor(grade)]"></span>
                  <span>{{ grade }}: {{ count }}人 ({{ calculatePercentage(count) }}%)</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 更多图表 -->
          <div class="charts-container-2">
          
            <!-- 5. 成绩进步预测趋势图 -->
            <div class="chart-box full-width">
              <h4>🚀 成绩进步预测（对全体学生整体分析和预测）</h4>
              <div class="algorithm-info">
                <div class="algo-badge">🔍 算法: 线性回归 (Linear Regression Forecast)</div>
                <p class="algo-description"><strong>原理:</strong> 根据学生的历史成绩数据, 计算成绩变化趋势, 预测未来成绩。</p>
                <p class="algo-description"><strong>公式:</strong> Future Score = Avg Score + Slope Value * Time Periods</p>
                <p class="algo-description"><strong>计算步骤:</strong>
                  <br> 1. 统计当前的成绩均值、最高分、最低分、中位数
                  <br> 2. 计算成绩变化趋势 (最高分 - 最低分) / 考试次数
                  <br> 3. 根据优秀、良好次数比例预测成绩优化趋势
                  <br> 4. 显示实际成绩与预测趋势对比
                </p>
              </div>
              <div class="progress-trend">
                <div class="trend-chart">
                  <!-- 模拟折线图 -->
                  <svg width="100%" height="280" class="trend-svg" viewBox="0 0 600 280">
                    <!-- 网格线 -->
                    <line x1="60" y1="220" x2="560" y2="220" stroke="#e8eef5" stroke-width="1"/>
                    <line x1="60" y1="180" x2="560" y2="180" stroke="#e8eef5" stroke-width="1"/>
                    <line x1="60" y1="140" x2="560" y2="140" stroke="#e8eef5" stroke-width="1"/>
                    <line x1="60" y1="100" x2="560" y2="100" stroke="#e8eef5" stroke-width="1"/>
                    <line x1="60" y1="60" x2="560" y2="60" stroke="#e8eef5" stroke-width="1"/>
                    <line x1="60" y1="20" x2="560" y2="20" stroke="#e8eef5" stroke-width="1"/>
                    
                    <!-- 竖轴 (Y轴) -->
                    <line x1="60" y1="20" x2="60" y2="240" stroke="#333" stroke-width="2"/>
                    <!-- Y轴刻度 -->
                    <text x="45" y="25" fill="#666" font-size="12" text-anchor="end">100</text>
                    <text x="45" y="65" fill="#666" font-size="12" text-anchor="end">90</text>
                    <text x="45" y="105" fill="#666" font-size="12" text-anchor="end">80</text>
                    <text x="45" y="145" fill="#666" font-size="12" text-anchor="end">70</text>
                    <text x="45" y="185" fill="#666" font-size="12" text-anchor="end">60</text>
                    <text x="45" y="225" fill="#666" font-size="12" text-anchor="end">50</text>
                    <!-- Y轴标签 -->
                    <text x="15" y="130" fill="#333" font-size="14" font-weight="600" text-anchor="middle" transform="rotate(-90, 15, 130)">成绩（分）</text>
                    
                    <!-- 横轴 (X轴) -->
                    <line x1="60" y1="240" x2="560" y2="240" stroke="#333" stroke-width="2"/>
                    <!-- X轴刻度 -->
                    <text x="110" y="255" fill="#666" font-size="12" text-anchor="middle">第1次</text>
                    <text x="210" y="255" fill="#666" font-size="12" text-anchor="middle">第2次</text>
                    <text x="310" y="255" fill="#666" font-size="12" text-anchor="middle">第3次</text>
                    <text x="410" y="255" fill="#666" font-size="12" text-anchor="middle">第4次</text>
                    <text x="510" y="255" fill="#666" font-size="12" text-anchor="middle">第5次</text>
                    <!-- X轴标签 -->
                    <text x="310" y="275" fill="#333" font-size="14" font-weight="600" text-anchor="middle">考试次数</text>
                    
                    <!-- 当前趋势线 -->
                    <polyline
                      points="110,200 210,180 310,150 410,130 510,110"
                      fill="none"
                      stroke="#4A90E2"
                      stroke-width="3"
                    />
                    <!-- 预测趋势线 -->
                    <polyline
                      points="510,110 560,95"
                      fill="none"
                      stroke="#52c41a"
                      stroke-width="3"
                      stroke-dasharray="8,5"
                    />
                    <!-- 数据点 -->
                    <circle cx="110" cy="200" r="5" fill="#4A90E2" />
                    <circle cx="210" cy="180" r="5" fill="#4A90E2" />
                    <circle cx="310" cy="150" r="5" fill="#4A90E2" />
                    <circle cx="410" cy="130" r="5" fill="#4A90E2" />
                    <circle cx="510" cy="110" r="5" fill="#4A90E2" />
                    <circle cx="560" cy="95" r="5" fill="#52c41a" />
                    
                    <!-- 数据标签 -->
                    <text x="110" y="195" fill="#4A90E2" font-size="11" text-anchor="middle" font-weight="600">65</text>
                    <text x="210" y="175" fill="#4A90E2" font-size="11" text-anchor="middle" font-weight="600">70</text>
                    <text x="310" y="145" fill="#4A90E2" font-size="11" text-anchor="middle" font-weight="600">78</text>
                    <text x="410" y="125" fill="#4A90E2" font-size="11" text-anchor="middle" font-weight="600">82</text>
                    <text x="510" y="105" fill="#4A90E2" font-size="11" text-anchor="middle" font-weight="600">88</text>
                    <text x="560" y="90" fill="#52c41a" font-size="11" text-anchor="middle" font-weight="600">92</text>
                  </svg>
                </div>
                <div class="trend-legend">
                  <div class="legend-item">
                    <span class="legend-color" style="background: #4A90E2;"></span>
                    <span>实际成绩</span>
                  </div>
                  <div class="legend-item">
                    <span class="legend-color" style="background: #52c41a; border: 2px dashed #52c41a; background: transparent;"></span>
                    <span>预测进步趋势</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 5. 学生汇总 -->
      <div v-if="activeTab === 'summary'" class="tab-pane">
        <div class="card">
          <h3 class="card-title">👥 学生成绩汇总</h3>

          <div class="student-list">
            <div
              v-for="student in students"
              :key="student.id"
              class="student-card"
              @click="viewStudentSummary(student.id)"
              style="cursor: pointer;"
            >
              <div class="student-name">{{ student.name }}</div>
              <div class="student-id">{{ student.username }}</div>
              <div class="summary-badge">查看详情 →</div>
            </div>
          </div>

          <!-- 学生详细汇总母窗 -->
          <div v-if="selectedStudentSummary" class="glass-modal-overlay" @click="selectedStudentSummary = null">
            <div class="glass-modal-content" @click.stop>
              <div class="glass-modal-header">
                <h4>{{ selectedStudentSummary.student.name }} 的成绩汇总</h4>
                <button class="glass-close-btn" @click="selectedStudentSummary = null">×</button>
              </div>

              <div class="glass-modal-body">
                <!-- 总体统计 -->
                <div class="overall-stats">
                  <div class="stat-item">
                    <span class="label">总成绩数:</span>
                    <span class="value">{{ selectedStudentSummary.overall.total_count }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="label">总体平均分:</span>
                    <span class="value">{{ selectedStudentSummary.overall.average }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="label">最高分:</span>
                    <span class="value">{{ selectedStudentSummary.overall.max }}</span>
                  </div>
                  <div class="stat-item">
                    <span class="label">最低分:</span>
                    <span class="value">{{ selectedStudentSummary.overall.min }}</span>
                  </div>
                </div>

                <!-- 科目详情 -->
                <div class="subjects-grid">
                  <div v-for="subject in selectedStudentSummary.subjects" :key="subject.subject" class="subject-card">
                    <h5>{{ subject.subject }}</h5>
                    <div class="subject-stats">
                      <div class="stat">
                        <span>次数: {{ subject.count }}</span>
                      </div>
                      <div class="stat">
                        <span>平均: {{ subject.average }}</span>
                      </div>
                      <div class="stat">
                        <span>最高: {{ subject.max }}</span>
                      </div>
                      <div class="stat">
                        <span>最低: {{ subject.min }}</span>
                      </div>
                    </div>
                    <div class="score-progression">
                      <span v-for="(score, idx) in subject.scores" :key="idx" class="score-badge">
                        {{ score }}
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 编辑成绩弹窗 -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="showEditModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>编辑成绩</h3>
          <button class="close-btn" @click="showEditModal = false">×</button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>成绩</label>
            <input v-model.number="editingScore.score" type="number" class="form-control">
          </div>
          <div class="form-group">
            <label>满分</label>
            <input v-model.number="editingScore.full_score" type="number" class="form-control">
          </div>
          <div class="form-group">
            <label>科目</label>
            <input v-model="editingScore.subject" type="text" class="form-control">
          </div>
          <div class="form-group">
            <label>考试日期</label>
            <input v-model="editingScore.exam_date" type="date" class="form-control">
          </div>
          <div class="form-group">
            <label>备注</label>
            <textarea v-model="editingScore.notes" class="form-control"></textarea>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn btn-secondary" @click="showEditModal = false">取消</button>
          <button class="btn btn-primary" @click="submitEditScore">保存修改</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { ElMessage } from 'element-plus'

// 状态
const activeTab = ref('add')
const students = ref([])
const subjects = ref([])
const scores = ref([])
const statistics = ref({
  count: 0,
  average: 0,
  max: 0,
  min: 0,
  std_dev: 0,
  median: 0,
  distribution: {}
})

// 表单数据
const form = ref({
  student_id: '',
  subject: '',
  score: null,
  full_score: 100,
  exam_date: new Date().toISOString().split('T')[0],
  exam_number: 1,
  notes: ''
})

const filters = ref({
  student_id: '',
  subject: ''
})

const analysisFilters = ref({
  subject: '',
  student_id: ''
})

// 上传文件
const fileInput = ref(null)
const selectedFile = ref(null)
const isImporting = ref(false)
const importResult = ref(null)

// 编辑模式
const showEditModal = ref(false)
const editingScore = ref({})

// 学生汇总
const selectedStudentSummary = ref(null)

// 功能卡片
const functions = [
  {
    id: 'add',
    name: '单条录入',
    icon: '📝',
    description: '逐条录入学生成绩'
  },
  {
    id: 'import',
    name: '批量导入',
    icon: '📊',
    description: '使用Excel导入多条成绩'
  },
  {
    id: 'query',
    name: '成绩查询',
    icon: '📋',
    description: '查询和管理成绩'
  },
  {
    id: 'analysis',
    name: '统计分析',
    icon: '📈',
    description: '成绩数据分析和可视化'
  },
  {
    id: 'summary',
    name: '学生汇总',
    icon: '👥',
    description: '查看学生成绩汇总'
  }
]

// 初始化
onMounted(() => {
  fetchStudents()
  fetchSubjects()
  fetchScores()
  fetchStatistics()
})

// 获取学生列表
const fetchStudents = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/grades/students', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.code === 200) {
      students.value = data.data
    }
  } catch (error) {
    console.error('获取学生列表失败:', error)
  }
}

// 获取科目列表
const fetchSubjects = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/grades/subjects', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.code === 200) {
      subjects.value = data.data
    }
  } catch (error) {
    console.error('获取科目列表失败:', error)
  }
}

// 获取成绩列表
const fetchScores = async () => {
  try {
    const token = localStorage.getItem('token')
    let url = 'http://localhost:5000/api/grades/list'
    const params = new URLSearchParams()
    if (filters.value.student_id) params.append('student_id', filters.value.student_id)
    if (filters.value.subject) params.append('subject', filters.value.subject)
    if (params.toString()) url += '?' + params.toString()

    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.code === 200) {
      scores.value = data.data.scores
    }
  } catch (error) {
    console.error('获取成绩列表失败:', error)
  }
}

// 获取统计数据
const fetchStatistics = async () => {
  try {
    const token = localStorage.getItem('token')
    let url = 'http://localhost:5000/api/grades/statistics'
    const params = new URLSearchParams()
    if (analysisFilters.value.subject) params.append('subject', analysisFilters.value.subject)
    if (analysisFilters.value.student_id) params.append('student_id', analysisFilters.value.student_id)
    if (params.toString()) url += '?' + params.toString()

    const response = await fetch(url, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    const data = await response.json()
    if (data.code === 200) {
      statistics.value = data.data
    }
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 提交添加成绩
const submitAddScore = async () => {
  if (!form.value.student_id || !form.value.subject || !form.value.score) {
    ElMessage.error('请填写必填字段')
    return
  }

  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/grades/add', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form.value)
    })

    const data = await response.json()
    if (data.code === 200 || data.code === 201) {
      ElMessage.success('成绩录入成功')
      resetForm()
      fetchScores()
      fetchStatistics()
      fetchSubjects()
    } else {
      ElMessage.error(data.message || '录入失败')
    }
  } catch (error) {
    ElMessage.error('录入出错: ' + error)
  }
}

// 重置表单
const resetForm = () => {
  form.value = {
    student_id: '',
    subject: '',
    score: null,
    full_score: 100,
    exam_date: new Date().toISOString().split('T')[0],
    exam_number: 1,
    notes: ''
  }
}

// 下载模板
const downloadTemplate = async () => {
  try {
    const response = await fetch('http://localhost:5000/api/grades/template/download')
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = '成绩导入模板.xlsx'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (error) {
    ElMessage.error('下载模板失败')
  }
}

// 处理文件选择
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 10 * 1024 * 1024) {
      ElMessage.error('文件过大，最大支持10MB')
      return
    }
    selectedFile.value = file
  }
}

// 提交导入
const submitImport = async () => {
  if (!selectedFile.value) {
    ElMessage.error('请选择文件')
    return
  }

  isImporting.value = true
  const formData = new FormData()
  formData.append('file', selectedFile.value)

  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/grades/import', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
      body: formData
    })

    const data = await response.json()
    importResult.value = data.data
    if (data.code === 200) {
      ElMessage.success('导入成功')
      fetchScores()
      fetchStatistics()
      fetchSubjects()
    } else {
      ElMessage.error(data.message || '导入失败')
    }
  } catch (error) {
    ElMessage.error('导入出错: ' + error)
  } finally {
    isImporting.value = false
  }
}

// 重置导入
const resetImport = () => {
  selectedFile.value = null
  importResult.value = null
  if (fileInput.value) fileInput.value.value = ''
}

// 获取学生名称
const getStudentName = (studentId) => {
  const student = students.value.find(s => s.id === studentId)
  return student ? student.name : '未知'
}

// 编辑成绩
const editScore = (score) => {
  editingScore.value = { ...score }
  showEditModal.value = true
}

// 提交编辑
const submitEditScore = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/grades/${editingScore.value.id}`, {
      method: 'PUT',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(editingScore.value)
    })

    const data = await response.json()
    if (data.code === 200) {
      ElMessage.success('更新成功')
      showEditModal.value = false
      fetchScores()
      fetchStatistics()
    } else {
      ElMessage.error(data.message || '更新失败')
    }
  } catch (error) {
    ElMessage.error('更新出错: ' + error)
  }
}

// 删除成绩
const deleteScore = async (scoreId) => {
  if (!confirm('确定要删除这条成绩记录吗？')) return

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/grades/${scoreId}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` }
    })

    const data = await response.json()
    if (data.code === 200) {
      ElMessage.success('删除成功')
      fetchScores()
      fetchStatistics()
    } else {
      ElMessage.error(data.message || '删除失败')
    }
  } catch (error) {
    ElMessage.error('删除出错: ' + error)
  }
}

// 查看学生汇总
const viewStudentSummary = async (studentId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/grades/student/${studentId}/summary`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })

    const data = await response.json()
    if (data.code === 200) {
      selectedStudentSummary.value = data.data
    } else {
      ElMessage.error(data.message || '获取失败')
    }
  } catch (error) {
    ElMessage.error('获取失败: ' + error)
  }
}

// 工具函数
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i]
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN')
}

const getScoreClass = (score) => {
  if (score >= 90) return 'excellent'
  if (score >= 80) return 'good'
  if (score >= 70) return 'average'
  if (score >= 60) return 'pass'
  return 'fail'
}

const getGradeColor = (grade) => {
  if (grade.includes('90-100')) return 'grade-a'
  if (grade.includes('80-89')) return 'grade-b'
  if (grade.includes('70-79')) return 'grade-c'
  if (grade.includes('60-69')) return 'grade-d'
  return 'grade-f'
}

// 计算百分比
const calculatePercentage = (count) => {
  const total = getTotalCount()
  return total > 0 ? Math.round((count / total) * 100) : 0
}

// 计算总数量
const getTotalCount = () => {
  return Object.values(statistics.value.distribution || {}).reduce((a, b) => a + b, 0)
}

// 计算及格率
const calculatePassRate = () => {
  const passCount = ['90-100', '80-89', '70-79', '60-69'].reduce((sum, grade) => {
    return sum + (statistics.value.distribution[grade] || 0)
  }, 0)
  const total = Object.values(statistics.value.distribution || {}).reduce((a, b) => a + b, 0)
  return total > 0 ? Math.round((passCount / total) * 100) : 0
}

// 获取特定分数段的人数
const getDistributionCount = (grade) => {
  return statistics.value.distribution?.[grade] || 0
}

// 生成牳状图段
const generateDonutSegments = () => {
  const total = Object.values(statistics.value.distribution || {}).reduce((a, b) => a + b, 0)
  if (total === 0) return []
  
  const colors = ['#ff4d4f', '#f5222d', '#fa8c16', '#faad14', '#52c41a']
  const grades = ['90-100', '80-89', '70-79', '60-69', '0-59']
  const segments = []
  let offset = 0
  
  grades.forEach((grade, idx) => {
    const count = statistics.value.distribution?.[grade] || 0
    const ratio = total > 0 ? count / total : 0
    const circumference = 2 * Math.PI * 80
    const dashArray = circumference * ratio
    segments.push({
      color: colors[idx],
      dashArray: dashArray + ',' + circumference,
      offset: -offset
    })
    offset += dashArray
  })
  
  return segments
}
</script>

<style scoped>
.grades-container {
  width: 100%;
  padding: 0;
  background: transparent;
  min-height: 100%;
}

.grades-header {
  display: none;
}

/* 功能卡片导航 */
.function-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
  max-width: 100%;
  margin-left: auto;
  margin-right: auto;
}

.function-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  border: 2px solid transparent;
}

.function-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(74, 144, 226, 0.15);
}

.function-card.active {
  border-color: #4A90E2;
  background: rgba(74, 144, 226, 0.05);
}

.card-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.function-card h3 {
  margin: 0.5rem 0;
  color: #333;
  font-size: 1rem;
}

.function-card p {
  margin: 0;
  color: #999;
  font-size: 0.85rem;
}

/* 选项卡内容 */
.tab-content {
  max-width: 100%;
  margin: 0;
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

.card {
  background: transparent;
  border-radius: 0;
  padding: 0;
  box-shadow: none;
  margin-bottom: 1rem;
}

.card-title {
  font-size: 1.3rem;
  color: #333;
  margin: 0 0 1.5rem 0;
  padding-bottom: 1rem;
  border-bottom: 2px solid #4A90E2;
}

/* 表单 */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 0.95rem;
}

.form-control {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.2s ease;
}

.form-control:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

textarea.form-control {
  min-height: 100px;
  resize: vertical;
}

/* 按钮 */
.form-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-top: 2rem;
}

.btn {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.btn-secondary {
  background: #f0f0f0;
  color: #333;
  border: 1px solid #ddd;
}

.btn-secondary:hover {
  background: #e8e8e8;
}

.btn-outline {
  background: white;
  color: #4A90E2;
  border: 2px solid #4A90E2;
}

.btn-outline:hover {
  background: #f0f8ff;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 上传区域 */
.upload-section {
  margin-bottom: 2rem;
}

.template-download {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: #f0f8ff;
  border-radius: 6px;
  margin-bottom: 1.5rem;
}

.upload-area {
  position: relative;
  margin-bottom: 1.5rem;
}

.file-input {
  position: absolute;
  opacity: 0;
  width: 100%;
  height: 100%;
  cursor: pointer;
}

.upload-prompt {
  border: 2px dashed #4A90E2;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  background: rgba(74, 144, 226, 0.05);
  cursor: pointer;
  transition: all 0.2s ease;
}

.upload-prompt:hover {
  background: rgba(74, 144, 226, 0.1);
  border-color: #357ABD;
}

.upload-icon {
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

.upload-prompt p {
  margin: 0.5rem 0 0 0;
  color: #333;
  font-weight: 500;
}

.upload-hint {
  display: block;
  margin-top: 0.5rem;
  color: #999;
  font-size: 0.85rem;
}

.file-info {
  padding: 1rem;
  background: #f5f5f5;
  border-radius: 6px;
  margin-bottom: 1rem;
}

.file-info p {
  margin: 0.5rem 0;
  color: #666;
}

/* 导入结果 */
.import-result {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f9f9f9;
  border-radius: 6px;
}

.import-result h4 {
  margin: 0 0 1rem 0;
  color: #333;
}

.result-box {
  padding: 1rem;
  background: white;
  border-radius: 6px;
  border-left: 4px solid #ff9800;
  margin-bottom: 1rem;
}

.result-box.success {
  border-left-color: #4caf50;
}

.result-box p {
  margin: 0.5rem 0;
  color: #666;
}

.error-list {
  background: white;
  padding: 1rem;
  border-radius: 6px;
  max-height: 200px;
  overflow-y: auto;
}

.error-list h5 {
  margin: 0 0 0.5rem 0;
  color: #d32f2f;
}

.error-list ul {
  margin: 0;
  padding-left: 1.5rem;
}

.error-list li {
  color: #666;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
}

/* 筛选栏 */
.filter-bar {
  display: flex;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  min-width: 200px;
}

.filter-group label {
  font-weight: 600;
  margin-bottom: 0.5rem;
  color: #333;
  font-size: 0.95rem;
}

/* 表格 */
.scores-table {
  overflow-x: auto;
  border-radius: 6px;
  border: 1px solid #e0e0e0;
}

table {
  width: 100%;
  border-collapse: collapse;
}

thead {
  background: #f5f5f5;
}

th {
  padding: 1rem;
  text-align: left;
  font-weight: 600;
  color: #333;
  border-bottom: 2px solid #ddd;
}

td {
  padding: 1rem;
  border-bottom: 1px solid #eee;
  color: #666;
}

tbody tr:hover {
  background: #f9f9f9;
}

.score-cell {
  font-weight: 600;
}

.score-cell.excellent {
  color: #4caf50;
}

.score-cell.good {
  color: #2196f3;
}

.score-cell.average {
  color: #ff9800;
}

.score-cell.pass {
  color: #f44336;
}

.score-cell.fail {
  color: #d32f2f;
}

/* 操作按钮 */
.btn-action {
  padding: 0.4rem 0.6rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  margin: 0 0.2rem;
  transition: all 0.2s ease;
  background: white;
  border: 1px solid #ddd;
}

.btn-action:hover {
  transform: scale(1.1);
}

.btn-action.edit:hover {
  border-color: #4A90E2;
  color: #4A90E2;
}

.btn-action.delete:hover {
  border-color: #f44336;
  color: #f44336;
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 1.5rem;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(74, 144, 226, 0.2);
}

.stat-label {
  color: #666;
  font-size: 0.95rem;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.stat-value {
  color: #4A90E2;
  font-size: 2rem;
  font-weight: 700;
}

/* 图表容器 */
.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
  gap: 2.5rem;
  margin-top: 2rem;
}

.chart-box {
  background: #f9f9f9;
  padding: 2rem;
  border-radius: 8px;
  border: 1px solid #e0e0e0;
}

.chart-box h4 {
  margin: 0 0 1.5rem 0;
  color: #333;
  font-size: 1.3rem;
}

/* 分数段分布 */
.distribution-chart {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.distribution-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.grade-label {
  min-width: 90px;
  font-weight: 600;
  color: #333;
  font-size: 1.05rem;
}

.bar-container {
  flex: 1;
  height: 40px;
  background: #e0e0e0;
  border-radius: 4px;
  overflow: hidden;
}

.bar {
  height: 100%;
  border-radius: 4px;
  transition: width 0.3s ease;
  display: flex;
  align-items: center;
  padding-left: 0.8rem;
  color: white;
  font-weight: 600;
  font-size: 1rem;
}

.bar.grade-a {
  background: linear-gradient(90deg, #4caf50 0%, #45a049 100%);
}

.bar.grade-b {
  background: linear-gradient(90deg, #2196f3 0%, #1976d2 100%);
}

.bar.grade-c {
  background: linear-gradient(90deg, #ff9800 0%, #f57c00 100%);
}

.bar.grade-d {
  background: linear-gradient(90deg, #ff6b6b 0%, #ee5a52 100%);
}

.bar.grade-f {
  background: linear-gradient(90deg, #d32f2f 0%, #c62828 100%);
}

.count {
  min-width: 40px;
  text-align: right;
  font-weight: 600;
  color: #333;
}

/* 饼图 */
.grade-pie {
  display: flex;
  height: 50px;
  border-radius: 25px;
  overflow: hidden;
  gap: 1px;
  background: #e0e0e0;
  margin-bottom: 1.5rem;
}

.pie-item {
  transition: all 0.3s ease;
  cursor: pointer;
}

.pie-item:hover {
  opacity: 0.8;
  transform: scaleY(1.2);
}

.pie-item.grade-a {
  background: #4caf50;
}

.pie-item.grade-b {
  background: #2196f3;
}

.pie-item.grade-c {
  background: #ff9800;
}

.pie-item.grade-d {
  background: #ff6b6b;
}

.pie-item.grade-f {
  background: #d32f2f;
}

.pie-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
  color: #666;
}

.color {
  width: 20px;
  height: 20px;
  border-radius: 3px;
}

.color.grade-a {
  background: #4caf50;
}

.color.grade-b {
  background: #2196f3;
}

.color.grade-c {
  background: #ff9800;
}

.color.grade-d {
  background: #ff6b6b;
}

.color.grade-f {
  background: #d32f2f;
}

/* 空状态 */
.empty-state {
  text-align: center;
  padding: 3rem;
  color: #999;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

/* 学生列表 */
.student-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.student-card {
  background: white;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.student-card:hover {
  border-color: #4A90E2;
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
  transform: translateY(-2px);
}

.student-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.5rem;
}

.student-id {
  color: #999;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.summary-badge {
  color: #4A90E2;
  font-weight: 600;
  font-size: 0.9rem;
}

/* 学生汇总 */
.student-summary {
  background: #f9f9f9;
  padding: 2rem;
  border-radius: 8px;
  margin-top: 2rem;
}

.student-summary h4 {
  color: #333;
  margin: 1.5rem 0 1rem 0;
  font-size: 1.2rem;
}

.overall-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
  padding: 1rem;
  background: white;
  border-radius: 6px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  padding: 0.5rem 0;
}

.stat-item .label {
  color: #666;
  font-weight: 500;
}

.stat-item .value {
  color: #4A90E2;
  font-weight: 600;
}

.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.subject-card {
  background: white;
  padding: 1.5rem;
  border-radius: 6px;
  border-left: 4px solid #4A90E2;
}

.subject-card h5 {
  margin: 0 0 1rem 0;
  color: #333;
}

.subject-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.subject-stats .stat {
  color: #666;
}

.score-progression {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.score-badge {
  background: #f0f0f0;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #4A90E2;
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
  border-radius: 12px;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e0e0e0;
}

.modal-header h3 {
  margin: 0;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: #333;
}

.modal-body {
  padding: 1.5rem;
  max-height: 60vh;
  overflow-y: auto;
}

.modal-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e0e0e0;
  justify-content: flex-end;
}

/* 响应式 */
@media (max-width: 768px) {
  .grades-container {
    padding: 1rem;
  }

  .function-cards {
    grid-template-columns: repeat(2, 1fr);
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .charts-container {
    grid-template-columns: 1fr;
  }

  .filter-bar {
    flex-direction: column;
  }

  .filter-group {
    width: 100%;
  }
}

/* 新添加的图表样式 */

/* 整会nd分布 */
.donut-chart {
  display: flex;
  justify-content: center;
  margin-bottom: 1.5rem;
}

.donut-chart svg {
  width: 150px;
  height: 150px;
}

.donut-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
  justify-content: center;
}

.donut-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
}

.dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.dot.grade-a {
  background: #4caf50;
}

.dot.grade-b {
  background: #2196f3;
}

.dot.grade-c {
  background: #ff9800;
}

.dot.grade-d {
  background: #ff6b6b;
}

.dot.grade-f {
  background: #d32f2f;
}

/* 更多图表容器 */
.charts-container-2 {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

/* 成绩范围分析 */
.range-analysis {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.range-item {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.range-title {
  width: 100px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
}

.range-bar {
  flex: 1;
  height: 30px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  padding-right: 1rem;
  position: relative;
  min-width: 100px;
}

.range-bar.excellent {
  background: linear-gradient(90deg, #4caf50 0%, #45a049 100%);
}

.range-bar.good {
  background: linear-gradient(90deg, #2196f3 0%, #1976d2 100%);
}

.range-bar.average {
  background: linear-gradient(90deg, #ff9800 0%, #f57c00 100%);
}

.range-bar.pass {
  background: linear-gradient(90deg, #ff6b6b 0%, #ee5a52 100%);
}

.range-bar.fail {
  background: linear-gradient(90deg, #d32f2f 0%, #c62828 100%);
}

.range-label {
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  margin-left: auto;
}

/* 指标卡片 */
.metrics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 1rem;
}

.metric-card {
  background: linear-gradient(135deg, #f5f9ff 0%, #e6f2ff 100%);
  border: 1px solid #d0e8f2;
  border-radius: 8px;
  padding: 1rem;
  text-align: center;
  transition: all 0.3s ease;
}

.metric-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
}

.metric-icon {
  font-size: 1.8rem;
  margin-bottom: 0.5rem;
}

.metric-info {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.metric-label {
  font-size: 0.8rem;
  color: #666;
  font-weight: 500;
}

.metric-value {
  font-size: 1.3rem;
  font-weight: 700;
  color: #4A90E2;
}

/* 成绩进步趋势图 */
.progress-trend {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.trend-chart {
  background: white;
  border: 1px solid #e8eef5;
  border-radius: 8px;
  padding: 1rem;
}

.trend-svg {
  width: 100%;
  height: 280px;
}

.trend-legend {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-wrap: wrap;
}

.trend-legend .legend-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1rem;
}

.legend-color {
  width: 20px;
  height: 20px;
  border-radius: 3px;
}

/* 全对图表 */
.chart-box.full-width {
  grid-column: 1 / -1;
}

/* 算法信息橫流 */
.algorithm-info {
  background: linear-gradient(135deg, rgba(255, 213, 0, 0.1) 0%, rgba(255, 193, 7, 0.08) 100%);
  border-left: 4px solid #ffc107;
  border-radius: 6px;
  padding: 1.2rem;
  margin-bottom: 1.5rem;
  backdrop-filter: blur(10px);
}

.algo-badge {
  display: inline-block;
  background: linear-gradient(135deg, #ffc107 0%, #ffb300 100%);
  color: white;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.8rem;
}

.algo-description {
  font-size: 0.9rem;
  color: #333;
  line-height: 1.6;
  margin: 0.5rem 0;
}

.algo-description code {
  background: rgba(0, 0, 0, 0.08);
  padding: 0.2rem 0.4rem;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
  color: #d32f2f;
}

/* 母窗样式 */
.glass-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(100, 150, 200, 0.2) 0%, rgba(150, 100, 200, 0.15) 100%);
  backdrop-filter: blur(10px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    backdrop-filter: blur(0px);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(10px);
  }
}

.glass-modal-content {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.92) 0%, rgba(255, 255, 255, 0.88) 100%);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.5);
  border-radius: 16px;
  max-width: 700px;
  width: 90%;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  animation: slideUp 0.3s ease;
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

.glass-modal-header {
  padding: 1.5rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.3);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, rgba(200, 220, 240, 0.5) 0%, rgba(220, 200, 240, 0.3) 100%);
}

.glass-modal-header h4 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
  font-weight: 600;
}

.glass-close-btn {
  background: none;
  border: none;
  font-size: 1.8rem;
  color: #999;
  cursor: pointer;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  transition: all 0.3s ease;
}

.glass-close-btn:hover {
  color: #333;
  background: rgba(0, 0, 0, 0.05);
}

.glass-modal-body {
  padding: 2rem;
}

.glass-modal-body .overall-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.08) 0%, rgba(74, 144, 226, 0.04) 100%);
  border-radius: 12px;
  border-left: 4px solid #4A90E2;
}

.glass-modal-body .stat-item {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.glass-modal-body .stat-item .label {
  font-size: 0.85rem;
  color: #999;
  font-weight: 500;
}

.glass-modal-body .stat-item .value {
  font-size: 1.4rem;
  font-weight: 700;
  color: #4A90E2;
}

.glass-modal-body .subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
}
</style>
