import json
import pandas as pd
import numpy as np
import tinytuya
import time


"""data = [{"devices": {
    "name": "LED Office",
            "ip": "192.168.1.147",
            "ver": "3.3",
            "id": "ebfc16d57ed374932cjqfk",
            "key": "805217605357161b",
            "devId": {'dps': {'20': True, '21': 'white', '22': 1000, '23': 1000,
                              '24': '009d03c603a1', '25': '020d0d00000000000000001903e8', '26': 0}}}}]"""
# print(type(data))
# data1 = {"name": "LED Office",
# "id": "ebfc16d57ed374932cjqfk", "key": "805217605357161b"}
# print(type(data1))
jsondata = [{"name": "LED Office", "id": "ebfc16d57ed374932cjqfk", "key": "805217605357161b", 'dps': {'20': False, '21': 'white', '22': 10, '23': 1000,
                                                                                                      '24': '009d03c603a1', '25': '020d0d00000000000000001903e8', '26': 0}}]
# if jsondata['dps'] == 20:
devices_list = json.dumps(jsondata)
key = jsondata[1:1]
print(key)
# print(type(devices_list))
# print(type(jsondata))
# print(jsondata[0:10])

# for dps in str(jsondata):  # )xfor i in node_status: gives dps devId)
"""jsondata = {"name": "LED Office",
            "ip": "192.168.1.147",
            "ver": "3.3",
            "id": "ebfc16d57ed374932cjqfk",
            "key": "805217605357161b",
            "devId": {
                "dps": {
                    "20": True,
                    "21": "colour",
                    "22": 10,
                    "23": 1000,
                    "24": "0000000003e8",
                    "25": "020d0d00000000000000001903e8",
                    "26": 0
                }
            }
            }"""

"""devices_list = json.dumps(jsondata)
print("%-25s %-24s %-16s %-17s %-5s" % ("Name", "ID", "IP", "Key", "Version"))
jsondata = str(devices_list)
for item in devices_list:
    name = item[0:0]
    print(name)
    id = item[0:10]
    print(id)
    ip = item[0:11]
    print(ip)
    key = item[1:10]
    print(key)
    ver = item[1:11]
    print(ver)"""


"""devices_list = json.dumps(jsondata)
# print(devices_list)
scan_results = tinytuya.deviceScan()
#scan_results = str(scan_results)
for value in scan_results.values():
    device_id = value['gwId']
    ip = value['ip']
    key = value['key']

    if len(device_id) > 10:
        device_id = device_id  # [:10]
        print(device_id)
        print(ip)
        print(key)
        time.sleep(0)
    tuya_device = tinytuya.BulbDevice(
        value['gwId'], value['ip'], value['key'])
    tuya_device.set_version(3.3)
    node_Switch_status = tuya_device.status()
    print(node_Switch_status)
    #   time.sleep(5)
    #   tuya_device2 = tinytuya.OutletDevice(
    #       value['gwId'], value['ip'])  # , value['key'])
    #   tuya_device2.set_version(3.3)
    #    node_Light_status = tuya_device2.status()
    #   print(node_Light_status)
    # print(type(node_status))
    # print(type(scan_results))
    #print(f"Device Scan Device IP: {ip}")
    for dict_found in [x for x in scan_results if x['id'] == value['gwId']]:
        value['name'] = dict_found['name']
        value['key'] = dict_found['key']
        device_node = device_id
        print(f"device_node: {device_node}")
        if device_node is None:
            print(f"Adding Node: {device_id} - {dict_found['name']}")
            print("Node Name {}".format(value['name']))
            print("Node key {}".format(value['key']))
            print("Node id {}".format(value['gwId']))
            print("Node ip {}".format(value['ip']))
            time.sleep(3)
            tuya_device = tinytuya.BulbDevice(
                value['gwId'], value['ip'], value['key'])
            node_status = tuya_device.status()
            print(node_status)
            print("Node Status {}".format(str(node_status)))
            # print(node_status)
            # tuya_device.set_version(3.3)"""


"""def Merge(data1, data):
    return (data1.update(data))


jData = (data)
print(Merge(data1, data))
df = pd.json_normalize(jData)  # jsonData['devices'])
# df = pd.read_json(jsondata)
df = df.fillna(-1)
print('devices')
print(df)
df['type'] = None

try:
    df['type'] = np.where(
        df['devId.dps.20'] != -1, 'light', df['type'])
except:
    pass
try:
    df['type'] = np.where(
        df['devId.dps.1'] != -1, 'switch', df['type'])
except:
    pass
try:
    df['type'] = np.where(df['dps.dps.101'] != -1, 'tuya', df['type'])
except:
    pass

lights = df[df['type'] == 'light'].reset_index(drop=True)
print(lights)
switches = df[df['type'] == 'switch'].reset_index(drop=True)
tuya = df[df['type'] == 'tuya'].reset_index(drop=True)

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

"""current = {
    "timestamp": 1667867832.176747,
    "devices": [
        {
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
        },
        {
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
                    "20": False,
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
                    "20": False,
                    "21": "colour",
                    "22": 10,
                    "23": 1000,
                    "24": "00000000000a",
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
# current = {'timestamp': time.time(), 'devices': polling}
output1 = json.dumps(current, indent=4)  # indent=4
print(type(output1))
print(output1)"""
