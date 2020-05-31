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
  //res.render('index', { title: 'Express' });
  //res.send(req.body)
});

// router.get('/eventRcv', function (req, res, next) {
//   res.send(global.cache_data);
// });

// router.get('/eventRcv', function (req, res, next) {

//   res.send(req.body);
//   // console.log(req.body);

//   // request.get('/eventRcv',req.body)
//   // res.sendStatus(200);
//   //res.render('index', { title: 'Express' });
//   //res.send(req.body)
// });


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

router.get('/api/v1/recognition/check', function (req, res, next) {


  // 将sign, timestamp, app_key三个参数连同业务参数一起提交给服务器，例如：
  // http://host:port/service/request.do?company_id=1&parent_id=3&app_key=35uifanj8i30kdng&timestamp=1477881215000&sign=e5ef72ef839bdf5397b4906b199b9fbf
  // 其中company_id, parent_id为业务参数,服务器对比当前的时间戳和客户端请求中的timestamp，相差若大于30分钟则返回失败。

  //https://HOST:PORT/api/v1/recognition/check


  var options = {
    url: "http://127.0.0.1:3001/testpost",
    qs: {//query
      //id: '20190929T060801Z'
    },
    headers: {
      // device: "asdfasdfaadfasdf"
    },//req.headers
    form: {// form-data
      face_avatar: '???',
      app_key: getAppKey(),
      sign: getSign(),
      timestamp: getTimestamp()
    }  //req.body
    // body: filedata   // bin data
  };

  request.post(options, function (error, response, body) {

    console.info('response:' + JSON.stringify(response));
    //console.info("statusCode:" + response.statusCode)
    //console.info('body: ' + body);
  });
  res.send(200);
});





router.get('/testfile', function (req, res, next) {

  var options = {
    url: 'http://127.0.0.1:3000/testpost',
    formData: {
      face_avatar: '???',
      app_key: getAppKey(),
      sign: getSign(),
      timestamp: getTimestamp()
    }
  }

  // var url = 'http://192.168.0.102:3000/addpic'
  // var formData = {
  //   // Pass a simple key-value pair
  //   my_field: 'my_value',
  //   // Pass data via Buffers
  //   my_buffer: new Buffer([1, 2, 3]),
  //   // Pass data via Streams
  //   my_file: fs.createReadStream(__dirname + '/unicycle.jpg'),
  // };
  request.post(options, function (error, response, body) {
    if (!error && response.statusCode == 200) {
    }
  });
  return;
});

router.post('/testpost', function (req, res, next) {
  //console.log(req.body);
  res.render('index', { title: 'Express' });
});

router.post('/addpic', filemulter.any(), function (req, res) {

  if (req.files.length != 0) {

    var oname = req.files[0].originalname.split('.');
    //获取上传文件后缀
    var suffix = oname.length > 0 ? oname[oname.length - 1] : '';
    if (suffix != 'png' && suffix != 'jpg' && suffix != 'gif' && suffix != 'jpeg') {
      fs.unlinkSync(req.files[0].path);
      return res.redirect('/addevent');
    }

    //设置文件大小限制
    if (req.files[0].size > global.filelimit * 1024 * 1024) {
      fs.unlinkSync(req.files[0].path);
      return res.redirect('/addevent');
    }

    var des_file = 'public/images/' + req.files[0].filename +
      (suffix == '' ? '' : ('.' + suffix));

    photofile = '/event_photo/' + req.files[0].filename +
      (suffix == '' ? '' : ('.' + suffix));;

    //通过rename 进行move
    fs.renameSync(req.files[0].path, des_file);
  }
});

module.exports = router;





  // var options = {
  //   url: 'http://www.baidu.com'
  //   // url: 'https://api.some-server.com/',
  //   // agentOptions: {
  //   //     cert: fs.readFileSync(certFile),
  //   //     key: fs.readFileSync(keyFile),
  //   //     passphrase: 'password',
  //   //     securityOptions: 'SSL_OP_NO_SSLv3'
  //   // }
  // };

  // request.get(options, function (err, response, body) {
  //   console.info(response.body);
  // });
