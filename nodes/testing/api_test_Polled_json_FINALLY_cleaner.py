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

###### Custom Parameters ######
new_sign_algorithm = True,
token = None,
headers = None,
body = None,
apiRegion = "us",
apiKey = "txejpdfda9iwmn5cg2es",
apiSecret = "46d6072ffd724e0ba5ebeb5cc6b9dce9",
uri = "token?grant_type = 1",


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
    # print(f"LINE 65 Token: {response}")
    try:
        response_dict = json.loads(response.content.decode())
    except:
        try:
            response_dict = json.dumps(response.content)
            # print(response_dict)
        except:
            print("Failed to get valid JSON response")
    return (response_dict)


##CONFIGFILE = 'tinytuya.json'
# print(CONFIGFILE)
# config = {
    # "apiKey": "txejpdfda9iwmn5cg2es",
    # "apiSecret": "46d6072ffd724e0ba5ebeb5cc6b9dce9",
    # "apiRegion": "us",
    # "apiDeviceID": "ebfc16d57ed374932cjqfk"
    # }
###### Custom Parameters ######
config = {}
config['apiKey'] = 'txejpdfda9iwmn5cg2es'
config['apiSecret'] = '46d6072ffd724e0ba5ebeb5cc6b9dce9'
config['apiRegion'] = 'us'
config['apiDeviceID'] = 'ebfc16d57ed374932cjqfk'
needconfigs = False

"""try:
    # Load defaults
    with open(CONFIGFILE) as f:
        config = json.load(f)
except:
    # First Time Setup
    pass"""

# First Message
print('LINE 89 TinyTuya Setup Wizard' +
      ' [%s]' % (tinytuya.version))
print('')

if (config['apiKey'] != '' and config['apiSecret'] != '' and
        config['apiRegion'] != '' and config['apiDeviceID'] != ''):
    needconfigs = False
    # Second Message
    print("    " + "LINE 117 Existing settings:" +
          "\n        API Key=%s \n        Secret=%s\n        DeviceID=%s\n        Region=%s" %
          (config['apiKey'], config['apiSecret'], config['apiDeviceID'],
           config['apiRegion']))
    # Third Message
    print('')
    answer = 'Y'  # input(subbold + '    Use existing credentials ' +
    #   normal + '(Y/n): ')
    if (answer[0:1].lower() == 'n'):
        needconfigs = True

    """if (needconfigs):
        # Ask user for config settings
        print('')
        config['apiKey'] = input("    Enter " + "API Key" +
                                 " from tuya.com: ")
        config['apiSecret'] = input("    Enter " + "API Secret" +
                                    " from tuya.com: ")
        config['apiDeviceID'] = input(
            "    Enter " + "any Device ID" +
            " currently registered in Tuya App (used to pull full list): ")
        # TO DO - Determine apiRegion based on Device - for now, ask
        config['apiRegion'] = input("    Enter " + "Your Region" +
                                    " (Options: us, eu, cn or in): ")
        # Write Config
        json_object = json.dumps(config, indent=4)
        print(json_object)"""

    KEY = config['apiKey']
    SECRET = config['apiSecret']
    DEVICEID = config['apiDeviceID']
    REGION = config['apiRegion']        # us, eu, cn, in
    LANG = 'en'                         # en or zh

    # Get Oauth Token from tuyaPlatform
    uri = 'token?grant_type=1'
    response_dict = tuyaPlatform(REGION, KEY, SECRET, uri)
    print(f"LINE 140 RESPONSE DICT ACESS TOKEN : {response_dict}")
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
    # print(output)

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
    print("\n\n" + "LINE 177 Device Listing\n")
    print(output)

# Find out if we should poll all devices
    answer = 'Y'  # input(subbold + '\nPoll local devices? ' +
    # normal + '(Y/n): ')
    if (answer[0:1].lower() != 'n'):
        # Scan network for devices and provide polling data
        print("\nLINE 185 Scanning local network for Tuya devices...")
        devices = tinytuya.deviceScan(False, 20)

        def getIP(d, gwid):
            for ip in d:
                if 'gwId' in d[ip]:
                    if (gwid == d[ip]['gwId']):
                        return (ip, d[ip]['version'])
            return (0, 0)

        polling = []
        print("LINE 196 Polling local devices...")
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
                print("    %s[%s] - %s%s - %sError: No IP found%s" %
                      (name, ip, ))
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
        # print(f"LINE 257 Local Device json {output1}")

        print('This is POLLED Add DPS sorter here')
        df = pd.read_json(output1)
        df = pd.json_normalize(df['devices'])  # Works with Tuple Inserted
        df = df.fillna(-1)

        # print(f"LINE 264 DF: {df}")
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
        switches = df[df['type'] == 'switch'].reset_index(drop=True)
        tuya = df[df['type'] == 'tuya'].reset_index(drop=True)
        print(f"LINE 285 LIGHTS: {lights}")
        print(f"LINE 286 SWITCHES: {switches}")

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

        print(output)
        print("\nDone.\n")
