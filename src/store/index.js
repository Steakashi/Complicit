import { createStore } from 'vuex'
import { nanoid } from 'nanoid'

import createWebSocketPlugin from './plugins/websocket'
import websocket from './modules/websocket'

function getOrCreateUserCookie() {
  const cookies = document.cookie.split('; ')
  const value = cookies
      .find(c => c.startsWith("complicitUser="))
      ?.split('=')[1]
  if (value === undefined) {
      const generatedClientId = nanoid();
      document.cookie = "complicitUser=" + generatedClientId + "; SameSite=Strict";
      return generatedClientId
  } 
  return decodeURIComponent(value)
}

const clientId = getOrCreateUserCookie();
const websocketInstance = new WebSocket("ws://localhost:8000/ws/" + clientId);
const plugin = createWebSocketPlugin(websocketInstance)

const store = createStore({
  modules: {
    websocket: websocket
  },
  plugins: [plugin]
})

export default store


store.commit("register_client_id", clientId)

