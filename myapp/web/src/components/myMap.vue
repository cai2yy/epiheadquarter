<template>
  <m-card title="疫情地图">
    <div id="myChartChina" :style="{ width: '400px', height: '400px' }"></div>
  </m-card>
</template>

<script>
import axios from "axios";
export default {
  data: function() {
    return {
      data: []
    };
  },
  methods: {
    async fetch() {
     
    },
    async drawLine() {
      // 基于准备好的dom，初始化echarts实例
      var myChartContainer = document.getElementById("myChartChina");
      var resizeMyChartContainer = function() {
        myChartContainer.style.width = document.body.offsetWidth + "px"; //页面一半的大小
      };
      resizeMyChartContainer();
      var myChartChina = this.$echarts.init(myChartContainer);

      function randomData() {
        return Math.round(Math.random() * 500);
      }
      randomData();
      var chinaPieces = [
        {
          min: 10000,
          max: 1000000,
          label: "大于等于10000人",
          color: "#372a28"
        },
        { min: 500, max: 9999, label: "确诊500-9999人", color: "#4e160f" },
        { min: 100, max: 499, label: "确诊100-499人", color: "#974236" },
        { min: 10, max: 99, label: "确诊10-99人", color: "#ee7263" },
        { min: 1, max: 9, label: "确诊1-9人", color: "#f5bba7" }
      ];

       const http2 = axios.create({
        // baseURL: `${API_PROXY}https://cdn.ipayy.net/yiqing/api.php`
        baseURL: `http://api.tianapi.com/txapi/ncovcity/index?key=45126bf7a0b423d5ee6fd2f63ff24cd4`
      });
      const res1 = await http2.get("");
      let data = res1.data.newslist;
      let temp = [];
      data.forEach(item => {
        let o = {
          name: item.provinceShortName,
          value: item.currentConfirmedCount,
          label: {
            textStyle: {
              fontSize: 7
            }
          }
        };
        temp.push(o);
      });
      // 绘制图表
      var optionMap = {
        tooltip: {},
        legend: {
          orient: "vertical",
          left: "left",
          data: [""]
        },
        visualMap: {
          type: "piecewise",
          pieces: chinaPieces,
          textStyle: {
            color: "#000000"
          },
          inRange: {
            color: ["lightskyblue", "yellow", "orangered"]
          },
          min: 0,
          max: 1500,
          left: "0%",
          top: "65%"
        },
        selectedMode: "single",
        series: [
          {
            name: "",
            type: "map",
            mapType: "china",
            itemStyle: {
              normal: {
                borderColor: "rgba(0, 0, 0, 0.2)"
              },
              emphasis: {
                shadowOffsetX: 0,
                shadowOffsetY: 0,
                shadowBlur: 20,
                borderWidth: 0,
                shadowColor: "rgba(0, 0, 0, 0.5)"
              }
            },
            zoom: 1.2,
            showLegendSymbol: true,
            label: {
              normal: {
                show: true
              },
              emphasis: {
                show: true
              }
            },
            data: temp
          }
        ]
      };

      myChartChina.setOption(optionMap);
      window.onresize = function() {
        resizeMyChartContainer();
        myChartChina.resize();
      };
    }
  },

  mounted() {
    this.fetch();

    this.drawLine();
  }
};
</script>

<style></style>
