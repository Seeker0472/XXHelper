from time import sleep

from appium.webdriver.common.appiumby import AppiumBy

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
        return False
