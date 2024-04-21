from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import swipe
from driver import driver


def to_normal():
    """
    返回首页
    :return:
    """
    for i in range(9):
        if exist_main_button():
            break
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID,
                        value="学习").click()


def to_bai_ling():
    """
    进入百灵
    :return:
    """
    to_normal()
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID,
                        value="百灵").click()


def to_tv():
    """
    进入电视台
    :return:
    """
    to_normal()
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID,
                        value="电视台").click()


def exist_main_button():
    """
    判断是否在首页,如果不在首页则返回
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ACCESSIBILITY_ID,
                            value="学习")
        return True
    except:
        driver.back()
        sleep(1)
        try:
            driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                value="new UiSelector().text(\"退出\")").click()
        except:
            pass
        try:
            driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                value="new UiSelector().text(\"取消\")").click()
        except:
            pass
        return False


def to_sep_page(page_name, text):
    """
    进入指定页面
    :param text:
    :param page_name:
    :return:
    """
    to_normal()

    # 点击积分
    driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().resourceId("
                                                               "\"cn.xuexi.android:id/ll_comm_head_score\")").click()
    # sleep(2)
    # wait = WebDriverWait(driver, 20)  # 等待最多20秒

    # 等待页面加载完成
    WebDriverWait(driver, 10).until(lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                             "new UiSelector().text(\"已完成\").instance(0)"))

    proceed = None
    # 找到指定模块并点击进入
    while proceed is None:
        # 所有子节点(积分项)
        elements = (driver.find_elements(By.XPATH, '//android.widget.ListView')[0]
                    .find_elements(By.XPATH, './android.widget.ListView/android.view.View'))
        for item in elements:

            try:
                title = item.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
                print(title)
                if title != page_name:
                    continue
                score = item.find_element(by=By.XPATH, value="./android.view.View/android.view.View[4]").find_elements(
                    by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
                proceed = item.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value="new UiSelector().text(\"" + text + "\")")
                # if score > 4:
                #     return
            except:
                continue
            print(title, score)

        # 如果当前页没有找到趣味答题,则向下滑动
        if proceed is None or (driver.get_window_size()['height'] - proceed.location['y']) < driver.get_window_size()['height'] / 10:
            proceed = None
            # 按照屏幕高度的5%向下滑动
            swipe.perform_swipe_down_percent(5)
    # 点击进入
    proceed.click()
