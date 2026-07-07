<template>
  <div>
    <div class="card" style="margin-bottom:18px">
      <div class="actions" style="align-items:center">
        <input class="input" style="max-width:240px" v-model="locationQuery" placeholder="Search by location" />
        <select class="input" style="max-width:180px" v-model="difficulty">
          <option value="">All Difficulties</option>
          <option>Easy</option>
          <option>Moderate</option>
          <option>Hard</option>
        </select>
        <button class="btn btn-primary" @click="applyFilters">Search</button>
        <button class="btn btn-gray" @click="clearFilters">Clear</button>
      </div>
    </div>

    <p v-if="error" class="error-msg">{{ error }}</p>
    <p v-if="message" class="note" style="color:#059669">{{ message }}</p>

    <div class="cards-grid">
      <div class="card" v-for="t in filteredTreks" :key="t.id">
        <div style="display:flex;justify-content:space-between;align-items:center">
          <h3 style="margin:0">{{ t.name }}</h3>
          <span class="badge badge-blue">{{ t.difficulty }}</span>
        </div>
        <ul style="list-style:none;padding:0;margin:10px 0;font-size:13px;line-height:1.9">
          <li><b>Location:</b> {{ t.location }}</li>
          <li><b>Duration:</b> {{ t.duration || '—' }}</li>
          <li><b>Dates:</b> {{ t.start_date || '—' }} → {{ t.end_date || '—' }}</li>
          <li><b>Slots:</b> {{ t.available_slots }} available / {{ t.slots }}</li>
          <li><b>Booking:</b>
            <span class="badge" :class="t.trek_status === 'Open' ? 'badge-green' : 'badge-red'">{{ t.trek_status }}</span>
          </li>
          <li><b>State:</b> <span class="badge" :class="stateBadge(t.trek_state)">{{ t.trek_state }}</span></li>
          <li><b>Coordinator:</b> {{ t.coordinator_name || 'Not Assigned' }}</li>
        </ul>

        <div class="actions">
          <template v-if="bookable">
            <button v-if="t.already_booked" class="btn btn-gray btn-sm" disabled>Already Booked</button>
            <button v-else-if="t.trek_status !== 'Open'" class="btn btn-gray btn-sm" disabled>Booking Closed</button>
            <button v-else-if="t.available_slots <= 0" class="btn btn-gray btn-sm" disabled>No slots available</button>
            <button v-else class="btn btn-primary btn-sm" @click="book(t)">Book Now</button>
          </template>
          <router-link
            v-if="t.coordinator_id"
            class="btn btn-blue btn-sm"
            :to="`/view_coordinator_profile/${t.coordinator_id}`">View Coordinator Profile</router-link>
        </div>
      </div>
    </div>
    <p v-if="!filteredTreks.length" class="note">No treks found.</p>
  </div>
</template>

<script>
import { api } from "../api.js";

export default {
  props: {
    bookable: { type: Boolean, default: false },
    currentOnly: { type: Boolean, default: false },
  },
  data() {
    return {
      treks: [],
      locationQuery: "",
      difficulty: "",
      appliedLocation: "",
      appliedDifficulty: "",
      error: "",
      message: "",
      userId: null,
    };
  },
  computed: {
    baseTreks() {
      if (this.currentOnly) {
        return this.treks.filter(
          (t) => t.trek_status === "Open" && t.trek_state === "upcoming"
        );
      }
      return this.treks;
    },
    filteredTreks() {
      return this.baseTreks.filter((t) => {
        const locOk = !this.appliedLocation ||
          (t.location || "").toLowerCase().includes(this.appliedLocation.toLowerCase());
        const diffOk = !this.appliedDifficulty || t.difficulty === this.appliedDifficulty;
        return locOk && diffOk;
      });
    },
  },
  mounted() {
    const u = JSON.parse(window.localStorage.getItem("user") || "null");
    this.userId = u ? u.id : null;
    this.load();
  },
  methods: {
    stateBadge(state) {
      if (state === "completed") return "badge-gray";
      if (state === "ongoing") return "badge-blue";
      return "badge-amber";
    },
    applyFilters() {
      this.appliedLocation = this.locationQuery;
      this.appliedDifficulty = this.difficulty;
    },
    clearFilters() {
      this.locationQuery = this.difficulty = "";
      this.appliedLocation = this.appliedDifficulty = "";
    },
    async load() {
      if (!this.userId) {
        this.error = "Please log in.";
        return;
      }
      try {
        this.treks = await api.get(`/user/treks/${this.userId}`);
      } catch (e) {
        this.error = e.message;
      }
    },
    async book(t) {
      this.error = this.message = "";
      try {
        const res = await api.post("/book_trek", { user_id: this.userId, trek_id: t.id });
        this.message = res.message;
        this.load();
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
