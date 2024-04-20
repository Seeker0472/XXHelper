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


def start(lasting_time=12):
    """
    开始
    :return:
    """

    normarize.to_normal()
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
            try:
                text = item.find_element(by=By.XPATH,
                                         value="./android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.TextView").text
            except Exception as e:
                print(e)
                continue
            time_total += try_article(item, text)
            print(text)
        swipe.perform_swipe_down(500)
        time.sleep(1)


def try_article(item, text):
    print(text)
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
        print("剩余时间:", sleep_time)
        rand_swipe = random.randint(200, 400) * random.choice([-1, 1])
        # swipe.perform_swipe_down(random.randint(-100, 300))
        swipe.perform_swipe_down(rand_swipe)
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


def quit_bookshelf():
    """
    退出书架
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"取消\")").click()
    except:
        pass
