const mongoose = require("mongoose");

const schema = new mongoose.Schema({
  title: { type: String },
  content: { type: String }
});

module.exports = mongoose.model("Article", schema);
