<template>
  <div class="card bg-white p-3 mt-3">
    <div class="card-header d-flex ai-center pb-3">
      <div class="fs-xl flex-1 px-2">
        <div class="title">
        <strong class="px-2">{{ title }}</strong>
        </div>
      </div>
    </div>
    <div class="card-body pt-3">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    title: { type: String, required: true }
  }
};
</script>

<style lang="scss">
@import "../assets/scss/_variables.scss";
.card {
  border-bottom: 1px solid map-get($map: $colors, $key: "grey");
  .card-header {
    border-bottom: 1px solid map-get($map: $colors, $key: "light-1");
    .title {
      border-left: 4px solid map-get($map: $colors, $key: "blue");
    }
  }
}
</style>
