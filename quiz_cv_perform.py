import base64

import cv2
import matplotlib.pyplot as plt
import numpy
import numpy as np
from ocr import read_img

SHOW_RESULT = False


# TODO:连接到程序(Doing!)

# TODO:传入base64(Half-Finish)

# TODO:提高运行速度

# TODO:合并答案--每个答案会有两个框框(Half-Finish)

# TODO:规范化返回值!!(Half-Finish)

def start(img=cv2.imread('./Screenshots/normal.png')):
    """
    读取图片,掉用get_border函数,获取问题和选项的位置,并在图片上标记,调用read_img函数,ocr识别问题和选项
    :param img:
    :return:
    """
    # 读取图片,后期之间传base64
    # print(type(img))
    if type(img) == bytes:
        img = base64_to_cv2(img)
    elif type(img) == numpy.ndarray:
        pass
    else:
        raise TypeError("img 的类型" + str(type(img)) + "不受支持:既不是 bytes 也不是 numpy.ndarray")
    # elif type(img) == str:
    # img = cv2.imread('./Screenshots/normal.png')
    # 识图的结果
    result = get_border(img)
    if result is None:
        raise ValueError("没有找到问题和选项")
    question = img[result['text']['y']:result['text']['y'] + result['text']['h'],
               result['text']['x']:result['text']['x'] + result['text']['w']]
    if question.size == 0:
        raise ValueError("没有找到问题")

    question_text = ""
    question_cv = read_img(question)
    for idx in range(len(question_cv)):
        res = question_cv[idx]
        if res is not None:
            for line in res:
                question_text += line[1][0] + " "
    question_text = question_text[:-1]
    print(question_text)
    print(result['choices'])

    # print(question_cv)
    if SHOW_RESULT:
        cv2.rectangle(img, (result['text']['x'], result['text']['y']),
                      (result['text']['x'] + result['text']['w'], result['text']['y'] + result['text']['h']),
                      (190, 37, 150, 1), 2)
        cv2.putText(img, "Question", (result['text']['x'], result['text']['y']), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                    (0, 0, 255),
                    2)

        i = 1
        for choice in result['choices']:
            cv2.rectangle(img, (choice['x'], choice['y']),
                          (choice['x'] + choice['w'], choice['y'] + choice['h']), (37, 150, 190, 1), 2)
            cv2.putText(img, "Ans" + str(i), (choice['x'], choice['y']), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                        (0, 0, 255), 2)
            i += 1

        cv2.imshow("img", img)
        # print(type(img))

        # plt.show()
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return {"question": question_text, "choices": result['choices']}


def get_border(img):
    """
    转灰阶图进行边缘检测,调用process_contours函数,获取问题和选项的位置
    :param img:
    :return:
    """
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 应用高斯模糊
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # Canny 边缘检测
    edges = cv2.Canny(blurred, 20, 30)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # cv2.imshow("img", blurred)
    return process_contours(img, contours)


def process_contours(img, contours):
    """
    先获取最大的框(题目的边界)调用find_choices获取问题和选项的位置,首先按照条件过滤选项框,
    然后调用get_text获取选项框和边界之间的黑色文字(题目)等待边界,返回问题和选项的位置
    :param img:
    :param contours:
    :return:
    """
    height = img.shape[0]
    width = img.shape[1]
    # print(height, width, img.shape)
    containers = []
    for contour in contours:
        # 计算轮廓的边界矩形
        x, y, w, h = cv2.boundingRect(contour)

        # 设定条件过滤
        if w > width / 3 * 2 and h > height / 10:  # 假设选项框的最小宽度和高度
            containers.append({"x": x, "y": y, "w": w, "h": h})

    max_container = max(containers, key=lambda x: x['h'])

    if not not_answered(contours, max_container, img):
        return None

    choices_area = find_choices(contours, max_container, img)

    border = {'x': max_container['x'], 'y': max_container['y'], 'w': max_container['w'],
              'h': min(choices_area, key=lambda x: x['y'])['y'] - max_container['y']}

    text_area = get_text(img, border)
    return {"choices": choices_area, "border": border, "text": text_area}


def not_answered(contours, max_container, img):
    """
    检查是否已经回答过问题
    :param contours:
    :param max_container:
    :param img:
    :return:
    """
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > max_container['w'] / 2 and h > max_container['h'] / 10 and max_container['x'] < x < max_container['x'] + \
                max_container['w'] and max_container['y'] < y < max_container['y'] + max_container['h']:
            answer = img[y:y + h, x:x + w]
            color = check_color(answer)
            if color == 1 or color == 2:
                return False
    return True


def find_choices(contours, max_container, img):
    """
    寻找选项, 选项的宽度大于最大项的一半, 高度大于最大项的十分之一, 且在最大项的范围内
    :param img:
    :param contours:
    :param max_container:
    :return:[{"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color}.....]
    """
    results = []
    i = False
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > max_container['w'] / 2 and h > max_container['h'] / 10 and max_container['x'] < x < max_container['x'] + \
                max_container['w'] and max_container['y'] < y < max_container['y'] + max_container['h']:
            if i:
                # TODO:颜色检测!!
                answer = img[y:y + h, x:x + w]
                color = check_color(answer)
                text_cv = read_img(answer)
                choice_text = ""
                for idx in range(len(text_cv)):
                    res = text_cv[idx]
                    for line in res:
                        choice_text += line[1][0] + " "
                choice_text = choice_text[:-1]
                results.append({"x": x, "y": y, "w": w, "h": h, "text": choice_text, "color": color})
            i = not i

    return results


def get_text(img, border):
    """
    获取选项框和边界之间的黑色文字(题目)
    :param img: 图像
    :param border:  边界
    :return:   {"x": x, "y": y, "w": w, "h": h}
    """
    # 将BGR颜色空间转成HSV空间
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_color = (0, 0, 0)
    upper_color = (110, 110, 110)
    # 查找颜色
    mask_img = cv2.inRange(src=hsv_img, lowerb=lower_color, upperb=upper_color)
    # 应用高斯模糊
    blurred = cv2.GaussianBlur(mask_img, (7, 7), 0)
    # Canny 边缘检测
    edges = cv2.Canny(blurred, 50, 100)
    contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # 寻找文字区域
    x1, y1, x2, y2 = border['x'] + border['w'], border['y'] + border['h'], border['x'], border['y'],
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if border['x'] < x < border['x'] + border['w'] and border['y'] < y < border['y'] + border['h']:
            x1 = min(x1, x)
            y1 = min(y1, y)
            x2 = max(x2, x + w)
            y2 = max(y2, y + h)

    x1 -= 5
    y1 -= 5
    x2 += 5
    y2 += 5

    return {"x": x1, "y": y1, "w": x2 - x1, "h": y2 - y1}


def check_color(item):
    """
    检查选项的颜色,从而获取状态
    :param item: 图像
    :return: 1-绿色, 2-红色, 3-灰色, 4-其他
    """
    average_color_row = np.average(item, axis=0)
    average_color = np.average(average_color_row, axis=0)
    # print("avg::  " + str(average_color))
    # 检测绿色
    if 110 < average_color[0] < 130 and 190 < average_color[1] < 210 and 30 < average_color[2] < 50:
        print("color is green")
        return 1
    # 检测红色
    if 110 < average_color[0] < 120 and 80 < average_color[1] < 100 and 240 < average_color[2] < 260:
        print("color is red")
        return 2
    # 检测灰色
    if 230 < average_color[0] < 250 and 230 < average_color[1] < 250 and 230 < average_color[2] < 250:
        # print("color is gray")
        return 3

    return 4


# base64转cv2
def base64_to_cv2(base64_code):
    """
    将 base64 编码转换为 cv2 图像
    :param base64_code: base64 编码
    :return: cv2 图像
    """
    # img_data = base64.b64decode(base64_code)
    # img_array = np.fromstring(img_data, np.uint8)
    # img = cv2.imdecode(img_array, cv2.COLOR_RGB2BGR)
    # 将二进制数据转换为 numpy 数组
    image_array = np.frombuffer(base64_code, dtype=np.uint8)

    # 使用 OpenCV 解码图像数据
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    return image
