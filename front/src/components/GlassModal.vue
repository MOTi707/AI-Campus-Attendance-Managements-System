<template>
  <transition name="modal-fade">
    <div v-if="visible" class="modal-overlay" @click.self="close">
      <div class="modal-content" :class="modalClass">
        <div class="modal-icon">{{ iconEmoji }}</div>
        <div class="modal-message">{{ message }}</div>
        <button class="modal-close-btn" @click="close">关闭</button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  message: {
    type: String,
    default: '提示信息'
  },
  type: {
    type: String,
    default: 'info', // 'success', 'error', 'warning', 'info'
  }
})

const emit = defineEmits(['close'])

const close = () => {
  emit('close')
}

const iconEmoji = {
  success: '✅',
  error: '❌',
  warning: '⚠️',
  info: 'ℹ️'
}[props.type] || 'ℹ️'

const modalClass = {
  'modal-success': props.type === 'success',
  'modal-error': props.type === 'error',
  'modal-warning': props.type === 'warning',
  'modal-info': props.type === 'info'
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
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-radius: 12px;
  padding: 2rem;
  max-width: 400px;
  width: 90%;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.5);
  text-align: center;
  animation: slideUp 0.3s ease-out;
}

.modal-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
  display: block;
}

.modal-message {
  font-size: 1rem;
  color: #333;
  margin-bottom: 1.5rem;
  line-height: 1.6;
  word-break: break-word;
}

.modal-close-btn {
  background: linear-gradient(135deg, #4A90E2 0%, #357ABD 100%);
  color: white;
  border: none;
  border-radius: 6px;
  padding: 0.75rem 2rem;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.modal-close-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 144, 226, 0.3);
}

.modal-close-btn:active {
  transform: translateY(0);
}

/* 类型特定样式 */
.modal-success {
  border-left: 4px solid #51cf66;
}

.modal-error {
  border-left: 4px solid #ff6b6b;
}

.modal-warning {
  border-left: 4px solid #ffc107;
}

.modal-info {
  border-left: 4px solid #4A90E2;
}

/* 动画 */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.3s ease;
}

.modal-fade-enter-from,
.modal-fade-leave-to {
  opacity: 0;
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
</style>
