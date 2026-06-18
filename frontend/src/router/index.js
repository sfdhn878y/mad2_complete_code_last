import { createRouter, createWebHistory } from "vue-router"

import Home from "../views/Home.vue"


const routes = [
    {
        path: "/",
        component: Home
    },
    {
        path: "/Register",
        component: () => import("../views/Register.vue")
    },
      {
        path: "/Login",
        component: () => import("../views/Login.vue")
    }
   
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router