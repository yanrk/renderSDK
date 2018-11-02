# -*-coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import os
import io
import re
import sys
import json
import subprocess
from renderSDK.compat import *

try:
    from configparser import RawConfigParser
except ImportError:
    from ConfigParser import RawConfigParser

VERSION = sys.version_info[0]


def ini2dict(path, node):
    parse = open_ini(path)
    d = parse._sections[node]
    return d


def open_ini(path):
    encodings = ["utf-16", "utf-8", None]
    for i, encoding in enumerate(encodings):
        try:
            parse = RawConfigParser()
            with io.open(path, encoding=encoding) as fp:
                parse.readfp(fp)
                # parse.read(path, encoding=encoding)
            return parse
        except (UnicodeDecodeError, UnicodeError) as e:
            if i == len(encodings) - 1:
                raise Exception("can't load {0}\n{1}".format(path, e))
            continue


def json_load(json_path, encoding='utf-8'):
    p = json_path
    mode = 'r'
    with io.open(p, mode, encoding=encoding) as fp:
        d = json.load(fp)

    return d


def json_save(json_path, obj, encoding='utf-8', ensure_ascii=True):
    p = json_path
    mode = 'w'
    indent = 2
    with io.open(p, mode, encoding=encoding) as fp:
        if VERSION == 3:
            json.dump(obj, fp, ensure_ascii=ensure_ascii, indent=indent)
        else:
            fp.write(unicode(json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent)))


def write(path, content, mode="w", encoding="utf-8"):
    with io.open(path, mode, encoding=encoding) as fp:
        fp.write(content)


def read(path, encoding="utf-8"):
    with io.open(path, "r", encoding=encoding) as fp:
        content = fp.read()
    return content


def ensure_str(string):
    if type(string) == bytes:
        try:
            string = string.decode("utf-8")
        except UnicodeDecodeError as e:
            string = string.decode("gbk")
    return string


def write_cfg(parser, cfg_path):
    encodings = ("utf-8", None)
    for index, encoding in enumerate(encodings):
        try:
            with io.open(cfg_path, "w", encoding=encoding) as fp:
                parser.write(fp)
        except (UnicodeEncodeError, UnicodeError) as e:
            if index == len(encodings) - 1:
                print("save cfg error", e)
            continue


def _inter_path(path):
    first_two = path[0:2]
    if first_two in ('//', '\\\\'):
        norm_path = path.replace('\\', '/')
        index = norm_path.find('/', 2)
        if index <= 2:
            return False
        return True


def _parse_inter_path(path):
    first_two = path[0:2]
    if first_two in ('//', '\\\\'):
        norm_path = path.replace('\\', '/')
        index = norm_path.find('/', 2)
        if index <= 2:
            return ''
        return path[:index], path[index:]


def convert_path(user_input, path):
    """
    :param user_input: e.g. "/1021000/1021394"
    :param path: e.g. "D:/work/render/19183793/max/d/Work/c05/111409-021212132P-embedayry.jpg"
    :return: \1021000\1021394\D\work\render\19183793\max\d\Work\c05\111409-021212132P-embedayry.jpg
    """
    result_file = path
    lower_file = os.path.normpath(path.lower()).replace('\\', '/')
    file_dir = os.path.dirname(lower_file)
    if file_dir is None or file_dir.strip() == '':
        pass
    else:
        if _inter_path(lower_file) is True:
            start, rest = _parse_inter_path(lower_file)
            # result_file = user_input + '/net/' + start.replace('//', '') + rest.replace('\\', '/')
            result_file = user_input + start + rest.replace('\\', '/')
        else:
            result_file = user_input + '\\' + path.replace('\\', '/').replace(':', '')

    result = os.path.normpath(result_file)
    result = result.replace("\\", "/")
    return result


def transcoding(render_task_cfg):
    path = render_task_cfg
    target = "utf-16"
    es = ["utf-16", 'utf-16-le', 'utf-16-be', "utf-8", "gbk", None]
    for encoding in es:
        try:
            content = read(path, encoding=encoding)
            write(path, content, encoding=target)
            return
        except (UnicodeDecodeError, UnicodeError) as e:
            continue


def wrap_subprocess(cmd):
    """用于把脚本打包成exe的时候方便修改subprocess"""
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, startupinfo=si)
    return p


def check_contain_chinese(string):
    pattern = re.compile('[\u4e00-\u9fa5]+')
    match = pattern.search(string)
    if match:
        return True
    else:
        return False


def test_convert_path():
    p1 = r"\\10.60.100.101\s\scene\as\qq.jpg"
    p2 = r"d:/xx/bbb/xxx.jpg"
    assert convert_path("", p1) == "//10.60.100.101/s/scene/as/qq.jpg"
    assert convert_path("", p2) == "/d/xx/bbb/xxx.jpg"


def main():
    pass
    test_convert_path()


if __name__ == '__main__':
    pass
    main()
