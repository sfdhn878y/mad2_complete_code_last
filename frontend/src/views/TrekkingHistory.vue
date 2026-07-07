<template>
  <Navbar />
  <div class="page">
    <h1>Trekking History</h1>
    <p class="note">All your bookings — booked, completed, and cancelled.</p>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="table-wrap">
      <table class="table" v-if="bookings.length">
        <thead>
          <tr>
            <th>Name</th><th>Location</th><th>Difficulty</th><th>Booked On</th>
            <th>Booking Status</th><th>Trek Booking</th><th>Trek State</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in bookings" :key="t.booking_id">
            <td>{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.difficulty }}</td>
            <td>{{ formatDate(t.booked_at) }}</td>
            <td><span class="badge" :class="statusBadge(t.status)">{{ t.status }}</span></td>
            <td><span class="badge" :class="t.trek_status === 'Open' ? 'badge-green' : 'badge-red'">{{ t.trek_status }}</span></td>
            <td><span class="badge" :class="stateBadge(t.trek_state)">{{ t.trek_state }}</span></td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No booking history yet.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { bookings: [], error: "" };
  },
  mounted() {
    this.load();
  },
  methods: {
    formatDate(v) {
      return v ? new Date(v).toLocaleDateString() : "—";
    },
    statusBadge(status) {
      if (status === "Completed") return "badge-green";
      if (status === "Cancelled") return "badge-red";
      return "badge-blue";
    },
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
        this.bookings = await api.get(`/user/bookings/${u.id}`);
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
