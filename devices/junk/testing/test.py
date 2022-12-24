import tinytuya
import json
import time
import operator
import json
import time
import pprint
import logging
import pandas as pd
import numpy as np


"""if dps == {'20'}:
                    self.poly.addNode(tuya_light_node.LightNode(
                        self.poly, self.address, address, name, id_new, ip, key))  # device_id,
                    self.wait_for_node_event()
                if dps == {'1'}:
                    self.poly.addNode(tuya_switch_node.SwitchNode(
                        self.poly, self.address, address, name, id_new, ip, key))
                    self.wait_for_node_event()
                if dps == {'101'}:
                    self.poly.addNode(TuyaNode(
                        self.poly, self.address, address, dict_found['name'], value))
                    self.wait_for_node_event()"""


# f = open('snapshot.json',)
# Work in Progress Here, needs to be a grab from the internal ip network for local addresses
# jsonData = [{"name": "Master Bedroom Outside", "ip": "192.168.1.126", "ver": "3.3", "id": "017743508caab5f126b0", "key": "17a1e4c963773637", "devId": {"devId": "017743508caab5f126b0", "dps": {"1": False, "9": 0}}}, {"name": "Garage", "ip": "192.168.1.148", "ver": "3.3", "id": "ebfd4f4263bb769d99zjkq", "key": "ec0b2b581a246eab", "devId": {"dps": {"20": False,
#                                                                                                                                                                                                                                                                                                                                                            "21": "white", "22": 10, "23": 1000, "24": "002501b603b5", "25": "000d0d0000000000000000180000", "26": 0}}}, {"name": "Office Light", "ip": "192.168.1.147", "ver": "3.3", "id": "ebfc16d57ed374932cjqfk", "key": "805217605357161b", "devId": {"dps": {"20": False, "21": "white", "22": 10, "23": 1000, "24": "002501b603b5", "25": "000d0d0000000000000000180000", "26": 0}}}, {"name": "Backyard Flood Light", "ip": "192.168.86.6", "ver": "3.3", "id": "ebd85577fae5b9605cpvpi", "key": "fef7d468e4d01d28", "dps": {"dps":  {"101": "AUTO", "104": "MEDIUM",  "105": "5MIN", "106": False, "107": "1000", "110": "true", "111": True}}}]
"""scan_results = tinytuya.deviceScan()
for value in scan_results.values():  # scan_results.values():
    print(value)
    dps = value['gwId']
    #name = value['name']
    ip = value['ip']
    key = value['productKey']
    device_id = value['gwId']
    device = device_id
    device_node = device_id
    # print(
    #    f"ID: {value['gwId']} - KEY {value['productKey']} IP: {value['ip']} ")
for key in scan_results.values():  # scan_results.values():
    #print(f"key: {key}")
    pass

# if len(device_id) > 10:
#    device_id = device_id[:10]
# for i in device_id:
#    print(f"Adding Node: {i}")

# if device_node is None:
tuya_device = tinytuya.BulbDevice(
    value['gwId'], value['ip'], value['productKey'], )  # value['devId'], value['devId']['dps'],
# self.device['gwId'], self.device['ip'], self.device['key'])
# print(tuya_device)

tuya_device.set_version(3.3)
# , {dict_found['dps']}
for i in tuya_device:
    print(f"tuya devices: {i}")
    pass
else:
    print("excues Me, Huu?")

for i in {device_id}:
    #print(f"New Node: {i}")
    pass
else:
    print("excues Me, What?")


print(
    f"Adding Node: 'ID' {device_id} - 'IP' {value['ip']}")"""


####### SORTS WITH JSON ##########
jsonData = [{"name": "Master Bedroom Outside", "ver": "3.3", "id": "017743508caab5f126b0",
            "key": "17a1e4c963773637", "devId": {"devId": "017743508caab5f126b0", "dps": {"1": True, "9": 0}}}, {"name": "Garage", "ip": "192.168.1.148", "ver": "3.3", "id": "ebfd4f4263bb769d99zjkq", "key": "ec0b2b581a246eab", "devId": {"dps": {"20": False,
                                                                                                                                                                                                                                                     "21": "white", "22": 10, "23": 1000, "24": "002501b603b5", "25": "000d0d0000000000000000180000", "26": 0}}}, ]
# Append
scan_results = tinytuya.deviceScan()

for value in scan_results.values():  # scan_results.values():
    ip = value['ip']
    dps = value['gwId']
    device_id = value['gwId']
    device = device_id

# if len(device_id) > 10:
#    device_id = device_id[:10]

#print(f"Device Scan Device IP: {ip}, {dps}")
for dict_found in [x for x in jsonData if x["id"] == value['gwId']]:
    value['name'] = dict_found['name']
    value['key'] = dict_found['key']
    device_node = device_id

    if device_node is None:
        tuya_device = tinytuya.BulbDevice(
            value['name'], value['id'], value['ip'], value['key'], value['devId'], value['devId']['dps'],)
        # self.device['gwId'], self.device['ip'], self.device['key'])
        print(tuya_device)
        tuya_device.set_version(3.3)
        # , {dict_found['dps']}
print(
    f"Adding Node: {device_id} - {value['ip']}")
# f"Adding Node: {device_id} - {value['name']}, {value['key']}, {value['id']}, {value['ip']}, {value['devId']['dps']},")

# jsonData = json.load(f)
for i in jsonData:
    # pass
    print(i)

# add string here for devices instead of jsonfile only for names
df = pd.json_normalize(jsonData)  # jsonData
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
# print(lights)
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

# This is to grab devices and NAME,
#devices = tinytuya.deviceScan(False, 20)
# print(devices)
# print("")


"""def getIP(d, gwid):
    for ip in d:
        if 'gwId' in d[ip]:
            if (gwid == d[ip]['gwId']):
                return (ip, d[ip]['version'])
    return (0, 0)


#### custom parameters ####
jsonData = [{"name": "Master Bedroom Outside", "ver": "3.3", "id": "017743508caab5f126b0",
            "key": "17a1e4c963773637", "devId": {"devId": "017743508caab5f126b0", "dps": {"1": True, "9": 0}}}, {"name": "Garage", "ip": "192.168.1.148", "ver": "3.3", "id": "ebfd4f4263bb769d99zjkq", "key": "ec0b2b581a246eab", "devId": {"dps": {"20": False,
                                                                                                                                                                                                                                                     "21": "white", "22": 10, "23": 1000, "24": "002501b603b5", "25": "000d0d0000000000000000180000", "26": 0}}}, ]

scan_results = tinytuya.deviceScan()
for value in scan_results.values():  # scan_results.values():
    ip = value['ip']
    dps = value['gwId']
    device_id = value['gwId']
    device = device_id
# if len(device_id) > 10:
#    device_id = device_id[:10]

#print(f"Device Scan Device IP: {ip}, {dps}")
for dict_found in [x for x in jsonData if x["id"] == value['gwId']]:
    value['name'] = dict_found['name']
    value['key'] = dict_found['key']
    device_node = device_id
    print(value['name'])
    for i in value['name']:
        print(i)
# Append

#print(f"Device Scan Device IP: {ip}, {dps}")
    if device_node is None:
        tuya_device = tinytuya.BulbDevice(
            value['name'], value['id'], value['ip'], value['key'], value['devId'], value['devId']['dps'],)
        # self.device['gwId'], self.device['ip'], self.device['key'])
        print(tuya_device)
        tuya_device.set_version(3.3)

    tuyadevices = []
    for i in jsonData['result']:
        item = {}
        item['name'] = i['name'].strip()
        item['id'] = i['id']
        item['key'] = i['local_key']
        tuyadevices.append(item)

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
                  (name, ip, ))

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
            polling.append(item)"""
