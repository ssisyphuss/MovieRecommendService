<template>
<div class="home">
  <home-main :key="componentKey"></home-main>
  <div class="test"></div>
  <genre-card v-if="isLoggedIn"></genre-card>
</div>
</template>

<script>
import GenreCard from '../components/GenreCard.vue'
import HomeMain from '../components/HomeMain.vue'
// @ is an alias to /src

export default {
  name: 'HomeView',
  components: {
    GenreCard,
    HomeMain
  },
  data() { return { componentKey: 0, }; }, 
  computed: {
    isLoggedIn : function() {
      return this.$store.getters.isLoggedIn
    }
  },
  methods: { forceRerender() { this.componentKey += 1; } } 

  
}
</script>

<style>
  .home {
  }
  
</style>


