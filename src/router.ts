import { createWebHistory, createRouter } from 'vue-router'

import Lobby from './components/Lobby.vue'
import Game from './components/Game.vue'

const routes = [
  { path: '/', component: Lobby },
  { path: '/game', component: Game },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router