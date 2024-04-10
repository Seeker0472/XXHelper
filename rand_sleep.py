import time
import random


def sleep_more_tan(sec):
    """
    休眠时间
    :param sec: 休眠时间
    :return:
    """
    rand_sec = random.randrange(0, sec/10)
    time.sleep(rand_sec)
    return rand_sec
