import requests
a = {"mobilephone":"18611000001","pwd":"xxxxxxxxxxxx"}
url = "http://120.27.249.122:3001/eventRcv"
#消息头指定
headers = {'Content-Type': 'application/json;charset=UTF-8'}
#发送post请求 json参数直接为一个字典数据。
res = requests.request("post",url,json=a,headers=headers)
print(res.status_code)
print(res.text)