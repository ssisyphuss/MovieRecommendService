<template>
  <div :class="{'sf': this.genreId === 2, 'horror': this.genreId === 1, 'anime': this.genreId === 3, 'action': this.genreId === 4, 'drama': this.genreId === 5, 'docu': this.genreId === 6, 'comedy': this.genreId === 7}">
    <div class="for-nav"></div>
    <!-- BGM -->
    <div >
      <audio autoplay loop>
        <source src="@/assets/sounds/horror.mp3" v-if="this.genreId === 1">
        <source src="@/assets/sounds/SF.mp3" v-if="this.genreId === 2">
        <source src="@/assets/sounds/Action.mp3" v-if="this.genreId === 4">
        <source src="@/assets/sounds/Anime.mp3" v-if="this.genreId === 3">
        <source src="@/assets/sounds/Drama.mp4" v-if="this.genreId === 5">
        <source src="@/assets/sounds/Docu.mp4" v-if="this.genreId === 6">
        <source src="@/assets/sounds/Comedy.mp4" v-if="this.genreId === 7">

      </audio>
    </div>

    <div :class="{'sf-title': this.genreId === 2, 'horror-title': this.genreId === 1, 'anime-title': this.genreId === 3, 'action-title': this.genreId === 4, 'drama-title': this.genreId === 5, 'docu-title': this.genreId === 6,'comedy-title': this.genreId === 7 }" class="main-box" >
      <div class="movie-title">
        <span style="font-size: 5em;" v-if="this.genreId === 1">HORROR / THRILLER </span>
        <span style="font-size: 5em;" v-if="this.genreId === 2">SF / FANTASY</span>
        <span style="font-size: 5em;" v-if="this.genreId === 3">ANIMATION</span>
        <span style="font-size: 5em;" v-if="this.genreId === 4">action</span>
        <span style="font-size: 5em;" v-if="this.genreId === 5">DRAMA / ROMANCE</span>
        <span style="font-size: 5em;" v-if="this.genreId === 6">DOCUMENTARY / HISTORY</span>
        <span style="font-size: 5em;" v-if="this.genreId === 7">코미디</span>

      </div>
      <div class="movie-overview">
        <span v-if="this.genreId === 1" class="horror-content">All work and no play makes Jack a dull boy</span>
        <span v-if="this.genreId === 2" class="sf-content">Do not gentle into that good night. rage, rage against the dying of the light.</span>
        <span v-if="this.genreId === 3" class="anime-content d-flex flex-column">PLANT!<br><span class="align-self-end content-margin" >. . .   &lt;WALL- E&gt;</span></span>
        <span v-if="this.genreId === 4">Age is no guarantee of efficiency And youth is no guarantee of innovation</span>
        <span v-if="this.genreId === 5" class="drama-content">My momma always said, "Life was like a box chocolates. You never know what you're gonna get"</span>
        <span v-if="this.genreId === 6" class="docu-content">One small step for a man, one giant leap for mankind.</span>
        <span v-if="this.genreId === 7" class="comedy-content">지금까지 이런 맛은 없었다. 이것은 갈비인가 통닭인가.</span>



      </div>
    </div>
    <button class="carousel-control-prev" type="button" data-bs-slide="prev" @click="goToGenreCommunity">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-slide="next" @click="goToGenreMovie">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</template>


<script>
export default {
  name: 'GenreView',
  data: function() {
    return {
      genreId : this.$route.params.genreId,
    }
  },
  methods: {
    goToGenreMovie: function() {
      console.log('장르로간다')
      this.$router.push({name: 'genreMovie', params: {movieId: this.genreId}})
    },
    goToGenreCommunity: function() {
      this.$router.push({name: 'genreCommunity', params: {genreId: this.genreId}})
    }
  }
}
</script>

<style>
  .for-nav{
  height: 5em;
}
/* 장르별 클래스 */
  .horror{
    height: 100vh;
    background:linear-gradient(0deg, rgba(0,0,0,1), rgba(0, 0, 0, 0.3)), url('@/assets/Horror.png');
    background-size: cover;
}
  .sf{
    height: 100vh;
    background:linear-gradient(0deg, rgba(0,0,0,1), rgba(255, 255, 255, 0.1)), url('@/assets/SF.jpg');
    background-size: cover;
 }
  .anime{
    height: 100vh;
    background:linear-gradient(0deg, rgba(0,0,0,1), rgba(255, 255, 255, 0.1)), url('@/assets/Anime.jpg');
    background-size: cover;
}
  .action{
    height: 100vh;
    background:linear-gradient(0deg, rgba(0,0,0,1), rgba(255, 255, 255, 0.1)), url('@/assets/Action.png');
    background-size: cover;
  }
  .drama{
    height: 100vh;
    background:linear-gradient(0deg, rgba(0,0,0,1), rgba(255, 255, 255, 0.1)), url('@/assets/Drama.jpg');
    background-size: cover;
  }
  .docu{
    height: 100vh;
    background:linear-gradient(0deg, rgba(0,0,0,1), rgba(0, 0, 0, 0.2)), url('@/assets/Documentary.jpg');
    background-size: cover;
  }
  .comedy{
    height: 100vh;
    background:linear-gradient(0deg, rgba(0,0,0,1), rgba(0, 0, 0, 0.2)), url('@/assets/Comedy.jpg');
    background-size: cover;
  }
  .horror-content{
    font-size:2em;
  }
  .sf-content{
    font-size:1.8em;
  }
  .anime-content{
    font-size:1.5em;
  }
  .drama-content{
    font-size:2.5em;
  }
  .docu-content{
    font-size: 1.5em;
  }
  .comedy-content{
    font-size: 1.8em;
  }
  .content-margin{
    margin-right:15em;
  }
</style>