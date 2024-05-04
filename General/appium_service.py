import subprocess


def start():
    subprocess.Popen('start appium', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
