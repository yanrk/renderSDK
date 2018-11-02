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

class RayvisionAPI(object):
    def __init__(self, domain_name, platform, access_id, access_key, log_obj=None):
        """
        API initialization.
        :param str domain_name:  域名，如：task.renderbus.com
        :param str platform:  平台号，如：2
        :param str access_id:  授权id，用于标识API调用者身份
        :param str access_key:  授权密钥，用于加密签名字符串和服务器端验证签名字符串
        :param log_obj: 日志对象或True或None，如为True，则print
        """
        # 是否需要打印API日志（POST, HTTP Headers, HTTP Body, HTTP Response）
        if log_obj is None:
            self.need_log = False
        else:
            self.need_log = True
            if log_obj is True:
                self.log_obj = print_sth
            else:
                self.log_obj = log_obj.debug

        api_version = '1.0.0'  # API版本号
        protocol = 'https'
        
        self.domain_name = domain_name
        self.access_key = access_key
        self._protocol_domain = r'{0}://{1}'.format(protocol, domain_name)  # 如https://task.renderbus.com
        self._headers = {
            'accessId': access_id,  # 授权ID，由渲染平台提供
            'channel': '4',  # 提交方式，固定值: 4
            'platform': platform,  # 平台标识
            'UTCTimestamp': '',  # UTC时间戳（秒）
            'nonce': '',  # 六位随机数（100000-999999），防止重放攻击
            'signature': '',  # 数据签名（不参与签名）
            'version': '1.0.0',  # 版本号，如1.0.0
            'Content-Type': 'application/json'  # 内容类型
        }
        
        self._uri_dict = {
            'queryPlatforms': '/api/render/common/queryPlatforms',  # 获取平台列表
            'queryUserProfile': '/api/render/user/queryUserProfile',  # 获取用户详情
            'queryUserSetting': '/api/render/user/queryUserSetting',  # 获取用户设置
            'updateUserSetting': '/api/render/user/updateUserSetting',  # 更新用户设置
            'getTransferBid': '/api/render/task/getTransferBid',  # 获取用户传输BID
            'createTask': '/api/render/task/createTask',  # 创建任务号
            'submitTask': '/api/render/task/submitTask',  # 提交任务
            'queryErrorDetail': '/api/render/common/queryErrorDetail',  # 获取分析错误码
            'getTaskList': '/api/render/task/getTaskList',  # 获取任务列表
            'stopTask': '/api/render/task/stopTask',  # 停止任务
            'startTask': '/api/render/task/startTask',  # 开始任务
            'abortTask': '/api/render/task/abortTask',  # 放弃任务
            'deleteTask': '/api/render/task/deleteTask',  # 删除任务
            'queryTaskFrames': '/api/render/task/queryTaskFrames',  # 获取任务渲染帧详情
            'queryAllFrameStats': '/api/render/task/queryAllFrameStats',  # 获取任务总渲染帧概况
            'restartFailedFrames': '/api/render/task/restartFailedFrames',  # 重提失败帧
            'restartFrame': '/api/render/task/restartFrame',  # 重提任务指定帧
            'queryTaskInfo': '/api/render/task/queryTaskInfo',  # 获取任务详情
            'addLabel': '/api/render/common/addLabel',  # 添加自定义标签
            'deleteLabel': '/api/render/common/deleteLabel',  # 删除自定义标签
            'getLabelList': '/api/render/common/getLabelList',  # 获取自定义标签
            'querySupportedSoftware': '/api/render/common/querySupportedSoftware',  # 获取支持的渲染软件
            'querySupportedPlugin': '/api/render/common/querySupportedPlugin',  # 获取支持的渲染软件插件
            'addRenderEnv': '/api/render/common/addRenderEnv',  # 新增用户渲染环境配置
            'updateRenderEnv': '/api/render/common/updateRenderEnv',  # 修改用户渲染环境配置
            'deleteRenderEnv': '/api/render/common/deleteRenderEnv',  # 删除用户渲染环境配置
            'setDefaultRenderEnv': '/api/render/common/setDefaultRenderEnv',  # 设置默认渲染环境配置
            'getRenderEnv': '/api/render/common/getRenderEnv'  # 获取用户渲染环境配置
        }

    def _generate_UTCTimestamp(self):
        """
        生成时间戳（秒）
        这里对时间戳的理解：
            UTC时间的时间戳 = UTC当前时间 - 本地起始时间
            本地时间戳 = 本地当前时间 - 本地起始时间

        :return: UTCTimestamp
        :rtype: str
        """
        return str(int(time.time() + time.timezone))
        
    def _generate_nonce(self):
        """
        生成6位随机数(100000-999999)，防止重放攻击
        :return: nonce
        :rtype: str
        """
        return str(random.randrange(100000, 999999))
        
    def _generate_signature(self, key, msg):
        """
        生成签名字符串，先用sha256算法将msg加盐key计算出摘要，再将摘要用base64算法得出签名字符串
        :param str key: salt
        :param str msg: source string
        :return: signature
        :rtype: str
        """
        key = to_bytes(key)
        msg = to_bytes(msg)

        hash_obj = hmac.new(key, msg=msg, digestmod=hashlib.sha256)
        digest = hash_obj.digest()  # 摘要

        signature = base64.b64encode(digest)  # 签名
        return to_unicode(signature)
        
    def _generate_header_body_str(self, api_uri, header, body):
        """
        根据Header和Body生成格式化字符串，用于生成签名（signature和Content-Type不参与签名）
        请求方法 + 域名 + API URI + 请求字符串
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
        对所有 自定义 http请求头 和 请求参数 按参数名的字典序（ASCII 码）升序排序
        :param dict header: 请求头
        :param dict body: 请求参数
        :return: 请求头与请求参数排序后的有序字典对象
        :rtype: OrderedDict
        """
        mix_dict = copy.deepcopy(header)
        body = copy.deepcopy(body)
        mix_dict.update(body)
        
        # 处理复杂对象
        mix_dict_new = self._handle_complex_dict(mix_dict)
        
        sorted_key_list = sorted(mix_dict_new)  # 排序好的字典
        
        new_dict = collections.OrderedDict()  # 有序字典
        for key in sorted_key_list:
            new_dict[key] = mix_dict_new[key]
            
        return new_dict
        
    def _handle_complex_dict(self, mix_dict):
        """
        "格式化"字典
        该字典中可能的数据类型：numbers.Number, str, bytes, list, dict, None（json的key只能为string，json的value可能为数字、字符串、逻辑值、数组、对象、null）
        如
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
        #格式化结果如下
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
            :param key: None/str, key若为None，说明value为源字典对象
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
        
        request = urllib2.Request(url, data=http_body.encode('utf-8'), headers=headers)
        
        try:
            response = urllib2.urlopen(request, timeout=18)
        except Exception as e:
            return_message = e
            raise APIError(400, return_message, url)  # Bad request

        content = response.read().decode('utf-8')
        r = json.loads(content)
        if self.need_log:
            self.log_obj('HTTP Response: {0}'.format(r))

        return_code = r.get('code', -1)
        return_message = r.get('message', 'No message!!!')
        return_data = r.get('data', None)

        if return_code != 200:
            raise APIError(return_code, return_message, url)
        return return_data

    def query_platforms(self):
        """
        获取平台列表
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
        获取用户详情
        """
        api_uri = self._uri_dict.get('queryUserProfile')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def query_user_setting(self):
        """
        获取用户设置
        """
        api_uri = self._uri_dict.get('queryUserSetting')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def update_user_setting(self, task_over_time):
        """
        更新用户设置
        :param int task_over_time: 任务超时时间设置
        """
        api_uri = self._uri_dict.get('updateUserSetting')
        data = {
            'taskOverTime': int(task_over_time)
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def get_transfer_bid(self):
        """
        获取用户传输BID
        """
        api_uri = self._uri_dict.get('getTransferBid')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def create_task(self, count=1, out_user_id=None):
        """
        创建任务号
        :param int count: 创建任务号数量
        :param long out_user_id: 非必须，外部用户ID，用于区分第三方接入的用户
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
        提交任务
        :param int task_id: 提交任务ID
        """
        api_uri = self._uri_dict.get('submitTask')
        data = {
            'taskId': int(task_id)
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def query_error_detail(self, code, language='0'):
        """
        获取分析错误码
        :param str code: 必须值，错误码
        :param str language: 非必须，语言, 0：中文（默认） 1：英文
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
        获取任务列表
        :param int page_num: 必须值，当前页数
        :param int page_size: 必须值，每页显示数量
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
        停止任务
        :param list task_param_list: 任务号列表
        """
        api_uri = self._uri_dict.get('stopTask')
        data = {
            'taskParam': task_param_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def start_task(self, task_param_list):
        """
        开始任务
        :param list task_param_list: 任务号列表
        """
        api_uri = self._uri_dict.get('startTask')
        data = {
            'taskParam': task_param_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def abort_task(self, task_param_list):
        """
        放弃任务
        :param list task_param_list: 任务号列表
        """
        api_uri = self._uri_dict.get('abortTask')
        data = {
            'taskParam': task_param_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def delete_task(self, task_param_list):
        """
        删除任务
        :param list task_param_list: 任务号列表
        """
        api_uri = self._uri_dict.get('deleteTask')
        data = {
            'taskParam': task_param_list
        }
        r_data = self._post(api_uri, data)
        return r_data

    def query_task_frames(self, task_id, page_num, page_size, search_keyword=None):
        """
        获取任务渲染帧详情
        :param int task_id: 任务ID号，是任务的唯一标识，必填字段
        :param int page_num: 当前页编号
        :param int page_size: 每页显示数据大小
        :param str search_keyword: 是一个字符串，根据一机渲多帧名这个字段名进行查询,选填
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
        获取任务总渲染帧概况
        """
        api_uri = self._uri_dict.get('queryAllFrameStats')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def restart_failed_frames(self, task_param_list):
        """
        重提失败帧
        :param list task_param_list: 任务号列表
        """
        api_uri = self._uri_dict.get('restartFailedFrames')
        data = {
            'taskParam': task_param_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def restart_frame(self, task_id, select_all, ids_list=[]):
        """
        重提任务指定帧
        :param int task_param_list: 任务ID
        :param list ids_list: 帧ID集合, selectAll为0时生效
        :param int select_all: 是否全部重提, 1全部重提，0指定帧重提
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
        获取任务详情
        :param list task_ids_list: 壳任务ID集合
        """
        api_uri = self._uri_dict.get('queryTaskInfo')
        data = {
            'taskIds': task_ids_list
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def add_label(self, new_name, status):
        """
        添加自定义标签
        :param str new_name: 标签名
        :param str status: 标签状态
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
        删除自定义标签
        :param str del_name: 待删除的标签名
        """
        api_uri = self._uri_dict.get('deleteLabel')
        data = {
            'delName': del_name
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def get_label_list(self):
        """
        获取自定义标签
        """
        api_uri = self._uri_dict.get('getLabelList')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def query_supported_software(self):
        """
        获取支持的渲染软件
        """
        api_uri = self._uri_dict.get('querySupportedSoftware')
        data = {}
        r_data = self._post(api_uri, data)
        return r_data
        
    def query_supported_plugin(self, cg_id):
        """
        获取支持的渲染软件插件
        :param int cg_id: 渲染软件ID
        """
        api_uri = self._uri_dict.get('querySupportedPlugin')
        data = {
            'cgId': int(cg_id)
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def add_render_env(self, cg_id, cg_name, cg_version, render_layer_type, edit_name, render_system, plugin_ids_list):
        """
        新增用户渲染环境配置
        :param int cg_id: 渲染软件ID
        :param str cg_name: 渲染软件名称
        :param str cg_version: 渲染软件版本
        :param int render_layer_type: maya渲染类型
        :param str edit_name: 渲染环境自定义名
        :param int render_system: 渲染系统, 0 linux, 1 windows
        :param list plugin_ids_list: 渲染插件集合
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
        修改用户渲染环境配置
        :param int cg_id: 渲染软件ID
        :param str cg_name: 渲染软件名称
        :param str cg_version: 渲染软件版本
        :param int render_layer_type: maya渲染类型
        :param str edit_name: 渲染环境自定义名
        :param int render_system: 渲染系统, 0 linux, 1 windows
        :param list plugin_ids_list: 渲染插件集合
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
        删除用户渲染环境配置
        :param str edit_name: 渲染环境自定义名
        """
        api_uri = self._uri_dict.get('deleteRenderEnv')
        data = {
            'editName': edit_name
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def set_default_render_env(self, edit_name):
        """
        删除用户渲染环境配置
        :param str edit_name: 渲染环境自定义名
        """
        api_uri = self._uri_dict.get('setDefaultRenderEnv')
        data = {
            'editName': edit_name
        }
        r_data = self._post(api_uri, data)
        return r_data
        
    def get_render_env(self, cg_id):
        """
        获取用户渲染环境配置
        :param int cg_id: 渲染软件ID
        """
        api_uri = self._uri_dict.get('getRenderEnv')
        data = {
            'cgId': int(cg_id)
        }
        r_data = self._post(api_uri, data)
        return r_data
        
        
if __name__ == '__main__':
    pass