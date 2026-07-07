<template>
  <Navbar />
  <div class="page">
    <h1>Participants — {{ trekName }}</h1>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="card">
      <ol v-if="participants.length" style="margin:0;padding-left:20px;line-height:2">
        <li v-for="p in participants" :key="p.booking_id">
          <b>{{ p.username }}</b> ({{ p.email }})
          <span class="badge badge-blue" style="margin-left:6px">{{ p.status }}</span>
        </li>
      </ol>
      <p v-else class="note">Nobody has booked this trek yet.</p>
    </div>

    <div class="actions" style="margin-top:16px">
      <router-link class="btn btn-gray" to="/manage_treks">Back to Manage Treks</router-link>
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
