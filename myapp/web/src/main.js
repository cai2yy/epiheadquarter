import Vue from "vue";
import App from "./App.vue";
import router from "./router";

Vue.config.productionTip = false;

import "./assets/iconfont/iconfont.css";
import "./assets/scss/style.scss";
import "./plugins/element.js";

import VueAwesomeSwiper from "vue-awesome-swiper";
// require styles
import "swiper/dist/css/swiper.css";
Vue.use(VueAwesomeSwiper /* { default global options } */);

//axios
// const API_PROXY = "https://bird.ioliu.cn/v1/?url=";
import axios from "axios";
Vue.prototype.$http = axios.create({
  // baseURL: `${API_PROXY}https://cdn.ipayy.net/yiqing/api.php`
  baseURL: `http://api.tianapi.com/txapi/ncovcity/index?key=45126bf7a0b423d5ee6fd2f63ff24cd4`
});

//Card
import Card from "./components/Card.vue";
Vue.component("m-card", Card);

// 引入echarts
import echarts from "echarts";
Vue.prototype.$echarts = echarts;

// 还要特别引入china.json，这样中国地图才会出现，不然只会出现右下角的南海诸岛

import "echarts/map/js/china"; // 这个是js引用
import china from "echarts/map/json/china.json";
echarts.registerMap("china", china);

//
import store from "./store";

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
