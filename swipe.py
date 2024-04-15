from driver import driver
import random


def perform_swipe_down(dist, duration=random.randint(100, 600)):
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
    start_x = int(window_size['width'] / 2)+random.randint(0, 50)
    end_x = int(window_size['width'] / 2)+random.randint(-50, 20)
    start_y = int(window_size['height'] / 3)
    driver.swipe(start_x, start_y+dist, end_x, start_y, duration)
