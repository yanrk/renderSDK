# -*-coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os
import time
import sys
import glob
import shutil
import traceback
from pprint import pprint
try:
    import _winreg
except ImportError:
    import winreg as _winreg

from renderSDK.CG.cg_base import CGBase
from renderSDK.CG import util
from renderSDK.CG import tips_code
from renderSDK.CG.exception import *
from renderSDK.CG.message import *

"""C4D
cmd:
"C:\Program Files\MAXON\CINEMA 4D R15\CINEMA 4D 64 Bit.exe" -task_id=65368 -cg_file="\\10.60.100.104\new_render_data\input\d\render_data\100000\100461\F\R15_test.c4d" -task_json="c:\work\render\65368\cfg\task.json" -asset_json="c:\work\render\65368\cfg\asset.json" -tips_json="c:\work\render\65368\cfg\tips.json"

Parameter Description:
1. Software ("C:\Program Files\MAXON\CINEMA 4D R15\CINEMA 4D 64 Bit.exe")
2. Task id (-task_id)
3. Source file (-cg_file)
4.task_json
5.asset_json
6.tips_json

"""

VERSION = sys.version_info[0]


class C4D(CGBase):
    def __init__(self, *args, **kwargs):
        super(C4D, self).__init__(*args, **kwargs)
        self.exe_name = "CINEMA 4D 64 Bit.exe"
        self.name = "C4D"

        self.init()

    def init(self):
        pass

    def location_from_reg(self, version):
        version_str = "{0} {1}".format(self.name, version)

        location = None

        string = 'SOFTWARE\MC4D'.format(version_str)
        log.info(string)
        try:
            handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, string)
            location, type = _winreg.QueryValueEx(handle, "InstallPath")
            log.info("{0} {1}".format(location, type))

        except FileNotFoundError as e:
            msg = traceback.format_exc()
            log.error(msg)

        return location

    def pre_analyse_custom_script(self):
        super(C4D, self).pre_analyse_custom_script()

    def analyse_cg_file(self):
        if VERSION == 3:
            version = self.check_version(self.cg_file)
        else:
            version = self.check_version1(self.cg_file)
        version = str(version)
        self.version = str(version)
        self.version_str = "{0} {1}".format("C4D", version)

        location = self.location_from_reg(version)
        exe_path = self.exe_path_from_location(os.path.join(location, "bin"), self.exe_name)
        if exe_path is None:
            self.tips.add(tips_code.cg_notexists, self.version_str)
            self.tips.save()
            raise CGExeNotExistError(error9899_cgexe_notexist.format(self.name))

        self.exe_path = exe_path

    def valid(self):
        super(C4D, self).valid()

    def dump_task_json(self):
        super(C4D, self).dump_task_json()

    def analyse(self):
        script_full_path = os.path.join(os.path.dirname(__file__), "analyse_houdini.py")
        # cmd = '"D:/plugins/C4D/160504/bin/hython.exe c:/script/new_py/CG/C4D/script/analyse.py -project "E:/houdini_maya/houdini_maya/untitled.hip" -outdir "c:/work/render/4431""'
        cmd = '"{exe_path}" "{script_full_path}" -project "{cg_file}" -outdir "{output_path}"'.format(
            exe_path=exe_path,
            script_full_path=script_full_path,
            cg_file=self.cg_file,
            output_path=output_path,
        )

    def load_output_json(self):
        # super().load_output_json()
        super(C4D, self).load_output_json()

    def handle_analyse_result(self):
        upload_asset = []

        asset_json = self.asset_json
        assets = asset_json["asset"]
        for asset_dict in assets:
            path_list = asset_dict["path"]

            for path in path_list:
                d = {}
                local = path
                server = util.convert_path(self.user_input, local)
                d["local"] = local
                d["server"] = server
                upload_asset.append(d)

        # Add the cg file to upload.json
        upload_asset.append({
            "local": self.cg_file,
            "server": util.convert_path(self.user_input, self.cg_file)
        })

        upload_json = {}
        upload_json["asset"] = upload_asset

        self.upload_json = upload_json
        self.job_info._upload_info = upload_json

        util.json_save(self.job_info._upload_json_path, upload_json)

    def write_cg_path(self):
        # super().write_cg_path()
        super(C4D, self).write_cg_path()

    def post_analyse_custom(self):
        pass

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
        #
        self.post_analyse_custom()
