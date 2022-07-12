#! /usr/bin/env python3


from pynput import keyboard as kk
import time
import findseed as getseed
import json
import shutil
import os
import random
import string

keyboard = kk.Controller()

keys = {
    'esc': kk.Key.esc,
    'tab': kk.Key.tab,
    'enter': kk.Key.enter,
    'f10': kk.Key.f10,
    'alt': kk.Key.alt
}
settings = json.load(open('settings.json'))
sdel = settings['delay']/1000
rkey = keys[settings['hotkey']]
worldfolder = settings['worldfolder']
movefolder = settings['movefolder']
ignorechar=settings['ignorechar']





def moveworlds():
    file_names = os.listdir(worldfolder)
    ext = ''.join(random.choices(string.ascii_uppercase, k=9))
    
    for file_name in file_names:
        if ignorechar not in file_name:
            if os.path.exists(movefolder + file_name):
                currentfile = os.path.join(worldfolder, file_name)
                file_name = os.path.join(worldfolder, file_name+ext)
                os.rename(currentfile, file_name)

            shutil.move(
                os.path.join(worldfolder, file_name),
                movefolder
            )


def resetworld(s):
    print("[+] Resetting World")
    global sdel
    global rkey
    global x

    rk = [
        'esc','tab','tab','tab','tab',
        'tab','tab','tab','tab','tab',
        'enter','pause','tab','enter','tab','tab',
        'tab','enter','tab','tab','enter',
        'enter','enter','tab','tab','tab',
        'tab','enter','tab', 'tab','tab','seed','tab','tab','tab','tab','tab','tab','enter'
    ]
    for i in rk:
        if i=="pause":
            time.sleep(1)
        elif i =="seed":
            keyboard.type(s)
        else:
            keyboard.press(keys[i])
            time.sleep(sdel/2)
            keyboard.release(keys[i])
            time.sleep(sdel/2)

    moveworlds()


print("[+] Starting Listener")
seed = getseed.run()
x = 1


def on_release(key):
    global seed
    global x
    if key == rkey:
        if x == 1:
            x = 0
            resetworld(seed)
            seed = getseed.run()
            x = 1


with kk.Listener(
        on_release=on_release) as listener:
    listener.join()