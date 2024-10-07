import './style.css'
import typescriptLogo from './typescript.svg'
import viteLogo from '/vite.svg'
import { setupCounter } from './counter.ts'

// document.querySelector<HTMLDivElement>('#app')!.innerHTML = `
//   <div>
//     <a href="https://vitejs.dev" target="_blank">
//       <img src="${viteLogo}" class="logo" alt="Vite logo" />
//     </a>
//     <a href="https://www.typescriptlang.org/" target="_blank">
//       <img src="${typescriptLogo}" class="logo vanilla" alt="TypeScript logo" />
//     </a>
//     <h1>Vite + TypeScript</h1>
//     <div class="card">
//       <button id="counter" type="button"></button>
//     </div>
//     <p class="read-the-docs">
//       Click on the Vite and TypeScript logos to learn more
//     </p>
//   </div>
// `

// setupCounter(document.querySelector<HTMLButtonElement>('#counter')!)

function getOrCreateUserCookie() {
  const cookies = document.cookie.split('; ')
  const value = cookies
      .find(c => c.startsWith("complicitUser="))
      ?.split('=')[1]
  if (value === undefined) {
      userId = new Date().getTime();
      document.cookie = "complicitUser=" + userId
      return userId
  } 
  return decodeURIComponent(value)
}

var clientId = 2 //getOrCreateUserCookie();
console.log(clientId)
document.querySelector("#ws-id").textContent = clientId;
const ws = new WebSocket(`ws://localhost:8000/ws`);
ws.onmessage = function(event) {
  console.log('onmessage')
  var messages = document.getElementById('messages')
  var message = document.createElement('li')
  var content = document.createTextNode(event.data)
  message.appendChild(content)
  messages.appendChild(message)
};

function sendMessage(event) {
  var input = document.getElementById("messageText")
  ws.send('{"value": "value","action": "action"}')
  input.value = ''
  event.preventDefault()
}

function createRoom() {
  console.log('ok bb');
  // //var input = document.getElementById("messageText")
  // connection.send(inputData.value)
  // //connection.send('{"action": "create_room", "room_name": "roomtest"}')
  // input.value = ''
  // event.preventDefault()
}