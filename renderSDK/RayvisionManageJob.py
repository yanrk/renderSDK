#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Manage Job Module.
"""

from .compat import *

import os
import sys
from . import RayvisionUtil


class RayvisionManageJob(object):
    def __init__(self, api_obj):
        self._api_obj = api_obj
        
    def is_job_end(self, job_id):
        """
        Check whether the job is end.
        :param int job_id: 111
        :return: True/False
        :rtype: bool
        """
        result = None
        job_end_status_code_list = ['10', '20', '23', '25', '30', '35', '45']  # see RayvisionUtil.py  job_status_description_dict
        
        job_status_list = self.get_job_status([job_id])
        job_status_code_list = self._find_job_status_code_iterater(job_status_list)
        if job_status_code_list:
            for job_status_code in job_status_code_list:
                if job_status_code not in job_end_status_code_list:
                    result = False
                    break
            if result is not False:
                result = True
            
        return result
        
    def get_job_status(self, job_id_list):
        """
        Input job_id to get job status.
        :param list<int> job_id_list: [111, 222]
        :return:
            [
                {
                    "job_id":"111",
                    "job_status_code":"25",
                    "job_status_text":"render_task_status_25",
                    "job_status_description":"Done",
                    "is_opener":"0",
                    "output_file_name":"111_test",
                    "sub_job_status":[]
                },
                {
                    "job_id":"222",
                    "job_status_code":"0",
                    "job_status_text":"render_task_status_0",
                    "job_status_description":"Waiting",
                    "is_opener":"1",
                    "output_file_name":None,
                    "sub_job_status":[
                        {
                            "job_id":"333",
                            "job_status_code":"25",
                            "job_status_text":"render_task_status_25",
                            "job_status_description":"Done",
                            "is_opener":"0",
                            "output_file_name":"333_test",
                            "sub_job_status":[]
                        }
                    ]
                }
            ]
        :rtype: list<dict>
        """
        
        task_info_list = self._api_obj.query_task_info(job_id_list).get('items', [])
        job_status_list = self._task_info_iterater(task_info_list)
        return job_status_list
            
    def _task_info_iterater(self, task_info_list):
        """
        :param task_info_list:
        :return: 
        :rtype: list
        """
        job_status_list = []
        for task_info in task_info_list:
            job_status_dict = {}
            
            job_id = task_info.get('id')
            job_status_code = task_info.get('taskStatus')  # e.g. 25
            job_status_text = task_info.get('statusText')  # e.g. "render_task_status_25"
            is_opener = task_info.get('isOpen')  # 0: have not sub_job_status; 1:have sub_job_status
            output_file_name = task_info.get('outputFileName')  # download directory name
            job_status_description = RayvisionUtil.get_job_status_description(job_status_code)
            sub_job_status = []
            if int(is_opener) == 1:
                task_info_list_new = task_info.get('respRenderingTaskList', [])
                sub_job_status = self._task_info_iterater(task_info_list_new)
            
            job_status_dict['job_id'] = str(job_id)
            job_status_dict['job_status_code'] = str(job_status_code)
            job_status_dict['job_status_text'] = str(job_status_text)
            job_status_dict['job_status_description'] = job_status_description
            job_status_dict['is_opener'] = str(is_opener)
            job_status_dict['output_file_name'] = output_file_name
            job_status_dict['sub_job_status'] = sub_job_status
            
            job_status_list.append(job_status_dict)
            
        return job_status_list

    def _find_output_file_name_iterater(self, job_status_list):
        """
        Find output_file_name from job_status_list
        :param job_status_list: self._manage_job_obj.get_job_status(job_id_list)
        :return dest_list: dest_list
        :rtype: list<str>
        """
        dest_list = []
        for job_status_dict in job_status_list:
            output_file_name = job_status_dict.get('output_file_name', None)
            is_opener = job_status_dict.get('is_opener')
            sub_job_status = job_status_dict.get('sub_job_status', [])

            if int(is_opener) == 1:  # have sub tasks
                if sub_job_status:
                    dest_list_sub = self._find_output_file_name_iterater(sub_job_status)
                    dest_list.extend(dest_list_sub)
            else:
                if output_file_name is not None:
                    dest_list.append(output_file_name)

        return dest_list
        
    def _find_job_status_code_iterater(self, job_status_list):
        """
        Find job_status_code from job_status_list
        :param job_status_list: self._manage_job_obj.get_job_status(job_id_list)
        :return: dest_list
        :rtype: list<int>
        """
        dest_list = []
        for job_status_dict in job_status_list:
            job_status_code = job_status_dict.get('job_status_code', None)
            is_opener = job_status_dict.get('is_opener')
            sub_job_status = job_status_dict.get('sub_job_status', [])

            if int(is_opener) == 1:  # have sub tasks
                if sub_job_status:
                    dest_list_sub = self._find_job_status_code_iterater(sub_job_status)
                    dest_list.extend(dest_list_sub)
            else:
                if job_status_code is not None:
                    dest_list.append(job_status_code)

        return dest_list
