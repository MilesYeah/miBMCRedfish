#!/usr/bin/python3

import os.path


class HandlerFolder(object):
    def __init__(self, dp):
        self._dp = dp

    @property
    def dir_path(self):
        """
        directory path
        :return:
        """
        return self._dp

    @dir_path.setter
    def dir_path(self, dp):
        self._dp = dp

    @property
    def is_exists(self):
        return True if os.path.exists(self.dir_path) else False

    def create_dir(self, dp=None):
        target = dp if dp else self.dir_path
        if not os.path.exists(target):
            os.mkdir(target)

    @property
    def is_dir(self):
        return True if os.path.isdir(self.dir_path) else False

    @property
    def current_files(self):
        for dir_path, dirs, files in os.walk(self.dir_path):
            return files

    @property
    def current_folders(self):
        for dir_path, dirs, files in os.walk(self.dir_path):
            return dirs

    @property
    def gene_contents(self):
        for dir_path, dirs, files in os.walk(self.dir_path):
            for f in files:
                yield os.path.join(dir_path, f)


if __name__ == "__main__":
    a = HandlerFolder(".")
    b = HandlerFolder("./abc/")

    pass
