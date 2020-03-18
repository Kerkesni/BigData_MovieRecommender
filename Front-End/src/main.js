import Vue from 'vue'
import App from './App.vue'
import VueLodash from 'vue-lodash'
import lodash from 'lodash'
import store from './store'

Vue.use(VueLodash, {
  lodash
})

Vue.config.productionTip = false

new Vue({
  store,
  render: h => h(App)
}).$mount('#app')