import random
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

from ..General.driver import driver
from ..General import normarize, swipe


def start(lasting_time=12):
    """
    开始,进入视频学习,然后调用flashing()刷视频
    :return:
    """
    # 降低10次音量
    for i in range(10):
        driver.press_keycode(25)
    normarize.to_bai_ling()
    # vid_list = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
    #                                value="new UiSelector().className(\"android.widget.ListView\")")
    vid_list = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                   value="new UiSelector().className(\"androidx.recyclerview.widget.RecyclerView\")")
    child_elements = vid_list.find_elements(By.XPATH,
                                            "./androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout")
    child_elements[1].click()
    sleep(2)
    flashing(lasting_time)


def flashing(lasting_time):
    """
    定时划到下一个视频
    :return:
    """
    # 随机化时间
    lasting_time += random.randint(1, 4)
    print("开始刷视频,总共会执行 " + str(lasting_time * 2 + 2) + " 次模拟滑动")
    for i in range(lasting_time * 2):
        conti()
        sleep(30 + random.randint(-10, 10))
        print("正在执行第 " + str(i) + " 次模拟滑动")
        # swipe.perform_swipe_down(500, 500)
        swipe.perform_swipe_down_percent(40, 500)


def conti():
    """
    如果弹出流量提示,点击继续播放
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"继续播放\")").click()
    except:
        pass
