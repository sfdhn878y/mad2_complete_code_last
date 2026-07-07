<template>
  <Navbar />
  <div class="page">
    <h1>All Treks</h1>
    <p class="note">Browse every trek in the system.</p>
    <TrekBrowser :bookable="false" :current-only="false" />
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import TrekBrowser from "../components/TrekBrowser.vue";

export default {
  components: { Navbar, TrekBrowser },
};
</script>
