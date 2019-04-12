VR Standalone configuration profile
======

> Analysis: We analyze the information that needed in the scene and save it to task.json, asset.json, upload.json, tips.json for further analysis and processing.
    
    
### 1.task.json analysis


> Description: Store scene analysis results, rendering settings, etc.


**task.json example**


```json
{
    "scene_info_render": {}, 
    "task_info": {
        "is_layer_rendering": "1", 
        "cg_id": "2008", 
        "ram": "64", 
        "os_name": "1", 
        "render_layer_type": "0", 
        "is_distribute_render": "1", 
        "input_cg_file": "H:\\test2014vr_vraystandaloneaCopy.vrscene", 
        "job_stop_time": "28800", 
        "user_id": "10000031", 
        "pre_frames": "000", 
        "platform": "2", 
        "is_picture": "0", 
        "project_id": "3316", 
        "channel": "4", 
        "tiles_type": "block", 
        "tiles": "1", 
        "project_name": "dasdd", 
        "distribute_render_node": "3", 
        "frames_per_task": "1", 
        "stop_after_test": "2", 
        "input_project_path": "", 
        "task_id": "440194", 
        "task_stop_time": "86400", 
        "time_out": "12"
    },
    "software_config": {
        "cg_version": "standalone_vray3.10.03", 
        "cg_name": "VR Standalone", 
        "plugins": {}
    }
}
```


**task.json parameter analysis**


Parameters | Type | Description | Examples
---|---|---|---
software_config | object | rendering environment (software type, version, and plugins used, etc.) | [see software_config object](#software_config)
task_info | object | Rendering settings (priority frame, number of rendered frames, timeout, etc.) | [see task_info object](#task_info)
scene_info_render | object | empty object | {}


**<span id="software_config">software_config object analysis</span>**


Parameters | Type | Description | Examples
---|---|---|---
cg_name | string | Software Name | "VR Standalone"
cg_version | string | Software Version | "standalone_vray3.10.03"
plugins | object | plugin object. <br>key is the plugin name, value is the plugin version | {}


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


### 2.upload.json analysis


> Description: Stores the asset path information that needs to be uploaded.


**upload.json example**
```json
{
    "asset": [
        {
            "local": "H:/test2014vr_vraystandaloneaCopy.vrscene", 
            "server": "/H/test2014vr_vraystandaloneaCopy.vrscene"
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
local | string | Asset Local Path | "H:/test2014vr_vraystandaloneaCopy.vrscene"
server | string | Server-side relative path, generally consistent with local path | "/H/test2014vr_vraystandaloneaCopy.vrscene"


### 3.tips.json analysis


> Description: Stores the analyzed errors and warnings


```json
{}
```
