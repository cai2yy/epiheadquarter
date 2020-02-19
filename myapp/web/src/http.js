//axios
// const API_PROXY = "https://bird.ioliu.cn/v1/?url=";
import axios from "axios";
const http = axios.create({
  // baseURL: `${API_PROXY}https://cdn.ipayy.net/yiqing/api.php`
  baseURL: `http://api.tianapi.com/txapi/ncovcity/index?key=45126bf7a0b423d5ee6fd2f63ff24cd4`
});

export default http;
