<template>
  <el-card class="box-card mt-4">
    <el-table :data="items" style="width: 100%">
      <el-table-column type="expand">
        <template class="sub-table" slot-scope="scope">
          <el-table
            :data="scope.row.cities"
            style="width: 100%"
            :show-header="showHeader"
          >
            <el-table-column prop="cityName"> </el-table-column>
            <el-table-column prop="confirmedCount"> </el-table-column>
            <el-table-column prop="currentConfirmedCount"> </el-table-column>
            <el-table-column prop="deadCount"> </el-table-column>
            <el-table-column prop="curedCount"> </el-table-column>
          </el-table>
        </template>
      </el-table-column>
      <el-table-column label="地区" prop="provinceShortName"> </el-table-column>
      <el-table-column label="确诊" prop="confirmedCount"> </el-table-column>
      <el-table-column label="现存确诊" prop="currentConfirmedCount"> </el-table-column>
      <el-table-column label="死亡" prop="deadCount"> </el-table-column>
      <el-table-column label="治愈" prop="curedCount"> </el-table-column>
    </el-table>
  </el-card>
</template>

<script>
export default {
  props: {
    items: { type: Array, required: true }
  },
  data: function() {
    return {
      showHeader: false
    };
  }
};
</script>

<style lang="scss">
.el-table__expanded-cell {
  padding-top: 0% !important;
}
</style>
