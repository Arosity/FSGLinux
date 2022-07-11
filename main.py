#! /usr/bin/env python3


# from pynput.keyboard import Key, Controller
from pynput import keyboard as kk
import time
import findseed as getseed
import json
keyboard = kk.Controller()

keys={
    'esc':kk.Key.esc,
    'tab':kk.Key.tab,
    'enter':kk.Key.enter,
    'f10':kk.Key.f10,
    'alt':kk.Key.alt
}
settings=json.load(open('settings.json'))
sdel=settings['delay']/1000
rkey=keys[settings['hotkey']]

def resetworld(s):
    print("[+] Resetting World")
    global sdel
    global rkey
    global x
    
    rk=[
        'esc',
        'tab',
        'tab',
        'tab',
        'tab',
        'tab',
        'tab',
        'tab',
        'tab',
        'tab',
        'enter',
    ]
    rk1=[
        'tab',
        'enter',
        'tab',
        'tab',
        'tab',
        'enter',
        'tab',
        'tab',
        'enter',
        'enter',
        'enter',
        'tab',
        'tab',
        'tab',
        'tab',
        'enter',
        'tab',
        'tab',
        'tab',
    ]
    rk2=[
        'tab',
        'tab',
        'tab',
        'tab',
        'tab',
        'tab',
        'enter'
    ]
    for i in rk:
        keyboard.press(keys[i])
        time.sleep(sdel/2)
        keyboard.release(keys[i])
        time.sleep(sdel/2)
    time.sleep(1)
    for i in rk1:
        keyboard.press(keys[i])
        time.sleep(sdel/2)
        keyboard.release(keys[i])
        time.sleep(sdel/2)
    keyboard.type(s)
    
    for i in rk2:
        keyboard.press(keys[i])
        time.sleep(sdel/2)
        keyboard.release(keys[i])
        time.sleep(sdel/2)
        
print("[+] Starting Listener")
seed=getseed.run()
x=1
def on_release(key):
    global seed
    global x
    if key==rkey:
        if x==1:
            x=0
            resetworld(seed)
            seed=getseed.run()
            x=1
with kk.Listener(
    on_release=on_release) as listener:
    listener.join()