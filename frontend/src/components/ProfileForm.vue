<template>
  <div class="card" style="margin-top:16px">
    <p v-if="error" class="error-msg">{{ error }}</p>
    <div class="form-grid">
      <div class="form-field">
        <label>Full Name</label>
        <input class="input" v-model="form.full_name" />
      </div>
      <div class="form-field">
        <label>Phone</label>
        <input class="input" v-model="form.phone" />
      </div>
      <div class="form-field">
        <label>Age</label>
        <input class="input" type="number" min="0" v-model.number="form.age" />
      </div>
      <div class="form-field">
        <label>Gender</label>
        <select class="input" v-model="form.gender">
          <option value="">Select</option>
          <option>Male</option>
          <option>Female</option>
          <option>Other</option>
        </select>
      </div>
      <div class="form-field full">
        <label>Address</label>
        <input class="input" v-model="form.address" />
      </div>
      <div class="form-field">
        <label>Emergency Contact Name</label>
        <input class="input" v-model="form.emergency_contact_name" />
      </div>
      <div class="form-field">
        <label>Emergency Contact Number</label>
        <input class="input" v-model="form.emergency_contact_number" />
      </div>
      <div class="form-field">
        <label>Blood Group</label>
        <input class="input" v-model="form.blood_group" />
      </div>
      <div class="form-field">
        <label>Fitness Level</label>
        <select class="input" v-model="form.fitness_level">
          <option value="">Select</option>
          <option>Beginner</option>
          <option>Intermediate</option>
          <option>Advanced</option>
        </select>
      </div>
      <div class="form-field full">
        <label>Medical Conditions</label>
        <input class="input" v-model="form.medical_conditions" placeholder="None, or list any" />
      </div>
    </div>
    <div style="margin-top:18px" class="actions">
      <button class="btn btn-primary" @click="submit">{{ submitLabel }}</button>
      <router-link class="btn btn-gray" :to="backTo">Cancel</router-link>
    </div>
  </div>
</template>

<script>
import { api } from "../api.js";

export default {
  props: {
    submitLabel: { type: String, default: "Save Profile" },
    redirectTo: { type: String, default: "/staff/view_profile" },
    backTo: { type: String, default: "/staff" },
  },
  data() {
    return {
      error: "",
      userId: null,
      form: {
        full_name: "", phone: "", age: null, gender: "", address: "",
        emergency_contact_name: "", emergency_contact_number: "",
        blood_group: "", medical_conditions: "", fitness_level: "",
      },
    };
  },
  mounted() {
    const user = JSON.parse(window.localStorage.getItem("user") || "null");
    this.userId = user ? user.id : null;
    this.load();
  },
  methods: {
    async load() {
      if (!this.userId) return;
      try {
        const p = await api.get(`/profile/${this.userId}`);
        for (const key of Object.keys(this.form)) {
          if (p[key] !== null && p[key] !== undefined) this.form[key] = p[key];
        }
      } catch (e) {
        this.error = e.message;
      }
    },
    async submit() {
      this.error = "";
      try {
        await api.post(`/profile/${this.userId}`, this.form);
        this.$router.push(this.redirectTo);
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
