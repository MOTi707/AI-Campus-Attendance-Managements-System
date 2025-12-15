<template>
  <div class="materials-container">
    <div class="materials-header">
      <h2>资料中心</h2>
      <p class="desc">智能分类和管理教学资料</p>
    </div>

    <!-- 操作栏 -->
    <div class="materials-toolbar">
      <button class="upload-btn" @click="showUploadModal = true">
        <span class="btn-icon">⬆️</span>
        上传资料
      </button>

      <!-- 分类筛选 -->
      <div class="category-filter">
        <select v-model="selectedCategory" @change="filterByCategory" class="filter-select">
          <option value="">全部分类</option>
          <option value="数学">数学</option>
          <option value="英语">英语</option>
          <option value="物理">物理</option>
          <option value="化学">化学</option>
          <option value="生物">生物</option>
          <option value="历史">历史</option>
          <option value="地理">地理</option>
          <option value="政治">政治</option>
          <option value="经济">经济</option>
          <option value="综合">综合</option>
        </select>
      </div>

      <!-- 搜索框和搜索类型选择 -->
      <div class="search-wrapper">
        <input
          v-model="searchKeyword"
          type="text"
          placeholder="搜索资料..."
          class="search-input"
          @keyup.enter="handleSearch"
        />
        <div class="search-type-tabs">
          <button
            :class="['tab-btn', { active: searchType === 'title' }]"
            @click="searchType = 'title'"
          >
            📄 标题搜索
          </button>
          <button
            :class="['tab-btn', { active: searchType === 'fulltext' }]"
            @click="searchType = 'fulltext'"
          >
            🔍 全文搜索
          </button>
        </div>
        <button class="search-btn" @click="handleSearch">
          🔍
        </button>
      </div>
    </div>

    <!-- 分类统计 -->
    <div class="category-stats">
      <div
        v-for="cat in categories"
        :key="cat.name"
        :class="['stat-card', { active: selectedCategory === cat.name }]"
        @click="selectedCategory = cat.name; filterByCategory()"
      >
        <div class="stat-label">{{ cat.name }}</div>
        <div class="stat-count">{{ cat.count }}</div>
      </div>
    </div>

    <!-- 文档列表 -->
    <div class="documents-section">
      <div v-if="documents.length === 0" class="empty-state">
        <div class="empty-icon">📄</div>
        <p>还没有上传任何资料</p>
        <button class="upload-btn-secondary" @click="showUploadModal = true">
          立即上传
        </button>
      </div>

      <div v-else class="documents-grid">
        <div
          v-for="doc in documents"
          :key="doc.id"
          :class="['document-card', `type-${doc.file_type}`]"
        >
          <div class="doc-header">
            <div class="doc-icon">{{ getFileIcon(doc.file_type) }}</div>
            <div class="doc-category">
              <span class="category-badge">{{ doc.category }}</span>
              <span v-if="doc.confidence_score" class="confidence">
                置信度: {{ (doc.confidence_score * 100).toFixed(0) }}%
              </span>
            </div>
          </div>

          <div class="doc-content">
            <h3 class="doc-title">{{ doc.original_name }}</h3>
            <p v-if="doc.title" class="doc-subtitle">{{ doc.title }}</p>
            <p v-if="doc.description" class="doc-desc">{{ doc.description }}</p>
            
            <!-- 全文搜索上下文 -->
            <div v-if="doc.search_type === 'fulltext' && doc.context" class="search-context">
              <span v-if="doc.context.type === 'file_content'" class="context-label file-label">📄 文件内容匹配</span>
              <span v-else-if="doc.context.type === 'description'" class="context-label desc-label">📝 描述匹配</span>
              <span v-else-if="doc.context.type === 'title'" class="context-label title-label">🏷️ 标题匹配</span>
              <div class="context-text">
                <span class="context-content">{{ doc.context.context }}</span>
                <span v-if="doc.context.text" class="matched-text">{{ doc.context.text }}</span>
              </div>
            </div>
            
            <!-- 标题搜索片段 -->
            <div v-if="doc.search_type === 'title'" class="search-badge">
              📄 标题搜索
            </div>
          </div>

          <div class="doc-keywords">
            <span
              v-for="(keyword, idx) in doc.keywords.slice(0, 3)"
              :key="idx"
              class="keyword-tag"
            >
              {{ keyword }}
            </span>
            <span v-if="doc.keywords.length > 3" class="more-keywords">
              +{{ doc.keywords.length - 3 }}个
            </span>
          </div>

          <div class="doc-footer">
            <span class="doc-size">{{ formatFileSize(doc.file_size) }}</span>
            <span class="doc-date">{{ formatDate(doc.created_at) }}</span>
            <div class="action-buttons">
              <button
                v-if="doc.file_type === 'txt'"
                class="action-btn open-btn"
                @click="openDocument(doc.id)"
                title="在线打开"
              >
                👁️
              </button>
              <button
                class="action-btn download-btn"
                @click="downloadDocument(doc.id, doc.original_name)"
                title="下载"
              >
                ⬇️
              </button>
              <button
                class="action-btn delete-btn"
                @click="deleteDocument(doc.id)"
                title="删除"
              >
                🗑️
              </button>
            </div>
          </div>

          <div v-if="doc.is_auto_classified" class="auto-tag">自动分类</div>
        </div>
      </div>
    </div>

    <!-- 上传弹窗 -->
    <div v-if="showUploadModal" class="modal-overlay" @click.self="showUploadModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h3>上传资料</h3>
          <button class="close-btn" @click="showUploadModal = false">×</button>
        </div>

        <div class="upload-area">
          <div class="file-input-wrapper">
            <input
              ref="fileInput"
              type="file"
              class="file-input"
              @change="handleFileSelect"
              accept=".pdf,.doc,.docx,.pptx,.txt,.xls,.xlsx"
            />
            <div class="upload-prompt">
              <div class="upload-icon">📤</div>
              <p>点击选择文件或拖拽上传</p>
              <span class="upload-hint">支持 PDF, DOC, DOCX, PPTX, TXT, XLS, XLSX 等格式</span>
            </div>
          </div>
        </div>

        <div v-if="selectedFile" class="file-info">
          <p><strong>文件：</strong> {{ selectedFile.name }}</p>
          <p><strong>大小：</strong> {{ formatFileSize(selectedFile.size) }}</p>
        </div>

        <div class="form-group">
          <label>文档标题</label>
          <input
            v-model="uploadForm.title"
            type="text"
            placeholder="输入文档标题（可选）"
            class="form-input"
          />
        </div>

        <div class="form-group">
          <label>文档描述</label>
          <textarea
            v-model="uploadForm.description"
            placeholder="输入文档描述（可选）"
            class="form-textarea"
            rows="3"
          ></textarea>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="showUploadModal = false">取消</button>
          <button
            class="btn-upload"
            @click="submitUpload"
            :disabled="!selectedFile || isUploading"
          >
            {{ isUploading ? '上传中...' : '上传' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const documents = ref([])
const categories = ref([])
const selectedCategory = ref('')
const searchKeyword = ref('')
const searchType = ref('title')  // 'title' 或 'fulltext'
const showUploadModal = ref(false)
const selectedFile = ref(null)
const isUploading = ref(false)
const fileInput = ref(null)
const uploadForm = ref({
  title: '',
  description: ''
})

// 获取分类列表
const fetchCategories = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/materials/categories', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    const data = await response.json()
    if (data.code === 200) {
      categories.value = data.data
    }
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  }
}

// 获取文档列表
const fetchDocuments = async (category = '') => {
  try {
    const token = localStorage.getItem('token')
    let url = 'http://localhost:5000/api/materials/list'
    if (category) {
      url += `?category=${category}`
    }

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    const data = await response.json()
    if (data.code === 200) {
      documents.value = data.data.documents
    }
  } catch (error) {
    console.error('Failed to fetch documents:', error)
    ElMessage.error('获取资料列表失败')
  }
}

// 按分类筛选
const filterByCategory = () => {
  fetchDocuments(selectedCategory.value)
}

// 搜索处理 - 调用后端 API 进行标题或全文搜索
const handleSearch = async () => {
  if (!searchKeyword.value.trim()) {
    // 如果搜索框为空，则恢复捐示所有资料
    fetchDocuments(selectedCategory.value)
    return
  }

  try {
    const token = localStorage.getItem('token')
    let url = `http://localhost:5000/api/materials/search?q=${encodeURIComponent(searchKeyword.value)}&type=${searchType.value}`
    
    if (selectedCategory.value) {
      url += `&category=${selectedCategory.value}`
    }

    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    const data = await response.json()
    if (data.code === 200) {
      documents.value = data.data.documents
    } else {
      ElMessage.error(data.message || '搜索失败')
    }
  } catch (error) {
    console.error('Search error:', error)
    ElMessage.error('搜索出错')
  }
}

// 文件选择处理
const handleFileSelect = (event) => {
  const file = event.target.files[0]
  if (file) {
    if (file.size > 50 * 1024 * 1024) {
      ElMessage.error('文件过大，最大支持50MB')
      return
    }
    selectedFile.value = file
  }
}

// 提交上传
const submitUpload = async () => {
  if (!selectedFile.value) {
    ElMessage.error('请选择文件')
    return
  }

  isUploading.value = true
  const formData = new FormData()
  formData.append('file', selectedFile.value)
  formData.append('title', uploadForm.value.title)
  formData.append('description', uploadForm.value.description)

  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/materials/upload', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      body: formData
    })

    const data = await response.json()
    if (data.code === 200 || data.code === 201) {
      ElMessage.success('上传成功！系统已自动分类')
      showUploadModal.value = false
      selectedFile.value = null
      uploadForm.value = { title: '', description: '' }
      if (fileInput.value) fileInput.value.value = ''
      fetchDocuments(selectedCategory.value)
      fetchCategories()
    } else {
      ElMessage.error(data.message || '上传失败')
    }
  } catch (error) {
    console.error('Upload error:', error)
    ElMessage.error('上传出错')
  } finally {
    isUploading.value = false
  }
}

// 下载文档
const downloadDocument = async (docId, originalName) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/materials/download/${docId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (!response.ok) {
      ElMessage.error('下载失败')
      return
    }

    // 从响应中获取文件
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = originalName
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    ElMessage.success('下载成功')
  } catch (error) {
    console.error('Download error:', error)
    ElMessage.error('下载出错')
  }
}

// 在线打开文档
const openDocument = async (docId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/materials/open/${docId}`, {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    const data = await response.json()
    if (data.code === 200) {
      // 存储文档内容到localStorage，以便在新窗口中显示
      sessionStorage.setItem('documentContent', JSON.stringify(data.data))
      // 打开新窗口显示文档
      window.open(`/document-viewer`, '_blank')
    } else {
      ElMessage.error(data.message || '打开失败')
    }
  } catch (error) {
    console.error('Open error:', error)
    ElMessage.error('打开文件失败')
  }
}

// 删除文档
const deleteDocument = async (docId) => {
  if (!confirm('确定要删除这个资料吗？')) {
    return
  }

  try {
    const token = localStorage.getItem('token')
    const response = await fetch(`http://localhost:5000/api/materials/delete/${docId}`, {
      method: 'DELETE',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    const data = await response.json()
    if (data.code === 200) {
      ElMessage.success('删除成功')
      fetchDocuments(selectedCategory.value)
      fetchCategories()
    } else {
      ElMessage.error(data.message || '删除失败')
    }
  } catch (error) {
    console.error('Delete error:', error)
    ElMessage.error('删除出错')
  }
}

// 获取文件图标
const getFileIcon = (fileType) => {
  const icons = {
    pdf: '📕',
    doc: '📗',
    docx: '📗',
    pptx: '📙',
    txt: '📄',
    xls: '📊',
    xlsx: '📊'
  }
  return icons[fileType] || '📎'
}

// 格式化文件大小
const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const k = 1024
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(k))
  return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

onMounted(() => {
  fetchCategories()
  fetchDocuments()
})
</script>

<style scoped>
.materials-container {
  padding: 2rem;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  min-height: 100vh;
}

.materials-header {
  margin-bottom: 2rem;
}

.materials-header h2 {
  margin: 0;
  font-size: 1.8rem;
  color: #333;
  font-weight: 600;
}

.materials-header .desc {
  margin: 0.5rem 0 0 0;
  color: #999;
  font-size: 0.95rem;
}

/* 操作栏 */
.materials-toolbar {
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.upload-btn,
.upload-btn-secondary {
  padding: 0.7rem 1.5rem;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.upload-btn:hover,
.upload-btn-secondary:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.btn-icon {
  font-size: 1rem;
}

.filter-select,
.search-input {
  padding: 0.7rem 1rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.95rem;
  background: white;
  transition: all 0.2s ease;
}

.filter-select {
  min-width: 150px;
}

.search-wrapper {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex: 1;
}

.search-input {
  flex: 1;
  min-width: 200px;
}

.search-type-tabs {
  display: flex;
  gap: 0.3rem;
  background: #f5f5f5;
  padding: 0.3rem;
  border-radius: 6px;
}

.tab-btn {
  padding: 0.5rem 0.8rem;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
  color: #666;
  font-weight: 500;
}

.tab-btn:hover {
  border-color: #4A90E2;
  color: #4A90E2;
}

.tab-btn.active {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border-color: #4A90E2;
  box-shadow: 0 2px 8px rgba(74, 144, 226, 0.2);
}

.search-btn {
  padding: 0.7rem 1.5rem;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 600;
}

.search-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.filter-select:focus,
.search-input:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

/* 分类统计 */
.category-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  padding: 1.2rem;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s ease;
  border: 2px solid transparent;
  box-shadow: 0 2px 8px rgba(74, 144, 226, 0.1);
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.2);
}

.stat-card.active {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border-color: #4A90E2;
}

.stat-label {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.stat-count {
  font-size: 1.8rem;
  font-weight: 700;
}

/* 文档列表 */
.documents-section {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 12px rgba(74, 144, 226, 0.1);
}

.empty-state {
  text-align: center;
  padding: 3rem;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.empty-state p {
  color: #666;
  font-size: 1rem;
  margin: 0 0 1.5rem 0;
}

.documents-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.document-card {
  border: 1px solid #e8eef5;
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
  background: white;
  position: relative;
}

.document-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(74, 144, 226, 0.15);
  border-color: #4A90E2;
}

.doc-header {
  padding: 1rem;
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.05) 0%, transparent 100%);
  display: flex;
  gap: 1rem;
  align-items: flex-start;
  border-bottom: 1px solid #e8eef5;
}

.doc-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.doc-category {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.category-badge {
  display: inline-block;
  background: #4A90E2;
  color: white;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  width: fit-content;
}

.confidence {
  font-size: 0.8rem;
  color: #4A90E2;
  font-weight: 500;
}

.doc-content {
  padding: 1rem;
}

.doc-title {
  margin: 0;
  font-size: 0.95rem;
  color: #333;
  font-weight: 600;
  word-break: break-word;
}

.doc-subtitle {
  margin: 0.5rem 0 0 0;
  font-size: 0.85rem;
  color: #999;
}

.doc-desc {
  margin: 0.5rem 0 0 0;
  font-size: 0.85rem;
  color: #999;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.doc-keywords {
  padding: 0.5rem 1rem;
  background: rgba(74, 144, 226, 0.05);
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.keyword-tag {
  background: white;
  border: 1px solid #4A90E2;
  color: #4A90E2;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.more-keywords {
  color: #999;
  font-size: 0.75rem;
  align-self: center;
}

.doc-footer {
  padding: 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-top: 1px solid #e8eef5;
  font-size: 0.85rem;
  color: #999;
}

.doc-size {
  font-weight: 500;
}

.doc-date {
  flex: 1;
  text-align: center;
}

.action-buttons {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  background: none;
  border: none;
  font-size: 1rem;
  cursor: pointer;
  padding: 0.3rem;
  transition: transform 0.2s ease;
}

.action-btn:hover {
  transform: scale(1.2);
}

.open-btn {
  color: #4A90E2;
}

.download-btn {
  color: #28a745;
}

.delete-btn {
  color: #dc3545;
}

.auto-tag {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: #fff3cd;
  color: #856404;
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.search-badge {
  display: inline-block;
  background: #e3f2fd;
  color: #1976d2;
  padding: 0.4rem 0.8rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-top: 0.5rem;
}

.search-context {
  margin-top: 0.8rem;
  padding: 0.8rem;
  background: #f5f9ff;
  border-left: 3px solid #4A90E2;
  border-radius: 4px;
}

.context-label {
  display: inline-block;
  background: #4A90E2;
  color: white;
  padding: 0.2rem 0.6rem;
  border-radius: 3px;
  font-size: 0.75rem;
  font-weight: 600;
  margin-bottom: 0.4rem;
}

.context-text {
  font-size: 0.85rem;
  color: #666;
  line-height: 1.5;
  word-break: break-word;
  margin: 0.4rem 0;
}

.context-content {
  color: #999;
}

.matched-text {
  background: #ffeb3b;
  color: #333;
  font-weight: 600;
  padding: 0.1rem 0.3rem;
  border-radius: 2px;
}

.context-type {
  display: block;
  font-size: 0.75rem;
  color: #999;
  margin-top: 0.3rem;
  font-style: italic;
}

/* 搜索类型标记样式 */
.context-label.file-label {
  background: linear-gradient(135deg, #4A90E2 0%, #2E5C8A 100%);
}

.context-label.desc-label {
  background: linear-gradient(135deg, #7B68EE 0%, #5a4ab0 100%);
}

.context-label.title-label {
  background: linear-gradient(135deg, #FF7043 0%, #D84315 100%);
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
  padding: 1rem;
}

.modal-content {
  background: white;
  border-radius: 12px;
  max-width: 500px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
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
  font-size: 1.3rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
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

.upload-area {
  padding: 2rem 1.5rem;
}

.file-input-wrapper {
  position: relative;
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
  margin: 0;
  color: #333;
  font-weight: 500;
}

.upload-hint {
  display: block;
  margin-top: 0.5rem;
  font-size: 0.85rem;
  color: #999;
}

.file-info {
  padding: 0 1.5rem;
  margin: 1rem 0;
  padding: 1rem;
  background: rgba(74, 144, 226, 0.05);
  border-radius: 6px;
}

.file-info p {
  margin: 0.5rem 0;
  font-size: 0.9rem;
  color: #333;
}

.form-group {
  padding: 0 1.5rem;
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  font-weight: 600;
  color: #333;
}

.form-input,
.form-textarea {
  width: 100%;
  padding: 0.7rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  font-family: inherit;
  transition: all 0.2s ease;
  box-sizing: border-box;
}

.form-input:focus,
.form-textarea:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.modal-footer {
  padding: 1.5rem;
  border-top: 1px solid #e8eef5;
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
}

.btn-cancel {
  padding: 0.7rem 1.5rem;
  background: #f5f5f5;
  color: #333;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-cancel:hover {
  background: #e8e8e8;
}

.btn-upload {
  padding: 0.7rem 1.5rem;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-upload:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.btn-upload:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* 响应式 */
@media (max-width: 768px) {
  .materials-container {
    padding: 1rem;
  }

  .materials-toolbar {
    flex-direction: column;
  }

  .filter-select,
  .search-input {
    width: 100%;
  }

  .category-stats {
    grid-template-columns: repeat(3, 1fr);
  }

  .documents-grid {
    grid-template-columns: 1fr;
  }

  .modal-content {
    max-width: 95vw;
  }
}
</style>
