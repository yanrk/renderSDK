#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

# 将最外层renderSDK目录加入python的搜索模块的路径集
renderSDK_path = r'D:\gitlab\renderSDK'
sys.path.append(renderSDK_path)

from renderSDK.Rayvision import Rayvision

# 1.登录
rayvision = Rayvision(domain_name='task.renderbus.com', platform='2', access_id='xxx', access_key='xxx', workspace='c:/renderfarm/sdk_test')

# 2.设置渲染环境（插件配置、所属项目）
rayvision.set_render_env(cg_name='Houdini', cg_version='16.5.268', plugin_config={}, label_name='dasdd')

# 3.分析
scene_info_render, task_info = rayvision.analyse(cg_file=r'D:\gitlab\renderSDK\scenes\houdini_test\sphere.hip', software_path=r'D:\plugins\houdini\165268\bin\hython.exe')

# 4.用户自行处理错误、警告
error_info_list = rayvision.check_error_warn_info()

# 5.用户修改参数列表（可选），并提交作业
scene_info_render_new = scene_info_render
task_info_new = task_info
rayvision.submit_job(scene_info_render_new, task_info_new)

# 6.下载
# rayvision.download(job_id_list=[370274], local_dir=r"d:\project\output")


