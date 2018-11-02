#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
Transfer Module.
"""

from .compat import *

import os
import sys
import codecs
import subprocess
from . import RayvisionUtil

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


class RayvisionTransfer(object):
    def __init__(self, user_info, api_obj, log_obj=None):
        self._user_info = user_info
        self._api_obj = api_obj
        self.G_SDK_LOG = log_obj
        
        self._domain_name = user_info.get('domain_name')
        self._platform = user_info.get('platform')
        self._local_os = user_info.get('local_os')
        self._user_id = user_info.get('user_id')
        # self._input_bid = user_info.get('input_bid')
        # self._output_bid = user_info.get('output_bid')
        # self._config_bid = user_info.get('config_bid')

        if self._local_os == 'windows':
            self._rayvision_exe = os.path.join(CURRENT_DIR, 'tool', 'transmission', self._local_os, 'rayvision_transmitter.exe')
        else:
            self._rayvision_exe = os.path.join(CURRENT_DIR, 'tool', 'transmission', self._local_os, 'rayvision_transmitter')

        self._transports_json = os.path.join(CURRENT_DIR, 'tool', 'transmission', 'transports.json')
        transport_info = self._parse_transports_json()
        self._engine_type = transport_info['engine_type']
        self._server_name = transport_info['server_name']
        self._server_ip = transport_info['server_ip']
        self._server_port = transport_info['server_port']

    def _parse_transports_json(self):
        """
        解析transports.json，获取传输服务器信息
        """
        if 'foxrenderfarm' in self._domain_name:
            key_first_half = 'foxrenderfarm'
        else:
            key_first_half = 'renderbus'

        if self._platform == '2':
            key_second_half = 'www2'
        elif self._platform == '3':
            key_second_half = 'www3'
        elif self._platform == '4':
            key_second_half = 'www3'
        elif self._platform == '9':
            key_second_half = 'www9'
        elif self._platform == '20':  # pic
            key_second_half = 'pic'
        elif self._platform == '21':  # gpu
            key_second_half = 'gpu'
        else:
            key_second_half = 'default'

        if key_second_half == 'default':
            key = key_second_half
        else:
            key = '%s_%s' % (key_first_half, key_second_half)
            
        if 'test' in self._domain_name:
            key = '%s_%s' % (key, 'test')

        with codecs.open(self._transports_json, 'r', 'utf-8') as f:
            transports_info = json.load(f)
        return transports_info[key]
    
    def _upload(self, job_id, cfg_list, upload_info):
        """
        上传配置文件和资产
        """
        self._upload_cfg(job_id, cfg_list)
        self._upload_asset(upload_info)
    
    def _upload_cfg(self, job_id, cfg_path_list, **kwargs):
        """
        上传任务配置文件
        """
        transmit_type = "upload_files"  # upload_files/upload_file_pairs/download_files

        for cfg_path in cfg_path_list:
            local_path = RayvisionUtil.str2unicode(cfg_path)

            cfg_basename = os.path.basename(cfg_path)
            server_path = '/{0}/cfg/{1}'.format(job_id, cfg_basename)
            server_path = RayvisionUtil.str2unicode(server_path)
            
            if not os.path.exists(local_path):
                print('{0} is not exists.'.format(local_path))
                continue

            transmit_cmd = u'echo y|"{exe_path}" "{engine_type}" "{server_name}" "{server_ip}" "{server_port}" \
            "{storage_id}" "{user_id}" "{transmit_type}" "{local_path}" "{server_path}" "{max_connect_failure_count}" \
            "{keep_path}"'.format(
                exe_path=self._rayvision_exe,
                engine_type=self._engine_type,
                server_name=self._server_name,
                server_ip=self._server_ip,
                server_port=self._server_port,
                storage_id=self._user_info['config_bid'],
                user_id=self._user_id,
                transmit_type=transmit_type,
                local_path=local_path.replace('\\', '/'),
                server_path=server_path.replace('\\', '/'),
                max_connect_failure_count='1',  # default is 1
                keep_path='false'
            )
            # print transmit_cmd
            sys.stdout.flush()
            # os.system(transmit_cmd.encode(sys.getfilesystemencoding()))
            RayvisionUtil.run_cmd(transmit_cmd, log_obj=self.G_SDK_LOG)
    
    def _upload_asset(self, upload_info, **kwargs):
        """
        上传资产
        """
        transmit_type = "upload_files"  # upload_files/upload_file_pairs/download_files

        for file_local_server in upload_info['asset']:
            local_path = file_local_server['local']
            local_path = RayvisionUtil.str2unicode(local_path)
            server_path = file_local_server['server']
            server_path = RayvisionUtil.str2unicode(server_path)
            if not os.path.exists(local_path):
                print('{0} is not exists.'.format(local_path))
                continue

            transmit_cmd = u'echo y|"{exe_path}" "{engine_type}" "{server_name}" "{server_ip}" "{server_port}" \
            "{storage_id}" "{user_id}" "{transmit_type}" "{local_path}" "{server_path}" "{max_connect_failure_count}" \
            "{keep_path}"'.format(
                exe_path=self._rayvision_exe,
                engine_type=self._engine_type,
                server_name=self._server_name,
                server_ip=self._server_ip,
                server_port=self._server_port,
                storage_id=self._user_info['input_bid'],
                user_id=self._user_id,
                transmit_type=transmit_type,
                local_path=local_path.replace('\\', '/'),
                server_path=server_path.replace('\\', '/'),
                max_connect_failure_count='1',  # default is 1
                keep_path='false'
            )
            # print transmit_cmd
            sys.stdout.flush()
            # os.system(transmit_cmd.encode(sys.getfilesystemencoding()))
            RayvisionUtil.run_cmd(transmit_cmd, log_obj=self.G_SDK_LOG)

    def _download(self, task_id, local_dir, **kwargs):
        """
        TODO：多个任务的下载
        """
        transmit_type = 'download_files'
        
        local_dir = RayvisionUtil.str2unicode(local_dir)
        
        task_id_list = []
        task_id_list.append(int(task_id))
        
        data = self._api_obj.query_task_info(task_id_list)
        if data:
            items = data.get('items', [])
            for task_result_dict in items:
                server_folder = task_result_dict['outputFileName']
                transmit_cmd = u'echo y|"{exe_path}" "{engine_type}" "{server_name}" "{server_ip}" "{server_port}" \
                               "{download_id}" "{user_id}" "{transmit_type}" "{local_path}" "{server_path}"'.format(
                    exe_path=self._rayvision_exe,
                    engine_type=self._engine_type,
                    server_name=self._server_name,
                    server_ip=self._server_ip,
                    server_port=self._server_port,
                    download_id=self._user_info['output_bid'],
                    user_id=self._user_id,
                    transmit_type=transmit_type,
                    local_path=local_dir,
                    server_path=server_folder,
                )
                # print transmit_cmd
                sys.stdout.flush()
                # os.system(transmit_cmd.encode(sys.getfilesystemencoding()))
                RayvisionUtil.run_cmd(transmit_cmd, log_obj=self.G_SDK_LOG)
