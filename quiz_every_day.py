from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

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
    处理填空题, 未完成
    :return:
    """
    text_edit = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className("
                                                                           "\"android.widget.EditText\")")
    edit_parent = driver.find_element(by=By.XPATH, value="//android.widget.EditText/..")
    parent_all = driver.find_elements(by=By.XPATH, value="//android.widget.EditText/../../../android.view.View")[1]
    text1 = parent_all.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
    text2 = parent_all.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[4].text
    all_space = edit_parent.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")
    answer_text = find_ans()
    # 答案的长度
    ans_len = len(all_space) - 1
    all_space[0].click()
    sleep(3)
    # text_edit.send_keys(u"会")

    # print(len(all_space))
    # print_all_child(all_space)
    pass


def print_all_child(element):
    """
    打印所有子节点的信息(Test Only)
    :param element:
    :return:
    """
    # 查找所有直接子节点
    child_elements = element.find_elements(By.XPATH, "./*")

    # 遍历并打印子节点的信息
    for index, child in enumerate(child_elements, start=1):
        # 获取子节点的标签名和其他属性，如class
        tag_name = child.tag_name
        class_name = child.get_attribute('class')

        print(f"Child {index}: Tag={tag_name}, Class={class_name}")


def find_ans():
    """
    查找答案
    :return:
    """
    driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"查看提示\")").click()
    sleep(2)
    ans_view = driver.find_element(by=By.XPATH,
                                   value="//android.view.View[@text=\"提示\"]/../../android.view.View[2]/android.view.View")
    print(ans_view.text)
    return ans_view.text
