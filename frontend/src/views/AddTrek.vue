<template>
 <div>
        <h1>Add Trek</h1>
    </div>
    <div>
        <input v-model="trekName" placeholder="Enter trek name">
        <input v-model="trekLocation" placeholder="Enter trek location">
        <input v-model="duration" placeholder="Enter trek duration">
        <input v-model="slots" placeholder="slots available">
        <select v-model="coordinatorId">
            <option disabled value="">Select a coordinator</option>
        <option v-for="user in coordinators" key="user.id" :value="user.id">
                {{ user.username }}
        </option>
        </select>
        <button @click="addTrek">Add Trek</button>
    </div>
</template>

<script>
export default {
    data() {
        return {
            trekName: "",
            trekLocation: "",
            duration: "",
            slots: "",
            coordinators: [],
            coordinatorId: ""
        };
    },
        mounted() {
            this.fetchCoordinators();
        },
    methods: {
        async fetchCoordinators() {
            try {
                const response = await fetch("http://127.0.0.1:5000/all_coordinators");
                if (response.ok) {
                    this.coordinators = await response.json();
                }
            } catch (error) {
                console.error("Error fetching coordinators:", error);
            }
        },

       async addTrek() {
            try {
                const response = await fetch("http://127.0.0.1:5000/add_treks", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        name: this.trekName,
                        location: this.trekLocation,
                        duration: this.duration,
                        slots: this.slots,
                        coordinator_id: this.coordinatorId
                    })
                });
                if (response.ok) {
                    this.$router.push("/admin");
                } else {
                    const data = await response.json();
                    alert(data.error || "Failed to add trek");
                }
            } catch (error) {
                console.error("Error adding trek:", error);
                alert("An error occurred while adding the trek");
            }
        }
    }
}

</script>

<style>

</style>