<template>
  <div class="app">
    <input class="input" type="text" placeholder="Title" v-model="title" />
    <input class="input" type="text" placeholder="Year" v-model="year" />
    <div class="columns">
      <div class="column prev">
        <button class="button" @click="previous">Previous</button>
      </div>
      <div class="column">
        <MovieCard
          :title="movieToShow.title ? movieToShow.title : ''"
          :id="movieToShow.movieId ? movieToShow.movieId : 0"
          :canRate="true"
          @next="next"
        />
      </div>
      <div class="column next">
        <button class="button" @click="next">Next</button>
      </div>
    </div>
    <button
      :disabled="$store.getters.getTasteCount === 0"
      class="button"
      @click="clear"
    >
      Clear Preferences
    </button>
    <br />
    <button :disabled="count < 4" class="button" @click="getRecommendationsPIP">
      Get PIP Recommendation
    </button>
    <button :disabled="count < 4" class="button" @click="getRecommendationsCos">
      Get COS Recommendation
    </button>
    <br>
    <button
      v-if="recommendations.length > 0"
      class="button"
      @click="clearRec"
    >
      Clear Recommendation
    </button>
    <Recommendations
      v-if="recommendations.length > 0"
      :movies="recommendations"
    />
  </div>
</template>

<script>
import { mapGetters } from "vuex";
import axios from "axios";

import MovieCard from "./components/MovieCard";
import Recommendations from "./components/Recommendations";

import movies from "./helpers/movies";

export default {
  components: {
    MovieCard,
    Recommendations
  },
  data() {
    return {
      index: 0,
      year: "",
      title: "",
      recommendations: []
    };
  },
  watch: {
    year: function() {
      this.index = 0;
    },
    title: function() {
      this.index = 0;
    }
  },
  computed: {
    ...mapGetters({
      count: "getTasteCount"
    }),
    mvs: function() {
      var tmp = movies;
      if (this.year)
        tmp = tmp.filter(a =>
          a.title
            .substring(a.title.length - 5, a.title.length - 1)
            .includes(this.year)
        );
      if (this.title)
        tmp = tmp.filter(a =>
          a.title.toLowerCase().includes(this.title.toLowerCase())
        );
      return tmp;
    },
    movieToShow: function() {
      if (this.mvs) return this.mvs[this.index];
      return {};
    }
  },
  methods: {
    next() {
      if (this.index + 1 >= this.mvs.length) this.index = 0;
      else this.index++;
    },
    previous() {
      if (this.index - 1 < 0) this.index = this.mvs.length - 1;
      else this.index--;
    },
    getRecommendationsPIP() {
      axios
        .post("http://localhost:5000/pip", {
          taste: this.$store.getters.getProfile
        })
        .then(res => {
          this.recommendations = res.data;
        })
        .catch(console.log);
    },
    getRecommendationsCos() {
      axios
        .post("http://localhost:5000/cos", {
          taste: this.$store.getters.getProfile
        })
        .then(res => {
          this.recommendations = res.data;
        })
        .catch(console.log);
    },
    clear: function() {
      this.$store.commit("clearMovies");
    },
    clearRec: function(){
      this.recommendations = []
    }
  }
};
</script>

<style lang="scss" scoped>
@import "../node_modules/bulma/bulma";
.app {
  display: grid;
}
.columns {
  padding: 2em;
}
.prev {
  text-align: right;
  margin: auto;
}
.next {
  text-align: left;
  margin: auto;
}
.input {
  margin: auto;
  width: 30%;
  margin-bottom: 1em;
}
.button {
  margin: auto;
  width: 30%;
}
</style>
