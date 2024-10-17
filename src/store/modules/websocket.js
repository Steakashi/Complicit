import room from '../../api/room';
import router from '../../router'
import * as notifier from '../../notifier'             


// @TODO : reset answer when game is ended
const state = () => ({
    clientId: null,
    userName: '',
    currentRoom: null,
    rooms: [],
    users: [],
    websocket: null,
    answer: null,
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
        
        if (state.currentRoom && state.currentRoom.game){
            const targetedPairId = state.currentRoom.game.pairs[state.clientId]
            state.answer = state.currentRoom.game.answers[targetedPairId]
        }
    },

    retrieve_user(state, data){
        state.userName = data.user.name;
    },

    update_user_name(state, data){
        state.userName = data.user.name;    
        notifier.success(data.success);
    },

    launch_game(state, data){
        router.push('/play').then(() => notifier.success(data.success));
    },

    register_answer(state, data){
        state.answer = data.answer;
        notifier.success(data.success);
    },

    trigger_associations_phase(state, data){
        return
    }

}

export default {
    state,
    actions,
    mutations
}

