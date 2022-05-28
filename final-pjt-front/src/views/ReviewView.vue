<template>
  <div>
    <div class="for-nav" style="height: 5em;"></div>
    <div class="for-nav" style="height: 5em;"></div>
    <div class="container">
      <div class="row poster-row">
        <div class="col-4 poster-box">
          <img :src="path + detail.poster_path" alt="" class="poster" @click="goToDetail(detail)">
          <div class="title align-self-start d-flex flex-column align-items-center" >
            <p>{{detail.title}}</p>
            <div class="botton-box d-flex justify-contetn-start my-2">
              <button type="button" class="btn btn-outline-light mx-2" v-for="genre, idx in detail.genres" :key="idx">{{ genre.genre_name }}</button> 
            </div>
          </div>
        </div>
        <div class="col detail d-flex flex-column">
          <!-- 영화 상세정보 -->
          
          <div class="d-flex review-title aligh-self-start mt-5">
            <h1 class="text-start me-2">{{review.title}}</h1>
            <button type="button" class="btn mx-2 btn-danger" @click="updateReview" v-if="currentUser.pk === review.user.pk">Update</button>
            <button type="button" class="btn mx-2 btn-danger" @click="deleteReview" v-if="currentUser.pk === review.user.pk">Delete</button>
          </div>
          <div class="d-flex align-items-center mt-3">
            <p class="mt-1 mx-1 user-name" @click="goToProfile(review.user.username)"> posted by {{review.user.username}}</p>
            <i class="fa-solid fa-star fa-xl mx-1"></i>
            <button type="button" class="mt-1 me-2 btn btn-outline-light rating-btn">{{review.rating}}</button>
            <i class="fa-solid fa-thumbs-up fa-xl mx-1"></i>
            <button type="button" class="mt-1 me-2 btn btn-outline-light rating-btn" @click="likeReview">{{review.good_eval_count}}</button>
            <i class="fa-solid fa-thumbs-down mx-1 fa-xl"></i>
            <button type="button" class="mt-1 me-2 btn btn-outline-light rating-btn" @click="badReview">{{review.bad_eval_count}}</button> 
          </div>
          <div class="d-flex mt-5">
            <p>{{review.content}}</p>
          </div>
        </div>
      </div>

      <div>
        <form @submit.prevent="commentCreate" id="comment-form">
          <div class="d-flex my-2 comment-input">
            <input type="text" id="inputPassword5" class="form-control mx-2" @input="changeKeyword" :value="content">
            <button type="submit" class=" btn btn-light comment-btn">submit</button>
          </div>
        </form>  
      </div>
      <ol class="list-group comment-list">
        <li class="list-group-item d-flex flex-column" v-for="comment, idx in commentList" :key="idx">
          <div class=" d-flex justify-content-between align-items-start ">
            <div class="ms-2 me-auto d-flex flex-column align-items-start">
              <div class="fw-bold comment-user-name" @click="goToProfile(comment.user)">
                {{comment.user.username}}
              </div>
              {{comment.content}}
            </div>
            <div>
              <button class="btn btn-secondary mx-1" type="button"  @click="deleteComment(comment)" v-if="currentUser.pk === comment.user.pk">
                delete
              </button>
              <button class="btn btn-secondary mx-1" type="button" data-bs-toggle="collapse" :data-bs-target="`#collapseExample-${idx}`" aria-expanded="false" aria-controls="collapseExample">
                comment
              </button>
            </div>
          </div>
          
          <ol class="list-group cocomment-list">
            <li class="list-group-item d-flex flex-column" v-for="cocomment, idx in comment.replies" :key="idx">
              <div class=" d-flex justify-content-between align-items-start ">
                <div class="ms-2 me-auto d-flex flex-column align-items-start">
                  <div class="fw-bold comment-user-name" @click="goToProfile(comment.user)">
                    {{cocomment.username}}
                  </div>
                  {{cocomment.content}}
                </div>
                <div>
                  <button class="btn btn-secondary mx-1" type="button"  @click="deleteComment(comment)" v-if="currentUser.pk === cocomment.user">
                    delete
                  </button>
                </div>
              </div>
            </li>
          </ol>

          <form @submit.prevent="coCommentCreate(comment)" class="collapse" :id="`collapseExample-${idx}`">
            <div class="d-flex my-2 comment-input">
              <input type="text" id="inputPassword5" class="form-control mx-2" @input="changeKeyword" :value="content">
              <button type="submit" class=" btn btn-light comment-btn" data-bs-toggle="collapse" :data-bs-target="`#collapseExample-${idx}`" aria-expanded="false" aria-controls="collapseExample">submit</button>
            </div>
          </form>
        </li>
      </ol>
      <div>
      </div>

    </div>
  </div>
</template>

<script>
export default {
  name: "ReviewView",
  created: function () {
    this.$store.dispatch('sendDetailRequest', this.movieId)
    this.$store.dispatch('sendReviewRequest', this.idPack)
    this.$store.dispatch('getCommentList', this.commentPack)
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
      reviewId: this.$route.params.reviewPk,
      idPack: {
        movieId: this.$route.params.movieId, 
        reviewId: this.$route.params.reviewPk
        },
      content: '',
      commentPack: {
        movieId: this.$route.params.movieId, 
        reviewId: this.$route.params.reviewPk,
        commentId: '',
        content: ''
      },
    }
  },
  computed:  {
    detail: function() {
      return this.$store.getters.movieDetail
    },
    review: function() {
      return this.$store.getters.reviewDetail
    },
    currentUser: function() {
      return this.$store.getters.currentUser
    },
    commentList: function() {
      return this.$store.getters.commentList
    }
  },
  methods: {
    updateReview: function() {
      this.$router.push({name: 'updateReview', params: {movieId: this.idPack.movieId, reviewId : this.idPack.reviewId, title: this.review.title, content: this.review.content, rating: this.review.rating}})
    },
    gotoReview: function(movieId, reviewId){
      this.$router.push({name: 'reviewView', params: {movieId: movieId,reviewPk: reviewId }})
    },
    likeReview: function() {
      this.$store.dispatch('sendReviewLikeRequest', this.idPack)
    },
    goToDetail: function(movieData) {
      this.$router.push({name: 'movieDetail', params: { movieId: movieData.movie_id, movie: movieData}})
    },
    badReview: function() {
      this.$store.dispatch('sendReviewBadRequest', this.idPack)
    },
    deleteReview: function() {
      this.$store.dispatch('deleteReview', this.idPack)
    },
    changeKeyword: function(event) {
      this.content = event.target.value
      event.target.value= this.content
    },
    commentCreate: function() {
      this.commentPack.content = this.content
      this.$store.dispatch('createComment', this.commentPack)
      this.content =''
    },
    deleteComment: function(comment) {
      this.commentPack.commentId = comment.id
      this.$store.dispatch('deleteComment', this.commentPack)
    },
    coCommentCreate: function(comment) {
      this.commentPack.content = this.content
      this.commentPack.commentId = comment.id
      console.log(this.commentPack)
      this.$store.dispatch('createCoComment', this.commentPack)
      this.content =''
    },
    goToProfile: function(user) {
      this.$router.push({name: 'profile', params: {username: user.username}})
    }

    // 잘라내기 해서 리뷰 작성페이지로 보내기

  },
  watch: {
    review(val){
      this.review.good_eval_count = val.good_eval_count
      this.review.bad_eval_count = val.bad_eval_count
    }
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
  .like-btn{
    height: 80%;
  }
  .comment-list li, input{
    background: rgba(30, 30, 30, 1);
    color: white;
  }
  .comment-input input, button{
    background: rgba(30, 30, 30, 1);
    color: white;
  }
  .comment-delete-btn:hover{
    cursor: pointer;
  }
  .comment-list{
    list-style: none;
  }
  .cocomment-list li, input{
    background: rgba(50, 50, 50, 1);
    color: white;
  }
  .comment-user-name:hover{
    cursor: pointer;
  }
  .user-name:hover{
    cursor: pointer;
  }

  .review-title button{
    height: 80%;
  }

</style>