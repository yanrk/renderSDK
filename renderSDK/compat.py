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
        """ If the input is unicode, it will be converted to utf-8 encoded bytes; others will be returned to original way. """
        if isinstance(data, unicode):
            return data.encode('utf-8')
        else:
            return data


    def to_string(data):
        """Convert input to str object"""
        return to_bytes(data)


    def to_unicode(data):
        """Convert the input to unicode, input is required to be unicode or utf-8 encoded bytes."""
        if isinstance(data, bytes):
            return data.decode('utf-8')
        else:
            return data


    def stringify(input):
        """If the string sub-object in the input object is unicode encoded, it is converted to a byte of utf-8; the other is returned as it is."""
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
        """If the input is str (ie unicode), it will be converted to utf-8 encoded bytes; others will return as they are."""
        if isinstance(data, str):
            return data.encode(encoding='utf-8')
        else:
            return data


    def to_string(data):
        """If the input is bytes, it is considered to be utf-8 encoding, and returns str"""
        if isinstance(data, bytes):
            return data.decode('utf-8')
        else:
            return data


    def to_unicode(data):
        """Convert the input to unicode, input is required to be unicode or utf-8 encoded bytes."""
        return to_string(data)


    def stringify(input):
        return input


    builtin_str = str
    bytes = bytes
    str = str
    
    long = int
