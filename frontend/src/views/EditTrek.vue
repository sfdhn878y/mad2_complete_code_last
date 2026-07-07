<template>
  <Navbar />
  <div class="page">
    <h1>Edit Trek</h1>

    <div class="card" style="margin-top:16px">
      <p v-if="error" class="error-msg">{{ error }}</p>
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
          <label>Difficulty</label>
          <select class="input" v-model="form.difficulty">
            <option>Easy</option>
            <option>Moderate</option>
            <option>Hard</option>
          </select>
        </div>
        <div class="form-field">
          <label>Duration</label>
          <input class="input" v-model="form.duration" />
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
          <label>Slots</label>
          <input class="input" type="number" min="0" v-model.number="form.slots" />
        </div>
        <div class="form-field">
          <label>Assigned Staff</label>
          <select class="input" v-model="form.coordinator_id">
            <option value="">Select staff</option>
            <option v-for="s in staff" :key="s.id" :value="s.id">{{ s.username }}</option>
          </select>
        </div>
      </div>
      <div style="margin-top:18px" class="actions">
        <button class="btn btn-primary" @click="submit">Save Changes</button>
        <router-link class="btn btn-gray" to="/manage_treks">Back to Manage Treks</router-link>
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
      staff: [],
      error: "",
      form: {
        name: "", location: "", difficulty: "Easy", duration: "",
        start_date: "", end_date: "", slots: 0, coordinator_id: "",
      },
    };
  },
  mounted() {
    this.load();
  },
  methods: {
    async load() {
      try {
        this.staff = await api.get("/all_staff");
        const t = await api.get(`/admin/trek_details/${this.$route.params.id}`);
        this.form = {
          name: t.name || "",
          location: t.location || "",
          difficulty: t.difficulty || "Easy",
          duration: t.duration || "",
          start_date: t.start_date || "",
          end_date: t.end_date || "",
          slots: t.slots || 0,
          coordinator_id: t.coordinator_id || "",
        };
      } catch (e) {
        this.error = e.message;
      }
    },
    async submit() {
      this.error = "";
      try {
        await api.put(`/admin/edit_trek/${this.$route.params.id}`, {
          ...this.form,
          coordinator_id: this.form.coordinator_id || null,
        });
        this.$router.push("/manage_treks");
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
