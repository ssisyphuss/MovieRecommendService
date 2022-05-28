<template>
  <div id="app">
    <nav-bar></nav-bar>
    <transition name="fade" mode="out-in">
      <router-view :key="$route.fullPath"/>
    </transition>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
export default {
  name: 'app',
  components: {
    NavBar
  }
}
</script>
<style>
#app {
  font-family: 'Montserrat', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: rgba(240,240, 240, 1);
  background: rgb(15,15,15);
  min-width : 100vw;
  min-height : 100vh;
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

body {

  margin: 0;

}

.test {
  height: 5em;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}


.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* 장르별 폰트 클래스 */
  .horror-title{
    font-family: 'Fredericka the Great', cursive;
  }
  .sf-title{
    font-family: 'Odibee Sans', cursive;
  }
  .anime-title {
    font-family: 'Audiowide', cursive;
  }
  .action-title{
    font-family: 'skyfall';
  }
  .drama-title {
    font-family: 'Ruthie', cursive;
  }
  .comedy-title{
    font-family:'궁서';
  }
  @font-face{
    font-family: 'skyfall';
    src: url('@/assets/fonts/SkyFall Done.ttf')
  }
  .fa-heart{
    color: #dc3545;
  }
</style>
