import json
import sys


def identify_sys():
    system = sys.platform
    if system == 'linux':
        with open('setting/config.json', 'r') as f:
            msg = json.loads(f.read())
            if not msg['message']:
                raise Exception(r'Your msg in setting\config.json is empty')
            return msg
    else:
        with open(r'setting\config.json', 'rb') as f:
            msg = json.loads(f.read())
            if not msg['message']:
                raise Exception(r'Your msg in setting\config.json is empty')
            return msg


message = {
    "msg": identify_sys()['message']
}


def get_username():
    username = input("Enter your INSTAGRAM username : ")

    if username:
        return username

    print('Please enter your INSTAGRAM username')
    return get_username()


def get_password():
    password = input("Enter your INSTAGRAM password : ")

    if password:
        return password

    print('Please enter your INSTAGRAM password')
    return get_password()


information = {"USERNAME": get_username(), "PASSWORD": get_password()}
