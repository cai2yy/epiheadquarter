<template>
  <div>
    <el-form
      @submit.native.prevent="saveArticle"
      ref="article"
      :model="article"
      label-width="80px"
    >
      <el-form-item label="文章标题">
        <el-input v-model="article.title"></el-input>
      </el-form-item>
      <el-form-item label="文章内容">
        <vue-editor v-model="article.content"></vue-editor>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit">立即创建</el-button>
        <el-button>取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import { VueEditor } from "vue2-editor";
export default {
  components: {
    VueEditor
  },
  data() {
    return {
      article: {
        title: "",
        content: ""
      }
    };
  },
  methods: {
    saveArticle() {
      this.$http.post("/rest/articles", this.article).then(res => {
        console.log(res.data);
        this.$message({
          showClose: true,
          message: "创建成功",
          type: "success"
        });
        this.$router.push("/articles/index");
      });
    }
  }
};
</script>
