import axios from 'axios'
import drf from '@/api/drf'
import router from '@/router'

export default{
  state: {
    reviewDetail: {},
    genreReviews : [],
    commentList: [],
  },
  getters: {
    reviewDetail: state => state.reviewDetail,
    genreReviews: state => state.genreReviews,
    commentList: state => state.commentList,
  },
  mutations: {
    setReviewDetail: function(state, review) {
      state.reviewDetail = review
    },
    setGenreReviews: function(state, reviews) {
      state.genreReviews = reviews
    },
    setCommentList: function(state, comments) {
      state.commentList = comments
    }
  },
  actions: {
    writeReview: function({getters}, credentials) {
      axios({
        method:'post',
        url: drf.communities.writeReview(credentials.movie_id),
        data: credentials,
        headers: getters.authHeader
      })
        .then(() =>
          router.push({name: 'movieDetail', params: { movieId: credentials.movie_id,}})
        )
    },
    sendReviewRequest: function({commit}, idPack){
      axios({
        method:'get',
        url: drf.communities.reviewDetail(idPack.reviewId, idPack.movieId)
      })
        .then( function(res) {
          commit('setReviewDetail', res.data)
        }
        
        )
    },
    sendReviewLikeRequest: function({getters, dispatch}, idPack) {
      axios({
        method: 'post',
        url: drf.communities.reviewLike(idPack.reviewId, idPack.movieId),
        headers: getters.authHeader
      })
        .then( () =>
          dispatch('sendReviewRequest', idPack)
        )
    },
    sendReviewBadRequest: function({getters, dispatch}, idPack) {
      axios({
        method: 'post',
        url: drf.communities.reviewBad(idPack.reviewId, idPack.movieId),
        headers: getters.authHeader
      })
        .then( () =>
          dispatch('sendReviewRequest', idPack)
        )
    },
    getReviews: function({commit}, genreId){
      axios({
        method: 'get',
        url: drf.communities.genreReviews(genreId)
      })
        .then((res) =>
          commit('setGenreReviews', res.data)
        )
    },
    updateReview: function({getters}, credentials) {
      axios({
        method:'put',
        url: drf.communities.updateReview(credentials.review_id, credentials.movie_id),
        data: credentials,
        headers: getters.authHeader
      })
        .then(() =>
          router.push({name: 'reviewView', params: { movieId: credentials.movie_id, reviewPk: credentials.review_id}})
        )
    },
    deleteReview: function({getters}, idPack) {
      axios({
        method: 'delete',
        url: drf.communities.updateReview(idPack.reviewId, idPack.movieId),
        headers: getters.authHeader,
      })
        .then(() =>
      router.push({name:'home'})
      )
    },
    getCommentList: function({commit}, commentPack) {
      axios({
        method: 'get',
        url: drf.communities.getCommentList(commentPack.reviewId)
      })
        .then((res) =>
        commit('setCommentList', res.data)
        )
    },

    createComment: function({getters, dispatch}, commentPack) {
      axios({
        method: 'post',
        url: drf.communities.commentCreate(commentPack.reviewId),
        data: commentPack,  
        headers: getters.authHeader,
      })
        .then(() =>
        dispatch('getCommentList', commentPack)
        )
    },
    deleteComment: function({getters, dispatch},commentPack) {
      console.log(commentPack)
      axios({
        method: 'delete',
        url: drf.communities.deleteComment(commentPack.reviewId, commentPack.commentId),
        headers: getters.authHeader,
      })
      .then(() =>
      dispatch('getCommentList',commentPack)
      )
    },
    createCoComment: function({getters, dispatch}, commentPack) {
      axios({
        method: 'post',
        url: drf.communities.coCommentCreate(commentPack.reviewId, commentPack.commentId),
        data: commentPack,
        headers: getters.authHeader
      })
        .then(() =>
        dispatch('getCommentList', commentPack))
    },

  },
}