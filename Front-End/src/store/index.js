import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    tasteProfile: [],
    selected: {}
  },
  getters: {
    getProfile: (state) => {
      return state.tasteProfile.map((movieData) => {
        return {
          'movieId': movieData.movieId,
          'rating': movieData.rating,
          'timestamp':movieData.timestamp
        }
      })
    },
    getRating: (state) => {
      if (state.selected && state.selected.rating)
        return state.selected.rating
      else return 0
    },
    getTasteCount: (state) => {
      return state.tasteProfile.length
    }
  },
  mutations: {
    addMovie: (state, movie) => {
      state.tasteProfile = state.tasteProfile.filter((data) => {
        return data.title !== movie.title
      })
      state.tasteProfile.push(movie)
    },
    removeMovie: (state, title) => {
      Vue.prototype._.remove(state.tasteProfile, (movie) => {
        movie.title === title
      })
    },
    selectMovie: (state, title) => {
      state.selected = state.tasteProfile.find((movie) => movie.title === title)
    },
    clearMovies: (state) => {
      state.tasteProfile = []
      state.selected = {}
    }
  },
})