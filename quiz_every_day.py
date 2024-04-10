from appium.webdriver.common.appiumby import AppiumBy

from driver import driver


def start():
    """
    开始
    :return:
    """
    pass


def answer():
    """
    回答一道题目
    :return:
    """
    match get_type():
        case 0:
            pass
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case _:
            pass


def get_type():
    """
    获取题目类型
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                            value="new UiSelector().text(\"单选题\")")
        return 1
    except:
        pass
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                            value="new UiSelector().text(\"多选题\")")
        return 2
    except:
        pass
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                            value="new UiSelector().text(\"填空题\")")
        return 3
    except:
        pass
    return 0


def handle_single():
    """
    处理单选题
    :return:
    """
    pass


def handle_multi():
    """
    处理多选题
    :return:
    """
    pass


def handle_fill():
    """
    处理填空题
    :return:
    """
    pass
