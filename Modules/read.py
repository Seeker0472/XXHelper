import random
import time

from appium.webdriver.common.appiumby import AppiumBy
import sqlite3

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from General.driver import driver
from General import normarize, swipe

import os
#
# # 获取上一层目录的绝对路径
# parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.curdir))
# print(os.path.join(parent_dir, 'main.sqlite'))
# # 连接数据库
# # conn = sqlite3.connect(os.path.join(parent_dir, 'main.sqlite'))

conn = sqlite3.connect("./main.sqlite")
cur = conn.cursor()


def start(lasting_time=12):
    """
    开始
    :return:
    """

    normarize.to_recommend()
    select_article(lasting_time)


def select_article(lasting_time):
    """
    遍历界面上的文章,调用try_article尝试读文章
    :return:
    """
    time_total = 0
    while time_total <= lasting_time * 65:
        # elements = driver.find_elements(by=By.XPATH,
        #                                 value="//android.widget.ListView/android.widget.FrameLayout")
        elements = driver.find_elements(by=By.XPATH,
                                        value="//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout")
        for item in elements:
            # 如果时间超过,则退出
            if time_total > lasting_time * 65:
                break
            try:
                text = item.find_element(by=By.XPATH,
                                         value="./android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView").text
            except NoSuchElementException as e:
                continue
            if lasting_time == 12:
                time_total += try_article(item, text, lasting_time - time_total / 60, 60 * 7)
            else:
                time_total += try_article(item, text, lasting_time - time_total / 60, random.randint(60 * 1, 60 * 2))
            # print(text)
        swipe.perform_swipe_down_percent(20)
        time.sleep(1)


def try_article(item, text, time_total_left, sleep_time=60 * 3):
    time_now = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    times = cur.execute("select COUNT(*) from Read where title=?", (text,)).fetchall()[0][0]
    # 如果读过这篇文章,则跳过
    if times != 0:
        print("已经读过的文章: " + text)
        return 0
    cur.execute("insert into Read (title,time) values (?,?)", (text, time_now))
    conn.commit()
    item.click()
    time.sleep(10)
    if is_video():
        print("检测到视频: " + text)
        driver.back()
        return 0
    print("剩余总时间(min): " + str(time_total_left) + "开始阅读: " + text)
    fake_swipe(sleep_time)
    driver.back()
    quit_bookshelf()
    return sleep_time


def fake_swipe(sleep_time):
    """
    模拟滑动
    :param sleep_time:
    :return:
    """
    while sleep_time > 0:
        rand = random.randint(0, 30)
        print("执行模拟滑动,这篇文章的剩余时间:", str(sleep_time))
        rand_swipe = random.randint(10, 20) * random.choice([-1, 1])
        # swipe.perform_swipe_down(random.randint(-100, 300))
        swipe.perform_swipe_down_percent(rand_swipe)
        sleep_time -= rand
        time.sleep(rand)


def is_video():
    """
    判断是否是视频
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"播放\")")
        return True
    except NoSuchElementException:
        return False
    pass


def quit_bookshelf():
    """
    退出书架
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"取消\")").click()
    except NoSuchElementException:
        pass
