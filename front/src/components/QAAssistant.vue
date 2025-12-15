<template>
  <div class="qa-assistant-container">
    <div class="panel-header">
      <h2>💬 智能问答助手</h2>
      <p class="panel-desc">基于 DeepSeek AI 的智能教学助手，帮助您解答课程管理问题</p>
    </div>

    <div class="chat-layout">
      <!-- 左侧对话列表 -->
      <div class="conversations-sidebar">
        <div class="sidebar-header">
          <h3>对话列表</h3>
          <button @click="createNewConversation" class="btn-new-chat">+ 新对话</button>
        </div>
        
        <div class="conversations-list">
          <div
            v-for="conv in conversations"
            :key="conv.id"
            :class="['conversation-item', { active: currentConversationId === conv.id }]"
            @click="selectConversation(conv.id)"
          >
            <div class="conv-title">{{ conv.title }}</div>
            <div class="conv-time">{{ formatTime(conv.updated_at) }}</div>
            <button @click.stop="deleteConversation(conv.id)" class="btn-delete">🗑️</button>
          </div>
          
          <div v-if="conversations.length === 0" class="empty-conversations">
            <p>暂无对话</p>
            <p class="hint">点击"新对话"开始</p>
          </div>
        </div>
      </div>

      <!-- 右侧聊天区域 -->
      <div class="chat-area">
        <!-- 消息列表 -->
        <div ref="messagesContainer" class="messages-container">
          <div v-if="messages.length === 0 && currentConversationId" class="empty-messages">
            <div class="empty-icon">💭</div>
            <p>开始新的对话</p>
          </div>

          <div v-for="msg in messages" :key="msg.id" :class="['message', msg.role]">
            <div class="message-avatar">
              {{ msg.role === 'user' ? '👤' : '🤖' }}
            </div>
            <div class="message-content">
              <div :class="['message-text', { 'loading': msg.content.includes('回复加载中') }]">
                {{ msg.content }}
                <div v-if="msg.content.includes('回复加载中')" class="loading-dots">
                  <span></span><span></span><span></span>
                </div>
              </div>
              <div class="message-time">{{ formatTime(msg.created_at) }}</div>
            </div>
          </div>

        </div>

        <!-- 快速问题 -->
        <div class="quick-questions-container">
          <button
            v-for="(q, index) in quickQuestions"
            :key="index"
            @click="sendQuickQuestion(q)"
            class="quick-question-btn"
            :disabled="!currentConversationId || isLoading"
          >
            {{ q }}
          </button>
        </div>

        <!-- 输入区域 -->
        <div class="input-area">
          <textarea
            v-model="inputMessage"
            @keydown.enter.prevent="handleEnterKey"
            placeholder="输入您的问题..."
            :disabled="!currentConversationId || isLoading"
            rows="3"
          ></textarea>
          <button
            @click="sendMessage"
            :disabled="!inputMessage.trim() || !currentConversationId || isLoading"
            class="btn-send"
          >
            {{ isLoading ? '发送中...' : '发送' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { ElMessage } from 'element-plus'

const conversations = ref([])
const currentConversationId = ref(null)
const messages = ref([])
const inputMessage = ref('')
const isLoading = ref(false)
const messagesContainer = ref(null)

const quickQuestions = [
  '如何制定有效的课程安排？',
  '学生作业管理有什么好方法？',
  '如何安排Python大作业？',
  '查询学生成绩情况',
  '如何提高课堂互动性？'
]

// 加载对话列表
const loadConversations = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/qa-assistant/conversations', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    const result = await response.json()
    if (result.code === 200) {
      conversations.value = result.data
      
      // 如果有对话且没有选中的，自动选中第一个
      if (conversations.value.length > 0 && !currentConversationId.value) {
        selectConversation(conversations.value[0].id)
      }
    }
  } catch (error) {
    console.error('加载对话列表失败:', error)
  }
}

// 检查API配置
const checkApiConfig = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/qa-assistant/config', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })
    
    const result = await response.json()
    if (result.code === 200) {
      if (!result.data.api_key_configured) {
        ElMessage.error('⚠️ 后端未配置 API Key，请修改 routes_qa_assistant.py 文件中的配置')
      }
    }
  } catch (error) {
    console.error('检查API配置失败:', error)
  }
}

// 创建新对话
const createNewConversation = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:5000/api/qa-assistant/conversations', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: '新对话'
      })
    })
    
    const result = await response.json()
    if (result.code === 200) {
      await loadConversations()
      selectConversation(result.data.id)
      ElMessage.success('创建对话成功')
    } else {
      ElMessage.error(result.message || '创建对话失败')
    }
  } catch (error) {
    ElMessage.error('创建对话失败: ' + error.message)
  }
}

// 选择对话
const selectConversation = async (conversationId) => {
  currentConversationId.value = conversationId
  await loadMessages(conversationId)
}

// 加载消息
const loadMessages = async (conversationId) => {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(
      `http://localhost:5000/api/qa-assistant/conversations/${conversationId}/messages`,
      {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    )
    
    const result = await response.json()
    if (result.code === 200) {
      messages.value = result.data
      await nextTick()
      scrollToBottom()
    }
  } catch (error) {
    console.error('加载消息失败:', error)
  }
}

// 删除对话
const deleteConversation = async (conversationId) => {
  if (!confirm('确定要删除这个对话吗？')) return
  
  try {
    const token = localStorage.getItem('token')
    const response = await fetch(
      `http://localhost:5000/api/qa-assistant/conversations/${conversationId}`,
      {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      }
    )
    
    const result = await response.json()
    if (result.code === 200) {
      ElMessage.success('删除成功')
      
      // 如果删除的是当前对话，清空消息
      if (currentConversationId.value === conversationId) {
        currentConversationId.value = null
        messages.value = []
      }
      
      await loadConversations()
    } else {
      ElMessage.error(result.message || '删除失败')
    }
  } catch (error) {
    ElMessage.error('删除失败: ' + error.message)
  }
}

// 发送消息
const sendMessage = async () => {
  const message = inputMessage.value.trim()
  if (!message || !currentConversationId.value) return
  
  isLoading.value = true
  const userMessage = message
  inputMessage.value = ''
  
  // 立即显示用户消息
  messages.value.push({
    id: Date.now(),
    role: 'user',
    content: userMessage,
    created_at: new Date().toISOString()
  })
  
  await nextTick()
  scrollToBottom()
  
  try {
    const token = localStorage.getItem('token')
    
    // 添加加载中消息
    const assistantMessageIndex = messages.value.length
    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: '💭 回复加载中...',
      created_at: new Date().toISOString()
    })
    
    await nextTick()
    scrollToBottom()
    
    // 发送请求
    const response = await fetch('http://localhost:5000/api/qa-assistant/chat', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        conversation_id: currentConversationId.value,
        message: userMessage
      })
    })
    
    const result = await response.json()
    
    if (result.code === 200) {
      // 更新AI回复内容
      messages.value[assistantMessageIndex].content = result.data.content
      await nextTick()
      scrollToBottom()
      
      // 刷新对话列表
      await loadConversations()
    } else {
      // 触认期阀消息并显示错误
      messages.value[assistantMessageIndex].content = result.message
      ElMessage.error(result.message || '转事执行失败')
    }
  } catch (error) {
    console.error('发送失败:', error)
    // 更新AI回复为错误信息
    messages.value[assistantMessageIndex].content = `❌ 网络错误: ${error.message}`
    ElMessage.error('发送失败: ' + error.message)
  } finally {
    isLoading.value = false
  }
}

// 发送快速问题
const sendQuickQuestion = (question) => {
  inputMessage.value = question
  sendMessage()
}

// 处理回车键
const handleEnterKey = (event) => {
  if (!event.shiftKey) {
    sendMessage()
  } else {
    // Shift + Enter 换行
    inputMessage.value += '\n'
  }
}

// 滚动到底部
const scrollToBottom = () => {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

// 格式化时间
const formatTime = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  const now = new Date()
  const diff = now - date
  
  // 小于1分钟
  if (diff < 60000) return '刚刚'
  // 小于1小时
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  // 小于1天
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  // 显示日期
  return date.toLocaleDateString('zh-CN')
}

// 监听消息变化，自动滚动
watch(messages, async () => {
  await nextTick()
  scrollToBottom()
}, { deep: true })

onMounted(() => {
  loadConversations()
  checkApiConfig()
})
</script>

<style scoped>
.qa-assistant-container {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel-header {
  margin-bottom: 1rem;
  border-bottom: 1px solid #e8eef5;
  padding-bottom: 0.8rem;
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

.chat-layout {
  display: flex;
  gap: 1rem;
  flex: 1;
  min-height: 0;
  overflow: hidden;
}

/* 左侧对话列表 */
.conversations-sidebar {
  width: 240px;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 0.8rem;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 8px rgba(74, 144, 226, 0.1);
  min-height: 0;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.8rem;
  padding-bottom: 0.4rem;
  border-bottom: 1px solid #e8eef5;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 0.95rem;
  color: #333;
}

.btn-new-chat {
  padding: 0.35rem 0.7rem;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-new-chat:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.conversations-list {
  flex: 1;
  overflow-y: auto;
}

.conversation-item {
  padding: 0.6rem;
  margin-bottom: 0.4rem;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
  border: 2px solid transparent;
}

.conversation-item:hover {
  background: #f8f9ff;
  border-color: #4A90E2;
}

.conversation-item.active {
  background: linear-gradient(135deg, rgba(74, 144, 226, 0.1) 0%, rgba(74, 144, 226, 0.05) 100%);
  border-color: #4A90E2;
}

.conv-title {
  font-size: 0.85rem;
  color: #333;
  font-weight: 500;
  margin-bottom: 0.2rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conv-time {
  font-size: 0.7rem;
  color: #999;
}

.btn-delete {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  opacity: 0;
  transition: opacity 0.3s;
}

.conversation-item:hover .btn-delete {
  opacity: 1;
}

.btn-delete:hover {
  transform: scale(1.2);
}

.empty-conversations {
  text-align: center;
  padding: 2rem 1rem;
  color: #999;
}

.empty-conversations .hint {
  font-size: 0.85rem;
  margin-top: 0.5rem;
}

/* 右侧聊天区域 */
.chat-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(255, 255, 255, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 1.2rem;
  box-shadow: 0 2px 8px rgba(74, 144, 226, 0.1);
  min-height: 0;
  overflow: hidden;
}

/* API Key 配置横幅 */
.api-key-banner {
  background: linear-gradient(135deg, #fff9e6 0%, #ffe6cc 100%);
  border: 2px solid #ffb84d;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.banner-content {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 0.8rem;
}

.banner-icon {
  font-size: 2rem;
}

.banner-text strong {
  display: block;
  color: #e67e22;
  margin-bottom: 0.3rem;
}

.banner-text p {
  margin: 0;
  font-size: 0.85rem;
  color: #666;
}

.api-key-input-area {
  display: flex;
  gap: 0.5rem;
}

.api-key-input {
  flex: 1;
  padding: 0.6rem;
  border: 2px solid #ffb84d;
  border-radius: 6px;
  font-size: 0.9rem;
}

.api-key-input:focus {
  outline: none;
  border-color: #e67e22;
}

.btn-save-key {
  padding: 0.6rem 1.2rem;
  background: #e67e22;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-save-key:hover {
  background: #d35400;
}

/* 消息容器 */
.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 0.8rem;
  margin-bottom: 0.8rem;
  background: rgba(248, 250, 252, 0.5);
  border-radius: 8px;
  min-height: 0;
}

.empty-messages {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #999;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.quick-questions {
  margin-top: 2rem;
  text-align: center;
}

.quick-title {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 0.8rem;
}

/* 快速问题容器 */
.quick-questions-container {
  display: flex;
  gap: 0.6rem;
  padding: 0.8rem;
  background: rgba(248, 250, 252, 0.5);
  border-radius: 8px;
  flex-wrap: wrap;
  justify-content: center;
  flex-shrink: 0;
}

.quick-question-btn {
  padding: 0.5rem 1rem;
  background: white;
  border: 2px solid #4A90E2;
  border-radius: 6px;
  color: #4A90E2;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.85rem;
  white-space: nowrap;
}

.quick-question-btn:hover:not(:disabled) {
  background: #4A90E2;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.quick-question-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 消息样式 */
.message {
  display: flex;
  gap: 0.8rem;
  margin-bottom: 1.5rem;
  animation: fadeIn 0.3s ease;
}

/* 用户消息稍后右对齐 */
.message.user {
  flex-direction: row-reverse;
  justify-content: flex-end;
}

/* AI 消息左对齐 */
.message.assistant {
  flex-direction: row;
  justify-content: flex-start;
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

.message-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
}

.message.assistant .message-avatar {
  background: linear-gradient(135deg, #52c41a 0%, #389e0d 100%);
}

.message-content {
  flex: 1;
  max-width: 70%;
}

/* 用户消息文字右对齐 */
.message.user .message-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

/* AI 消息文字左对齐 */
.message.assistant .message-content {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.message-text {
  padding: 1rem;
  border-radius: 12px;
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.message.user .message-text {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border-bottom-right-radius: 4px;
}

.message.assistant .message-text {
  background: white;
  border: 2px solid #e8eef5;
  color: #333;
  border-bottom-left-radius: 4px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

/* 加载中状态的消息文本 */
.message.assistant .message-text.loading {
  background: rgba(74, 144, 226, 0.1);
  padding: 1rem;
}

.message-time {
  font-size: 0.75rem;
  color: #999;
  margin-top: 0.3rem;
  padding-left: 0.5rem;
}

/* 加载动画 */
.loading-dots {
  display: flex;
  gap: 0.3rem;
  padding: 0.5rem 0;
}

.loading-dots span {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #4A90E2;
  animation: bounce 1.4s infinite ease-in-out both;
}

.loading-dots span:nth-child(1) {
  animation-delay: -0.32s;
}

.loading-dots span:nth-child(2) {
  animation-delay: -0.16s;
}

@keyframes bounce {
  0%, 80%, 100% {
    transform: scale(0);
  }
  40% {
    transform: scale(1);
  }
}

/* 输入区域 */
.input-area {
  display: flex;
  gap: 0.6rem;
  align-items: flex-end;
  flex-shrink: 0;
}

.input-area textarea {
  flex: 1;
  padding: 0.6rem;
  border: 2px solid #e8eef5;
  border-radius: 8px;
  font-size: 0.85rem;
  font-family: inherit;
  resize: none;
  transition: border-color 0.3s;
}

.input-area textarea:focus {
  outline: none;
  border-color: #4A90E2;
}

.input-area textarea:disabled {
  background: #f5f5f5;
  cursor: not-allowed;
}

.btn-send {
  padding: 0.6rem 1.2rem;
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.3s;
  white-space: nowrap;
}

.btn-send:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.btn-send:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* 滚动条美化 */
.conversations-list::-webkit-scrollbar,
.messages-container::-webkit-scrollbar {
  width: 6px;
}

.conversations-list::-webkit-scrollbar-track,
.messages-container::-webkit-scrollbar-track {
  background: transparent;
}

.conversations-list::-webkit-scrollbar-thumb,
.messages-container::-webkit-scrollbar-thumb {
  background: rgba(74, 144, 226, 0.3);
  border-radius: 3px;
}

.conversations-list::-webkit-scrollbar-thumb:hover,
.messages-container::-webkit-scrollbar-thumb:hover {
  background: rgba(74, 144, 226, 0.5);
}
</style>
