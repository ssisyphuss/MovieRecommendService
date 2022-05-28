<template>
  <div class="home container mt-5">
    <h2 class="text-start ms-3" style="color: rgba(240,240,240,1);">Genres</h2>
    <div class="row p-3 g-3">
      <div class="col" @click= "gotoGenre(1)">
        <div class="col-in horror-card"></div>
        <div class="genre-name d-flex flex-column justify-content-center ">
          <p> Thriller </p>
        </div>
      </div>
      <div class="col even" @click= "gotoGenre(2)">
        <div class="col-in sf-card"></div>
        <div class="genre-name d-flex flex-column justify-content-center ">
            <p> SF / Fantasy </p>
        </div>
      </div>
      <div class="col" @click= "gotoGenre(3)">
        <div class="col-in anime-card"></div>
        <div class="genre-name d-flex flex-column justify-content-center ">
            <p> Animation </p>
        </div>
      </div>
      <div class="col even" @click= "gotoGenre(4)">
        <div class="col-in action-card"></div>
        <div class="genre-name d-flex flex-column justify-content-center ">
            <p> Action </p>
        </div>
      </div>
      <div class="col" @click= "gotoGenre(5)">
        <div class="col-in drama-card"></div>
        <div class="genre-name d-flex flex-column justify-content-center ">
            <p> Drama </p>
        </div>
      </div>
      <div class="col even" @click= "gotoGenre(6)">
        <div class="col-in docu-card"></div>
        <div class="genre-name d-flex flex-column justify-content-center ">
            <p> Documentary </p>
        </div>
      </div>
      <div class="col" @click= "gotoGenre(7)">
        <div class="col-in comedy-card"></div>
        <div class="genre-name d-flex flex-column justify-content-center ">
            <p> Comedy</p>
        </div>
      </div>
    </div>
    <div class="test"></div>
  </div>
</template>

<script>
export default {
  name: 'GenreCard',
  methods: {
    gotoGenre: function(gid) {
      this.$router.push({name: 'genre', params: { genreId: gid}})
    }
  },
}
</script>

<style>
  .even {
    position: relative;
    top: 20px;
  }
  .col{
  height:400px;
  }
  .col-in:hover{
    opacity:0.5; 
    cursor:pointer;
  }
  /* 장르 카드 전체 css */
  .col-in{
    width: 100%;
    height: 100%;
    overflow: hidden;
  }
  /* 장르별 카드 CSS */
  .horror-card{
    background-image:linear-gradient(0deg, rgba(15,15,15,1) 10%,rgba(255,255,255,0) 40%,rgba(255,255,255,0) 60%, rgba(15, 15, 15, 1)90%), url('@/assets/Horror-card.jpg');
    background-size: cover;
    background-position: center;
  }
  .sf-card{
    background-image:linear-gradient(0deg, rgba(15,15,15,1) 10%,rgba(255,255,255,0) 40%,rgba(255,255,255,0) 60%, rgba(15, 15, 15, 1)90%), url('@/assets/SF-card.jpg');
    background-size: contain;
  }
  .anime-card{
    background-image:linear-gradient(0deg, rgba(15,15,15,1) 10%,rgba(255,255,255,0) 40%,rgba(255,255,255,0) 60%, rgba(15, 15, 15, 1)90%), url('@/assets/Anime-card.jpg');
    background-size: cover;
    background-position: center;
  }
  .action-card{
    background-image:linear-gradient(0deg, rgba(15,15,15,1) 10%,rgba(255,255,255,0) 40%,rgba(255,255,255,0) 60%, rgba(15, 15, 15, 1)90%), url('@/assets/Action-card.jpg');
    background-size: contain;
    background-position: center;
  }
  .drama-card{
    background-image:linear-gradient(0deg, rgba(15,15,15,1) 10%,rgba(255,255,255,0) 40%,rgba(255,255,255,0) 60%, rgba(15, 15, 15, 1)90%), url('@/assets/Drama-card.jpg');
    background-size: cover;
    background-position: center;
  }
  .docu-card{
    background-image:linear-gradient(0deg, rgba(15,15,15,1) 10%,rgba(255,255,255,0) 40%,rgba(255,255,255,0) 60%, rgba(15, 15, 15, 1)90%), url('@/assets/Docu-card.jpg');
    background-size: cover;
    background-position: center;
  }
  .comedy-card{
    background-image:linear-gradient(0deg, rgba(15,15,15,1) 10%,rgba(255,255,255,0) 40%,rgba(255,255,255,0) 60%, rgba(15, 15, 15, 1)90%), url('@/assets/Comedy-card.jpg');
    background-size: cover;
    background-position-x: 20em;
  }

  /*  */
  .genre-name{
    position: relative;
    height: 4em;
    bottom: 14em;
    background:linear-gradient(0deg, rgba(0,0,0,0.5), rgba(0, 0, 0, 0.5));
  }
  p {
    font-size: 1.3em;
    margin-bottom: 0;
    color: white;
  }
</style>