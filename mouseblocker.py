from pynput import keyboard
import subprocess
from threading import Timer
import json
import os


def find_path():
    global path
    path = f'./'


def load_device_id():
    global device_id
    global ban_time
    with open(f'{path}\\Device_PID_VID.json', newline='') as jsonfile:
        data = json.load(jsonfile)
        device_id = data['device_id']
        ban_time = data['ban_time']


def setting_timer():
    ##print("Setting Timer")
    global t
    t = Timer(ban_time, turn_on_device)


def Timer_start():
    if t.is_alive():
        #print("Timer reseted")
        t.cancel()
        setting_timer()
    else:
        CREATE_NO_WINDOW = 0x08000000
        subprocess.run(
            f'{path}\\devcon.exe disable "{device_id}"', creationflags=CREATE_NO_WINDOW)
    t.start()
    #print("Timer started")


def on_press(key):
    Timer_start()


def turn_on_device():
    DETACHED_PROCESS = 0x00000008
    subprocess.run(
        f'{path}\\devcon.exe enable "{device_id}"', creationflags=DETACHED_PROCESS)
    setting_timer()


if __name__ == '__main__':
    find_path()
    load_device_id()
    setting_timer()
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press) as listener:
        listener.join()
