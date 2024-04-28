# import check_info
# import driver
# import swipe
# import normarize
# import ints_quiz
# import vid
# import read
# import quiz_every_day
# import local_channel
# import subscribe
#
# # swipe.perform_swipe()
# # check_info.check_score()
# # ints_quiz.check_type()
# # vid.start()
# # read.start()
# # ints_quiz.pair()
#
# # quiz_every_day.answer()
# # local_channel.start()
# # subscribe.start()
#
# print("init FInish")
#
# # normarize.to_sep_page("趣味答题","去看看")
# # print(dir(driver.driver))
#
# # print(driver.driver.page_source)
#
# print(type(driver.driver.get_screenshot_as_png()) == bytes)
# from time import sleep
#
# from appium.webdriver.common.appiumby import AppiumBy
#
# # import quiz_cv_perform
# # quiz_cv_perform.start()
#
# import quiz_cv
# from driver import driver
#
# sleep(2)
# while True:
#     driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"开始比赛\")").click()
#     sleep(5)
#     quiz_cv.start_answer()
#     driver.back()
#     sleep(2)



from normarize import to_recommend

to_recommend()
