#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Util
"""
from .compat import *
import os
import sys
import re
import time
import subprocess
import hashlib
import hmac
import base64
import random
from .RayvisionException import RayvisionError

cg_id_name_dict = {
    'Maya': '2000',
    '3ds Max': '2001',
    'Lightwave': '2002',
    'Arnold Standalone': '2003',
    'Houdini': '2004',
    'Cinema 4D': '2005',
    'Softimage': '2006',
    'Blender': '2007',
    'VR Standalone': '2008',
    'MR Standalone': '2009',
    'SketchUp': '2010',
    'VUE': '2011',
    'Keyshot': '2012',
    'Clarisse': '2013',
    'Octane Render': '2014',
    'Nuke': '2015',
    'Katana': '2016',
    '2000': 'Maya',
    '2001': '3ds Max',
    '2002': 'Lightwave',
    '2003': 'Arnold Standalone',
    '2004': 'Houdini',
    '2005': 'Cinema 4D',
    '2006': 'Softimage',
    '2007': 'Blender',
    '2008': 'VR Standalone',
    '2009': 'MR Standalone',
    '2010': 'SketchUp',
    '2011': 'VUE',
    '2012': 'Keyshot',
    '2013': 'Clarisse',
    '2014': 'Octane Render',
    '2015': 'Nuke',
    '2016': 'Katana'
}


def get_os():
    """
    sys.platform:
        Linux (2.x and 3.x)     'linux2'
        Windows                 'win32'
        Windows/Cygwin          'cygwin'
        Mac OS X                'darwin'
        OS/2                    'os2'
        OS/2 EMX                'os2emx'
        RiscOS                  'riscos'
        AtheOS                  'atheos'
    :return: windows/linux
    :rtype: str
    """
    if sys.platform.startswith('win'):
        local_os = 'windows'
    elif sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
        local_os = 'linux'
    else:
        local_os = 'windows'
    return local_os


def hump2underline(hump_str):
    """
    将驼峰形式字符串转成下划线形式
    :param str hump_str: 驼峰形式字符串
    :return: 字母全小写的下划线形式字符串
    :rtype: str
    """
    patt = re.compile(r'([a-z]|\d)([A-Z])')
    underline_str = re.sub(patt, r'\1_\2', hump_str).lower()
    return underline_str
    

def str2unicode(str1, str_decode='default'):
    if not isinstance(str1, str):
        try:
            if str_decode != 'default':
                str1 = str1.decode(str_decode.lower())
            else:
                try:
                    str1 = str1.decode('utf-8')
                except:
                    try:
                        str1 = str1.decode('gbk')
                    except:
                        str1 = str1.decode(sys.getfilesystemencoding())
        except Exception as e:
            print('[err]str2unicode:decode %s to str failed' % (str1))
            print(e)
    return str1

    
def unicode2str(str1, str_encode='system'):
    if isinstance(str1, str):
        try:
            if str_encode.lower() == 'system':
                str1 = str1.encode(sys.getfilesystemencoding())
            elif str_encode.lower() == 'utf-8':
                str1 = str1.encode('utf-8')
            elif str_encode.lower() == 'gbk':
                str1 = str1.encode('gbk')
            else:
                str1 = str1.encode(str_encode)
        except Exception as e:
            print('[err]unicode2str:encode %s to %s failed' % (str1, str_encode))
            print(e)
    else:
        print('%s is not str ' % (str1))
    return str1

def print_sth(sth):
    print(sth)
    
def decorator_use_in_class(log_obj=None):
    if log_obj is None:
        log = print_sth
    else:
        log = log_obj.info
        
    def wrapper(f):
        def _wrapper(self, *args, **kwargs):
            log_info_start = r'[{0}.{1}.start.....]'.format(self.__class__.__name__, f.__name__)
            log_info_end = r'[{0}.{1}.end.....]'.format(self.__class__.__name__, f.__name__)
            log(log_info_start)
            out = f(self,*args, **kwargs)
            log(log_info_end)
            return out
        return _wrapper
    return wrapper
    

def format_time(format='%Y%m%d%H%M%S'):
    return time.strftime(format, time.localtime())
    
    
def run_cmd(cmd_str, my_shell=True, log_obj=None):
    """
    Run cmd.
    """
    if log_obj is not None:
        log_obj.info(u'cmd...{0}'.format(str2unicode(cmd_str)))
        
    if is_py2:
        cmd_str = str2unicode(cmd_str)
        cmd_str = cmd_str.encode(sys.getfilesystemencoding())
        
    cmdp = subprocess.Popen(cmd_str, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=my_shell)

    while True:
        result_line = cmdp.stdout.readline()
        if result_line:  # not EOF
            result_line = result_line.strip()
            if result_line:  # not empty line
                if log_obj is not None:
                    result_line = str2unicode(result_line)
                    log_obj.info(result_line)
        else:
            break

    return True
    
    