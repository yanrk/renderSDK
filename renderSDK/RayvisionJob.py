#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Store job information module.
"""
from .compat import *
import os
# import json
import codecs

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

class RayvisionJob(object):
    def __init__(self, user_info, job_id):
        self._job_id = job_id
        self._local_os = user_info['local_os']  # "windows"/"linux"
        
        # work directory
        self._work_dir = os.path.join(user_info['workspace'], 'work', self._job_id)
        if not os.path.exists(self._work_dir):
            os.makedirs(self._work_dir)
        
        # log directory
        self._log_dir = os.path.join(user_info['workspace'], 'log', 'analyse')
        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)

        if self._local_os == 'windows':
            self._zip_path = os.path.join(CURRENT_DIR, 'tool', 'zip', self._local_os, '7z.exe')
        else:
            self._zip_path = os.path.join(CURRENT_DIR, 'tool', 'zip', self._local_os, '7z')

        self._task_json_path = os.path.join(self._work_dir, 'task.json')
        self._asset_json_path = os.path.join(self._work_dir, 'asset.json')
        self._tips_json_path = os.path.join(self._work_dir, 'tips.json')
        self._upload_json_path = os.path.join(self._work_dir, 'upload.json')

        self._task_info = {
            'task_info': {
                'input_cg_file': '',  # The scene file path
                'is_picture': '0',  # Choose if it is the rendered effect picture or not。0: False, 1: True
                'task_id': self._job_id,  # job id
                'frames_per_task': '1',  # Quantity of frames that rendered on one machine
                'pre_frames': '000',  # The frames of test render
                'job_stop_time': '28800',  # Small task stopped due to timingout，unite is second。default is 8 hours
                'task_stop_time': '86400',  # Big task stopped due to timingout，unite is second。default is 24 hours
                'time_out': '12',  # time-out period，turn into yellow color。unite is second。default is 12 hours
                'stop_after_test': '2',  # Whether to pause the task after the priority rendering is completed, 1: Pause the task after the priority rendering is completed 2. Do not pause the task after the priority rendering is completed
                'project_name': '',  # Project name
                'project_id': '',  # Project id
                'channel': '4',  # Submit method
                'cg_id': '',  # Render software id
                'platform': user_info['platform'],  # Submit platform
                'tiles_type': 'block',  #  "block(block-based),strip(strip-based)"
                'tiles': '1',  # If the number of blocks is greater than 1,  or stripe is equal to 1 , then it is a single machine.
                'is_layer_rendering': '1',  # If maya has turned on the layers。"0":Turn off "1":Turn on
                'is_distribute_render': '0',  # Whether to turn on the distributed rendering。"0":Turn off"1":Turn on
                'distribute_render_node': '3',  # The quantities of distributed rendering machine
                'input_project_path':'',  # Project path，transfer the empty string if not setting up
                'render_layer_type':'0',  # Render layer mode selection。"0"：renderlayer mode；"1"：rendersetup mode
                'user_id': user_info['user_id'],  # User ID
                'os_name': '1',  # rendering os type。"0": Linux;  "1": Windows
                'ram': '64'  # rendering machine RAM。"64": 64G；"128": 128G
            },
            'software_config': {},
            'scene_info': {},
            'scene_info_render': {}
        }  # task.json
        self._asset_info = {}  # asset.json
        self._tips_info = {}  # tips.json
        self._upload_info = {}  # upload.json
