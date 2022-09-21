import logging

from logging import handlers

# import colorlog as colorlog

from py_core.base0core import CORE_PARENT_PATH
# from handlerFile import HandlerFile
from py_core.handlerFile import HandlerFile


class Logger(object):

    # 日志级别关系映射
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }

    def __init__(self,
                 filename=f"{CORE_PARENT_PATH}/logs/all.log",
                 level='info',
                 when='D',
                 backCount=3,
                 fmt='%(asctime)s-%(filename)s[#%(lineno)d]-%(levelname)s: %(message)s'):
        obj_file = HandlerFile(filename)
        obj_file.create_file(bak=True)

        self.logger = logging.getLogger(filename)

        # 设置日志格式
        self.log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }
        # fmt_str = colorlog.ColoredFormatter('%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
        #                                     log_colors=self.log_colors_config)
        # fmt_str = '%(asctime)s-%(filename)s[#%(lineno)d]-%(levelname)s: %(message)s'
        fmt_str = '%(asctime)s-%(filename)s-%(levelname)s: %(message)s'
        fmt = logging.Formatter(fmt_str)

        # 设置日志级别
        self.logger.setLevel(self.level_relations.get(level))

        # # 往屏幕上输出
        # sh = logging.StreamHandler()
        # # 设置屏幕上显示的格式
        # sh.setFormatter(fmt)
        # self.logger.addHandler(sh)
        # 往文件里写入#指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8')
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨

        # 设置文件里写入的格式
        th.setFormatter(fmt)
        # 把对象加到logger里
        self.logger.addHandler(th)


logger = Logger().logger


if __name__ == '__main__':
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")

    pass
