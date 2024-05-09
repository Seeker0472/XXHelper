import subprocess
import os
from time import sleep


def start():
    start_adb()
    sleep(5)
    subprocess.Popen('start appium', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def start_adb():
    os.system('adb connect 192.168.2.123:5555')


