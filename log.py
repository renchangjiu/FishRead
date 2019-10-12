import os

from app_attribute import AppAttribute as app


class ReadLog(object):

    @staticmethod
    def read_schedule(book_path) -> int:
        path = app.root + "/read.log"
        file = open(path, "r", encoding="utf=8")
        lines = file.readlines()
        file.close()
        schedule = 0
        for line in lines:
            split = line.split("?")
            if len(split) == 2 and split[0] == book_path:
                schedule = int(split[1])
        return schedule

    @staticmethod
    def write_schedule(book_path: str, schedule: int):
        path = app.root + "/read.log"
        file = open(path, "a", encoding="utf=8")
        file.write("%s?%d\r" % (book_path, schedule))
        file.close()

    @staticmethod
    def get_last_book():
        """读取阅读记录中的最后一条记录的文件路径"""
        path = app.root + "/read.log"
        if not os.path.isfile(path):
            open(path, "w", encoding="utf=8").close()
        file = open(path, "r", encoding="utf=8")
        lines = file.readlines()
        book_path = ""
        if len(lines) != 0:
            book_path = lines[-1].split("?")[0]
        file.close()
        return book_path


if __name__ == "__main__":
    log = ReadLog()
    print(log.read_schedule("D:/Downloads/仙逆-贴吧精校版.txt"))
