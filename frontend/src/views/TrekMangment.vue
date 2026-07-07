<template>
  <Navbar />
  <div class="container">
    <h1>Manage Treks</h1>

    <input v-model="search" placeholder="Search trek by name or ID" />

    <table v-if="filtered_treks.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Location</th>
          <th>Duration</th>
          <th>Slots</th>
          <th>Coordinator</th>
          <th>Assign Staff</th>
          <th>Total Bookings</th>
          <th>status</th>
          <th>state</th>
          <th>Action</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="trek in filtered_treks" :key="trek.id">
          <td>{{ trek.id }}</td>
          <td>{{ trek.name }}</td>
          <td>{{ trek.location }}</td>
          <td>{{ trek.duration }}</td>
          <td>{{ trek.slots }}</td>

          <td>
            {{ trek.coordinator_name ? trek.coordinator_name : "Not Assigned" }}
          </td>

          <td>
            <select v-model="trek.assign_id">
              <option disabled value="">Select staff</option>
              <option v-for="staff in coordinators" :key="staff.id" :value="staff.id">
                {{ staff.username }}
              </option>
            </select>
            <button @click="assignStaff(trek)">Assign</button>
          </td>

          <td>{{ trek.bookings ? trek.bookings.length : 0 }}</td>
          <td>{{ trek.trek_status }}</td>
          <td>{{ trek.trek_state }}</td>
          <td>
            <button v-on:click="deleteTrek(trek.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>No treks found.</p>
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
      all_treks: [],
      coordinators: [],
      search: ""
    };
  },

  computed: {
    filtered_treks() {
      const term = this.search.toLowerCase();
      return this.all_treks.filter(
        (trek) =>
          trek.name.toLowerCase().includes(term) ||
          String(trek.id).includes(term)
      );
    }
  },

  methods: {
    async assignStaff(trek) {
      try {
        const response = await fetch("http://127.0.0.1:5000/assign_staff", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            trek_id: trek.id,
            coordinator_id: trek.assign_id
          })
        });
        const data = await response.json();
        if (response.ok) {
          this.get_all_trek_by_admin();
        } else {
          alert(data.error || "Failed to assign staff");
        }
      } catch (error) {
        console.error("Error assigning staff:", error);
      }
    },

    async deleteTrek(trekId) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/delete_trek/${trekId}`, {
          method: "DELETE"
        });
        if (response.ok) {
          this.get_all_trek_by_admin();
        } else {
          const data = await response.json();
          alert(data.error || "Failed to delete trek");
        }
      } catch (error) {
        console.error("Error deleting trek:", error);
        alert("An error occurred while deleting the trek");
      }
    },

    async get_all_trek_by_admin() {
      try {
        const responce = await fetch("http://127.0.0.1:5000/all_treks", {
          method: "GET"
        });
        if (responce.ok) {
          const all_treks = await responce.json();
          this.all_treks = all_treks;
        }
      } catch (error) {
        console.error("Error fetching treks:", error);
      }
    },

    async get_coordinators() {
      try {
        const response = await fetch("http://127.0.0.1:5000/all_coordinators");
        if (response.ok) {
          this.coordinators = await response.json();
        }
      } catch (error) {
        console.error("Error fetching coordinators:", error);
      }
    }
  },
  mounted() {
    this.get_all_trek_by_admin();
    this.get_coordinators();
  }
};
</script>

<style>
</style>
