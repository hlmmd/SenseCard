import requests
a = {
    'messageId': '75835750-6dd9-4eed-a929-ba1b4c062405',
    'eventType': 30000,
    'sendTime': 1583726626015,
    'data': { 
        'id': 120260,
        'userId': 30707,
        'name': 'Jeff',
        'type': 1,
        'avatar': '5e65c020f54fd90001fe4a33',
        'direction': 0,
        'verifyScore': 0,
        'receptionUserId': 0,
        'receptionUserName': '',
        'groups': [ { 'id': 1, 'name': '默认组', 'type': 1 } ],
        'deviceName': 'SenseTest2',
        'sn': 'SPS-e33b1811dbd9189c5eeedffd557fd779',
        'signDate': '2020-03-09',
        'signTime': 1583726625,
        'signAvatar': '5e65c021f54fd90001fe4a37',
        'signBgAvatar': '5e65c021f54fd90001fe4a38',
        'companyId': 1,
        'mobile': '18014398265',
        'icNumber': '',
        'idNumber': '',
        'jobNumber': '3867452109',
        'remark': 'welcome',
        'entryMode': 1,
        'signTimeZone': '+08:00',
        'docPhoto': '',
        'latitude': 0,
        'longitude': 0,
        'address': '',
        'location': 'SZ-40F',
        'abnormalType': 40001,
        'userIcNumber': '4751283096',
        'userIdNumber': '1g2qW2hz5OwbudHe5gekKbZtmUt0Xwfy',
        'bodyTemperature': 38,
        'mask': 1
    }
}
#url = "http://127.0.0.1:4000/eventRcv"
url = "http://192.168.1.102:4000/eventRcv"
#消息头指定
headers = {'Content-Type': 'application/json;charset=UTF-8'}
#发送post请求 json参数直接为一个字典数据。

try:
    res = requests.request("post",url,json=a,headers=headers,timeout = 8)
    print(res.status_code)
    print(res.text)
except Exception:
    print('响应超时')
