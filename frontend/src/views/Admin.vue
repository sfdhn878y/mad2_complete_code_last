<template>
    <div>
        <h1>Admin Dashboard</h1>
    </div>
    <button @click="add_treak">Add Trek</button>
</template>

<script>
export default {
    methods: {
        add_treak() {
            this.$router.push("/add_trek");
        }
    }

}
</script>

<style>

</style>