import { createRouter, createWebHistory } from "vue-router"




const routes = [
   {
        path: "/Home",
        component: () => import("../views/Home.vue")
    },
    {
        path: "/Register",
        component: () => import("../views/Register.vue")
    },
    {
        path: "/Login",
        component: () => import("../views/Login.vue")
    },
    {
        path: "/Coordinator",
        component: () => import("../views/Coordinator.vue")
    },
    {
        path: "/Add_trek",
        component: () => import("../views/AddTrek.vue")
    },
    {
        path: "/Admin",
        component: () => import("../views/Admin.vue")
    }

]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router