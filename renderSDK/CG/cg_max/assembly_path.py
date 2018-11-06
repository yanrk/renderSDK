# -*-coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import os
import io
import re
import logging as log
import glob
from pprint import pprint

from renderSDK.CG.util import convert_path

"""
Collecting assets rules
"""


def ensure_str(string):
    if type(string) == bytes:
        try:
            string = string.decode("utf-8")
        except UnicodeDecodeError as e:
            string = string.decode("gbk")
    return string


def general_rule(path, file):
    """通用规则"""
    assert os.path.isabs(path) is True
    # 1) According to the given path, check the existance
    if os.path.exists(path):
        return path

    # 2) If 1) does not exist, then judge whether the max folder exists in this file.
    file_path = os.path.dirname(file)
    # The map name
    filename = os.path.basename(path)
    new_path = os.path.join(file_path, filename)
    if os.path.exists(new_path):
        return path

    # 3) If 1) 2) do not exist, according to the underlying file of the given path, find whether the corresponding file exists in the path of folder that contains max file 
    # Find the parent directory
    parent_path = os.path.abspath(os.path.dirname(path))
    # Name of the parent directory
    parent_name = os.path.split(parent_path)[-1]
    new_path = os.path.join(file_path, parent_name, filename)
    if os.path.exists(new_path):
        return new_path
    else:
        return None


def general_rule_by_re(path, file):
    """"""
    assert os.path.isabs(path) is True
    # 1) According to the given path, check the existance
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)
    pattern = "{0}/{1}*{2}".format(dirname, name, ext)
    result = glob.glob(pattern)
    if len(result) > 0:
        return result

    # 2) If 1) does not exist, then check whether the max folder exists in this file.
    file_path = os.path.dirname(file)
    pattern = "{0}/{1}*{2}".format(file_path, name, ext)
    result = glob.glob(pattern)
    if len(result) > 0:
        return result

    # 3) If 1) 2) do not exist, according to the underlying file of the given path, find whether the corresponding file exists in the path of folder that contains max file 
    # Find the parent directory of map
    parent_path = os.path.abspath(os.path.dirname(path))
    # The name of the directory of the map
    parent_name = os.path.split(parent_path)[-1]
    new_path = os.path.join(file_path, parent_name)
    pattern = "{0}/{1}*{2}".format(new_path, name, ext)
    result = glob.glob(pattern)
    if len(result) > 0:
        return result
    else:
        return None


def _ifl_rule(path, file):
    # 1) According to the given path, check the existance
    # If path is not an absolute path, it is considered to be non-existent
    if not os.path.isabs(path):
        pass
    elif os.path.exists(path):
        return path

    # 2) If 1) does not exist, then check whether the max folder exists in this file.
    file_path = os.path.dirname(file)
    # The map name
    filename = os.path.basename(path)
    new_path = os.path.join(file_path, filename)
    if os.path.exists(new_path):
        return new_path
    else:
        return None


def _handle_ifl(ifl_path, cg_file):
    os.path.abspath(os.path.dirname(ifl_path))
    with io.open(ifl_path, "r", encoding="utf-8") as fp:
        lines = fp.readlines()
    result = {
        "exist": [],
        "missing": [],
    }

    for line in lines:
        line = ensure_str(line)
        if not line:
            continue
        ext = os.path.splitext(line)[-1]
        l = ext.split(" ")
        if len(l) > 1:
            # Attached the numbers to the path `f:/kk/bb/ag11c_00000.jpg 3` Re-assignment
            line = line.replace(l[1], "").strip()
        path = line
        # Determine whether the path is with or without a drive, and apply to according rules
        r = _ifl_rule(line, ifl_path)
        if r is not None:
            result["exist"].append(r)
            continue

        r = _ifl_rule(path, cg_file)
        if r is not None:
            result["exist"].append(r)
        else:
            result["missing"].append(path)
    return result


def _point_cache_rule(path, file):
    assert os.path.isabs(path) is True
    # 1) According to the given path, check the existance
    dirname = os.path.dirname(path)
    basename = os.path.basename(path)
    name, ext = os.path.splitext(basename)
    if ext == ".xml":
        pattern = "{0}/{1}*{2}".format(dirname, name, ".mc")
    elif ext == ".mcx":
        pattern = "{0}/{1}*{2}".format(dirname, name, ".mcx")
    else:
        return None
    result = glob.glob(pattern)
    if len(result) > 0:
        return result

    # 2) If 1) does not exist, then check whether the max folder exists in this file.
    file_path = os.path.dirname(file)
    pattern = "{0}/{1}*{2}".format(file_path, name, ext)
    result = glob.glob(pattern)
    if len(result) > 0:
        return result

    # 3)  # 3) If 1) 2) do not exist, according to the underlying file of the given path, find whether the corresponding file exists in the path of folder that contains max file 
    # Find the parent directory of map
    parent_path = os.path.abspath(os.path.dirname(path))
    # The name of the directory of the map
    parent_name = os.path.split(parent_path)[-1]
    new_path = os.path.join(file_path, parent_name)
    pattern = "{0}/{1}*{2}".format(new_path, name, ext)
    result = glob.glob(pattern)
    if len(result) > 0:
        return result
    else:
        return None


def assemble_texture(path_list, cg_file, task_json):
    l = []
    for index, path in enumerate(path_list):
        d = {}
        
        ext = os.path.splitext(path)[-1]
        if ext.lower() == ".ifl":
            # Find the contents of the ifl file to get the map sequence,  additional processing needed.
            result = _handle_ifl(path, cg_file)
            exist = result["exist"]
            for p in exist:
                d["local"] = p.replace("\\", "/")
                d["server"] = convert_path("", p)
                l.append(d)
        else:
            result = general_rule(path, cg_file)
            if result is not None:
                server_path = convert_path("", result)
                d["local"] = result.replace("\\", "/")
                d["server"] = server_path
                l.append(d)
            else:
                # If the result is none, add missing, and handle it later
                pass

    return l


def assemble_vrmap(path_list, cg_file, task_json):
    task_json = task_json
    scene_info = task_json["scene_info"]
    
    renderer = scene_info["renderer"]
    #
    gi = renderer["gi"]
    primary_gi_engine = renderer["primary_gi_engine"]
    irradiance_map_mode = renderer["irradiance_map_mode"]

    l = []
    # a
    if gi == "1" and primary_gi_engine == "0" and irradiance_map_mode == "2":
        for index, path in enumerate(path_list):
            d = {}
            result = general_rule(path, cg_file)
            if result is not None:
                server_path = convert_path("", result)
                d["local"] = result.replace("\\", "/")
                d["server"] = server_path
                l.append(d)
            else:
                pass
    # b
    if gi == "1" and primary_gi_engine == "0" and irradiance_map_mode == "7":
        for index, path in enumerate(path_list):
            result = general_rule_by_re(path, cg_file)
            if result is not None:
                for p in result:
                    server_path = convert_path("", p)
                    d["local"] = result.replace("\\", "/")
                    d["server"] = server_path
                    l.append(d)
            else:
                pass
    return l


def assemble_vlmap(path_list, cg_file, task_json):
    task_json = task_json
    scene_info = task_json["scene_info"]
    
    renderer = scene_info["renderer"]
    #
    gi = renderer["gi"]
    primary_gi_engine = renderer["primary_gi_engine"]
    secondary_gi_engine = renderer["secondary_gi_engine"]
    light_cache_mode = renderer["light_cache_mode"]

    l = []
    if gi == "1" and (primary_gi_engine == "3" or secondary_gi_engine == "3") and light_cache_mode == "2":
        for index, path in enumerate(path_list):
            d = {}
            result = general_rule(path, cg_file)
            if result is not None:
                server_path = convert_path("", result)
                d["local"] = result.replace("\\", "/")
                d["server"] = server_path
            else:
                pass
    return l


def assemble_point_cache(path_list, cg_file, task_json):
    l = []
    for index, path in enumerate(path_list):
        d = {}
        result = _point_cache_rule(path, cg_file)
        if result is not None:
            server_path = convert_path("", result)
            d["local"] = result.replace("\\", "/")
            d["server"] = server_path
        else:
            pass
    return l


handle_funcs = {
    "texture": assemble_texture,
    "vrmap": assemble_vrmap,
    "vrlmap": assemble_vlmap,
    "point_cache": assemble_point_cache,
}


def test__handle_ifl():
    # 1. ifl content without path
    ifl_path = r"d:\no.ifl"
    cg_file = r"E:\test_find_path\find.max"
    result = _handle_ifl(ifl_path, cg_file)
    pprint(result)

    print("-" * 20)

    # 2.  ifl content with path
    ifl_path = r"d:\no1.ifl"
    cg_file = r"E:\test_find_path\find.max"
    result = _handle_ifl(ifl_path, cg_file)
    pprint(result)


def main():
    pass
    test__handle_ifl()


if __name__ == '__main__':
    pass
    main()
