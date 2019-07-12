import logging


# 日志格式化输出
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# 日期格式
DATE_FORMAT = "%m/%d/%Y %H:%M:%S %p"

# 仅仅把警告以上的写入日志文件
fp = logging.FileHandler("a.txt", "w", encoding="utf-8")
fp.setLevel(logging.WARNING)

# 日志信息全部输出到控制台
fs = logging.StreamHandler()
fs.setLevel(logging.DEBUG)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=DATE_FORMAT, handlers=[fp, fs])
