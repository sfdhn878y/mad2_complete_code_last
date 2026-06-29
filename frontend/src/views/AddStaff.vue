<template>
  <h1>Add Staff</h1>
  <input type="text" placeholder="Staff Name" v-model="staff_name" />
    <input type="text" placeholder="Staff Email" v-model="staff_email" />
    <input type="text" placeholder="Staff Password" v-model="staff_password" />
    <button @click="add_staff">Add Staff</button>
    <div v-if="errorData" class="error-message">
      <p>Error adding staff: {{ errorData }}</p>
    </div>
</template>

<script>
export default {
    data() {
        return {
            staff_name: "",
            staff_email: "",
            staff_password: "",
            data:"",
            errorData: null
        };
    },
    methods: {
        async add_staff() {
            const response = await fetch("http://127.0.0.1:5000/add_staff", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    username: this.staff_name,
                    email: this.staff_email,
                    password: this.staff_password
                })
            });

            if (response.ok) {
                const data = await response.json();
                this.staff_name = "";
                this.staff_email = "";
                this.staff_password = "";
            } else {
                const errorData = await response.json();
                this.errorData = errorData.error || "An error occurred while adding staff.";
                console.error("Error adding staff:", errorData);
            }
        }
    }
}
</script>

<style>

</style>