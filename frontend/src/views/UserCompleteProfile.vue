<template>
  <Navbar />
  <div class="page">
    <h1>Complete Profile</h1>
    <ProfileForm
      submit-label="Save Profile"
      redirect-to="/view_profile"
      back-to="/user/dashboard" />
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import ProfileForm from "../components/ProfileForm.vue";

export default {
  components: { Navbar, ProfileForm },
};
</script>
