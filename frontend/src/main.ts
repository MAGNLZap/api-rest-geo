import { createApp } from 'vue'
import App from './App.vue'
import favicon from '@portal/ecuador_hero.svg'
import './styles/institutional-tokens.css'
import './styles/control-tokens.css'
import './styles/selects.css'
import './styles/text-fields.css'
import './styles/interactions.css'

const icon = document.createElement('link')
icon.rel = 'icon'
icon.type = 'image/svg+xml'
icon.href = favicon
document.head.appendChild(icon)
createApp(App).mount('#app')
