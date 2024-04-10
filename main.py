from time import sleep

from vid import start as vid_start
from check_info import check_score
from read import start as read_start
from quiz_every_day import start as eq_start
from ints_quiz import start as ints_start


def main():
    start()


def start():
    while True:
        result = check_score()
        print(result['我要选读文章'])
        if result['我要选读文章'] < 12:
            read_start()
            sleep(1)
        if result['我要视听学习'] < 12:
            vid_start()
            sleep(1)
        if result['每日答题'] < 5:
            eq_start()
        if result['趣味答题'] < 8:
            ints_start()
        if result['我要选读文章'] + result['我要视听学习'] + result['每日答题'] + result['趣味答题'] >= 36:
            return "All Done!"
        print(result)


if __name__ == '__main__':
    main()
