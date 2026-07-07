<template>
  <Navbar />
  <div class="page">
    <h1>Current Treks</h1>
    <p class="note">Open treks that are upcoming and available to book.</p>
    <TrekBrowser :bookable="true" :current-only="true" />
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import TrekBrowser from "../components/TrekBrowser.vue";

export default {
  components: { Navbar, TrekBrowser },
};
</script>
