from driver import driver
import random


def perform_swipe_down(dist, duration=random.randint(100, 600)):
    """
    向下滑动TODO:让数据更合法
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
    xy["end_y"] = int(window_size['height'] / 3)
    xy["start_y"] = int(xy["end_y"] + dist)
    xy = correct_number(xy)
    driver.swipe(xy["start_x"], xy["start_y"], xy["end_x"], xy["end_y"], duration)


def correct_number(number):
    """
    修正数字
    :param number:
    :return:
    """

    while number["start_x"] > driver.get_window_size()['width']:
        number["start_x"] -= 10
    while number["start_y"] > driver.get_window_size()['height']:
        number["start_y"] -= 10
    while number["end_x"] > driver.get_window_size()['width']:
        number["end_x"] -= 10
    while number["end_y"] > driver.get_window_size()['height']:
        number["end_y"] -= 10
    return number
