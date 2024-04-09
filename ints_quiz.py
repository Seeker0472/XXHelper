from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

from driver import driver
import normarize
import swipe

import sqlite3
import ask_gpt

conn = sqlite3.connect('main.sqlite')
cur = conn.cursor()

GPT = True


def start():
    """
    开始答题
    进入答题界面,然后调用check_type()判断是什么类型的答题
    :return:
    """
    # 切换到主界面
    normarize.to_normal()
    # 点击积分
    driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().resourceId("
                                                               "\"cn.xuexi.android:id/ll_comm_head_score\")").click()
    sleep(2)

    proceed = None
    # 找到趣味答题并点击进入
    while proceed is None:
        # 所有子节点(积分项)
        elements = (driver.find_elements(By.XPATH, '//android.widget.ListView')[0]
                    .find_elements(By.XPATH, './android.widget.ListView/android.view.View'))
        for item in elements:
            try:
                title = item.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
                print(title)
                if title != "趣味答题":
                    continue
                score = item.find_element(by=By.XPATH, value="./android.view.View/android.view.View[4]").find_elements(
                    by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
                proceed = item.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"去看看\")")
                if score > 7:
                    return
            except:
                continue
            print(title, score)
        # 如果当前页没有找到趣味答题,则向下滑动
        if proceed is None:
            swipe.perform_swipe_down(400)
    # 点击进入
    proceed.click()

    sleep(2)

    check_type()


def check_type():
    """
    判断是什么类型的答题
    :return:
    """
    # 是否是挑战答题
    if is_challenge():
        print("挑战答题")
        challenge()


def is_challenge():
    """
    是否是挑战答题
    :return: True:是挑战答题,False:不是挑战答题
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"挑战答题\")")
        return True
    except:
        return False


def challenge():
    """
    开始挑战答题,暂时只答一项
    :return:
    """
    driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"历史文化\")").click()

    sleep(3)

    while True:
        # 获取题目
        block = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                    value="new UiSelector().className(\"android.view.View\").instance(13)")
        # 题干
        text = block.find_elements(by=AppiumBy.CLASS_NAME, value="android.view.View")[0].text
        # 选项的父节点
        list_view = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                        value="new UiSelector().className(\"android.widget.ListView\")")

        # 查找所有直接子节点
        child_elements = list_view.find_elements(By.XPATH, "./android.widget.ListView/*")

        # 访问数据库，如果没有则插入
        text_id = cur.execute("select id from Texts where text=(?)", (text,)).fetchall()
        if len(text_id) == 0:
            cur.execute("insert into Texts (text) values (?)", (text,))
            conn.commit()
            text_id = cur.execute("select id from Texts where text=?", (text,)).fetchall()[0][0]
            for index, child in enumerate(child_elements, start=1):
                # 获取子节点的标签名和其他属性，如class
                content = child.find_element(by=By.XPATH,
                                             value="./android.view.View/android.view.View/android.view.View").text
                cur.execute("insert into Answers (text_id,content, ok) values (?, ?, ?)", (text_id, content, 0))
            conn.commit()
        else:
            text_id = text_id[0][0]
        db_result = cur.execute("select id, content, ok from Answers where text_id=(?)", (text_id,)).fetchall()

        choice = None
        # 是否询问GPT
        if not GPT:
            # 确定选项,不访问GPT
            for item in db_result:
                if item[2] == 0:
                    choice = item[1]
                    break
                if item[2] == 2:
                    choice = item[1]
                    break
        else:
            # 确定选项,使用GPT
            for item in db_result:
                if item[2] == 2:
                    choice = item[1]
                    break
            if choice is None:
                # 数据库中没有正确的选项,问gpt
                choice = ask_gpt.ask_gpt3(text, [item[1] for item in db_result])

        # 遍历所有选项
        for index, child in enumerate(child_elements, start=1):
            # 获取子节点的标签名和其他属性，如class
            content = child.find_element(by=By.XPATH,
                                         value="./android.view.View/android.view.View/android.view.View").text
            if content == choice:
                child.find_element(by=By.XPATH,
                                   value="./android.view.View/android.view.View/android.view.View").click()
                break

        print(text)

        sleep(4)

        # 通过判断是否有"挑战结束"来判断是否答对
        if challenge_over():
            cur.execute("update Answers set ok=1 where text_id=? and content=?", (text_id, choice,))
            conn.commit()
            sleep(2)
            driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"再来一局\")").click()
            sleep(4)
            # break
        else:
            cur.execute("update Answers set ok=1 where text_id=? ", (text_id,))
            cur.execute("update Answers set ok=2 where text_id=? and content=?", (text_id, choice,))
            conn.commit()


def challenge_over():
    """
    判断是否挑战结束,如果挑战结束,则点击结束本局
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"挑战结束\")")
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"结束本局\")").click()
        return True
    except:
        return False