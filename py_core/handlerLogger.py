#!/usr/bin/python3

import logging

from logging import handlers

import colorlog as colorlog

from py_core.base0core import CORE_PARENT_PATH
from py_core.handlerFile import HandlerFile

# 日志级别关系映射
LEVEL_RELATIONS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'crit': logging.CRITICAL
}

# 定义不同日志等级颜色
LOG_COLORS_CONFIG = {
    'DEBUG': 'bold_cyan',
    'INFO': 'bold_green',
    'WARNING': 'bold_yellow',
    'ERROR': 'bold_red',
    'CRITICAL': 'red',
}


class Logger(logging.Logger):

    def __init__(self,
                 name="logger",
                 level='info',
                 filename=f"{CORE_PARENT_PATH}/logs/all.log",
                 when='D',
                 back_count=3):
        super().__init__(name)

        obj_file = HandlerFile(filename)
        obj_file.create_file(bak=True)

        self.level = LEVEL_RELATIONS.get(level)
        # self.logger = logging.getLogger(filename)

        # fmt_str = colorlog.ColoredFormatter('%(log_color)s[%(asctime)s] [%(name)s] [%(levelname)s]: %(message)s',
        #                                     log_colors=self.log_colors_config)
        # fmt_str = '%(asctime)s-%(filename)s[#%(lineno)d]-%(levelname)s: %(message)s'
        fmt_str = '%(asctime)s-%(filename)s-%(levelname)s: %(message)s'
        fmt = logging.Formatter(fmt_str)

        # formatter = colorlog.ColoredFormatter(
        #     '%(log_color)s%(levelname)1.1s %(asctime)s %(reset)s| '
        #     '%(message_log_color)s%(levelname)-8s %(reset)s| '
        #     '%(log_color)s[%(filename)s%(reset)s:%(log_color)s%(module)s%(reset)s:%(log_color)s%(funcName)s%(reset)s:%(log_color)s%(''lineno)d] %(reset)s- '
        #     '%(white)s%(message)s',
        #     reset=True,
        #     log_colors=LOG_COLORS_CONFIG,
        #     secondary_log_colors={
        #         'message': {
        #             'DEBUG': 'blue',
        #             'INFO': 'blue',
        #             'WARNING': 'blue',
        #             'ERROR': 'red',
        #             'CRITICAL': 'bold_red'
        #         }
        #     },
        #     style='%'
        # )  # 日志输出格式
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(levelname)1.1s %(asctime)s %(reset)s| '
            '%(message_log_color)s%(levelname)-8s %(reset)s| '
            '%(log_color)s%(filename)s%(reset)s:%(log_color)s%(lineno)d %(reset)s- '
            '%(white)s%(message)s',
            reset=True,
            log_colors=LOG_COLORS_CONFIG,
            secondary_log_colors={
                'message': {
                    'DEBUG': 'blue',
                    'INFO': 'blue',
                    'WARNING': 'blue',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red'
                }
            },
            style='%'
        )  # 日志输出格式


        # # 设置日志级别
        # self.setLevel(LEVEL_RELATIONS.get(level))

        # 往文件里写入#指定间隔时间自动生成文件的处理器
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=back_count, encoding='utf-8')
        th.setFormatter(fmt)
        th.setLevel(self.level)
        self.addHandler(th)

        # 往屏幕上输出
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        sh.setLevel(self.level)
        self.addHandler(sh)


logger = Logger()


if __name__ == '__main__':
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
    logger.critical("critical")

    pass
