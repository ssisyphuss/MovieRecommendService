<template>
  <div class="container">
    <div class="for-nav"></div>
    <h1>영화 검색 결과</h1>
    <div class="row my-5 align-items-center search-hover" v-for="search, idx in searchList" :key="idx" @click ="goToDetail(search)">
      <img :src="path + search.poster_path" class="col-2">
      <div class="col-10 d-flex align-items-center">
        <p>{{search.title}}</p>
        <i class="fa-solid fa-star ms-4"> {{search.vote_average}}</i>
      </div>
      
    </div>
  </div>
</template>

<script>
export default {
  name:"SearchVue",
  data: function() {
    return {
      path: 'https://image.tmdb.org/t/p/w600_and_h900_bestv2/'
    }
  },
  computed: {
    searchList: function() {
      return this.$route.params.searchList
    }
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
  .search-hover:hover{
    cursor: pointer;
  }
</style>