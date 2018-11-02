# -*-coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals
import sys
import logging
import subprocess

from renderSDK.CG import util
from renderSDK.compat import *

VERSION = sys.version_info[0]
logger = logging.getLogger("analyse")


class Cmd(object):
    def __init__(self):
        pass

    def tasklist(self, filter=None):
        exe_name = filter
        if exe_name is not None:
            cmd = 'tasklist /FI "imagename eq {0}"'.format(exe_name)
        else:
            cmd = 'tasklist'
        returncode = self.run(cmd)
        return returncode

    def run(self, cmd, shell=False, log_output=True):
        # log = print
        log = logger.info

        log("run command:\n{0}".format(cmd))
        cmd = self.compatible(cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell)
        stdout, stderr = p.communicate()
        stdout = util.ensure_str(stdout)
        stderr = util.ensure_str(stderr)

        if log_output is True:
            log("stdout:\n{0}".format(stdout))
        if stderr:
            log("stderr:\n{0}".format(stderr))
        return p.returncode, stdout, stderr

    def power_run(self, cmd):
        pass

    def wrap_subprocess(self, cmd):
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        p = subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, startupinfo=si)
        return p

    def compatible(self, cmd):
        if VERSION == 3:
            pass
        else:
            cmd = unicode(cmd)
            cmd = cmd.encode(sys.getfilesystemencoding())
        return cmd


def main():
    cmd = Cmd()
    command = "tasklist"
    cmd.run(command)


if __name__ == '__main__':
    main()
