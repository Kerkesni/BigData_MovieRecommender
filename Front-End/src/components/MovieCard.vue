<template>
  <div class="tile is-vertical box">
    <img
      class="cover"
      :src="'http://image.tmdb.org/t/p/w500/' + cover"
      :alt="title"
    />
    <StarRating
      class="rating"
      v-model="value"
      :show-rating="false"
      :star-size="40"
      @rating-selected="setRating"
      v-if="canRate"
    ></StarRating>
    <span class="title">{{ this.title }}</span>
  </div>
</template>

<script>
import axios from "axios";
import StarRating from "vue-star-rating";

export default {
  props: ["title", "id", "canRate"],
  components: {
    StarRating
  },
  data() {
    return {
      cover: "",
      value: 0
    };
  },
  watch: {
    title: function() {
      this.getCover();
    }
  },
  methods: {
    getCover: function() {
      if (!this.title) return;
      var titleNoDate = this.title.substring(0, this.title.indexOf("("));
      axios
        .get(
          "https://api.themoviedb.org/3/search/movie?api_key=15d2ea6d0dc1d476efbca3eba2b9bbfb&query=" +
            titleNoDate
        )
        .then(json => {
          this.cover = json.data.results[0].poster_path;
        })
        .catch(console.log);
    },
    setRating: function(val) {
      this.$store.commit("addMovie", {
        movieId: this.id,
        title: this.title,
        rating: val.toFixed(1),
        timestamp: Math.floor(Date.now() / 1000)
      });
      this.$emit("next");
    }
  },
  mounted() {
    this.getCover();
  },
  updated() {
    this.$store.commit("selectMovie", this.title);
    this.value = this.$store.getters.getRating;
  }
};
</script>

<style lang="scss" scoped>
@import "../../node_modules/bulma/bulma";

.box {
  text-align: -webkit-center;
  width: 500px;
  min-height: 550px !important;
  .cover {
    width: 20em;
    margin: auto;
  }
  .title {
    padding-top: 0.5em;
    font-size: 2em;
    margin: auto;
  }
  .rating {
    padding-top: 0.5em;
    min-height: auto;
    margin: auto;
  }
}
</style>
