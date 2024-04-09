from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

from driver import driver
import swipe
import normarize


def start():
    """
    开始,进入视频学习,然后调用flashing()刷视频
    :return:
    """
    normarize.to_bai_ling()
    vid_list = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                   value="new UiSelector().className(\"android.widget.ListView\")")
    child_elements = vid_list.find_elements(By.XPATH, "./android.widget.ListView/android.widget.FrameLayout")
    child_elements[1].click()
    sleep(2)
    flashing()


def flashing():
    """
    定时划到下一个视频
    :return:
    """
    for i in range(30):
        conti()
        sleep(30)
        swipe.perform_swipe_down(500, 600)


def conti():
    """
    如果弹出流量提示,点击继续播放
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"继续播放\")").click()
    except:
        pass