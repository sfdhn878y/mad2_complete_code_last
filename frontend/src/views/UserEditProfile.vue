<template>
  <Navbar />
  <div class="page">
    <h1>Edit Profile</h1>
    <ProfileForm
      submit-label="Update Profile"
      redirect-to="/view_profile"
      back-to="/view_profile" />
  </div>
</template>

<script>
import Navbar from "../components/Navbar.vue";
import ProfileForm from "../components/ProfileForm.vue";

export default {
  components: { Navbar, ProfileForm },
};
</script>
