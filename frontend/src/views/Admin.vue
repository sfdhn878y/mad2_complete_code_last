<template>
  <Navbar />
  <div class="page">
    <div class="stats-grid">
      <div class="stat-box">
        <div class="value">{{ stats.total_treks ?? 0 }}</div>
        <div class="label">Total Treks</div>
      </div>
      <div class="stat-box">
        <div class="value">{{ stats.total_users ?? 0 }}</div>
        <div class="label">Total Users</div>
      </div>
      <div class="stat-box">
        <div class="value">{{ stats.total_staff ?? 0 }}</div>
        <div class="label">Trek Staff</div>
      </div>
      <div class="stat-box">
        <div class="value">{{ stats.total_bookings ?? 0 }}</div>
        <div class="label">Total Bookings</div>
      </div>
    </div>

    <div class="card header-card">
      <h1 style="margin:0">Admin Dashboard</h1>
      <div class="actions">
        <router-link class="btn btn-primary" to="/add_treak">+ Add Trek</router-link>
        <router-link class="btn btn-primary" to="/add_staff">+ Add Staff</router-link>
        <router-link class="btn btn-blue" to="/admin/bookings">View All Bookings</router-link>
      </div>
    </div>

    <input class="input search-bar" v-model="search" placeholder="Search treks by name or ID" />

    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="cards-grid">
      <div class="card" v-for="trek in filteredTreks" :key="trek.id">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <h3 style="margin:0 0 6px">{{ trek.name }}</h3>
          <span class="badge" :class="stateBadge(trek.trek_state)">{{ trek.trek_state }}</span>
        </div>
        <p class="note" style="margin:2px 0">ID #{{ trek.id }} &middot; {{ trek.location }}</p>
        <ul style="list-style:none;padding:0;margin:10px 0;font-size:13px;line-height:1.9">
          <li><b>Dates:</b> {{ trek.start_date || '—' }} → {{ trek.end_date || '—' }}</li>
          <li><b>Duration:</b> {{ trek.duration || '—' }}</li>
          <li><b>Slots:</b> {{ trek.slots }} ({{ trek.registered_count }} booked)</li>
          <li><b>Staff:</b> {{ trek.coordinator_name || 'Not Assigned' }}</li>
          <li>
            <b>Booking:</b>
            <span class="badge" :class="trek.trek_status === 'Open' ? 'badge-green' : 'badge-red'">
              {{ trek.trek_status }}
            </span>
          </li>
        </ul>
        <div class="actions">
          <button
            v-if="trek.trek_status === 'Open'"
            class="btn btn-amber btn-sm"
            @click="toggleBooking(trek)">Close Trek</button>
          <button
            v-else-if="trek.trek_state === 'upcoming'"
            class="btn btn-primary btn-sm"
            @click="toggleBooking(trek)">Open Trek</button>

          <router-link class="btn btn-blue btn-sm" :to="`/admin/edit_treak/${trek.id}`">Edit</router-link>
          <button class="btn btn-red btn-sm" @click="deleteTrek(trek)">Delete Trek</button>
        </div>
      </div>
    </div>
    <p v-if="!filteredTreks.length" class="note">No treks found.</p>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { stats: {}, treks: [], search: "", error: "" };
  },
  computed: {
    filteredTreks() {
      const term = this.search.trim().toLowerCase();
      if (!term) return this.treks;
      return this.treks.filter(
        (t) => t.name.toLowerCase().includes(term) || String(t.id).includes(term)
      );
    },
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
      try {
        this.stats = await api.get("/stats");
        this.treks = await api.get("/all_treks");
      } catch (e) {
        this.error = e.message;
      }
    },
    async toggleBooking(trek) {
      try {
        await api.post(`/admin/toggle_booking/${trek.id}`);
        this.load();
      } catch (e) {
        alert(e.message);
      }
    },
    async deleteTrek(trek) {
      if (!confirm(`Delete "${trek.name}" and all its bookings?`)) return;
      try {
        await api.del(`/delete_trek/${trek.id}`);
        this.load();
      } catch (e) {
        alert(e.message);
      }
    },
  },
};
</script>
