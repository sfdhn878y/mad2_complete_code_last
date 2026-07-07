<template>
  <Navbar />
  <div class="container">
    <h1>Trekking Statistics</h1>

    <ul>
      <li>Total Users: {{ stats.total_users }}</li>
      <li>Total Staff: {{ stats.total_staff }}</li>
      <li>Total Treks: {{ stats.total_treks }}</li>
      <li>Total Bookings: {{ stats.total_bookings }}</li>
      <li>Open Treks: {{ stats.open_treks }}</li>
      <li>Closed Treks: {{ stats.closed_treks }}</li>
      <li>Completed Treks: {{ stats.completed_treks }}</li>
    </ul>
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
      stats: {}
    };
  },

  mounted() {
    this.get_stats();
  },

  methods: {
    async get_stats() {
      try {
        const response = await fetch("http://127.0.0.1:5000/stats");
        if (response.ok) {
          this.stats = await response.json();
        }
      } catch (error) {
        console.error("Error fetching stats:", error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
}

li {
  padding: 5px;
  font-size: 18px;
}
</style>
