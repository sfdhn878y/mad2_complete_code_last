<template>
  <Navbar />
  <div class="page">
    <div class="header-card card">
      <h1 style="margin:0">Manage Treks</h1>
      <router-link class="btn btn-primary" to="/add_treak">+ Add Trek</router-link>
    </div>

    <input class="input search-bar" v-model="search" placeholder="Search trek by name or ID" />
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="table-wrap">
      <table class="table" v-if="filteredTreks.length">
        <thead>
          <tr>
            <th>ID</th><th>Name</th><th>Location</th><th>Start</th><th>End</th>
            <th>Duration</th><th>Slots</th><th>Participants</th><th>Staff</th>
            <th>Booking</th><th>State</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="trek in filteredTreks" :key="trek.id">
            <td>{{ trek.id }}</td>
            <td>{{ trek.name }}</td>
            <td>{{ trek.location }}</td>
            <td>{{ trek.start_date || '—' }}</td>
            <td>{{ trek.end_date || '—' }}</td>
            <td>{{ trek.duration || '—' }}</td>
            <td>
              {{ trek.slots }}
              <div v-if="trek.pending_approval" class="badge badge-amber" style="margin-top:4px">
                {{ trek.slots }} → {{ trek.pending_slots }}
              </div>
            </td>
            <td>
              {{ trek.registered_count }}
              <router-link class="btn btn-gray btn-sm" :to="`/view_participants/${trek.id}`">View List</router-link>
            </td>
            <td>
              {{ trek.coordinator_name || 'Not Assigned' }}
              <router-link
                v-if="trek.coordinator_id"
                class="btn btn-gray btn-sm"
                :to="`/staff_profile/${trek.coordinator_id}`">Profile</router-link>
            </td>
            <td>
              <span class="badge" :class="trek.trek_status === 'Open' ? 'badge-green' : 'badge-red'">
                {{ trek.trek_status }}
              </span>
            </td>
            <td>
              <span class="badge" :class="stateBadge(trek.trek_state)">{{ trek.trek_state }}</span>
            </td>
            <td>
              <div class="actions">
                <router-link class="btn btn-blue btn-sm" :to="`/admin/trek_details/${trek.id}`">View Details</router-link>
                <template v-if="trek.pending_approval">
                  <button class="btn btn-primary btn-sm" @click="approve(trek)">Approve</button>
                  <button class="btn btn-red btn-sm" @click="reject(trek)">Reject</button>
                </template>
                <router-link class="btn btn-gray btn-sm" :to="`/admin/edit_treak/${trek.id}`">Edit</router-link>
                <button
                  v-if="trek.trek_status === 'Open'"
                  class="btn btn-amber btn-sm"
                  @click="toggleBooking(trek)">Close Trek</button>
                <button
                  v-else-if="trek.trek_state === 'upcoming'"
                  class="btn btn-primary btn-sm"
                  @click="toggleBooking(trek)">Open Trek</button>
                <button class="btn btn-red btn-sm" @click="deleteTrek(trek)">Delete</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No treks found.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { treks: [], search: "", error: "" };
  },
  computed: {
    filteredTreks() {
      const term = this.search.trim().toLowerCase();
      if (!term) return this.treks;
      return this.treks.filter(
        (t) => t.name.toLowerCase().includes(term) || String(t.id).includes(term)
      );
    },
  },
  mounted() {
    this.load();
  },
  methods: {
    stateBadge(state) {
      if (state === "completed") return "badge-gray";
      if (state === "ongoing") return "badge-blue";
      return "badge-amber";
    },
    async load() {
      try {
        this.treks = await api.get("/all_treks");
      } catch (e) {
        this.error = e.message;
      }
    },
    async approve(trek) {
      try { await api.post(`/admin/approve_change/${trek.id}`); this.load(); }
      catch (e) { alert(e.message); }
    },
    async reject(trek) {
      try { await api.post(`/admin/reject_change/${trek.id}`); this.load(); }
      catch (e) { alert(e.message); }
    },
    async toggleBooking(trek) {
      try { await api.post(`/admin/toggle_booking/${trek.id}`); this.load(); }
      catch (e) { alert(e.message); }
    },
    async deleteTrek(trek) {
      if (!confirm(`Delete "${trek.name}" and all its bookings?`)) return;
      try { await api.del(`/delete_trek/${trek.id}`); this.load(); }
      catch (e) { alert(e.message); }
    },
  },
};
</script>
