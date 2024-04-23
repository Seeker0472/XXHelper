from time import sleep

from quiz_cv_perform import start
from driver import driver
import queue
import sqlite3
from driver import driver

import threading

from thefuzz import fuzz
from thefuzz import process

result_queue = queue.Queue()
# TODO: 未完成
last_status = None

GPT = False

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
    i = 1
    while not_finished():
        # 如果队列为空,则读取屏幕
        if result_queue.empty():
            # read_screen()
            threading.Thread(target=read_screen, args=(i,)).start()
            # read_screen(i)
            sleep(1)
            continue
        # 如果队列不为空,则读取队列信息
        result = result_queue.get()
        if result['time'] == i:
            # 这个可能会遇到问题
            i += 1
            if result['type'] == 'wrong' or result['type'] =='right':
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
    判断是否答对,和是否需要更新数据库,注意模糊匹配!!!
    :return:
    """
    right_ans = None
    if result['type'] == 'right':
        for item in result['result']['choices']:
            if item['color'] == 1:
                # 答对了
                right_ans = item['text']

        if last_status is None or last_status['type'] == 'first':
            # 状态未知或者是第一次答对
            question_id = cur.execute("SELECT id FROM Questions WHERE question=?",
                             (result['result']['question'],)).fetchall()[0][0]
            choices = cur.execute("SELECT choice FROM QuestionAns WHERE QUESTION_ID=?", (question_id,)).fetchall()
            right_db = process.extractOne(right_ans, [item[0] for item in choices])
            if right_db[1] < 90:
                # 无法匹配
                return
            else:
                cur.execute("UPDATE QuestionAns SET ok=1 WHERE QUESTION_ID=?", (question_id,))
                cur.execute("UPDATE QuestionAns SET ok=2 WHERE QUESTION_ID=? AND CHOICE=?", (question_id, right_db[0]))
                con.commit()
    elif result['type'] == 'wrong':
        for item in result['result']['choices']:
            if item['color'] == 1:
                # 答对了
                right_ans = item['text']

        question_id = cur.execute("SELECT id FROM Questions WHERE question=?",
                         (result['result']['question'],)).fetchall()[0][0]
        choices = cur.execute("SELECT choice FROM QuestionAns WHERE QUESTION_ID=?", (question_id,)).fetchall()
        right_db = process.extractOne(right_ans, [item[0] for item in choices])
        if right_db[1] < 90:
            # 无法匹配
            return
        else:
            cur.execute("UPDATE QuestionAns SET ok=1 WHERE QUESTION_ID=?", (question_id,))
            cur.execute("UPDATE QuestionAns SET ok=2 WHERE QUESTION_ID=? AND CHOICE=?", (question_id, right_db[0]))
            con.commit()
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
        last_status = {'type': 'second', 'question': information['question'], 'answer': answer}
        select_answer(answer)
    else:
        # 不能从数据库中找到答案,先把题目和选项存入数据库
        cur.execute("INSERT INTO Questions (question) VALUES(?)", (information['question'],))
        question_id = cur.lastrowid
        for choice in information['choices']:
            cur.execute("INSERT INTO QuestionAns(QUESTION_ID, CHOICE) VALUES(?,?)", (question_id, choice['text']))
        con.commit()

        result = generate_answer(information)
        last_status = {'type': 'first', 'question': information['question'], 'answer': result}
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
    if result[1] < 90:
        return False, None
    else:
        db_answers = cur.execute("select choice,ok from QuestionAns join Questions Q "
                                 "on QuestionAns.question_id = Q.id where Q.question=?", (result[0],)).fetchall()
        for choice in question['choices']:
            res = process.extractOne(choice['text'], [item[0] for item in db_answers])
            if res[1] < 90:
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
    同时还要点复活!
    :return:
    """
    return True


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
        return
    colors = [item['color'] for item in result['choices']]
    if 4 in colors:
        # 有未知颜色
        pass
    if 2 in colors:
        # 有红色!,答错了
        if 1 in colors:
            # 有绿色,说明有正确答案
            result_queue.put({'type': 'wrong', 'result': result, 'time': time})
        # result_queue.put({'type': 'wrong', 'result': result})
        pass
    elif 1 in colors:
        # 只有绿色!答对了
        result_queue.put({'type': 'right', 'result': result, 'time': time})
        pass
    else:
        # 既没有红色也没有绿色,没选!
        result_queue.put({'type': 'not_selected', 'result': result, 'time': time})
        return
