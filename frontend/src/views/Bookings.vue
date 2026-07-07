<template>
  <Navbar />
  <div class="page">
    <h1>All Bookings</h1>
    <input class="input search-bar" v-model="search" placeholder="Search by user, trek name or ID" />
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="table-wrap">
      <table class="table" v-if="filtered.length">
        <thead>
          <tr>
            <th>Booking ID</th><th>User</th><th>User ID</th><th>Trek</th><th>Trek ID</th>
            <th>Location</th><th>Difficulty</th><th>Trek State</th><th>Booking Status</th><th>Booked At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="b in filtered" :key="b.id">
            <td>{{ b.id }}</td>
            <td>{{ b.username }}</td>
            <td>{{ b.user_id }}</td>
            <td>{{ b.trek_name }}</td>
            <td>{{ b.trek_id }}</td>
            <td>{{ b.location }}</td>
            <td>{{ b.difficulty }}</td>
            <td><span class="badge badge-blue">{{ b.trek_state }}</span></td>
            <td><span class="badge" :class="statusBadge(b.booking_status)">{{ b.booking_status }}</span></td>
            <td>{{ formatDate(b.booked_at) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No bookings found.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { bookings: [], search: "", error: "" };
  },
  computed: {
    filtered() {
      const term = this.search.trim().toLowerCase();
      if (!term) return this.bookings;
      return this.bookings.filter(
        (b) => b.username.toLowerCase().includes(term) ||
               b.trek_name.toLowerCase().includes(term) ||
               String(b.id).includes(term) ||
               String(b.trek_id).includes(term)
      );
    },
  },
  mounted() {
    this.load();
  },
  methods: {
    statusBadge(status) {
      if (status === "Completed") return "badge-green";
      if (status === "Cancelled") return "badge-red";
      return "badge-blue";
    },
    formatDate(v) {
      return v ? new Date(v).toLocaleString() : "—";
    },
    async load() {
      try { this.bookings = await api.get("/all_bookings"); }
      catch (e) { this.error = e.message; }
    },
  },
};
</script>
