<template>
  <transition name="modal-fade">
    <div v-if="visible" class="modal-overlay" @click.self="close">
      <div class="modal-content">
        <div class="modal-header">
          <h2>{{ title }}</h2>
          <button class="close-btn" @click="close">×</button>
        </div>
        
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="form-group">
              <label>{{ inputLabel }} *</label>
              <textarea 
                v-if="taskType === 'question'" 
                v-model="formData.taskName" 
                :placeholder="placeholder"
                rows="4"
              ></textarea>
              <input 
                v-else
                v-model="formData.taskName" 
                type="text" 
                :placeholder="placeholder"
              />
            </div>
          </form>
        </div>

        <div class="modal-footer">
          <button class="btn btn-secondary" @click="close">取消</button>
          <button class="btn btn-primary" @click="handleSubmit">创建</button>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  taskType: {
    type: String,
    required: true,
    validator: (value) => ['poll', 'question', 'barrage'].includes(value)
  },
  formData: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'submit'])

const title = computed(() => {
  const titles = {
    poll: '创建投票任务',
    question: '创建提问任务',
    barrage: '创建弹幕讨论'
  }
  return titles[props.taskType]
})

const inputLabel = computed(() => {
  const labels = {
    poll: '投票主题',
    question: '问题内容',
    barrage: '讨论主题'
  }
  return labels[props.taskType]
})

const placeholder = computed(() => {
  const placeholders = {
    poll: '如：本节课重点理解吗？',
    question: '请输入提问内容',
    barrage: '如：课堂讨论'
  }
  return placeholders[props.taskType]
})

const close = () => {
  emit('close')
}

const handleSubmit = () => {
  if (!props.formData.taskName || !props.formData.taskName.trim()) {
    alert('请输入内容')
    return
  }
  emit('submit')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  width: 90%;
  max-width: 500px;
  overflow: hidden;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid #e8eef5;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
  font-weight: 600;
}

.close-btn {
  background: none;
  border: none;
  font-size: 2rem;
  color: #999;
  cursor: pointer;
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.close-btn:hover {
  color: #333;
  transform: rotate(90deg);
}

.modal-body {
  padding: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-weight: 500;
  color: #333;
  margin-bottom: 0.8rem;
  font-size: 0.95rem;
}

.form-group input,
.form-group textarea {
  padding: 0.8rem;
  border: 1px solid #e8eef5;
  border-radius: 6px;
  font-size: 0.95rem;
  font-family: inherit;
  transition: all 0.3s ease;
  resize: vertical;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #4A90E2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.1);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding: 1.5rem;
  border-top: 1px solid #e8eef5;
  background: #f8f9fc;
}

.btn {
  padding: 0.7rem 1.5rem;
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
  background: #f0f0f0;
  color: #666;
}

.btn-secondary:hover {
  background: #e8e8e8;
}

/* 过渡动画 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
}
</style>
