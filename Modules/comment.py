import random
from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from General.driver import driver
from General import normarize
from General.variables import comments


#TODO:更加智能地发表回复,添加到main中
def start():
    print("开始评论")
    normarize.to_recommend()
    select_article()
    sleep(2)
    submit_comment()


def select_article():
    while True:
        # elements = driver.find_elements(by=By.XPATH,
        #                                 value="//android.widget.ListView/android.widget.FrameLayout")
        elements = driver.find_elements(by=By.XPATH,
                                        value="//androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout")
        for item in elements:
            try:
                text = item.find_element(by=By.XPATH,
                                         value="./android.widget.FrameLayout/android.widget.LinearLayout/android"
                                               ".widget.LinearLayout/android.widget.TextView").text
                item.click()
                return
            except NoSuchElementException as e:
                continue


def submit_comment():
    WebDriverWait(driver, 10).until(lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                             "new UiSelector().text(\"欢迎发表你的观点\")"))
    driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"欢迎发表你的观点\")").click()
    sleep(1)
    driver.find_element(by=By.CLASS_NAME, value="android.widget.EditText").send_keys(random.choice(comments))
    sleep(1)
    driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"发布\")").click()
    sleep(1)
