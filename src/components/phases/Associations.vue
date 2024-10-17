<script setup>

  import { useRoute, useRouter } from 'vue-router'
  import { onMounted, ref, reactive, computed } from 'vue'

  import store from '../../store'
  import router from '../../router'
  import send from '../../api/send'

  const allZonesFilled = ref(null)
  const alreadyFilledUserName = ref(null)
  const alreadyFilledAnswer = ref(null)
  const answersLength = ref(null)

  const currentRoom = computed(() => { return store.state.websocket.currentRoom })

  const users = computed(() => { 
    let allUsers = [];
    let pairedUserID = store.state.websocket.currentRoom.game.pairs[store.state.websocket.clientId];

    for(let i=0; i<store.state.websocket.currentRoom.users.length; i++){
      if (store.state.websocket.currentRoom.users[i].id != pairedUserID){
        allUsers.push(store.state.websocket.currentRoom.users[i]);
      }
      else{
        alreadyFilledUserName.value = store.state.websocket.currentRoom.users[i].name
      }
    }

    return shuffleArray(allUsers);
  })

  const answers = computed(() => { 
    let allAnswers = {...store.state.websocket.currentRoom.game.answers};
    alreadyFilledAnswer.value = allAnswers[store.state.websocket.clientId];
    delete allAnswers[store.state.websocket.clientId];

    answersLength.value = Object.keys(allAnswers).length
    return shuffleArray(allAnswers);
  })

  function retrieveUser(givenUsers, userID){
    for (let i=0; i<Object.keys(givenUsers).length; i++){
      if (givenUsers[i].id === userID){ return givenUsers[i]; }
    }
  }

  function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      const temp = array[i];
      array[i] = array[j];
      array[j] = temp;
    }
    return array
  }

  function allAnswersFilled(){
    for (let i=1; i<Object.keys(store.state.websocket.currentRoom.game.pairs).length; i++){
      let dropZone = document.getElementById("drop-zone-" + i)
      if ((dropZone === null) || !(dropZone.firstChild)){ return false; }
    } 

    return true;
  }

  const startDrag = (ev) => {
    ev.dataTransfer.setData("elementID", ev.target.id);
    ev.dataTransfer.setData("elementParentID", ev.target.parentNode.id);

    ev.dataTransfer.effectAllowed = "move";
  }

  const dragHover = (ev) => {
    ev.preventDefault();
    ev.dataTransfer.dropEffect = "move";
  }

  const onDrop = (ev) => {
    ev.preventDefault();

    const movedElementID = ev.dataTransfer.getData("elementID");
    const sourceNode = document.getElementById(movedElementID);
    const targetNode = ev.target;

    if (movedElementID === ev.target.id){ return; }
    else if (ev.target.id.startsWith('answer')){
      const sourceParentNodeID = ev.dataTransfer.getData("elementParentID");
      const sourceParentNode = document.getElementById(sourceParentNodeID);
      const targetParentNode = ev.target.parentNode
      
      sourceParentNode.appendChild(targetNode);
      targetParentNode.appendChild(sourceNode);

    }
    else { 
      targetNode.appendChild(sourceNode); 
      if ((allAnswersFilled()) && (allZonesFilled.value.disabled = true)) { allZonesFilled.value.disabled = false; }
    }
  }

</script>

<template>

  <div class="container mx-auto w-[64rem]">

    <div class="mt-16 text-center text-lg italic font-bold">
      <h2>Your theme is</h2>
      <hr class="h-0.5 border-t-0 bg-neutral-100 dark:bg-white/10" />
    </div>

    <div class="mt-60"></div>
    <div class="flex flex-row rounded-lg bg-base-200 m-1 p-2 empty:hidden">
      <div class="bg-gradient-to-r from-cyan-900 via-teal-900 to-lime-900 flex rounded-lg fit-content px-4 pt-[2px] text-gray-50 border-2 border-base-100 h-8 hover:cursor-pointer" :id="'answer-'+ index" v-for="(answer, index) in answers" :key=index draggable="true" @dragstart="startDrag($event)">
        {{ answer }}
      </div>
    </div>


    <div class="grid grid-cols-2 gap-4">
      <span class="text-center bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-transparent bg-clip-text font-bold">Users</span>
      <span class="text-center bg-gradient-to-r from-cyan-500 via-teal-500 to-lime-500 text-transparent bg-clip-text font-bold">Answers</span>
    </div>

    <hr class="h-0.5 border-t-0 bg-neutral-100 dark:bg-white/10 my-2"/>

    <div class="grid grid-cols-2 gap-4 -ml-3">
      <div>
        <div class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-gray-50 hover:cursor-not-allowed my-1 px-4 pt-1 grid grid-cols-1 gap-4 h-8 rounded-lg">
          {{ alreadyFilledUserName }}
        </div>
        <div class="bg-gradient-to-r from-indigo-950 via-purple-950 to-pink-950 text-gray-50 hover:cursor-not-allowed my-1 px-4 pt-1 grid grid-cols-1 gap-4 h-8 rounded-lg" v-for="user in users">
          {{ user.name }}
        </div>
      </div>
      <div id="drop-zones">
        <div class="bg-gradient-to-r from-cyan-500 via-teal-500 to-lime-500 text-gray-50 hover:cursor-not-allowed my-1 px-4 pt-1 grid grid-cols-1 gap-4 h-8 rounded-lg">
          {{ alreadyFilledAnswer }} {{ answersLength  }}
        </div>
        <div class="bg-base-200 grid grid-cols-1 gap-4 h-8 my-1 rounded-lg" v-for="index in answersLength" :key="index" :id="'drop-zone-' + index" @drop="onDrop($event)" @dragover="dragHover($event)">
        </div>
        <div class="flex justify-end mt-2">
          <button ref="allZonesFilled" type="submit" disabled class="btn btn-success" role="button">
            <span>Validate pairs</span>  
          </button>
        </div>
        
      </div>
    </div>

    <div class="flex flex-row py-3">
      <span class="flex mr-1" v-for="user in currentRoom.users">
        <span class="flex w-fit bg-base-200 p-2 rounded-lg" :class="user.game_status == 'ANSWERED' ? 'bg-green-600': 'bg-orange-600' ">
          <span class="flex text-neutral-300" v-if="user.game_status == 'ANSWERED'">
            {{ user.name }}
            <svg class="flex h-7 pl-1 w-6 fill-green-600 stroke-neutral-300" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <g id="Interface / Check"> <path id="Vector" d="M6 12L10.2426 16.2426L18.727 7.75732" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path> </g> </g></svg>
          </span>
          <span class="flex text-neutral-300" v-else>
            {{ user.name }}
            <svg class="flex h-7 pl-1 w-11 fill-neutral-300" id="Layer_1" data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><g id="SVGRepo_bgCarrier" stroke-width="0"></g><g id="SVGRepo_tracerCarrier" stroke-linecap="round" stroke-linejoin="round"></g><g id="SVGRepo_iconCarrier"> <path class="cls-1" d="M8,6.5A1.5,1.5,0,1,1,6.5,8,1.5,1.5,0,0,1,8,6.5ZM.5,8A1.5,1.5,0,1,0,2,6.5,1.5,1.5,0,0,0,.5,8Zm12,0A1.5,1.5,0,1,0,14,6.5,1.5,1.5,0,0,0,12.5,8Z"></path> </g></svg>
          </span>
        </span>
      </span>
    </div>

  </div>

</template>