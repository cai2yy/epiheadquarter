const express = require("express")

const app = express()


app.use(require('cors')())
app.use(express.json())

app.set('secret', 'sault blabla');

require('./plugins/db')(app)
require('./routes/admin')(app)

app.get('/', (req, res) => {
  res.send('root');
});

app.listen(3000, () => {
  console.log('http://localhost:3000');
});