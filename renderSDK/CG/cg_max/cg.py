# -*-coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os
import re
import sys
import time
import datetime
import traceback
import subprocess

try:
    import _winreg
except ImportError:
    import winreg as _winreg
from pprint import pprint

from renderSDK.compat import *
from renderSDK.CG.cg_base import CGBase
from renderSDK.CG import util
from renderSDK.CG import tips_code
from renderSDK.CG.exception import *
from renderSDK.CG.message import *
from .assembly_path import handle_funcs

VERSION = sys.version_info[0]


def cmp(a, b):
    r = (a > b) - (a < b)
    return r


# TODO
"""
To be improved: tips.add() tips.save()
Exception tips_code and other conditions

Determine if the path and file name are too long
"""


class Max(CGBase):
    def __init__(self, *args, **kwargs):
        super(Max, self).__init__(*args, **kwargs)
        self.exe_name = "3dsmax.exe"
        self.vray = None
        self.name = "3ds Max"
        self.ms_name_a = "analysea.mse"
        self.ms_name_u = "analyseu.mse"
        self.temp_task_json_name = "task_temp.json"
        self.file_version = None

        self.init()

    def init(self):
        """
        1. check filename
        """
        # check filename
        basename = os.path.basename(self.cg_file)
        short_name, extension = os.path.splitext(basename)
        pattern = r'^[A-Z][^-]*?\d$'
        m = re.match(pattern, short_name)
        if m is None:
            # self.tips.add(tips_code.max_name_illegal, self.cg_file)
            # self.tips.save()
            # raise CGFileNameIllegalError("")
            pass

    def location_from_reg(self, bit, file_version):
        """
        Read the directory where 3dsmax.exe is located from the registry
        :param bit: bit
        :param file_version: the version read from the cg file
        :return:
        """
        location = None
        language_code = ''

        software_str = 'SOFTWARE\Autodesk\\'
        if bit == '32':
            software_str = 'SOFTWARE\Wow6432Node\Autodesk\\'
        # get max locaction from regedit
        type_list = ['3dsMax', '3dsMaxDesign']
        if file_version < 15:
            language_code_list = ['409', '40C', '407', '411', '412', '804']  # English,French,German,Japanese,Korean,Chinese
            # HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\3dsMax\12.0\MAX-1:409
            for t in type_list:
                for code in language_code_list:
                    try:
                        version_str = software_str + t + '\\' + str(file_version) + '.0\MAX-1:' + code
                        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, version_str)
                        location, type = _winreg.QueryValueEx(key, "Installdir")
                        language_code = code
                        break
                    except Exception as e:
                        self.log.debug(traceback.format_exc())
                        pass
        else:
            for t in type_list:
                self.log.debug(t)
                try:
                    version_str = software_str + t + '\\' + str(file_version) + '.0'  # Software\Autodesk\3dsMax\15.0
                    key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, version_str)
                    location, type = _winreg.QueryValueEx(key, "Installdir")
                except Exception as e:
                    self.log.debug(traceback.format_exc())
                    pass
        return location, language_code

    def location_from_env(self, bit, cg_version_str):
        """
        Find the installation path from the environment variable
        # ADSK_3DSMAX_x64_2012    C:\Program Files\Autodesk\3ds Max 2012\
        # ADSK_3DSMAX_x64_2014    C:\Program Files\Autodesk\3ds Max 2014\
        """
        location = None
        env_key = 'ADSK_3DSMAX_x' + bit + '_' + cg_version_str.replace('3ds Max ', '')
        self.log.debug(env_key)
        try:
            location = os.environ[env_key]
        except Exception as e:
            self.log.debug(traceback.format_exc())
        return location

    def exe_path_with_hardcode(self):
        """
        Find the default installation location
        :return:
        """
        driver_max_list = ['c:', 'd:', 'e:', 'f:']
        for driver in driver_max_list:
            location = os.path.join(driver, r"Program Files\Autodesk", self.version_str, self.exe_name)
            if os.path.exists(location):
                exe_path = location
                return exe_path

    def exe_path_from_ftype(self):
        """
        Use the windows command line ftype to find
        :return:
        """
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags = subprocess.CREATE_NEW_CONSOLE | subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        cmd = 'ftype 3dsmax'

        returncode, stdout, stderr = self.cmd.run(cmd, shell=True)
        if returncode != 0:
            self.tips.add(tips_code.unknow_err, stdout, stderr)

        if stdout.startswith('3dsmax="') and self.version_str in stdout:
            location = stdout.replace('3dsmax="', '').replace('"%1"', '').replace('"', '').strip()
            if os.path.exists(location):
                exe_path = location
                return exe_path

    def find_location(self):
        """
        etc. cg_version = 16
        cg_version_str = 3ds Max 2016
        Software year (2016) differs from file version 2
        For example file version = 13.00
        The max version is 2011

        Assignment:
        self.version
        self.version_str
        self.exe_path
        self.vray
        """
        language_code = ""
        file_version = self.file_version
        cg_version_str = self.version_str

        location, language_code = self.location_from_reg("64", file_version)
        if location is None:
            location, language_code = self.location_from_reg("32", file_version)
        if location is None:
            location, language_code = self.location_from_env("64", cg_version_str)
        if location is None:
            location, language_code = self.location_from_env("32", cg_version_str)
        if location is None:
            raise RayvisionError("Can't find Max location.")

        exe_path = self.exe_path_from_location(location, self.exe_name)
        if exe_path in (None, ""):
            exe_path = self.exe_path_with_hardcode()
        if exe_path in (None, ""):
            exe_path = self.exe_path_from_ftype()

        if exe_path in (None, ""):
            self.tips.add(tips_code.cg_notexists, cg_version_str)
            self.tips.save()
            raise MaxExeNotExistError(error9899_maxexe_notexist)
        self.exe_path = exe_path
        if file_version < 15 and language_code in ['40C', '407', '411', '412', '804']:
            self.tips.add(tips_code.not_english_max, exe_path)

    def get_cg_file_info(self, cg_file):
        """
        File_version is parsed from GetMaxProperty.exe and cg_version is computed from file_version.
        :param cg_file:
        :return: (cg_version :str, file_version :int)

        Assignment:
        self.vray
        """
        # Use exe to parse the max file and get the version of the software used.
        exe_name = "GetMaxProperty.exe"
        path = os.path.abspath(os.path.join(os.path.abspath(__file__), "../../../tool/max"))
        cmd = '{0} "{1}"'.format(
            os.path.join(path, exe_name),
            cg_file,
        )
        returncode, stdout, stderr = self.cmd.run(cmd, log_output=False)

        if returncode != 0:
            self.tips.add(tips_code.cginfo_failed)
            self.tips.save()
            raise RayvisionError("Load max info fail")

        # TODO if useful to others (except vray) parse_lines need to be fixed
        lines = stdout.splitlines()
        lines = [line for line in lines if line]
        stdout1 = "\n".join(lines)
        # self.log.debug(stdout1)
        # info = self.parse_lines(lines)
        # pprint(info)

        
        vray_version = self._find_vray_version(stdout)

        # Compatible Chinese or other...
        patterns = [
            r"3ds Max Version: (\d+\.\d+)",
            r"3ds Max 版本: (\d+\.\d+)",
        ]

        file_version = None
        cg_version = None
        for pattern in patterns:
            result = re.search(pattern, stdout)
            if result is not None:
                file_version = result.groups()[0]
                file_version = int(float(file_version))
                #
                if file_version > 9:
                    cg_version = str(int(file_version) + 1998)
                self.log.debug("file_version={0}, type={1}".format(file_version, type(file_version)))
                self.log.debug("cg_version={0}, type={1}".format(cg_version, type(cg_version)))
                break
        if file_version is None or cg_version is None:
            raise MaxDamageError(error9900_max_damage)

        self.log.debug("cg_version={0}, file_version={1}".format(cg_version, file_version))

        d = dict(
            cg_version=cg_version,
            file_version=file_version,
            vray_version=vray_version,
        )
        return d

    def _find_vray_version(self, string):
        """find vray version by re"""
        p = "Renderer Name=(.*) \r"
        result = re.search(p, string)
        if result is not None:
            renderer_name = result.groups()[0].lower()
            if "missing" in renderer_name:
                self.log.info("missing renderer")
                self.tips.add(tips_code.realflow_missing)
                self.tips.save()
                raise RayvisionError("missing renderer")
            else:
                vray = renderer_name.replace('v-ray ', 'vray').replace('v_ray ', 'vray').replace('adv ', '').replace('edu ', '').replace('demo ', '').replace(' ', '')
        else:
            self.tips.add(tips_code.cginfo_failed)
            self.tips.save()
            raise RayvisionError("get max info failed")
        self.log.debug("vray={0}".format(vray))
        return vray

    def _find_max_version(self, string):
        pass

    def parse_lines(self, lines):
        """deprecated"""
        index = 0
        d = {}
        now = ""
        pprint(lines)
        while index < len(lines):
            line = lines[index]
            index += 1
            try:
                next_line = lines[index]
            except IndexError as e:
                next_line = ""
            if not line.startswith("\t"):
                key = line.strip()
                now = key
                if next_line.startswith("\t"):
                    if ":" in next_line or "=" in next_line:
                        d[key] = {}
                    else:
                        d[key] = []
                    continue
                else:
                    d[key] = None
            else:
                line = line.strip()
                if "=" in line:
                    char = "="
                elif ":" in line:
                    char = ":"
                else:
                    try:
                        d[now].append(line)
                    except AttributeError as e:
                        # traceback.print_exc()
                        d[now][line] = None  # Avoid "Uncompressed"
                    continue

                # if "&" in line:
                #     ss = line.split("&")
                #     for item in ss:
                #         k, v = item.split(char)
                #         k, v = k.strip(), v.strip()
                #         if "," in v:
                #             print(222, d)
                #             print(333, d[now])
                #             print(now, k, v)
                #             print(type(now), type(k), type(v))
                #             # d[now] sometimes is a list
                #             d[now][k] = v.split(",")
                #         else:
                #             d[now][k] = v

                k, v = line.split(char)
                k, v = k.strip(), v.strip()
                d[now][k] = v
        # pprint(d)
        return d

    def template_ms(self, ms_path, ms_name, cg_file, task_json, asset_json, tips_json, ignore_analyse_array="false"):
        t = '''
(DotNetClass "System.Windows.Forms.Application").CurrentCulture = dotnetObject "System.Globalization.CultureInfo" "zh-cn"
filein @"{ms_path}/{ms_name}"

analyse_main  cg_file:"{cg_file}" task_json:"{task_json}" asset_json:"{asset_json}" tips_json:"{tips_json}" ignore:#("{ignore_analyse_array}")
'''
        t = t.format(
            ms_path=ms_path,
            cg_file=cg_file,
            task_json=task_json,
            asset_json=asset_json,
            tips_json=tips_json,
            ignore_analyse_array=ignore_analyse_array,
            ms_name=ms_name,
        )
        return t

    def zip_max(self, max_list):
        """
        return format:
        {
            "local_max": "zip_path",
            "d:/test1/test2/test.max": "<project_path>/<task_id>/test.max.7z",
            "\\10.80.3.44\test1\test2\test.max": "<project_path>/<task_id>/test.max.7z"
        }
        :param max_list:
        :return:
        """
        temp_project_path = self.job_info._work_dir

        zip_dict = {}
        for max_file in max_list:
            basename = os.path.basename(max_file)
            zip_name = os.path.join(temp_project_path, basename + '.7z')
            returncode = self.zip7z.pack([max_file], zip_name)
            if returncode != 0:
                self.tips.add(tips_code.cg_zip_failed)
                self.tips.save()
                raise CGFileZipFailError("zip fail")
            zip_dict[max_file] = zip_name

        return zip_dict

    def assemble_upload_json(self, asset_json, zip_result_dict):
        """
        Assembling upload.json,
        1. Process max compressed files .7z
        2. Process other assets of asset.json
        upload.json format:
        {
            "asset":[
                {
                    "local":"local_path1",
                    "server":"server_path1"
                },
                {
                    "local":"local_path2",
                    "server":"server_path2"
                }
            ]
        }
        """
        upload_json = {"asset": []}

        # Process the compressed file of .max first, {xxx.max: xxx.max.7z, xxx.max: xxx.max.7z,}
        for local_path, zip_path in zip_result_dict.items():
            d = {}
            d["local"] = zip_path.replace("\\", "/")
            #
            d["server"] = util.convert_path("", local_path + ".7z")
            upload_json["asset"].append(d)

        # Process Other assets in asset.json
        for k, v in asset_json.items():
            if "missing" in k.lower():
                continue

            k = k.lower()
            func = handle_funcs.get(k, None)
            self.log.info("handle key: {0}".format(k))
            if func is not None:
                l = func(asset_json[k], self.cg_file, self.task_json)
                self.log.info("handle result: {0}".format(l))
                upload_json["asset"].append(l)

        return upload_json

    def plugin_conflict(self, max='', plugin1='', plugin2=''):
        vray_multiscatter = ['2010_2.00.01_1.0.18a', '2010_2.00.02_1.0.18a', '2010_2.10.01_1.0.18a', '2010_2.20.02_1.0.18a', '2010_2.40.03_1.0.18a',
                             '2010_2.00.01_1.1.05', '2010_2.00.02_1.1.05', '2010_2.10.01_1.1.05', '2010_2.20.02_1.1.05', '2010_2.40.03_1.1.05',
                             '2010_2.00.01_1.1.05a', '2010_2.10.01_1.1.05a', '2010_2.20.02_1.1.05a', '2010_2.40.03_1.1.05a', '2010_2.00.01_1.1.07a',
                             '2010_2.20.02_1.1.07a', '2010_2.40.03_1.1.07a', '2010_2.00.01_1.1.08b', '2010_2.20.02_1.1.08b', '2010_2.40.03_1.1.08b',
                             '2010_2.00.01_1.1.09', '2010_2.00.02_1.1.09', '2010_2.10.01_1.1.09', '2010_2.20.02_1.1.09', '2010_2.40.03_1.1.09',
                             '2010_2.00.01_1.1.09a', '2010_2.40.03_1.1.09a', '2010_2.00.01_1.1.09c', '2010_2.40.03_1.1.09c', '2010_2.00.01_1.1.09d',
                             '2010_2.40.03_1.1.09d', '2010_2.00.01_1.2.0.3', '2010_2.00.02_1.2.0.3', '2010_2.10.01_1.2.0.3', '2010_2.20.02_1.2.0.3',
                             '2010_2.40.03_1.2.0.3', '2010_2.00.01_1.3.1.3a', '2010_2.00.02_1.3.1.3a',
                             '2010_2.10.01_1.3.1.3a', '2010_2.20.02_1.3.1.3a', '2010_2.40.03_1.3.1.3a', '2011_2.00.01_1.0.18a', '2011_2.00.02_1.0.18a',
                             '2011_2.10.01_1.0.18a', '2011_2.20.02_1.0.18a', '2011_2.20.03_1.0.18a', '2011_2.40.03_1.0.18a', '2011_3.30.04_1.0.18a',
                             '2011_3.30.05_1.0.18a', '2011_2.00.02_1.1.05', '2011_2.10.01_1.1.05', '2011_2.20.02_1.1.05', '2011_2.20.03_1.1.05',
                             '2011_2.40.03_1.1.05', '2011_3.30.04_1.1.05', '2011_3.30.05_1.1.05', '2011_2.10.01_1.1.05a', '2011_2.20.02_1.1.05a',
                             '2011_2.20.03_1.1.05a', '2011_2.40.03_1.1.05a', '2011_3.30.04_1.1.05a', '2011_3.30.05_1.1.05a', '2011_2.20.02_1.1.07a',
                             '2011_2.20.03_1.1.07a', '2011_2.40.03_1.1.07a', '2011_3.30.04_1.1.07a', '2011_3.30.05_1.1.07a', '2011_2.20.02_1.1.08b',
                             '2011_2.20.03_1.1.08b', '2011_2.40.03_1.1.08b', '2011_3.30.04_1.1.08b', '2011_3.30.05_1.1.08b', '2011_3.30.04_1.1.09',
                             '2011_3.30.05_1.1.09', '2011_2.40.03_1.1.09a', '2011_3.30.04_1.1.09a', '2011_3.30.05_1.1.09a', '2011_2.40.03_1.1.09c',
                             '2011_3.30.04_1.1.09c', '2011_3.30.05_1.1.09c', '2011_2.40.03_1.1.09d', '2011_3.30.04_1.1.09d', '2011_3.30.05_1.1.09d',
                             '2011_3.30.04_1.2.0.3', '2011_3.30.05_1.2.0.3', '2011_2.00.01_1.3.1.3a', '2011_2.00.02_1.3.1.3a',
                             '2011_2.10.01_1.3.1.3a', '2011_2.20.02_1.3.1.3a', '2011_2.20.03_1.3.1.3a', '2011_2.40.03_1.3.1.3a', '2011_3.30.04_1.3.1.3a',
                             '2011_3.30.05_1.3.1.3a', '2012_2.20.02_1.1.07a', '2012_2.20.03_1.1.07a', '2012_2.30.01_1.1.07a', '2012_2.40.03_1.1.07a',
                             '2012_3.30.04_1.1.07a', '2012_3.30.05_1.1.07a', '2012_3.40.01_1.1.07a', '2012_2.20.02_1.1.08b', '2012_2.20.03_1.1.08b',
                             '2012_2.30.01_1.1.08b', '2012_2.40.03_1.1.08b', '2012_3.30.04_1.1.08b', '2012_3.30.05_1.1.08b', '2012_3.40.01_1.1.08b',
                             '2012_2.30.01_1.1.09', '2012_2.40.03_1.1.09', '2012_3.30.04_1.1.09', '2012_3.30.05_1.1.09', '2012_3.40.01_1.1.09',
                             '2012_2.30.01_1.1.09a', '2012_2.40.03_1.1.09a', '2012_3.30.04_1.1.09a', '2012_3.30.05_1.1.09a', '2012_3.40.01_1.1.09a',
                             '2012_2.40.03_1.1.09c', '2012_3.30.04_1.1.09c', '2012_3.30.05_1.1.09c', '2012_3.40.01_1.1.09c',
                             '2012_3.30.04_1.1.09d', '2012_3.30.05_1.1.09d', '2012_3.40.01_1.1.09d', '2012_3.30.04_1.2.0.3', '2012_3.30.05_1.2.0.3',
                             '2012_3.40.01_1.2.0.3', '2012_2.00.03_1.3.1.3a', '2012_2.10.01_1.3.1.3a',
                             '2012_2.20.02_1.3.1.3a', '2012_2.20.03_1.3.1.3a', '2012_2.30.01_1.3.1.3a', '2012_2.40.03_1.3.1.3a', '2012_3.30.04_1.3.1.3a',
                             '2012_3.30.05_1.3.1.3a', '2012_3.40.01_1.3.1.3a', '2013_2.40.03_1.1.09c', '2013_2.40.04_1.1.09c', '2013_3.30.04_1.1.09c',
                             '2013_3.30.05_1.1.09c', '2013_3.40.01_1.1.09c', '2013_2.40.03_1.1.09d', '2013_2.40.04_1.1.09d', '2013_3.30.04_1.1.09d',
                             '2013_3.30.05_1.1.09d', '2013_3.40.01_1.1.09d',
                             '2013_3.30.04_1.2.0.3', '2013_3.30.05_1.2.0.3', '2013_3.40.01_1.2.0.3',
                             '2013_2.30.01_1.3.1.3a', '2013_2.40.03_1.3.1.3a', '2013_2.40.04_1.3.1.3a', '2013_3.30.04_1.3.1.3a', '2013_3.30.05_1.3.1.3a',
                             '2013_3.40.01_1.3.1.3a', '2014_2.40.03_1.1.09c', '2014_2.40.04_1.1.09c', '2014_3.30.04_1.1.09c', '2014_3.30.05_1.1.09c',
                             '2014_3.40.01_1.1.09c', '2014_2.40.03_1.1.09d', '2014_2.40.04_1.1.09d', '2014_3.30.04_1.1.09d', '2014_3.30.05_1.1.09d',
                             '2014_3.40.01_1.1.09d', '2014_3.30.04_1.2.0.3',
                             '2014_3.30.05_1.2.0.3', '2014_3.40.01_1.2.0.3', '2014_2.30.01_1.3.1.3a', '2014_2.40.03_1.3.1.3a', '2014_2.40.04_1.3.1.3a',
                             '2012_3.40.02_1.1.09c', '2012_3.40.02_1.1.09d', '2012_3.40.02_1.2.0.3',
                             '2012_3.50.03_1.1.09c', '2012_3.50.03_1.1.09d', '2012_3.50.03_1.2.0.3',
                             '2012_2.30.01_1.1.09d']
        str_a = "{0}_{1}_{2}".format(max, plugin1, plugin2)
        if str_a in vray_multiscatter:
            return True
        else:
            return False

    # def kill(self, parent_id):
    #     """Temporarily not used"""
    #     log.debug("kill max")
    #     cmd_str = 'wmic process where name="3dsmax.exe" get Caption,Parent_process_id,Process_id'
    #     p = subprocess.Popen(cmd_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    #     while True:
    #         buff = p.stdout.readline().strip()
    #         if buff == '' and p.poll() is not None:
    #             break
    #         if buff is not None and buff != '':
    #             try:
    #                 buff_arr = buff.split()
    #                 # log.debug(buff)
    #                 if int(buff_arr[1]) == parent_id:
    #                     # log.debug('kill...'+buff)
    #                     os.system("taskkill /f /pid %s" % (buff_arr[2]))
    #             except Exception as e:
    #                 traceback.print_exc()
    def get_ms(self, version):
        pass

    def pre_analyse_custom_script(self):
        super(Max, self).pre_analyse_custom_script()

    def analyse_cg_file(self):
        d = self.get_cg_file_info(self.cg_file)
        cg_version_str = "{0} {1}".format(self.name, d["cg_version"])
        self.version = d["cg_version"]
        self.version_str = cg_version_str
        self.file_version = d["file_version"]
        self.vray = d["vray_version"]

        if self.custom_exe_path is not None:
            self.exe_path = self.custom_exe_path
        else:
            self.find_location()

    def valid(self):
        super(Max, self).valid()
        software_config = self.job_info._task_info["software_config"]
        cg_version = software_config["cg_version"]

        year = cg_version
        plugins = software_config["plugins"]
        if "multiscatter" in plugins:
            multiscatter = plugins["multiscatter"]
            vray_version = self.vray.replace("vray", "")
            if self.plugin_conflict(year, vray_version, multiscatter) is True:
                self.tips.add(tips_code.conflict_multiscatter_vray, vray_version, "Multiscatter" + multiscatter)
                self.tips.save()
                raise MultiscatterandvrayConfilictError(error_multiscatterandvray_confilict.format(vray_version, multiscatter))

    def dump_task_json(self):
        super(Max, self).dump_task_json()

    def analyse(self):
        # TODO sdk_path TODO config? --> ms_path ms_name gen_ms_path
        ms_path = os.path.abspath(os.path.dirname(__file__))
        cg_file = self.cg_file
        task_json = self.job_info._task_json_path
        # Temporarily temp task.json
        temp_task_json = os.path.join(os.path.dirname(task_json), self.temp_task_json_name)
        asset_json = self.job_info._asset_json_path
        tips_json = self.job_info._tips_json_path
        # ####
        version = int(self.version)
        if version < 2013:
            ms_name = self.ms_name_a
        else:
            ms_name = self.ms_name_u
        ms = self.template_ms(ms_path, ms_name, cg_file, temp_task_json, asset_json, tips_json, ignore_analyse_array="false").replace("\\", "/")
        self.log.info(ms)

        now = datetime.datetime.now()
        now = now.strftime("%Y%m%d%H%M%S")

        ms_full_path = os.path.join(self.job_info._work_dir, "Analyse{0}.ms".format(now))
        util.write(ms_full_path, ms)
        #
        cmd = "\"{0}\" -silent -mip -mxs \"filein \\\"{1}\\\"\"".format(
            self.exe_path,
            ms_full_path.replace("\\", "/"),
        )

        returncode, stdout, stderr = self.cmd.run(cmd, shell=True)
        self.log.info("returncode: {0}".format(returncode))
        # Run successfully The return code is not necessarily 0
        # Determine whether the analysis is successful by judging whether a json file is generated.
        status, msg = self.json_exist()
        if status is False:
            self.tips.add(tips_code.unknow_err, msg)
            self.tips.save()
            raise AnalyseFailError(msg)

    def json_exist(self):
        """If the json file is not generated, the analysis fails."""
        task_path = self.job_info._task_json_path
        temp_task_path = os.path.join(os.path.dirname(task_path), self.temp_task_json_name)
        asset_path = self.job_info._asset_json_path
        tips_path = self.job_info._tips_json_path

        for p in [temp_task_path, asset_path, tips_path]:
            if not os.path.exists(p):
                msg = "Json file is not generated: {0}".format(p)
                return False, msg
        return True, None

    def load_output_json(self):
        task_path = self.job_info._task_json_path
        temp_task_path = os.path.join(os.path.dirname(task_path), self.temp_task_json_name)
        asset_path = self.job_info._asset_json_path
        tips_path = self.job_info._tips_json_path

        encodings = ["utf-8-sig", "gbk", "utf-8"]
        temp_task_json = self.json_load(temp_task_path, encodings=encodings)
        asset_json = self.json_load(asset_path, encodings=encodings)
        tips_json = self.json_load(tips_path, encodings=encodings)

        # Add the contents of temp_task.json to task.json and write it as a file
        task_json = self.job_info._task_info
        # Directory update the replacement
        task_json.update(temp_task_json)
        util.json_save(task_path, task_json, ensure_ascii=False)

        # json contains BOM, need to be converted to non-contain BOM
        util.json_save(asset_path, asset_json, ensure_ascii=False)
        util.json_save(tips_path, tips_json, ensure_ascii=False)

        self.task_json = task_json
        self.job_info._task_info = task_json

        self.asset_json = asset_json
        self.job_info._asset_info = asset_json

        self.tips_json = tips_json
        self.job_info._tips_info = tips_json

    def write_vray(self):
        if "vray" in self.vray:
            task_path = self.job_info._task_json_path
            task_json = self.job_info._task_info
            task_json["software_config"]["plugins"]["vray"] = self.vray.replace("vray", "")
            util.json_save(task_path, task_json, ensure_ascii=False)
            self.task_json = task_json
            self.job_info._task_info = task_json

    def handle_analyse_result(self):
        # Remove zip list compression
        asset_json = self.asset_json
        key = "zip"
        if key in asset_json:
            maxs = asset_json[key]
            assert type(maxs) == list
            # Compress .max file, get the compressed path list
            zip_result_dict = self.zip_max(maxs)
        else:
            zip_result_dict = {}
        asset_json.pop(key)

        # Assemble the full path including max.zip and the path that should be uploaded in asset.json to upload.json
        upload_json = self.assemble_upload_json(asset_json, zip_result_dict)
        self.upload_json = upload_json
        self.job_info._upload_info = upload_json
        util.json_save(self.job_info._upload_json_path, upload_json, ensure_ascii=False)

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
        # Write the vray version to task.json
        self.write_vray()
        # Write task configuration file (custom information, independent upload list), compress specific files (compress files, upload path, delete path)
        self.handle_analyse_result()

        # Used for developing
        if VERSION == 3:
            self.log.debug(self)
        else:
            self.log.debug(self.exe_name)
            self.log.debug(self.exe_path)
            self.log.debug(self.vray)
            self.log.debug(self.name)
            self.log.debug(self.version)
            self.log.debug(self.cg_file)
            self.log.debug(self.cg_id)

        self.log.info("analyse end.")
