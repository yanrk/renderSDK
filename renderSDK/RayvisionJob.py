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
        
        # work目录
        self._work_dir = os.path.join(user_info['workspace'], 'work', self._job_id)
        if not os.path.exists(self._work_dir):
            os.makedirs(self._work_dir)
        
        # log目录
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
                'input_cg_file': '',  # 提交场景文件路径
                'is_picture': '0',  # 是否渲染效果图。0: False, 1: True
                'task_id': self._job_id,  # 作业id
                'frames_per_task': '1',  # 一机渲多帧的帧数量
                'test_frames': '000',  # 优先渲染
                'job_stop_time': '28800',  # 小任务超时停止，单位秒。默认8小时
                'task_stop_time': '86400',  # 大任务超时停止，单位秒。默认24小时
                'time_out': '12',  # 超时时间，变黄。单位小时。默认12小时
                'stop_after_test': '2',  # 优先渲染完成后是否暂停任务,1:优先渲染完成后暂停任务 2.优先渲染完成后不暂停任务
                'project_name': '',  # 项目名称
                'project_id': '',  # 项目id
                'channel': '4',  # 提交方式
                'cg_id': '',  # 渲染软件id
                'platform': user_info['platform'],  # 提交平台
                'tiles_type': 'block',  #  "block(分块),strip(分条)"
                'tiles': '1',  # 分块数量 大于1就分块或者分条 等于1 就是单机
                'is_layer_rendering': '1',  # maya是否开启分层。"0":关闭 "1":开启
                'is_distribute_render': '0',  # 是否开启分布式渲染。"0":关闭 "1":开启
                'distribute_render_node': '3',  # 分布式渲染机器数
                'input_project_path':'',  # 项目路径，如未设置传空字符串
                'render_layer_type':'0',  # 渲染层方式选择。"0"：renderlayer方式；"1"：rendersetup方式
                'user_id': user_info['user_id']  # 用户ID
            },
            'software_config': {},
            'scene_info': {},
            'scene_info_render': {}
        }  # task.json
        self._asset_info = {}  # asset.json
        self._tips_info = {}  # tips.json
        self._upload_info = {}  # upload.json
