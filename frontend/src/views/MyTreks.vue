<template>
  <Navbar />
  <div class="page">
    <h1>My Treks</h1>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="table-wrap">
      <table class="table" v-if="activeTreks.length">
        <thead>
          <tr>
            <th>Name</th><th>Location</th><th>Difficulty</th><th>Duration</th><th>Coordinator</th>
            <th>Booking Status</th><th>Trek Booking</th><th>Trek State</th><th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in activeTreks" :key="t.booking_id">
            <td>{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.difficulty }}</td>
            <td>{{ t.duration || '—' }}</td>
            <td>{{ t.coordinator_name || '—' }}</td>
            <td><span class="badge badge-blue">{{ t.status }}</span></td>
            <td><span class="badge" :class="t.trek_status === 'Open' ? 'badge-green' : 'badge-red'">{{ t.trek_status }}</span></td>
            <td><span class="badge" :class="stateBadge(t.trek_state)">{{ t.trek_state }}</span></td>
            <td><button class="btn btn-red btn-sm" @click="cancel(t)">Cancel</button></td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">You have no active treks.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { bookings: [], error: "", userId: null };
  },
  computed: {
    activeTreks() {
      return this.bookings.filter((b) => b.status === "Booked");
    },
  },
  mounted() {
    const u = JSON.parse(window.localStorage.getItem("user") || "null");
    this.userId = u ? u.id : null;
    this.load();
  },
  methods: {
    stateBadge(state) {
      if (state === "completed") return "badge-gray";
      if (state === "ongoing") return "badge-blue";
      return "badge-amber";
    },
    async load() {
      if (!this.userId) {
        this.error = "Please log in.";
        return;
      }
      try {
        this.bookings = await api.get(`/user/bookings/${this.userId}`);
      } catch (e) {
        this.error = e.message;
      }
    },
    async cancel(t) {
      if (!confirm(`Cancel your booking for "${t.name}"? This frees your slot.`)) return;
      try {
        await api.post("/cancel_booking", { user_id: this.userId, booking_id: t.booking_id });
        this.load();
      } catch (e) {
        alert(e.message);
      }
    },
  },
};
</script>
