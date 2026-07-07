import { createRouter, createWebHistory } from "vue-router"




const routes = [
   {
        path: "/",
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
        path: "/add_trek",
        component: () => import("../views/AddTrek.vue")
    },
    {
        path: "/Admin",
        component: () => import("../views/Admin.vue")
    },
    {
        path:'/trek_managment',
        component:()=>import('../views/TrekMangment.vue')
    },
     {
        path:'/add_staff',
        component:()=>import('../views/AddStaff.vue')
    },
   { path : '/staff_managment',
    component : () => import('../views/StaffMangment.vue')
},
{
    path:'/user_managment',
    component:()=>import('../views/UserMangment.vue')
},
{
    path:'/staff_dashboard',
    component:()=>import('../views/StaffDashboard.vue')
},
{
    path:'/bookings',
    component:()=>import('../views/Bookings.vue')
},
{
    path:'/statistics',
    component:()=>import('../views/Statistics.vue')
}
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router