export default {

    create(user_id, user_name){
        const user = {
            id: user_id,
            name: user_name,
        }
        return user
    }

}