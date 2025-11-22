import { createApp } from 'vue'
import App from './App.vue'

// 创建Naive UI通用配置
const meta = document.createElement('meta')
meta.name = 'naive-ui-style'
document.head.appendChild(meta)

createApp(App).mount('#app')
