#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

# Add renderSDK path to sys.path
renderSDK_path = r'/root/chensr/renderSDK'
sys.path.append(renderSDK_path)

from renderSDK.Rayvision import Rayvision

workspace=r'/root/chensr/renderSDK/sdk_test'

# 1.Log in
rayvision = Rayvision(domain_name='task.foxrenderfarm.com', platform='2', access_id='xxx', access_key='xxx', workspace=workspace)

# 2.Set up rendering environment(plug-in configuration, project name）
job_id = rayvision.set_render_env(cg_name='Katana', cg_version='2.6v3', plugin_config={}, label_name='dasdd')

# 3.Set up render parameter
scene_info_render = {
    "rendernodes": {
        "001_005_Render": {
            "frames": "1-1[1]", 
            "aov": {
                "specular": "/w/aovs/specular_1.exr", 
                "diffuse": "/w/aovs/diffuse_1.exr", 
                "primary": "/w/aovs/beauty_1.exr"
            }, 
            "renderable": "1", 
            "denoise": "0"
        }
    }
}

task_info = {
    'input_cg_file': r'/root/chensr/renderSDK/scenes/001_005_test.katana',
    'os_name': '0'  # Linux
}

upload_info = {
    "asset": [
        {
            "local": "/root/chensr/renderSDK/scenes/001_005_test.katana", 
            "server": "/root/chensr/renderSDK/scenes/001_005_test.katana"
        }
    ]
}

# 4.Submit job
rayvision.submit_job(scene_info_render, task_info, upload_info, max_speed=100)

# 5.Download
rayvision.auto_download(job_id_list=[job_id], local_dir=r"/root/chensr/renderSDK/sdk_test/output")
# rayvision.auto_download_after_job_completed(job_id_list=[job_id], local_dir=r"c:/renderfarm/sdk_test/output")
