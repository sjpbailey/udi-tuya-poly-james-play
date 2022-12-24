import asyncio
import json
import pandas as pd
import numpy as np
import tinytuya
import requests
import time
import hmac
import hashlib


jsondata = [{"name": "LED Office", "id": "ebfc16d57ed374932cjqfk", "key": "805217605357161b", 'dps': {'20': False, '21': 'white', '22': 10, '23': 1000,
                                                                                                      '24': '009d03c603a1', '25': '020d0d00000000000000001903e8', '26': 0}}]

"""jsondata = [
    {
        "name": "Switch Dutch Door",
        "id": "eb9f1eaef823420e19bewt",
        "key": "659ef2b2c7d3a60a"
    },
    {
        "name": "Switch Master Outside",
        "id": "017743508caab5f126b0",
        "key": "17a1e4c963773637"
    },
    {
        "name": "Switch Garden Outside",
        "id": "017743508caab5f385a7",
        "key": "2bc2d5aef80f3aee"
    },
    {
        "name": "Switch Garage Overhead",
        "id": "eb7ac0fbe689ca95f7dxxk",
        "key": "449ebc60812eb8bb"
    },
    {
        "name": "Switch Side Garage Outside",
        "id": "eb577fdd6642efcbc3g0qc",
        "key": "85861de497baa60d"
    },
    {
        "name": "LED Strip Cabinets",
        "id": "ebe097c0407da32084kvtr",
        "key": "22ad5946c44356a4"
    },
    {
        "name": "Switch Office Outside Lights",
        "id": "017743508caab5f0973e",
        "key": "e779c96c964f71b2"
    },
    {
        "name": "Switch Front Door",
        "id": "eb7053a032f633f952bqq2",
        "key": "a792deae091dff2c"
    },
    {
        "name": "Switch Dining Pool Outside",
        "id": "017743508caab5f29984",
        "key": "be9d5b1387e6f231"
    },
    {
        "name": "LED Garage",
        "id": "ebfd4f4263bb769d99zjkq",
        "key": "ec0b2b581a246eab"
    },
    {
        "name": "LED Office",
        "id": "ebfc16d57ed374932cjqfk",
        "key": "805217605357161b"
    },
    {
        "name": "Motion Front Door",
        "id": "eb6f0f8c067d064a64word",
        "key": "ad62e302f4b5315d"
    }
]"""


"""async def main():
    devices_list = json.dumps(jsondata)
    # print(devices_list)
    scan_results = tinytuya.deviceScan(False, 30)
    for value in scan_results.values():
        # await asyncio.sleep(5)
        device_id = value['gwId']
        # await asyncio.sleep(5)
        ip = value['ip']
        await asyncio.sleep(5)
        key = value['key']

        print(device_id)
        print(ip)
        print(key)

        if len(device_id) > 10:
            device_id = device_id  # [:10]
            await asyncio.sleep(3)
            print(device_id)
            print(ip)
            print(key)
            await asyncio.sleep(3)
        tuya_device = tinytuya.BulbDevice('dev_id', 'address')
        # tuya_device = tinytuya.OutletDevice(
        #    value['gwId'], value['ip'], value['key'])
        # tuya_device.set_version(3.3)
        node_Switch_status = tuya_device.status()
        print(node_Switch_status)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
devices_list = [json.dumps(jsondata)]
print(devices_list)
print(type(devices_list))
scan_results = tinytuya.deviceScan()
for value in scan_results.values():
    ip = value['ip']
    device_id = value['gwId']
    #key = value['key']
    # print(key)

    if len(device_id) > 10:
        device_id = device_id  # [:10]
        print(device_id)
    if len(ip) > 10:
        ip = ip  # [:10]
        print(ip)
    if len(key) > 10:
        ip = key  # [:10]
        print(key)
    tuya_device = tinytuya.OutletDevice(
        value['gwId'], value['ip'])  # , value['key']"""

#LOGGER.info(f"Device Scan Device IP: {ip}")
# for dict_found in [x for x in devices_list if x["id"] == value['gwId']]:
#    value['name'] = dict_found['name']
#    value['key'] = dict_found['key']
#    device_node = (device_id)
#    print(f"device_node: {device_node}")
#    if device_node is None:
#        print(f"Adding Node: {device_id} - {dict_found['name']}")
#        print("Node Name {}".format(value['name']))
#        print("Node key {}".format(value['key']))
#        print("Node id {}".format(value['gwId']))
#        print("Node ip {}".format(value['ip']))
#        time.sleep(3)
#        tuya_device = tinytuya.BulbDevice(
#            value['gwId'], value['ip'], value['key'])
#        node_status = tuya_device.status()
#        print(node_status)
#        print("Node Status {}".format(str(node_status)))
#        # print(node_status)
#        tuya_device.set_version(3.3)


def tuyaPlatform(apiRegion, apiKey, apiSecret, uri, token=None, new_sign_algorithm=True, body=None, headers=None):
    ###### Authentacation ######
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
    print(f"LINE 58 Token: {response}")
    try:
        response_dict = json.loads(response.content.decode())
    except:
        try:
            response_dict = json.dumps(response.content)
            print(response_dict)
        except:
            print("Failed to get valid JSON response")
    # return (response_dict)

    print(response_dict)


# Custom Parameters Credentials
###### TO TEST ADD YOUR CREDNTIALS HERE ######
config = {}
config['apiKey'] = 'txejpdfda9iwmn5cg2es'
config['apiSecret'] = '46d6072ffd724e0ba5ebeb5cc6b9dce9'
config['apiRegion'] = 'us'
config['apiDeviceID'] = 'ebfc16d57ed374932cjqfk'
needconfigs = False
if config['apiKey'] == '':
    print('PLEASE ADD YOUR CREDENTIALS')
# First Message
print('LINE 81 TinyTuya Device Appender ' + ' [%s]' % (tinytuya.version))
print('')
