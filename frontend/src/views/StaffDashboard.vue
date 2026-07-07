<template>
  <Navbar />
  <div class="container">
    <h1>Staff Dashboard</h1>
    <p>Welcome, {{ staff.username }}!</p>
    <p>Total assigned treks: {{ my_treks.length }}</p>

    <table v-if="my_treks.length > 0" border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Location</th>
          <th>Duration</th>
          <th>Slots</th>
          <th>Trekkers</th>
          <th>Status</th>
          <th>State</th>
          <th>Actions</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="trek in my_treks" :key="trek.id">
          <td>{{ trek.id }}</td>
          <td>{{ trek.name }}</td>
          <td>{{ trek.location }}</td>
          <td>{{ trek.duration }}</td>

          <td>
            <input type="number" v-model="trek.slots" style="width: 60px" />
            <button @click="updateSlots(trek)">Save</button>
          </td>

          <td>{{ trek.trekkers_count }}</td>

          <td>
            <select v-model="trek.trek_status" @change="updateStatus(trek)">
              <option value="Open">Open</option>
              <option value="Closed">Closed</option>
            </select>
          </td>

          <td>
            <select v-model="trek.trek_state" @change="updateState(trek)">
              <option value="Upcoming">Upcoming</option>
              <option value="started">started</option>
              <option value="ongoing">ongoing</option>
              <option value="completed">completed</option>
            </select>
          </td>

          <td>
            <button @click="viewParticipants(trek)">View Participants</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>No treks assigned to you yet.</p>

    <div v-if="selected_trek">
      <h2>Participants for {{ selected_trek.name }}</h2>
      <table v-if="participants.length > 0" border="1">
        <thead>
          <tr>
            <th>User ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in participants" :key="p.booking_id">
            <td>{{ p.user_id }}</td>
            <td>{{ p.username }}</td>
            <td>{{ p.email }}</td>
            <td>
              <button @click="removeParticipant(p.booking_id)">Remove</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>No registered users for this trek.</p>
    </div>
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
      staff: {},
      my_treks: [],
      participants: [],
      selected_trek: null
    };
  },

  mounted() {
    this.staff = JSON.parse(localStorage.getItem("user"));
    this.get_my_treks();
  },

  methods: {
    async get_my_treks() {
      try {
        const response = await fetch(`http://127.0.0.1:5000/coordinator_treks/${this.staff.id}`);
        if (response.ok) {
          this.my_treks = await response.json();
        }
      } catch (error) {
        console.error("Error fetching treks:", error);
      }
    },

    async updateSlots(trek) {
      try {
        const response = await fetch("http://127.0.0.1:5000/update_slots", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            trek_id: trek.id,
            coordinator_id: this.staff.id,
            slots: trek.slots
          })
        });
        const data = await response.json();
        if (response.ok) {
          alert(data.message);
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error("Error updating slots:", error);
      }
    },

    async updateStatus(trek) {
      try {
        const response = await fetch("http://127.0.0.1:5000/update_trek_status", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            trek_id: trek.id,
            coordinator_id: this.staff.id,
            trek_status: trek.trek_status
          })
        });
        const data = await response.json();
        if (!response.ok) {
          alert(data.error);
        }
      } catch (error) {
        console.error("Error updating status:", error);
      }
    },

    async updateState(trek) {
      try {
        const response = await fetch("http://127.0.0.1:5000/update_trek_state", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            trek_id: trek.id,
            coordinator_id: this.staff.id,
            trek_state: trek.trek_state
          })
        });
        const data = await response.json();
        if (!response.ok) {
          alert(data.error);
        }
      } catch (error) {
        console.error("Error updating state:", error);
      }
    },

    async viewParticipants(trek) {
      try {
        const response = await fetch(`http://127.0.0.1:5000/trek_participants/${trek.id}`);
        if (response.ok) {
          this.participants = await response.json();
          this.selected_trek = trek;
        }
      } catch (error) {
        console.error("Error fetching participants:", error);
      }
    },

    async removeParticipant(bookingId) {
      try {
        const response = await fetch("http://127.0.0.1:5000/remove_participant", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            booking_id: bookingId,
            coordinator_id: this.staff.id
          })
        });
        const data = await response.json();
        if (response.ok) {
          this.viewParticipants(this.selected_trek);
          this.get_my_treks();
        } else {
          alert(data.error);
        }
      } catch (error) {
        console.error("Error removing participant:", error);
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
  margin-bottom: 20px;
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
