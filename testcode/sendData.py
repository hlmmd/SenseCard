import requests
a = {"mobilephone":"18611000001","pwd":"xxxxxxxxxxxx"}
url = "http://127.0.0.1:5000/eventRcv"
#消息头指定
headers = {'Content-Type': 'application/json;charset=UTF-8'}
#发送post请求 json参数直接为一个字典数据。

try:
    res = requests.request("post",url,json=a,headers=headers,timeout = 1)
    print(res.status_code)
    print(res.text)
except Exception:
    print('响应超时')
