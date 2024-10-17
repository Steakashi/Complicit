<script setup>

  import { useRoute, useRouter } from 'vue-router'
  import { onMounted, ref, reactive, computed } from 'vue'

  import store from '../../store'
  import router from '../../router'
  import send from '../../api/send'
  import Answer from './Answer.vue'

  const themeAnswer = defineModel()

  const AnswerValidationButton = ref(null)  

  const answer = computed(() => {
    updateButtonVisibility();
    return store.state.websocket.answer; 
  })
  const pairedUser = computed(() => {
    let pairedUserID = store.state.websocket.currentRoom.game.pairs[store.state.websocket.clientId]
    for (let i=0; i<store.state.websocket.currentRoom.users.length; i++){
      if (store.state.websocket.currentRoom.users[i].id == pairedUserID){
        return store.state.websocket.currentRoom.users[i]
      }
    }
  })

  const currentRoom = computed(() => {
    return store.state.websocket.currentRoom 
  })

  function updateButtonVisibility(){
    if (AnswerValidationButton.value && store.state.websocket.answer != null){
      AnswerValidationButton.value.disabled = themeAnswer.value === store.state.websocket.answer
    }
  }

  function validateAnswer() { 
    send.validate_answer(
      store.state.websocket.currentRoom.name, 
      store.state.websocket.currentRoom.game.id, 
      themeAnswer.value
    ); 
  }

  function show_users_states(){

  }

  themeAnswer.value = store.state.websocket.answer

</script>

<template>

  <div class="container mx-auto w-[64rem]">

    <div class="mt-16 text-center text-lg italic font-bold">
      <h2>Your theme is</h2>
      <hr class="h-0.5 border-t-0 bg-neutral-100 dark:bg-white/10" />
    </div>

    <div class="flex-row bg-base-200 mt-60 p-3 rounded-lg">
      <div class="flex justify-center text-center font-semibold">
        <h3 cass="pt-2">Now let's find a good fit for your comrade,</h3>
        <div class=" border-2 border-dashed pb-1 px-4 mx-2 border-slate-500 rounded-lg bg-gradient-to-r from-pink-900 via-indigo-900 to-green-900">
          <span class=" bg-gradient-to-r from-pink-100 via-indigo-100 to-green-100 bg-clip-text font-bold text-transparent">
            {{ pairedUser.name }}
          </span>
        </div>
      </div>
      <form @submit.prevent="validateAnswer" class="flex flex-row p-2">
        <input type="text" v-model="themeAnswer" v-on:input="updateButtonVisibility()" placeholder="Choose a good thing that fits the theme !" class="placeholder-gray-600 placeholder:italic py-2 px-4 mr-2 w-10/12" @keyup.enter="submit" required>
        <button ref="AnswerValidationButton" type="submit" class="btn btn-success" :class="{'btn-warning': answer}" role="button">
          <span v-if="answer">Update answer</span>
          <span v-else>Validate answer</span>  
        </button>
      </form>
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