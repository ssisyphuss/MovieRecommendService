const HOST = 'http://localhost:8000/api/v1/'

const ACCOUNTS = 'accounts/'
const COMMUNITIES = 'communities/'
// const COMMENTS = 'comments/'
const MOVIES = 'movies/'

export default {
  accounts: {
    login: () => HOST + ACCOUNTS + 'login/',
    logout: () => HOST + ACCOUNTS + 'logout/',
    signup: () => HOST + ACCOUNTS + 'signup/',
    // Token 으로 현재 user 판단
    currentUserInfo: () => HOST + ACCOUNTS + 'user/',
    // username으로 프로필 제공
    profile: username => HOST + ACCOUNTS + 'profile/' + username,
    saveLikes: () => HOST + ACCOUNTS + 'likes_movie/',
    follow: username => HOST + ACCOUNTS + 'profile/' + username +'/follow',
    searchUser: () => HOST + ACCOUNTS + 'search/'
  },
  communities: {
    // /articles/
    // articles: () => HOST + ARTICLES,
    // /articles/1/
    // article: articlePk => HOST + ARTICLES + `${articlePk}/`,
    // likeArticle: articlePk => HOST + ARTICLES + `${articlePk}/` + 'like/',
    // comments: articlePk => HOST + ARTICLES + `${articlePk}/` + COMMENTS,
    // comment: (articlePk, commentPk) =>
    //   HOST + ARTICLES + `${articlePk}/` + COMMENTS + `${commentPk}/`,
    writeReview: (movieId) =>
      HOST + COMMUNITIES + `${movieId}/` +'review_create/',
    reviewDetail: (reviewId, movieId) =>
      HOST + COMMUNITIES + `${movieId}/` + `${reviewId}/`,
    reviewLike: (reviewId, movieId) =>
      HOST + COMMUNITIES + `${movieId}/` + `${reviewId}/` + 'good/',
    reviewBad: (reviewId, movieId) =>
    HOST + COMMUNITIES + `${movieId}/` + `${reviewId}/` + 'bad/',
    genreReviews: (genreId) =>
      HOST + COMMUNITIES +'genre-reviews/' + `${genreId}/`,
    updateReview: (reviewId, movieId) =>
      HOST + COMMUNITIES + `${movieId}/` + `${reviewId}/`+ 'update/',
    commentCreate: (reviewId) =>
      HOST + COMMUNITIES + 'review/' + `${reviewId}/` + 'comment_create/',
    getCommentList: (reviewId) =>
      HOST + COMMUNITIES + 'review/' + `${reviewId}/` +'comments/',
    deleteComment: (reviewId, commentId) =>
      HOST + COMMUNITIES + 'review/' + `${reviewId}/` + 'comment_delete/' + `${commentId}/`,
    coCommentCreate: (reviewId,commentId) =>
      HOST + COMMUNITIES + 'review/' + `${reviewId}/` + 'comment_create/' + `${commentId}/`,
    
    
  },
  movies: {
    chooseMovies: () => HOST + MOVIES + 'signup_movies/',
    homeMainMovies: () => HOST + MOVIES + 'main_page_recommend/',
    genreMainMovies: (genreId) => HOST + MOVIES + 'genre_main_page/' + `${genreId}`,
    sendSearchRequest: () => HOST + MOVIES + 'search/',
    sendDetailRequest: () => HOST + MOVIES + 'detail/',
    movieRecommendation: (genreId) => HOST + MOVIES + 'genre_recommend/' + `${genreId}`
  }
}
