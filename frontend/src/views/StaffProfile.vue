<template>
  <Navbar />
  <div class="page" v-if="staff">
    <router-link class="btn btn-gray" to="/manage_staff">← Back</router-link>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="card" style="max-width:520px;margin-top:16px">
      <h1 style="margin:0 0 4px">{{ staff.full_name || staff.username }}</h1>
      <span class="badge" :class="statusBadge(staff.status)">{{ staff.status }}</span>
      <ul style="list-style:none;padding:0;margin:18px 0 0;font-size:14px;line-height:2.1">
        <li><b>ID:</b> #{{ staff.id }}</li>
        <li><b>Username:</b> {{ staff.username }}</li>
        <li><b>Email:</b> {{ staff.email }}</li>
        <li><b>Phone:</b> {{ staff.phone || '—' }}</li>
      </ul>
    </div>

    <h2 style="font-size:18px;margin:24px 0 12px">Managed Treks</h2>
    <div class="table-wrap">
      <table class="table" v-if="staff.managed_treks && staff.managed_treks.length">
        <thead>
          <tr><th>ID</th><th>Name</th><th>Location</th><th>Price</th><th>Date</th><th>Total Bookings</th></tr>
        </thead>
        <tbody>
          <tr v-for="t in staff.managed_treks" :key="t.id">
            <td>{{ t.id }}</td>
            <td>{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td></td>
            <td>{{ t.start_date || '' }}</td>
            <td>{{ t.total_bookings }}</td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No treks assigned.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { staff: null, error: "" };
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
      try { this.staff = await api.get(`/staff_profile/${this.$route.params.id}`); }
      catch (e) { this.error = e.message; }
    },
  },
};
</script>
