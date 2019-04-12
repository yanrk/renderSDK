#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

# Add renderSDK path to sys.path
renderSDK_path = r'D:\gitlab\renderSDK'
sys.path.append(renderSDK_path)

from renderSDK.Rayvision import Rayvision

# 1.Log in
rayvision = Rayvision(domain_name='task.foxrenderfarm.com', platform='2', access_id='xxx', access_key='xxx', workspace='c:/renderfarm/sdk_test')

# 2.Set up rendering environment(plug-in configuration, project name)
job_id = rayvision.set_render_env(cg_name='VR Standalone', cg_version='standalone_vray3.10.03', plugin_config={}, label_name='dasdd')

# 3.Set up render parameter

task_info = {
    'input_cg_file': r'H:\test2014vr_vraystandaloneaCopy.vrscene',
    'is_distribute_render': '1',
    'distribute_render_node': '3'
}

upload_info = {
    "asset": [
        {
            "local": r"H:\test2014vr_vraystandaloneaCopy.vrscene", 
            "server": r"\H\test2014vr_vraystandaloneaCopy.vrscene"
        }
    ]
}

# 4.Submit job
rayvision.submit_job(task_info=task_info, upload_info=upload_info, max_speed=100)

# 5.Download
rayvision.auto_download(job_id_list=[job_id], local_dir=r"c:/renderfarm/sdk_test/output")
# rayvision.auto_download_after_job_completed(job_id_list=[job_id], local_dir=r"c:/renderfarm/sdk_test/output")
