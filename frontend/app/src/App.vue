<template>
  <div id="page">
    <NavBar />
    <!-- <router-link to="/"></router-link> -->
    <router-view/>
    <!-- <HomePage/> -->
  </div>
</template>

<script>


import NavBar from './components/NavBar.vue'
// import HomePage from './components/HomePage.vue'
export default {
  name: 'App',
  components: {
    NavBar,
  }
}
</script>

<style>

  body{
    margin: 0px;
  }
</style>
