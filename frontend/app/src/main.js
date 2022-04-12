import { createApp } from 'vue'
import App from './App.vue'
import router from './routes/routes'
import store from './store/store.js'
// import { createStore } from 'vuex'

// const store = createStore({
//     state () {
//       return {
//         loggedin : false,
//         user_email : null
//       }
//     },
//     mutations: {
//         user_login(state,value){
//             state.loggedin = value
//         },
//         setEmail(state,email){
//             state.user_email = email
//         }
//     },
//     getters : {
//         returnLoggedIn(state){
//             return state.loggedin
//         },
//         retrunEmail(state){
//             return state.user_email
//         }
//     }
// })

createApp(App).use(router).use(store).mount('#app')
