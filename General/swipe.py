from time import sleep

from selenium.common import InvalidElementStateException

from driver import driver
import random


def perform_swipe_down(dist, duration=random.randint(300, 600)):
    """
    执行向下滑动,如果出现异常(在运行速度较慢的设备上连续滑动可能会触发)则等待3秒后再次尝试
    :param duration:
    :param dist:
    :return:
    """
    try:
        down_swipe(dist, duration)
    except InvalidElementStateException:
        sleep(3)
        down_swipe(dist, duration)


def perform_swipe_down_percent(percent, duration=random.randint(400, 600)):
    """
    执行向下滑动,按照屏幕百分比
    :param duration:
    :param percent:
    :return:
    """
    if percent > 100 or percent < -100:
        raise ValueError("滑动的百分比应该在 [-100,100] 之间")
    perform_swipe_down(driver.get_window_size()['height'] * percent / 100, duration)


def down_swipe(dist, duration=random.randint(300, 600)):
    """
    向下滑动
    :param dist:
    :param duration:
    :return:
    """
    window_size = driver.get_window_size()
    dist = dist + random.randint(-50, 50)
    duration = duration + random.randint(-300, 300)
    while duration < 0:
        duration += 100
    xy = {}
    xy["start_x"] = int(window_size['width'] / 2) + random.randint(0, 50)
    xy["end_x"] = int(window_size['width'] / 2) + random.randint(-50, 20)
    xy["end_y"] = end_y = int(window_size['height'] / 3)
    xy["start_y"] = int(end_y + dist)
    xy = correct_number(xy)
    # TODO:catch  io.appium.uiautomator2.common.exceptions.InvalidElementStateException: Unable to perform W3C actions. Check the logcat output for possible error reports and make sure your input actions chain is valid.
    driver.swipe(xy["start_x"], xy["start_y"], xy["end_x"], xy["end_y"], duration)


def correct_number(number):
    """
    修正数字
    :param number:
    :return:
    """
    # TODO:减去底部和顶部侧边栏
    while number["start_x"] > driver.get_window_size()['width']:
        number["start_x"] -= 10
    while number["start_y"] > driver.get_window_size()['height']:
        number["start_y"] -= 10
    while number["end_x"] > driver.get_window_size()['width']:
        number["end_x"] -= 10
    while number["end_y"] > driver.get_window_size()['height']:
        number["end_y"] -= 10
    return number
