<template>
  <m-card :title="title">
    <swiper :options="swiperOption" ref="mySwiper">
      <swiper-slide v-for="(item, index) in items" :key="`${index} + 1`">
        <img class="w-100" :src="item.imgUrl" alt />
      </swiper-slide>
      <div class="swiper-pagination" slot="pagination"></div>
    </swiper>

    <el-row class="w-100 d-flex jc-around pt-2">
      <el-button
        v-for="(item, index) in items"
        :key="`${index} + 1`"
        class="title-btn"
        type="info"
        plain
        size="small"
        @click="changePage(index)"
        >{{ item.title }}</el-button
      >
    </el-row>
  </m-card>
</template>

<script>
export default {
  props: {
    title: { type: String, required: true },
    items: { type: Array, required: true }
  },
  data: function() {
    return {
      data: {},
      swiperOption: {
        pagination: {
          el: ".swiper-pagination",
          clickable: true
        }
      }
    };
  },
  methods: {
    changePage(index) {
      this.$refs.mySwiper.swiper.slideTo(index, 1000, false);
    }
  },
  components: {}
};
</script>

<style scoped></style>
