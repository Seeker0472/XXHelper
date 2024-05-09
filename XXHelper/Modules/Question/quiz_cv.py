from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from selenium.common import NoSuchElementException

from ...Modules.Question.quiz_cv_perform import start
import sqlite3
from ...General.driver import driver

from thefuzz import process

GPT = False

con = sqlite3.connect('./main.sqlite')
cur = con.cursor()
# 数据库中的问题
questions_db = [item[1] for item in cur.execute("SELECT * FROM Questions").fetchall()]


def start_answer():
    """
    注意,进入这个Function需要已经进入答题界面,并使用手段干掉了安卓的Flag Secure的截屏限制
    wrapper_function
    :return:
    """
    answering()
    pass


def answering():
    """
    回答问题
    :return:
    """
    i = 1
    while not not_finished():

        OK, result = read_screen(i)
        if OK:
            answer_question(result)
            sleep(3)
        else:
            sleep(0.5)
            pass


def answer_question(information):
    """
    回答问题,只有当没选的时候调用
    :param information:如果截图中没有选答案,information是{"question": question_text(str),
            "choices": [{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}....]}
    :return:
    """
    ok, answer = find_answer(information)
    if ok:
        select_answer(answer)
    else:
        # 不能从数据库中找到答案
        result = generate_answer(information)
        select_answer(result)


def find_answer(question):
    """
    从数据库中找到答案,模糊匹配!!!
    :param question:{"question": question_text(str),
            "choices": [{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}....]}
    :return:True,{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}; False,None
    """
    # 规范化数据格式
    question = normalize_question(question)
    result = process.extractOne(question['question'], questions_db)
    if result[1] < 80:
        return False, None
    else:
        db_answers = cur.execute("select choice,ok from QuestionAns join Questions Q "
                                 "on QuestionAns.question_id = Q.id where Q.question=?", (result[0],)).fetchall()
        for choice in question['choices']:
            res = process.extractOne(choice['text'], [item[0] for item in db_answers])
            if res[1] < 80:
                return False, None
            # TODO: 修改!!!!
            # res是最佳匹配的答案,匹配数据库记录查询是否正确
            for db_answer in db_answers:
                if db_answer[0] == res[0]:
                    if db_answer[1] == 2:
                        # 正确答案
                        return True, choice
                    else:
                        break
        # 找到的答案中没有正确答案
        #TODO:修改!!!!
        # result_queue.put({'type': '404NF', 'result': question})
        return False, None


def generate_answer(question):
    """
    对于无法找到的问题生成答案,问GPT或者随机
    :param question:  {"question": question_text(str),
            "choices": [{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}....]}
    :return:{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}
    """
    if GPT:
        # 问GPT
        pass
    else:
        # 随机
        import random
        return random.choice(question['choices'])


def select_answer(answer):
    """
    选择答案,点击指定位置
    :param answer: {"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}
    :return:
    """
    print("select" + str(answer))
    driver.tap([(answer['x'] + answer['w'] / 2, answer['y'] + answer['h'] / 2)], 100)
    pass


def normalize_question(result):
    """
    规范化OCR结果,目前打算 1.规范化标点(英转中) 2.连续空格转为一个 3.去除每个选项的 A. B. C. D.
    :param result: {"question": question_text(str),
            "choices": [{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}....]}
    :return:{"question": question_text(str),
            "choices": [{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}....]}
    """
    result['question'] = result['question'].replace("?", "？").replace("!", "！").replace(":", "：").replace(";", "；")
    result['question'] = result['question'].replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " ")
    for choice in result['choices']:
        choice['text'] = (choice['text'].replace("A.", "").replace("B.", "").replace("C.", "").replace("D.", "")
                          .replace("a.", "").replace("b.", "").replace("c.", "").replace("d.", ""))
    return result


def not_finished():
    """
    判断是否结束,也许能实现更加智能的判断
    :return:
    """
    try:
        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"继续挑战\")")
        return True
    except NoSuchElementException:
        return False


def read_screen(time):
    """
    调用quiz_cv_perform读取屏幕,并将结果放入队列
    当主进程读取到队列不为空时,应该读取队列(同时能阻塞循环)
    :return:
    """
    png = driver.get_screenshot_as_png()
    try:
        result = start(png)
    except ValueError:
        # 如果出现ValueError,则说明没有找到选项,直接返回
        return False, None
    # colors = [item['color'] for item in result['choices']]
    # if 4 in colors:
    #     # 有未知颜色
    #     pass
    # if 2 in colors:
    #     # 有红色!,答错了
    #     return False, None
    # elif 1 in colors:
    #     # 只有绿色!答对了
    #     return False, None
    #     pass
    # else:
    #     # 既没有红色也没有绿色,没选!
    #     return True, result
    return True, result
