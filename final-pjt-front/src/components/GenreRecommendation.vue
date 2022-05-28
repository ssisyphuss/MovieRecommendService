<template>
  <div class="container">
    <div class="recommendation-carousel d-flex flex-column align-items-start my-5" v-for="algorithm,name, idx in movieRecommendations" :key="idx">
      <h1 class="mx-3">{{name}}</h1>
      <div :id="`carouselExampleControls-${idx}`" class="carousel slide row container" data-bs-ride="carousel">
        <div class="carousel-inner row">
          <div class="carousel-item active">
            <div class=" row row-cols-5 g-4 ">
              <div class="col topten-item" v-for="movie, idx in algorithm.slice(0,5)" :key="idx" >
                <div class="topten-item" :style="`background-image: url(${ poster_path + movie.poster_path }); background-size: cover; background-position: center;`" @click="goToDetail(movie)"></div>
              </div>
            </div>
          </div>
          <div class="carousel-item">
            <div class=" row row-cols-5 g-4 ">
              <div class="col topten-item" v-for="movie, idx in algorithm.slice(5,10)" :key="idx" @click="goToDetail(movie)">
                <div class="topten-item" :style="`background-image: url(${ poster_path + movie.poster_path }); background-size: cover; background-position: center;`" @click="goToDetail(movie)"></div>
              </div>
            </div>
          </div>
        </div>
        <button class="carousel-control-prev" type="button" :data-bs-target="`#carouselExampleControls-${idx}`" data-bs-slide="prev">
          <span class="carousel-control-prev-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Previous</span>
        </button>
        <button class="carousel-control-next" type="button" :data-bs-target="`#carouselExampleControls-${idx}`" data-bs-slide="next">
          <span class="carousel-control-next-icon" aria-hidden="true"></span>
          <span class="visually-hidden">Next</span>
        </button>
      </div>
      <div class="em-blank"></div>
    </div>
      
      
    <div class="test"></div>

    
  </div>
</template>

<script>
export default {
  name: 'GenreRecommendation',
  data: function() {
    return {
       poster_path: 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/',

    }
  },
  created: function() {
    this.$store.dispatch('getRecommendation', this.$route.params.genreId)
  },
  computed: {
    movieRecommendations: function() {
      return this.$store.getters.movieRecommendation
    },
  },
  methods: {
    goToDetail: function(movieData) {
      console.log(movieData)
      this.$router.push({name: 'movieDetail', params: { movieId: movieData.movie_id, movie: movieData}})
    },
  }
}
</script>

<style>
  .topten-item {
    height: 25em;
  }
  .topten-item:hover {
    cursor: pointer;
    opacity: 70%;
  }
  .em-blank{
    height: 2em;
  }
</style>