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
    #print(f"LINE 65 Token: {response}")
    try:
        response_dict = json.loads(response.content.decode())
    except:
        try:
            response_dict = json.dumps(response.content)
            # print(response_dict)
        except:
            print("Failed to get valid JSON response")

    return (response_dict)


color = True
CONFIGFILE = 'tinytuya.json'
# DEVICEFILE = 'devices.json'
# RAWFILE = 'tuya-raw.json'
# SNAPSHOTFILE = 'snapshot.json'
config = {}
config['apiKey'] = ''
config['apiSecret'] = ''
config['apiRegion'] = ''
config['apiDeviceID'] = ''
needconfigs = True
try:
    # Load defaults
    with open(CONFIGFILE) as f:
        config = json.load(f)
except:
    # First Time Setup
    pass

if (color == False):
    # Disable Terminal Color Formatting
    bold = subbold = normal = dim = alert = alertdim = ""
else:
    # Terminal Color Formatting
    bold = "\033[0m\033[97m\033[1m"
    subbold = "\033[0m\033[32m"
    normal = "\033[97m\033[0m"
    dim = "\033[0m\033[97m\033[2m"
    alert = "\033[0m\033[91m\033[1m"
    alertdim = "\033[0m\033[91m\033[2m"
# First Message
print(bold + 'LINE 109 TinyTuya Setup Wizard' + dim +
      ' [%s]' % (tinytuya.version) + normal)
print('')

if (config['apiKey'] != '' and config['apiSecret'] != '' and
        config['apiRegion'] != '' and config['apiDeviceID'] != ''):
    needconfigs = False
    # Second Message
    print("    " + subbold + "LINE 117 Existing settings:" + dim +
          "\n        API Key=%s \n        Secret=%s\n        DeviceID=%s\n        Region=%s" %
          (config['apiKey'], config['apiSecret'], config['apiDeviceID'],
           config['apiRegion']))
    # Third Message
    print('')
    answer = 'Y'  # input(subbold + '    Use existing credentials ' +
    #   normal + '(Y/n): ')
    if (answer[0:1].lower() == 'n'):
        needconfigs = True

    if (needconfigs):
        # Ask user for config settings
        print('')
        config['apiKey'] = input(subbold + "    Enter " + bold + "API Key" + subbold +
                                 " from tuya.com: " + normal)
        config['apiSecret'] = input(subbold + "    Enter " + bold + "API Secret" + subbold +
                                    " from tuya.com: " + normal)
        config['apiDeviceID'] = input(subbold +
                                      "    Enter " + bold + "any Device ID" + subbold +
                                      " currently registered in Tuya App (used to pull full list): " + normal)
        # TO DO - Determine apiRegion based on Device - for now, ask
        config['apiRegion'] = input(subbold + "    Enter " + bold + "Your Region" + subbold +
                                    " (Options: us, eu, cn or in): " + normal)
        # Write Config
        json_object = json.dumps(config, indent=4)
        # with open(CONFIGFILE, "w") as outfile:
        #    outfile.write(json_object)
        # print(bold + "\n>> Configuration Data Saved to " + CONFIGFILE)
        print(dim + json_object)

    KEY = config['apiKey']
    SECRET = config['apiSecret']
    DEVICEID = config['apiDeviceID']
    REGION = config['apiRegion']        # us, eu, cn, in
    LANG = 'en'                         # en or zh

    # Get Oauth Token from tuyaPlatform
    uri = 'token?grant_type=1'
    response_dict = tuyaPlatform(REGION, KEY, SECRET, uri)
    print(f"LINE 157 RESPONSE DICT : {response_dict}")
    if not response_dict['success']:
        # print('\n\n' + bold + 'Error from Tuya server: ' +
        #     dim + response_dict['msg'])
        pass

    token = response_dict['result']['access_token']

    # Get UID from sample Device ID
    uri = 'devices/%s' % DEVICEID
    response_dict = tuyaPlatform(REGION, KEY, SECRET, uri, token)

    if not response_dict['success']:
        print('\n\n' + bold + 'Error from Tuya server: ' +
              dim + response_dict['msg'])
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
    print("\n\n" + bold + "LINE 195 Device Listing\n" + dim)
    output = json.dumps(tuyadevices, indent=4)  # sort_keys=True')
    print(output)


# Find out if we should poll all devices
    answer = 'Y'  # input(subbold + '\nPoll local devices? ' +
    # normal + '(Y/n): ')
    if (answer[0:1].lower() != 'n'):
        # Scan network for devices and provide polling data
        print(normal + "\nLINE 205 Scanning local network for Tuya devices...")
        devices = tinytuya.deviceScan(False, 20)
        print("    %s%s local devices discovered%s" %
              (dim, len(devices), normal))
        print("")

        def getIP(d, gwid):
            for ip in d:
                if 'gwId' in d[ip]:
                    if (gwid == d[ip]['gwId']):
                        return (ip, d[ip]['version'])
            return (0, 0)

        polling = []
        print("LINE 219 Polling local devices...")
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
                      (subbold, name, dim, ip, alert, normal))
            else:
                try:
                    d = tinytuya.OutletDevice(i['id'], ip, i['key'])
                    if ver == "3.3":
                        d.set_version(3.3)
                    data = d.status()
                    if 'dps' in data:
                        item['dps'] = data
                        state = alertdim + "Off" + dim
                        try:
                            if '1' in data['dps'] or '20' in data['dps']:
                                if '1' in data['dps']:
                                    if data['dps']['1'] == True:
                                        state = bold + "On" + dim
                                if '20' in data['dps']:
                                    if data['dps']['20'] == True:
                                        state = bold + "On" + dim
                                print("    %s[%s] - %s%s - %s - DPS: %r" %
                                      (subbold, name, dim, ip, state, data['dps']))
                            else:
                                print("    %s[%s] - %s%s - DPS: %r" %
                                      (subbold, name, dim, ip, data['dps']))
                        except:
                            print("    %s[%s] - %s%s - %sNo Response" %
                                  (subbold, name, dim, ip, alertdim))
                    else:
                        print("    %s[%s] - %s%s - %sNo Response" %
                              (subbold, name, dim, ip, alertdim))
                except:
                    print("    %s[%s] - %s%s - %sNo Response" %
                          (subbold, name, dim, ip, alertdim))
            polling.append(item)
            # for loop

        # Save polling data snapsot
        current = {'timestamp': time.time(), 'devices': polling}
        output1 = json.dumps(current, indent=4)  # indent=4
        # print(output1)
        #print(f"LINE 269 Local Device json {output1}")
        #output2 = dict(output1)
        print(type(output1))  # Type STR
        # print(output1)
        #res = tuple(map(int(base=10), output1.split(', ')))
        # JSON Recieved Below
        # print(type(res))

        """output1 = {
            "name": "Switch Dutch Door",
            "ip": "192.168.1.134",
            "ver": "3.3",
            "id": "eb9f1eaef823420e19bewt",
            "key": "659ef2b2c7d3a60a",
            "dps": {
                    "dps": {
                        "1": False,
                        "7": 0,
                        "15": "none",
                        "18": ""
                    }
            }
        }, {
            "name": "Switch Garage Overhead",
            "ip": "192.168.1.132",
            "ver": "3.3",
            "id": "eb7ac0fbe689ca95f7dxxk",
            "key": "449ebc60812eb8bb",
            "dps": {
                    "dps": {
                        "1": False,
                        "9": 0,
                        "38": "off",
                        "40": "relay",
                        "41": False,
                        "42": "",
                        "43": "",
                        "44": ""
                    }
            }
        }, {
            "name": "Switch Front Door",
            "ip": "192.168.1.133",
            "ver": "3.3",
            "id": "eb7053a032f633f952bqq2",
            "key": "a792deae091dff2c",
            "dps": {
                    "dps": {
                        "1": False,
                        "7": 0,
                        "15": "none",
                        "18": ""
                    }
            }
        }, {
            "name": "Switch Side Garage Outside",
            "ip": "192.168.1.131",
            "ver": "3.3",
            "id": "eb577fdd6642efcbc3g0qc",
            "key": "85861de497baa60d",
            "dps": {
                    "dps": {
                        "1": False,
                        "9": 0,
                        "38": "off",
                        "40": "relay",
                        "41": False,
                        "42": "",
                        "43": "",
                        "44": ""
                    }
            }
        }, {
            "name": "LED Garage",
            "ip": "192.168.1.148",
            "ver": "3.3",
            "id": "ebfd4f4263bb769d99zjkq",
            "key": "ec0b2b581a246eab",
            "dps": {
                    "dps": {
                        "20": False,
                        "21": "white",
                        "22": 10,
                        "23": 1000,
                        "24": "000003250221",
                        "25": "000d0d0000000000000000180000",
                        "26": 0
                    }
            }
        }, {
            "name": "Switch Dining Pool Outside",
            "ip": "192.168.1.130",
            "ver": "3.3",
            "id": "017743508caab5f29984",
            "key": "be9d5b1387e6f231",
            "dps": {
                    "devId": "017743508caab5f29984",
                    "dps": {
                        "1": False,
                        "9": 0
                    }
            }
        }, {
            "name": "LED Office",
            "ip": "192.168.1.147",
            "ver": "3.3",
            "id": "ebfc16d57ed374932cjqfk",
            "key": "805217605357161b",
            "dps": {
                    "dps": {
                        "20": False,
                        "21": "colour",
                        "22": 10,
                        "23": 1000,
                        "24": "00000000000a",
                        "25": "020d0d00000000000000001903e8",
                        "26": 0
                    }
            }
        }, {
            "name": "Switch Office Outside Lights",
            "ip": "192.168.1.145",
            "ver": "3.3",
            "id": "017743508caab5f0973e",
            "key": "e779c96c964f71b2",
            "dps": {
                    "devId": "017743508caab5f0973e",
                    "dps": {
                        "1": False,
                        "9": 0
                    }
            }
        },
        {
            "name": "LED Strip Cabinets",
            "ip": "192.168.1.155",
            "ver": "3.3",
            "id": "ebe097c0407da32084kvtr",
            "key": "22ad5946c44356a4",
            "dps": {
                    "dps": {
                        "20": False,
                        "21": "colour",
                        "24": "000003e803e8",
                        "25": "000e0d00002e03e802cc00000000",
                        "26": 0
                    }
            }
        }, {
            "name": "Switch Master Outside",
            "ip": "192.168.1.126",
            "ver": "3.3",
            "id": "017743508caab5f126b0",
            "key": "17a1e4c963773637",
            "dps": {
                    "devId": "017743508caab5f126b0",
                    "dps": {
                        "1": False,
                        "9": 0
                    }
            }
        }, {
            "name": "Switch Garden Outside",
            "ip": "192.168.1.146",
            "ver": "3.3",
            "id": "017743508caab5f385a7",
            "key": "2bc2d5aef80f3aee",
            "dps": {
                    "devId": "017743508caab5f385a7",
                    "dps": {
                        "1": False,
                        "9": 0
                    }
            }
        }"""

        print(output1)  # Tuple
        print('This is POLLED Add DPS sorter here')
        # Works with String but missing Data?
        df = pd.read_json(output1)
        df = pd.json_normalize(df['devices'])  # Works with Tuple Inserted
        df = df.fillna(-1)

        print(f"LINE 453 DF: {df}")
        df['type'] = None

        try:

            df['type'] = np.where(
                df['devId.dps.20'] != -1, 'light')  # , df['type']
            # df = pd.DataFrame(
            #    columns=['timestamp', 'devices', 'type'], index=pd.TimedeltaIndex([]))

        except:
            pass
        try:
            df['type'] = np.where(df['devId.dps.1'] != -
                                  1, 'switch')  # , df['type']
        except:
            pass
        try:
            df['type'] = np.where(df['dps.101'] != -1, 'tuya', df['type'])
        except:
            pass
        lights = df[df['type'] == 'light'].reset_index(drop=True)
        switches = df[df['type'] == 'switch'].reset_index(drop=True)
        tuya = df[df['type'] == 'tuya'].reset_index(drop=True)
        print(f"LINE 477 LIGHTS: {lights}")
        print(f"LINE 478 SWITCHES: {switches}")
        # {device_id} - {dict_found['name']}, {dict_found['key']}, {
        # lights = device_id
        # value['gwId']}, {value['ip']}

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

# print(output)
print("\nDone.\n")
