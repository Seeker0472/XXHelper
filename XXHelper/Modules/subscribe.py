from time import sleep

from ..General.driver import driver
from ..General import normarize, swipe
from ..Modules.Question.quiz_cv_perform import base64_to_cv2
import cv2
from ..Modules.Question import ocr

prev_img = None


def start(left=2):
    """
    订阅,暂时无解,以后上计算机视觉
    :return:
    """
    left = start_QGH(left)
    if left > 0:
        start_QGH(left)


def start_QGH(left):
    sleep(5)
    index = 0
    normarize.to_sep_page("订阅", "去看看")
    sleep(8)
    while left > 0:
        if index >= 9:
            break
        left = read_screen(left)
        goto_module(index)
        index += 1
    return left


def start_DFPT(left):
    sleep(5)
    index = 1
    goto_DFPT()
    sleep(8)
    while left > 0:
        if index >= 4:
            break
        left = read_screen(left)
        goto_module(index)
        index += 1
    return left


def goto_DFPT():
    """
    跳转到地方平台
    :return:
    """
    cv_result = ocr.read_img(get_cv2())
    for items in cv_result[0]:
        if items[1][0] == "地方平台":
            driver.tap([((items[0][0][0] + items[0][1][0] + items[0][2][0] + items[0][3][0]) / 4,
                         (items[0][0][1] + items[0][1][1] + items[0][2][1] + items[0][3][1]) / 4)], 100)
            sleep(5)
            return


def read_screen(left=2):
    """
    读取屏幕
    :return:
    """
    global prev_img
    prev_img = None
    img_now = get_cv2()
    while different(img_now):
        img_now = get_cv2()
        ocr_result = ocr.read_img(img_now)
        left = click_subscribe(ocr_result, left)
        if left == 0:
            break
        swipe.perform_swipe_down_percent(10)
    return left


def click_subscribe(ocr_result, times=2):
    """
    点击订阅
    :param times:
    :param ocr_result:
    :return:
    """
    for res in ocr_result[0]:
        if times == 0:
            break
        if res[1][0] == "订阅":
            times -= 1
            driver.tap([((res[0][0][0] + res[0][1][0] + res[0][2][0] + res[0][3][0]) / 4,
                         (res[0][0][1] + res[0][1][1] + res[0][2][1] + res[0][3][1]) / 4)], 100)
    return times


def different(img_now):
    """
    比较两张图片
    :param img_now:
    :return:
    """
    global prev_img
    if prev_img is None:
        prev_img = img_now
        return True
    else:
        ret = cv2.absdiff(prev_img, img_now).sum() > 100
        prev_img = img_now
        return ret
    pass


def get_cv2():
    """
    截屏并转为cv2
    :return:
    """
    png = driver.get_screenshot_as_png()
    cv = base64_to_cv2(png)
    return cv


def goto_module(index):
    """
    跳转到指定模块
    :return:
    """
    modules = ["推荐", "上新", "主要央媒", "行业媒体", "机关企事业", "党刊", "高校", "地方媒体", "社会机构"]
    screen = get_cv2()
    ocr_result = ocr.read_img(screen)
    for items in ocr_result[0]:
        if items[1][0] == modules[index]:
            driver.tap([((items[0][0][0] + items[0][1][0] + items[0][2][0] + items[0][3][0]) / 4,
                         (items[0][0][1] + items[0][1][1] + items[0][2][1] + items[0][3][1]) / 4)], 100)
            return

def goto_module_DFPT(index):
    """
    跳转到指定模块
    :return:
    """
    modules = ["推荐", "上新", "地区", "其他"]
    screen = get_cv2()
    ocr_result = ocr.read_img(screen)
    for items in ocr_result[0]:
        if items[1][0] == modules[index]:
            driver.tap([((items[0][0][0] + items[0][1][0] + items[0][2][0] + items[0][3][0]) / 4,
                         (items[0][0][1] + items[0][1][1] + items[0][2][1] + items[0][3][1]) / 4)], 100)
            return
