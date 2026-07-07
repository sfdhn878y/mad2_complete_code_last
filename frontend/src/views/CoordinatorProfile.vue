<template>
  <Navbar />
  <div class="page" v-if="coordinator">
    <h1>Coordinator Profile</h1>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="card" style="max-width:460px">
      <h2 style="margin:0 0 10px">{{ coordinator.full_name || coordinator.username }}</h2>
      <ul style="list-style:none;padding:0;margin:0;font-size:14px;line-height:2.1">
        <li><b>Username:</b> {{ coordinator.username }}</li>
        <li><b>Email:</b> {{ coordinator.email }}</li>
        <li><b>Phone:</b> {{ coordinator.phone || '—' }}</li>
      </ul>
      <div class="actions" style="margin-top:16px">
        <button class="btn btn-gray" @click="$router.back()">← Back</button>
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
    return { coordinator: null, error: "" };
  },
  mounted() {
    this.load();
  },
  methods: {
    async load() {
      try {
        this.coordinator = await api.get(`/view_coordinator_profile/${this.$route.params.id}`);
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
