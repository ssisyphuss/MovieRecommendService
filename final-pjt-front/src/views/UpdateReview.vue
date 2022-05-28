<template>
  <div>
    <div class="for-nav"></div>
    <div class="sign-up-form">
      <h1 style="color: rgba(240,240,240,1);" class="mb-5">Review {{ $route.params.movieId }}</h1>
      <div class="form-box d-flex justify-content-center">
        <div class="form-content">
          <form @submit.prevent="updateReview(credentials)" class="d-flex flex-column align-items-start my-1">
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
              <star-rating :increment="0.5" :show-rating="false" v-model="credentials.rating"></star-rating>
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
  name: 'UpdateReview',
  components:{
    StarRating,
  },
  created: function() {
    this.credentials.movie_id = this.$route.params.movieId
    this.credentials.title = this.$route.params.title
    this.credentials.review_id = this.$route.params.reviewId
    this.credentials.content = this.$route.params.content
    this.credentials.rating = this.$route.params.rating
  },
  data: function() {
    return {
      credentials: {
        movie_id: '',
        review_id: null,
        title: '',
        content: '',
        rating: null,
      }
    }
  },
  methods: {
    updateReview: function() {
      this.credentials.rating = this.credentials.rating * 2
      this.$store.dispatch('updateReview', this.credentials)
    }
  }
}
</script>

<style>

</style>