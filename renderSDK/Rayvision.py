#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Main
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
        :param str domain_name: domain name, such as: task.renderbus.com
        :param str platform: platform number, such as: 2
        :param str access_id: Authorization id to identify the API caller
        :param str access_key: authorization key used to encrypt the signature string and the server-side verification signature string
        :param str workspace: working directory, used to store configuration files and logs generated in the analysis, etc.
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
        self._manage_job_obj = RayvisionManageJob(self._api_obj)
        self._transfer_obj = RayvisionTransfer(self._user_info, self._api_obj, self._manage_job_obj, log_obj=self.G_SDK_LOG)

    @decorator_use_in_class(SDK_LOG)
    def set_render_env(self, cg_name, cg_version, plugin_config={}, edit_name=None, label_name=None):
        """
        Set the job rendering environment, label (optional)
        :param str cg_name: Software name, such as 3ds Max, Maya, Houdini
        :param str cg_version: software version
        :param dict plugin_config: {"3dhippiesterocam":"2.0.13"}
        :param str edit_name: The unique identifier name of the rendering environment, temporarily unused
        :param str label_name:  label name, is project name, optional
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
        
        # initialize the variables
        self.is_analyse = False  # Whether to call the analysis method
        self.errors_number = 0  # number of errors in tips.json
        self.error_warn_info_list = []  # error, warning message
        # self.cg_name = str(cg_name)  # Software name (3ds Max, Maya, Houdini)
        
        cg_id = cg_id_name_dict.get(cg_name, None)  # Software id
        if cg_id is None:
            raise RayvisionError(1000000, r'Please input correct cg_name!')  # Please enter the correct cg_name
        
        # Generate job ID
        job_id = str(self._api_obj.create_task().get(r'taskIdList', [''])[0])
        if job_id == '':
            raise RayvisionError(1000000, r'Failed to create task number!')  # task ID creating failed
        self.G_SDK_LOG.info('JOB ID:{0}'.format(job_id))
        
        # Instantiate the RayvisionJob object
        self._job_info = RayvisionJob(self._user_info, job_id)
        self._job_info._task_info['task_info']['cg_id'] = cg_id
        
        # Set up label
        self.set_label(label_name)
            
        # Set the task rendering environment (that is, the software configuration of the task)
        software_config_dict = {}
        software_config_dict['cg_name'] = cg_name
        software_config_dict['cg_version'] = cg_version
        software_config_dict['plugins'] = plugin_config

        self._job_info._task_info['software_config'] = software_config_dict
        
        return job_id

    @decorator_use_in_class(SDK_LOG)
    def analyse(self, cg_file, project_dir=None, software_path=None):
        """
        Analyse cg file.
        :param str cg_file: scene file path
        :param str project_dir: The project path of the scene. If set, all assets are searched from the project path when rendering.
        :param str software_path: Local rendering software path, read from the registry by default, user-definable
        :return:
        """
        cg_file = str(cg_file)
        cg_id = self._job_info._task_info['task_info']['cg_id']
        if project_dir is not None:
            project_dir = str(project_dir)
        
        self.G_SDK_LOG.info('INPUT:')
        self.G_SDK_LOG.info('='*20)
        self.G_SDK_LOG.info('cg_file:{0}'.format(cg_file))
        self.G_SDK_LOG.info('project_dir:{0}'.format(project_dir))
        self.G_SDK_LOG.info('='*20)
        
        self.is_analyse = True
        # Pass self.job_info, directly modify job_info
        self._job_info._task_info['task_info']['input_cg_file'] = cg_file.replace('\\', '/')
        if project_dir is not None:
            self._job_info._task_info['task_info']['input_project_path'] = project_dir
            
        RayvisionAnalyse.execute(cg_id, cg_file, self._job_info, exe_path=software_path)
        
        scene_info_data = self._job_info._task_info['scene_info']
        
        # add frames to scene_info_render.<layer>.common.frames
        if cg_id == '2000':  # Maya
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
        Get the analyzed error and warning information
        :param str language: Return language 0: Chinese (default) 1: English
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

    @decorator_use_in_class(SDK_LOG)
    def submit_job(self, scene_info_render=None, task_info=None, upload_info=None, max_speed=None):
        """
        Submit job
        (1) Determine if there are any errors or warnings
        (2) Edit rendering parameters
        (3) Upload configuration files and assets
        (4) Submit the job ID
        :param dict scene_info_render: rendering parameters
        :param dict task_info: task parameters
        :param dict upload_info: upload files infomations
        :param int max_speed: Upload speed limit.The unit of 'max_speed' is KB/S, default value is 1048576 KB/S, means 1 GB/S
        """
        self._is_scene_have_error()  # check error
        
        self._edit_param(scene_info_render, task_info, upload_info)
        self._upload(max_speed)
        self._submit_job()

    @decorator_use_in_class(SDK_LOG)
    def download(self, job_id_list, local_dir, max_speed=None, print_log=True):
        """
        Download
        :param list<int> job_id_list:Job ID
        :param str local_dir: Download the stored directory
        :param int max_speed: Download speed limit.The unit of 'max_speed' is KB/S, default value is 1048576 KB/S, means 1 GB/S
        :param bool print_log: Whether to display the download command line. True: display; False: not display
        """
        self.G_SDK_LOG.info('INPUT:')
        self.G_SDK_LOG.info('='*20)
        self.G_SDK_LOG.info('job_id_list:{0}'.format(job_id_list))
        self.G_SDK_LOG.info('local_dir:{0}'.format(local_dir))
        self.G_SDK_LOG.info('='*20)

        self._transfer_obj._download(job_id_list, local_dir, max_speed, print_log)

        return True
        
    @decorator_use_in_class(SDK_LOG)
    def auto_download(self, job_id_list, local_dir, max_speed=None, print_log=False, sleep_time=10):
        """
        Auto download as long as any frame is complete.
        :param list<int> job_id_list:Job ID
        :param str local_dir: Download the stored directory
        :param int max_speed: Download speed limit.The unit of 'max_speed' is KB/S, default value is 1048576 KB/S, means 1 GB/S
        :param bool print_log: Whether to display the download command line. True: display; False: not display
        :param int/float sleep_time: Sleep time between download, unit is second
        """
        self.G_SDK_LOG.info('INPUT:')
        self.G_SDK_LOG.info('='*20)
        self.G_SDK_LOG.info('job_id_list:{0}'.format(job_id_list))
        self.G_SDK_LOG.info('local_dir:{0}'.format(local_dir))
        self.G_SDK_LOG.info('='*20)

        while True:
            if len(job_id_list) > 0:
                time.sleep(float(sleep_time))
                for job_id in job_id_list:
                    is_job_end = self._manage_job_obj.is_job_end(job_id)
                    self._transfer_obj._download([job_id], local_dir, max_speed, print_log)
                    
                    if is_job_end is True:
                        self.G_SDK_LOG.info('The job end: {0}'.format(job_id))
                        job_id_list.remove(job_id)
            else:
                break

        return True
        
    @decorator_use_in_class(SDK_LOG)
    def auto_download_after_job_completed(self, job_id_list, local_dir, max_speed=None, print_log=True, sleep_time=10):
        """
        Auto download after the job render completed.
        :param list<int> job_id_list:Job ID
        :param str local_dir: Download the stored directory
        :param int max_speed: Download speed limit.The unit of 'max_speed' is KB/S, default value is 1048576 KB/S, means 1 GB/S
        :param bool print_log: Whether to display the download command line. True: display; False: not display
        :param int/float sleep_time: Sleep time between download, unit is second
        """
        self.G_SDK_LOG.info('INPUT:')
        self.G_SDK_LOG.info('='*20)
        self.G_SDK_LOG.info('job_id_list:{0}'.format(job_id_list))
        self.G_SDK_LOG.info('local_dir:{0}'.format(local_dir))
        self.G_SDK_LOG.info('='*20)

        while True:
            if len(job_id_list) > 0:
                time.sleep(float(sleep_time))
                for job_id in job_id_list:
                    is_job_end = self._manage_job_obj.is_job_end(job_id)
                    
                    if is_job_end is True:
                        self.G_SDK_LOG.info('The job end: {0}'.format(job_id))
                        self._transfer_obj._download([job_id], local_dir, max_speed, print_log)
                        job_id_list.remove(job_id)
            else:
                break

        return True

    def _init_log(self, log_obj, log_path, is_print_log=True):
        log_dir = os.path.dirname(log_path)
        
        # If the log_dir path is a file, add timestamp after the log folder name.
        if os.path.exists(log_dir):
            if not os.path.isdir(log_dir):
                log_dir = '{0}{1}'.format(log_dir, format_time())

        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # If the log_path path is a folder, add timestamp after the log file name.
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
        Query user information and update to self._user_info
        1. Get user details (query_user_profile)
        2. Get user settings (query_user_setting)
        3. Get user transfer BID (get_transfer_bid)
        :return: True
        """
        self.G_SDK_LOG.info('[Rayvision.login.start.....]')
        
        data1 = self._api_obj.query_user_profile()
        data2 = self._api_obj.query_user_setting()
        data3 = self._api_obj.get_transfer_bid()
        data1.update(data2)
        data1.update(data3)
        
        # Update the above interface results to self._user_info and convert all the keys into underscores.
        for key, value in data1.items():
            if isinstance(value, (int, long, float)):
                value = str(value)
            key_underline = hump2underline(key)  # Variable name: hump to underline
            self._user_info[key_underline] = value
            
        self.G_SDK_LOG.info('USER INFO:{0}'.format(self._user_info))
        
        self.G_SDK_LOG.info('[Rayvision.login.end.....]')
        return True

    def set_label(self, label_name):
        """
        Customize the label to the job, find the task by label
        :param str label_name: label name
        """
        if label_name is not None:
            is_label_exist = False
            label_id = ''
            for _ in range(3):  # try by three time
                label_dict_list = self._api_obj.get_label_list().get('projectNameList', [])  # Get the list of existing users
                for label_dict in label_dict_list:
                    if label_dict['projectName'] == label_name:
                        is_label_exist = True
                        label_id = str(label_dict['projectId'])
                        break
                
                if is_label_exist:
                    if label_id == '':
                        continue
                    break
                else:  # Add a label if the no label exists
                    self._api_obj.add_label(label_name, '0')
                    is_label_exist = True
                
            self._job_info._task_info['task_info']['project_name'] = label_name
            self._job_info._task_info['task_info']['project_id'] = str(label_id)

    def _edit_param(self, scene_info_render=None, task_info=None, upload_info=None):
        """
        Modify rendering parameters, task parameters
        :param dict scene_info_render: rendering parameters
        :param dict task_info: task parameters
        :param dict upload_info: upload path informations
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
                'input_cg_file',  # The scene file path
                'frames_per_task',  # Quantity of frames that rendered on one machine
                'test_frames',  # The frames of test render
                'job_stop_time',  # Small task stopped due to timingout，unite is second。default is 8 hours
                'task_stop_time',  # Big task stopped due to timingout，unite is second。default is 24 hours
                'time_out',  # time-out period，turn into yellow color。unite is second。default is 12 hours
                'stop_after_test',  # Whether to pause the task after the priority rendering is completed, 1: Pause the task after the priority rendering is completed 2. Do not pause the task after the priority rendering is completed
                'tiles_type',  # "block(block-based),strip(strip-based)"
                'tiles',  # If the number of blocks is greater than 1,  or stripe is equal to 1 , then it is a single machine.
                'is_layer_rendering',  # If maya has turned on the layers。"0":Turn off "1":Turn on
                'is_distribute_render',  # Whether to turn on the distributed rendering。"0":Turn off"1":Turn on
                'distribute_render_node',  # The quantities of distributed rendering machine
                'input_project_path',  # Project path
                'render_layer_type',  # Render layer mode selection。"0"：renderlayer mode；"1"：rendersetup mode
                'os_name',  # rendering os type。"0": Linux;  "1": Windows
                'ram'  # rendering machine RAM。"64": 64G；"128": 128G
            ]  # Modifiable parameters list
            for key, value in task_info.items():
                if key in modifiable_param:
                    if isinstance(value, (int, long, float)):
                        value = str(value)
                    self._job_info._task_info['task_info'][key] = value
        
        # write upload.json
        if upload_info is not None:
            self._job_info._upload_info = upload_info
            with codecs.open(self._job_info._upload_json_path, 'w', 'utf-8') as f_upload_json:
                json.dump(upload_info, f_upload_json, indent=4, ensure_ascii=False)
        
        # write task.json
        with codecs.open(self._job_info._task_json_path, 'w', 'utf-8') as f_task_json:
            json.dump(self._job_info._task_info, f_task_json, indent=4, ensure_ascii=False)
            
        # write tips.json
        if not os.path.exists(self._job_info._tips_json_path):
            with codecs.open(self._job_info._tips_json_path, 'w', 'utf-8') as f_tips_json:
                json.dump(self._job_info._tips_info, f_tips_json, indent=4, ensure_ascii=False)
        
        return True

    def _upload(self, max_speed=None):
        cfg_list = []
        root = self._job_info._work_dir
        for file_name in os.listdir(self._job_info._work_dir):
            if file_name.endswith('.7z'):
               continue
            file_path = os.path.join(root, file_name)
            cfg_list.append(file_path)

        self._transfer_obj._upload(self._job_info._job_id, cfg_list, self._job_info._upload_info, max_speed)  # upload assets and config files
        return True

    def _submit_job(self):
        self._api_obj.submit_task(int(self._job_info._job_id))
        return True

    def _is_scene_have_error(self):
        if self.errors_number > 0:
            return_message = r'There are {0} errors. error_warn_info_list:{1}'.format(self.errors_number, self.error_warn_info_list)
            raise RayvisionError(1000000, return_message)  # Analysis completed with errors
