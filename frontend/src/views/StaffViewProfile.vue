<template>
  <Navbar />
  <div class="page" v-if="profile">
    <h1>My Profile</h1>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="card" style="max-width:560px">
      <h2 style="margin:0 0 4px">{{ profile.full_name || profile.username }}</h2>
      <span class="badge badge-blue">{{ profile.role }}</span>
      <span class="badge" :class="profile.status === 'Approved' ? 'badge-green' : 'badge-amber'" style="margin-left:6px">
        {{ profile.status }}
      </span>

      <ul style="list-style:none;padding:0;margin:18px 0 0;font-size:14px;line-height:2.1">
        <li><b>Username:</b> {{ profile.username }}</li>
        <li><b>Email:</b> {{ profile.email }}</li>
        <li><b>Phone:</b> {{ profile.phone || '—' }}</li>
        <li><b>Age:</b> {{ profile.age || '—' }}</li>
        <li><b>Gender:</b> {{ profile.gender || '—' }}</li>
        <li><b>Address:</b> {{ profile.address || '—' }}</li>
        <li><b>Emergency Contact:</b> {{ profile.emergency_contact_name || '—' }} ({{ profile.emergency_contact_number || '—' }})</li>
        <li><b>Blood Group:</b> {{ profile.blood_group || '—' }}</li>
        <li><b>Medical Conditions:</b> {{ profile.medical_conditions || '—' }}</li>
        <li><b>Fitness Level:</b> {{ profile.fitness_level || '—' }}</li>
      </ul>

      <div class="actions" style="margin-top:18px">
        <router-link class="btn btn-blue" to="/staff/edit_profile">Edit Profile</router-link>
        <router-link class="btn btn-gray" to="/staff">Back to Dashboard</router-link>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { profile: null, error: "" };
  },
  mounted() {
    this.load();
  },
  methods: {
    async load() {
      const user = JSON.parse(window.localStorage.getItem("user") || "null");
      if (!user) {
        this.error = "Please log in.";
        return;
      }
      try {
        this.profile = await api.get(`/profile/${user.id}`);
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
