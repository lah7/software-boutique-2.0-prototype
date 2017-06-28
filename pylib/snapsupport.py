#!/usr/bin/python3

import getpass
import gi
import json
import os
import sys
gi.require_version ('Snapd', '1')
from gi.repository import Snapd

def progress_snap_cb (client, change, deprecated, user_data):
    # Interate over tasks to determine the aggregate tasks for completion.
    print(change)


def load_auth_data():
    if os.path.exists(os.path.join(os.path.expanduser('~'),'.deleteme')):
        with open(os.path.join(os.path.expanduser('~'),'.deleteme')) as stream:
            auth_data = json.load(stream)
        macaroon = auth_data['macaroon']
        discharges = auth_data['discharges']
        auth_data = Snapd.AuthData.new(macaroon, discharges)
        print(auth_data)
    else:
        auth_data = None

    return auth_data

def save_auth_data(auth_data):
    #print(auth_data)

    macaroon = Snapd.AuthData.get_macaroon(auth_data)
    discharges = Snapd.AuthData.get_discharges(auth_data)
    data = {'macaroon': macaroon,
            'discharges': discharges}
    #if os.access(os.path.join(os.path.expanduser('~'),'.deleteme'), os.W_OK):
    f = open(os.path.join(os.path.expanduser('~'),'.deleteme'), "w+")
    f.write(json.dumps(data))
    f.close()
    #else:
    #    print('Doh!')


def snap_login():
    username = input('Username:')
    password = getpass.getpass(prompt='Password:')

    try:
        auth_data = Snapd.login_sync(username, password, None)
    except Exception as e:
        if e.domain == 'snapd-error-quark' and e.code == Snapd.Error.TWO_FACTOR_REQUIRED:
            otp = input('OTP:')
            try:
                auth_data = Snapd.login_sync(username, password, otp)
            except:
                return None
        else:
            return None

    client.set_auth_data(auth_data)
    save_auth_data(auth_data)
    return True
    
#@snap_login
def snap_install(snapname):
    print("Installing")
    client.install_sync(snapname,
                        None, # channel
                        progress_snap_cb, (None,),
                        None) # cancellable


#@snap_login
def snap_remove(snapname):
    print("Removing")
    client.remove_sync(snapname,
                       progress_snap_cb, (None,),
                       None) # cancellable

client = Snapd.Client()
client.connect_sync()

auth_data = load_auth_data()
if auth_data:
    client.set_auth_data(auth_data)    
else:
    snap_login()
    
#snap_install('moon-buggy')
snap_remove('moon-buggy')