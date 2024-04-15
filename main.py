import time
from time import sleep

from vid import start as vid_start
from check_info import check_score
from read import start as read_start
from quiz_every_day import start as eq_start
from ints_quiz import start as ints_start
from driver import driver
from local_channel import start as local_start

last_exception_time = None


def main():
    global last_exception_time
    try:
        start()
    except Exception as e:
        if last_exception_time is not None:
            if time.time() - last_exception_time < 60:
                return
        last_exception_time = time.time()
        print(e)
        sleep(10)
        main()
    driver.quit()


def start():
    while True:
        result = check_score()
        print(result['我要选读文章'])
        if result['我要选读文章'] < 12:
            read_start(12 - result['我要选读文章'])
            sleep(1)
        if result['我要视听学习'] < 12:
            vid_start(12 - result['我要视听学习'])
            sleep(1)
        if result['每日答题'] < 5:
            eq_start()
        if result['趣味答题'] < 8:
            ints_start()
        if result['本地频道'] != 1:
            local_start()
        if result['我要选读文章'] + result['我要视听学习'] + result['每日答题'] + result['趣味答题'] >= 36:
            return "All Done!"
        print(result)


if __name__ == '__main__':
    main()
