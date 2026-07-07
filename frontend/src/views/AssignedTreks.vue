<template>
  <Navbar />
  <div class="page">
    <h1>Allocated Treks</h1>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <h2 style="font-size:18px;margin:8px 0 12px">Active Treks</h2>
    <div class="table-wrap" style="margin-bottom:28px">
      <table class="table" v-if="activeTreks.length">
        <thead>
          <tr>
            <th>Name</th><th>Location</th><th>Start</th><th>End</th><th>Duration</th>
            <th>Participants</th><th>Slots</th><th>Booking</th><th>State</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in activeTreks" :key="t.id">
            <td>{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.start_date || '—' }}</td>
            <td>{{ t.end_date || '—' }}</td>
            <td>{{ t.duration || '—' }}</td>
            <td>{{ t.registered_count }}</td>
            <td>{{ t.slots }}</td>
            <td><span class="badge" :class="t.trek_status === 'Open' ? 'badge-green' : 'badge-red'">{{ t.trek_status }}</span></td>
            <td><span class="badge" :class="stateBadge(t.trek_state)">{{ t.trek_state }}</span></td>
            <td><router-link class="btn btn-blue btn-sm" :to="`/staff/trek/${t.id}`">Manage Trek</router-link></td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No active treks.</p>
    </div>

    <h2 style="font-size:18px;margin:0 0 12px">Completed Treks</h2>
    <div class="table-wrap">
      <table class="table" v-if="completedTreks.length">
        <thead>
          <tr><th>Name</th><th>Location</th><th>Duration</th><th>Participants</th><th>Actions</th></tr>
        </thead>
        <tbody>
          <tr v-for="t in completedTreks" :key="t.id">
            <td>{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.duration || '—' }}</td>
            <td>{{ t.total_bookings }}</td>
            <td><router-link class="btn btn-gray btn-sm" :to="`/staff/trek/${t.id}/participants`">View Participants</router-link></td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No completed treks yet.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { treks: [], error: "" };
  },
  computed: {
    activeTreks() {
      return this.treks.filter((t) => t.trek_state !== "completed");
    },
    completedTreks() {
      return this.treks.filter((t) => t.trek_state === "completed");
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
      const user = JSON.parse(window.localStorage.getItem("user") || "null");
      if (!user) {
        this.error = "Please log in as staff.";
        return;
      }
      try {
        const data = await api.get(`/staff/overview/${user.id}`);
        this.treks = data.treks;
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
