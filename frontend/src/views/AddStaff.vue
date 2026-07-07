<template>
  <Navbar />
  <div class="page">
    <h1>Add Staff</h1>
    <div class="card" style="max-width:460px">
      <p v-if="errorData" class="error-msg">{{ errorData }}</p>
      <p v-if="success" class="note" style="color:#059669">{{ success }}</p>
      <div class="form-field" style="margin-bottom:12px">
        <label>Username</label>
        <input class="input" v-model="staff_name" placeholder="Staff username" />
      </div>
      <div class="form-field" style="margin-bottom:12px">
        <label>Email</label>
        <input class="input" v-model="staff_email" placeholder="Staff email" />
      </div>
      <div class="form-field" style="margin-bottom:16px">
        <label>Password</label>
        <input class="input" type="password" v-model="staff_password" placeholder="Password" />
      </div>
      <p class="note">New staff are created as <b>Approved</b> and can log in right away.</p>
      <div class="actions" style="margin-top:14px">
        <button class="btn btn-primary" @click="add_staff">Add Staff</button>
        <router-link class="btn btn-gray" to="/manage_staff">Back to Manage Staff</router-link>
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
      staff_name: "",
      staff_email: "",
      staff_password: "",
      errorData: null,
      success: "",
    };
  },
  methods: {
    async add_staff() {
      this.errorData = null;
      this.success = "";
      if (!this.staff_name || !this.staff_email || !this.staff_password) {
        this.errorData = "All fields are required";
        return;
      }
      try {
        await api.post("/add_staff", {
          username: this.staff_name,
          email: this.staff_email,
          password: this.staff_password,
        });
        this.success = "Staff added successfully";
        this.staff_name = this.staff_email = this.staff_password = "";
      } catch (e) {
        this.errorData = e.message;
      }
    },
  },
};
</script>
