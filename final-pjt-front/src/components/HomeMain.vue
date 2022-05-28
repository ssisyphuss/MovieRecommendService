<template>
  <div>
    <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        <div class="home-main carousel-item active " v-for="movie, index in homeMainMovies.recommended_movies" :key="index" 
        :style="`background-image: linear-gradient(0deg, rgba(15,15,15,1), rgba(100, 100, 100, 0.2)), url(${ movie.movieimage_set[0].image_URL }); background-size: cover; background-position: center;`" >
          <div class="for-nav"></div>
          <!-- <p>{{ movie}}</p> -->
          <div class="main-box">
            <div class="movie-title">
              <span style="font-size: 5em;">{{ movie.title }}</span>
            </div>
            <div class="movie-overview">
              <span>{{movie.overview}}</span>
              <div class="movie-info">
              <!-- 장르 버튼에 v-for= "" key="#"넣기 -->
              <button type="button" class="btn btn-outline-light mx-2" v-for="genre, idx in movie.genres" :key="idx">{{ genre.genre_name }}</button> 
              <button type="button" class="btn btn-outline-light mx-2">{{movie.vote_average}}</button> 
                <div class="movie-add d-flex align-items-center" v-if="isLoggedIn">
                  <!-- v-on click통해 디테일페이지로 라우트 / 영화 좋아요하기 -->
                  <button type="button" class="btn btn-danger mx-2" @click="goToDetail(movie)">Detail</button>
                  <div v-if="profile.liked_movie_ids">
                    <i class="fa-regular fa-2xl fa-heart mx-2" @click="saveLike(movie.movie_id)" v-if="!profile.liked_movie_ids.includes(movie.movie_id)"></i>
                    <i class="fa-solid fa-2xl fa-heart mx-2" @click="saveLike(movie.movie_id)" v-if="profile.liked_movie_ids.includes(movie.movie_id)"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>



  </div>



  
</template>

<script>
export default {
  name: "HomeMain",
  created: function() {
      this.$store.dispatch('getMovieForHome')
      if (this.isLoggedIn){
        this.$store.dispatch('fetchProfile', { username: this.currentUser.username })
      }
    },
  data: function() {
    return {
      url: 'https://www.themoviedb.org/t/p/original/6RuU7NumrO08Bcml5sIgj9zNWFm.jpg',
      a: [1,2,3]
    }
  },
  computed: {
      homeMainMovies: function() {
        return this.$store.getters.movieForHome
      },
      profile: function() {
        return this.$store.getters.profile
      },
      currentUser: function() {
        return this.$store.getters.currentUser
      },
      isLoggedIn: function() {
        return this.$store.getters.isLoggedIn
      },
      
    },
  methods: {
    goToDetail: function(movieData) {
      console.log(movieData)
      this.$router.push({name: 'movieDetail', params: { movieId: movieData.movie_id, movie: movieData}})
    },
    saveLike: function(movie) {
      const credentials = {
        username: this.currentUser.username,
        likeMovieIds: [movie],
      }
      this.$store.dispatch('saveLike', credentials)
    }
  }
}
</script>

<style>
.home-main {
  height:60em;
  overflow: hidden;
  background-repeat: no-repeat;
  
}
.home-img {
  width: 100%;
}
.for-nav{
  height: 5em;
}
.main-box{
  height: 55em;
}
.movie-title{
  font:'';
  position: absolute;
  top: 13em;
  left: 10em;
  color: rgba(240,240,240,1);
}
.movie-overview
{
  width: 30%;
  font:'';
  position: absolute;
  top: 20.5em;
  left: 10em;
  color: rgba(240,240,240,1);
  text-align: left;

}
.movie-info{
  font:'';
  position: relative;
  top: 2em;
  color: rgba(240,240,240,1)
}
.movie-add{
  font:'';
  position: relative;
  top: 2em;
  color: rgba(240,240,240,1)
}
.fa-heart:hover{
  cursor: pointer;
}
</style>