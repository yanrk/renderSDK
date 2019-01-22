# 渲染SDK

[README of English](README.md)


## 概览

    我们开放一个简单的Python渲染SDK来更方便地使用我们的云渲染服务；
    这个官方渲染SDK由 FOXRenderfarm / RENDERBUS 的 RD和TD 团队一起维护开发；
    这个渲染SDK在 python2.7.10 and python3.4.4 下测试通过。
    
    
## 为什么要使用渲染SDK

    1. 自动化。SDK将使用云渲染服务的流程（分析场景、上传资产、渲染、下载）全部自动化。且可嵌入到客户自身的调度中（如DeadLine、Qube等）
    2. 开源。用户可自定义开发或提交开发建议
    3. 跨版本。支持python2和python3
    4. 跨平台。支持Windows和Linux
    5. 安全性高。使用动态签名算法认证（HmacSHA256 + Base64 + UTC时间戳限时认证 + 随机数防止重放攻击），更安全
    6. 提供多种使用方式。支持本地分析和不本地分析
    7. 独立性好。将API与业务逻辑独立开来，易扩展
    8. 有详细文档
    
    
## 支持的软件

- [x] Maya
- [x] 3ds Max
- [x] Houdini
- [x] Katana
- [x] Cinema 4d
- [x] VR Standalone


## 准备工作

1. 您需要一个 [RENDERBUS](https://task.renderbus.com) 账号
2. 您还需要在 [RENDERBUS 开发者中心](https://task.renderbus.com/user/developer) 申请使用渲染SDK，并获取AccessID和AccessKey


## 下载SDK

```bash
git clone https://github.com/renderbus/renderSDK.git
```

or

[直接下载](https://github.com/renderbus/renderSDK/archive/master.zip)


## 开始使用

> 该SDK有两种使用方法：使用本地分析 和 不使用本地分析

1. 使用本地分析

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
示例代码一：使用本地分析
"""

import sys

# 将源代码目录（renderSDK目录）的路径加到python的搜索模块的路径集
renderSDK_path = r'<Your renderSDK location>'
sys.path.append(renderSDK_path)

from renderSDK.Rayvision import Rayvision

# 1.登录
rayvision = Rayvision(domain_name='task.renderbus.com', platform='2', access_id='<Your AccessID>', access_key='<Your AccessKey>', workspace='<SDK workspace: The path to save job information and logs>')

# 2.设置渲染环境（配置插件、标签名等）
job_id = rayvision.set_render_env(cg_name='Maya', cg_version='2016', plugin_config={"mtoa": "3.0.1.1"}, label_name='label_name')

# 3.本地分析
scene_info_render, task_info = rayvision.analyse(cg_file=r'<Your scene file path>')

# 4. 用户自行处理错误、警告
error_info_list = rayvision.check_error_warn_info()

# 5.用户修改参数列表（可选），并提交作业
rayvision.submit_job(scene_info_render, task_info)

# 6.自动下载
rayvision.auto_download(job_id_list=[job_id], local_dir=r"<Your output path>")
# rayvision.auto_download_after_job_completed(job_id_list=[job_id], local_dir=r"<Your output path>")

```

2. 不使用本地分析

```python
#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
示例代码二：不使用本地分析
"""

import sys

# 将源代码目录（renderSDK目录）的路径加到python的搜索模块的路径集
renderSDK_path = r'<Your renderSDK location>'
sys.path.append(renderSDK_path)

from renderSDK.Rayvision import Rayvision

# 1.登录
rayvision = Rayvision(domain_name='task.renderbus.com', platform='2', access_id='<Your AccessID>', access_key='<Your AccessKey>', workspace='<SDK workspace: The path to save job information and logs>')

# 2.设置渲染环境（配置插件、标签名等）
job_id = rayvision.set_render_env(cg_name='Maya', cg_version='2016', plugin_config={"mtoa": "3.0.1.1"}, label_name='label_name')

# 3.设置参数（参见docs_zh目录中的软件配置文件文档）
scene_info_render = {}
task_info = {}
upload_info = {}

# 4.提交作业
rayvision.submit_job(scene_info_render, task_info, upload_info)

# 5.自动下载
rayvision.auto_download(job_id_list=[job_id], local_dir=r"<Your output path>")
# rayvision.auto_download_after_job_completed(job_id_list=[job_id], local_dir=r"<Your output path>")

```


## 更多使用
- [更多示例程序](demos)
- [更多详细文档](docs_zh)
- [SDK使用文档](docs_zh/SDK使用文档.md)
- [API参考](docs_zh/瑞云渲染APIV4.0.pdf)


## 目录结构描述

- [demos](demos): 示例程序
- [docs](docs): 英文文档
- [docs_zh](docs_zh): 中文文档
- [image](image): 文档中所引用的图片
- [renderSDK](renderSDK): 源代码
- [scenes](scenes): 测试场景


## 其他

> - Windows支持: Maya, Houdini, 3ds Max, Cinema 4d, VR Standalone
> - Linux支持: Maya, Houdini, Katana

> - 支持中文: 3ds Max
> - 不支持中文: Maya, Houdini, Katana, Cinema 4d, VR Standalone> 


## 更新日志

[CHANGELOG.md](CHANGELOG.md)


## 许可证

[Apache License 2.0](https://github.com/renderbus/renderSDK/blob/master/LICENSE).
