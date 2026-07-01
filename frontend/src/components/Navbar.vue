  <template>
    <nav>
      <router-link to="/">Home</router-link>
      <template v-if="logedIn()">
              <router-link to="/user_managment">user_managment </router-link>
      <router-link to="/staff_managment">staff_managment</router-link>
      <router-link to="/trek_managment">trek_managment</router-link>

              <button @click.prevent="logout">Logout</button>

      </template>
      <template v-else>

        <router-link to="/login">Login</router-link>
        <router-link to="/register">Register</router-link>
      </template>
    </nav>
  </template>
  <script>
  export default {
    methods: {
    logout() {
        window.localStorage.removeItem("token");
        window.localStorage.removeItem("user");
        this.$router.push("/login");
      
      },
      logedIn() {
      return !!window.localStorage.getItem("token");
      
    }
    },
    
  };

  </script>
  <style scoped>
  nav {
    padding: 15px;
    background-color: #333;
  }

  a {
    color: white;
    margin-right: 15px;
    text-decoration: none;
  }

  a.router-link-active {
    font-weight: bold;
    color: yellow;
  }
  </style>