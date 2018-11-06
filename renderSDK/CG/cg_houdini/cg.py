# -*-coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os
import re
import time
import sys
import traceback

try:
    import _winreg
except ImportError:
    import winreg as _winreg

from renderSDK.CG.cg_base import CGBase
from renderSDK.CG import util
from renderSDK.CG import tips_code
from renderSDK.CG.exception import *
from renderSDK.CG.message import *

VERSION = sys.version_info[0]
basedir = os.path.abspath(os.path.dirname(__file__))
"""
D:/Program Files/Side Effects Software/Houdini 16.5.268/bin/hython.exe D:/api/HfsBase.py -project "E:/houdini_test/sphere.hip" -task "D:/api/out/task.json" -asset "D:/api/out/asset.json" -tips "D:/api/out/tips.json"
"""


class Houdini(CGBase):
    def __init__(self, *args, **kwargs):
        super(Houdini, self).__init__(*args, **kwargs)
        self.exe_name = "hython.exe"
        self.name = "Houdini"

        self.init()

    def init(self):
        pass

    def location_from_reg(self, version):
        log = self.log
        version_str = "{0} {1}".format(self.name, version)

        location = None

        string = 'SOFTWARE\Side Effects Software\{0}'.format(version_str)
        log.debug(string)
        try:
            handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, string)
            location, type = _winreg.QueryValueEx(handle, "InstallPath")
            log.debug("{0} {1}".format(location, type))

        except (WindowsError, FileNotFoundError) as e:
            msg = traceback.format_exc()
            log.error(msg)

        return location

    @staticmethod
    def get_save_version(hipfile=""):
        if os.path.exists(hipfile):
            with open(hipfile, "rb") as hipf:
                not_find = True
                search_elm = 2
                search_elm_cunt = 0
                while not_find:
                    line = str(hipf.readline()).encode("utf-8")
                    if "set -g _HIP_SAVEVERSION = " in str(line):
                        # print(str(line))
                        pattern = re.compile("\d+\.\d+\.\d+\.?\d+")
                        _HV = pattern.findall(str(line))
                        _hfs_save_version = _HV[0]
                        search_elm_cunt += 1

                    # The $HIP val with this file saved
                    if "set -g HIP = " in str(line):
                        pattern = re.compile("\\'.*\\'") if sys.version[:1] == "2" else re.compile(r"\\'.*\\'")
                        _Hip = pattern.search(str(line)).group()
                        _hip_save_val = _Hip.split("\'")[1].replace("\\", "/")
                        search_elm_cunt += 1
                    if search_elm_cunt >= search_elm:
                        not_find = False
        else:
            print("The .hip file is not exist.")
            _hfs_save_version, _hip_save_val = ("", "")
        return _hfs_save_version, _hip_save_val

    def pre_analyse_custom_script(self):
        super(Houdini, self).pre_analyse_custom_script()

    def find_location(self):
        log = self.log
        location = self.location_from_reg(self.version)
        exe_path = self.exe_path_from_location(os.path.join(location, "bin"), self.exe_name)
        if exe_path is None:
            self.tips.add(tips_code.cg_notexists, self.version_str)
            self.tips.save()
            raise CGExeNotExistError(error9899_cgexe_notexist.format(self.name))

        self.exe_path = exe_path
        log.info("exe_path: {0}".format(exe_path))

    def analyse_cg_file(self):
        log = self.log
        version = self.get_save_version(self.cg_file)[0]
        log.info("version: {0}".format(version))
        self.version = version
        self.version_str = "{0} {1}".format(self.name, version)

        if self.custom_exe_path is not None:
            self.exe_path = self.custom_exe_path
        else:
            self.find_location()

    def valid(self):
        super(Houdini, self).valid()

    def dump_task_json(self):
        super(Houdini, self).dump_task_json()

    def analyse(self):
        script_name = "HfsBase.py"
        script_full_path = os.path.join(os.path.dirname(__file__), script_name)
        task_path = self.job_info._task_json_path
        asset_path = self.job_info._asset_json_path
        tips_path = self.job_info._tips_json_path

        cmd = '"{exe_path}" "{script_full_path}" -project "{cg_file}" -task "{task_path}" -asset "{asset_path}" -tips "{tips_path}"'.format(
            exe_path=self.exe_path,
            script_full_path=script_full_path,
            cg_file=self.cg_file,
            task_path=task_path,
            asset_path=asset_path,
            tips_path=tips_path,
        )
        returncode, stdout, stderr = self.cmd.run(cmd, shell=True)
        self.log.info("returncode: {0}".format(returncode))
        if returncode != 0:
            self.tips.add(tips_code.unknow_err)
            self.tips.save()
            raise RayvisionError("analyse fail.")

    def load_output_json(self):
        # super().load_output_json()
        super(Houdini, self).load_output_json()

    def handle_analyse_result(self):
        upload_asset = []

        asset_json = self.asset_json
        normal = asset_json["Normal"]
        ## eg. asset = {"Normal":{"node1":["nodename",["files"]],"node2":["nodename",["files"]]},
        ##                    "Miss":{"node1":["nodename",["files"]],"node2":["nodename",["files"]]}}

        for _, value in normal.items():
            path_list = value[-1]

            for path in path_list:
                d = {}
                local = path
                server = util.convert_path("", local)
                d["local"] = local.replace("\\", "/")
                d["server"] = server
                upload_asset.append(d)

        # handle upload.json
        upload_asset.append({
            "local": self.cg_file.replace("\\", "/"),
            "server": util.convert_path("", self.cg_file)
        })

        upload_json = {}
        upload_json["asset"] = upload_asset

        self.upload_json = upload_json
        self.job_info._upload_info = upload_json

        util.json_save(self.job_info._upload_json_path, upload_json)

    def write_cg_path(self):
        # super().write_cg_path()
        super(Houdini, self).write_cg_path()

    def run(self):
        # run a custom script if exists
        self.pre_analyse_custom_script()
        # Get scene information
        self.analyse_cg_file()
        # Basic check (whether the version of the project configuration and the version of the scenario match, etc.)
        self.valid()
        # Set job_info.task_info dump into a file
        self.dump_task_json()
        # Run CMD startup analysis (find the path of CG through configuration information, the path of CG can be customized)
        self.analyse()
        # Read the three json of the analysis result into memory
        self.load_output_json()
        #Write task configuration file (custom information, independent upload list), compress specific files (compress files, upload path, delete path)
        self.handle_analyse_result()
        # Write cg_file and cg_id to task_info
        self.write_cg_path()

        self.log.info("analyse end.")
