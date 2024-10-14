<script setup>
  import { computed, shallowRef } from 'vue'

  import store from '../store'

  import Answer from './phases/Answer.vue'
  import Associations from './phases/Associations.vue'

  const phases = {
    1: Answer,
    2: Associations
  }

  const activeComponent = shallowRef(Answer)

  const game = computed(() => { 
    if (!store.state.websocket.game){ return; }
    activeComponent.value = phases[store.state.websocket.game.phase] 
    return store.state.websocket.game; 
  })
  const theme = computed(() => { return store.state.websocket.game.theme; })
  const answer = computed(() => {
    if (store.state.websocket.answer) { updateButtonVisibility(); }
    return store.state.websocket.answer; 
  })
  const pairedUser = computed(() => {
    let pairedUserID = store.state.websocket.game.pairs[store.state.websocket.clientId]
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
    AnswerValidationButton.value.disabled = themeAnswer.value === store.state.websocket.answer
  }

  function validateAnswer() { 
    send.validate_answer(
      store.state.websocket.currentRoom.name, 
      store.state.websocket.game.id, 
      themeAnswer.value
    ); 
  }

</script>


<style>

.content-enter-active,
.content-leave-active {
  transition: all .5s ease;
}

.content-enter-from{
  transform: translateX(-200px);
  opacity: 0;
}

.content-leave-to{
  transform: translateX(200px);
  opacity: 0;
}

.theme-enter-active{
  /* transition: all 2s ease; */
  animation: bounce-in 2s;
}


.theme-leave-active{
  animation: bounce-in 2s reverse;
}

/* .theme-enter-from,
.theme-leave-to {
  animation-delay: 2s;
  transform: translateX(200px);
  opacity: 50;
} */

@keyframes bounce-in {
  0% {
    transform: translateY(120px) scale(0);
  }
  25% {
    transform: translateY(120px) scale(0);
  }
  50% {
    transform: translateY(-120px) scale(1.25);
  }
  100% {
    transform: translateY(-76px) scale(1);
  }
}

</style>

<template>
  
  <div v-if="!game">
    
    <div role="alert" class="container mx-auto w-[64rem] mt-8 alert alert-error">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        class="h-6 w-6 shrink-0 stroke-current"
        fill="none"
        viewBox="0 0 24 24">
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
      <span>No game has been found. Try to recreate room from lobby.</span>
    </div>
  </div>

  <div v-else>

    <Transition name="theme" appear>
      <div>
        
        <div>
          <div v-for="index in 300" class="stylized_cell"></div>

          <div class="stylized_content">
            <div v-for="index in 10" class="stylized_css">{{ theme }}</div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- <Transition name="slide-fade"><Answer v-if="game.phase===1"/></Transition>
    <Transition name="slide-fade"><Associations v-if="game.phase===2"/></Transition> -->

    <Transition name="content" appear>
      <component :is="activeComponent"></component>
      <!-- <Answer v-if="game.phase===1"/> -->
    </Transition>
    <!-- <Transition>
      <component :is="activeComponent"></component>
      <Associations v-if="game.phase===2"/>
    </Transition> -->

    
    

  </div>
  
</template>