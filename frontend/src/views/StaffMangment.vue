<template>
  <Navbar />
  <div class="page">
    <div class="header-card card">
      <h1 style="margin:0">Manage Staff</h1>
      <router-link class="btn btn-primary" to="/add_staff">+ Add Staff</router-link>
    </div>

    <input class="input search-bar" v-model="search" placeholder="Search by name, email or ID" />
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="table-wrap">
      <table class="table" v-if="filtered.length">
        <thead>
          <tr><th>ID</th><th>Username</th><th>Email</th><th>Status</th><th>Profile</th><th>Actions</th></tr>
        </thead>
        <tbody>
          <tr v-for="s in filtered" :key="s.id">
            <td>{{ s.id }}</td>
            <td>{{ s.username }}</td>
            <td>{{ s.email }}</td>
            <td><span class="badge" :class="statusBadge(s.status)">{{ s.status }}</span></td>
            <td>
              <router-link class="btn btn-gray btn-sm" :to="`/staff_profile/${s.id}`">View Profile</router-link>
            </td>
            <td>
              <div class="actions">
                <button v-if="s.status !== 'Approved'" class="btn btn-primary btn-sm" @click="setStatus(s, 'Approved')">Approve</button>
                <button v-if="s.status !== 'Blacklisted'" class="btn btn-amber btn-sm" @click="setStatus(s, 'Blacklisted')">Blacklist</button>
                <button class="btn btn-red btn-sm" @click="remove(s)">Remove</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No staff found.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { staff: [], search: "", error: "" };
  },
  computed: {
    filtered() {
      const term = this.search.trim().toLowerCase();
      if (!term) return this.staff;
      return this.staff.filter(
        (s) => s.username.toLowerCase().includes(term) ||
               s.email.toLowerCase().includes(term) ||
               String(s.id).includes(term)
      );
    },
  },
  mounted() {
    this.load();
  },
  methods: {
    statusBadge(status) {
      if (status === "Approved") return "badge-green";
      if (status === "Blacklisted") return "badge-red";
      return "badge-amber";
    },
    async load() {
      try { this.staff = await api.get("/all_staff"); }
      catch (e) { this.error = e.message; }
    },
    async setStatus(s, status) {
      try { await api.post("/staff/status", { id: s.id, status }); this.load(); }
      catch (e) { alert(e.message); }
    },
    async remove(s) {
      if (!confirm(`Permanently remove staff "${s.username}"?`)) return;
      try { await api.del(`/staff/remove/${s.id}`); this.load(); }
      catch (e) { alert(e.message); }
    },
  },
};
</script>
