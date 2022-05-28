<template>
<div class="home">
  <genre-movie-main :key="componentKey"></genre-movie-main>
  <genre-recommendation></genre-recommendation>
</div>
</template>

<script>
import GenreRecommendation from '@/components/GenreRecommendation.vue';
import GenreMovieMain from '../components/GenreMovieMain.vue'
// @ is an alias to /src

export default {
  name: 'GenreMovie',
  components: {
    GenreMovieMain,
    GenreRecommendation
  },
  data() { return { componentKey: 0, }; }, 
  methods: { forceRerender() { this.componentKey += 1; } } 

  
}
</script>

<style>
  
</style>
