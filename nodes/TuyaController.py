import udi_interface
import tinytuya
import json
import time
import ast
import pandas as pd
import numpy as np

from nodes import TuyaNode
from nodes import tuya_light_node
from nodes import tuya_switch_node

# IF you want a different log format than the current default
LOGGER = udi_interface.LOGGER
Custom = udi_interface.Custom


class TuyaController(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name):
        super(TuyaController, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.name = name
        self.primary = primary
        self.address = address
        self.n_queue = []

        self.Notices = Custom(polyglot, 'notices')
        self.Parameters = Custom(polyglot, 'customparams')

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.STOP, self.stop)
        self.poly.subscribe(self.poly.CUSTOMPARAMS, self.parameter_handler)
        self.poly.subscribe(self.poly.ADDNODEDONE, self.node_queue)

        self.poly.ready()
        self.poly.addNode(self)

    def node_queue(self, data):
        self.n_queue.append(data['address'])

    def wait_for_node_event(self):
        while len(self.n_queue) == 0:
            time.sleep(0.1)
        self.n_queue.pop()

    def parameter_handler(self, params):
        self.Notices.clear()
        self.Parameters.load(params)
        # self.check_params()

    def start(self):
        LOGGER.info('Staring Tuya NodeServer')
        self.poly.updateProfile()
        self.poly.setCustomParamsDoc()
        self.discover()

    # def query(self, command=None):
    #    LOGGER.info("Query sensor {}".format(self.address))
        # self.discover()

    def discover(self, *args, **kwargs):
        LOGGER.info("Starting Tuya Device Discovery")
        devices_list = json.loads(self.Parameters['devices'])

        LOGGER.info(json.dumps(devices_list))
        scan_results = tinytuya.deviceScan(False, 20)

        for value in scan_results.values():
            ip = value['ip']
            device_id = value['gwId']
            if len(device_id) > 10:
                device_id = device_id[:10]

            #LOGGER.info(f"Device Scan Device IP: {ip}")
            for dict_found in [x for x in devices_list if x["id"] == value['gwId']]:
                value['name'] = dict_found['name']
                value['key'] = dict_found['key']
                device_node = self.poly.getNode(device_id)
                LOGGER.info(f"device_node: {device_node}")
                if device_node is None:
                    LOGGER.info(
                        f"Adding Node: {device_id} - {dict_found['name']}")
                    LOGGER.info("Node Name {}".format(value['name']))
                    LOGGER.info("Node key {}".format(value['key']))
                    LOGGER.info("Node id {}".format(value['gwId']))
                    LOGGER.info("Node ip {}".format(value['ip']))
                    time.sleep(3)
                    self.tuya_device = tinytuya.BulbDevice(
                        value['gwId'], value['ip'], value['key'])
                    self.tuya_device.set_version(3.3)

                    # HERE DPS
                    node_status = self.tuya_device.status()
                    LOGGER.info("Node Status {}".format(str(node_status)))
                    LOGGER.info(self.tuya_device + node_status)

                    """for i in node_status:  # )xfor i in node_status: gives dps devId)
                        LOGGER.info(i)

                    polling = []
                    print("LINE 143 Polling local devices...")
                    for i in node_status:
                        item = {}
                        name = i['name']
                        (ip, ver) = scan_results, i['gwId']
                        item['name'] = name
                        item['ip'] = ip
                        item['ver'] = ver
                        item['id'] = i['id']
                        item['key'] = i['key']
                        if (ip == 0):
                            pass
                        else:
                            try:
                                d = tinytuya.OutletDevice(
                                    i['id'], ip, i['key'])
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
                        current = {'timestamp': time.time(),
                                   'devices': polling}
                        output1 = json.dumps(current, indent=4)  # indent=4
                        LOGGER.info(f"LINE 196 Local Device json {output1}")"""

        # LOGGER.info(
        #    f"Adding Node: {device_id} - {dict_found['name']}")
        # self.poly.addNode(
        #    TuyaNode(self.poly, self.address, device_id, dict_found['name'], value))
        # self.wait_for_node_event()
        # works to read dict with single quotes
                    jsonData = json.dumps(+ str(node_status))
        #jsonData = json.dumps(str(node_status))
        #jsonData1 = json.loads(jsonData)
                    LOGGER.info(jsonData)
        # print(jsonData1)
        #jsonData = ast.literal_eval(jsonData)
        #df = pd.read_json(str(node_status))
        """df = pd.json_normalize(jsonData)  # jsonData['devices'])

        df.to_dict()
        df = df.fillna(-1)
        LOGGER.info('devices')
        LOGGER.info(df)
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
        LOGGER.info(lights)
        switches = df[df['type'] == 'switch'].reset_index(drop=True)
        LOGGER.info(switches)

        device_list = [lights]
        for device in device_list:
            for idx, row in device.iterrows():
                name = row['name']
                id = row['id']
                id_new = id
                ip = row['ip']
                key = row['key']
                ver = row['ver']
                #id_new = id
                address = row['type'] + '_%s' % (idx+1)
                LOGGER.info('{name}\n{id_new}\n{ip}\n{key}\n{ver}\n{address}\n'.format(
                    name=name, id_new=id_new, ip=ip, key=key, ver=ver, address=address,))
                node = tuya_light_node.LightNode(
                    self.poly, self.address, address, name, id_new, ip, key)
                self.poly.addNode(node)
                self.wait_for_node_done()

        device_list = [switches]
        for device in device_list:
            for idx, row in device.iterrows():
                name = row['name']
                id = row['id']
                id_new = id
                ip = row['ip']
                key = row['key']
                ver = row['ver']
                address = row['type'] + '_%s' % (idx+1)
                LOGGER.info('{name}\n{id_new}\n{ip}\n{key}\n{ver}\n{address}\n'.format(
                    name=name, id_new=id_new, ip=ip, key=key, ver=ver, address=address,))
                node = tuya_switch_node.SwitchNode(
                    self.poly, self.address, address, name, id_new, ip, key)
                self.poly.addNode(node)
                self.wait_for_node_done()"""

        LOGGER.info('Finished Tuya Device Discovery')

    def delete(self):
        LOGGER.info('Deleting Tuya Node Server')

    def stop(self):
        nodes = self.poly.getNodes()
        for node in nodes:
            if node != 'controller':  # but not the controller node
                nodes[node].setDriver('ST', 0, True, True)
        self.poly.stop()
        LOGGER.info('Daikin Tuya stopped.')

    def query(self, command=None):
        LOGGER.info("Query sensor {}".format(self.address))

    id = 'tuya'
    commands = {
        'QUERY': query,
        'DISCOVER': discover
    }

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2}
    ]
