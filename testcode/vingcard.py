import base64
import hashlib
import hmac
import json
import requests
import socket
import re
import email
#from time import strptime, mktime, timezone, time, gmtime, strftime, daylight
import time
import binascii

host_url = "https://10.10.175.108:443/api/v1"
base_path = "/api/v1"
credentials = {
    'username': 'sym',
    'password': 'sym'
}

debug_level = 0

session = {}

time_skew = 0

def send_single_request(method, url, body=None, sign=True):
    """ Send a properly signed request to the web service."""
    path_url = base_path+url
    url = host_url + url
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
        #"%a, %d-%b-%y %H:%M:%S +0800", time.localtime(time.time()))
        "%a, %d %b %Y %H:%M:%S +0800", time.localtime(time.time()))

    headers['Date'] = 'Thu, 28 May 2020 23:22:34 +0800' #format_date
    if sign == True and 'id' in session:
        print(path_url)
        (canonicalized_resource, q, query_string) = path_url . partition('?')
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


        key = b"CONSUMER_SECRET&TOKEN_SECRET" 


        # The Base String as specified here: 
        raw = b"BASE_STRING" # as specified by OAuth

        hashed = hmac.new(key, raw, hashlib. sha1)
        
        print(hashed.hexdigest())





        print(string_to_sign)
        print(session['accessKey'].encode('utf-8'))
        print( string_to_sign . encode('utf-8'))

        sha1 = hashlib.sha1()
        sha1.update(session['accessKey'].encode('utf-8')+string_to_sign.encode('utf-8'))
        print(sha1.hexdigest())

        h = hmac.new(session['accessKey'].encode('utf-8'),string_to_sign.encode('utf-8'), hashlib.sha1)
        #h = hmac.new( bytes( session['accessKey']),   bytes(string_to_sign), hashlib.sha1)
        print(h.hexdigest())
        #teststr ="GET\n\n\nWed, 16 Jan 2013 15:23:02 +0000\n/api/v1/cards?cardHolder=jdoe&validTime=20130105T1200"
        #h = hmac.new("AQIDBAUGBwg=".encode('utf-8'),teststr.encode('utf-8'), hashlib.sha1)
        
        headers['Authorization'] = 'AWS %s:%s' % (
            session['id'], base64.b64encode(h.digest()).decode()   )
    
    print(headers)
    exit(0)
    if method == "GET":
        result = requests.get(url, verify=False)
    elif method == "POST":
        result = requests.post(url, headers=headers, data=body, verify=False)
    elif method == "PUT":
        result = requests.put(url, headers=headers, data=body, verify=False)

    return result


def create_session():
    """ Send user credentials and record the ID and the access key."""
    uri = '/sessions'
    result = send_single_request("POST", uri, credentials, sign=False)
    print(result.headers)
    print(result.status_code)
    print(result.content)
    return result.text


def send_request_get(url):
    # cached
    if 'accessKey' in session:
        pass



# session = json.loads(create_session())

# print(session)

session = {
  "id" : "d93edb3dc380489495afe8421ffaa310",
  "accessKey" : "84b93884470f4d22870c59e54e33397e"
}


add_user_data = {
    "autoDelete": False,
    "cellPhone": "12345",
    "pin": "1224",
    "confirmPin": "1224",
    "defaultReportTime": "03:00",
    "email": "email@email.com",
    "givenName": "Name",
    "hidden": False,
    "surname": "SurName",
    "userDetails1": "detail1",
    "userDetails2": "detail2",
    "userDetails3": "detail3",
    "userDetails4": "detail4",
    "userGroup": "UserGroup1"
}


res = send_single_request("GET", "/users/jdoe")
print(res.headers)
print(res.text)


# class AAHWebService (object):
#     def __init__(self, baseUrl, username, password, debug_level=0):
#         """Constructor of AAHWebService object"""
#         # Use SSL if baseUrl starts with 'https://'.
#         # Split the rest of baseURL at the first '/' into host and basePath.
#         m = re . match('(https ?)://(.+?)(/.*)', baseUrl)
#         self . _use_ssl = (m . group(1) == 'https')
#         self . _host = m . group(2)
#         self . _basepath = m . group(3)
#         # Store credentials in an object ready to be sent to the server.
#         self . _credentials = {'username': username, 'password': password}
#         self . _debug_level = debug_level  # Get text output from HTTPConnection
#         self . _session = {}  # Placeholder for session ID and access key
#         self . _time_skew = 0  # Assume that server and client times match

#     def send_request(self, method, url, body=None):
#         """Send a request to the web service.
#         Automatically handle session creation and time skew.
#         """
#         # Send the request at most 3 times: The first request may need
#         # a new time skew , the second request may hit an expired session ,
#         # the third request is successful or has a permanent error.
#         for _ in range(3):
#             try:
#                 # If we are already logged in, send the request. Otherwise ,
#                 # create the session and then send the request in the next
#                 # loop iteration.
#                 if 'accessKey' in self . _session:
#                     (status, resource, server_time) = self . _send_single_request(
#                         method, url, body)
#                     request_was_sent = True
#                 else:
#                     (status, resource, server_time) = self . _create_session()
#                     request_was_sent = False
#                     # Handle time skew (40101) and expired session (40103).
#                     # If the request was sent and everything went fine , or if any
#                     # other type of error occurred , we leave that to the caller.
#                 if status == 401 and resource['code'] == 40101:
#                     _ = strptime(server_time, '%a, %d %b %Y %H:%M:%S GMT')
#                     self . _time_skew = mktime(
#                         _)-timezone-time() + daylight * 3600
#                 elif status == 401 and resource['code'] == 40103:
#                     del self . _session['accessKey']
#                 elif request_was_sent:
#                     return (status, resource)
#             except (IOError, ValueError) as e:
#                 # Handle connection refused , nameserver lookup failure ,
#                 # sslv3 alert handshake failure or server response that was
#                 # not in JSON format.
#                 # Set a temporary error code and try again.
#                 (status, resource) = (
#                     500, {'message': str(e) . decode('utf -8')})
#                 if self . _debug_level:
#                     print('error: %s' % resource['message'])
#             # If the server still returns an error after 3 attempts , nothing
#             # else can be done except for returning the error to the caller.
#         return (status, resource)

#     def _create_session(self):
#         """ Send user credentials and record the ID and the access key."""
#         (status, resource, server_time) =\
#             self . _send_single_request('POST', '/sessions',
#                                         self . _credentials, False)
#         if status == 201:
#             self . _session = resource  # Success! Store ID and key.
#         return (status, resource, server_time)

#     def _send_single_request(self, method, url, body, sign=True):
#         """ Send a properly signed request to the web service."""
#         url = self . _basepath+url
#         headers = {}
#         if body:
#             # Encode request body as JSON
#             body = json . dumps(body)
#             headers['Content-Type'] = 'application/json;charset = utf - 8'
#             # Compute MD5 digest
#             h = hashlib . new('md5')
#             h . update(body)
#             headers['Content-MD5'] = base64 . b64encode(h . digest())

#         # Format the date correctly , after applying the client/server skew headers [ ’Date’ ]= email . Utils . formatdate ( time ( ) + self . _time_skew )
#         if sign and 'id' in self . _session:
#             # Canonicalize the URL
#             (canonicalized_resource, q, query_string) = url . partition('?')
#             canonicalized_resource += q + \
#                 '&' . join(sorted(query_string . split('&')))
#             # Build the string to be signed
#             string_to_sign = method+"\n"
#             if 'Content-MD5' in headers:
#                 string_to_sign += headers['Content-MD5']
#             string_to_sign += "\n"
#             if 'Content-Type' in headers:
#                 string_to_sign += headers['Content-Type']
#             string_to_sign += "\n" + \
#                 headers['Date'] + "\n"+canonicalized_resource
#             # Create the signature
#             h = hmac . new(self . _session['accessKey'] . encode(
#                 'utf-8'),  string_to_sign . encode('utf-8'), hashlib . sha1)
#             headers['Authorization'] = 'AWS % s: % s' % (
#                 self . _session['id'], base64 . b64encode(h . digest()))

#         # Communicate with server
#         if self . _use_ssl:
#             conn = httplib . HTTPSConnection(self . _host)
#         else:
#             conn = httplib . HTTPConnection(self . _host)
#         conn . set_debuglevel(self . _debug_level)
#         conn . request(method, url, body, headers)
#         response_obj = conn . getresponse()
#         # Interpret response
#         server_time = response_obj . getheader('Date')
#         response_body = response_obj . read()
#         if self . _debug_level:
#             print("reply body: "+response_body)
#         try:
#             resource = json . loads(response_body)
#         except ValueError as e:
#             resource = {'message': e . message +
#                         "\nServer response :\n"+response_body}
#         return (response_obj . status, resource, server_time)


# # Example of how the AAHWebService class can be used
# if __name__ == "__main__":
#     ws = AAHWebService('https://dc.example.com:443/api/v1',
#                        'cardAdministrator01', 'secret', 1)
#     (status, resource) = ws . send_request("GET", "/users/jdoe")
#     print(json . dumps(resource, indent=4, sort_keys=True))
#     assert (status == 200)
#     (status, resource) = ws . send_request(
#         "POST", "/users/jdoe", {'givenName': 'Jane'})
#     print(json . dumps(resource, indent=4, sort_keys=True))
#     assert (status == 200)
