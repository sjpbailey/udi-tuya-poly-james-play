import requests
import time
import hmac
import hashlib
import json
import pprint
import logging
import tinytuya


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
    print(response)
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
print(bold + 'TinyTuya Setup Wizard' + dim +
      ' [%s]' % (tinytuya.version) + normal)
print('')

if (config['apiKey'] != '' and config['apiSecret'] != '' and
        config['apiRegion'] != '' and config['apiDeviceID'] != ''):
    needconfigs = False
    # Second Message
    print("    " + subbold + "Existing settings:" + dim +
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
    print(f"RESPONSE DICT : {response_dict}")
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
    print("\n\n" + bold + "Device Listing\n" + dim)
    output = json.dumps(tuyadevices, indent=4)  # sort_keys=True)
    print(output)
    print('Add DPS sorter here')
#### Add device sorter here ####
    """# Save list to devices.json
    print(bold + "\n>> " + normal + "Saving list to " + DEVICEFILE)
    with open(DEVICEFILE, "w") as outfile:
        outfile.write(output)
    print(dim + "    %d registered devices saved" % len(tuyadevices))

    # Save raw TuyaPlatform data to tuya-raw.json
    print(bold + "\n>> " + normal +
          "Saving raw TuyaPlatform response to " + RAWFILE)
    try:
        with open(RAWFILE, "w") as outfile:
            outfile.write(json.dumps(json_data, indent=4))
    except:
        print('\n\n' + bold + 'Unable to save raw file' + dim)"""
