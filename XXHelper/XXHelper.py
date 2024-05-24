import threading
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
    atexit.register(exit_handler)
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
            # eq_start()
            start_thread(eq_start, 60*5, ())
            sleep(1)
        if result['趣味答题'] < 8:
            # if result['趣味答题'] < 8 or True:
            change = True
            # ints_start()
            start_thread(ints_start, 60*5, ())
            sleep(1)
        if result['我要选读文章'] < 12:
            change = True
            # read_start(12 - result['我要选读文章'])
            start_thread(read_start, 60*15, (12 - result['我要选读文章'],))
            sleep(1)
        if result['我要视听学习'] < 12:
            change = True
            # vid_start(12 - result['我要视听学习'])
            start_thread(vid_start, 60*15, (12 - result['我要视听学习'],))
            sleep(1)
        if result['本地频道'] != 1:
            change = True
            # local_start()
            start_thread(local_start, 60*5, ())
            sleep(1)
        if result['订阅'] != 2:
            change = True
            # sub_start(2 - result['订阅'])
            start_thread(sub_start, 60*5, (2 - result['订阅'],))
            sleep(1)
        if result['发表观点'] != 1:
            change = True
            # comment_start()
            start_thread(comment_start, 60*3, ())
            sleep(1)
        if not change:
            # send_msg_start()
            start_thread(send_msg_start, 60*3, ())
            return 0

def start_thread(function,timeout,args):
    """
    :param function: 需要执行的函数
    :param timeout: 超时(秒)
    :param args: 参数
    :return:
    """
    class FuncThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = None
            self.exception = None

        def run(self):
            try:
                self.result = function(*args)
            except Exception as e:
                self.exception = e

    thread=FuncThread()
    thread.run()
    thread.join(timeout=timeout)
    if thread.is_alive():
        thread.terminate()
        raise TimeoutError("线程超时")
    if thread.exception is not None:
        raise thread.exception


def exit_handler():
    # TODO:WTF??
    try:
        driver.terminate_app('cn.xuexi.android')
    except WebDriverException as e:
        pass
    driver.quit()
    print("exit normally")


if __name__ == '__main__':
    main()
