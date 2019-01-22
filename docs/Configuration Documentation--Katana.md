Katana configuration profile
======

> Analysis: We analyze the information that needed in the scene and save it to task.json, asset.json, upload.json, tips.json for further analysis and processing.
    
    
### 1.task.json analysis


> Description: Store scene analysis results, rendering settings, etc.


**task.json example**


```json
{
    "scene_info_render":{
        "rendernodes":{
            "001_005_Render":{
                "frames":"1-1[1]",
                "aov":{
                    "specular":"/w/aovs/specular_1001.exr",
                    "primary":"/w/aovs/beauty_1001.exr",
                    "diffuse":"/w/aovs/diffuse_1001.exr"
                },
                "denoise":"0",
                "renderable":"1"
            },
            "001_005_002_Render":{
                "frames":"10-100[1]",
                "aov":{
                    "specular":"/w/aovs/002_specular_1001.exr",
                    "primary":"/w/aovs/002_beauty_1001.exr",
                    "diffuse":"/w/aovs/002_diffuse_1001.exr"
                },
                "denoise":"0",
                "renderable":"1"
            }
        }
    },
    "task_info":{
        "test_frames":"000",
        "task_stop_time":"86400",
        "frames_per_task":"1",
        "channel":"4",
        "input_project_path":"",
        "task_id":"386182",
        "is_layer_rendering":"1",
        "is_distribute_render":"0",
        "project_name":"dasdd",
        "platform":"2",
        "time_out":"12",
        "tiles_type":"block",
        "tiles":"1",
        "is_picture":"0",
        "user_id":"10001136",
        "project_id":"2380",
        "cg_id":"2016",
        "job_stop_time":"28800",
        "stop_after_test":"2",
        "distribute_render_node":"3",
        "input_cg_file":"/root/chensr/renderSDK/scenes/001_005_test.katana",
        "os_name":"0",
        "render_layer_type":"0"
    },
    "software_config":{
        "plugins":{

        },
        "cg_version":"2.5v3",
        "cg_name":"Katana"
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
cg_name | string | Software Name | "Katana"
cg_version | string | Software Version | "2.5v3"
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
rendernodes | object | Render node information | [see scene_info_render.rendernodes object analysis](#scene_info_render.rendernodes)


**<span id="scene_info_render.rendernodes">scene_info_render.rendernodes object analysis</span>**


Parameters | Type | Description | Examples
---|---|---|---
rendernodes | object | All node information, the key is the specific node name, and the value is the specific node information. | [See scene_info_render.rendernodes.rendernode object analysis](#scene_info_render.rendernodes.rendernode)


**<span id="scene_info_render.rendernodes.rendernode">scene_info_render.rendernodes.rendernode object analysis</span>**


Parameters | Type | Description | Examples
---|---|---|---
Frames | string | The rendered frame of the node. <br>"1-200[1]" means the starting frame is 1, the ending frame is 200, and the frame interval is 1; <br>"1,7,11,100" means the rendering frames are the first, seventh, eleventh, and 100th frame| "1-200[1]"
Aov | object | aov information.<br>key is aov name, value is aov output path. | {"specular": "/w/aovs/specular_1001.exr","diffuse": "/w/aovs/diffuse_1001. Exr"}
Denoise | string | Whether to generate additional tasks to deoise the current sequence, not supported at this time, the default value is 0 | "0"
Renderable | string | Whether to render the current node, the default value is 1 |


### 2.upload.json analysis


> Description: Stores the asset path information that needs to be uploaded.


**upload.json example**
```json
{
    "asset": [
        {
            "server": "/root/chensr/renderSDK/scenes/001_005_test.katana",
            "local": "/root/chensr/renderSDK/scenes/001_005_test.katana"
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
local | string | Asset Local Path | "/root/chensr/renderSDK/scenes/001_005_test.katana"
server | string | Server-side relative path, generally consistent with local path | "/root/chensr/renderSDK/scenes/001_005_test.katana"


### 3.tips.json analysis


> Description: Stores the analyzed errors and warnings


```json
{}
```
