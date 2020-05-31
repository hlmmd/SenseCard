var express = require('express');
var router = express.Router();
var crypto = require('crypto');

var request = require("request");

var http = require('http');
//上传文件使用
var multer = require('multer');
//上传的文件放在临时文件夹中
var filemulter = multer({ dest: './public/tmp/' });

global.cache_data;

global.app_secret = 'xxxxxxx';
global.app_key = 'keykey';


function getTimestamp() {
  return Date.now();
}

function getAppSecret() {
  return global.app_secret;
}

function getAppKey() {
  return global.app_key;
}

// 计算方法：sign=md5(timestamp#app_secret)，例如：
// app_secret=2323dsfadfewrasa3434
// timestamp=1477881215000
// sign=md5(1477881215000#2323dsfadfewrasa3434)=e5ef72ef839bdf5397b4906b199b9fbf
function getSign() {
  str = getTimestamp() + '#' + getAppSecret();
  var md5 = crypto.createHash('md5');
  return md5.update(str).digest('hex');
}

/* GET home page. */
router.get('/', function (req, res, next) {
  if (global.cache_data == undefined)
    res.send("no data");
  else
    res.send(global.cache_data);
});

router.get('/reset', function (req, res, next) {
  global.cache_data = undefined
  res.send("reset ok ");
});


router.post('/eventRcv', function (req, res, next) {
  console.log(req.body);
  global.cache_data = req.body;
  res.sendStatus(200);
});

//send by json sample
router.get('/testsend', function (req, res, next) {

  //var url = 'http://120.27.249.122:3001/eventRcv';
  var url = 'http://127.0.0.1:3001/eventRcv'
  request.post(url, {
    json: {
      todo: 'Buy the milk'
    }
  }, (error, res, body) => {
    if (error) {
      console.error(error)
      return
    }
    console.log(`statusCode: ${res.statusCode}`)
    console.log(body)
  })

  res.sendStatus(200);
});


module.exports = router;
