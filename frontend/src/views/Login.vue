<template>
  <Navbar />
  <div>
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="login">Submit</button>

    <p>{{ message }}</p>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";

export default {
  components: {
    Navbar
  },
  data() {
    return {
      email: "",
      password: "",
      message: ""
    };
  },

  methods: {
    async login() {
      try {
        console.log('try blcock hit`')
        const response = await fetch("http://127.0.0.1:5000/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password
          })
        });
    const data = await response.json();

    if (response.ok) {
      localStorage.setItem("token", data.token);
      localStorage.setItem("user", JSON.stringify(data.user));

      if (data.user.role === "admin") {
        this.$router.push("/admin");
      } else if (data.user.role === "user") {
        this.$router.push("/user");
      } else if (data.user.role === "coordinator") {
        this.$router.push("/coordinator");
      }
    } else {
      this.message = data.error;
    }
  } catch (error) {
    console.error(error);
    this.message = "Server error";
  }
}
  }
};
</script>

<style>
</style>