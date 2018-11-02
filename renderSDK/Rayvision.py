#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Main

Warning:
    job_id即task_id，莫纠结；
    label_name即project_name，莫纠结；
    edit_name即config_name，莫纠结；
"""

from .compat import *

import os
import sys
import logging
import codecs
import time

from .RayvisionUtil import get_os, hump2underline, cg_id_name_dict, decorator_use_in_class, format_time
from .RayvisionAPI import RayvisionAPI
from .RayvisionJob import RayvisionJob
from .RayvisionTransfer import RayvisionTransfer
from .RayvisionException import RayvisionError
from .RayvisionManageJob import RayvisionManageJob

from .analyse import RayvisionAnalyse

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
SDK_LOG = logging.getLogger('sdk_log')

class Rayvision(object):
    def __init__(self, domain_name, platform, access_id, access_key, workspace=None, *args, **kwargs):
        """
        :param str domain_name:  域名，如：task.renderbus.com
        :param str platform:  平台号，如：2
        :param str access_id:  授权id，用于标识API调用者身份
        :param str access_key:  授权密钥，用于加密签名字符串和服务器端验证签名字符串
        :param str workspace: 工作目录，用来存放分析中产生的配置文件和日志等
        :param kwargs:
        """
        domain_name = str(domain_name)
        platform = str(platform)
        access_id = str(access_id)
        access_key = str(access_key)
        if workspace is None:
            workspace = os.path.join(CURRENT_DIR, 'workspace')  # default workspace
        else:
            workspace = str(workspace)
        
        # init log
        self.G_SDK_LOG = SDK_LOG
        sdk_log_filename = 'run_{0}.log'.format(format_time('%Y%m%d'))
        sdk_log_path = os.path.join(workspace, 'log', 'sdk', sdk_log_filename)
        self._init_log(self.G_SDK_LOG, sdk_log_path)
        self.G_SDK_LOG.info('='*50)
        
        self._user_info = {
            'domain_name': domain_name,
            'platform': platform,
            'access_id': access_id,
            'access_key': access_key,
            'local_os': get_os(),
            'workspace': workspace
        }
        self._api_obj = RayvisionAPI(domain_name, platform, access_id, access_key, log_obj=self.G_SDK_LOG)
        self._login()  # update self._user_info
        self._transfer_obj = RayvisionTransfer(self._user_info, self._api_obj, log_obj=self.G_SDK_LOG)
        self._manage_job_obj = RayvisionManageJob(self._api_obj)
    
    def _init_log(self, log_obj, log_path, is_print_log=True):
        log_dir = os.path.dirname(log_path)
        
        # 如果log_dir路径为文件，则在日志文件夹名后加timestamp
        if os.path.exists(log_dir):
            if not os.path.isdir(log_dir):
                log_dir = '{0}{1}'.format(log_dir, format_time())

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 如果log_path路径为文件夹，则在日志文件名后加timestamp
        if os.path.isdir(log_path):
            log_dir = '{0}{1}'.format(log_path, format_time())
        
        log_obj.setLevel(logging.DEBUG)
        # FileHandler
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        fm=logging.Formatter("%(asctime)s  %(levelname)s - %(message)s","%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(fm)
        log_obj.addHandler(file_handler)
        
        # StreamHandler
        if is_print_log:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            log_obj.addHandler(stream_handler)
    
    def _login(self):
        """
        查询用户信息并更新到self._user_info中
            1.获取用户详情(query_user_profile)
            2.获取用户设置(query_user_setting)
            3.获取用户传输BID(get_transfer_bid)
        :return: True
        """
        self.G_SDK_LOG.info('[Rayvision.login.start.....]')
        
        data1 = self._api_obj.query_user_profile()
        data2 = self._api_obj.query_user_setting()
        data3 = self._api_obj.get_transfer_bid()
        data1.update(data2)
        data1.update(data3)
        
        # 将上述接口结果更新到self._user_info中，并将其中key全转换成下划线命名方式
        for key, value in data1.items():
            if isinstance(value, (int, long, float)):
                value = str(value)
            key_underline = hump2underline(key)  # 变量名：驼峰转下划线
            self._user_info[key_underline] = value
            
        self.G_SDK_LOG.info('USER INFO:{0}'.format(self._user_info))
        
        self.G_SDK_LOG.info('[Rayvision.login.end.....]')
        return True

    @decorator_use_in_class(SDK_LOG)
    def set_render_env(self, cg_name, cg_version, plugin_config={}, edit_name=None, label_name=None):
        """
        设置job渲染环境、标签（可选）
        :param str cg_name: 软件名，如3ds Max、Maya、Houdini
        :param str cg_version: 软件版本
        :param dict plugin_config: {"3dhippiesterocam":"2.0.13"}
        :param str edit_name: 渲染环境唯一标识名，暂时未用
        :param str label_name: 标签名，即项目名，可选
        """
        cg_name = str(cg_name)
        cg_version = str(cg_version)
        if edit_name is not None:
            edit_name = str(edit_name)
        if label_name is not None:
            label_name = str(label_name)
        
        self.G_SDK_LOG.info('INPUT:')
        self.G_SDK_LOG.info('='*20)
        self.G_SDK_LOG.info('cg_name:{0}'.format(cg_name))
        self.G_SDK_LOG.info('cg_version:{0}'.format(cg_version))
        self.G_SDK_LOG.info('plugin_config:{0}'.format(plugin_config))
        self.G_SDK_LOG.info('edit_name:{0}'.format(edit_name))
        self.G_SDK_LOG.info('label_name:{0}'.format(label_name))
        self.G_SDK_LOG.info('='*20)
        
        # 初始化作业所需的变量
        self.is_analyse = False  # 是否调用分析方法
        self.errors_number = 0  # tips.json中错误数量
        self.error_warn_info_list = []  # 错误、警告信息
        # self.cg_name = str(cg_name)  # 软件名（3ds Max、Maya、Houdini）
        
        cg_id = cg_id_name_dict.get(cg_name, None)  # 软件id
        if cg_id is None:
            raise RayvisionError(1000000, r'Please input correct cg_name!')  # 请输入正确的cg_name
        
        # 生成作业号
        job_id = str(self._api_obj.create_task().get(r'taskIdList', [''])[0])
        if job_id == '':
            raise RayvisionError(1000000, r'Failed to create task number!')  # 创建任务号失败
        self.G_SDK_LOG.info('JOB ID:{0}'.format(job_id))
        
        # 实例化RayvisionJob对象
        self._job_info = RayvisionJob(self._user_info, job_id)
        self._job_info._task_info['task_info']['cg_id'] = cg_id
        
        # 设置标签
        self.set_label(label_name)
            
        # 设置任务渲染环境（即任务的软件配置）
        software_config_dict = {}
        software_config_dict['cg_name'] = cg_name
        software_config_dict['cg_version'] = cg_version
        software_config_dict['plugins'] = plugin_config

        self._job_info._task_info['software_config'] = software_config_dict
        
        return True

    def set_label(self, label_name):
        """
        给job自定义标签，可通过标签查找所属任务
        :param str label_name: 标签名
        """
        if label_name is not None:
            is_label_exist = False
            label_id = ''
            for _ in range(3):  # 尝试3次
                label_dict_list = self._api_obj.get_label_list().get('projectNameList', [])  # 获取用户已有标签列表
                for label_dict in label_dict_list:
                    if label_dict['projectName'] == label_name:
                        is_label_exist = True
                        label_id = str(label_dict['projectId'])
                        break
                
                if is_label_exist:
                    if label_id == '':
                        continue
                    break
                else:  # 标签不存在则新增标签
                    self._api_obj.add_label(label_name, '0')
                    is_label_exist = True
                
            self._job_info._task_info['task_info']['project_name'] = label_name
            self._job_info._task_info['task_info']['project_id'] = str(label_id)

    @decorator_use_in_class(SDK_LOG)
    def analyse(self, cg_file, project_dir=None, software_path=None):
        """
        Analyse cg file.
        :param str cg_file: 场景文件路径
        :param str project_dir: 场景的项目路径，如设置则在渲染时所有资产从项目路径中搜索
        :param str software_path: 本地渲染软件路径，默认从注册表中读取，用户可自定义
        :return:
        """
        cg_file = str(cg_file)
        if project_dir is not None:
            project_dir = str(project_dir)
        
        self.G_SDK_LOG.info('INPUT:')
        self.G_SDK_LOG.info('='*20)
        self.G_SDK_LOG.info('cg_file:{0}'.format(cg_file))
        self.G_SDK_LOG.info('project_dir:{0}'.format(project_dir))
        self.G_SDK_LOG.info('='*20)
        
        self.is_analyse = True
        # 传self.job_info过去，直接修改job_info
        self._job_info._task_info['task_info']['input_cg_file'] = cg_file.replace('\\', '/')
        self._job_info._task_info['task_info']['scenefile'] = cg_file.replace('\\', '/')
        self._job_info._task_info['task_info']['cgfile'] = cg_file.replace('\\', '/')
        self._job_info._task_info['task_info']['original_cg_file'] = cg_file.replace('\\', '/')
        if project_dir is not None:
            self._job_info._task_info['task_info']['input_project_path'] = project_dir
            
        RayvisionAnalyse.execute(cg_file, self._job_info, exe_path=software_path)
        
        scene_info_data = self._job_info._task_info['scene_info']
        
        # add frames to scene_info_render.<layer>.common.frames
        if self._job_info._task_info['task_info']['cg_id'] == '2000':  # Maya
            for layer_name, layer_dict in scene_info_data.items():
                start_frame = layer_dict['common']['start']
                end_frame = layer_dict['common']['end']
                by_frame = layer_dict['common']['by_frame']
                frames = '{0}-{1}[{2}]'.format(start_frame, end_frame, by_frame)
                scene_info_data[layer_name]['common']['frames'] = frames
        
        self._job_info._task_info['scene_info_render'] = scene_info_data
        
        return_scene_info_render = self._job_info._task_info['scene_info_render']
        return_task_info = self._job_info._task_info['task_info']
        
        return  return_scene_info_render, return_task_info

    @decorator_use_in_class(SDK_LOG)
    def check_error_warn_info(self, language='0'):
        """
        获取分析出的错误、警告信息
        :param str language: 返回语言  0：中文（默认） 1：英文
        """
        if len(self._job_info._tips_info) > 0:
            for code, value in self._job_info._tips_info.items():
                code_info_list = self._api_obj.query_error_detail(code, language=language)
                for code_info in code_info_list:
                    code_info['details'] = value
                    if str(code_info['type']) == '1':  # 0:warning  1:error
                        self.errors_number += 1
                    self.error_warn_info_list.append(code_info)

        self.G_SDK_LOG.info('error_warn_info_list:{0}'.format(self.error_warn_info_list))
        return self.error_warn_info_list


    def _edit_param(self, scene_info_render=None, task_info=None):
        """
        修改渲染参数、任务参数
        :param dict scene_info_render: 渲染参数
        :param dict task_info: 任务参数
        :return: True
        """
        self.G_SDK_LOG.info('INPUT:')
        self.G_SDK_LOG.info('='*20)
        self.G_SDK_LOG.info('scene_info_render:{0}'.format(scene_info_render))
        self.G_SDK_LOG.info('task_info:{0}'.format(task_info))
        self.G_SDK_LOG.info('='*20)
        
        if scene_info_render is not None:
            self._job_info._task_info['scene_info_render'] = scene_info_render
            if not self.is_analyse:
                self._job_info._task_info['scene_info'] = scene_info_render
                
        if task_info is not None:
            modifiable_param = [
                'frames_per_task',  # 一机渲多帧的帧数量
                'test_frames',  # 优先渲染
                'job_stop_time',  # 小任务超时停止，单位秒。默认8小时
                'task_stop_time',  # 大任务超时停止，单位秒。默认24小时
                'time_out',  # 超时时间，变黄。单位秒。默认12小时
                'stop_after_test',  # 优先渲染完成后是否暂停任务,1:优先渲染完成后暂停任务 2.优先渲染完成后不暂停任务
                'tiles_type',  # "block(分块),strip(分条)"
                'tiles',  # 分块数量 大于1就分块或者分条 等于1 就是单机
                'is_layer_rendering',  # maya是否开启分层。"0":关闭 "1":开启
                'is_distribute_render',  # 是否开启分布式渲染。"0":关闭 "1":开启
                'distribute_render_node',  # 分布式渲染机器数
                'input_project_path',  # 工程目录路径
                'render_layer_type'  # 渲染层类型。"0"：renderlayer方式；"1"：rendersetup方式
            ]  # 可修改的参数列表
            for key, value in task_info.items():
                if key in modifiable_param:
                    if isinstance(value, (int, long, float)):
                        value = str(value)
                    self._job_info._task_info['task_info'][key] = value
        
        with codecs.open(self._job_info._task_json_path, 'w', 'utf-8') as f:
            json.dump(self._job_info._task_info, f, indent=4, ensure_ascii=False)
        
        return True


    def _upload(self):
        cfg_list = []
        root = self._job_info._work_dir
        for file_name in os.listdir(self._job_info._work_dir):
            if file_name.endswith('.7z'):
               continue
            file_path = os.path.join(root, file_name)
            cfg_list.append(file_path)

        self._transfer_obj._upload(self._job_info._job_id, cfg_list, self._job_info._upload_info)  # 上传配置文件和资产
        return True


    def _submit_job(self):
        self._api_obj.submit_task(int(self._job_info._job_id))
        return True
    
    
    @decorator_use_in_class(SDK_LOG)
    def submit_job(self, scene_info_render=None, task_info=None):
        """
        提交作业
        （1）判断是否有错误、警告
        （2）编辑渲染参数
        （3）上传配置文件和资产
        （4）提交作业号
        :param dict scene_info_render: 渲染参数
        :param dict task_info: 任务参数
        """
        self._is_scene_have_error()  # check error
        
        self._edit_param(scene_info_render, task_info)
        self._upload()
        self._submit_job()
    

    @decorator_use_in_class(SDK_LOG)
    def download(self, job_id_list, local_dir):
        """
        下载
        :param list<int> job_id_list: 作业号列表
        :param str local_dir: 下载存放目录
        """
        self.G_SDK_LOG.info('INPUT:')
        self.G_SDK_LOG.info('='*20)
        self.G_SDK_LOG.info('job_id_list:{0}'.format(job_id_list))
        self.G_SDK_LOG.info('local_dir:{0}'.format(local_dir))
        self.G_SDK_LOG.info('='*20)
        
        for job_id in job_id_list:
            self._transfer_obj._download(job_id, local_dir)
        return True

    def _is_scene_have_error(self):
        if self.errors_number > 0:
            return_message = r'There are {0} errors. error_warn_info_list:{1}'.format(self.errors_number, self.error_warn_info_list)
            raise RayvisionError(1000000, return_message)  # 分析完成有错误



    
    
    