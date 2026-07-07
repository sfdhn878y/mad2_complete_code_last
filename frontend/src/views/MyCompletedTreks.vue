<template>
  <Navbar />
  <div class="page">
    <h1>My Completed Treks</h1>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="table-wrap">
      <table class="table" v-if="completed.length">
        <thead>
          <tr>
            <th>Name</th><th>Location</th><th>Difficulty</th><th>Booked On</th>
            <th>Booking Status</th><th>Trek State</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in completed" :key="t.booking_id">
            <td>{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.difficulty }}</td>
            <td>{{ formatDate(t.booked_at) }}</td>
            <td><span class="badge badge-green">{{ t.status }}</span></td>
            <td><span class="badge badge-gray">{{ t.trek_state }}</span></td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">You have no completed treks yet.</p>
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
  computed: {
    completed() {
      return this.bookings.filter((b) => b.status === "Completed");
    },
  },
  mounted() {
    this.load();
  },
  methods: {
    formatDate(v) {
      return v ? new Date(v).toLocaleDateString() : "—";
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
