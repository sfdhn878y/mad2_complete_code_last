<template>
  <Navbar />
  <div class="page">
    <h1>Registered Users — {{ trekName }}</h1>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="table-wrap">
      <table class="table" v-if="participants.length">
        <thead>
          <tr><th>ID</th><th>Username</th><th>Email</th><th>Phone</th><th>Full Name</th></tr>
        </thead>
        <tbody>
          <tr v-for="p in participants" :key="p.booking_id">
            <td>{{ p.user_id }}</td>
            <td>{{ p.username }}</td>
            <td>{{ p.email }}</td>
            <td>{{ p.phone || '—' }}</td>
            <td>{{ p.full_name || '—' }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No registered users yet.</p>
    </div>

    <div class="actions" style="margin-top:16px">
      <router-link class="btn btn-blue" :to="`/staff/trek/${$route.params.id}`">Back to Trek</router-link>
      <router-link class="btn btn-gray" to="/staff">Back to Dashboard</router-link>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { trekName: "", participants: [], error: "" };
  },
  mounted() {
    this.load();
  },
  methods: {
    async load() {
      try {
        const data = await api.get(`/view_participants/${this.$route.params.id}`);
        this.trekName = data.trek_name;
        this.participants = data.participants;
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
