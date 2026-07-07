<template>
  <Navbar />
  <div class="page">
    <h1>Manage Users</h1>
    <input class="input search-bar" v-model="search" placeholder="Search by name, email or ID" />
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="table-wrap">
      <table class="table" v-if="filtered.length">
        <thead>
          <tr><th>ID</th><th>Username</th><th>Email</th><th>Status</th><th>Total Treks</th><th>Actions</th></tr>
        </thead>
        <tbody>
          <tr v-for="u in filtered" :key="u.id">
            <td>{{ u.id }}</td>
            <td>{{ u.username }}</td>
            <td>{{ u.email }}</td>
            <td><span class="badge" :class="u.status === 'Blacklisted' ? 'badge-red' : 'badge-green'">{{ u.status }}</span></td>
            <td>{{ u.total_treks }}</td>
            <td>
              <div class="actions">
                <router-link class="btn btn-gray btn-sm" :to="`/admin/user-profile/${u.id}`">View Profile</router-link>
                <button v-if="u.status !== 'Blacklisted'" class="btn btn-amber btn-sm" @click="setStatus(u, 'Blacklisted')">Blacklist</button>
                <button v-else class="btn btn-primary btn-sm" @click="setStatus(u, 'Active')">Unblock</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No users found.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { users: [], search: "", error: "" };
  },
  computed: {
    filtered() {
      const term = this.search.trim().toLowerCase();
      if (!term) return this.users;
      return this.users.filter(
        (u) => u.username.toLowerCase().includes(term) ||
               u.email.toLowerCase().includes(term) ||
               String(u.id).includes(term)
      );
    },
  },
  mounted() {
    this.load();
  },
  methods: {
    async load() {
      try { this.users = await api.get("/all_users"); }
      catch (e) { this.error = e.message; }
    },
    async setStatus(u, status) {
      try { await api.post("/user/status", { id: u.id, status }); this.load(); }
      catch (e) { alert(e.message); }
    },
  },
};
</script>
