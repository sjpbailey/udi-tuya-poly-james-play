import requests
import time
import hmac
import hashlib
import json
import pprint
import logging
import tinytuya

new_sign_algorithm = True
token = None
headers = None
body = None
apiRegion = "us"
apiKey = "txejpdfda9iwmn5cg2es"
apiSecret = "46d6072ffd724e0ba5ebeb5cc6b9dce9"
uri = "token?grant_type = 1"


url = "https://openapi.tuya%s.com/v1.0/%s" % (apiRegion, uri)
now = int(time.time()*1000)
headers = dict(list(headers.items(
)) + [('Signature-Headers', ":".join(headers.keys()))]) if headers else {}
if (token == None):
    payload = apiKey + str(now)
    headers['secret'] = apiSecret
else:
    payload = apiKey + token + str(now)

# If running the post 6-30-2021 signing algorithm update the payload to include it's data
if new_sign_algorithm:
    payload += ('GET\n' +                                                                # HTTPMethod
                # Content-SHA256
                hashlib.sha256(bytes((body or "").encode('utf-8'))).hexdigest() + '\n' +
                ''.join(['%s:%s\n' % (key, headers[key])                                   # Headers
                        for key in headers.get("Signature-Headers", "").split(":")
                        if key in headers]) + '\n' +
                '/' + url.split('//', 1)[-1].split('/', 1)[-1])
# Sign Payload
signature = hmac.new(
    apiSecret.encode('utf-8'),
    msg=payload.encode('utf-8'),
    digestmod=hashlib.sha256
).hexdigest().upper()

# Create Header Data
headers['client_id'] = apiKey
headers['sign'] = signature
headers['t'] = str(now)
headers['sign_method'] = 'HMAC-SHA256'

if (token != None):
    headers['access_token'] = token

# Get Token
response = requests.get(url, headers=headers)
print(response)
try:
    response_dict = json.loads(response.content.decode())
except:
    try:
        response_dict = json.loads(response.content)
        print(response_dict)
    except:
        print("Failed to get valid JSON response")

    print(response_dict)
