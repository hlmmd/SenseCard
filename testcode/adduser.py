import requests
import time
import hashlib
import os.path


users=[]


#输入你的app_key
app_key = "e86b7b728466b964"
#输入你的app_secret
app_secret = "337649c8bf8822ae32ece7f69e27f6f8"

#输入你要使用的api的uri,此处是检测图片人脸个数的uri
uri = "/api/v1/user"


def getTimestamp():
    return str(round(time.time()) * 1000)

def getSign(timestamp):
    hl = hashlib.md5()
    hl.update((timestamp + '#' +app_secret).encode(encoding='utf-8'))
    return hl.hexdigest()


if __name__ == '__main__':

    with open('out.txt', encoding='utf-8') as file:
        lines = file.read().split('\n')

        for row, line in enumerate(lines):
            if len(line)==0 or  line[0]=='#':
                continue
            cols = line.split(',')
            user = []
            for j,col in enumerate(cols):
                user.append(col)
            users.append(user)

    for user in users:
        timestamp = getTimestamp()
        sign = getSign(timestamp)
        path = "C:\\Users\\qinrui\\Desktop\\jpg\\" +user[2]+ ".jpg"
        url = "http://10.10.175.109/" + uri
        data = {
            "remark":"",
            "mobile":"12345678901",
            "groups":"",
            "icNumber":user[3],
            "jobNumber":user[2],
            "name":user[1],
            #"departmentId":user[4],
            "position":user[5],
            "gender":user[6],
            "app_key": app_key,
            "sign": sign,
            "timestamp": timestamp
        }
        if os.path.exists(path)==True:
            files = {
                "avatarFile": (str.split(path, "/")[-1], open(path, "rb"), "image/jpeg")
            }
            result = requests.post(url, data=data, files=files)
        else:
            result = requests.post(url, data=data)
        print(result.text)
        result.close()
        exit(0)