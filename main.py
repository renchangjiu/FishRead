import os
import re
import msvcrt
import sys
from typing import TextIO

from app_attribute import AppAttribute as app
from log import ReadLog

null = None

book_path = "D:/Downloads/仙逆-贴吧精校版.txt"

# 每页显示的行数
page_row = 1

# 阅读进度
schedule = ""

# 每次翻页是否清屏
clear = False


# 读一页
def read_page(file: TextIO):
    for i in range(0, page_row):
        print(file.readline())


def check_path():
    return True


def seek(file: TextIO, pos: int) -> int:
    try:
        file.seek(pos)
        for i in range(0, 20):
            file.readline()
    except UnicodeDecodeError as error:
        pos += 1
        seek(file, pos)
    else:
        file.seek(pos)
        return file.tell()


def clear_screen():
    if clear:
        os.system("cls")


"""
todo: 上翻一页

"""


# -row num: 每页显示的行数
def main():
    if not check_path():
        return
    tip()
    file = open(book_path, mode="r", encoding="utf-8")
    size = os.path.getsize(book_path)
    if schedule != "":
        pos = seek(file, int(schedule * size))
    else:
        pos = seek(file, ReadLog.get_schedule(book_path))
    while True:
        key = msvcrt.getch()
        clear_screen()
        if is_quit(key):
            break
        if is_page_up(key):
            # file.seek(pos)
            read_page(file)
        elif is_page_down(key):
            pos = file.tell()
            read_page(file)
    ReadLog.set_schedule(book_path, pos)
    print(round(file.tell() / size, 2))


def is_quit(key):
    return key == b"q"


def is_page_up(key):
    """
    上方向键: H
    """
    return key == b"H"


def is_page_down(key):
    """
    下方向键: P
    """
    return key == b"P"


def tip():
    """提示性输出"""
    print(os.path.basename(book_path))
    print("按下 '下方向键' 向下翻页")
    print("按下 'q' 退出")


def init_app_attribute():
    app.root = os.path.split(sys.argv[0])[0]


if __name__ == "__main__":
    init_app_attribute()
    main()
