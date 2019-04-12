Katana 配置文件文档
======

> 分析：我们将场景中需要的信息分析出来并保存到task.json, asset.json, upload.json, tips.json中，以便进一步解析和处理
    
    
### 1.task.json解析


> 说明: 存放场景分析结果、渲染设置等信息


**task.json示例**


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


**task.json参数解析**


参数 | 类型 | 说明 | 示例
---|---|---|---
software_config | object | 渲染环境（软件类型、版本和用到的插件等） | [见software_config对象解析](#software_config)
task_info | object | 渲染设置（优先帧、渲染帧数、超时时间等） | [见task_info对象解析](#task_info)
scene_info_render | object | 场景的分析结果（场景中的渲染节点、输出路径等） | [见scene_info_render对象解析](#scene_info_render)


**<span id="software_config">software_config对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
cg_name | string | 软件名称 | "Katana"
cg_version | string | 软件版本 | "2.5v3"
plugins | object | 插件对象。<br>key为插件名称，value为插件版本 | {}


**<span id="task_info">task_info对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
is_layer_rendering | string | maya是否开启分层。<br/>"0":关闭<br/>"1":开启<br/> | "1"
cg_id | string | 渲染软件id."2016": 3ds Max | "2016"
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
rendernodes | object | 渲染节点信息 | [见scene_info_render.rendernodes对象解析](#scene_info_render.rendernodes)


**<span id="scene_info_render.rendernodes">scene_info_render.rendernodes对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
rendernodes | object | 所有节点信息，key为具体节点名，value为具体节点信息 | [见scene_info_render.rendernodes.rendernode对象解析](#scene_info_render.rendernodes.rendernode)


**<span id="scene_info_render.rendernodes.rendernode">scene_info_render.rendernodes.rendernode对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
frames | string | 节点的渲染帧。<br>"1-200[1]"表示起始帧为1，结束帧为200，帧间隔为1；<br>"1,7,11,100"表示渲染第1、7、11、100帧 | "1-200[1]"
aov | object | aov信息.<br>key为aov name, value为aov output path. | {"specular": "/w/aovs/specular_1001.exr","diffuse": "/w/aovs/diffuse_1001.exr"}
denoise | string | 是否生成额外的任务对当前序列做denoise，暂不支持，默认值为0 | "0"
renderable | string | 是否渲染当前节点，默认值为1 |


### 2.upload.json解析


> 说明: 存放需要上传的资产路径信息


**upload.json示例**
```json
{
    "asset": [
        {
            "local": "/root/chensr/renderSDK/scenes/001_005_test.katana",
            "server": "/root/chensr/renderSDK/scenes/001_005_test.katana"
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
local | string | 资产本地路径 | "/root/chensr/renderSDK/scenes/001_005_test.katana"
server | string | 服务器端相对路径，一般与local保持一致 | "/root/chensr/renderSDK/scenes/001_005_test.katana"


### 3.tips.json解析


> 说明: 存放分析出的错误、警告信息


```json
{}
```

