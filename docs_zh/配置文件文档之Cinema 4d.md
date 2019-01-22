Cinema 4D 配置文件文档
======

> 分析：我们将场景中需要的信息分析出来并保存到task.json, asset.json, upload.json, tips.json中，以便进一步解析和处理
    
    
### 1.task.json解析


> 说明: 存放场景分析结果、渲染设置等信息


**task.json示例**


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


**task.json参数解析**


参数 | 类型 | 说明 | 示例
---|---|---|---
software_config | object | 渲染环境（软件类型、版本和用到的插件等） | [见software_config对象解析](#software_config)
task_info | object | 渲染设置（优先帧、渲染帧数、超时时间等） | [见task_info对象解析](#task_info)
scene_info_render | object | 场景的分析结果（场景中的渲染节点、输出路径等） | [见scene_info_render对象解析](#scene_info_render)


**<span id="software_config">software_config对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
cg_name | string | 软件名称 | "Cinema 4D"
cg_version | string | 软件版本 | "R19"
plugins | object | 插件对象。<br>key为插件名称，value为插件版本 | {"VrayBridge":"3.26"}


**<span id="task_info">task_info对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
is_layer_rendering | string | maya是否开启分层。<br/>"0":关闭<br/>"1":开启<br/> | "1"
cg_id | string | 渲染软件id."2005": Cinema 4D | "2005"
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


**<span id="scene_info_render">scene_info_render对象</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
renderer | object | 渲染器设置信息 | "renderer":{<br>"name": "Physical",<br>"physical_sampler_mode": "Infinite",<br>"physical_sampler": "Adaptive"}
common | object | 场景普通信息 | "frames": "0-50[1]",<br>"multipass_saveonefile": "1",<br>"fps": "30",<br>"multipass_save_enabled": "1",<br>"frame_rate": "30"}

**<span id="scene_info_render">scene_info_render.renderer对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
name | string | 渲染器名字："VrayBridge"<br>"standard"<br>"physical" | "standard"
physical_sampler | dict | 当渲染器是physical的时候的模式<br> 0:'Fixed',1:'Adaptive',2:'Progressive' | {"physical_sampler":"Progressive"}
physical_sampler_mode | dict | 对应上面3个模式的3个类型，选择infinite时会进入报错提醒<br>0:'Infinite',1:'Pass Count',2:'Time Limit'	 | {"physical_sampler_mode":"Infinite"}

**<span id="scene_info_render">scene_info_render.common对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
regular_image_format | string | 主图输出格式(默认显示的输出格式) | "regular_image_format": "PNG"
multi_pass_format | string | 通道输出格式 | "multi_pass_format": "OpenEXR"
multipass_save_enabled | string | 	通道输出开关（开为1，关为0） | "multipass_save_enabled":"1"
all_camera | list | 场景中的所有相机 | ["Camera"，"Camera1"，"Camera2"]
multi_pass | dict |  场景中的通道 | {"Ambient Occlusion": [],<br>"Material Normal": [], <br>"Material Diffusion": [], <br>"Material Luminance": [], <br>"Material Color": [], <br>"Material Specular Color": []}
frames | string | 起始帧，隔帧 |  "frames":"40-40[1]"
width | string | 宽 | "1203"
height | string | 高 | "34242"
c4d_version | string | c4d版本 | "c4d_version":18048
created_version | string | 创建版本 | "created_version":"MAXON CINEMA 4D Studio (RC - R19) 19.024"
saved_version | string | 保存版本 | 	"saved_version":"MAXON CINEMA 4D Studio (RC - R18) 18.011"
regular_image_saveimage_path | string | 即主图输出名（(默认显示的输出文件名） | "regular_image_saveimage_path": "'D:\\ffffff'"
multipass_saveimage_path | string | 即通道输出名 | "multipass_saveimage_path": "'D:\\ffffff'"


### 2.upload.json解析


> 说明: 存放需要上传的资产路径信息


**upload.json示例**
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


**upload.json参数解析**


参数 | 类型 | 说明 | 示例
---|---|---|---
asset | object | 需要上传的资产路径信息 | [见asset对象解析](#asset)


**<span id="asset">asset对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
local | string | 资产本地路径 | "c:/render/scenes/001_005_test.c4d"
server | string | 服务器端相对路径，一般与local保持一致 | "/c/render/scenes/001_005_test.c4d"


### 3.tips.json解析


> 说明: 存放分析出的错误、警告信息


```json
{}
```
