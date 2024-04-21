from time import sleep

from selenium.webdriver.support.wait import WebDriverWait

import swipe
import normarize

from driver import driver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By


def check_page():
    """
    检查积分页面,返回积分数值
    :return:
    """
    driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().resourceId("
                                                               "\"cn.xuexi.android:id/ll_comm_head_score\")").click()
    # 等待页面加载完成
    WebDriverWait(driver, 10).until(lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                             "new UiSelector().text(\"已完成\").instance(0)"))

    # 滑动到底部(直到能够获取到所有分数)
    while not login_sport_getable():
        swipe.perform_swipe_down_percent(40)

    result = dict()
    # 所有子节点(积分项)
    elements = driver.find_elements(By.XPATH, '//android.widget.ListView')[0].find_elements(By.XPATH,
                                                                                            './android.widget.ListView/android.view.View')

    for item in elements:
        try:
            title = item.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
            score = item.find_element(by=By.XPATH, value="./android.view.View/android.view.View[4]").find_elements(
                by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
        except:
            continue
        result[title] = int(score)
        # print(title, score)

    return result


def check_score():
    """
    直接翻到底部,获取所有积分
    :return:
    """
    normarize.to_normal()

    result = check_page()
    # print(result)
    return result


def login_sport_getable():
    """
    检查是否可以获取运动积分(是否能获取到第一项和最后一项)
    :return:
    """
    result = tuple()
    # 所有子节点(积分项)
    elements = driver.find_elements(By.XPATH, '//android.widget.ListView')[0].find_elements(By.XPATH,
                                                                                            './android.widget.ListView/android.view.View')

    for item in elements:
        try:
            title = item.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
            score = item.find_element(by=By.XPATH, value="./android.view.View/android.view.View[4]").find_elements(
                by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
        except:
            continue
        result += (title,)
    if "登录" in result and "强国运动" in result:
        return True
    else:
        return False
