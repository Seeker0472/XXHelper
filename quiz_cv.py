from time import sleep

from quiz_cv_perform import start
from driver import driver
import queue
import sqlite3

from thefuzz import fuzz
from thefuzz import process

result_queue = queue.Queue()
# TODO: 未完成
last_status = None

con = sqlite3.connect('main.sqlite')
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
    while not_finished():
        # 如果队列为空,则读取屏幕
        if result_queue.empty():
            read_screen()
            sleep(0.2)
            continue
        # 如果队列不为空,则读取队列信息
        result = result_queue.get()
        if result['type'] == 'wrong' or 'right':
            update_db(result)
            # 答错了或者答对了
            pass
        elif result['type'] == 'not_selected':
            # 没选
            answer_question(result['result'])
            pass
        else:
            # 未知类型
            pass


def update_db(result):
    """
    更新数据库
    判断是否答对,和是否需要更新数据库
    :return:
    """
    pass


def answer_question(information):
    """
    回答问题,只有当没选的时候调用
    :param information:如果截图中没有选答案,information是{"question": question_text(str),
            "choices": [{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}....]}
    :return:
    """
    global last_status
    ok, answer = find_answer(information)
    if ok:
        # 能从数据库中找到答案,就直接选择答案
        select_answer(information, answer)
    else:
        # 不能从数据库中找到答案,先把题目和选项存入数据库
        cur.execute("INSERT INTO Questions (question) VALUES(?)", (information['result']['question'],))
        question_id = cur.lastrowid
        for choice in information['result']['choices']:
            cur.execute("INSERT INTO QuestionAns(QUESTION_ID, CHOICE) VALUES(?,?)", (question_id, choice))
        con.commit()

        result = generate_answer(information)
        last_status = {'type': 'first', 'question': information['question'], 'answer': result}
        select_answer(information, result)


def find_answer(question):
    """
    从数据库中找到答案,模糊匹配!!!
    :param question:{"question": question_text(str),
            "choices": [{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}....]}
    :return:True,{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}; False,None
    """
    result = process.extractOne(question['question'], questions_db)
    if result[1] < 90:
        return False, None
    else:
        db_answers = cur.execute("select choice,ok from QuestionAns join Questions Q "
                                 "on QuestionAns.question_id = Q.id where Q.question=?", (result[0],)).fetchall()
        for choices in question['choices']:
            res = process.extractOne(choices['text'], [item[0] for item in db_answers])
            if res[1] < 90:
                return False, None
            # TODO: 修改!!!!
            for db_answer in db_answers:
                if db_answer[0] == res[0]:
                    if db_answer[1] == 1:
                        return True, db_answer[0]
                    else:
                        break


def generate_answer(question):
    """
    对于无法找到的问题生成答案,问GPT或者随机
    :param question:
    :return:
    """
    return "Right Answer"


def select_answer(information, answer):
    """
    选择答案
    :param information:{"question": question_text(str),
            "choices": [{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}....]}
    :param answer: str 要与information模糊匹配
    :return:
    """
    pass


def normalize_question(result):
    """
    规范化OCR结果
    :param result:
    :return:
    """
    return result


def not_finished():
    """
    判断是否结束,也许能实现更加智能的判断
    同时还要点复活!
    :return:
    """
    return True


def read_screen():
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
        return
    colors = [item['color'] for item in result['choices']]
    if 4 in colors:
        # 有未知颜色
        pass
    if 2 in colors:
        # 有红色!,答错了
        if 1 in colors:
            # 有绿色,说明有正确答案
            result_queue.put({'type': 'wrong', 'result': result})
        # result_queue.put({'type': 'wrong', 'result': result})
        pass
    elif 1 in colors:
        # 只有绿色!答对了
        result_queue.put({'type': 'right', 'result': result})
        pass
    else:
        # 既没有红色也没有绿色,没选!
        result_queue.put({'type': 'not_selected', 'result': result})
        return
