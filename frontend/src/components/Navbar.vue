<template>
  <nav>
    <div class="nav-brand">TrekManager</div>
    <div class="nav-links">
      <template v-if="loggedIn">
        <template v-if="role === 'admin'">
          <router-link to="/admin">Home</router-link>
          <router-link to="/manage_treks">Manage Treks</router-link>
          <router-link to="/manage_staff">Manage Staff</router-link>
          <router-link to="/manage_users">Manage Users</router-link>
          <router-link to="/admin/bookings">Bookings</router-link>
        </template>

        <template v-else-if="role === 'staff'">
          <router-link to="/staff">Home</router-link>
          <router-link to="/assigned_treks">Manage Treks</router-link>
        </template>

        <template v-else>
          <router-link to="/user/dashboard">Home</router-link>
          <router-link to="/my_treks">My Treks</router-link>
          <router-link to="/current_treks">Current Treks</router-link>
          <router-link to="/all_treks">All Treks</router-link>
          <router-link to="/trekking_history">Trekking History</router-link>
          <router-link to="/my_bookings">My Completed Treks</router-link>
        </template>

        <button class="logout-btn" @click.prevent="logout">Logout</button>
      </template>

      <template v-else>
        <router-link to="/login">Login</router-link>
        <router-link to="/register">Signup</router-link>
      </template>
    </div>
  </nav>
</template>

<script>
export default {
  data() {
    return {
      loggedIn: !!window.localStorage.getItem("token"),
      role: (() => {
        const user = JSON.parse(window.localStorage.getItem("user") || "null");
        return user ? user.role : "";
      })(),
    };
  },
  methods: {
    logout() {
      window.localStorage.removeItem("token");
      window.localStorage.removeItem("user");
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 24px;
  background-color: #1f2937;
  color: #fff;
}
.nav-brand {
  font-weight: 700;
  font-size: 18px;
  color: #34d399;
}
.nav-links {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}
a {
  color: #e5e7eb;
  text-decoration: none;
  font-size: 14px;
}
a:hover {
  color: #fff;
}
a.router-link-exact-active {
  color: #34d399;
  font-weight: 600;
}
.logout-btn {
  background: #ef4444;
  color: #fff;
  border: none;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}
.logout-btn:hover {
  background: #dc2626;
}
</style>
