import base64
import hashlib
import hmac
import json
import requests
import socket
import re
#from time import strptime, mktime, timezone, time, gmtime, strftime, daylight
import time
import binascii

class AAHWebService(object):
    def __init__(self, baseUrl, username, password, debug_level=0):
        # Use SSL if baseUrl starts with 'https://'.
        # Split the rest of baseURL at the first '/' into host and basePath.
        m = re.match('(https?)://(.+?)(/.*)', baseUrl)
        self._baseUrl = baseUrl
        self._use_ssl = (m.group(1) == 'https')
        self._host = m.group(2)
        self._basepath = m.group(3)
        self._credentials = {'username': username, 'password': password}
        self._debug_level = debug_level
        self._session = {}
        self._time_skew = 0

    def send_request(self, method, url, body=None):
        # Send the request at most 2 times:
        # The first request may hit an expired session ,
        # the second request is successful or has a permanent error.
        for _ in range(2):
            try:
                # If we are already logged in, send the request. Otherwise ,
                # create the session and then send the request in the next
                # loop iteration.
                if 'accessKey' in self._session:
                    (status,text) = self._send_single_request(method,url,body)
                    request_was_sent = True
                else:
                    (status,text)= self._create_session()
                    request_was_sent = False                   
                if status == 401 and text['code'] == 40103:
                    del self._session['accessKey']
                elif request_was_sent:
                    return  (status,text)
            except (IOError, ValueError) as e:
                return (500,{'message':str(e) . decode('utf -8')})
        return  (status,text)

    def _create_session(self):

        (status,text) = self._send_single_request("POST",'/sessions',self._credentials,sign = False)
        if status == 201:
            self._session = text
        return  (status,text)

    def _send_single_request(self, method, cmd, body, sign=True):
        uri = self._basepath + cmd
        headers = {}
        if body:
            # Encode request body as JSON
            body = json.dumps(body)
            headers['Content-Type'] = 'application/json;charset=utf-8'
            # Compute MD5 digest
            h = hashlib.new('md5')
            h.update(body.encode("utf8"))
            headers['Content-MD5'] = base64.b64encode(h.digest()).decode()

        format_date = time.strftime(
            # "%a, %d-%b-%y %H:%M:%S +0800", time.localtime(time.time()))
            "%a, %d %b %Y %H:%M:%S +0800", time.localtime(time.time()))
        
        #headers['Date'] = 'Thu, 28 May 2020 23:22:34 +0800' #format_date
        headers['Date'] = format_date
    
        if sign ==True and 'id' in self._session:
            
            (canonicalized_resource, q, query_string) = uri . partition('?')
            canonicalized_resource += q + \
                '&' . join(sorted(query_string . split('&')))
            print(canonicalized_resource)

            # Build the string to be signed
            string_to_sign = method+"\n"
            if 'Content-MD5' in headers:
                string_to_sign += str( headers['Content-MD5'] )
            string_to_sign += "\n"
            if 'Content-Type' in headers:
                string_to_sign += headers['Content-Type']
            string_to_sign += "\n" + headers['Date'] + "\n"+canonicalized_resource
            # Create the signature
            h = hmac.new(self._session['accessKey'].encode('utf-8'),string_to_sign.encode('utf-8'), hashlib.sha1)           
            headers['Authorization'] = 'AWS %s:%s' % (
                self._session['id'], base64.b64encode(h.digest()).decode())
        
        url  = self._baseUrl+ cmd
        # print(headers)
        # print(url)
        # exit(0)
        try:
            timeout_time = 3
            if method == "GET":
                result = requests.get(url,verify = False,timeout = timeout_time)
            elif method =="POST":
                result = requests.post(url, headers=headers, data=body, verify=False,timeout = timeout_time)
        except Exception:
            print('server timeout')  
            return (404,'connect error'  )
        if self._debug_level:
            print("reply body:"+result.text)
        return (result.status_code,result.text)


# if __name__ == "__main__":
#     ws = AAHWebService('https://10.10.175.108:443/api/v1',
#                        'sym', 'sym', 1)
#     (status,text) = ws.send_request("POST","/doors/101?timeout=30",{'open':True})
#     print(text)
