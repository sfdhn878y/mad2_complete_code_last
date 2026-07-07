<template>
  <Navbar />
  <div>
    <h1>User Management</h1>
    <input v-model="search" placeholder="Search user by name or ID" />
    <table v-if="filtered_users.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Username</th>
          <th>Email</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="user in filtered_users" :key="user.id">
          <td>{{ user.id }}</td>
          <td>{{ user.username }}</td>
          <td>{{ user.email }}</td>
           <button
          :class="user.status === 'Active' ? 'blacklist-btn' : 'unblacklist-btn'"
          @click="toggleStatus(user)"
        >
          {{ user.status === "Active" ? "Blacklist" : "Unblacklist" }}
        </button>
        </tr>
      </tbody>
    </table>

    <p v-else>No users found.</p>
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
        all_users: [],
        search: "",
        };
    },

    computed: {
        filtered_users() {
            const term = this.search.toLowerCase();
            return this.all_users.filter(
                (user) =>
                    user.username.toLowerCase().includes(term) ||
                    String(user.id).includes(term)
            );
        },
    },

    mounted() {
        this.get_all_users();
    },
    
    methods: {
        async get_all_users() {
        try {
            const response = await fetch("http://127.0.0.1:5000/all_users");
            const users = await response.json();
            this.all_users = users;
        } catch (error) {
            console.error("Error fetching users:", error);
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



}
</script>

<style>

</style>