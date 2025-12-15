import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../components/HomePage.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import ForgotPassword from '../components/ForgotPassword.vue'
import TeacherDashboard from '../components/TeacherDashboard.vue'
import MaterialsCenter from '../components/MaterialsCenter.vue'
import DocumentViewer from '../components/DocumentViewer.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/register',
    name: 'Register',
    component: Register
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword
  },
  {
    path: '/dashboard',
    name: 'TeacherDashboard',
    component: TeacherDashboard
  },
  {
    path: '/materials',
    name: 'MaterialsCenter',
    component: MaterialsCenter
  },
  {
    path: '/document-viewer',
    name: 'DocumentViewer',
    component: DocumentViewer
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router