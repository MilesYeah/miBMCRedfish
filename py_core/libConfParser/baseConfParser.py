#!/usr/bin/python3

import json

import yaml

from py_core.handlerFile import HandlerFile
from py_core.handlerLogger import logger


class BaseConfParser(HandlerFile):
    def __init__(self, fpn, encoding="utf-8"):
        super().__init__(fpn, encoding)
        self._data_all = None

    def reload(self):
        if self.file_exists:
            with open(self.fpn, mode='r', encoding=self.encoding) as f:
                if self.file_type == "json":
                    try:
                        self._data_all = json.load(f)
                    except json.decoder.JSONDecodeError as e:
                        self._data_all = None
                        logger.error(f"Failed to load data from {self.fpn} for {e}")
                elif self.file_type == "yaml":
                    # loader可选择BaseLoader、SafeLoader、FullLoader、UnsafeLoader
                    self._data_all = yaml.load(f, Loader=yaml.BaseLoader)

    @property
    def data_all(self):
        if not self._data_all:
            self.reload()
        return self._data_all

    @property
    def data_group_names(self):
        if self.data_all:
            return self.data_all.keys()

    def get_group(self, group, default=None):
        if self.data_all:
            if group in self.data_all:
                return self.data_all.get(group, None)
            else:
                return default
