<template>
  <Navbar />
  <div class="auth-wrap">
    <div class="auth-card">
      <h2 class="auth-title">Create your account</h2>
      <p class="auth-sub">Sign up to browse and book treks</p>

      <p v-if="success" class="auth-success">{{ success }}</p>
      <p v-if="error" class="auth-error">{{ error }}</p>

      <form @submit.prevent="register">
        <div class="auth-field">
          <label>Username</label>
          <input v-model="username" type="text" placeholder="Choose a username" required />
        </div>
        <div class="auth-field">
          <label>Email</label>
          <input v-model="email" type="email" placeholder="you@example.com" required />
        </div>
        <div class="auth-field">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="Create a password" required />
        </div>
        <button class="auth-btn" type="submit" :disabled="loading">
          {{ loading ? "Creating..." : "Sign Up" }}
        </button>
      </form>

      <p class="auth-foot">
        Already have an account?
        <router-link to="/login">Log in</router-link>
      </p>
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
      username: "",
      email: "",
      password: "",
      success: "",
      error: "",
      loading: false,
    };
  },
  methods: {
    async register() {
      this.error = this.success = "";
      this.loading = true;
      try {
        await api.post("/register", {
          username: this.username,
          email: this.email,
          password: this.password,
        });
        this.success = "Account created! Redirecting to login...";
        setTimeout(() => this.$router.push("/login"), 1200);
      } catch (e) {
        this.error = e.message;
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.auth-wrap {
  min-height: calc(100vh - 60px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 16px;
  background: linear-gradient(135deg, #ecfdf5 0%, #eff6ff 100%);
}
.auth-card {
  background: #fff;
  width: 100%;
  max-width: 400px;
  padding: 32px;
  border-radius: 14px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}
.auth-title {
  margin: 0 0 4px;
  font-size: 22px;
  color: #111827;
}
.auth-sub {
  margin: 0 0 22px;
  color: #6b7280;
  font-size: 14px;
}
.auth-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 16px;
}
.auth-field label {
  font-size: 13px;
  font-weight: 600;
  color: #374151;
}
.auth-field input {
  padding: 10px 12px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
}
.auth-field input:focus {
  border-color: #059669;
  box-shadow: 0 0 0 3px rgba(5, 150, 105, 0.15);
}
.auth-btn {
  width: 100%;
  padding: 11px;
  background: #059669;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  margin-top: 4px;
}
.auth-btn:hover { background: #047857; }
.auth-btn:disabled { opacity: 0.6; cursor: not-allowed; }
.auth-foot {
  text-align: center;
  margin: 20px 0 0;
  font-size: 14px;
  color: #6b7280;
}
.auth-foot a { color: #059669; font-weight: 600; text-decoration: none; }
.auth-error {
  background: #fee2e2;
  color: #991b1b;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px;
  margin: 0 0 16px;
}
.auth-success {
  background: #d1fae5;
  color: #065f46;
  padding: 10px 12px;
  border-radius: 8px;
  font-size: 14px;
  margin: 0 0 16px;
}
</style>
