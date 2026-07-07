import { createRouter, createWebHistory } from "vue-router"

const routes = [
    { path: "/", component: () => import("../views/Home.vue") },
    { path: "/Register", component: () => import("../views/Register.vue") },
    { path: "/Login", component: () => import("../views/Login.vue") },

    // ----- Admin dashboard -----
    { path: "/admin", component: () => import("../views/Admin.vue") },
    { path: "/add_treak", component: () => import("../views/AddTrek.vue") },
    { path: "/manage_treks", component: () => import("../views/TrekMangment.vue") },
    { path: "/admin/trek_details/:id", component: () => import("../views/TrekDetails.vue") },
    { path: "/admin/edit_treak/:id", component: () => import("../views/EditTrek.vue") },
    { path: "/manage_staff", component: () => import("../views/StaffMangment.vue") },
    { path: "/manage_users", component: () => import("../views/UserMangment.vue") },
    { path: "/admin/user-profile/:id", component: () => import("../views/UserProfile.vue") },
    { path: "/staff_profile/:id", component: () => import("../views/StaffProfile.vue") },
    { path: "/admin/bookings", component: () => import("../views/Bookings.vue") },
    { path: "/view_participants/:id", component: () => import("../views/ViewParticipants.vue") },

    // ----- Staff dashboard -----
    { path: "/staff", component: () => import("../views/StaffDashboard.vue") },
    { path: "/assigned_treks", component: () => import("../views/AssignedTreks.vue") },
    { path: "/staff/trek/:id", component: () => import("../views/StaffTrek.vue") },
    { path: "/edit_treak/:id", component: () => import("../views/StaffEditTrek.vue") },
    { path: "/staff/trek/:id/participants", component: () => import("../views/StaffParticipants.vue") },
    { path: "/staff/complete_profile", component: () => import("../views/StaffCompleteProfile.vue") },
    { path: "/staff/edit_profile", component: () => import("../views/StaffEditProfile.vue") },
    { path: "/staff/view_profile", component: () => import("../views/StaffViewProfile.vue") },

    // ----- User dashboard -----
    { path: "/user/dashboard", component: () => import("../views/UserDashboard.vue") },
    { path: "/current_treks", component: () => import("../views/CurrentTreks.vue") },
    { path: "/all_treks", component: () => import("../views/AllTreks.vue") },
    { path: "/my_treks", component: () => import("../views/MyTreks.vue") },
    { path: "/my_bookings", component: () => import("../views/MyCompletedTreks.vue") },
    { path: "/trekking_history", component: () => import("../views/TrekkingHistory.vue") },
    { path: "/complete_profile", component: () => import("../views/UserCompleteProfile.vue") },
    { path: "/edit_profile", component: () => import("../views/UserEditProfile.vue") },
    { path: "/view_profile", component: () => import("../views/UserViewProfile.vue") },
    { path: "/view_coordinator_profile/:id", component: () => import("../views/CoordinatorProfile.vue") },

    // ----- legacy helpers -----
    { path: "/add_staff", component: () => import("../views/AddStaff.vue") },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router
