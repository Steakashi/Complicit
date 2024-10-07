import user from "./user"

export default {

    create(room_name, user_id, user_name){
        const room = {
            name: room_name,
            users: [
                user.create(
                    user_id, 
                    user_name
                )
            ]
        }
        return room
    },

    get_client_room(rooms, client_id){
        for (let room_number = 0; room_number < rooms.length; room_number++) {
            let concerned_room = rooms[room_number]
            let users_id = concerned_room.users.map(user => user.id );
            if (users_id.includes(client_id)){
                return concerned_room
            }
        }

        return null
    }

}