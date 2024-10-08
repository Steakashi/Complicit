export default function createWebSocketPlugin (websocket) {
    return (store) => {
        // websocket.addEventListener("open", (event) => {
        //     store.dispatch("send", {'action': 'synchronize'})
        // })
        websocket.onmessage = function(response) {
            let data = JSON.parse(response.data)
            store.commit(data['action'], data)
        }
        store.subscribe(mutation => {
            let data = JSON.stringify(mutation.payload)
            if (mutation.type === 'send'){ websocket.send(data) }
        })
    }
};
