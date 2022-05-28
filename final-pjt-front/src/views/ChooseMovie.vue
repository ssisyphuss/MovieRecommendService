<template>
  <div>
    <div class="for-nav"></div>
      <div class="sidebar col-1 d-flex flex-column align-items-end">
          <div class="d-flex flex-column align-items-center justify-content-center sidebar-box">
            <p v-if="choosedMovie.length < 10">아직 {{ 10 - choosedMovie.length }}개의 영화를 더 고르셔야 합니다.</p>
            <button type="button" class="btn btn-danger" @click="saveLikes" v-else>회원 가입 완료하기</button>
          </div>
      </div>
    <div class="choose-movie-container container">
      <p id="instruction" >{{ this.$route.params.username }}님 재미있게 봤던, 혹은 보고싶은 영화를 10개 이상 골라주세요!</p>
      <p v-if="choosedMovie.length < 10">아직 {{ 10 - choosedMovie.length }}개의 영화를 더 고르셔야 합니다.</p>
      <div v-else>
        <p>다음 단계로 넘어가세요! {{choosedMovieList.length }}개의 영화를 고르셨습니다!</p>
        <button type="button" class="btn btn-danger" @click="saveLikes" >회원 가입 완료하기</button>
      </div>
      <div class="row mt-5">
        <!-- div에 v-for 돌리기 키값으로 title div에 id 줘서 숨겼다 보였다-->
        <div class="poster-card col-2" v-for="movie in movieList" :key="movie.movie_id" @mouseover="showTitle(movie.movie_id)" @mouseout="hideTitle(movie.movie_id)" @click="addMovie(movie.movie_id)" :id="`movieselected-${movie.movie_id}`">
          <img :src="poster_path + movie.poster_path" alt="" class="card-img">
          <div class="card-title d-flex flex-column justify-content-center hide" :id="`movie-${movie.movie_id}`" >
            <p>{{ movie.title}}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import drf from '@/api/drf'
import router from '@/router'
export default {
  name: 'ChooseMovie',
  data: function() {
    return {
      poster_path: 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/',
      choosedMovie: [],
      test: null,
      data: {
        username: this.$route.params.username,
        likeMovieIds: [],
      }
      
    }
  },
  computed: {
    movieList: function() {
      return this.$store.getters.movieForChoose
    },
    choosedMovieList: function() {
      return this.choosedMovie
    }
    
  },

  beforeMount: function() {
      this.$store.dispatch('getMovieForChoose')
    },

  methods: {
    showTitle: function(id) {
      let target = this.$el.querySelector(`#movie-${id}`)
      target.classList.add('show')
      target.classList.remove('hide')
    },
    hideTitle: function(id) {
      let target = document.querySelector(`#movie-${id}`)
      console.log(target)
      target.classList.add('hide')
      target.classList.remove('show')
    },
    addMovie: function(id) {
      if (this.choosedMovie.includes(id) === false) {
          this.choosedMovie.push(id)
          let target = this.$el.querySelector(`#movieselected-${id}`)
          target.setAttribute('style', 'opacity:10%;')
      }
      else {
        this.choosedMovie = this.choosedMovie.filter( function(ele){
          return ele !== id
        })
        let target = this.$el.querySelector(`#movieselected-${id}`)
        target.setAttribute('style', 'opacity:100%;')
      }
      
    },
    saveLikes: function() {
      this.data.likeMovieIds = this.choosedMovie
      axios({
        method: 'post',
        url: drf.accounts.saveLikes(),
        data: this.data
      })
      // 리스폰스 받아서 장르 페이지로 보내주기
      .then((res) =>
          router.push({name:'genre', params: {genreId: res.data.beloved_genre_sort}})
        )
    }
  }
}
</script>

<style>
  #instruction {
    font-size : 2em;
  }
  .choose-movie-container {
    position: relative;
    top: 5em;
  }
  .card-img {
    width: 100%;
  }
  .card-img:hover {
    opacity: 50%;
  }
  .card-title {
    position: relative;
    bottom: 10em;
    max-width: 100%;
  }
  .card-title:hover{
    cursor: pointer;
  }
  .show {
    visibility: visible;
  }
  .hide {
    visibility: hidden;
  }
  .sidebar{
    position: sticky;
    width:100%;
  }
  .sidebar-box{
    position: fixed;
    height: 40%;
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
</style>