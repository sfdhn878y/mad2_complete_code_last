<template>
  <Navbar />
  <div class="page" v-if="trek">
    <h1>{{ trek.name }}</h1>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="card">
      <ul style="list-style:none;padding:0;margin:0;font-size:14px;line-height:2;columns:2">
        <li><b>ID:</b> #{{ trek.id }}</li>
        <li><b>Location:</b> {{ trek.location }}</li>
        <li><b>Difficulty:</b> {{ trek.difficulty }}</li>
        <li><b>Start Date:</b> {{ trek.start_date || '—' }}</li>
        <li><b>End Date:</b> {{ trek.end_date || '—' }}</li>
        <li><b>Duration:</b> {{ trek.duration || '—' }}</li>
        <li><b>Slots:</b> {{ trek.slots }}</li>
        <li><b>Registered Participants:</b> {{ trek.registered_count }}</li>
        <li><b>Assigned Staff:</b> {{ trek.coordinator_name || 'Not Assigned' }}</li>
        <li><b>Booking Status:</b> {{ trek.trek_status }}</li>
        <li><b>Trek State:</b> {{ trek.trek_state }}</li>
      </ul>
      <div class="actions" style="margin-top:16px">
        <router-link class="btn btn-blue" :to="`/admin/edit_treak/${trek.id}`">Edit Trek</router-link>
        <router-link class="btn btn-gray" to="/manage_treks">Back to Manage Treks</router-link>
      </div>
    </div>

    <h2 style="font-size:18px;margin:24px 0 12px">Participants</h2>
    <div class="table-wrap">
      <table class="table" v-if="trek.participants && trek.participants.length">
        <thead>
          <tr><th>ID</th><th>Username</th><th>Email</th><th>Booking Status</th><th>Booked At</th></tr>
        </thead>
        <tbody>
          <tr v-for="p in trek.participants" :key="p.booking_id">
            <td>{{ p.user_id }}</td>
            <td>{{ p.username }}</td>
            <td>{{ p.email }}</td>
            <td><span class="badge badge-blue">{{ p.status }}</span></td>
            <td>{{ formatDate(p.booked_at) }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No participants yet.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { trek: null, error: "" };
  },
  mounted() {
    this.load();
  },
  methods: {
    formatDate(v) {
      return v ? new Date(v).toLocaleString() : "—";
    },
    async load() {
      try {
        this.trek = await api.get(`/admin/trek_details/${this.$route.params.id}`);
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
