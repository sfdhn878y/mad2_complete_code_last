<template>
  <Navbar />
  <div class="page" v-if="user">
    <router-link class="btn btn-gray" to="/manage_users">← Back</router-link>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="card" style="max-width:520px;margin-top:16px">
      <h1 style="margin:0 0 4px">{{ user.username }}</h1>
      <span class="badge badge-blue">{{ user.role }}</span>
      <span class="badge" :class="user.verified ? 'badge-green' : 'badge-red'" style="margin-left:6px">
        {{ user.verified ? 'Verified' : 'Not Verified' }}
      </span>

      <ul style="list-style:none;padding:0;margin:18px 0 0;font-size:14px;line-height:2.1">
        <li><b>ID:</b> #{{ user.id }}</li>
        <li><b>Full Name:</b> {{ user.full_name || '—' }}</li>
        <li><b>Email:</b> {{ user.email }}</li>
        <li><b>Phone:</b> {{ user.phone || '—' }}</li>
        <li><b>Status:</b> {{ user.status }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { user: null, error: "" };
  },
  mounted() {
    this.load();
  },
  methods: {
    async load() {
      try { this.user = await api.get(`/admin/user_profile/${this.$route.params.id}`); }
      catch (e) { this.error = e.message; }
    },
  },
};
</script>
