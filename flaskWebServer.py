from flask import Flask
from flask import request
from multiprocessing import Process
import logging
import time
import inspect
import ctypes
import threading

from vingcard import *


def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)


class WebServer(object):
    def __init__(self, host="127.0.0.1", port=4000):
        self.app = Flask('SenseCard')
        self._data = {}
        self._host = host
        self._port = port

        @self.app.route('/eventRcv', methods=['POST'])
        def eventRcv():
            # only handle json
            if request.is_json:
                if 'data' in request.json and 'deviceName' in request.json['data']:
                    self._data = request.json
                    data = request.json['data']
                    deviceName = data['deviceName']                    
                    rules = self._config['rules']
                    if deviceName != '' and deviceName in rules:
                        doorId = rules[deviceName]
                        ws = AAHWebService(
                            self._config['url'], self._config['username'], self._config['password'], 1)

                        uri = "/doors/" + str(doorId)+"?timeout=30"
                        ws.send_request("POST", uri, {'open': True})
                        #(status,text) = ws.send_request("POST","/doors/101?timeout=30",{'open':True})                        
                        data['doorId'] = doorId
                        logging.info(data)
                    else:
                        logging.error('Unknown deviceName: '+deviceName)

            return ''

        @self.app.route('/', methods=['GET'])
        def home():
            return self._data

        logging.basicConfig(
            filename="logging.txt", format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)
        # ignore flask logging
        logging.getLogger("werkzeug").setLevel(logging.ERROR)
        # self.app.run(port=port)

    def setConfig(self, config):
        self._config = config

    def run(self, host="127.0.0.1", port=4000):
        self.app.run(host=host, port=port)

    def process(self):
        # args是关键字参数，需要加上名字，写成args=(self,)
        self._th1 = threading.Thread(
            target=WebServer.run, args=(self, self._host, self._port))
        self._th1.daemon = True
        self._th1.start()

        # self._th1._stop()
        # th1.join()

    def close(self):
        if self._th1:
            _async_raise(self._th1.ident, SystemExit)


# app = Flask(__name__)

# data = {}

# @app.route('/eventRcv', methods=['POST'])
# def eventRcv():
#     #only handle json
#     if request.is_json:
#         data = request.json
#         logging.info(request.json)
#         print(request.json)
#     return ''

# @app.route('/', methods=['GET'])
# def home():
#     return data

# if __name__ == '__main__':
#     WebServer(4000)
#     exit()
#     logging.basicConfig(filename= "logging.txt" ,format='%(asctime)s - %(levelname)s: %(message)s', level=logging.INFO)
#     #ignore flask logging
#     logging.getLogger("werkzeug").setLevel(logging.ERROR)

#     app.run(port=4000)
