<template>
  <Navbar />
  <div>
    <h2>Register</h2>
  </div>
  <div>
    <input v-model="username" type="text" placeholder="Username" />
    <input v-model="email" type="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="register">Register</button>
  </div>
  <div v-if="data">{{ data }}</div>
  <div v-if="error">{{ error }}</div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import About from './About.vue';
export default {
  components: {
    Navbar,
    About
  },
  data() {
    return {
      username: "",
      email: "",
      password: "",
      data: null,
      error: null,
    };
  },
  methods: {
    async register() {
      console.log("funtiom called");
      try {
        const response = await fetch("http://localhost:5000/register", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
            password: this.password,
          }),
        });
        if (response.ok) {
          const data = await response.json();
          this.data = data; //{"message": "User registration suffessly completed"}
          console.log("Registration successful:", data);
        } else {
            const errorData = await response.json();
        this.error = errorData.error;
          console.error("Registration failed:", response.statusText);
        }
      } catch (error) {
        const errorData = await response.json();
        this.error = errorData.error;
      }
    },
  },
};
</script>

<style>
</style>