import axios from "axios";
import Vue from "vue";
import router from "./router";

//给Vue挂载一些东西的时候一定要放在new Vue前面，要不然刷新页面时候按照Vue的流程，会出现没挂上的情况
const http = axios.create({
  baseURL: "http://localhost:3000/admin/api"
});

http.interceptors.request.use(
  config => {
    if (localStorage.token) {
      config.headers.Authorization = "Bearer " + localStorage.token;
    }
    return config;
  },
  err => {
    return Promise.reject(err);
  }
);

http.interceptors.response.use(
  res => {
    return res;
  },
  err => {
    if (err.response.data.message) {
      Vue.prototype.$message({
        type: "error",
        message: err.response.data.message
      });
    }

    if (err.response.status === 401) {
      console.log("login");
      router.push("/login");
    }
    return Promise.reject(err);
  }
);

export default http;
