<template>
  <div>
    <input v-model="email" placeholder="Email" />
    <input v-model="password" type="password" placeholder="Password" />
    <button @click="login">Submit</button>

    <p>{{ message }}</p>
  </div>
</template>

<script>
export default {
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
        this.message = data.message;
      } catch (error) {
        console.error("Error:", error);
        this.message = "Server error";
      }
    }
  }
};
</script>

<style>
</style>