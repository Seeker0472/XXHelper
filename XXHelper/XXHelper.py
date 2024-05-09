from .General.appium_service import start as appium_start
from time import sleep

# TODO:优化代码结构
#TODO: Catch NoSuchElementException,重新启动程序
appium_start()
sleep(2)

import time

import atexit

from selenium.common import WebDriverException

from .Modules.vid import start as vid_start
from .General.check_info import check_score
from .Modules.read import start as read_start
from .Modules.Question.quiz_every_day import start as eq_start
from .Modules.Question.ints_quiz import start as ints_start
from .General.driver import driver
from .Modules.local_channel import start as local_start
from .Modules.subscribe import start as sub_start
from .Modules.comment import start as comment_start
from .Modules.send_msg import start as send_msg_start

last_exception_time = None


def main():
    global last_exception_time
    while True:
        try:
            if start() == 0:
                break
        except Exception as e:
            if last_exception_time is not None:
                if time.time() - last_exception_time < 60:
                    print("短期内连续两次异常,退出")
                    print(e)
                    return
            last_exception_time = time.time()
            print(e)
            sleep(10)


def start():
    sleep(5)
    change = False
    while True:
        change = False
        result = check_score()
        print(result)
        if result['每日答题'] < 5:
            change = True
            eq_start()
            sleep(1)
        if result['趣味答题'] < 8:
            # if result['趣味答题'] < 8 or True:
            change = True
            ints_start()
            sleep(1)
        if result['我要选读文章'] < 12:
            change = True
            read_start(12 - result['我要选读文章'])
            sleep(1)
        if result['我要视听学习'] < 12:
            change = True
            vid_start(12 - result['我要视听学习'])
            sleep(1)
        if result['本地频道'] != 1:
            change = True
            local_start()
            sleep(1)
        if result['订阅'] != 2:
            change = True
            sub_start(2 - result['订阅'])
            sleep(1)
        if result['发表观点'] != 1:
            change = True
            comment_start()
            sleep(1)
        if not change:
            send_msg_start()
            return 0


def exit_handler():
    # TODO:WTF??
    try:
        driver.terminate_app('cn.xuexi.android')
    except WebDriverException as e:
        pass
    driver.quit()
    print("exit normally")


if __name__ == '__main__':
    atexit.register(exit_handler)
    main()