<template>
  <Navbar />
  <div class="page">
    <h1>Trekking History</h1>
    <p class="note">All your bookings — booked, completed, and cancelled.</p>

    <button class="btn" @click="exportCsv" :disabled="exporting">
      {{ exporting ? "Exporting..." : "Export CSV" }}
    </button>
    <p v-if="exportMsg" class="note">{{ exportMsg }}</p>
    <p v-if="error" class="error-msg">{{ error }}</p>

    <div class="table-wrap">
      <table class="table" v-if="bookings.length">
        <thead>
          <tr>
            <th>Name</th><th>Location</th><th>Difficulty</th><th>Booked On</th>
            <th>Booking Status</th><th>Trek Booking</th><th>Trek State</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="t in bookings" :key="t.booking_id">
            <td>{{ t.name }}</td>
            <td>{{ t.location }}</td>
            <td>{{ t.difficulty }}</td>
            <td>{{ formatDate(t.booked_at) }}</td>
            <td><span class="badge" :class="statusBadge(t.status)">{{ t.status }}</span></td>
            <td><span class="badge" :class="t.trek_status === 'Open' ? 'badge-green' : 'badge-red'">{{ t.trek_status }}</span></td>
            <td><span class="badge" :class="stateBadge(t.trek_state)">{{ t.trek_state }}</span></td>
          </tr>
        </tbody>
      </table>
      <p v-else class="note">No booking history yet.</p>
    </div>
  </div>
</template>
<script>
import Navbar from "../components/Navbar.vue";
import { api } from "../api.js";

export default {
  components: { Navbar },
  data() {
    return { bookings: [], error: "" ,exporting: false, exportMsg: "" };
  },
  mounted() {
    this.load();
  },
  methods: {
 async exportCsv() {
  const u = JSON.parse(window.localStorage.getItem("user") || "null");
  if (!u) {
    this.error = "Please log in.";
    return;
  }
  this.exporting = true;
  this.exportMsg = "";
  this.error = "";
  try {
    const res = await api.post("/user/export-history");
    this.exportMsg = "Export started...";
    const jobId = res.job_id;

    let status;
    while (true) {
      await new Promise((r) => setTimeout(r, 2000));
      status = await api.get(`/user/export-status/${jobId}`);
      if (status.status === "done") break;
      if (status.status === "failed") throw new Error("Export failed");
    }

    this.exportMsg = "Export ready! Downloading...";

    const token = window.localStorage.getItem("token");
    const downloadRes = await fetch(
      `http://127.0.0.1:5000/exports/${status.filename}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );
    if (!downloadRes.ok) throw new Error("Download failed");

    const blob = await downloadRes.blob();
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = status.filename;
    a.click();
    URL.revokeObjectURL(url);

    this.exportMsg = "Export downloaded!";
  } catch (e) {
    this.error = e.message;
  } finally {
    this.exporting = false;
  }
},
    formatDate(v) {
      return v ? new Date(v).toLocaleDateString() : "—";
    },
    statusBadge(status) {
      if (status === "Completed") return "badge-green";
      if (status === "Cancelled") return "badge-red";
      return "badge-blue";
    },
    stateBadge(state) {
      if (state === "completed") return "badge-gray";
      if (state === "ongoing") return "badge-blue";
      return "badge-amber";
    },
    async load() {
      const u = JSON.parse(window.localStorage.getItem("user") || "null");
      if (!u) {
        this.error = "Please log in.";
        return;
      }
      try {
        this.bookings = await api.get(`/user/bookings/${u.id}`);
      } catch (e) {
        this.error = e.message;
      }
    },
  },
};
</script>
