const express = require("express");
const app = express();

app.use(require("cors")());
app.use(express.json());
const mongoose = require("mongoose");

mongoose.connect("mongodb://localhost:27017/element-admin", {
  useCreateIndex: true,
  useFindAndModify: true,
  useNewUrlParser: true,
  useUnifiedTopology: true
});

const ArticleSchema = new mongoose.Schema({
  title: { type: String, unique: true },
  body: { type: String }
});

const Article = mongoose.model("Article", ArticleSchema);

app.get("/", async (req, res) => {
  res.send("index");
});

//获取文章列表
app.get("/api/articles", async (req, res) => {
  const articles = await Article.find();
  res.send(articles);
});

//id查询
app.get("/api/articles/:id", async (req, res) => {
  const article = await Article.findById(req.params.id);
  res.send(article);
});

//新增文章
app.post("/api/articles", async (req, res) => {
  const article = await Article.create(req.body);
  article.save();
  res.send(article);
});

//编辑文章
app.put("/api/articles/:id", async (req, res) => {
  // const article = await Article.findById(req.params.id);
  // console.log(req.body);
  // article.title = req.body.title;
  // article.body = req.body.body;
  // await article.save();
  const article = await Article.findByIdAndUpdate(req.params.id, req.body);
  res.send(article);
});

//删除文章
app.delete("/api/articles/:id", async (req, res) => {
  await Article.findByIdAndDelete(req.params.id);
  res.send({
    message: "删除成功"
  });
});

app.listen(3001, () => {
  console.log("App listening on port http://localhost:3001");
});
