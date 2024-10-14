import room from '../../api/room';
import router from '../../router'
import * as notifier from '../../notifier'             


    // TODO : reset answer when game is ended
const state = () => ({
    clientId: null,
    userName: '',
    currentRoom: null,
    rooms: [],
    users: [],
    websocket: null,
    game: null,
    answer: '',
})

const actions = {

    send({commit}, data) {
        commit('send', data); 
    }
}

const mutations = {
    success(state, data){ notifier.success(data.success) },
    error(state, data){ notifier.error(data.error); },

    register_client_id(state, clientId){
        state.clientId = clientId;
    },

    send () { return; },

    synchronize(state, data){
        state.currentRoom = room.get_client_room(data.rooms, state.clientId);
        state.rooms = data.rooms;
        state.users = data.users;
    },

    retrieve_user(state, data){
        state.userName = data.user.name;
    },

    update_user_name(state, data){
        state.userName = data.user.name;    
        notifier.success(data.success);
    },

    launch_game(state, data){
        state.game = data.game;
        router.push('/game').then(() => notifier.success(data.success));
    },

    register_answer(state, data){
        state.answer = data.answer;
        notifier.success(data.success);
    },

    trigger_associations_phase(state, data){
        state.game = data.game
        console.log('next step !')
    }

}

export default {
    state,
    actions,
    mutations
}

