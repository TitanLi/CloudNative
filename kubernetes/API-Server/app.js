const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const Joi = require('joi');
const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
// postman
app.use(bodyParser.json());
app.get('/', (req, res) => {
    for(let i=0;i<Number(req.query.apple);i++){
        let data = Math.random();
        console.log(data);
    }
    res.send('ok');
});

app.listen(3000);
