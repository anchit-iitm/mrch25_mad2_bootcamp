<template>
  <nav>
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link> |
    <router-link :to="{'name': 'Login'}">Login</router-link> |
    <router-link :to="{'name': 'Register'}">Register</router-link> |
    <router-link :to="{'name': 'CreateCategory'}">CreateCategory</router-link> |
    <router-link :to="{'name': 'Dashboard'}">Dashboard</router-link>
  </nav>
  <router-view/>
</template>

<script>
</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>
