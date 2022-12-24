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

##### Json Data we need to Grab ####
"""jsonData = [{
    "name": "Switch Side Garage Outside",
            "ip": "192.168.1.131",
            "ver": "3.3",
            "id": "eb577fdd6642efcbc3g0qc",
            "key": "85861de497baa60d",
            "devId": {
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
            "devId": {
                "dps": {
                    "20": False,
                    "21": "white",
                    "22": 10,
                    "23": 1000,
                    "24": "010e023b0389",
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
            "devId": {
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
            "devId": {
                "dps": {
                    "20": False,
                    "21": "white",
                    "22": 10,
                    "23": 1000,
                    "24": "00450364039d",
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
            "devId": {
                "devId": "017743508caab5f0973e",
                "dps": {
                    "1": False,
                    "9": 0
                }
            }
}, {
    "name": "LED Strip Cabinets",
            "ip": "192.168.1.155",
            "ver": "3.3",
            "id": "ebe097c0407da32084kvtr",
            "key": "22ad5946c44356a4",
            "devId": {
                "dps": {
                    "20": False,
                    "21": "colour",
                    "24": "00f003e800d0",
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
            "devId": {
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
            "devId": {
                "devId": "017743508caab5f385a7",
                "dps": {
                    "1": False,
                    "9": 0
                }
            }
}]"""

jsonData = {
    "timestamp": 1667819939.804203,
    "devices": [
        {
            "name": "Switch Garage Overhead",
            "ip": "192.168.1.132",
            "ver": "3.3",
            "id": "eb7ac0fbe689ca95f7dxxk",
            "key": "449ebc60812eb8bb",
            "dps": {
                "dps": {
                    "1": True,
                    "9": 0,
                    "38": "off",
                    "40": "relay",
                    "41": False,
                    "42": "",
                    "43": "",
                    "44": ""
                }
            }
        },
        {
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
        },
        {
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
        },
        {
            "name": "LED Garage",
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
                    "24": "000003250221",
                    "25": "000d0d0000000000000000180000",
                    "26": 0
                }
            }
        },
        {
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
        },
        {
            "name": "LED Office",
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
                    "24": "00e603a001ee",
                    "25": "020d0d00000000000000001903e8",
                    "26": 0
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
        },
        {
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
        },
        {
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
        }
    ]
}


# print(jsonData)
# for i in output1:
# pass
#    print(i)
# add string here for devices instead of jsonfile only for names
# df = pd.json_normalize(jsonData['devices'])
df = pd.json_normalize(jsonData['devices'])  # jsonData
df = df.fillna(-1)
# print(df)
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
tuya = df[df['type'] == 'tuya'].reset_index(drop=True)
print(lights)
print(switches)
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
        address = row['type'] + '_%s' % (idx+1)
        print('{name}\n{id_new}\n{ip}\n{key}\n{ver}\n{address}\n'.format(
            name=name, id_new=id_new, ip=ip, key=key, ver=ver, address=address,))

print(jsonData)
print("\nDone.\n")

"""with open(SNAPSHOTFILE, "w") as outfile:
        outfile.write(output)

    print("\nDone.\n")
    pass"""
