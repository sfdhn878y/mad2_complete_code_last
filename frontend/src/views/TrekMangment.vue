<template>
  <div class="container">
    <h1>Manage Treks</h1>

    <table v-if="all_treks.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Location</th>
          <th>Duration</th>
          <th>Slots</th>
          <th>Status</th>
          <th>Coordinator</th>
          <th>Total Bookings</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="trek in all_treks" :key="trek.id">
          <td>{{ trek.id }}</td>
          <td>{{ trek.name }}</td>
          <td>{{ trek.location }}</td>
          <td>{{ trek.duration }}</td>
          <td>{{ trek.slots }}</td>
          <td>{{ trek.status }}</td>

          <td>
            {{ trek.coordinator_name ? trek.coordinator_name : "Not Assigned" }}
          </td>

          <td>
            {{ trek.bookings ? trek.bookings.length : 0 }}
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>No treks found.</p>
  </div>
</template>
<script>
export default {
    data(){
        return {
            all_treks:[]
        }
    },

    methods:{
        async get_all_trek_by_admin(){
            try {
                const responce = await fetch('http://127.0.0.1:5000/all_treks',{
                    method:'GET',
                    
                });
                if(responce.ok){
                    const all_treks = await responce.json();
                    this.all_treks = all_treks;
                }

               
            }catch(error){
                console.error('Error fetching treks:',error);
            }

        }
    },
    mounted(){
        this.get_all_trek_by_admin();
    }
}
</script>

<style>

</style>