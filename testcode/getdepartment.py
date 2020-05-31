import requests
import time
import hashlib
import os.path

#输入你的app_key
app_key = "e86b7b728466b964"
#输入你的app_secret
app_secret = "337649c8bf8822ae32ece7f69e27f6f8"


def getTimestamp():
    return str(round(time.time()) * 1000)

def getSign(timestamp):
    hl = hashlib.md5()
    hl.update((timestamp + '#' +app_secret).encode(encoding='utf-8'))
    return hl.hexdigest()


#输入你要使用的api的uri,此处是检测图片人脸个数的uri
uri = "/api/v1/user"

timestamp = getTimestamp()
sign = getSign(timestamp)
url = "http://10.10.175.109/" + uri
data = {
    "app_key": app_key,
    "sign": sign,
    "timestamp": timestamp
}
result = requests.get(url, params= data)
print(result.text)
exit(0)
