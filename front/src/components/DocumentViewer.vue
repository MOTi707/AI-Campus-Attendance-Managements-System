<template>
  <div class="viewer-container">
    <div class="viewer-header">
      <div class="header-left">
        <button class="back-btn" @click="goBack">← 返回</button>
        <h2>{{ documentData.filename }}</h2>
      </div>
      <button class="close-btn" @click="closeWindow">✕</button>
    </div>

    <!-- 文档信息栏 -->
    <div class="document-info-bar">
      <div class="info-item">
        <span class="label">分类:</span>
        <span class="value">{{ documentData.category }}</span>
      </div>
      <div class="info-item">
        <span class="label">子分类:</span>
        <span class="value">{{ documentData.sub_category || '未分类' }}</span>
      </div>
      <div class="info-item">
        <span class="label">关键词:</span>
        <div class="keywords">
          <span v-for="(kw, idx) in documentData.keywords.slice(0, 5)" :key="idx" class="keyword">
            {{ kw }}
          </span>
          <span v-if="documentData.keywords.length > 5" class="more">
            +{{ documentData.keywords.length - 5 }}
          </span>
        </div>
      </div>
    </div>

    <!-- 文档内容 -->
    <div class="document-content">
      <div class="content-text">
        {{ documentData.content }}
      </div>
    </div>

    <!-- 操作栏 -->
    <div class="viewer-footer">
      <button class="action-btn download-btn" @click="downloadContent">
        📥 下载
      </button>
      <button class="action-btn copy-btn" @click="copyContent">
        📋 复制全文
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const documentData = ref({
  filename: '',
  content: '',
  category: '',
  sub_category: '',
  keywords: [],
  title: ''
})

// 从sessionStorage获取文档数据
const loadDocumentData = () => {
  const data = sessionStorage.getItem('documentContent')
  if (data) {
    try {
      documentData.value = JSON.parse(data)
      // 清除后立即删除，防止刷新时再次加载
      sessionStorage.removeItem('documentContent')
    } catch (e) {
      console.error('Failed to parse document data:', e)
    }
  }
}

// 返回上一页
const goBack = () => {
  window.history.back()
}

// 关闭窗口
const closeWindow = () => {
  window.close()
}

// 下载内容为文件
const downloadContent = () => {
  const element = document.createElement('a')
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(documentData.value.content))
  element.setAttribute('download', documentData.value.filename)
  element.style.display = 'none'
  document.body.appendChild(element)
  element.click()
  document.body.removeChild(element)
}

// 复制全文到剪贴板
const copyContent = () => {
  navigator.clipboard.writeText(documentData.value.content).then(() => {
    alert('已复制到剪贴板')
  }).catch(err => {
    console.error('复制失败:', err)
    alert('复制失败，请重试')
  })
}

onMounted(() => {
  loadDocumentData()
})
</script>

<style scoped>
.viewer-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.viewer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem 2rem;
  background: white;
  border-bottom: 1px solid #ddd;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-btn {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border: none;
  padding: 0.6rem 1.2rem;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.viewer-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
  word-break: break-word;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  padding: 0.5rem;
  transition: color 0.2s ease;
}

.close-btn:hover {
  color: #333;
}

/* 文档信息栏 */
.document-info-bar {
  background: white;
  padding: 1.5rem 2rem;
  border-bottom: 1px solid #ddd;
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.label {
  font-weight: 600;
  color: #333;
  font-size: 0.9rem;
}

.value {
  color: #666;
  font-size: 0.9rem;
}

.keywords {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.keyword {
  background: #f0f4f8;
  color: #4A90E2;
  padding: 0.3rem 0.6rem;
  border-radius: 4px;
  font-size: 0.8rem;
  border: 1px solid #4A90E2;
}

.more {
  color: #999;
  font-size: 0.8rem;
  align-self: center;
}

/* 文档内容区域 */
.document-content {
  flex: 1;
  overflow-y: auto;
  padding: 2rem;
}

.content-text {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  line-height: 1.8;
  color: #333;
  font-size: 0.95rem;
  word-wrap: break-word;
  white-space: pre-wrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 操作栏 */
.viewer-footer {
  display: flex;
  gap: 1rem;
  padding: 1.5rem 2rem;
  background: white;
  border-top: 1px solid #ddd;
  justify-content: center;
}

.action-btn {
  padding: 0.7rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.download-btn {
  background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
  color: white;
}

.download-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(40, 167, 69, 0.3);
}

.copy-btn {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
}

.copy-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

/* 滚动条样式 */
.document-content::-webkit-scrollbar {
  width: 8px;
}

.document-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.document-content::-webkit-scrollbar-thumb {
  background: #4A90E2;
  border-radius: 10px;
}

.document-content::-webkit-scrollbar-thumb:hover {
  background: #357ABD;
}

/* 响应式 */
@media (max-width: 768px) {
  .viewer-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .document-info-bar {
    flex-direction: column;
    gap: 1rem;
  }

  .viewer-footer {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
    justify-content: center;
  }
}
</style>
