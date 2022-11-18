import requests
import time
import hmac
import hashlib
import json
import pprint
import logging
import tinytuya
import pandas as pd
import numpy as np


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
    #print(f"LINE 48 Token: {response}")
    try:
        response_dict = json.loads(response.content.decode())
    except:
        try:
            response_dict = json.dumps(response.content)
            print(response_dict)
        except:
            print("Failed to get valid JSON response")
    return (response_dict)


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
print('LINE 71 TinyTuya Device Appender ' + ' [%s]' % (tinytuya.version))
print('')

if (config['apiKey'] != '' and config['apiSecret'] != '' and
        config['apiRegion'] != '' and config['apiDeviceID'] != ''):
    needconfigs = False
    # Second Message
    print("    " + "LINE 78 Existing settings:" + "\nAPI Key=%s \nSecret=%s\nDeviceID=%s\n Region=%s" %
          (config['apiKey'], config['apiSecret'], config['apiDeviceID'], config['apiRegion']))
    # Append Config
    json_object = json.dumps(config, indent=4)
    # print(json_object)

    KEY = config['apiKey']
    SECRET = config['apiSecret']
    DEVICEID = config['apiDeviceID']
    REGION = config['apiRegion']
    LANG = 'en'             # us, eu, cn, in
    # en or zh

    # Get Oauth Token from tuyaPlatform
    uri = 'token?grant_type=1'
    response_dict = tuyaPlatform(REGION, KEY, SECRET, uri)
    print(f"LINE 94 RESPONSE DICT ACCESS TOKEN : {response_dict}")
    if not response_dict['success']:
        print('\n\n' 'Error from Tuya server: ' + response_dict['msg'])
        pass
    token = response_dict['result']['access_token']

    # Get UID from sample Device ID
    uri = 'devices/%s' % DEVICEID
    response_dict = tuyaPlatform(REGION, KEY, SECRET, uri, token)

    if not response_dict['success']:
        print('\n\n' + 'Error from Tuya server: ' + response_dict['msg'])
        pass
    uid = response_dict['result']['uid']

    # Use UID to get list of all Devices for User
    uri = 'users/%s/devices' % uid
    json_data = tuyaPlatform(REGION, KEY, SECRET, uri, token)

    # Here internet IP address everything
    output = json.dumps(json_data, indent=4)
    #print(f"\nLINE 115 Future Cloud Control json: {output}\n")

    # Filter to only Name, ID and Key
    tuyadevices = []
    for i in json_data['result']:
        item = {}
        item['name'] = i['name'].strip()
        item['id'] = i['id']
        item['key'] = i['local_key']
        tuyadevices.append(item)

    # Display device list
    output = json.dumps(tuyadevices, indent=4)  # sort_keys=True')
    #print("\n\n" + "LINE 128 Device Listing\n")
    print(output)

    # Scan network for devices and provide polling data
    #print("\nLINE 132 Scanning local network for Tuya devices...")
    devices = tinytuya.deviceScan(False, 20)

    def getIP(d, gwid):
        for ip in d:
            if 'gwId' in d[ip]:
                if (gwid == d[ip]['gwId']):
                    return (ip, d[ip]['version'])
        return (0, 0)

    polling = []
    print("LINE 143 Polling local devices...")
    for i in tuyadevices:
        item = {}
        name = i['name']
        (ip, ver) = getIP(devices, i['id'])
        item['name'] = name
        item['ip'] = ip
        item['ver'] = ver
        item['id'] = i['id']
        item['key'] = i['key']
        if (ip == 0):
            pass
        else:
            try:
                d = tinytuya.OutletDevice(i['id'], ip, i['key'])
                if ver == "3.3":
                    d.set_version(3.3)
                data = d.status()
                if 'dps' in data:
                    item['dps'] = data
                    state = "Off"
                    try:
                        if '1' in data['dps'] or '20' in data['dps']:
                            if '1' in data['dps']:
                                if data['dps']['1'] == True:
                                    state = "On"
                            if '20' in data['dps']:
                                if data['dps']['20'] == True:
                                    state = "On"
                            # print("    %s[%s] - %s%s - %s - DPS: %r" %
                            #     (name, ip, state, data['dps']))
                        else:
                            # print("    %s[%s] - %s%s - DPS: %r" %
                            #      (name, ip, data['dps']))
                            pass
                    except:
                        # print("    %s[%s] - %s%s - %sNo Response" %
                        #      (name, ip))
                        pass
                else:
                    # print("    %s[%s] - %s%s - %sNo Response" %
                    #      (name, ip,))
                    pass
            except:
                # print("    %s[%s] - %s%s - %sNo Response" %
                #      (name, ip))
                pass
        polling.append(item)
        # for loop

    # Save polling data snapsot
    current = {'timestamp': time.time(), 'devices': polling}
    output1 = json.dumps(current, indent=4)  # indent=4
    # print(f"LINE 196 Local Device json {output1}")

    #print('\nThis is POLLED Add DPS sorter here\n')
    df = pd.read_json(output1)
    df = pd.json_normalize(df['devices'])  # Works with Tuple Inserted
    df = df.fillna(-1)

    # print(f"LINE 203 DF: {df}")
    df['type'] = None

    try:
        df['type'] = np.where(df['dps.dps.20'] != -1, 'light', df['type'])
    except:
        pass
    try:
        df['type'] = np.where(df['dps.dps.1'] != -1, 'switch', df['type'])
    except:
        pass
    try:
        df['type'] = np.where(df['dps.101'] != -1, 'tuya', df['type'])
    except:
        pass

    lights = df[df['type'] == 'light'].reset_index(drop=True)
    print(f"\nLINE 231 LIGHTS: {lights}\n")
    switches = df[df['type'] == 'switch'].reset_index(drop=True)
    print(f"\nLINE 233 SWITCHES: {switches}\n")
    tuya = df[df['type'] == 'tuya'].reset_index(drop=True)
    print(f"\nLINE 235 SWITCHES: {tuya}\n")
    print('\nSort POLLED and Add Nodes\n')

    device_list = [lights]
    for device in device_list:
        for idx, row in device.iterrows():
            name = row['name']
            id = row['id']
            id_new = id
            ip = row['ip']
            key = row['key']
            ver = row['ver']
            # id_new = id
            address = row['type'] + '_%s' % (idx+1)
            print('{name}\n{id_new}\n{ip}\n{key}\n{ver}\n{address}\n'.format(
                name=name, id_new=id_new, ip=ip, key=key, ver=ver, address=address,))
            # node = tuya_light_node.LightNode(
            #    self.poly, self.address, address, name, id_new, ip, key)
            # self.poly.addNode(node)
            # self.wait_for_node_event()

    device_list = [switches]
    for device in device_list:
        for idx, row in device.iterrows():
            name = row['name']
            id = row['id']
            id_new = id
            ip = row['ip']
            key = row['key']
            ver = row['ver']
            # id_new = id
            address = row['type'] + '_%s' % (idx+1)
            print('{name}\n{id_new}\n{ip}\n{key}\n{ver}\n{address}\n'.format(
                name=name, id_new=id_new, ip=ip, key=key, ver=ver, address=address,))
            # node = tuya_switch_node.SwitchNode(
            #    self.poly, self.address, address, name, id_new, ip, key)
            # self.poly.addNode(node)
            # self.wait_for_node_event()

    device_list = [tuya]
    for device in device_list:
        for idx, row in device.iterrows():
            name = row['name']
            id = row['id']
            id_new = id
            ip = row['ip']
            key = row['key']
            ver = row['ver']
            # id_new = id
            address = row['type'] + '_%s' % (idx+1)
            print('{name}\n{id_new}\n{ip}\n{key}\n{ver}\n{address}\n'.format(
                name=name, id_new=id_new, ip=ip, key=key, ver=ver, address=address,))
            # node = TuyaNode(
            #    self.poly, self.address, address, name, value)
            # self.poly.addNode(node)
            # self.wait_for_node_event()

print("\nDone.\n")
