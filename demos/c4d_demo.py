#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys

# Add renderSDK path to sys.path
renderSDK_path = r'C:\Users\guokaixing\PycharmProjects\renderSDK'
sys.path.append(renderSDK_path)

from renderSDK.Rayvision import Rayvision

# 1.Log in
rayvision = Rayvision(domain_name='task.foxrenderfarm.com', platform='2', access_id='xxx', access_key='xxx', workspace='c:/renderfarm/sdk_test')

# 2.Set up rendering environment(plug-in configuration, project name）
job_id = rayvision.set_render_env(cg_name='Cinema 4D', cg_version='R19', plugin_config={}, label_name='dasdd')
print(job_id)

# 3.Set up render parameter
scene_info_render = {
    "renderer": {
        "name": "Physical",
        "physical_sampler_mode": "Infinite",
        "physical_sampler": "Adaptive"
    },
    "common": {
        "frames": "0-50[1]",
        "multipass_saveonefile": "1",
        "fps": "30",
        "multipass_save_enabled": "1",
        "frame_rate": "30",
        "multi_pass": {
            "Post Effects": []
        },
        "saved_version": "MAXON CINEMA 4D Studio (R16) 16.038",
        "regular_image_format": "TIFF",
        "multi_pass_format": "PSD",
        "regular_image_saveimage_path": "test_c4d",
        "all_format": [
            "RLA",
            "HDR",
            "PSB",
            "TIFF",
            "TGA",
            "BMP",
            "IFF",
            "JPEG",
            "PICT",
            "PSD",
            "DDS",
            "RPF",
            "B3D",
            "PNG",
            "DPX",
            "EXR"
        ],
        "regular_image_save_enabled": "1",
        "created_version": "MAXON CINEMA 4D Studio (R16) 16.038",
        "all_camera": [
            "Camera.1",
            "Camera"
        ],
        "width": "1080",
        "isConstrained": 0,
        "multipass_saveimage_path": "",
        "height": "1080",
        "c4d_software_version": 19024
    }
}

task_info = {
    'input_cg_file': r"C:\Users\guokaixing\Desktop\test_c4d\test_c4d.c4d",  # The scene file path
    'is_picture': '0',  # Choose if it is the rendered effect picture or not。0: False, 1: True
    'frames_per_task': '1',  # Quantity of frames that rendered on one machine
    'pre_frames': '000',  # The frames of test render
    'job_stop_time': '28800',  # Small task stopped due to timingout，unite is second。default is 8 hours
    'task_stop_time': '86400',  # Big task stopped due to timingout，unite is second。default is 24 hours
    'time_out': '12',  # time-out period，turn into yellow color。unite is second。default is 12 hours
    'stop_after_test': '2',  # Whether to pause the task after the priority rendering is completed, 1: Pause the task after the priority rendering is completed 2. Do not pause the task after the priority rendering is completed
    'channel': '4',  # Submit method
    "task_id": job_id,
    'os_name': '1',  # rendering os type。"0": Linux;  "1": Windows
    'ram': '64'  # rendering machine RAM。"64": 64G；"128": 128G

}

upload_info = {
    "asset": [
        {
            "local": r"C:\Users\guokaixing\Desktop\test_c4d\test_c4d.c4d",
            "server": r"\C\Users\guokaixing\Desktop\test_c4d\test_c4d.c4d"
        },
        {
            "local": r"C:\Users\guokaixing\Desktop\test_c4d\tex\circles.jpg",
            "server": r"\C\Users\guokaixing\Desktop\test_c4d\tex\circles.jpg"
        }
    ]
}

# 4.Submit job
rayvision.submit_job(scene_info_render, task_info, upload_info)

# 5.Download
rayvision.auto_download(job_id_list=[job_id], local_dir=r"c:/renderfarm/sdk_test/output")
# rayvision.auto_download_after_job_completed(job_id_list=[job_id], local_dir=r"c:/renderfarm/sdk_test/output")

