#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
API
"""

from .compat import *

import urllib
# import urllib2
import logging
import time
import random
import hashlib
import hmac
import base64
import copy
import collections
from numbers import Number

from .RayvisionException import APIError
from .RayvisionUtil import print_sth

try:  # Python 2.7.9+
    # solve urlopen HTTPS url will verify SSL certificate
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
except:
    pass


class HTTPErrorProcessorNew(urllib2.HTTPErrorProcessor):
    """Process HTTP error responses."""
    handler_order = 1000  # after all other processing

    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()

        # According to RFC 2616, "2xx" code indicates that the client's
        # request was successfully received, understood, and accepted.
        if (not (200 <= code < 300)) and code != 400:
            response = self.parent.error(
                'http', request, response, code, msg, hdrs)

        return response

    https_response = http_response


class RayvisionAPI(object):
    def __init__(self, domain_name, platform, access_id, access_key, log_obj=None):
        """
        API initialization.
        :param str domain_name:  domain name，for example：task.renderbus.com
        :param str platform:  Platform number，for example：2
        :param str access_id:  Authorization id，Used to identity the API caller
        :param str access_key:  Authorization key，Used to encrypt signature strings and server-side validation signature strings
        :param log_obj: Log object or True or None, if True, then is print
        """
        # Choose if to print the API log or no（POST, HTTP Headers, HTTP Body, HTTP Response）
        if log_obj is None:
            self.need_log = False
        else:
            self.need_log = True
            if log_obj is True:
                self.log_obj = print_sth
            else:
                self.log_obj = log_obj.debug

        api_version = '1.0.0'  #API version number
        protocol = 'https'
        
        self.domain_name = domain_name
        self.access_key = access_key
        self._protocol_domain = r'{0}://{1}'.format(protocol, domain_name)  # 如https://task.renderbus.com
        self._headers = {
            'accessId': access_id,  # authorization ID, provided by the rendering platform
            'channel': '4',  # submission method, fixed value: 4
            'platform': platform,  # platform identifier
            'UTCTimestamp': '',  # UTC timestamp (seconds)
            'nonce': '',  # six-digit random number (100000-999999) to prevent replay attacks
            'signature': '',  # data signature (do not participate in signature)
            'version': '1.0.0',  # version number, such as 1.0.0
            'Content-Type': 'application/json'  # content type
        }
        
        self._uri_dict = {
            'queryPlatforms': '/api/render/common/queryPlatforms',  # Get platform list
            'queryUserProfile': '/api/render/user/queryUserProfile',  # Get user details
            'queryUserSetting': '/api/render/user/queryUserSetting',  # Get user settings
            'updateUserSetting': '/api/render/user/updateUserSetting',  # Update user settings
            'getTransferBid': '/api/render/task/getTransferBid',  # Get user transfer BID
            'createTask': '/api/render/task/createTask',  # Create job id
            'submitTask': '/api/render/task/submitTask',  # Submit job
            'queryErrorDetail': '/api/render/common/queryErrorDetail',  # Get the analysis error code
            'getTaskList': '/api/render/task/getTaskList',  # Get the job list
            'stopTask': '/api/render/task/stopTask',  # Stop the job
            'startTask': '/api/render/task/startTask',  # Start job
            'abortTask': '/api/render/task/abortTask',  # Give up the job
            'deleteTask': '/api/render/task/deleteTask',  # Delete job
            'queryTaskFrames': '/api/render/task/queryTaskFrames',  # Get job rendering frame details
            'queryAllFrameStats': '/api/render/task/queryAllFrameStats',  # Get the general  overview of the rendering frame of the job
            'restartFailedFrames': '/api/render/task/restartFailedFrames',  # Re-submit the failed frame
            'restartFrame': '/api/render/task/restartFrame',  # Re-submit the specified frame
            'queryTaskInfo': '/api/render/task/queryTaskInfo',  # Get job details
            'addLabel': '/api/render/common/addLabel',  # Add custom label
            'deleteLabel': '/api/render/common/deleteLabel',  # Delete custom label
            'getLabelList': '/api/render/common/getLabelList',  # Get a custom label
            'querySupportedSoftware': '/api/render/common/querySupportedSoftware',  # Get supported rendering software
            'querySupportedPlugin': '/api/render/common/querySupportedPlugin',  # Get supported rendering software plugins
            'addRenderEnv': '/api/render/common/addRenderEnv',  # Add user rendering environment configuration
            'updateRenderEnv': '/api/render/common/updateRenderEnv',  # Modify user rendering environment configuration
            'deleteRenderEnv': '/api/render/common/deleteRenderEnv',  # Delete user rendering environment configuration
            'setDefaultRenderEnv': '/api/render/common/setDefaultRenderEnv',  # Set the default rendering environment configuration
            'getRenderEnv': '/api/render/common/getRenderEnv'  # Get the user rendering environment configuration
        }

    def _generate_UTCTimestamp(self):
        """
        Generate timestamp (seconds)
        Here's an understanding of timestamps:
            Timestamp of UTC time = UTC current time - local start time
            Local timestamp = local current time - local start time

        :return: UTCTimestamp
        :rtype: str
        """
        return str(int(time.time() + time.timezone))
        
    def _generate_nonce(self):
        """
        Generate a 6-digit random number (100000-999999) to prevent replay attacks
        :return: nonce
        :rtype: str
        """
        return str(random.randrange(100000, 999999))
        
    def _generate_signature(self, key, msg):
        """
        Generate a signature string, first use the sha256 algorithm to calculate the summary of the msg hashed key, and then use the base64 algorithm to get the signature string.
        :param str key: salt
        :param str msg: source string
        :return: signature
        :rtype: str
        """
        key = to_bytes(key)
        msg = to_bytes(msg)

        hash_obj = hmac.new(key, msg=msg, digestmod=hashlib.sha256)
        digest = hash_obj.digest()  # abstract

        signature = base64.b64encode(digest)  # Signature
        return to_unicode(signature)
        
    def _generate_header_body_str(self, api_uri, header, body):
        """
        Generate formatted strings based on Header and Body for generating signatures (signature and Content-Type do not participate in signatures)
        Request Method + Domain Name + API URI + Request String
        :param str api_uri:
        :param dict header:
        :param dict body:
        """
        result_str = ''
        header = copy.deepcopy(header)
        body = copy.deepcopy(body)
        try:
            header.pop('signature')
        except:
            pass
        try:
            header.pop('Content-Type')
        except:
            pass
        header_body_dict = self._header_body_sort(header, body)
        
        header_body_list = []
        for key, value in header_body_dict.items():
            header_body_list.append('{0}={1}'.format(key, value))
        header_body_str = '&'.join(header_body_list)
        
        result_str = '[POST]{domain_name}:{api_uri}&{header_body_str}'.format(
            domain_name=self.domain_name,
            api_uri=api_uri,
            header_body_str=header_body_str
        )
        
        return result_str
    
    def _header_body_sort(self, header, body):
        """
        Sort all custom http request headers and request parameters in ascending order by lexicographical order (ASCII) of the parameter name
        :param dict header: request header
        :param dict body: request parameters
        :return: Ordered dictionary object after request header and request parameters are sorted
        :rtype: OrderedDict
        """
        mix_dict = copy.deepcopy(header)
        body = copy.deepcopy(body)
        mix_dict.update(body)
        
        # Handling complex objects
        mix_dict_new = self._handle_complex_dict(mix_dict)
        
        sorted_key_list = sorted(mix_dict_new)  # Sorted dictionary
        
        new_dict = collections.OrderedDict()  # ordered dictionary
        for key in sorted_key_list:
            new_dict[key] = mix_dict_new[key]
            
        return new_dict
        
    def _handle_complex_dict(self, mix_dict):
        """
        "formatted" dictionary
        Possible data types in the dictionary: numbers.Number, str, bytes, list, dict, None (json's key can only be string, json's value may be number, string, logical value, array, object, null)
        Such as
        {
            "taksId":2,
            "renderEnvs":[
                {
                    "envId":1,
                    "pluginIds":[
                        2,
                        3,
                        4
                    ]
                },
                {
                    "envId":3,
                    "pluginIds":[
                        7,
                        8,
                        10
                    ]
                }
            ]
        }
        # The formatting result is as follows
        {
            "taksId":2
            "renderEnvs0.envId":1
            "renderEnvs0.pluginIds0":2
            "renderEnvs0.pluginIds1":3
            "renderEnvs0.pluginIds2":4
            "renderEnvs1.envId":3
            "renderEnvs1.pluginIds0":7
            "renderEnvs1.pluginIds1":8
            "renderEnvs1.pluginIds2":10
        }
       
        """
        new_dict = {}
        def _format_dict(value, key=None):
            """
            :param value: 
            :param key: None/str, If the key is None, the value is the source dictionary object.
            """
            if isinstance(value, dict):
                for key_new_part, value in value.items():
                    if key is None:
                        new_key = key_new_part
                    else:
                        new_key = '{0}.{1}'.format(key, key_new_part)
                    _format_dict(value, new_key)
                    
            elif isinstance(value, list):
                for index, value in enumerate(value):
                    new_key = '{0}{1}'.format(key, index)
                    _format_dict(value, new_key)
                   
            elif isinstance(value, Number):
                new_dict[key] = value
            elif isinstance(value, (str, bytes)):
                new_dict[key] = value
            elif value is None:
                new_dict[key] = value
                
        _format_dict(mix_dict)
        return new_dict
        
    def _post(self, api_uri, data={}):
        """
        Send an post request and return data object if no error occurred.
        :param str api_uri: The api uri.
        :param dict data:
        :return:
        :rtype: dict/List/None
        """
        url = r'{0}{1}'.format(self._protocol_domain, api_uri)
        
        headers = copy.deepcopy(self._headers)
        headers['UTCTimestamp'] = self._generate_UTCTimestamp()
        headers['nonce'] = self._generate_nonce()
        
        msg = self._generate_header_body_str(api_uri, headers, data)
        headers['signature'] = self._generate_signature(self.access_key, msg)
        
        # http_body = urllib.urlencode(data)
        http_headers = json.dumps(headers)
        http_body = json.dumps(data)
        
        if self.need_log:
            self.log_obj('POST: {0}'.format(url))
            self.log_obj('HTTP Headers: {0}'.format(http_headers))
            self.log_obj('HTTP Body: {0}'.format(http_body))

        # add handler HTTPErrorProcessorNew to get HTTP400's response
        opener = urllib2.build_opener(HTTPErrorProcessorNew)

        request = urllib2.Request(url, data=http_body.encode('utf-8'), headers=headers)
        
        try:
            response = opener.open(request, timeout=8)
        except Exception as e:
            return_message = e
            raise APIError(400, return_message, url)  # Bad request

        content = response.read().decode('utf-8')
        r = json.loads(content)
        if self.need_log:
            self.log_obj('HTTP Response: {0}'.format(content))

        return_code = r.get('code', -1)
        return_message = r.get('message', 'No message!!!')
        return_data = r.get('data', None)

        if return_code != 200:
            raise APIError(return_code, return_message, url)
        return return_data

    def query_platforms(self):
        """
        Get platform
        """
        api_uri = self._uri_dict.get('queryPlatforms')
        zone = 1 if 'renderbus' in self.domain_name.lower() else 2
        data = {
            'zone': zone
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def query_user_profile(self):
        """
        Get user profile
        """
        api_uri = self._uri_dict.get('queryUserProfile')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def query_user_setting(self):
        """
        Get user setting
        """
        api_uri = self._uri_dict.get('queryUserSetting')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def update_user_setting(self, task_over_time):
        """
        Update user settings
        :param int task_over_time: job timeout setting
        """
        api_uri = self._uri_dict.get('updateUserSetting')
        data = {
            'taskOverTime': int(task_over_time)
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def get_transfer_bid(self):
        """
        Get user transfer BID
        """
        api_uri = self._uri_dict.get('getTransferBid')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def create_task(self, count=1, out_user_id=None):
        """
        Create job ID
        :param int count: the quantity of job ID
        :param long out_user_id: Non-required, external user ID, used to distinguish users accessing third parties
        """
        api_uri = self._uri_dict.get('createTask')
        data = {
            'count': int(count)
        }
        if out_user_id is not None:
            data['outUserId'] = out_user_id
        r_data = self._post(api_uri, data)
        return r_data
        
    def submit_task(self, task_id):
        """
        Submit job
        :param int task_id: Submit job ID
        """
        api_uri = self._uri_dict.get('submitTask')
        data = {
            'taskId': int(task_id)
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def query_error_detail(self, code, language='0'):
        """
        Get analysis error code
        :param str code: required value, error code
        :param str language: not required, language, 0: Chinese (default) 1: English
        """
        api_uri = self._uri_dict.get('queryErrorDetail')
        data = {
            'code': str(code),
            'language': language
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def get_task_list(self, page_num, page_size):
        """
        Get job list
        :param int page_num: required value, current page
        :param int page_size: required value, numbers displayed per page
        """
        api_uri = self._uri_dict.get('getTaskList')
        data = {
            'pageNum': int(page_num),
            'pageSize': int(page_size)
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def stop_task(self, task_param_list):
        """
        Stop the job
        :param list task_param_list: job ID list
        """
        api_uri = self._uri_dict.get('stopTask')
        data = {
            'taskParam': task_param_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def start_task(self, task_param_list):
        """
        Start job
        :param list task_param_list: job ID list
        """
        api_uri = self._uri_dict.get('startTask')
        data = {
            'taskParam': task_param_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def abort_task(self, task_param_list):
        """
        Give up the job
        :param list task_param_list: job ID list
        """
        api_uri = self._uri_dict.get('abortTask')
        data = {
            'taskParam': task_param_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def delete_task(self, task_param_list):
        """
        Delete job
        :param list task_param_list: job ID list
        """
        api_uri = self._uri_dict.get('deleteTask')
        data = {
            'taskParam': task_param_list
        }
        r_data = self._post(api_uri, data)
        return r_data

    def query_task_frames(self, task_id, page_num, page_size, search_keyword=None):
        """
        Get job rendering frame details
        :param int task_id: The job ID number, which is the unique identifier of the job, required field
        :param int page_num: current page number
        :param int page_size: displayed data size per page
        :param str search_keyword: is a string, which is queried according to the name of a multi-frame name of a machine rendering, optional
        """
        api_uri = self._uri_dict.get('queryTaskFrames')
        data = {
            'taskId': int(task_id),
            'pageNum': int(page_num),
            'pageSize': int(page_size)
        }
        if search_keyword is not None:
            data['searchKeyword'] = search_keyword
        r_data = self._post(api_uri, data)
        return r_data

    def query_all_frame_stats(self):
        """
        Get the overview of job rendering frame
        """
        api_uri = self._uri_dict.get('queryAllFrameStats')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def restart_failed_frames(self, task_param_list):
        """
        Re-submit the failed frame
        :param list task_param_list: job ID list
        """
        api_uri = self._uri_dict.get('restartFailedFrames')
        data = {
            'taskParam': task_param_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def restart_frame(self, task_id, select_all, ids_list=[]):
        """
        Re-submit the specified frame
        :param int task_param_list: job ID
        :param list ids_list: Frame ID list, valid when selectAll is 0
        :param int select_all: whether to re-request all, 1 all re-raised, 0 specified frame re-request
        """
        api_uri = self._uri_dict.get('restartFrame')
        data = {
            'taskId': int(task_id),
            'ids': ids_list,
            'selectAll': int(select_all)
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def query_task_info(self, task_ids_list):
        """
        Get job details
        :param list task_ids_list: shell job ID list
        """
        api_uri = self._uri_dict.get('queryTaskInfo')
        data = {
            'taskIds': task_ids_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def add_label(self, new_name, status):
        """
        Add a custom label
        :param str new_name:  label name
        :param str status:  label status
        """
        api_uri = self._uri_dict.get('addLabel')
        data = {
            'newName': new_name,
            'status': status
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def delete_label(self, del_name):
        """
        Delete custom label
        :param str del_name: the name of the  label to be deleted
        """
        api_uri = self._uri_dict.get('deleteLabel')
        data = {
            'delName': del_name
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def get_label_list(self):
        """
        Get custom labels
        """
        api_uri = self._uri_dict.get('getLabelList')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def query_supported_software(self):
        """
        Get supported rendering software
        """
        api_uri = self._uri_dict.get('querySupportedSoftware')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def query_supported_plugin(self, cg_id):
        """
        Get supported rendering software plugins
        :param int cg_id: rendering software ID
        """
        api_uri = self._uri_dict.get('querySupportedPlugin')
        data = {
            'cgId': int(cg_id)
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def add_render_env(self, cg_id, cg_name, cg_version, render_layer_type, edit_name, render_system, plugin_ids_list):
        """
        Adjust user rendering environment configuration
        :param int cg_id: rendering software ID
        :param str cg_name: rendering software name
        :param str cg_version: rendering software version
        :param int render_layer_type: maya render type
        :param str edit_name: rendering environment custom name
        :param int render_system: rendering system, 0 linux, 1 windows
        :param list plugin_ids_list: Rendering plugin collection
        """
        api_uri = self._uri_dict.get('addRenderEnv')
        data = {
            'cgId': int(cg_id),
            'cgName': cg_name,
            'cgVersion': cg_version,
            'renderLayerType': int(render_layer_type),
            'editName': edit_name,
            'renderSystem': int(render_system),
            'pluginIds': plugin_ids_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def update_render_env(self, cg_id, cg_name, cg_version, render_layer_type, edit_name, render_system, plugin_ids_list):
        """
        Modify the user rendering environment configuration
        :param int cg_id: rendering software ID
        :param str cg_name: rendering software name
        :param str cg_version: rendering software version
        :param int render_layer_type: maya render type
        :param str edit_name: rendering environment custom name
        :param int render_system: rendering system, 0 linux, 1 windows
        :param list plugin_ids_list: Rendering plugin list
        """
        api_uri = self._uri_dict.get('updateRenderEnv')
        data = {
            'cgId': int(cg_id),
            'cgName': cg_name,
            'cgVersion': cg_version,
            'renderLayerType': int(render_layer_type),
            'editName': edit_name,
            'renderSystem': int(render_system),
            'pluginIds': plugin_ids_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def delete_render_env(self, edit_name):
        """
        Delete user rendering environment configuration
        :param str edit_name: rendering environment custom name
        """
        api_uri = self._uri_dict.get('deleteRenderEnv')
        data = {
            'editName': edit_name
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def set_default_render_env(self, edit_name):
        """
        Delete user rendering environment configuration
        :param str edit_name: rendering environment custom name
        """
        api_uri = self._uri_dict.get('setDefaultRenderEnv')
        data = {
            'editName': edit_name
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def get_render_env(self, cg_id):
        """
        Get the user rendering environment configuration
        :param int cg_id: rendering software ID
        """
        api_uri = self._uri_dict.get('getRenderEnv')
        data = {
            'cgId': int(cg_id)
        }
        r_data = self._post(api_uri, data)
        return r_data
        
        
if __name__ == '__main__':
    pass
