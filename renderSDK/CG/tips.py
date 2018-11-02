# -*-coding: utf-8 -*-
import os
import time
import sys
import glob
import json
import shutil
from pprint import pprint

from renderSDK.compat import *
from renderSDK.CG import util


class Tips(object):
    def __init__(self, save_path=None):
        self._tips_list = {}
        self.path = save_path

    def add(self, key, *values):
        if key in self._tips_list:
            for v in values:
                self._tips_list[key].append(v)
        else:
            self._tips_list[key] = list(values)

    def set(self, key, value):
        self._tips_list[key] = value

    def save(self, path=None):
        if path is None:
            if self.path is not None:
                path = self.path
            else:
                raise Exception("The Tips' path is not defined")

        filename = os.path.join(path, "tips.json")
        util.json_save(filename, self._tips_list, ensure_ascii=False)

    def save_and_exit(self, path, exit_code=-1):
        self.save(path)
        sys.exit(exit_code)


def main():
    pass


if __name__ == '__main__':
    pass
    main()
