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

  const users = computed(() => { 
    let allUsers = [];
    let pairedUserID = store.state.websocket.game.pairs[store.state.websocket.clientId];

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
    for (let i=1; i<Object.keys(store.state.websocket.game.pairs).length - 1; i++){
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
      <div class="flex rounded-lg fit-content px-4 border-2 border-base-100 border-dashed h-8 hover:cursor-pointer" :id="'answer-'+ index" v-for="(answer, index) in answers" :key=index draggable="true" @dragstart="startDrag($event)">
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
        <div class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-gray-100 hover:cursor-not-allowed my-1 px-4 pt-1 grid grid-cols-1 gap-4 h-8 rounded-lg">
          {{ alreadyFilledUserName }}
        </div>
        <div class="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-gray-100 hover:cursor-not-allowed my-1 px-4 pt-1 grid grid-cols-1 gap-4 h-8 rounded-lg" v-for="user in users">
          {{ user.name }}
        </div>
      </div>
      <div id="drop-zones">
        <div class="bg-gradient-to-r from-cyan-500 via-teal-500 to-lime-500 text-gray-100 hover:cursor-not-allowed my-1 px-4 pt-1 grid grid-cols-1 gap-4 h-8 rounded-lg">
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

  </div>

</template>