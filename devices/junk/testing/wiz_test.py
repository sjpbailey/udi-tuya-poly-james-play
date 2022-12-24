# Modules
import requests
import time
import hmac
import hashlib
import json
import pprint
import logging
import tinytuya
import logging
import pandas as pd
import numpy as np


color = False
# Get Configuration Data
CONFIGFILE = 'tinytuya.json'
DEVICEFILE = 'devices.json'
RAWFILE = 'tuya-raw.json'
SNAPSHOTFILE = 'snapshot.json'
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

print(bold + 'TinyTuya Setup Wizard' + dim +
      ' [%s]' % (tinytuya.version) + normal)
print('')

"""if (config['apiKey'] != '' and config['apiSecret'] != '' and
        config['apiRegion'] != '' and config['apiDeviceID'] != ''):
    needconfigs = False
    print("    " + subbold + "Existing settings:" + dim +
          "\n        API Key=%s \n        Secret=%s\n        DeviceID=%s\n        Region=%s" %
          (config['apiKey'], config['apiSecret'], config['apiDeviceID'],
           config['apiRegion']))
    print('')
    answer = input(subbold + '    Use existing credentials ' +
                   normal + '(Y/n): ')
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
    with open(CONFIGFILE, "w") as outfile:
        outfile.write(json_object)
    print(bold + "\n>> Configuration Data Saved to " + CONFIGFILE)
    print(dim + json_object)

KEY = config['apiKey']
SECRET = config['apiSecret']
DEVICEID = config['apiDeviceID']
REGION = config['apiRegion']        # us, eu, cn, in
LANG = 'en'                         # en or zh

# Get Oauth Token from tuyaPlatform
uri = 'token?grant_type=1'
response_dict = tuyaPlatform(REGION, KEY, SECRET, uri)

if not response_dict['success']:
    print('\n\n' + bold + 'Error from Tuya server: ' +
          dim + response_dict['msg'])
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
uid = response_dict['result']['uid']
uri = 'users/%s/devices' % uid
json_data = tuyaPlatform(REGION, KEY, SECRET, uri, token)"""


json_data = {
    "result": [
        {
            "active_time": 1667065898,
            "biz_type": 0,
            "category": "kg",
            "create_time": 1667064851,
            "icon": "smart/icon/ay14906729310721fNjn/1568862445415ffab0175.jpg",
            "id": "017743508caab5f126b0",
            "ip": "98.41.236.33",
            "lat": "37.7183",
            "local_key": "17a1e4c963773637",
            "lon": "-121.4701",
            "model": "SS01S(\u4e0d\u5206\u8d1f\u8f7d)\u4e50\u946b",
            "name": "Master Bedroom Outside ",
            "online": True,
            "owner_id": "33161067",
            "product_id": "pigcdkf9bdubtskr",
            "product_name": "Smart Light Switch",
            "status": [
                {
                    "code": "switch_1",
                    "value": False
                },
                {
                    "code": "countdown_1",
                    "value": 0
                }
            ],
            "sub": False,
            "time_zone": "-08:00",
            "uid": "az1610958067414WkfOO",
            "update_time": 1667065906,
            "uuid": "017743508caab5f126b0"
        },
        {
            "active_time": 1611129340,
            "biz_type": 0,
            "category": "dj",
            "create_time": 1610826967,
            "icon": "smart/icon/ay1526363067472WHq8d/b354bef20490dfd22c5a3d4c89b6269c.png",
            "id": "ebfd4f4263bb769d99zjkq",
            "ip": "98.41.236.33",
            "lat": "37.7183",
            "local_key": "ec0b2b581a246eab",
            "lon": "-121.4701",
            "name": "Garage",
            "online": True,
            "owner_id": "33161067",
            "product_id": "vcbxdeohrcq4tcpq",
            "product_name": "Smart Bulb-SL10",
            "status": [
                {
                    "code": "switch_led",
                    "value": True
                },
                {
                    "code": "work_mode",
                    "value": "white"
                },
                {
                    "code": "bright_value_v2",
                    "value": 10
                },
                {
                    "code": "temp_value_v2",
                    "value": 1000
                },
                {
                    "code": "colour_data_v2",
                    "value": "{\"h\":35,\"s\":662,\"v\":964}"
                },
                {
                    "code": "scene_data_v2",
                    "value": "{\"scene_num\":1,\"scene_units\":[{\"bright\":24,\"h\":0,\"s\":0,\"temperature\":0,\"unit_change_mode\":\"static\",\"unit_gradient_duration\":13,\"unit_switch_duration\":13,\"v\":0}]}"
                },
                {
                    "code": "countdown_1",
                    "value": 0
                },
                {
                    "code": "music_data",
                    "value": ""
                },
                {
                    "code": "control_data",
                    "value": ""
                },
                {
                    "code": "rhythm_mode",
                    "value": "AAAAAAA="
                },
                {
                    "code": "sleep_mode",
                    "value": "AAA="
                },
                {
                    "code": "wakeup_mode",
                    "value": "AAA="
                }
            ],
            "sub": False,
            "time_zone": "-08:00",
            "uid": "az1610958067414WkfOO",
            "update_time": 1667064381,
            "uuid": "51ff978b119a9dc2"
        },
        {
            "active_time": 1660708648,
            "biz_type": 0,
            "category": "dd",
            "create_time": 1612504334,
            "icon": "smart/icon/ay14906729310721fNjn/f266b748d1b92584887cde26ea9212ca.png",
            "id": "ebe097c0407da32084kvtr",
            "ip": "98.41.236.33",
            "lat": "37.7183",
            "local_key": "22ad5946c44356a4",
            "lon": "-121.4701",
            "name": "Under Cabinets ",
            "online": True,
            "owner_id": "33161067",
            "product_id": "e8naaq4xcsfvuunf",
            "product_name": "LED Strip Lights",
            "status": [
                {
                    "code": "switch_led",
                    "value": False
                },
                {
                    "code": "work_mode",
                    "value": "colour"
                },
                {
                    "code": "colour_data",
                    "value": "{\"h\":240,\"s\":1000,\"v\":1000}"
                },
                {
                    "code": "scene_data",
                    "value": "{\"scene_num\":1,\"scene_units\":[{\"bright\":0,\"h\":46,\"s\":1000,\"temperature\":0,\"unit_change_mode\":\"static\",\"unit_gradient_duration\":13,\"unit_switch_duration\":14,\"v\":716}]}"
                },
                {
                    "code": "countdown",
                    "value": 0
                }
            ],
            "sub": False,
            "time_zone": "-07:00",
            "uid": "az1610958067414WkfOO",
            "update_time": 1667064379,
            "uuid": "c2854608edea94d7"
        },
        {
            "active_time": 1656839758,
            "biz_type": 0,
            "category": "kg",
            "create_time": 1615015039,
            "icon": "smart/icon/ay14906729310721fNjn/1568862445415ffab0175.jpg",
            "id": "017743508caab5f385a7",
            "ip": "98.41.236.33",
            "lat": "37.7183",
            "local_key": "2bc2d5aef80f3aee",
            "lon": "-121.4701",
            "name": "Switch Family Room Sconces",
            "online": True,
            "owner_id": "33161067",
            "product_id": "pigcdkf9bdubtskr",
            "product_name": "Smart Light Switch",
            "status": [
                {
                    "code": "switch_1",
                    "value": True
                },
                {
                    "code": "countdown_1",
                    "value": 0
                }
            ],
            "sub": False,
            "time_zone": "-08:00",
            "uid": "az1610958067414WkfOO",
            "update_time": 1667064379,
            "uuid": "017743508caab5f385a7"
        },
        {
            "active_time": 1610958245,
            "biz_type": 0,
            "category": "kg",
            "create_time": 1610826905,
            "icon": "smart/icon/ay14906729310721fNjn/1568862445415ffab0175.jpg",
            "id": "017743508caab5f0973e",
            "ip": "98.41.236.33",
            "lat": "37.7183",
            "local_key": "e779c96c964f71b2",
            "lon": "-121.4701",
            "model": "SS01S(\u4e0d\u5206\u8d1f\u8f7d)\u4e50\u946b",
            "name": "Switch Office Outside Lights",
            "online": True,
            "owner_id": "33161067",
            "product_id": "pigcdkf9bdubtskr",
            "product_name": "Smart Light Switch",
            "status": [
                {
                    "code": "switch_1",
                    "value": False
                },
                {
                    "code": "countdown_1",
                    "value": 0
                }
            ],
            "sub": False,
            "time_zone": "-08:00",
            "uid": "az1610958067414WkfOO",
            "update_time": 1667064378,
            "uuid": "017743508caab5f0973e"
        },
        {
            "active_time": 1610958307,
            "biz_type": 0,
            "category": "dj",
            "create_time": 1610825045,
            "icon": "smart/icon/ay1526363067472WHq8d/b354bef20490dfd22c5a3d4c89b6269c.png",
            "id": "ebfc16d57ed374932cjqfk",
            "ip": "98.41.236.33",
            "lat": "37.7183",
            "local_key": "805217605357161b",
            "lon": "-121.4701",
            "name": "Office Light",
            "online": True,
            "owner_id": "33161067",
            "product_id": "vcbxdeohrcq4tcpq",
            "product_name": "Smart Bulb-SL10",
            "status": [
                {
                    "code": "switch_led",
                    "value": True
                },
                {
                    "code": "work_mode",
                    "value": "white"
                },
                {
                    "code": "bright_value_v2",
                    "value": 10
                },
                {
                    "code": "temp_value_v2",
                    "value": 1000
                },
                {
                    "code": "colour_data_v2",
                    "value": "{\"h\":195,\"s\":564,\"v\":694}"
                },
                {
                    "code": "scene_data_v2",
                    "value": "{\"scene_num\":3,\"scene_units\":[{\"bright\":25,\"h\":0,\"s\":0,\"temperature\":1000,\"unit_change_mode\":\"static\",\"unit_gradient_duration\":13,\"unit_switch_duration\":13,\"v\":0}]}"
                },
                {
                    "code": "countdown_1",
                    "value": 0
                },
                {
                    "code": "music_data",
                    "value": ""
                },
                {
                    "code": "control_data",
                    "value": ""
                },
                {
                    "code": "rhythm_mode",
                    "value": "AAAAAAA="
                },
                {
                    "code": "sleep_mode",
                    "value": "AAA="
                },
                {
                    "code": "wakeup_mode",
                    "value": "AAA="
                }
            ],
            "sub": False,
            "time_zone": "-08:00",
            "uid": "az1610958067414WkfOO",
            "update_time": 1667064377,
            "uuid": "8d46651d2af2bb95"
        }
    ],
    "success": True,
    "t": 1667446547530,
    "tid": "9aede31b5b2811eda761b2ff20907124"
}


# output = json.dumps(json_data, indent=4)
# Filter to only Name, ID and Key
tuyadevices = []
for i in json_data['result']:
    item = {}
    item['name'] = i['name'].strip()
    item['id'] = i['id']
    item['key'] = i['local_key']
    tuyadevices.append(item)

# Display device list
print("\n\n" + bold + "Device Listing\n" + dim)
output = json.dumps(tuyadevices, indent=4)  # sort_keys=True)
print(output)

# Save list to devices.json
print(bold + "\n>> " + normal + "Saving list to " + DEVICEFILE)
with open(DEVICEFILE, "w") as outfile:
    outfile.write(output)
print(dim + "    %d registered devices saved" % len(tuyadevices))

# Save raw TuyaPlatform data to tuya-raw.json
print(bold + "\n>> " + normal + "Saving raw TuyaPlatform response to " + RAWFILE)
try:
    with open(RAWFILE, "w") as outfile:
        outfile.write(json.dumps(json_data, indent=4))
except:
    print('\n\n' + bold + 'Unable to save raw file' + dim)

# Find out if we should poll all devices
answer = 'Y'  # input(subbold + '\nPoll local devices? ' +
#     normal + '(Y/n): ')
if (answer[0:1].lower() != 'n'):
    # Scan network for devices and provide polling data
    print(normal + "\nScanning local network for Tuya devices...")
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
print("Polling local devices...")
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
                        # print("    %s[%s] - %s%s - %s - DPS: %r" %
                              # (subbold, name, dim, ip, state, data['dps']))
                    else:
                        pass
                        # print("    %s[%s] - %s%s - DPS: %r" %
                        # (subbold, name, dim, ip, data['dps']))
                except:
                    pass
                    # print("    %s[%s] - %s%s - %sNo Response" %
                    # (subbold, name, dim, ip, alertdim))
            else:
                pass
                # print("    %s[%s] - %s%s - %sNo Response" %
                # (subbold, name, dim, ip, alertdim))
        except:
            pass
            # print("    %s[%s] - %s%s - %sNo Response" %
            # (subbold, name, dim, ip, alertdim))
    polling.append(item)
# for loop
# print("\nDone with tuya polling.\n")
# Save polling data snapsot
    current = {'timestamp': time.time(), 'devices': polling}
# print("\n\n" + bold + "LED's Switches\n" + dim)
# print(current)
    jsonData2 = json.dumps(current, indent=4)
    print(jsonData2)

"""output1 = {
    "name": "Master Bedroom Outside",
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
},
{
    "name": "Garage",
    "ip": "192.168.1.148",
    "ver": "3.3",
    "id": "ebfd4f4263bb769d99zjkq",
    "key": "ec0b2b581a246eab",
    "dps": {
            "dps": {
                "20": True,
                "21": "white",
                "22": 10,
                "23": 1000,
                "24": "0023029603c4",
                "25": "000d0d0000000000000000180000",
                "26": 0
            }
    }
},
{
    "name": "Under Cabinets",
    "ip": "192.168.1.155",
    "ver": "3.3",
    "id": "ebe097c0407da32084kvtr",
    "key": "22ad5946c44356a4",
    "dps": {
            "dps": {
                "20": False,
                "21": "colour",
                "24": "00f003e803e8",
                "25": "000e0d00002e03e802cc00000000",
                "26": 0
            }
    }
},
{
    "name": "Switch Family Room Sconces",
    "ip": "192.168.1.146",
    "ver": "3.3",
    "id": "017743508caab5f385a7",
    "key": "2bc2d5aef80f3aee",
    "dps": {
            "devId": "017743508caab5f385a7",
            "dps": {
                "1": True,
                "9": 0
            }
    }
},
{
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
    "name": "Office Light",
    "ip": "192.168.1.147",
    "ver": "3.3",
    "id": "ebfc16d57ed374932cjqfk",
    "key": "805217605357161b",
    "dps": {
            "dps": {
                "20": True,
                "21": "white",
                "22": 10,
                "23": 1000,
                "24": "00c3023402b6",
                "25": "020d0d00000000000000001903e8",
                "26": 0
            }
    }
}"""

# print(current)

# add string here for devices instead of jsonfile only for names
# df = pd.json_normalize(jsonData2[1])  # jsonData
df = pd.read_json(jsonData2[0])
df = df.fillna(-1)
print(df)
df['type'] = None
# print(df['devId.dps.1'])
# if df['devId.dps.20'] == True:
try:
    df['type'] = np.where(df['devId.dps.20'] != -1, 'light', df['type'])
except:
    pass
try:
    df['type'] = np.where(df['devId.dps.1'] != -1, 'switch', df['type'])
except:
    pass
try:
    df['type'] = np.where(df['dps.dps.101'] != -1, 'tuya', df['type'])
except:
    pass

lights = df[df['type'] == 'light'].reset_index(drop=True)
switches = df[df['type'] == 'switch'].reset_index(drop=True)
print(lights)
"""df = pd.read_json(current)
df = df.fillna(-1)

df['type'] = None
df['type'] = np.where(df['devId.dps.20'] != -1, 'light', df['type'])
df['type'] = np.where(df['devId.dps.1'] != -1, 'switch', df['type'])


#lights = df[df['type'] == 'light'].reset_index(drop=True)
#switches = df[df['type'] == 'switch'].reset_index(drop=True)
#tuya = df[df['type'] == 'tuya'].reset_index(drop=True)
# print(lights)
# {device_id} - {dict_found['name']}, {dict_found['key']}, {
# lights = device_id
# value['gwId']}, {value['ip']}"""

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
# self.wait_for_node_event()"""

"""    device_list = [switches]
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
            address = row['type'] + '_%s' % (idx+1)
            print('{name}\n{id_new}\n{ip}\n{key}\n{ver}\n{address}\n'.format(
                name=name, id_new=id_new, ip=ip, key=key, ver=ver, address=address,))"""


"""with open(SNAPSHOTFILE, "w") as outfile:
        outfile.write(output)"""

print("\nDone.\n")
pass
