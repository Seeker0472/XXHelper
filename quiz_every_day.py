from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import normarize
from driver import driver
import swipe


def start():
    """
    开始
    :return:
    """
    normarize.to_sep_page("每日答题", "去答题")

    WebDriverWait(driver, 10).until(lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                             "new UiSelector().text(\"查看提示\").instance(0)"))

    answer()


def answer():
    """
    回答一道题目
    TODO:未完成
    :return:
    """
    while True:
        match get_type():
            case 0:
                return 0
                pass
            case 1:
                handle_single()
                pass
            case 2:
                handle_multi()
                pass
            case 3:
                handle_fill()
            case _:
                pass
        complete()


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
    swipe.perform_swipe_down(400)
    options_list = get_options()
    result = []
    ans = find_ans()
    for option in options_list:
        if ans.find(option) != -1:
            result.append(option)
            break
    select_options(result)
    complete()
    pass


def handle_multi():
    """
    处理多选题
    :return:
    """
    swipe.perform_swipe_down(400)
    options_list = get_options()
    result = []
    ans = find_ans()
    for option in options_list:
        if ans.find(option) != -1:
            result.append(option)
    select_options(result)
    complete()


def get_options():
    """
    获取选项
    :return:
    """
    options_list = []
    options = driver.find_elements(by=By.XPATH, value="//android.widget.ListView/android.view.View")
    for option in options:
        text = option.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[1].text
        options_list.append(text)
    print(options_list)
    return options_list


def select_options(options_ans):
    """
    选择选项
    :param options_ans:
    :return:
    """
    options = driver.find_elements(by=By.XPATH, value="//android.widget.ListView/android.view.View")
    if len(options_ans) == 0:
        options[0].click()

    for option in options:
        text = option.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[1].text
        if text in options_ans:
            option.click()


def get_text():
    """
    获取题目(选择题)
    :return:
    """
    parent_view = driver.find_element(by=By.XPATH, value="//android.widget.ListView/../../android.view.View")
    childs = parent_view.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")
    for child in childs:
        print(child.text)
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
    # 空格前的文字(4个字符)
    text1 = parent_all.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
    search_text = text1[-4:]
    # text2 = parent_all.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[4].text
    # print(text2,text2[0:4])
    all_space = edit_parent.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")
    answer_text = find_ans()
    # 答案的长度
    result = answer_text.find(search_text)

    ans_len = len(all_space) - 1
    print(result, answer_text[result + 4:result + 4 + ans_len])
    all_space[0].click()
    sleep(3)
    text_edit.send_keys(answer_text[result + 4:result + 4 + ans_len])

    # print(len(all_space))
    # print_all_child(all_space)


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
    result = driver.find_element(by=By.XPATH,
                                 value="//android.view.View[@text=\"提示\"]/../../android.view.View[2]/android.view.View").text
    driver.back()
    sleep(2)
    return result


def complete():
    """
    提交,检查是否正确
    :return:
    """
    sleep(1)
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"确定\")").click()
        sleep(2)
    # 到底要不要catch?
    except Exception as e:
        print("Function complete")
        print(e)
        pass

    sleep(2)
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"下一题\")").click()
    except Exception as e:
        print("Function complete1")
        print(e)
        pass

