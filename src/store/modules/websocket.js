import { toast } from 'vue3-toastify';
import room from '../../api/room';

const notify_error = (error) => {
    toast.error(error, {
        autoClose: 2000,
    });
}

const notify_success = (success) => {
    toast.success(success, {
        autoClose: 2000,
    });
}

const state = () => ({
    clientId: null,
    userName: '',
    currentRoom: null,
    rooms: [],
    websocket: null
})

const actions = {

    send({commit}, data) {
        commit('send', data); 
    }
}

const mutations = {
    success(state, data){ notify_success(data.success) },
    error(state, data){ notify_error(data.error); },

    register_client_id(state, clientId){
        state.clientId = clientId
    },

    send () { return; },

    synchronize(state, data){
        state.currentRoom = room.get_client_room(data.rooms, state.clientId);
        state.rooms = data.rooms;
        state.users = data.users;
    },

    retrieve_user(state, data){
        state.userName = data.user.name
    },

    update_user_name(state, data){
        state.userName = data.user.name
        notify_success(data.success)
    },

    create_room(state, data){
        // #TODO : maybe move that in another call ?
        // if (data.client_id == state.clientId){ 
        //state.currentRoom = data.room;
        notify_success(data.success)
        // }
    
        // state.rooms.push(
        //     data.room
        // );
    },

    join_room(state, data){
        // #TODO : maybe move that in another call ?
        // #TODO : just getting repeated at each call, we need to improve this.
        // state.currentRoom = room.get_client_room(data.rooms, state.clientId) 
        // state.rooms = data.rooms;
        notify_success(data.success)
    },

    leave_room(state, data){
        // state.currentRoom = room.get_client_room(data.rooms, state.clientId) 
        // state.rooms = data.rooms;
        notify_success(data.success)
    }

}

export default {
    state,
    actions,
    mutations
}

