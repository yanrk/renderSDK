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
    def __init__(self, user_info, api_obj, manage_job_obj, log_obj=None):
        self._user_info = user_info
        self._api_obj = api_obj
        self._manage_job_obj = manage_job_obj
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
        Analyze transports.json，obtain transfer server info
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
            key_second_half = 'www4'
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
    
    def _upload(self, job_id, cfg_list, upload_info, max_speed=None):
        """
        Upload configuration profiles and assets
        """
        self._upload_cfg(job_id, cfg_list, max_speed)
        self._upload_asset(upload_info, max_speed)
    
    def _upload_cfg(self, job_id, cfg_path_list, max_speed=None, **kwargs):
        """
        Upload configuration profiles and assets
        """
        transmit_type = "upload_files"  # upload_files/upload_file_pairs/download_files
        max_speed = str(max_speed) if max_speed is not None else "1048576"  # the unit of 'max_speed' is KB/S, default value is 1048576 KB/S, means 1 GB/S

        for cfg_path in cfg_path_list:
            local_path = RayvisionUtil.str2unicode(cfg_path)

            cfg_basename = os.path.basename(cfg_path)
            server_path = '/{0}/cfg/{1}'.format(job_id, cfg_basename)
            server_path = RayvisionUtil.str2unicode(server_path)
            
            if not os.path.exists(local_path):
                print('{0} is not exists.'.format(local_path))
                continue

            transmit_cmd = u'echo y|"{exe_path}" "{engine_type}" "{server_name}" "{server_ip}" "{server_port}" ' \
                            '"{storage_id}" "{user_id}" "{transmit_type}" "{local_path}" "{server_path}" ' \
                            '"{max_connect_failure_count}" "{keep_path}" "{max_speed}"'.format(
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
                keep_path='false',
                max_speed=max_speed
            )
            # print transmit_cmd
            sys.stdout.flush()
            # os.system(transmit_cmd.encode(sys.getfilesystemencoding()))
            RayvisionUtil.run_cmd(transmit_cmd, log_obj=self.G_SDK_LOG)
    
    def _upload_asset(self, upload_info, max_speed=None, **kwargs):
        """
        Upload assets
        """
        transmit_type = "upload_files"  # upload_files/upload_file_pairs/download_files
        max_speed = str(max_speed) if max_speed is not None else "1048576"  # the unit of 'max_speed' is KB/S, default value is 1048576 KB/S, means 1 GB/S

        for file_local_server in upload_info['asset']:
            local_path = file_local_server['local']
            local_path = RayvisionUtil.str2unicode(local_path)
            server_path = file_local_server['server']
            server_path = RayvisionUtil.str2unicode(server_path)
            if not os.path.exists(local_path):
                print('{0} is not exists.'.format(local_path))
                continue

            transmit_cmd = u'echo y|"{exe_path}" "{engine_type}" "{server_name}" "{server_ip}" "{server_port}" ' \
                            '"{storage_id}" "{user_id}" "{transmit_type}" "{local_path}" "{server_path}" ' \
                            '"{max_connect_failure_count}" "{keep_path}" "{max_speed}"'.format(
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
                keep_path='false',
                max_speed=max_speed
            )
            # print transmit_cmd
            sys.stdout.flush()
            # os.system(transmit_cmd.encode(sys.getfilesystemencoding()))
            RayvisionUtil.run_cmd(transmit_cmd, log_obj=self.G_SDK_LOG)

    def _download(self, job_id_list, local_dir, max_speed=None, **kwargs):
        """
        TODO：Multiple task download
        """
        transmit_type = 'download_files'
        local_dir = RayvisionUtil.str2unicode(local_dir)
        max_speed = str(max_speed) if max_speed is not None else "1048576"  # the unit of 'max_speed' is KB/S, default value is 1048576 KB/S, means 1 GB/S

        job_status_list = self._manage_job_obj.get_job_status(job_id_list)
        output_file_name_list = self._find_output_file_name_iterater(job_status_list)

        for output_file_name in output_file_name_list:
            transmit_cmd = u'echo y|"{exe_path}" "{engine_type}" "{server_name}" "{server_ip}" "{server_port}" ' \
                            '"{download_id}" "{user_id}" "{transmit_type}" "{local_path}" "{server_path}" ' \
                            '"{max_connect_failure_count}" "{keep_path}" "{max_speed}"'.format(
                exe_path=self._rayvision_exe,
                engine_type=self._engine_type,
                server_name=self._server_name,
                server_ip=self._server_ip,
                server_port=self._server_port,
                download_id=self._user_info['output_bid'],
                user_id=self._user_id,
                transmit_type=transmit_type,
                local_path=local_dir,
                server_path=output_file_name,
                max_connect_failure_count='1',  # default is 1
                keep_path='true',
                max_speed=max_speed
            )
            # print transmit_cmd
            sys.stdout.flush()
            # os.system(transmit_cmd.encode(sys.getfilesystemencoding()))
            RayvisionUtil.run_cmd(transmit_cmd, log_obj=self.G_SDK_LOG)


    def _find_output_file_name_iterater(self, job_status_list):
        """
        Find output_file_name from job_status_list
        :param job_status_list: self._manage_job_obj.get_job_status(job_id_list)
        :param dest_list: dest_list
        :return:
        """
        dest_list = []
        for job_status_dict in job_status_list:
            output_file_name = job_status_dict.get('output_file_name', None)
            # is_opener = job_status_dict.get('is_opener')
            sub_job_status = job_status_dict.get('sub_job_status', [])

            if output_file_name is not None:
                dest_list.append(output_file_name)

            if sub_job_status:
                dest_list_sub = self._find_output_file_name_iterater(sub_job_status)
                dest_list.extend(dest_list_sub)

        return dest_list
