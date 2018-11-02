#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys

__all__ = ['json', 'is_py2', 'is_py3', 'urlquote', 'urlunquote', 'urlparse', 'urllib2', 'to_bytes',
           'to_unicode', 'stringify', 'builtin_str', 'bytes', 'str', 'configparser', 'long']

try:
    import simplejson as json
except (ImportError, SyntaxError):
    import json

_py_ver = sys.version_info
is_py2 = (_py_ver[0] == 2)
is_py3 = (_py_ver[0] == 3)

if is_py2:    
    reload(sys)
    sys.setdefaultencoding('utf-8')

    from urllib import quote as urlquote, unquote as urlunquote
    from urlparse import urlparse
    import urllib2
    import ConfigParser as configparser


    def to_bytes(data):
        """若输入为unicode， 则转为utf-8编码的bytes；其他则原样返回。"""
        if isinstance(data, unicode):
            return data.encode('utf-8')
        else:
            return data


    def to_string(data):
        """把输入转换为str对象"""
        return to_bytes(data)


    def to_unicode(data):
        """把输入转换为unicode，要求输入是unicode或者utf-8编码的bytes。"""
        if isinstance(data, bytes):
            return data.decode('utf-8')
        else:
            return data


    def stringify(input):
        """若输入对象中的字符串子对象为unicode编码，则转成utf-8的bytes；其他则原样返回。"""
        if isinstance(input, dict):
            return dict([(stringify(key), stringify(value)) for key, value in input.iteritems()])
        elif isinstance(input, list):
            return [stringify(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input


    builtin_str = str
    bytes = str
    str = unicode

    long = long

elif is_py3:
    from urllib.parse import quote as urlquote, unquote as urlunquote
    from urllib.parse import urlparse
    import urllib.request as urllib2
    import configparser

    def to_bytes(data):
        """若输入为str（即unicode），则转为utf-8编码的bytes；其他则原样返回"""
        if isinstance(data, str):
            return data.encode(encoding='utf-8')
        else:
            return data


    def to_string(data):
        """若输入为bytes，则认为是utf-8编码，并返回str"""
        if isinstance(data, bytes):
            return data.decode('utf-8')
        else:
            return data


    def to_unicode(data):
        """把输入转换为unicode，要求输入是unicode或者utf-8编码的bytes。"""
        return to_string(data)


    def stringify(input):
        return input


    builtin_str = str
    bytes = bytes
    str = str
    
    long = int
