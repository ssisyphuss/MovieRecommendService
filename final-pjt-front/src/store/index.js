import Vue from 'vue'
import Vuex from 'vuex'

import movies from './modules/movies'
import accounts from './modules/accounts'
import communities from './modules/communities'

Vue.use(Vuex)

export default new Vuex.Store({
  modules: { accounts, movies, communities },
})
