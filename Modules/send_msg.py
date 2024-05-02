import json
from time import sleep

import requests
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.wait import WebDriverWait

from General.secret import WeChat_APPID, WeChat_APPSECRET, WeChat_Receiver_OpenID, OSS_Auth
import oss2
import numpy, cv2
from General.normarize import to_normal
from General.driver import driver
import time
from General.check_info import check_score


def get_wechat_access_token():
    result = requests.get('https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + WeChat_APPID +
                          '&secret=' + WeChat_APPSECRET).json()
    return result['access_token']


def send_template_msg(time, total, detail, url):
    access_token = get_wechat_access_token()
    data = {
        "touser": WeChat_Receiver_OpenID,
        "template_id": "kZxUJu52P1WFN9ODPgY40M9DWXuk61-ejI2pfzXi0Us",
        "url": url,
        "data": {
            "time": {
                "value": time
            },
            "total": {
                "value": total
            },
            "detail": {
                "value": str(detail)
            }
        }
    }
    result = requests.post('https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=' + access_token,
                           json=data).json()
    print(result)


def upload(path, data):
    # # 从环境变量中获取访问凭证。运行本代码示例之前，请确保已设置环境变量OSS_ACCESS_KEY_ID和OSS_ACCESS_KEY_SECRET。
    # auth = oss2.ProviderAuth(EnvironmentVariableCredentialsProvider())
    bucket = oss2.Bucket(OSS_Auth, 'https://oss-cn-chengdu.aliyuncs.com', 'qgsc')

    # 上传文件。
    result = bucket.put_object(path, data)
    # HTTP返回码。
    print('http response code: {0}'.format(result.status))
    # 查看本次上传Object的版本ID。
    print('put object version:', result.versionid)


def get_screen_shot():
    to_normal()
    sleep(1)
    driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().resourceId("
                                                               "\"cn.xuexi.android:id/ll_comm_head_score\")").click()
    # 等待页面加载完成
    WebDriverWait(driver, 10).until(lambda x: x.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                             "new UiSelector().text(\"已完成\").instance(0)"))
    sleep(1)
    png1 = driver.get_screenshot_as_png()
    sleep(1)
    to_normal()
    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="强国通").click()
    sleep(1)
    png2 = driver.get_screenshot_as_png()
    img = cv2.hconcat([base64_to_cv2(png1), base64_to_cv2(png2)])
    img=cv2.resize(src=img, fx=0.5, fy=0.5, dsize=(0, 0))
    img = cv2.imencode('.png', img)[1]
    return img.tobytes()


def base64_to_cv2(base64_code):
    """
    将 base64 编码转换为 cv2 图像
    :param base64_code: base64 编码
    :return: cv2 图像
    """
    image_array = numpy.frombuffer(base64_code, dtype=numpy.uint8)

    # 使用 OpenCV 解码图像数据
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    return image


def get_points():
    result = check_score()
    total = 0
    for key in result:
        total += result[key]
    return total, result


def start():
    img = get_screen_shot()
    local_time = time.localtime()
    file_time = time.strftime('%Y-%m-%d', local_time)
    sep_time = time.strftime('%Y-%m-%d:%H-%M-%S', local_time)
    upload('result/' + file_time + '.png', img)
    json_info = {
        "time": sep_time,
        "id": file_time
    }
    upload('info/newest.json', json.dumps(json_info))
    url = 'http://record.seekerer.com/info/index.html?id=' + file_time + '&time=' + sep_time
    total, detail = get_points()
    send_template_msg(sep_time, total, detail, url)


