VR Standalone 配置文件文档
======

> 分析：我们将场景中需要的信息分析出来并保存到task.json, asset.json, upload.json, tips.json中，以便进一步解析和处理
    
    
### 1.task.json解析


> 说明: 存放场景分析结果、渲染设置等信息


**task.json示例**


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


**task.json参数解析**


参数 | 类型 | 说明 | 示例
---|---|---|---
software_config | object | 渲染环境（软件类型、版本和用到的插件等） | [见software_config对象解析](#software_config)
task_info | object | 渲染设置（优先帧、渲染帧数、超时时间等） | [见task_info对象解析](#task_info)
scene_info_render | object | 空对象即可 | {}


**<span id="software_config">software_config对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
cg_name | string | 软件名称 | "VR Standalone"
cg_version | string | 软件版本 | "standalone_vray3.10.03"
plugins | object | 插件对象。<br>key为插件名称，value为插件版本 | {}


**<span id="task_info">task_info对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
is_layer_rendering | string | maya是否开启分层。<br/>"0":关闭<br/>"1":开启<br/> | "1"
cg_id | string | 渲染软件id."2008": VR Standalone | "2008"
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


### 2.upload.json解析


> 说明: 存放需要上传的资产路径信息


**upload.json示例**
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


**upload.json参数解析**


参数 | 类型 | 说明 | 示例
---|---|---|---
asset | object | 需要上传的资产路径信息 | [见asset对象解析](#asset)


**<span id="asset">asset对象解析</span>**


参数 | 类型 | 说明 | 示例
---|---|---|---
local | string | 资产本地路径 | "H:/test2014vr_vraystandaloneaCopy.vrscene"
server | string | 服务器端相对路径，一般与local保持一致 | "/H/test2014vr_vraystandaloneaCopy.vrscene"


### 3.tips.json解析


> 说明: 存放分析出的错误、警告信息


```json
{}
```

