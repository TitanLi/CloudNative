const koa = require('koa');
const Router = require('koa-router');
const dotenv = require('dotenv').load();
const nodemailer = require('nodemailer');

const app = new koa();
const router = Router();

//建立郵件客戶端
//允許低安全性應用程式：已開啟
var transporter = nodemailer.createTransport({
    //使用Gmail郵件伺服器
    service:'Gmail',
    auth:{
      user : process.env.from_user_name,
      pass : process.env.from_user_password
    }
  });
  
  var mailOptions = {
    //寄件者
    from : process.env.from_user_name,
    //收件者
    to : process.env.to_user,
    //主旨
    subject : 'apple',
    //內文
    text : 'Titan',
    //Html內文
    html : ''
  };  

//http://127.0.0.1:3001/?message=123456
router.get('/success',async (ctx) => {
    console.log(ctx.query.message);
    mailOptions.html = `<b>Send message from Mistral <br> ${ctx.query.message}</br>`;
    //傳送郵件
    transporter.sendMail(mailOptions,function(error,info){
        if(error){
            console.log(error);
        }else{
            console.log('Message sent : ' + info.response);
        }
    });
    ctx.body = 'ok';
})

router.get('/fail',async (ctx) => {
    console.log(ctx.query.message);
    mailOptions.html = `<b>Send message from Mistral <br> ${ctx.query.message}</br>`;
    //傳送郵件
    transporter.sendMail(mailOptions,function(error,info){
        if(error){
            console.log(error);
        }else{
            console.log('Message sent : ' + info.response);
        }
    });
    ctx.body = 'ok';
})

app.use(router.routes());
app.listen(3001,()  => {
    console.log('App now running on port 3001')
});