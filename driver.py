from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='UiAutomator2',
    deviceName='38fe22a5',
    appPackage='cn.xuexi.android',
    appActivity='com.alibaba.android.rimet.biz.SplashActivity',
    platformVersion="14",
    noReset=True,
    unicodeKeyboard=True,
    resetKeyboard=True
)
appium_server_url = 'http://localhost:4723'

driver = webdriver.Remote(appium_server_url, options=UiAutomator2Options().load_capabilities(capabilities))
