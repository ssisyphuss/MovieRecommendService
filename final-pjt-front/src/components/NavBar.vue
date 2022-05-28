<template>
  <nav class="navbar navbar-expand-lg fixed-top">
  <div class="container-fluid">
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarTogglerDemo01" aria-controls="navbarTogglerDemo01" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarTogglerDemo01">
      <img src="@/assets/My_project.png" alt="" @click= "gotoHome" class="ms-3 me-auto logo">

      <div class="dropdown me-2 ">
        <input class="form-control dropdown-toggle" type="search" id="dropdownMenuButton1" data-bs-toggle="dropdown" aria-expanded="false" :value="searchData" @input="changeKeyword" @keyup.enter="goToSearch(searchData)"> 
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1" v-show="searchData !== ''" >
          <li class="d-flex align-items-center search-item dropdown-item list-gr" > Movie </li>

          <li v-for="search, idx in searchList.slice(0,5)" :key="idx" class="d-flex align-items-center search-item dropdown-item list-con" @click="goToDetail(search)" >
            <img :src="path + search.poster_path" alt="" class="search-img me-2">
            <a href="javascript:void(0);" style="text-decoration: none;">{{ search.title }}</a>
          </li>
          <li class="d-flex align-items-center search-item dropdown-item list-gr" > User </li>
          <li v-for="search in userSearchResult.slice(0,5)" :key="search.username" class="d-flex align-items-center search-item dropdown-item list-con" @click="goToProfile(search.username)" >
            <a href="javascript:void(0);" style="text-decoration: none;">{{ search.username }}</a>
          </li>
          
        </ul>
      </div>


      <!-- <div class="d-flex mx-5" role="search">
        <input class="form-control me-2 dropdown-toggle" type="search" id="dropdownMenuButton1"  data-bs-toggle="dropdown" aria-expanded="false" placeholder="Search" aria-label="Search" :value="searchData" @input="changeKeyword">
      </div> -->


      <ul class="navbar-nav mb-2 mb-lg-0 me-3">
        <li class="nav-item nav-route mx-1" v-if="isLoggedIn">
          <router-link :to="{name: 'profile', params: { username } }" class="nav-route">Profile</router-link>
        </li>
        <li class="nav-item nav-route mx-1" v-if="!isLoggedIn">
          <router-link :to="{name: 'signup'}" class="nav-route">SignUp</router-link>
        </li>
        <li class="nav-item nav-route mx-1" v-if="isLoggedIn">
          <router-link :to="{name: 'logout' }" class="nav-route">Logout</router-link>
        </li>
        <li v-if="!isLoggedIn" class="nav-item nav-route mx-1">
          <router-link :to="{ name: 'signin' }" class="nav-route">Login</router-link>
        </li>
        <!-- <li class="nav-item nav-route mx-1" @click="goBack">
          Back
        </li> -->
      </ul>
      


    </div>
  </div>
</nav>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'NavBar',
  data: function() {
    return {
      searchData: '',
      path: 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/',
    }
  },
  methods: {
    gotoHome: function() {
      this.$router.push({ name: 'home'})
    },
    sendSearchRequest: function() {
      this.$store.dispatch("sendSearchRequest", this.searchData )
    },
    sendUserSearchRequest: function() {
      this.$store.dispatch("sendUserSearchRequest", this.searchData)
    },
    goToDetail: function(movieData) {
      console.log(movieData)
      this.$router.push({name: 'movieDetail', params: { movieId: movieData.movie_id, movie: movieData}})
    },
    changeKeyword: function(word) {
      this.searchData = word.target.value
      this.sendSearchRequest()
      this.sendUserSearchRequest()
    },
    goBack: function() {
      this.$router.go(-1)
    },
    goToProfile: function(username) {
      this.$router.push({name: 'profile', params: {username}})
    },
    goToSearch: function(keyword) {
      this.$router.push({name: 'searchView', query:{keyword}, params:{searchList: this.searchList}})
    }
    },
  computed: {
    ...mapGetters(['isLoggedIn', 'currentUser', 'searchList', 'userSearchResult']),
    username() {
      return this.currentUser.username ? this.currentUser.username : 'guest'
    },
  },

}
</script>

<style>
  .logo{
    width:10rem;
  }
  img:hover{
    cursor: pointer;
  }
  nav{
    height: 5em;
  }
  .search-img {
    height: 5em;
  }
  .search-item {
    border-color: grey;
  }
  .nav-route {
    color: rgba(240, 240, 240, 1)
  }
  .list-gr {
    background-color: rgba(200, 200, 200, 1)
  }
  .list-con:hover{
    cursor: pointer;
  }
</style>