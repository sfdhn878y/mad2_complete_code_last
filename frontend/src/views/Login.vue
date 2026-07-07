<template>
  <Navbar />
  <div class="auth-wrap">
    <div class="auth-card">
      <h2 class="auth-title">Welcome back</h2>
      <p class="auth-sub">Log in to your account</p>

      <p v-if="message" class="auth-error">{{ message }}</p>

      <form @submit.prevent="login">
        <div class="auth-field">
          <label>Email</label>
          <input v-model="email"  placeholder="you@example.com" required />
        </div>
        <div class="auth-field">
          <label>Password</label>
          <input v-model="password" type="password" placeholder="Enter your password" required />
        </div>
        <button class="auth-btn" type="submit" :disabled="loading">
          {{ loading ? "Logging in..." : "Log In" }}
        </button>
      </form>

      <p class="auth-foot">
        Don't have an account?
        <router-link to="/register">Sign up</router-link>
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
      email: "",
      password: "",
      message: "",
      loading: false,
    };
  },
  methods: {
    async login() {
      this.message = "";
      this.loading = true;
      try {
        const data = await api.post("/login", {
          email: this.email,
          password: this.password,
        });
        localStorage.setItem("token", data.token);
        localStorage.setItem("user", JSON.stringify(data.user));

        if (data.user.role === "admin") {
          this.$router.push("/admin");
        } else if (data.user.role === "staff") {
          this.$router.push("/staff");
        } else {
          this.$router.push("/user/dashboard");
        }
      } catch (e) {
        this.message = e.message;
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
</style>
