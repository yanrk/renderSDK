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

job_status_description_dict = {
    "0":{
        "0":"等待中",
        "1":"Waiting"
    },
    "5":{
        "0":"渲染中",
        "1":"Rendering"
    },
    "8":{
        "0":"预处理中",
        "1":"Preprocessing"
    },
    "10":{
        "0":"停止",
        "1":"Stop"
    },
    "20":{
        "0":"欠费停止",
        "1":"Arrearage-stop"
    },
    "23":{
        "0":"超时停止",
        "1":"Timeout stop"
    },
    "25":{
        "0":"已完成",
        "1":"Done"
    },
    "30":{
        "0":"已完成(有失败帧)",
        "1":"Done(with failed frame)"
    },
    "35":{
        "0":"放弃",
        "1":"Abort"
    },
    "40":{
        "0":"等待全速渲染",
        "1":"Test done"
    },
    "45":{
        "0":"失败",
        "1":"Failed"
    }
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
    Convert the hump  form string to an underscore
    :param str hump_str: hump  form string
    :return: All lowercase underlined string of letters
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
            print('[err]str2unicode:decode failed')
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
            print('[err]unicode2str:encode failed')
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
    
    
def get_job_status_description(job_status_code=None, job_status_text=None, language='1'):
    """
    Input job_status_code or job_status_text to get job status description.
    :param str job_status_code: "40"
    :param str job_status_text: "render_task_status_40"
    :param str language: "0": Simplified Chinese; "1": English
    """
    job_status_code = job_status_code
    if job_status_text is not None:
        job_status_code = job_status_text.split('_')[-1]
        
    if job_status_code is None:
        raise RayvisionError(1000000, r'Please input job_status_code or job_status_text!')
    
    job_status_description = job_status_description_dict.get(str(job_status_code), {}).get(str(language), '')
    if job_status_description == '':
        print('[warn]Get empty job_status_description, Please check the input.')
    
    return job_status_description
    