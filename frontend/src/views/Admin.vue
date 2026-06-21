<template>
    <div>
        <h1>Admin Dashboard</h1>
    </div>
    <button @click="add_treak">Add Trek</button>
    <ul>
        <li v-for="trek in data" :key="trek.id">
            {{ trek.name }} - {{ trek.location }}
        </li>
    </ul>
</template>

<script>
export default {
    data() {
        return {
            data:[]
        };
    },
    mounted() {
        this.all_treaks();
    },
    methods: {
        add_treak() {
            this.$router.push("/add_trek");
        },
        async all_treaks() {
             const response = await fetch("http://127.0.0.1:5000/all_treks",{
                method: "GET",
             });
                if (response.ok) {
                    this.data = await response.json();
                    console.log(this.data);
                }

                
               
        }
    }

}
</script>

<style>

</style>