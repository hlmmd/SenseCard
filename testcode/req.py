import requests
import time
import hashlib
import os.path

host_url = "http://10.10.175.109/"

# 输入你的app_key
app_key = "e86b7b728466b964"
# 输入你的app_secret
app_secret = "337649c8bf8822ae32ece7f69e27f6f8"

users = []


def getTimestamp():
    return str(round(time.time()) * 1000)


def getSign(timestamp):
    hl = hashlib.md5()
    hl.update((timestamp + '#' + app_secret).encode(encoding='utf-8'))
    return hl.hexdigest()


def GetType(typecode):

    type = {
        '01': '本科生',
        '02': '编制类人员',
        '03': '协作单位人员',
        '04': '研究生',
        '05': '其他学校聘用人员',
        '06': '专职科研人员',
        '07': '继续教育',
        '08': '进修生',
        '09': '网络教育',
        '10': '校外交流生',
        '11': '协作单位',
        '12': '校外国内交流生',
        '13': '本科生临时卡',
        '14': '其它正式卡',
        '15': '其它类教师',
        '16': '非餐饮人员',
        '17': '联合大学',
        '18': '单位卡',
        '19': '短期学习人员',
        '20': '校内聘用人员',
        '21': '非编制附属医院人员',
        '22': '派遣人员',
        '23': '兼任教师',
        '24': '柔性引进人员',
        '25': '附属医院人员',
        '26': '其他学校聘用人员',
        '27': '高等研究院人员',
        '28': '博士后人员',
        '29': '校外兼职人员',
        '30': '访问学者',
        '31': '校友',
        '32': '校外挂职人员'
    }

    if typecode in type:
        return type[typecode]
    else:
        return "未知"


def ReadUserData():
    with open('out.txt', encoding='utf-8') as file:
        lines = file.read().split('\n')
        for line in lines:
            if len(line) == 0 or line[0] == '#':
                continue
            cols = line.split(',')
            user = []
            for col in cols:
                user.append(col)
            users.append(user)


def getDepartment():
    uri = "/api/v2/department"
    timestamp = getTimestamp()
    sign = getSign(timestamp)
    url = "http://10.10.175.109/" + uri
    data = {
        "app_key": app_key,
        "sign": sign,
        "timestamp": timestamp
    }
    result = requests.get(url, params=data)
    print(result.text)


def getUser():
    uri = "/api/v1/user"
    timestamp = getTimestamp()
    sign = getSign(timestamp)
    url = "http://10.10.175.109/" + uri
    data = {
        "app_key": app_key,
        "sign": sign,
        "timestamp": timestamp
    }
    result = requests.get(url, params=data)
    print(result.text)


def deleteUser(id):
    uri = "api/v1/user/delete/"
    timestamp = getTimestamp()
    sign = getSign(timestamp)
    url = "http://10.10.175.109/" + uri + '/'+str(id)
    data = {
        "id": str(id),
        "app_key": app_key,
        "sign": sign,
        "timestamp": timestamp
    }
    result = requests.get(url, params=data)
    print(result.text)


def addAllUser():
    uri = "/api/v1/user"
    #flag = False
    for user in users:

        # if(user[2] == '07048'):
        #     flag = True
        # if flag == False:
        #     continue

        if int (user[6]) == 2:
            user[6] = 1
        else:
            user[6] = 2

       
        timestamp = getTimestamp()
        sign = getSign(timestamp)
        path = "C:\\Users\\qinrui\\Desktop\\jpg\\" + user[2] + ".jpg"
        url = "http://10.10.175.109/" + uri
        data = {
            "remark": "",
            "mobile": "",
            "groups": "",
            "icNumber": user[3],
            "jobNumber": user[2],
            "name": user[1],
            "departmentId": 5,
            "position":  GetType(user[5]),
            "gender": user[6],
            "app_key": app_key,
            "sign": sign,
            "timestamp": timestamp
        }
        if os.path.exists(path) == True:
            ff =  open(path, "rb")
            files = {
                "avatarFile": (str.split(path, "/")[-1], ff, "image/jpeg")
            }
            result = requests.post(url, data=data, files=files)
            ff.close()
            while   result.status_code ==  500:
                time.sleep(1)
                ff =  open(path, "rb")
                files = {
                    "avatarFile": (str.split(path, "/")[-1], ff, "image/jpeg")
                }
                result = requests.post(url, data=data, files=files)
                ff.close()
        else:
            continue
            result = requests.post(url, data=data)
            while   result.status_code ==  500:
                time.sleep(1)
                result = requests.post(url, data=data)

        print(result.text)
        result.close()
        #exit(0)


if __name__ == '__main__':

   
    #for id in range(18371,18372):
    #    deleteUser(id)

    # getDepartment()
    #getUser()
    ReadUserData()
    addAllUser()
    # print(GetType("33"))
