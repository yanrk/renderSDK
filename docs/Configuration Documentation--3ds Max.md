3ds Max configuration profile
======

> Analysis: We analyze the information that needed in the scene and save it to task.json, asset.json, upload.json, tips.json for further analysis and processing.
    
    
### 1.task.json analysis


> Description: Store scene analysis results, rendering settings, etc.


**task.json example**


```json
{
    "scene_info_render": {
        "common": {
            "output_file_type": ".tga", 
            "all_camera": [
                "Camera001"
            ], 
            "global_proxy": "false", 
            "output_file_basename": "Renderbus", 
            "element_list": [], 
            "rend_save_file": "false", 
            "element_active": "1", 
            "in_gamma": "2.2", 
            "height": "480", 
            "output_file": "Renderbus.tga", 
            "rend_timeType": "1", 
            "element_type": ".tga", 
            "animation_range": "0-100", 
            "frames": "0", 
            "renderable_camera": [
                "Camera001"
            ], 
            "gamma_val": "2.2", 
            "out_gamma": "2.2", 
            "width": "640", 
            "gamma": "0", 
            "cgv": "undefined"
        }, 
        "renderer": {
            "channel_file": "E:/Workspaces/3dmax/2014/aa.exr", 
            "displacement": "true", 
            "raw_img_name": "", 
            "subdivs": "8", 
            "renderer": "vray", 
            "secbounce": "3", 
            "gi": "0", 
            "light_cache_file": "", 
            "irrmap_file": "", 
            "filter_kernel": "Area", 
            "rend_raw_img_name": "false", 
            "gi_height": "480", 
            "filter_on": "true", 
            "gi_width": "640", 
            "gi_frames": "0", 
            "save_sep_channel": "true", 
            "light_cache_mode": "0", 
            "primary_gi_engine": "0", 
            "renderer_orign": "V_Ray_Adv_3_00_03", 
            "image_sampler_type": "1", 
            "irradiance_map_mode": "0", 
            "secondary_gi_engine": "2", 
            "name": "vray", 
            "vfb": "1", 
            "onlyphoton": "false", 
            "reflection_refraction": "true", 
            "mem_limit": "4000", 
            "default_geometry": "2"
        }
    }, 
    "task_info": {
        "is_layer_rendering": "1", 
        "cg_id": "2001", 
        "ram": "64", 
        "os_name": "1", 
        "render_layer_type": "0", 
        "is_distribute_render": "0", 
        "input_cg_file": "D:/gitlab/renderSDK/scenes/max2014_vray3.00.03.max", 
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
        "task_id": "440111", 
        "task_stop_time": "86400", 
        "time_out": "12"
    }, 
    "software_config": {
        "cg_version": "2014", 
        "cg_name": "3ds Max", 
        "plugins": {
            "vray": "3.00.03"
        }
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
cg_name | string | Software Name | "3ds Max"
cg_version | string | Software Version | "2014"
plugins | object | plugin object. <br>key is the plugin name, value is the plugin version | {"vray":"3.00.03"}


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
common | object | Scene common information | [See scene_info_render.common object](#scene_info_render.common)
renderer | object | Renderer settings information | [See scene_info_render.renderer object](#scene_info_render.renderer)


**<span id="scene_info_render.common">scene_info_render.common object</span>**


Parameters | Type | Description | Examples
---|---|---|---
output_file_type | string | output file type | ".tga"
all_camera | array<string> | all camera list | ["Camera001", "Camera002"]
global_proxy | string | Whether to enable global bitmap proxy | "false"
output_file_basename | string | output file basename | "Renderbus"
element_list | array<string> | element list | ["VRayAlpha","VRayNormals"]
rend_save_file | string | Whether to save the output file | "false"
element_active | string | Whether to enable rendering of rendered elements. 0: not enabled; 1: enabled | "1"
in_gamma | string | input gamma | "2.2"
height | string | Resolution-height | "480"
output_file | string | output file name | "Renderbus.tga"
rend_timeType | string | Rendering type (1. Single frame, 2. By timeline, 3. Custom time range, 4. Custom frame) | "1"
element_type | string | element type | ".tga"
animation_range | string | animation range | "0-100"
frames | string | frames | "0-50[2]"
renderable_camera | array<string> | renderable camera list | ["Camera001"]
gamma_val | string | gamma value | "2.2"
out_gamma | string | output gamma | "2.2"
width | string | Resolution-width | "640"
gamma | string | gamma switch | "0"
cgv | string | CG software version | "2014"



**<span id="scene_info_render.renderer">scene_info_render.renderer object</span>**


Parameters | Type | Description | Examples
---|---|---|---
channel_file | string | Separate render channels path | "E:/Workspaces/3dmax/2014/aa.exr"
displacement | string | vray displacement | "true"
raw_img_name | string | raw image file path | 
subdivs | string | sub divs | "8"
renderer | string | Renderer | "vray"
secbounce | string |  | "3"
gi | string | Global Illumination.0: Close, 1：On | "0"
light_cache_file | string | light cache file path | 
irrmap_file | string | irrmap file path | 
filter_kernel | string | filter kernel. <br/>"Area"<br/>"Sharp Quadratic"<br/>"Catmull-Rom"<br/>"Plate Match/MAX R2"<br/>"Quadratic"<br/>"cubic"<br/>"Video"<br/>"Soften"<br/>"Cook Variable"<br/>"Blend"<br/>"Blackman"<br/>"Mitchell-Netravali"<br/>"VRayLanczosFilter"<br/>"VRaySincFilter"<br/>"VRayBoxFilter"<br/>"VRayTriangleFilter"<br/> | "Area"
rend_raw_img_name | string | Whether to enable V-Ray raw image file | "false"
gi_height | string | gi-height | "480"
filter_on | string | Whether to turn on the anti-aliasing filter | "true"
gi_width | string | gi-width | "640"
gi_frames | string | gi-frames | "0"
save_sep_channel | string | Whether to enable Separate render channels | "true"
light_cache_mode | string | light cache mode. <br/>0：Single frame<br/>1：Fly-through<br/>2：From file<br/>3：Progressive path tracing<br/>| "0"
primary_gi_engine | string | primary gi engine. <br/>0：Irradiance map<br/>1：Photon map<br/>2：Brute force<br/>3：Light cache<br/> | "0"
renderer_orign | string | Renderer origin name | "V_Ray_Adv_3_00_03"
image_sampler_type | string | image sampler type. <br/>0：Fixed<br/>1：Adaptive<br/>2：Adaptive subdivision<br/>3：Progressive<br/> | "1"
irradiance_map_mode | string | irradiance map mode. <br/>0：Single frame<br/>1：Multiframe incremental<br/>2：From file<br/>3：Add to current map<br/>4：Incremental add to current map<br/>5：Bucket mode<br/>6：Animation(prepass)<br/>7：Animation(rendering)<br/> | "0"
secondary_gi_engine | string | secondary gi engine. <br/>0：None<br/>1：Photon map<br/>2：Brute force<br/>3：Light cache<br/> | "2"
name | string | Renderer name | "vray"
vfb | string | Whether to enable vray frame buffer | "1"
onlyphoton | string | false: Render photon and main image, true: Only render photons, do not render the main image | "false"
reflection_refraction | string | reflection/refraction | "true"
mem_limit | string | memory limit | "4000"
default_geometry | string | default geometry.1:Static; 2:Dynamic; 3:Auto | "2"

### 2.upload.json analysis


> Description: Stores the asset path information that needs to be uploaded.


**upload.json example**
```json
{
  "asset": [
    {
      "local": "c:/renderfarm/sdk_test/work/440111/max2014_vray3.00.03.max.7z", 
      "server": "/D/gitlab/renderSDK/scenes/max2014_vray3.00.03.max.7z"
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
local | string | Asset Local Path | "c:/renderfarm/sdk_test/work/440111/max2014_vray3.00.03.max.7z"
server | string | Server-side relative path, generally consistent with local path | "/D/gitlab/renderSDK/scenes/max2014_vray3.00.03.max.7z"


### 3.tips.json analysis


> Description: Stores the analyzed errors and warnings


```json
{}
```
