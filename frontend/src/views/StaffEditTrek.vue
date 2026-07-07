<template>
  <Navbar />
  <div class="page">
    <h1>Edit Trek</h1>
    <p class="note">Your changes are submitted for <b>admin approval</b> and only apply once approved.</p>

    <div class="card" style="margin-top:16px">
      <p v-if="error" class="error-msg">{{ error }}</p>
      <p v-if="message" class="note" style="color:#059669">{{ message }}</p>
      <div class="form-grid">
        <div class="form-field">
          <label>Trek Name</label>
          <input class="input" v-model="form.name" />
        </div>
        <div class="form-field">
          <label>Location</label>
          <input class="input" v-model="form.location" />
        </div>
        <div class="form-field">
          <label>Start Date</label>
          <input class="input" type="date" v-model="form.start_date" />
        </div>
        <div class="form-field">
          <label>End Date</label>
          <input class="input" type="date" v-model="form.end_date" />
        </div>
        <div class="form-field">
          <label>Duration</label>
          <input class="input" v-model="form.duration" />
        </div>
        <div class="form-field">
          <label>Total Slots (min {{ minSlots }})</label>
          <input class="input" type="number" :min="minSlots" v-model.number="form.slots" />
        </div>
      </div>
      <div style="margin-top:18px" class="actions">
        <button class="btn btn-primary" @click="submit">Save Changes</button>
        <router-link class="btn btn-gray" :to="`/staff/trek/${$route.params.id}`">Back to Trek</router-link>
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
    return {
      error: "", message: "", minSlots: 0, coordinatorId: null,
      form: { name: "", location: "", start_date: "", end_date: "", duration: "", slots: 0 },
    };
  },
  mounted() {
    const user = JSON.parse(window.localStorage.getItem("user") || "null");
    this.coordinatorId = user ? user.id : null;
    this.load();
  },
  methods: {
    async load() {
      try {
        const t = await api.get(`/staff/trek/${this.$route.params.id}`);
        this.minSlots = t.registered_count;
        this.form = {
          name: t.name || "",
          location: t.location || "",
          start_date: t.start_date || "",
          end_date: t.end_date || "",
          duration: t.duration || "",
          slots: t.slots || 0,
        };
      } catch (e) {
        this.error = e.message;
      }
    },
    async submit() {
      this.error = this.message = "";
      try {
        const res = await api.post("/staff/edit_trek", {
          trek_id: Number(this.$route.params.id),
          coordinator_id: this.coordinatorId,
          ...this.form,
        });
        this.message = res.message;
        setTimeout(() => this.$router.push(`/staff/trek/${this.$route.params.id}`), 800);
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
