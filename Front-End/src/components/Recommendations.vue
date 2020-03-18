<template>
  <div class="box">
    <span class="title">Recommendations:</span>
    <div class="columns">
      <div class="column" v-for="(movie, index) in movies" :key="index">
        <MovieCard :title="movie" :id="index" :canRate="false" />
      </div>
    </div>
  </div>
</template>

<script>
import MovieCard from "./MovieCard.vue";

export default {
  props: ["movies"],
  components: {
    MovieCard
  },
  mounted() {
    window.scrollBy(0,document.body.scrollHeight)
  },
};
</script>

<style lang="scss" scoped>
@import "../../node_modules/bulma/bulma";

.box {
  margin-top: 2em;
  overflow: scroll;
}

.title {
  position: absolute;
}

::-webkit-scrollbar {
  display: none;
}
</style>
