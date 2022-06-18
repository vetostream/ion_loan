import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import Buefy from 'buefy'
import 'buefy/dist/buefy.css'
import "@fortawesome/fontawesome-free/css/all.css"
import "@fortawesome/fontawesome-free/css/fontawesome.css"
import VueFormulate from '@braid/vue-formulate'
import VueMask from 'v-mask'
import moment from 'moment'

const toCurrency = new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'PHP'
})

Vue.use(VueFormulate)
Vue.use(VueMask)
Vue.use(Buefy, {
  defaultIconPack: 'fas'
})

Vue.filter('displayMoney', (value) => {
    return toCurrency.format(value)
});

Vue.filter('shortDate', (value) => {
  return moment(value).format('MM/DD/YYYY')
});

Vue.filter('monthYearDate', (value) => {
  return moment(value).format('MMM YYYY')
});

Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
