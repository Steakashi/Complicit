import { createApp } from 'vue'
import App from './App.vue'
import store from './store'
import Vue3Toasity, { type ToastContainerOptions } from 'vue3-toastify';
import FloatingVue from 'floating-vue'
import 'vue3-toastify/dist/index.css';


var app = createApp(App)
app.use(store)
app.use(FloatingVue)
app.use(
    Vue3Toasity,
    {
      autoClose: 3000,
    } as ToastContainerOptions,
)
app.mount('#app')

