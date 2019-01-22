Cinema 4D configuration profile
======

> Analysis: We analyze the information that needed in the scene and save it to task.json, asset.json, upload.json, tips.json for further analysis and processing.
    
    
### 1.task.json analysis


> Description: Store scene analysis results, rendering settings, etc.


**task.json example**


```json
{
    "scene_info_render":{
        "renderer": {
            "name": "Physical",
            "physical_sampler_mode": "Infinite",
            "physical_sampler": "Adaptive"
        }
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
    },
    "task_info":{
        "input_cg_file": "C:\test_c4d\test_c4d.c4d",
        "is_picture": "0",
        "frames_per_task": "1",
        "pre_frames": "000",
        "job_stop_time": "28800",
        "task_stop_time": "86400",
        "time_out": "12",
        "stop_after_test": "2",
        "channel": "4",
        "task_id": "job_id",
        "os_name": "1",
        "ram": "64"

    },
    "software_config":{
        "plugins":{

        },
        "cg_version":"R16",
        "cg_name":"Cinema 4D"
    }
}
```


**task.json parameter analysis**


Parameters | Type | Description | Examples
---|---|---|---
software_config | object | rendering environment (software type, version, and plugins used, etc.) | [see software_config object](#software_config)
task_info | object | Rendering settings (priority frame, number of rendered frames, timeout, etc.) | [see task_info object](#task_info)
scene_info_render | object | Analysis result of the scene (render nodes, output paths, etc. in the scene) | [see scene_info_render object](#scene_info_render)


**<span id="software_config">software_config object analysis</span>**


Parameters | Type | Description | Examples
---|---|---|---
cg_name | string | Software Name | "Cinema 4D"
cg_version | string | Software Version | "R19"
plugins | object | plugin object. <br>key is the plugin name, value is the plugin version | {"VrayBridge":"3.26"}


**<span id="task_info">task_info object analysis</span>**


Parameters | Type | Description | Examples
---|---|---|---
is_layer_rendering | string | Whether maya enables layered rendering.<br/>"0":Close<br/>"1":On<br/> | "1"
cg_id | string | Render software id."2016": Katana | "2016"
ram | string | Rendering machine memory requirements. 64/128 GB| "64"
os_name | string | Rendering operating system, "0":Linux; "1": Windows | "0"
render_layer_type | string | Render layer mode. <br/>"0": renderlayer<br/>"1": rendersetup | "0"
is_distribute_render | string | Whether to enable distributed rendering. <br/>"0":Close<br/>"1":On | "0"
input_cg_file | string | Render scene local path | 
job_stop_time | string | Minor task stops due to timeout, unit: second | "28800"
user_id | string | User id | 
pre_frames | string | Priority rendering | "000:1,3-4[1]" means: <br/>Priority rendering of the first frame: No<br/>Priority rendering of the middle frame: No<br/>Priority rendering of the last frame: No<br/>Priority rendering of the custome frame: 1,3-4[1]
platform | string | Submit platform | "2"
is_picture | string | Is picture | "0"
project_id | string | Project id | 
channel | string | Submission channel. "4":API/SDK | "4"
tiles_type | string | block/strip | "block"
tiles | string | The number of blocks, greater than 1 is divided into blocks or strips, equal to 1 is a single machine | "1"
project_name | string | Project name | "test"
distribute_render_node | string | Distributed rendering machine number | "3"
frames_per_task | string | The quantity of the frames that rendered in one machine| "1"
stop_after_test | string | Whether to pause the task after the priority rendering is completed <br/>"1":Pause the task after the priority rendering is completed<br/>"2". Do not pause the task after the priority rendering is completed.
input_project_path | string | Project path, such as user does not set a null string passing| 
task_id | string | Task id | 
task_stop_time | string | major task stops due to timeout  unit: second | "86400"
time_out | string | Timeout period unit:hour | "12"


**<span id="scene_info_render">scene_info_render object analysis</span>**


Parameters | Type | Description | Examples
---|---|---|---
renderer | object | Renderer settings information | "renderer":{<br>"name": "Physical",<br>"physical_sampler_mode": "Infinite",<br>"physical_sampler": "Adaptive"}
common | object | Scene common information | "frames": "0-50[1]",<br>"multipass_saveonefile": "1",<br>"fps": "30",<br>"multipass_save_enabled": "1",<br>"frame_rate": "30"}

**<span id="scene_info_render">scene_info_render.renderer object</span>**


Parameters | Type | Description | Examples
---|---|---|---
name | string | Renderer name: "VrayBridge"<br>"standard"<br>"physical" | "standard"
physical_sampler | dict | The mode when the renderer is physical<br> 0:'Fixed',1:'Adaptive',2:'Progressive' | {"physical_sampler":"Progressive"}
physical_sampler_mode | dict | 
Corresponding to the 3 types of the above 3 modes, when you select infinite, you will get an error notification.<br>0:'Infinite',1:'Pass Count',2:'Time Limit'	 | {"physical_sampler_mode":"Infinite"}

**<span id="scene_info_render">scene_info_render.common object</span>**


Parameters | Type | Description | Examples
---|---|---|---
regular_image_format | string | Main image output format (default output format) | "regular_image_format": "PNG"
multi_pass_format | string |  | "multi_pass_format": "OpenEXR"
multipass_save_enabled | string | 1: On, 0: Close | "multipass_save_enabled":"1"
all_camera | list | all camera list | ["Camera"，"Camera1"，"Camera2"]
multi_pass | dict |  | {"Ambient Occlusion": [],<br>"Material Normal": [], <br>"Material Diffusion": [], <br>"Material Luminance": [], <br>"Material Color": [], <br>"Material Specular Color": []}
frames | string | frames | "40-40[1]"
width | string | Resolution-width | "1203"
height | string | Resolution-height | "34242"
c4d_version | string | Cinema 4d software version | "18048"
created_version | string | created version | "created_version":"MAXON CINEMA 4D Studio (RC - R19) 19.024"
saved_version | string | saved version | "saved_version":"MAXON CINEMA 4D Studio (RC - R18) 18.011"
regular_image_saveimage_path | string | Main image output path (default output path) | "regular_image_saveimage_path": "'D:\\ffffff'"
multipass_saveimage_path | string |  | "multipass_saveimage_path": "'D:\\ffffff'"


### 2.upload.json analysis


> Description: Stores the asset path information that needs to be uploaded.


**upload.json example**
```json
{
    "asset": [
        {
            "server": "c:/chensr/render/scenes/001_005_test.c4d",
            "local": "/c/chensr/render/scenes/001_005_test.c4d"
        }
    ]
}
```


**upload.json parameter analysis**


Parameters | Type | Description | Examples
---|---|---|---
asset | object | The asset path information that needed to be uploaded | [See asset object analysis](#asset)


**<span id="asset">asset object analysis</span>**


Parameters | Type | Description | Examples
---|---|---|---
local | string | Asset Local Path | "c:/render/scenes/001_005_test.c4d"
server | string | Server-side relative path, generally consistent with local path | "/c/render/scenes/001_005_test.c4d"


### 3.tips.json analysis


> Description: Stores the analyzed errors and warnings


```json
{}
```
