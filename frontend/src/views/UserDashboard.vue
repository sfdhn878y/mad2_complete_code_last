<template>
  <Navbar />
  <div class="page">
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="card header-card" v-if="user">
      <div>
        <h1 style="margin:0 0 4px">Welcome, {{ user.username }}</h1>
        <p class="note" style="margin:0">{{ user.email }} &middot; <span class="badge badge-blue">{{ user.role }}</span></p>
      </div>
      <div class="actions">
        <router-link class="btn btn-gray" to="/view_profile">View Profile</router-link>
        <router-link v-if="user.profile_completed" class="btn btn-blue" to="/edit_profile">Edit Profile</router-link>
        <router-link v-else class="btn btn-primary" to="/complete_profile">Complete Profile</router-link>
      </div>
    </div>

    <h2 style="font-size:18px;margin:0 0 12px">My Booked Treks</h2>
    <div class="table-wrap">
      <table class="table" v-if="bookedTreks.length">
        <thead>
          <tr>
            <th>Name</th><th>Location</th><th>Duration</th><th>Coordinator</th>
            <th>Booking Status</th><th>Trek Booking</th><th>Trek State</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in bookedTreks" :key="t.booking_id">
            <td>{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.duration || '—' }}</td>
            <td>{{ t.coordinator_name || '—' }}</td>
            <td><span class="badge badge-blue">{{ t.status }}</span></td>
            <td><span class="badge" :class="t.trek_status === 'Open' ? 'badge-green' : 'badge-red'">{{ t.trek_status }}</span></td>
            <td><span class="badge" :class="stateBadge(t.trek_state)">{{ t.trek_state }}</span></td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">You haven't booked any treks yet. <router-link to="/current_treks">Browse current treks</router-link>.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { user: null, bookedTreks: [], error: "" };
  },
  mounted() {
    this.load();
  },
  methods: {
    stateBadge(state) {
      if (state === "completed") return "badge-gray";
      if (state === "ongoing") return "badge-blue";
      return "badge-amber";
    },
    async load() {
      const u = JSON.parse(window.localStorage.getItem("user") || "null");
      if (!u) {
        this.error = "Please log in.";
        return;
      }
      try {
        const data = await api.get(`/user/overview/${u.id}`);
        this.user = data.user;
        this.bookedTreks = data.booked_treks;
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
