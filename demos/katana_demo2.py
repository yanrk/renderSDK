#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import sys

# Add renderSDK path to sys.path
renderSDK_path = r'/root/chensr/renderSDK'
sys.path.append(renderSDK_path)

from renderSDK.Rayvision import Rayvision

workspace='/root/chensr/renderSDK/sdk_test'

# 1.Log in
rayvision = Rayvision(domain_name='task.foxrenderfarm.com', platform='2', access_id='xxx', access_key='xxx', workspace=workspace)

# 2.Set up rendering environment(plug-in configuration, project name）
rayvision.set_render_env(cg_name='Katana', cg_version='2.6v3', plugin_config={}, label_name='dasdd')

# 3.Set up render parameter
scene_info_render = {
    "rendernodes": {
        "825_100_r1_envir_Din_Apt_Curtain_MATTE": {
            "frames": "101-103[1]", 
            "aov": {
                "denoiseVariance": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt_Curtain/preDenoise/denoiseVariance/beauty_variance.0101.exr", 
                "BTY": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt_Curtain/preDenoise/BTY/Din_Apt_Curtain_BTY.0101.exr", 
                "denoise_BTY": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_envir_Din_Apt_Curtain_MATTE_denoise_BTY_misc_raw.101.exr", 
                "denoise_primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_envir_Din_Apt_Curtain_MATTE_denoise_primary_misc_raw.101.exr", 
                "cpuTime": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt_Curtain/preDenoise/cpuTime/Din_Apt_Curtain_cpuTime.0101.exr", 
                "primary": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt_Curtain/preDenoise/primary/Din_Apt_Curtain_primary.0101.exr", 
                "MATTE": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt_Curtain/MATTE/Din_Apt_Curtain_MATTE.0101.exr", 
                "DATA": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt_Curtain/DATA/Din_Apt_Curtain_DATA.0101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }, 
        "825_100_r1_envir_Din_Apt_Curtain_BTY": {
            "frames": "101-103[1]", 
            "aov": {
                "denoiseVariance": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt_Curtain/preDenoise/denoiseVariance/beauty_variance.0101.exr", 
                "BTY": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt_Curtain/preDenoise/BTY/Din_Apt_Curtain_BTY.0101.exr", 
                "denoise_BTY": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_envir_Din_Apt_Curtain_BTY_denoise_BTY_misc_raw.101.exr", 
                "denoise_primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_envir_Din_Apt_Curtain_BTY_denoise_primary_misc_raw.101.exr", 
                "cpuTime": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt_Curtain/preDenoise/cpuTime/Din_Apt_Curtain_cpuTime.0101.exr", 
                "primary": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt_Curtain/preDenoise/primary/Din_Apt_Curtain_primary.0101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }, 
        "825_100_r1_char_din_MATTE": {
            "frames": "101-103[1]", 
            "aov": {
                "MATTE": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/din/MATTE/din_MATTE.0101.exr", 
                "DATA": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/din/DATA/din_DATA.0101.exr", 
                "primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_char_din_MATTE_primary_rgba_misc_linear.101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }, 
        "825_100_r1_char_long_MATTE": {
            "frames": "101-256[1]", 
            "aov": {
                "MATTE": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/long/MATTE/long_MATTE.0101.exr", 
                "DATA": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/long/DATA/long_DATA.0101.exr", 
                "primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_char_long_MATTE_primary_rgba_misc_linear.101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }, 
        "825_100_r1_envir_Din_Apt_BTY": {
            "frames": "101-103[1]", 
            "aov": {
                "denoiseVariance": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt/preDenoise/denoiseVariance/beauty_variance.0101.exr", 
                "BTY": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt/preDenoise/BTY/Din_Apt_BTY.0101.exr", 
                "denoise_BTY": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_envir_Din_Apt_BTY_denoise_BTY_misc_raw.101.exr", 
                "denoise_primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_envir_Din_Apt_BTY_denoise_primary_misc_raw.101.exr", 
                "cpuTime": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt/preDenoise/cpuTime/Din_Apt_cpuTime.0101.exr", 
                "primary": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt/preDenoise/primary/Din_Apt_primary.0101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }, 
        "825_100_r1_char_long_BTY": {
            "frames": "101-256[1]", 
            "aov": {
                "denoiseVariance": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/long/preDenoise/denoiseVariance/beauty_variance.0101.exr", 
                "BTY": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/long/preDenoise/BTY/long_BTY.0101.exr", 
                "denoise_BTY": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_char_long_BTY_denoise_BTY_misc_raw.101.exr", 
                "denoise_primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_char_long_BTY_denoise_primary_misc_raw.101.exr", 
                "cpuTime": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/long/preDenoise/cpuTime/long_cpuTime.0101.exr", 
                "primary": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/long/preDenoise/primary/long_primary.0101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }, 
        "825_100_r1_envir_Din_Apt_MATTE": {
            "frames": "101-103[1]", 
            "aov": {
                "denoiseVariance": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt/preDenoise/denoiseVariance/beauty_variance.0101.exr", 
                "BTY": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt/preDenoise/BTY/Din_Apt_BTY.0101.exr", 
                "denoise_BTY": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_envir_Din_Apt_MATTE_denoise_BTY_misc_raw.101.exr", 
                "denoise_primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_envir_Din_Apt_MATTE_denoise_primary_misc_raw.101.exr", 
                "cpuTime": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt/preDenoise/cpuTime/Din_Apt_cpuTime.0101.exr", 
                "primary": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt/preDenoise/primary/Din_Apt_primary.0101.exr", 
                "MATTE": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt/MATTE/Din_Apt_MATTE.0101.exr", 
                "DATA": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/envir/Din_Apt/DATA/Din_Apt_DATA.0101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }, 
        "825_100_r1_char_din_BTY": {
            "frames": "101-103[1]", 
            "aov": {
                "denoiseVariance": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/din/preDenoise/denoiseVariance/beauty_variance.0101.exr", 
                "BTY": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/din/preDenoise/BTY/din_BTY.0101.exr", 
                "denoise_BTY": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_char_din_BTY_denoise_BTY_misc_raw.101.exr", 
                "denoise_primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_char_din_BTY_denoise_primary_misc_raw.101.exr", 
                "cpuTime": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/din/preDenoise/cpuTime/din_cpuTime.0101.exr", 
                "primary": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/char/din/preDenoise/primary/din_primary.0101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }, 
        "825_100_r1_vol_dinApt_PRIMARY": {
            "frames": "101-103[1]", 
            "aov": {
                "denoise_primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_vol_dinApt_PRIMARY_denoise_primary_misc_raw.101.exr", 
                "primary": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/vol/dinApt/preDenoise/primary/dinApt_primary.0101.exr", 
                "denoiseVariance": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/vol/dinApt/preDenoise/denoiseVariance/beauty_variance.0101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }, 
        "825_100_r1_vol_dinApt_VOL": {
            "frames": "101-103[1]", 
            "aov": {
                "VOL": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/vol/dinApt/preDenoise/VOL/dinApt_VOL.0101.exr", 
                "denoise_VOL": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_vol_dinApt_VOL_denoise_VOL_misc_raw.101.exr", 
                "denoise_primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_vol_dinApt_VOL_denoise_primary_misc_raw.101.exr", 
                "primary": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/vol/dinApt/preDenoise/primary/dinApt_primary.0101.exr", 
                "denoiseVariance": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/vol/dinApt/preDenoise/denoiseVariance/beauty_variance.0101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }, 
        "825_100_r1_vol_dinApt_RGB_VOL": {
            "frames": "101-103[1]", 
            "aov": {
                "VOL": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/vol/dinApt_RGB/preDenoise/VOL/dinApt_RGB_VOL.0101.exr", 
                "denoise_VOL": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_vol_dinApt_RGB_VOL_denoise_VOL_misc_raw.101.exr", 
                "denoise_primary": "/tmp/katana_tmpdir_9670/825_100_scene_825_100_r1_vol_dinApt_RGB_VOL_denoise_primary_misc_raw.101.exr", 
                "primary": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/vol/dinApt_RGB/preDenoise/primary/dinApt_RGB_primary.0101.exr", 
                "denoiseVariance": "/W/WDN/misc/user/tho/825_100/render/lgt/work/images/r1/vol/dinApt_RGB/preDenoise/denoiseVariance/beauty_variance.0101.exr"
            }, 
            "denoise": "0", 
            "renderable": "1"
        }
    }
}

task_info = {
    'input_cg_file': r'/W/WDN/misc/user/tho/825_100/825_100_scene.katana'
    'os_name': '0',  # Linux
}

upload_info = {
  "asset": [
  ]
}

# 4.Submit job
rayvision.submit_job(scene_info_render, task_info, upload_info)

# 5.Download
# rayvision.download(job_id_list=[370271], local_dir=r"d:\project\output")
