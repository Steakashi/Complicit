import store from '../store'

const SEND = "send"

export default {

    synchronize(){
        store.dispatch(
            SEND, 
            {
                action: "synchronize"
            }
        ) 
    },

    create_room(room_name){
        store.dispatch(
            SEND, 
            {
                action: "create_room",
                room_name: room_name
            }
        ) 
    },

    join_room(room_name){
        store.dispatch(
            SEND,
            {
                action: "join_room",
                room_name: room_name,
            }
        )
    },

    leave_room(room_name){
        store.dispatch(
            SEND,
            {
                action: "leave_room",
                room_name: room_name
            }
        )
    },

    update_user_name(user_name){
        store.dispatch(
            SEND,
            {
                action: "update_user_name",
                user_name: user_name
            }
        )
    },

    launch_game(room_name){
        store.dispatch(
            SEND,
            {
                action: "launch_game",
                room_name: room_name
            }
        )
    },

    validate_answer(room_name,game_id, answer){
        store.dispatch(
            SEND,
            {
                action: "register_answer",
                room_name: room_name,
                game_id: game_id,
                answer: answer
            }
        )
    }

}