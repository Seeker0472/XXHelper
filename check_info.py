from time import sleep
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
    normarize.to_normal()
    driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().resourceId("
                                                               "\"cn.xuexi.android:id/ll_comm_head_score\")").click()
    # sleep(3)
    # element = driver.find_element(By.XPATH, '//android.widget.ListView/android.view.View[2]').find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[0]

    result = []
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
        result.append({"title": title, "score": score})
        print(title, score)

    return result


def check_score():
    """
    直接翻到底部,获取所有积分
    :return:
    """
    swipe.perform_swipe_down(1000)
    swipe.perform_swipe_down(1000)
    swipe.perform_swipe_down(1000)
    result = check_page()
    print(result)
    return result


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
