<template>
  <Navbar />
  <div class="container">
    <h1>Booking Records</h1>

    <table v-if="bookings.length > 0" border="1">
      <thead>
        <tr>
          <th>Booking ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Trek</th>
          <th>Status</th>
          <th>State</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="b in bookings" :key="b.id">
          <td>{{ b.id }}</td>
          <td>{{ b.username }}</td>
          <td>{{ b.email }}</td>
          <td>{{ b.trek_name }}</td>
          <td>{{ b.trek_status }}</td>
          <td>{{ b.trek_state }}</td>
        </tr>
      </tbody>
    </table>

    <p v-else>No booking records found.</p>
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
      bookings: []
    };
  },

  mounted() {
    this.get_all_bookings();
  },

  methods: {
    async get_all_bookings() {
      try {
        const response = await fetch("http://127.0.0.1:5000/all_bookings");
        if (response.ok) {
          this.bookings = await response.json();
        }
      } catch (error) {
        console.error("Error fetching bookings:", error);
      }
    }
  }
};
</script>

<style scoped>
.container {
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

th {
  background-color: #2c3e50;
  color: white;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}
</style>
