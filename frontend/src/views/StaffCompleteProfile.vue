<template>
  <Navbar />
  <div class="page">
    <h1>Complete Profile</h1>
    <ProfileForm
      submit-label="Save Profile"
      redirect-to="/staff/view_profile"
      back-to="/staff" />
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import ProfileForm from "../components/ProfileForm.vue";

export default {
  components: { Navbar, ProfileForm },
};
</script>
