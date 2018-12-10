# -*-coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os
import re
import sys
import math
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


"""

options = {
    "cg_file": "d:/100000056/ocean13.mb",
    "task_json": "d:/100000056/2030/cfg/task.json",
    "task_id": "2030",
    "asset_json": "d:/100000056/2030/cfg/asset.json",
    "cg_project": "d:/100000056",
    "user_id": "100000056",
    "cg_plugins": {},
    "tips_json": "d:/100000056/2030/cfg/tips.json",
    "cg_version": "2015"
}

path = r"C:/Program Files/Autodesk/Maya2015/bin/mayabatch.exe"

script_path = 'c:/script/new_py/CG/Maya/script'

# cmd = '"{exe_path}" -command ""'

analyse_cmd = "\"%s\" -command \"python \\\"options=%s;" \
      "import sys;sys.path.insert(0, '%s');import Analyze;reload(Analyze);" \
      "Analyze.analyze_maya(options)\\\"" % \
      (path, options, script_path)

print(analyse_cmd)
"""

"""
Interface rendering, you need to seal the maya Analyze.py functions.
"""

VERSION = sys.version_info[0]


class Maya(CGBase):
    def __init__(self, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        super(Maya, self).__init__(*args, **kwargs)
        self.exe_name = "mayabatch.exe"
        self.name = "Maya"

        self.init()

    def init(self):
        """
        1. check filename
        """
        cg_file = self.cg_file
        if util.check_contain_chinese(cg_file):
            self.tips.add(tips_code.contain_chinese, cg_file)
            self.tips.save()
            raise FileNameContainsChineseError

    def check_version(self, cg_file):
        """Python3 version of check_version"""
        result = None
        if cg_file.endswith(".ma"):
            infos = []
            with open(cg_file, "rb") as f:
                while 1:
                    line = f.readline()
                    if line.startswith(b"createNode"):
                        break
                    elif line.strip() and not line.startswith(b"//"):
                        infos.append(line.strip())

            file_infos = [i for i in infos if i.startswith(b"fileInfo")]
            for i in file_infos:
                if b"product" in i:
                    r = re.findall(br'Maya.* (\d+\.?\d+)', i, re.I)
                    if r:
                        try:
                            result = int(r[0].split(b".")[0])
                        except Exception as e:
                            raise GetCGVersionError

        elif cg_file.endswith(".mb"):
            with open(cg_file, "rb") as f:
                info = f.readline()

            file_infos = re.findall(br'FINF\x00+\x11?\x12?K?\r?(.+?)\x00(.+?)\x00',
                                    info, re.I)
            for i in file_infos:
                if i[0] == b"product":
                    try:
                        result = int(i[1].split()[1])
                    except Exception as e:
                        raise GetCGVersionError
        return result

    def check_version1(self, cg_file):
        """Python2 version of check_version"""
        result = None
        if cg_file.endswith(".ma"):
            infos = []
            with open(cg_file, "rb") as f:
                while 1:
                    line = f.readline()
                    if line.startswith("createNode"):
                        break
                    elif line.strip() and not line.startswith("//"):
                        infos.append(line.strip())

            file_infos = [i for i in infos if i.startswith("fileInfo")]
            for i in file_infos:
                if "product" in i:
                    r = re.findall(r'Maya.* (\d+\.?\d+)', i, re.I)
                    if r:
                        try:
                            result = int(r[0].split(".")[0])
                        except Exception as e:
                            raise GetCGVersionError

        elif cg_file.endswith(".mb"):
            with open(cg_file, "rb") as f:
                info = f.readline()

            file_infos = re.findall(r'FINF\x00+\x11?\x12?K?\r?(.+?)\x00(.+?)\x00',
                                    info, re.I)
            for i in file_infos:
                if i[0] == "product":
                    try:
                        result = int(i[1].split()[1])
                    except Exception as e:
                        raise GetCGVersionError
        return result

    def location_from_reg(self, version):
        # for 2013/2013.5, 2016/2016.5
        versions = (version, "{0}.5".format(version))
        location = None
        for v in versions:
            string = 'SOFTWARE\Autodesk\Maya\{0}\Setup\InstallPath'.format(v)
            self.log.debug(string)
            try:
                handle = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, string)
                location, type = _winreg.QueryValueEx(handle, "MAYA_INSTALL_LOCATION")
                self.log.debug('localtion:{0}, type:{1}'.format(location, type))
                break
            except (WindowsError, FileNotFoundError) as e:
                self.log.debug(traceback.format_exc())
                pass

        return location

    def pre_analyse_custom_script(self):
        super(Maya, self).pre_analyse_custom_script()

    def analyse_cg_file(self):
        #Find the version from the cg file
        if VERSION == 3:
            version = self.check_version(self.cg_file)
        else:
            version = self.check_version1(self.cg_file)
        version = str(version)
        self.version = str(version)
        self.version_str = "{0} {1}".format(self.name, version)
        # Find the installation path with the version
        location = self.location_from_reg(version)
        exe_path = self.exe_path_from_location(os.path.join(location, "bin"), self.exe_name)
        if exe_path is None:
            self.tips.add(tips_code.cg_notexists, self.version_str)
            self.tips.save()
            raise CGExeNotExistError(error9899_cgexe_notexist.format(self.name))

        self.exe_path = exe_path

    def valid(self):
        software_config = self.job_info._task_info["software_config"]
        cg_version = software_config["cg_version"]
        # If you find a version of .5, consider it an integer version
        # outer int for compatibility with py2
        cg_version = str(int(math.floor(int(cg_version))))
        cg_name = software_config["cg_name"]
        self.log.debug("cg_name={0}, cg_version={1}".format(cg_name, cg_version))
        if cg_name.capitalize() != self.name.capitalize() and cg_version != self.version:
            self.tips.add(tips_code.cg_notmatch, self.version_str)
            self.tips.save()
            raise VersionNotMatchError(version_not_match)

    def dump_task_json(self):
        # super().dump_task_json()
        super(Maya, self).dump_task_json()

    def analyse(self):
        analyse_script_name = "Analyze"

        task_path = self.job_info._task_json_path
        asset_path = self.job_info._asset_json_path
        tips_path = self.job_info._tips_json_path

        options = {
            "cg_file": self.cg_file.replace("\\", "/"),
            "task_id": self.job_info._job_id,
            "task_json": task_path.replace("\\", "/"),
            "asset_json": asset_path.replace("\\", "/"),
            "tips_json": tips_path.replace("\\", "/"),
            "cg_project": os.path.dirname(os.path.normpath(__file__)).replace("\\", "/"),
            "cg_plugins": self.job_info._task_info["software_config"]["plugins"],
            "cg_version": self.version,
        }
        exe_path = self.exe_path

        script_path = os.path.dirname(os.path.normpath(__file__)).replace("\\", "/")

        cmd = '"{exe_path}" -command "python \\"options={options};import sys;sys.path.insert(0, \'{script_path}\');import {analyse_script_name};reload({analyse_script_name});{analyse_script_name}.analyze_maya(options)\\"'.format(
            exe_path=exe_path,
            options=options,
            script_path=script_path,
            analyse_script_name=analyse_script_name,
        )
        self.log.debug(cmd)
        returncode, stdout, stderr = self.cmd.run(cmd, shell=True)
        if returncode != 0:
            self.tips.add(tips_code.unknow_err)
            self.tips.save()
            raise AnalyseFailError

        # Determine whether the analysis is successful by determining whether a json file is generated.
        status, msg = self.json_exist()
        if status is False:
            self.tips.add(tips_code.unknow_err, msg)
            self.tips.save()
            raise AnalyseFailError(msg)

    def load_output_json(self):
        # super().load_output_json()
        super(Maya, self).load_output_json()

    def handle_analyse_result(self):
        upload_asset = []

        asset_json = self.asset_json
        assets = asset_json["asset"]
        for asset_dict in assets:
            path_list = asset_dict["path"]

            for path in path_list:
                d = {}
                local = path
                server = util.convert_path("", local)
                d["local"] = local.replace("\\", "/")
                d["server"] = server
                upload_asset.append(d)

        # Add the cg file to upload.json
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
        super(Maya, self).write_cg_path()

    def run(self):
        # run a custom script if exists
        # Analyze pre-custom scripts (configuration environment, specify the corresponding BAT/SH)
        self.pre_analyse_custom_script()
        #Get scene information
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

    def run1(self):
        """Temporary test"""
        # self.analyse_cg_file()
        self.location_from_reg(version="2016")
