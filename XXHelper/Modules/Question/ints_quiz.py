import random
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from ...General.driver import driver
from ...General import normarize
from ...Modules.Question.quiz_cv import start_answer as cv_start
import sqlite3
from ...Modules.Question import ask_gpt as ask_gpt

from ...General.db import get_connection,close_connection

conn = None
cur = None

# 是否询问GPT
GPT = True

# 是否使用CV,否则乱选(多人挑战)
CV = True


# TODO:把CV加入
def start():
    """
    开始答题
    进入答题界面,然后调用check_type()判断是什么类型的答题
    :return:
    """
    global cur,conn
    cur,conn = get_connection()

    normarize.to_sep_page("趣味答题", "去看看")

    sleep(10)

    check_type()

    close_connection(cur)



def check_type():
    """
    判断是什么类型的答题
    :return:
    """
    # 是否是挑战答题
    if is_challenge():
        print("挑战答题")
        challenge()
    else:
        if is_muti():
            print("多人擂台")
            # 进入多人擂台
            driver.find_element(by=By.XPATH,
                                value="//android.view.View[@text=\"随机匹配\"]/../android.view.View").click()
            if CV:
                cv_start()
            else:
                pair()
        if is_four():
            print("四人赛")
            driver.find_element(by=By.XPATH,
                                value="//android.view.View[@text=\"开始比赛\"]").click()
            if CV:
                cv_start()
            else:
                pair()


def is_challenge():
    """
    是否是挑战答题
    :return: True:是挑战答题,False:不是挑战答题
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"挑战答题\")")
        return True
    except NoSuchElementException:
        return False


# TODO:查询数据库
def challenge():
    """
    开始挑战答题,暂时只答一项
    :return:
    """
    driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"历史文化\")").click()

    sleep(3)

    while not challenge_die():
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
            # driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"再来一局\")").click()
            # sleep(4)
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
    # TODO: Infinite Loop!
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"挑战结束\")")
        # driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"再来一局\")")
        try:
            driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"立即复活\")").click()
            sleep(2)
        except NoSuchElementException:
            pass
        return True
    except NoSuchElementException:
        return False


def challenge_die():
    """
    判断是否彻底结束(复活了一次)
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"再来一局\")")
        return True
    except NoSuchElementException:
        return False


def is_muti():
    """
    判断是否是多人擂台
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"随机匹配\")")
        return True
    except NoSuchElementException:
        return False


def is_four():
    """
    判断是否是四人赛
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"开始比赛\")")
        return True
    except NoSuchElementException:
        return False


def pair():
    """
    多人擂台
    :return:
    """
    while True:
        try:
            if is_finished():
                break
            list_view = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR,
                                            value="new UiSelector().className(\"android.widget.ListView\")")

            child_elements = list_view.find_elements(By.XPATH, "./android.widget.ListView/*")

            # 随机选择一个
            child_elements[random.randint(0, len(child_elements) - 1)].click()
            sleep(2)
        except NoSuchElementException:
            sleep(4)


def is_finished():
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"继续挑战\")")
        return True
    except NoSuchElementException:
        return False
