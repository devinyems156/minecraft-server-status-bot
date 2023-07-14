import json
import os


def readjson(name, home_folder=''):
    try:
        with open(home_folder + name, 'r') as f:
            value = json.load(f)
            return value
    except json.decoder.JSONDecodeError:
        print('JSONDecodeError: file data is too short or file is empty')
    except FileNotFoundError:
        print('FileNotFoundError: no such file')


def writejson(name, value, home_folder='', abs=False):
    if abs:
        self_file = __file__
        own_path = ''
        for i in self_file.split(sep='\\')[:-1]:
            own_path = own_path + i + '/'
        print(own_path)
        home_folder = own_path + home_folder
    print(home_folder)
    if not home_folder == '':
        os.makedirs(name=home_folder, exist_ok=True),
    with open(home_folder + name, 'w') as f:
        json.dump(value, f, indent=4)


default = {
    'token': 'ENTER_YOUR_TOKEN_HERE',
    'time': 60,
    'ip': 'game1.falixserver.net:63546',
    'channel_id': 1129045123955703871,
    'embed_color': 0x75a4c3,
    'message_id':  None,
    'timezone_offset': 3,
    'log_channel_id': 1129084586169733220
}


def getdata():
    info = readjson('info.json')
    if not info:
        writejson('info.json', default)
        info = readjson('info.json')
    return info


def senddata(data):
    writejson('info.json', data)


