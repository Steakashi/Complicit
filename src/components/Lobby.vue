<script setup>

  import store from '../store'
  import router from '../router'
  import send from '../api/send'
  import { onMounted, ref, reactive, computed } from 'vue'

  import 'floating-vue/dist/style.css'

  const roomName = defineModel()

  const lobbyCheckbox = ref(null)
  const UpdateNameButton = ref(null)  
  const updatedUserName = ref(null)
  const lobbyButton = ref(null)
  const lobbyError = ref(null)

  const clientId = computed(() => { return store.state.websocket.clientId; })
  const rooms = computed(() => { return store.state.websocket.rooms; })
  const users = computed(() => { return store.state.websocket.users; })
  const gameInProgress = computed(() => { return store.state.websocket.currentRoom.game_in_progress; })
  const userName = computed(() => {
    updatedUserName.value = store.state.websocket.userName;
    if (UpdateNameButton.value){ UpdateNameButton.value.hidden = true; }
    return store.state.websocket.userName;
  })
  const currentRoom = computed(() => {
    if (store.state.websocket.currentRoom){ 
      lobbyCheckbox.value.checked = false;
    }
    return store.state.websocket.currentRoom 
  })
  const lobbyTooltip = computed(() => {
    if (!(store.state.websocket.currentRoom)) { return; }
    else {
      if (store.state.websocket.currentRoom.game_in_progress) { return "Re-join already started game." }
      else if (store.state.websocket.currentRoom.users.length == 1) { return "There is not enough players to launch game."; }
      else if (store.state.websocket.currentRoom.leader.id != store.state.websocket.clientId) { return "Only the leader of the room can launch game."; }
      else return;
    }
  })

  function createRoom() { send.create_room(roomName.value); }
  function joinRoom(joinedRoomName) { send.join_room(joinedRoomName); }
  function leaveRoom(roomNameToLeave) { send.leave_room(roomNameToLeave); }
  function updateUserName() { send.update_user_name(updatedUserName.value); }

  function updateButtonVisibility(){
    UpdateNameButton.value.hidden = updatedUserName.value === store.state.websocket.userName
  }

  function checkRoomNameValidity(){
    let isInvalid = store.state.websocket.rooms.map(room => {
      return room.name.toLowerCase();
    }).includes(roomName.value.toLowerCase()); 
    lobbyButton.value.disabled = isInvalid
    lobbyError.value.className = isInvalid ? "" : "hidden"
  }

  function launchGame(roomName) {
    if (store.state.websocket.currentRoom.game_in_progress) { router.push('/play'); }
    else send.launch_game(roomName);
  }

</script>

<template>
                
  <div class="container mx-auto w-[64rem] mt-8">
    <div class="flex flex-row">
      <h2 class="text-xl font-bold dark:text-white">Welcome back 
        <input class="ml-2 p-2 bg-base-200" v-model="updatedUserName" v-on:input="updateButtonVisibility()">
        <div class="hidden">{{ userName }}</div>
      </h2>
      <button ref="UpdateNameButton" class="ml-2 -mt-0.5 btn btn-outline btn-success" hidden @click="updateUserName()">Update</button>
    </div>
      <div>
      <div v-if="!currentRoom" class="block my-8 p-6 border-dashed border-4 border-neutral rounded-lg text-center text-lg font-normal text-gray-500">
        <p>Please create a new room or join an existing one.</p>
      </div>
      <div v-else class="justify-between flex block my-8 p-6 border-4 border-neutral-content bg-neutral rounded-lg text-center text-lg font-normal">
          <div class="flex flex-row">
            <p>You are in room <b>{{ currentRoom.name }}</b> with {{ currentRoom.users.length - 1 }} other players.</p>
            <ul class="flex flex-row pl-5">
              <li v-for="user in currentRoom.users">
                <div class="tooltip block cursor-default" :data-tip="user.name">
                  <span v-if="user.id == clientId">🦖</span>
                  <span v-else>🦔</span>
                </div>
              </li>
            </ul>
          </div>
          <div class="flex flex-row">
            
            <div v-tooltip="{
                  content: lobbyTooltip,
                  disabled: (!(lobbyTooltip))
              }">
              <button @click="launchGame(currentRoom.name)" 
                class="btn btn-outline mr-6"
                :class="gameInProgress ? 'btn-warning': 'btn-success'"
                :disabled="!(lobbyTooltip)"
                >
                <span v-if="gameInProgress">Re-join game</span>
                <span v-else="gameInProgress">Launch game</span>
              </button>
            </div>

            <div @click="leaveRoom(currentRoom.name)" v-tooltip="'Leave room'">
              <svg class="w-11 fill-neutral-900 hover:fill-neutral-950 hover:cursor-pointer" xmlns="http://www.w3.org/2000/svg" id="Layer_1" data-name="Layer 1" viewBox="0 0 24 24">
                <path d="m23.473,16.247l-2.862,2.863-1.414-1.414,1.696-1.696h-6.892v-2h6.956l-1.76-1.761,1.414-1.414,2.862,2.862c.706.706.706,1.854,0,2.56Zm-9.473,1.753h2v5.999H0V4.199C0,2.775,1.014,1.538,2.411,1.258L8.412.057c.886-.174,1.793.051,2.491.622.428.351.728.812.908,1.319h1.19c1.654,0,3,1.346,3,3v7.001h-2v-7.001c0-.552-.449-1-1-1h-1v18h2v-3.999Zm-4.999-5.501c0-.829-.672-1.501-1.501-1.501s-1.501.672-1.501,1.501.672,1.501,1.501,1.501,1.501-.672,1.501-1.501Z"/>
              </svg>
            </div>
          </div>

      </div>
    </div>

    <div 
      v-tooltip="{
        content: 'You can not create new room because you are already in a room.',
        disabled: (!(currentRoom))
      }">
        <div class="text-center collapse bg-base-200 my-5" >
        <input ref="lobbyCheckbox" type="checkbox" :disabled="currentRoom"/>
        <div class="collapse-title text-xl font-medium" :class="{ 'opacity-30': currentRoom }">Create Room</div>
        <div class="collapse-content">
          <form @submit.prevent="createRoom" class="flex flex-row">
            <input type="text" v-model="roomName" class="p-1 mr-2" @keyup.enter="submit" :disabled="currentRoom" v-on:input="checkRoomNameValidity()" required>
            <button type="submit" ref="lobbyButton" class="btn btn-success" role="button" :disabled="currentRoom">
              Create Room
            </button>
            <span class="p-3 italic opacity-70 text-error"><p ref="lobbyError" class="hidden">A room already exists with this name.</p></span>
          </form>
        </div>
      </div>
    </div>

    <div class="text-center collapse bg-base-200 my-5">
      <input type="checkbox" checked/>
      <div class="collapse-title text-xl font-medium">Join Room</div>
      <div class="collapse-content flex flex-row">
        <div v-if="rooms.length === 0">
          <p>There is currently no available room.</p>
        </div>
        <div 
          v-else v-for="room in rooms" 
          class="flex flex-row"
          v-tooltip="{
            content: 'Join room',
            disabled: currentRoom == room
          }">
          <button 
            @click="joinRoom(room.name)"
            class="btn m-1 btn-success pointer-events-none flex flex-row" 
            :class="{ 'btn-outline pointer-events-auto': currentRoom != room }"
          >
            {{ room.name }}
            <ul class="flex flex-row p-3">
              <li v-for="user in room.users">
                <span v-if="user.id == clientId">🦖</span>
                <span v-else>🦔</span>
              </li>
            </ul>
          </button>
        </div>
      </div>
    </div>
    <div class="collapse">
      <input type="checkbox" class="peer text-gray-500"/>
      <div class="collapse-title italic opacity-40 [.peer:checked+&]:opacity-70">
        See connected users
      </div>
      <div class="collapse-content opacity-70">
        <ul>
          <li class=" text-sm flex flex-row" v-for="user in users">
            <span 
              class="w-2 h-2 m-2 rounded-full shadow-xl" 
              :class="{'bg-success': user.status == 'CONNECTED', 'bg-neutral': user.status == 'DISCONNECTED'}">
            </span>
            <span>{{ user.name }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
  
  
</template>


