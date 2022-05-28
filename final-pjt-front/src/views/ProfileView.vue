<template>
  <div>
     
    <div class="container">
      <div class="for-nav"></div>
      <div class="profile-box">
        <div>
          <h1>{{ profile.username }}님의 프로필 페이지</h1>
          <div v-if="profile.username !== currentUser.username">
            <button type="button" class="btn btn-outline-light mx-2" @click="follow(profile.username)" v-if="!profile.followers.includes(currentUser.pk)">Follow</button>
            <button type="button" class="btn btn-outline-light mx-2" @click="follow(profile.username)" v-if="profile.followers.includes(currentUser.pk)">Unfollow</button>
          </div>
          <div class="test"></div>
          <div class="test"></div>
          <div class="row">
            <div class="col-4 d-flex flex-column align-items-start">
              <p class="mb-2">Favorite Genres</p>
              <div class="d-flex mb-2">
                <button type="button" class="btn btn-outline-secondary mx-1 profile-genre-btn" v-for="genre, idx in slicedGenreList" :key="idx">{{genre.genre_name}}</button>
              </div>
              <div class="test"></div>
              <div class="d-flex align-items-center">
                <span>Followers:</span>
                <button type="button" class="btn btn-outline-secondary mx-2 profile-genre-btn" >{{profile.followers.length}}</button>
                <span>Followings:</span>
                <button type="button" class="btn btn-outline-secondary mx-2 profile-genre-btn" >{{profile.followings.length}}</button>
              </div>
            </div>
            <div class="liked-movie-box d-flex flex-column col-8">
                <div class="d-flex">
                  <p class="liked-movie-p align-self-start mx-3 mb-2">Favorite Actors</p>
                </div>
              
                <div class="liked-movie-img-box d-flex justify-content-center align-items-center">
                  <div v-for=" (actor,index) in slicedActorList" :key="index" class="liked-movie-img mx-3" :id="`movie-${index}`">
                    <!-- 클릭하면 영화 상세페이지로 가게 하기 -->
                    <img :src="poster_path + actor.profile_path" alt="" class="movie-img">
                    <h5>{{actor.actor_name}}</h5>
                  </div>
                </div>
              </div>
          </div>
        </div>
        
      <!-- <h1>{{ profile}}</h1> -->
      </div>
      
      <!-- 좋아요 누른 영화 -->
      <div class="row">
        <div class="liked-movie-box d-flex flex-column col-12">
          <div class="d-flex">
            <p class="liked-movie-p align-self-start mx-3">Liked Movies</p>
            <button type="button" class="btn btn-danger mx-3" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
              See all
            </button>
          </div>
          
          <div class="liked-movie-img-box d-flex justify-content-center align-items-center">
            <div v-for=" (movie,index) in slicedMovieList" :key="index" class="liked-movie-img mx-3" :id="`movie-${index}`">
              <!-- 클릭하면 영화 상세페이지로 가게 하기 -->
              <img :src="poster_path + movie.poster_path" alt="" class="movie-img" @click="goToDetail(movie)">
            </div>
          </div>
        </div>
      </div>

      <!-- Modal For liked Movies -->
      <div>
        <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
            <div class="modal-dialog liked-movie-modal-dialog modal-lg">
              <div class="modal-content liked-movie-modal-content">
                <div class="modal-header">
                  <h5 class="modal-title liked-movie-p" id="staticBackdropLabel">Liked Movies</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <div class="container-fluid">
                    <div class="row row-cols-4">
                      <img class="modal-img my-3" @click="goToDetail(movie)" data-bs-dismiss="modal" :src="poster_path + movie.poster_path" alt="" v-for="movie, idx in profile.movie_likes" :key="idx">
                    </div>
                  </div>
                </div>
                <div class="modal-footer">
                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
              </div>
            </div>
          </div>
      </div>

      
        <!-- 작성한 글 -->
      <h2>작성한 글</h2>
      <div class="row mt-5">
          <ul class="list-group col-12">
            <li class="list-group-item review-lst-item border-secondary d-flex justify-content-between align-items-center" v-for="review, idx in profile.review_set" :key="idx"
            @click='goToReview(review.movie, review.id)'>
              <span class="d-flex align-items-center"> {{ review.title}} </span>
              <span> 
                <i class="fa-solid fa-star ms-2"></i>
                <span class="mx-2">{{review.rating}}</span>
                <i class="fa-solid fa-thumbs-up ms-2"></i>
                <span class="badge badge-primary badge-pill mx-1">{{review.user_good_eval.length}}</span>
              </span>
            </li>
          </ul>
        </div>
      <div class="test"></div>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'


export default {
  name: 'ProfileView',
  components: {

  },
  data : function() {
    return{
      poster_path: 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/',
    }
  },
  computed: {
    ...mapGetters(['profile', 'currentUser']),
    slicedMovieList: function() {
      const reversedList = [...this.profile.movie_likes].reverse()
      return reversedList.slice(0,8)
    },
    slicedActorList: function() {
      return this.profile.favorite_actors
    },
    slicedGenreList: function() {
      return this.profile.genre_counts.slice(0,5)
    }
  },
  methods: {
    ...mapActions(['fetchProfile']),
    goToDetail: function(movieData) {
      this.$router.push({name: 'movieDetail', params: { movieId: movieData.movie_id, movie: movieData}})
    },
    goToReview: function(movieId, reviewId){
      this.$router.push({name: 'reviewView', params: {movieId: movieId,reviewPk: reviewId }})
    },
    follow: function(username) {
      this.$store.dispatch('follow', username)
    }
  },
  created() {
    const payload = { username: this.$route.params.username }
    this.fetchProfile(payload)
    
  },
}
</script>

<style>
.for-nav{
  height: 5em;
}

h1{
  color: rgba(240,240,240,1);
}

.liked-movie-box {
  /* width: 45em; */
  height: 24em;
  border-radius: 0.8em;
}

.liked-movie-img-box{
  width: 100%;
  height: 60%;
  background: rgb(10,10,10);
  border-radius: 1em;
}

.liked-movie-img {

  position: relative;
}
/* .liked-movie-img:not(#movie-0, #movie-1) {
  right: 5em;
}
#movie-1 {

  right: 2.5em;
} */
.movie-img {
  width: 100%;
  border-radius: 0.5em;
}

.movie-img:hover {
  opacity: 50%;
}

.liked-movie-modal-content{
  background: rgba(30,30,30,1);
}
.modal-img {
  border-radius: 1em;
}
.liked-movie-p{
  color: rgba(240,240,240,1);
}
.profile-genre-btn{
  color: rgba(240,240,240,1);
  border-color: rgb(240, 240, 240)
}


</style>