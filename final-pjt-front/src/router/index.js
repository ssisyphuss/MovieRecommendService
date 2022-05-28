import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue'
import GenreView from '../views/GenreView.vue'
import BoardView from '../views/BoardView.vue'
import ProfileView from '../views/ProfileView.vue'
import SignUp from '../views/SignUp.vue'
import ChooseMovie from '../views/ChooseMovie.vue'
import SignIn from '../views/SignIn.vue'
import LogOut from '../views/LogoutView.vue'
import MovieDetail from '../views/MovieDetail.vue'
import WriteReview from '../views/WriteReview.vue'
import ReviewView from '../views/ReviewView.vue'
import GenreMovie from '../views/GenreMovie.vue'
import CommunityView from '../views/CommunityView.vue'
import UpdateReView from '../views/UpdateReview.vue'
import SearchView from '../views/SearchView.vue'
import store from '../store'
Vue.use(VueRouter)
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/genre/:genreId',
    name: 'genre',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: GenreView,
  },
  {
    path: '/board/:genreId',
    name: 'board',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: BoardView,
  },
  {
    path: '/signup',
    name: 'signup',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: SignUp,
  },
  {
    path: '/signup/choose/:username',
    name: 'choosemovie',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: ChooseMovie,
  },
  {
    path: '/signin',
    name: 'signin',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: SignIn,
  },
  {
    path: '/:movieId',
    name: 'movieDetail',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: MovieDetail,
  },
  {
    path: '/:genreId/movies',
    name: 'genreMovie',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: GenreMovie,
  },
  {
    path: '/:genreId/community',
    name: 'genreCommunity',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: CommunityView,
  },
  {
    path: '/search',
    name: 'searchView',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: SearchView,
  },



  // 로그인이 필요한 라우팅
  {
    path: '/logout',
    name: 'logout',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: LogOut,
  },
  {
    path: '/:movieId/:reviewPk',
    name: 'reviewView',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: ReviewView,
  },
  
  {
    path: '/review/:movieId',
    name: 'writeReview',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: WriteReview,
  },
  {
    path: '/profile/:username',
    name: 'profile',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: ProfileView,
  },
  {
    path: '/review/:movieId/reviewId/update',
    name: 'updateReview',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: UpdateReView,
  },

  
]



const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

router.beforeEach((to, from, next) => {
  const { isLoggedIn } = store.getters
  const authPages = ['logout', 'writeReview', 'profile', 'reviewView', 'updateReview']
  const isAuthRequired = authPages.includes(to.name)
  if (isAuthRequired && !isLoggedIn) {
    next({name: 'signin'})
  }
  else {
    next()
  }
})

export default router
