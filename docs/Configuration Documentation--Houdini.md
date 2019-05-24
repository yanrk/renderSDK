Houdini configuration profile
======

> Analysis: We analyze the information that needed in the scene and save it to task.json, asset.json, upload.json, tips.json for further analysis and processing.
    
    
### 1.task.json analysis


> Description: Store scene analysis results, rendering settings, etc.


**task.json example**


```json
{
    "scene_info_render": {
        "rop_node": [
            {
                "node": "/out/mantra1", 
                "frames": "1-10[1]", 
                "option": "-1", 
                "render": "1"
            }
        ], 
        "geo_node": []
    }, 
    "task_info": {
        "is_layer_rendering": "1", 
        "cg_id": "2004", 
        "ram": "64", 
        "os_name": "1", 
        "render_layer_type": "0", 
        "is_distribute_render": "0", 
        "input_cg_file": "D:/gitlab/renderSDK/scenes/houdini_test/sphere.hip", 
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
        "task_id": "440149", 
        "task_stop_time": "86400", 
        "time_out": "12"
    },  
    "software_config": {
        "cg_version": "16.5.268", 
        "cg_name": "Houdini", 
        "plugins": {}
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
cg_name | string | Software Name | "Houdini"
cg_version | string | Software Version | "16.5.268"
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


**<span id="scene_info_render">scene_info_render object analysis</span>**


Parameters | Type | Description | Examples
---|---|---|---
rop_node | object | rop node | 
geo_node | object | geo node | 


**<span id="scene_info_render.rop_node">scene_info_render.rop_node and geo_node object</span>**


Parameters | Type | Description | Examples
---|---|---|---
node | string | rop / geo node path | "/out/mantra1"
frames | string | rop / frames | "1-10[1]"
option | string | rop / -1: rop; other: geo, and the value is the number of machines settled. | "-1"
render | string | rop / Whether to activate rendering. 1 is to render (solve) the node, 0 is the node does not participate in rendering (solving) | "1"

### 2.upload.json analysis


> Description: Stores the asset path information that needs to be uploaded.


**upload.json example**
```json
{
  "asset": [
    {
      "local": "D:/gitlab/renderSDK/scenes/houdini_test/sphere.hip", 
      "server": "/D/gitlab/renderSDK/scenes/houdini_test/sphere.hip"
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
local | string | Asset Local Path | "D:/gitlab/renderSDK/scenes/houdini_test/sphere.hip"
server | string | Server-side relative path, generally consistent with local path | "/D/gitlab/renderSDK/scenes/houdini_test/sphere.hip"


### 3.tips.json analysis


> Description: Stores the analyzed errors and warnings


```json
{}
```
