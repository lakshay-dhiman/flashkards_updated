import { createRouter, createWebHistory } from "vue-router";
import HomePage from '../components/HomePage'
import RegisterPage from '../components/RegisterPage'
import LoginPage from '../components/LoginPage'
import UserDecks from '../components/UserDecks'
import DeckCards from '../components/DeckCards'
import TestDownload from '../components/TestDownload'
import AllDecks from '../components/AllDecks'
import AllCards from '../components/AllCards'





const routes = [
    {
        path : '/',
        name: 'Home',
        component : HomePage
    },
    {
        path: '/register',
        name : 'Register',
        component: RegisterPage
    },
    {
        path: '/login',
        name : 'Login',
        component : LoginPage
    },
    {
        path: '/decks',
        name:'Decks',
        component : UserDecks
    },
    {
        path:'/cards/:id',
        name: "Cards",
        component : DeckCards
    },
    {
        path:'/test',
        name: "Test",
        component : TestDownload
    },
    {
        path:'/alldecks',
        name: "AllDecks",
        component : AllDecks
    },
    {
        path:'/allcards/:id',
        name: "AllCards",
        component : AllCards
    },


]

const router = createRouter({
    history : createWebHistory(process.env.BASE_URL),
    routes
})

export default router