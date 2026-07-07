<template>
  <Navbar />
  <div class="page">
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="card header-card" v-if="staff">
      <div>
        <h1 style="margin:0 0 4px">Welcome, {{ staff.username }}</h1>
        <p class="note" style="margin:0">{{ staff.email }} &middot; <span class="badge badge-blue">{{ staff.role }}</span></p>
      </div>
      <div class="actions">
        <router-link class="btn btn-gray" to="/staff/view_profile">View Profile</router-link>
        <router-link
          v-if="staff.profile_completed"
          class="btn btn-blue"
          to="/staff/edit_profile">Edit Profile</router-link>
        <router-link
          v-else
          class="btn btn-primary"
          to="/staff/complete_profile">Complete Profile</router-link>
      </div>
    </div>

    <div class="stats-grid">
      <div class="stat-box"><div class="value">{{ stats.total_conducted ?? 0 }}</div><div class="label">Total Treks Conducted</div></div>
      <div class="stat-box"><div class="value">{{ stats.current_assigned ?? 0 }}</div><div class="label">Current Assigned Treks</div></div>
      <div class="stat-box"><div class="value">{{ stats.registered_trekkers ?? 0 }}</div><div class="label">Registered Trekkers</div></div>
      <div class="stat-box"><div class="value">{{ stats.open_bookings ?? 0 }}</div><div class="label">Open Bookings</div></div>
    </div>

    <div class="card" style="margin-bottom:20px">
      <b>Status guide:</b>
      <span class="note">
        <b>Booking</b> Open/Closed controls whether users can book.
        <b>Trek State</b> goes upcoming → ongoing → completed.
        Slot changes and edits need admin approval before they apply.
      </span>
    </div>

    <h2 style="font-size:18px;margin:0 0 12px">Current Assigned Treks</h2>
    <div class="table-wrap" style="margin-bottom:28px">
      <table class="table" v-if="currentTreks.length">
        <thead>
          <tr>
            <th>Name</th><th>Location</th><th>Expected Time</th><th>Participants</th>
            <th>Available Slots</th><th>Progress</th><th>Booking</th><th>Trek Status</th><th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in currentTreks" :key="t.id">
            <td>{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.duration || '—' }}</td>
            <td>{{ t.registered_count }}</td>
            <td>{{ t.slots - t.registered_count }}</td>
            <td>{{ t.progress }}%</td>
            <td><span class="badge" :class="t.trek_status === 'Open' ? 'badge-green' : 'badge-red'">{{ t.trek_status }}</span></td>
            <td><span class="badge" :class="stateBadge(t.trek_state)">{{ t.trek_state }}</span></td>
            <td>
              <div class="actions">
                <router-link class="btn btn-blue btn-sm" :to="`/staff/trek/${t.id}`">Open Trek</router-link>
                <router-link
                  v-if="!t.pending_approval"
                  class="btn btn-gray btn-sm"
                  :to="`/edit_treak/${t.id}`">Edit</router-link>
                <span v-else class="badge badge-amber">Pending Approval</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No current assigned treks.</p>
    </div>

    <h2 style="font-size:18px;margin:0 0 12px">Past Completed Treks</h2>
    <div class="table-wrap">
      <table class="table" v-if="pastTreks.length">
        <thead>
          <tr><th>Name</th><th>Location</th><th>Duration</th><th>Participants</th><th>Actions</th></tr>
        </thead>
        <tbody>
          <tr v-for="t in pastTreks" :key="t.id">
            <td>{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.duration || '—' }}</td>
            <td>{{ t.total_bookings }}</td>
            <td>
              <router-link class="btn btn-gray btn-sm" :to="`/staff/trek/${t.id}/participants`">View Participants</router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No completed treks yet.</p>
    </div>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { staff: null, stats: {}, treks: [], error: "" };
  },
  computed: {
    currentTreks() {
      return this.treks.filter((t) => t.trek_state !== "completed");
    },
    pastTreks() {
      return this.treks.filter((t) => t.trek_state === "completed");
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
      const user = JSON.parse(window.localStorage.getItem("user") || "null");
      if (!user) {
        this.error = "Please log in as staff.";
        return;
      }
      try {
        const data = await api.get(`/staff/overview/${user.id}`);
        this.staff = data.staff;
        this.stats = data.stats;
        this.treks = data.treks;
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
