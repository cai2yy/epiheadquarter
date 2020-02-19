<template>
  <div class="pt-3">
    <el-card class="box-card">
      <div slot="header" class="clearfix ">
        <span class="title">{{ item.title }}</span>
      </div>
      <div class="summary">
        {{ item.summary }}
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  props: {
    item: { type: Object, required: true }
  },
  methods: {},
  components: {}
};
</script>

<style lang="scss">
.title {
  font: 1.3rem sans-serif;
  font-weight: 600;
}
.summary {
  color: #999;
}
</style>
