<template>
  <Navbar />
  <div class="page" v-if="trek">
    <h1>{{ trek.name }}</h1>
    <p v-if="error" class="error-msg">{{ error }}</p>
    <p v-if="message" class="note" style="color:#059669">{{ message }}</p>

    <div v-if="trek.pending_approval" class="card" style="margin-bottom:16px;border-color:#d97706">
      <span class="badge badge-amber">Pending Approval</span>
      <span class="note"> A change you submitted is awaiting admin approval. Some actions are locked.</span>
    </div>

    <div class="stats-grid">
      <div class="stat-box"><div class="value">{{ trek.duration || '—' }}</div><div class="label">Expected Time</div></div>
      <div class="stat-box"><div class="value">{{ trek.progress }}%</div><div class="label">Completion Progress</div></div>
      <div class="stat-box"><div class="value">{{ trek.registered_count }}</div><div class="label">Registered Trekkers</div></div>
      <div class="stat-box"><div class="value">{{ trek.available_slots }}</div><div class="label">Available Slots</div></div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <div style="background:#e5e7eb;border-radius:999px;height:14px;overflow:hidden">
        <div :style="{ width: trek.progress + '%', background: '#059669', height: '100%' }"></div>
      </div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <h3 style="margin:0 0 10px">Trek Info</h3>
      <ul style="list-style:none;padding:0;margin:0;line-height:2;font-size:14px">
        <li><b>Booking Status:</b> <span class="badge" :class="trek.trek_status === 'Open' ? 'badge-green' : 'badge-red'">{{ trek.trek_status }}</span></li>
        <li><b>Trek Status:</b> <span class="badge" :class="stateBadge(trek.trek_state)">{{ trek.trek_state }}</span></li>
        <li><b>Total Capacity:</b> {{ trek.registered_count }} booked + {{ trek.available_slots }} available = {{ trek.slots }}</li>
      </ul>
    </div>

    <div class="card" style="margin-bottom:16px">
      <h3 style="margin:0 0 10px">Update Total Slots</h3>
      <p v-if="trek.pending_approval" class="note">Locked — a change is already pending approval.</p>
      <div v-else class="actions" style="align-items:center">
        <input class="input" style="max-width:120px" type="number" :min="trek.registered_count" v-model.number="newSlots" />
        <button class="btn btn-primary" @click="requestSlotChange">Request Slot Change</button>
        <span class="note">Must be ≥ current bookings ({{ trek.registered_count }}). Goes to admin for approval.</span>
      </div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <h3 style="margin:0 0 10px">Booking Status</h3>
      <button
        class="btn"
        :class="trek.trek_status === 'Open' ? 'btn-amber' : 'btn-primary'"
        @click="toggleBooking">
        {{ trek.trek_status === 'Open' ? 'Close Booking' : 'Open Booking' }}
      </button>
    </div>

    <div class="card" style="margin-bottom:16px">
      <h3 style="margin:0 0 10px">Trek Status</h3>
      <div class="actions">
        <button
          v-if="trek.trek_state === 'upcoming'"
          class="btn btn-blue"
          @click="updateState('ongoing')">Mark as Ongoing</button>
        <button
          v-if="trek.trek_state !== 'completed'"
          class="btn btn-primary"
          :disabled="trek.trek_status !== 'Closed'"
          @click="updateState('completed')">Mark as Completed</button>
        <span v-if="trek.trek_state !== 'completed' && trek.trek_status !== 'Closed'" class="note">
          Close booking before marking completed.
        </span>
      </div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <h3 style="margin:0 0 10px">Edit Trek Details</h3>
      <router-link
        v-if="!trek.pending_approval"
        class="btn btn-blue"
        :to="`/edit_treak/${trek.id}`">Edit Trek</router-link>
      <p v-else class="note">Locked — a change is already pending approval.</p>
    </div>

    <div class="card" style="margin-bottom:16px">
      <h3 style="margin:0 0 10px">Participants</h3>
      <router-link class="btn btn-gray" :to="`/staff/trek/${trek.id}/participants`">View Registered Users</router-link>
    </div>

    <router-link class="btn btn-gray" to="/staff">Back to Dashboard</router-link>
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { trek: null, newSlots: 0, error: "", message: "", coordinatorId: null };
  },
  mounted() {
    const user = JSON.parse(window.localStorage.getItem("user") || "null");
    this.coordinatorId = user ? user.id : null;
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
        this.trek = await api.get(`/staff/trek/${this.$route.params.id}`);
        this.newSlots = this.trek.slots;
      } catch (e) {
        this.error = e.message;
      }
    },
    async requestSlotChange() {
      this.error = this.message = "";
      try {
        const res = await api.post("/staff/request_slot_change", {
          trek_id: this.trek.id,
          coordinator_id: this.coordinatorId,
          slots: this.newSlots,
        });
        this.message = res.message;
        this.load();
      } catch (e) {
        this.error = e.message;
      }
    },
    async toggleBooking() {
      this.error = this.message = "";
      try {
        await api.post("/staff/toggle_booking", {
          trek_id: this.trek.id,
          coordinator_id: this.coordinatorId,
        });
        this.load();
      } catch (e) {
        this.error = e.message;
      }
    },
    async updateState(state) {
      this.error = this.message = "";
      try {
        await api.post("/staff/update_state", {
          trek_id: this.trek.id,
          coordinator_id: this.coordinatorId,
          trek_state: state,
        });
        this.load();
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
