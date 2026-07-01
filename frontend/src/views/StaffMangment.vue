<template>
  <Navbar />
  <div class="container">
    <h1>Staff Management</h1>

    <table border="1">
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Verified</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="staff in staffs" :key="staff.id">
          <td>{{ staff.id }}</td>
          <td>{{ staff.username }}</td>
          <td>{{ staff.email }}</td>
           <button
          :class="staff.status === 'Active' ? 'blacklist-btn' : 'unblacklist-btn'"
          @click="toggleStatus(staff)"
        >
          {{ staff.status === "Active" ? "Blacklist" : "Unblacklist" }}
        </button>
        </tr>
      </tbody>
    </table>
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
      staffs: [],
    };
  },

  mounted() {
    this.loadStaff();
  },

  methods: {
    async loadStaff() {
      try {
        const response = await fetch("http://127.0.0.1:5000/staff");

        if (!response.ok) {
          throw new Error("Failed to fetch staff.");
        }

        this.staffs = await response.json();
      } catch (error) {
        console.error("Error:", error);
      }
    },
async toggleStatus(staff) {
  const newStatus =
    staff.status === "Active" ? "Blacklisted" : "Active";

  try {
    const response = await fetch("http://127.0.0.1:5000/staff/status", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        id: staff.id,
        status: newStatus,
      }),
    });

    const result = await response.json();

    if (response.ok) {
      staff.status = newStatus;
      console.log(result.message);
    } else {
      alert(result.error);
    }
  } catch (error) {
    console.error(error);
  }
}  
},
  
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