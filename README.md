# SenseCard客户端使用说明

version:0.1

## 操作说明

需要将config.json配置文件与exe文件置于同一目录

生成的日志在logging.txt中

* 如果收到的deviceName不在配置中，记录该deviceName
* 正常接受消息，记录data，以及对应的doorId(最后一项)
* 其他消息均忽略

说明：

* ServerIp：WebServer IP地址，一般为本机IP
* ServerPort:WebServer 端口
* Dest URL：Vingcard服务器的URL
* 用户名：Vingcard服务器 用户名
* 密码：Vingcard服务器 密码
* 配置：SenseLink消息推送中deviceName到VingCard doorId的映射。在最后一行可以新增配置，将某一行清空可删除对应配置（均需保存）
* 保存：保存配置更改，写入config.json
* 开启服务器：开启WebServer，接收消息推送，此时配置不可保存更改
* 关闭服务器：关闭WebServer。

## 编译说明

操作系统：windows10

语言：python3

主要python依赖项：

* pyqt5
* pyinstaller
* requests
* flask 
* ……

```bash
pip install flask pyqt5 requests pyinstaller
```

文件内容说明

* flaskWebServer.py:基于flask的web server
* sensecard.py:主程序
* vingcard.py：向vingcard服务器发送命令开锁
* sendData.py：用于测试，模拟senselink平台发送的信息
* config.json:配置文件
* senseui.ui:基于qt Desinger创建的GUI文件

```bash
#将.ui文件转化为.py文件
python -m PyQt5.uic.pyuic  senseui.ui -o senseui.py

#编译生成exe文件,使用pyinstaller
pyinstaller -F -w sensecard.py
```