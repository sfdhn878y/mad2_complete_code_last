<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link to="/addtrek">Add Trek</router-link>
    <router-link to="/admin">Admin</router-link>
    <router-link to="/coordinator">Coordinator</router-link>
    <router-link to="/login">Login</router-link>
    <router-link to="/register">Register</router-link>
  </nav>
</template>

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