<template>
  <div>
    <div class="for-nav"></div>
    <div class="sign-up-form">
      <h1 style="color: rgba(240,240,240,1);" class="mb-5">Review</h1>

      <div class="form-box d-flex justify-content-center">
        <div class="form-content">
          <form @submit.prevent="writeReview(credentials)" class="d-flex flex-column align-items-start my-1">
            <div class="d-flex justify-content-between form-item align-items-center">
              <label for="username" style="color: rgba(240,240,240,1);">Title: </label>
              <input  v-model="credentials.title" type="text" id="title" class="my-1" required/>
            </div>
            <div class="d-flex justify-content-between form-item align-items-center">
              <label for="password1" style="color: rgba(240,240,240,1);">Content: </label>
              <textarea v-model="credentials.content" type="text" id="content" class="my-1" required />
            </div>
            <div class="d-flex justify-content-between form-item align-items-center">
              <label for="password2" style="color: rgba(240,240,240,1);">Rating:</label>
              <!-- <input v-model="credentials.rating" type="number" id="rating" class="my-1" required /> -->
              <star-rating :increment="0.5" :star-size="30" :show-rating="false" v-model="credentials.rating"></star-rating>
            </div>
            <div class="d-flex form-item justify-content-end">
              <button class="my-1">Submit</button> 
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import StarRating from 'vue-star-rating'
export default {
  name: 'WriteReview',
  components:{
    StarRating,
  },
  data: function() {
    return {
      credentials: {
        movie_id: '',
        title: '',
        content: '',
        rating: null,
      }
    }
  },
  methods: {
    writeReview: function() {
      this.credentials.rating = this.credentials.rating * 2
      this.credentials.movie_id = this.$route.params.movieId
      this.$store.dispatch('writeReview', this.credentials)
    }
  }
}
</script>

<style>

</style>