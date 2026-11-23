import { createApp } from 'vue'
import App from './App.vue'
import favicon from '@portal/ecuador_hero.svg'

const icon = document.createElement('link')
icon.rel = 'icon'
icon.type = 'image/svg+xml'
icon.href = favicon
document.head.appendChild(icon)
createApp(App).mount('#app')
