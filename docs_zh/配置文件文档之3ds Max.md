3ds Max 配置文件文档
======

> 分析：我们将场景中需要的信息分析出来并保存到task.json, asset.json, upload.json, tips.json中，以便进一步解析和处理
    
    
### 1.task.json解析


> 说明: 存放场景分析结果、渲染设置等信息


**task.json示例**


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


**task.json参数解析**


参数 | 类型 | 说明 | 示例
---|---|---|---
software_config | object | 渲染环境（软件类型、版本和用到的插件等） | [见software_config对象解析](#software_config)
task_info | object | 渲染设置（优先帧、渲染帧数、超时时间等） | [见task_info对象解析](#task_info)
scene_info_render | object | 场景的分析结果（场景中的渲染节点、输出路径等） | [见scene_info_render对象解析](#scene_info_render)


**<span id="software_config">software_config对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
cg_name | string | 软件名称 | "3ds Max"
cg_version | string | 软件版本 | "2014"
plugins | object | 插件对象。<br>key为插件名称，value为插件版本 | {"vray":"3.00.03"}


**<span id="task_info">task_info对象部分解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
is_layer_rendering | string | maya是否开启分层。<br/>"0":关闭<br/>"1":开启<br/> | "1"
cg_id | string | 渲染软件id."2001": 3ds Max | "2001"
ram | string | 内存要求。64/128 | "64"
os_name | string | 渲染操作系统, "0":Linux; "1": Windows | "0"
render_layer_type | string | 渲染层方式选择。<br/>"0"：renderlayer方式<br/>"1"：rendersetup方式 | "0"
is_distribute_render | string | 是否开启分布式渲染。<br/>"0":关闭<br/>"1":开启 | "0"
input_cg_file | string | 渲染场景本地路径 | 
job_stop_time | string | 小任务超时停止, 单位秒 | "28800"
user_id | string | 用户ID | 
pre_frames | string | 优先渲染 | "000:1,3-4[1]" 表示：<br>优先渲染首帧：否<br>优先渲染中间帧：否<br>优先渲染末帧：否<br>优先渲染自定义帧：1,3-4[1]
platform | string | 提交平台 | "2"
is_picture | string | 是否效果图 | "0"
project_id | string | 项目id | 
channel | string | 提交方式。"4":API/SDK提交 | "4"
tiles_type | string | "block(分块),strip(分条)" | "block"
tiles | string | 分块数量，大于1就分块或者分条，等于1 就是单机 | "1"
project_name | string | 项目名称 | "test"
distribute_render_node | string | 分布式渲染机器数 | "3"
frames_per_task | string | 一机渲多帧的帧数量 | "1"
stop_after_test | string | 优先渲染完成后是否暂停任务<br>"1":优先渲染完成后暂停任务<br>"2".优先渲染完成后不暂停任务 |
input_project_path | string | 项目路径，如用户未设置传空字符串 |
task_id | string | 任务号 | 
task_stop_time | string | 大任务超时停止 单位秒 | "86400"
time_out | string | 超时时间 单位小时 | "12"



**<span id="scene_info_render">scene_info_render对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
common | object | 场景普通信息 | [见scene_info_render.common对象解析](#scene_info_render.common)
renderer | object | 渲染器设置信息 | [见scene_info_render.renderer对象解析](#scene_info_render.renderer)


**<span id="scene_info_render.common">scene_info_render.common对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
output_file_type | string | 输出文件类型 | ".tga"
all_camera | array<string> | 所有相机列表 | ["Camera001", "Camera002"]
global_proxy | string | 是否启用全局位图代理 | "false"
output_file_basename | string | 输出文件名，不带后缀 | "Renderbus"
element_list | array<string> | 渲染元素列表 | ["VRayAlpha","VRayNormals"]
rend_save_file | string | 渲染保存出图文件 | "false"
element_active | string | 是否启用渲染元素渲染. 0：不启用; 1：启用 | "1"
in_gamma | string | 输入gamma | "2.2"
height | string | 分辨率，高 | "480"
output_file | string | 输出文件名 | "Renderbus.tga"
rend_timeType | string | 渲染类型（1.单帧，2.按时间线，3.自定义时间范围，4.自定义帧） | "1"
element_type | string | 渲染元素输出文件类型 | ".tga"
animation_range | string | 动画帧范围 | "0-100"
frames | string | 帧范围 | "0-50[2]"
renderable_camera | array<string> | 待渲染相机列表 | ["Camera001"]
gamma_val | string | gamma值 | "2.2"
out_gamma | string | 输出gamma | "2.2"
width | string | 分辨率，宽 | "640"
gamma | string | gamma开关 | "0"
cgv | string | CG软件版本 | "2014"



**<span id="scene_info_render.renderer">scene_info_render.renderer对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
channel_file | string | Separate render channels路径 | "E:/Workspaces/3dmax/2014/aa.exr"
displacement | string | vray转换 | "true"
raw_img_name | string | raw image file路径 | 
subdivs | string | 细分 | "8"
renderer | string | 渲染器 | "vray"
secbounce | string |  | "3"
gi | string | 是否开启全局光照。0：关; 1：开 | "0"
light_cache_file | string | 光缓存文件路径 | 
irrmap_file | string | 发光贴图文件路径 | 
filter_kernel | string | 抗锯齿过滤器。<br/>"Area"<br/>"Sharp Quadratic"<br/>"Catmull-Rom"<br/>"Plate Match/MAX R2"<br/>"Quadratic"<br/>"cubic"<br/>"Video"<br/>"Soften"<br/>"Cook Variable"<br/>"Blend"<br/>"Blackman"<br/>"Mitchell-Netravali"<br/>"VRayLanczosFilter"<br/>"VRaySincFilter"<br/>"VRayBoxFilter"<br/>"VRayTriangleFilter"<br/> | "Area"
rend_raw_img_name | string | 是否启用 V-Ray raw image file | "false"
gi_height | string | 渲染发光贴图宽 | "480"
filter_on | string | 是否开启抗锯齿过滤器 | "true"
gi_width | string | 渲染发光贴图宽 | "640"
gi_frames | string | 渲染发光贴图帧数 | "0"
save_sep_channel | string | 是否启用Separate render channels | "true"
light_cache_mode | string | 灯光缓存模式。<br/>0：Single frame<br/>1：Fly-through<br/>2：From file<br/>3：Progressive path tracing<br/>| "0"
primary_gi_engine | string | 首次引擎。<br/>0：Irradiance map<br/>1：Photon map<br/>2：Brute force<br/>3：Light cache<br/> | "0"
renderer_orign | string | 渲染器原始名 | "V_Ray_Adv_3_00_03"
image_sampler_type | string | 图片采样器（抗锯齿）类型。<br/>0：Fixed<br/>1：Adaptive<br/>2：Adaptive subdivision<br/>3：Progressive<br/> | "1"
irradiance_map_mode | string | 发光贴图模式。<br/>0：Single frame<br/>1：Multiframe incremental<br/>2：From file<br/>3：Add to current map<br/>4：Incremental add to current map<br/>5：Bucket mode<br/>6：Animation(prepass)<br/>7：Animation(rendering)<br/> | "0"
secondary_gi_engine | string | 二次引擎。<br/>0：None<br/>1：Photon map<br/>2：Brute force<br/>3：Light cache<br/> | "2"
name | string | 渲染器名称 | "vray"
vfb | string | 是否启用vray frame buffer | "1"
onlyphoton | string | false：不启用只渲染光子；true：启用只渲染光子 | "false"
reflection_refraction | string | 反射/折射 | "true"
mem_limit | string | 内存限制 | "4000"
default_geometry | string | 默认几何体。1:Static; 2:Dynamic; 3:Auto | "2"



### 2.upload.json解析


> 说明: 存放需要上传的资产路径信息


**upload.json示例**
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


**upload.json参数解析**


参数 | 类型 | 说明 | 示例
---|---|---|---
asset | object | 需要上传的资产路径信息 | [见asset对象解析](#asset)


**<span id="asset">asset对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
local | string | 资产本地路径 | "c:/renderfarm/sdk_test/work/440111/max2014_vray3.00.03.max.7z"
server | string | 服务器端相对路径，一般与local保持一致 | "/D/gitlab/renderSDK/scenes/max2014_vray3.00.03.max.7z"


### 3.tips.json解析


> 说明: 存放分析出的错误、警告信息


```json
{}
```

