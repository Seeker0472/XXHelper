import random
from time import sleep

from selenium.webdriver.common.by import By

from General.driver import driver
from General import normarize


def start():
    normarize.to_sep_page("本地频道", "去看看")
    sleep(2)
    rand_open()


def rand_open():
    pages=driver.find_elements(by=By.XPATH, value="//androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout")
    pages[random.randint(0, len(pages)-1)].click()



