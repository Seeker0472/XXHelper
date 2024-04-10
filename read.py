import random
import time

from appium.webdriver.common.appiumby import AppiumBy
import sqlite3

from selenium.webdriver.common.by import By

import swipe
from driver import driver
import normarize

conn = sqlite3.connect("main.sqlite")
cur = conn.cursor()


def start():
    """
    开始
    :return:
    """
    normarize.to_normal()
    select_article()


def select_article():
    """
    遍历界面上的文章,调用try_article尝试读文章
    :return:
    """
    time_total = 0
    while time_total <= 60 * 15:
        elements = driver.find_elements(by=By.XPATH,
                                        value="//android.widget.ListView/android.widget.FrameLayout")
        for item in elements:
            try:
                text = item.find_element(by=By.XPATH,
                                         value="./android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView").text
            except:
                continue
            time_total += try_article(item, text)
            print(text)
        swipe.perform_swipe_down(500)


def try_article(item, text):
    sleep_time = 60 * 3
    time_now = str(time.strftime('%Y-%m-%d', time.localtime(time.time())))
    times = cur.execute("select COUNT(*) from Read where title=?", (text,)).fetchall()[0][0]
    if times != 0:
        return 0
    cur.execute("insert into Read (title,time) values (?,?)", (text, time_now))
    conn.commit()
    item.click()
    time.sleep(5)
    if is_video():
        driver.back()
        return 0
    # time.sleep(sleep_time)
    fake_swipe(sleep_time)
    driver.back()
    return sleep_time


def fake_swipe(sleep_time):
    """
    模拟滑动
    :param slee_time:
    :return:
    """
    while sleep_time > 0:
        rand = random.randint(0, 30)
        swipe.perform_swipe_down(random.randint(-100, 300))
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
    except:
        return False
    pass
