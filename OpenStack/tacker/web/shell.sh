#!/bin/sh
sudo apt-get update
sudo apt-get install -y build-essential libssl-dev
curl https://raw.githubusercontent.com/creationix/nvm/v0.25.0/install.sh | bash
source ~/.profile
nvm install 8
nvm alias default 8
npm install koa
npm install koa-router
npm install -g pm2
cat << EOF >> /home/ubuntu/app.js
const koa = require('koa');
const Router = require('koa-router');
const app = new koa();
const router = Router();
router.get('/',async (ctx) => {
  console.log('apple');
  ctx.body = 'apple';
});
app.use(router.routes());
app.listen(3000);
EOF
pm2 start /home/ubuntu/app.js