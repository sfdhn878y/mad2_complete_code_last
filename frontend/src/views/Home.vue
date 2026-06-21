<template>
  <section class="hero">

    <img
      :src="mountainBg"
      alt="mountain"
      class="bg-image"
    />

    <div class="overlay"></div>

    <!-- Navbar -->
    <nav class="navbar">
      <div class="logo">
        Trek<span>Hub</span>
      </div>

      <ul class="nav-menu">
        <li>Home</li>
        <li>Treks</li>
        <li>Routes</li>
        <li>Guides</li>
        <li>About</li>
      </ul>

      <button class="login-btn">
        Login
      </button>
    </nav>

    <!-- Hero Content -->
    <div class="hero-content">

      <div class="content-left">

       
      <h1 class="hero-title">
  Manage Treks.<br>
  Organize Teams.<br>
  <span>Conquer Mountains.</span>
</h1>

<p class="hero-description">
  Plan routes, assign guides, manage trekkers
  and track every adventure in one place.
</p>

        <div class="hero-buttons">
          <button class="start-btn">
            Start Trek
          </button>

          <button class="route-btn">
            View Routes
          </button>
        </div>

      </div>

   

    </div>

  </section>
  <!-- Treks Section -->
<section id="treks" class="section">
 <section class="expedition-map">
  <div class="section-header">
    <h2>Popular Treks</h2>
    <p>Choose your next Himalayan adventure.</p>
  </div>

  <div class="map-area">

    <!-- Route Line -->
    <div class="route-line"></div>

    <!-- Trek 1 -->
    <div class="trek-point everest">
      <span class="pin"></span>

      <div class="trek-card">
        <span class="altitude">5,364m</span>
        <h3>Everest Base Camp</h3>
        <p>Legendary Himalayan expedition with breathtaking views.</p>
      </div>
    </div>

    <!-- Trek 2 -->
    <div class="trek-point kedarkantha">
      <span class="pin"></span>

      <div class="trek-card">
        <span class="altitude">3,810m</span>
        <h3>Kedarkantha Trek</h3>
        <p>Snow-covered winter trails perfect for beginners.</p>
      </div>
    </div>

  </div>
</section>
</section>

<!-- Routes Section -->
<section id="routes" class="section light-section">
  <div class="section-container">
    <h2>Route Management</h2>
    <p class="section-text">
      Organize routes, checkpoints, campsites and trek schedules effortlessly.
    </p>

    <div class="card-grid">
      <div class="info-card">
        <h3>Trail Planning</h3>
        <p>Create custom trekking routes with distance tracking.</p>
      </div>

      <div class="info-card">
        <h3>Live Monitoring</h3>
        <p>Track group progress throughout the journey.</p>
      </div>

      <div class="info-card">
        <h3>Safety Checkpoints</h3>
        <p>Manage emergency and safety locations easily.</p>
      </div>
    </div>
  </div>
</section>

<!-- Guides Section -->
<section id="guides" class="section">
  <div class="section-container">
    <h2>Professional Guides</h2>
    <p class="section-text">
      Connect with experienced trekking guides and expedition leaders.
    </p>

    <div class="card-grid">
      <div class="info-card">
        <h3>Certified Experts</h3>
        <p>Highly trained mountain professionals.</p>
      </div>

      <div class="info-card">
        <h3>Local Knowledge</h3>
        <p>Explore hidden trails with experienced locals.</p>
      </div>

      <div class="info-card">
        <h3>Group Support</h3>
        <p>Dedicated guidance throughout your trek.</p>
      </div>
    </div>
  </div>
</section>

<!-- About Section -->
<section id="about" class="section light-section">
  <div class="section-container">
    <h2>About TrekHub</h2>

    <p class="section-text">
      TrekHub helps adventure organizers manage treks, routes,
      guides and participants through one powerful platform.
      From planning to execution, everything stays organized
      in a simple and intuitive dashboard.
    </p>

    <div class="about-box">
      <div>
        <h3>500+</h3>
        <span>Treks Managed</span>
      </div>

      <div>
        <h3>100+</h3>
        <span>Professional Guides</span>
      </div>

      <div>
        <h3>10K+</h3>
        <span>Happy Trekkers</span>
      </div>
    </div>
  </div>
</section>
</template>

<script setup>
import mountainBg from '../assets/images/mountain-bg.png'
</script>

<style scoped>

*{
  margin:0;
  padding:0;
  box-sizing:border-box;
}

.hero{
  position:relative;
  min-height:100vh;
  overflow:hidden;
   width: 100vw;
  margin: 0;
}

.bg-image{
  position:absolute;
  width:100%;
  height:100%;
  object-fit:cover;
}
.overlay{
  position:absolute;
  inset:0;

  background:linear-gradient(
    90deg,
    rgba(255,255,255,0.95) 0%,
    rgba(255,255,255,0.85) 40%,
    rgba(255,255,255,0.20) 75%,
    rgba(255,255,255,0.05) 100%
  );
}

.navbar{
  position:relative;
  z-index:10;
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:25px 80px;
}

.logo{
  font-size:32px;
  font-weight:800;
  color:#16325c;
}

.logo span{
  color:#3d8b40;
}

.nav-menu{
  display:flex;
  list-style:none;
  gap:40px;
  color:#16325c;
  font-size:17px;
  font-weight:600;
}
.nav-menu li{
  cursor:pointer;
}

.login-btn{
  background:#ff7a18;
  color:white;
  border:none;
  padding:12px 28px;
  border-radius:10px;
  cursor:pointer;
}

.hero-content{
  position:relative;
  z-index:10;
  min-height:80vh;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 80px;
}

.content-left{
  max-width:650px;
}

.badge{
  display:inline-block;
  background:rgba(255,122,24,0.15);
  color:#ff7a18;
  border:1px solid rgba(255,122,24,0.4);
  padding:10px 20px;
  border-radius:30px;
  margin-bottom:25px;
}
.hero-title{
  font-size:72px;
  font-weight:800;
  line-height:1.05;
  color:#16325c;
  letter-spacing:-2px;
  font-family:'Poppins',sans-serif;
}

.hero-title span{
  color:#3d8b40;
}
.content-left h1 span{
  color:#ff7a18;
}

.hero-description{
  margin-top:18px;
  max-width:500px;
  font-size:20px;
  color:#5f6b7a;
  line-height:1.6;
}
.hero-buttons{
  display:flex;
  gap:20px;
  margin-top:35px;
}

.start-btn{
  background:#4CAF50;
  color:white;
  border:none;
  padding:16px 30px;
  border-radius:14px;
  font-size:16px;
  font-weight:600;
  cursor:pointer;
  box-shadow:0 8px 20px rgba(76,175,80,.25);
}


.route-btn{
  background:white;
  border:1px solid #d6dbe3;
  color:#1e293b;
  padding:16px 30px;
  border-radius:14px;
  font-size:16px;
  font-weight:600;
  cursor:pointer;
}
.glass-card{
  width:320px;
  padding:25px;
  border-radius:20px;
  background:rgba(255,255,255,0.1);
  backdrop-filter:blur(12px);
  color:white;
  border:1px solid rgba(255,255,255,0.2);
}

.glass-card h3{
  margin-bottom:10px;
}

.card-info{
  margin-top:20px;
  display:flex;
  justify-content:space-between;
  color:#ff7a18;
}

html{
  scroll-behavior:smooth;
}

.nav-menu a{
  text-decoration:none;
  color:#16325c;
}

.section{
  padding:100px 80px;
  background:white;
}

.light-section{
  background:#f8fafc;
}

.section-container{
  max-width:1200px;
  margin:auto;
}

.section h2{
  font-size:48px;
  color:#16325c;
  margin-bottom:20px;
  text-align:center;
}

.section-text{
  max-width:700px;
  margin:auto;
  text-align:center;
  color:#64748b;
  font-size:18px;
  line-height:1.7;
}

.card-grid{
  margin-top:50px;
  display:grid;
  grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
  gap:25px;
}

.info-card{
  background:white;
  padding:30px;
  border-radius:18px;
  box-shadow:0 8px 25px rgba(0,0,0,.08);
  transition:.3s;
}

.info-card:hover{
  transform:translateY(-8px);
}

.info-card h3{
  color:#16325c;
  margin-bottom:12px;
}

.info-card p{
  color:#64748b;
  line-height:1.6;
}

.about-box{
  margin-top:60px;
  display:flex;
  justify-content:center;
  gap:80px;
  text-align:center;
}

.about-box h3{
  color:#ff7a18;
  font-size:42px;
}

.about-box span{
  color:#64748b;
}

@media(max-width:768px){

  .section{
    padding:80px 25px;
  }

  .section h2{
    font-size:36px;
  }

  .about-box{
    flex-direction:column;
    gap:30px;
  }
}
</style>