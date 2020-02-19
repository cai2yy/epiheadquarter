<template>
  <div>
    <el-table :data="articles">
      <el-table-column prop="_id" label="ID" width="140"> </el-table-column>
      <el-table-column prop="title" label="标题" width="140"> </el-table-column>
      <el-table-column prop="content" label="内容"> </el-table-column>
      <el-table-column fixed="right" label="操作" width="100">
        <template slot-scope="scope">
          <!-- {{scope.row}} -->
          <el-button @click="edit(scope.row._id)" type="text" size="small"
            >编辑</el-button
          >
          <el-button @click="remove(scope.row._id)" type="text" size="small"
            >删除</el-button
          >
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
export default {
  data() {
    return {
      articles: []
    };
  },
  methods: {
    edit(id) {
      this.$router.push(`/articles/edit/${id}`);
    },
    remove(id) {
      this.$http.delete(`/rest/articles/${id}`).then(res => {
        this.$message({
          showClose: true,
          message: res.data,
          type: "success"
        });
        this.fetchArticles();
      });
    },
    fetchArticles() {
      this.$http.get("/rest/articles").then(res => {
        this.articles = res.data;
      });
    }
  },
  created() {
    this.fetchArticles();
  }
};
</script>
