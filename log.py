from app_attribute import AppAttribute as app


class ReadLog(object):

    @staticmethod
    def get_schedule(book_path) -> int:
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
    def set_schedule(book_path: str, schedule: int):
        path = app.root + "/read.log"
        file = open(path, "a", encoding="utf=8")
        file.write("%s?%d\r" % (book_path, schedule))
        file.close()


if __name__ == "__main__":
    log = ReadLog()
    print(log.get_schedule("D:/Downloads/仙逆-贴吧精校版.txt"))
