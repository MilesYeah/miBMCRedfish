import glob
import json
import logging
import os
import re
import shutil

import yaml

from py_core.handlerDatetime import timestamp2datetime, str2datetime, datetime2str
# from handlerLogger import logger


class SheetNotFoundError(Exception):
    pass


def save_binary_to_file(bytes, fpn):
    """将二进制内容存储到文件"""
    fp, fn = os.path.split(fpn)
    if not os.path.exists(fp):
        os.mkdir(fp)
    with open(fpn, 'wb') as f:
        f.write(bytes)


class FileState(object):
    def __init__(self, stat):
        self._stat = stat

    @property
    def stat(self):
        return self._stat

    @property
    def f_time_a(self):
        return timestamp2datetime(self.stat.st_atime)

    @property
    def s_time_a(self):
        return datetime2str(self.f_time_a)

    @property
    def f_time_c(self):
        return timestamp2datetime(self.stat.st_ctime)

    @property
    def s_time_c(self):
        return datetime2str(self.f_time_c)

    @property
    def f_time_m(self):
        return timestamp2datetime(self.stat.st_mtime)

    @property
    def s_time_m(self):
        return datetime2str(self.f_time_m)


class FileContent(object):
    def __init__(self, content):
        self._stat = content


class HandlerFile(object):
    def __init__(self, fpn: str, encoding="utf-8"):
        self._fpn = fpn
        self.encoding = encoding

    @property
    def fpn(self):
        if self._fpn:
            return os.path.abspath(self._fpn)

    @property
    def fp(self):
        if self.fpn:
            return os.path.split(self.fpn)[0]

    @property
    def fn(self):
        if self.fpn:
            return os.path.split(self.fpn)[1]

    @property
    def file_exists(self):
        if os.path.exists(self.fpn):
            return True

    @property
    def file_type(self):
        if re.findall("json$", self.fpn, re.I):
            return "json"
        elif re.findall("y[a]?ml$", self.fpn, re.I):
            return "yaml"
        elif re.findall("xls[x]?$", self.fpn, re.I):
            return "excel"
        elif re.findall("ini$", self.fpn, re.I):
            return "ini"
        else:
            return

    # @property
    # def content_raw(self):
    #     if self.file_exists:
    #         with open(self.fpn, encoding=self.encoding, mode='r') as f:
    #             return f

    @property
    def content(self):
        if self.file_exists:
            with open(self.fpn, encoding=self.encoding, mode='r') as f:
                return f.read()

    @property
    def content_lines(self):
        if self.file_exists:
            with open(self.fpn, encoding=self.encoding, mode='r') as f:
                return [line.strip("\n") for line in f.readlines()]

    @property
    def file_stat(self):
        if self.file_exists:
            return FileState(os.stat(self.fpn))

    def create_file(self, bak=False):
        if bak is True:
            if self.file_exists:
                fn_new = f"{self.fn}.{str(self.file_stat.s_time_m)}.bak"
                fpn_new = os.path.join(self.fp, fn_new)
                shutil.move(self.fpn, fpn_new)
                pass

        if not self.file_exists:
            if not os.path.exists(self.fp):
                os.mkdir(self.fp)
            with open(self.fpn, encoding=self.encoding, mode='w') as f:
                logging.info(f"Successfully created {self.fpn}")

    def save_file(self):
        pass

    def remove_file(self):
        if self.file_exists:
            os.remove(self.fpn)



if __name__ == "__main__":
    a = HandlerFile("aaa.log")
    a.create_file(bak=True)

    pass
