<template>
  <div>
    <img class="img" src="../assets/images/bg.png" />

    <div class="bg-white py-3">
      <div class="nav d-flex text-black jc-around">
        <div class="nav-item active">
          <router-link clss="nav-link" tag="div" to="">疫情地图</router-link>
        </div>
        <div class="nav-item">
          <router-link clss="nav-link" tag="div" to="">辟谣与知识</router-link>
        </div>
        <div class="nav-item">
          <router-link clss="nav-link" tag="div" to="">实时播报</router-link>
        </div>
        <div class="nav-item">
          <router-link clss="nav-link" tag="div" to="">疾病知识</router-link>
        </div>
      </div>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  data: function() {
    return {};
  },
  name: "Main",
  components: {}
};
</script>

<style lang="scss">
.img {
  height: 170px;
  width: 404px;
  border: none;
  padding: 0;
}
</style>
