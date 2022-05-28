<template>
  <div class="container">
    <div class="for-nav"></div>
    <div class="row">
      <div class="col-3 my-2"  v-for="review, idx in genreReviews" :key="idx" @click="goToReview(review.movie.movie_id,review.id)">
        <div class="card genre-card border-secondary px-2 py-2">
          <img :src="poster_path + review.movie.poster_path" class="card-img-top genre-poster" alt="...">
          <div class="card-body">
            <h5 class="card-text review-title">{{review.title}}</h5>
            <p class="card-text">{{review.rating}}</p>
          </div>
        </div>
      </div>
    </div>
    <button class="carousel-control-prev" type="button" data-bs-slide="prev" @click="goToGenreMovie">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-slide="next" @click="goToGenreView">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>

<script>
export default {
  name: 'CommunityView',
  data: function() {
    return {
      genreId: this.$route.params.genreId,
      poster_path: 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/',
    }
  },
  created: function() {
    this.$store.dispatch("getReviews", this.genreId)
  },
  computed: {
    genreReviews: function() {
      return this.$store.getters.genreReviews
    },
  },
  methods: {
    goToReview: function(movieId, reviewId){
      this.$router.push({name: 'reviewView', params: {movieId: movieId,reviewPk: reviewId, }})
    },
    goToGenreView: function() {
      this.$router.push({name:'genre', params: {genreId: this.$route.params.genreId}})
    },
    goToGenreMovie: function() {
      console.log('장르로간다')
      this.$router.push({name: 'genreMovie', params: {movieId: this.genreId}})
    },
  }
}
</script>

<style>
  .genre-card {
    background-color: rgba(15, 15, 15, 1);
  }
  .genre-poster {
    border-radius: 1em;
  }
  .review-title {
    color: white;
  }
</style>