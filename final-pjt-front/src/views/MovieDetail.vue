<template>
  <div>
    <div class="for-nav" style="height: 5em;"></div>
    <div class="for-nav" style="height: 5em;"></div>
      <div class="sidebar col-1 d-flex flex-column align-items-end">
          <div class="d-flex flex-column align-items-center sidebar-box">
            <p class="mt-4">For you</p>
            <img :src="path + movie.poster_path" class="sidebar-item my-3" alt="" v-for="movie, idx in detail.similar_movies" :key="idx" @click="goToDetail(movie)">
          </div>
      </div>
    <div class="container">
      
      <div class="row poster-row">
        <div class="col-4 poster-box">
          <img :src="path + detail.poster_path" alt="" class="poster">
        </div>
        <div class="col detail d-flex flex-column">
          <!-- 영화 상세정보 -->
          <div class="title align-self-start d-flex align-items-center" >
            <h1>{{detail.title}}</h1>
            <button type="button" class="btn btn-outline-light mx-2" @click="writeReview(detail.movie_id  )">Write Review</button>
            <div v-if="isLoggedIn">
                <!-- v-on click통해 디테일페이지로 라우트 / 영화 좋아요하기 -->
                <i class="fa-regular fa-2xl fa-heart mx-2" @click="saveLike(detail.movie_id)" v-if="!profile.liked_movie_ids.includes(detail.movie_id)"></i>
                <i class="fa-solid fa-2xl fa-heart mx-2" @click="saveLike(detail.movie_id)" v-if="profile.liked_movie_ids.includes(detail.movie_id)"></i>
              </div>
          </div>
          <div class="botton-box d-flex justify-contetn-start my-2">
            <button type="button" class="btn btn-outline-light mx-2" v-for="genre, idx in detail.genres" :key="idx">{{ genre.genre_name }}</button> 
            <button type="button" class="btn btn-outline-light mx-2">{{detail.vote_average}}</button>
          </div>
          <div class="overview aligh-self-start my-2">
            <p class="text-start">{{detail.overview}}</p>
          </div>
        </div>
      </div>
      <!-- 캐스팅정보 -->
      <h1>Casting</h1>
      <div class="row p-3 g-3">
        <div class="card border-secondary cast-card col mx-2" style="width: 18rem; background:rgb(15,15,15);" v-for="actor in detail.actors" :key="actor.actor_id">
          <img class="card-img-top mt-2" :src="path + actor.profile_path" alt="Card image cap">
          <div class="card-body">
            <p class="card-text">{{ actor.name }}</p>
          </div>
        </div>
      </div>
      <!-- 리뷰 -->
      <div class="row mt-5">
        <ul class="list-group col-12">
          <li class="list-group-item review-lst-item border-secondary d-flex justify-content-between align-items-center" v-for="review, idx in detail.review_set" :key="idx"
          @click='goToReview(detail.movie_id, review.id)'>
            <span class="d-flex align-items-center"> {{ review.title}} </span>
            <span> 
              <span class="mx-1">username: {{review.user.username}}</span>
              <span class="mx-1">rating: {{review.rating}}</span>
              <span class="badge badge-primary badge-pill mx-1">{{review.user_good_eval.length}}</span>
            </span>
          </li>
        </ul>
      </div>
    </div>
    <div class="test"></div>
  </div>
</template>

<script>
export default {
  name: "MovieDetail",
  created: function () {
    this.$store.dispatch('sendDetailRequest', this.movieId)
    if (this.isLoggedIn){
        this.$store.dispatch('fetchProfile', { username: this.currentUser.username })
      }
  },
  // beforeRouteUpdate(to, from, next){
  //   console.log('next')
  //   this.$store.dispatch('sendDetailRequest', this.movie.movie_id)
  //   console.log(this.movie)
  //   next()
  // },
  data: function() {
    return {
      // movie: this.$route.params.movie,
      movieId: this.$route.params.movieId,
      path: 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/',
    }
  },
  computed:  {
    detail: function() {
      return this.$store.getters.movieDetail
    },
    profile: function() {
        return this.$store.getters.profile
      },
      currentUser: function() {
        return this.$store.getters.currentUser
      },
      isLoggedIn: function() {
        return this.$store.getters.isLoggedIn
      }
  },
  methods: {
    writeReview: function(id) {
      this.$router.push({name: 'writeReview', params: {movieId: id}})
    },
    goToReview: function(movieId, reviewId){
      this.$router.push({name: 'reviewView', params: {movieId: movieId,reviewPk: reviewId }})
    },
    saveLike: function(movie) {
      const credentials = {
        username: this.currentUser.username,
        likeMovieIds: [movie],
      }
      this.$store.dispatch('saveLike', credentials)
    },
    goToDetail: function(movieData) {
      console.log(movieData)
      this.$router.push({name: 'movieDetail', params: { movieId: movieData.movie_id, movie: movieData}})
    },
  }
}
</script>

<style>
  .poster-row {
    height: 40em;
  }
  .poster{
    height: 80%;
    width: auto;
  }
  .poster-box{
    height: 100%;
  }
  .review-lst-item {
    background: rgb(15,15,15);
    color:rgba(240, 240, 240, 1)
  }
  .review-lst-item:hover{
    cursor: pointer;
  }
  .sidebar{
    position: sticky;
    width:100%;
  }
  .sidebar-box{
    position: fixed;
    top: 25vh;
    width: 7%;
    background:linear-gradient(0deg, rgba(15,15,15,1) 7%,rgba(50,50,50,1) 40%,rgba(50,50,50,1) 60%, rgba(15, 15, 15, 1)93%);
    margin-right: 2.5%;
    border-radius: 2em;
    padding: 0.5em;
  }
  .sidebar-item{
    width: 75%;
    border-radius: 0.5em;;
  }
  .cast-card {
    height: 28em;
  }
</style>