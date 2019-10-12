import os
import msvcrt
import sys
import math

import click

from app_attribute import AppAttribute as app
from log import ReadLog


@click.command()
@click.option("-p", default="", help="文件路径, 若为空, 则读取阅读记录中的最后一条记录")
@click.option("-r", default=1, help="每页显示的行数, 默认为: 1, 示例: 5")
@click.option("-s", default=0, type=float, help="跳页, 默认为文件第一行, 示例: 12.35, 即跳到 12.35% 位置")
@click.option("-e", default="utf-8", help="文件编码, 默认为: utf-8, 示例: gbk")
@click.option("-c", default=1, help="每次翻页是否清屏, 1清屏/0不清屏, 默认为: 1, 示例: 0")
def main(p, r, s, e, c):
    book_path = p
    if book_path == "":
        book_path = ReadLog.get_last_book()
    # book_path = "D:/Downloads/仙逆-贴吧精校版.txt"

    # 每页显示的行数
    page_row = r

    # 文件编码
    encoding = e

    # 每次翻页是否清屏, 1清屏/0不清屏
    clear = c

    # 阅读进度(当前行数/总行数)
    schedule = s / 100

    lines = read_txt(book_path, encoding)
    tip(book_path)
    if schedule != 0:
        pos = math.floor(schedule * len(lines))
    else:
        pos = ReadLog.read_schedule(book_path)
    while True:
        key = msvcrt.getch()
        clear_screen(clear)
        if is_quit_key(key):
            break
        if is_page_up_key(key):
            pos = read_page(lines, pos - page_row * 2, page_row)
        elif is_page_down_key(key):
            pos = read_page(lines, pos, page_row)
        elif is_clear_key(key):
            os.system("cls")
    ReadLog.write_schedule(book_path, pos - 1)
    print("当前进度: %s%%" % str(round((pos - 1) / len(lines), 4) * 100))


# 读一页
def read_page(lines: list, pos: int, page_row: int):
    if pos <= 0:
        pos = 1
    string = ""
    ret = pos
    for i in range(pos - 1, page_row + pos - 1):
        if i >= len(lines):
            string += "\r\n已到结尾"
            break
        ret += 1
        string += lines[i]
    print(string)
    return ret


def clear_screen(clear: int):
    if clear == 1:
        os.system("cls")


def is_quit_key(key):
    return key == b"q" or key == b"Q"


def is_page_up_key(key):
    """
    上方向键: H
    """
    return key == b"w" or key == b"W"


def is_page_down_key(key):
    """
    下方向键: P
    """
    return key == b"s" or key == b"S"


def is_clear_key(key):
    """
    其他键清屏
    """
    return (not is_quit_key(key)) and (not is_page_up_key(key)) and (not is_page_down_key(key))


def tip(book_path):
    """提示性输出"""
    print(os.path.basename(book_path))
    print("按下 '下方向键' 向下翻页")
    print("按下 'q' 退出")


def init_app_attribute():
    app.root = os.path.split(sys.argv[0])[0]


def read_txt(path: str, encoding: str) -> list:
    if not os.path.isfile(path):
        print("文件不存在")
        sys.exit(1)
    try:
        file = open(path, mode="r", encoding=encoding)
        lines = file.readlines()
        file.close()
    except UnicodeDecodeError:
        print("无法以%s编码打开文件, 请选择其他编码方式" % encoding)
        sys.exit(1)
    return lines


if __name__ == "__main__":
    init_app_attribute()
    main()
