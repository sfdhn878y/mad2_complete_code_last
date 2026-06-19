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
        if (response.ok) {
          response.json().then(data => {
          
            if (data.role === "admin") {
              this.$router.push("/admin");
            } else if (data.role === "user") {
              this.$router.push("/user");
            } else if (data.role === "coordinator") {
              this.$router.push("/coordinator");
            } else {
              this.message = "Unknown role";
            }
          });
        } else {
          const data = await response.json();
          this.message = data.error || "Login failed";
        }
       
      } catch (error) {
      console.log('catch block hit')
        console.error("Error:", error);
        this.message = "Server error";
      }
    }
  }
};
</script>

<style>
</style>